"""Verify the transcription ledger against the raw filed-accounts PDFs, and build processed data.

Each Companies House PDF is a stack of 300 dpi bilevel page images (no text layer). For every
ledger row we extract the cited page image (lossless, via `pdfimages`), OCR it with Tesseract
and check that the transcribed number appears on that page. Raw OCR is not used as the value
source: it misreads separators ("19;790") and is only a second, independent read of the page.

Outputs
- data/processed/verification.csv   one row per ledger figure with its check status
- data/processed/financials.csv     each fiscal year as reported in its own filing
- data/processed/discrepancies.csv  comparatives that differ from the originally reported figure
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from . import ledger, paths

PSM_MODES = ("6", "4", "11")  # uniform block, single column, sparse text
_SEP = r"[,.;:'’`]?\s?"  # thousands separators as OCR renders them, with an optional stray space


def _tool(name: str) -> str:
    exe = shutil.which(name)
    if exe is None:
        raise RuntimeError(f"`{name}` not found: install poppler-utils and tesseract-ocr")
    return exe


def page_image(pdf: Path, page: int, workdir: Path) -> Path:
    """Extract the embedded page image (1-based page number) losslessly."""
    prefix = workdir / f"{pdf.stem}_p{page:03d}"
    subprocess.run([_tool("pdfimages"), "-f", str(page), "-l", str(page), "-png", str(pdf), str(prefix)],
                   check=True, capture_output=True)
    images = sorted(workdir.glob(f"{prefix.name}-*.png"))
    if len(images) != 1:
        raise RuntimeError(f"{pdf.name} p.{page}: expected one page image, found {len(images)}")
    return images[0]


def ocr_page(pdf: Path, page: int, psm: str = "6") -> str:
    """OCR text of one page, cached under data/interim/ocr keyed by PDF hash."""
    paths.OCR_CACHE.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]
    cache = paths.OCR_CACHE / f"{pdf.stem}_{digest}_p{page:03d}_psm{psm}.txt"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        img = page_image(pdf, page, Path(tmp))
        env = {**os.environ, "OMP_THREAD_LIMIT": "1"}  # one thread per page; pages run in parallel
        out = subprocess.run([_tool("tesseract"), str(img), "stdout", "--psm", psm],
                             check=True, capture_output=True, text=True, env=env).stdout
    cache.write_text(out, encoding="utf-8")
    return out


def number_pattern(value: float) -> re.Pattern:
    """Regex matching `value` as printed in the accounts, tolerant of OCR separator noise.

    Integers are matched digit-group by digit-group ("19,790" also matches "19;790" and
    "19, 790"); the match may not be glued to further digits. Signs and brackets are ignored
    because the accounts show negatives in brackets and OCR often drops them.
    """
    v = abs(value)
    if float(v).is_integer():
        s = f"{int(v):,}"
        groups = s.split(",")
        body = _SEP.join(re.escape(g) for g in groups)
    else:
        whole, frac = f"{v}".split(".")
        body = rf"{re.escape(whole)}[.,]\s?{re.escape(frac)}"
    return re.compile(rf"(?<![\d,.;:])(?:{body})(?![\d])")


def _clean(text: str) -> str:
    # Common OCR confusions inside numbers: letter O / l / I next to digits.
    text = re.sub(r"(?<=\d)[Oo](?=\d)", "0", text)
    text = re.sub(r"(?<=\d)[lI|](?=\d)", "1", text)
    return text


def check_row(row: pd.Series) -> tuple[str, str]:
    if row.verify == "nil":
        return "nil_not_checked", "shown as '-' or not presented; zero cannot be located by OCR"
    pdf = paths.FILINGS[int(row.filing_fy)]
    pat = number_pattern(float(row.value))
    for psm in PSM_MODES:
        if pat.search(_clean(ocr_page(pdf, int(row.pdf_page), psm))):
            weak = abs(float(row.value)) < 10 and float(row.value).is_integer()
            return ("verified_weak" if weak else "verified"), f"found on pdf p.{row.pdf_page} (psm {psm})"
    return "NOT_FOUND", f"not found on pdf p.{row.pdf_page}"


CONFIRMED = {"verified", "verified_weak", "nil_not_checked"}


def _confirm_by_identity(df: pd.DataFrame) -> pd.DataFrame:
    """A figure OCR could not find is confirmed if it is the only unconfirmed term of an accounting
    identity (e.g. a subtotal) that holds exactly and whose other terms OCR did find on the page.
    Typical case: the scans' italic comparatives where OCR reads '1' as '4' ("1,213" -> "4,213")."""
    status = {(r.filing_fy, r.period_fy, r.line_item): r.status for r in df.itertuples()}
    for _ in range(3):  # allow chains (e.g. a subtotal confirmed, then used to confirm another)
        changed = False
        for res in ledger.identity_results():
            if abs(res["difference"]) > 0.5:
                continue
            key = lambda item: (res["filing_fy"], res["period_fy"], item)  # noqa: E731
            members = [res["total"], *res["terms"]]
            unconfirmed = [m for m in members if status.get(key(m)) not in CONFIRMED | {"verified_by_identity"}]
            if len(unconfirmed) == 1:
                status[key(unconfirmed[0])] = "verified_by_identity"
                mask = ((df.filing_fy == res["filing_fy"]) & (df.period_fy == res["period_fy"])
                        & (df.line_item == unconfirmed[0]))
                df.loc[mask, "status"] = "verified_by_identity"
                df.loc[mask, "detail"] = f"OCR misread on page; implied exactly by identity '{res['total']}'"
                changed = True
        if not changed:
            break
    return df


def _warm_cache(pages: set[tuple[int, int]], psm: str) -> None:
    """OCR the given (filing, page) pairs in parallel so the row checks hit the cache."""
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as pool:
        list(pool.map(lambda fp: ocr_page(paths.FILINGS[fp[0]], fp[1], psm), sorted(pages)))


def verify_ledger() -> pd.DataFrame:
    df = ledger.load().copy()
    todo = df[df.verify == "ocr"]
    _warm_cache(set(zip(todo.filing_fy.astype(int), todo.pdf_page.astype(int))), PSM_MODES[0])
    first = todo.apply(lambda r: bool(number_pattern(float(r.value)).search(
        _clean(ocr_page(paths.FILINGS[int(r.filing_fy)], int(r.pdf_page), PSM_MODES[0])))), axis=1)
    retry = todo[~first]
    for psm in PSM_MODES[1:]:
        _warm_cache(set(zip(retry.filing_fy.astype(int), retry.pdf_page.astype(int))), psm)
    results = df.apply(check_row, axis=1, result_type="expand")
    df["status"], df["detail"] = results[0], results[1]
    return _confirm_by_identity(df)


def find_discrepancies() -> pd.DataFrame:
    """Comparative figures (year t-1 shown in filing t) that differ from filing t-1's own figure."""
    df = ledger.load()
    orig = df[df.filing_fy == df.period_fy].set_index(["period_fy", "line_item"])
    comp = df[df.filing_fy == df.period_fy + 1]
    rows = []
    for _, r in comp.iterrows():
        key = (r.period_fy, r.line_item)
        if key in orig.index:
            o = orig.loc[key]
            if float(o.value) != float(r.value):
                rows.append({
                    "fiscal_year": int(r.period_fy), "line_item": r.line_item,
                    "originally_reported": float(o.value), "comparative_in_next_filing": float(r.value),
                    "difference": float(r.value) - float(o.value), "unit": r.unit,
                    "original_ref": f"FY{int(r.period_fy) % 100} accounts pdf p.{o.pdf_page}",
                    "comparative_ref": f"FY{int(r.filing_fy) % 100} accounts pdf p.{r.pdf_page}",
                })
    return pd.DataFrame(rows)


def run(verify: bool = True) -> pd.DataFrame:
    paths.ensure_dirs()
    if verify:
        ver = verify_ledger()
        ver.to_csv(paths.PROCESSED / "verification.csv", index=False)
        failed = ver[ver.status == "NOT_FOUND"]
        if len(failed):
            raise SystemExit("OCR could not confirm these ledger figures:\n" +
                             failed[["filing_fy", "period_fy", "line_item", "value", "pdf_page"]].to_string())
    fin = ledger.current_year_table()
    fin.to_csv(paths.PROCESSED / "financials.csv", index=False)
    find_discrepancies().to_csv(paths.PROCESSED / "discrepancies.csv", index=False)
    return fin


if __name__ == "__main__":
    run()
