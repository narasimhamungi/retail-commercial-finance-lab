"""Source ledger: every figure transcribed from the filed accounts, with its page reference.

The filed accounts are scanned images (Companies House tiff2pdf, no text layer), so figures
are transcribed by reading the page image and recorded here. `extract.py` then OCRs each
cited page and fails the build if a transcribed number cannot be found on that page.
"""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from . import paths

COLUMNS = ["filing_fy", "period_fy", "line_item", "value", "unit", "pdf_page",
           "printed_page", "section", "verify", "note"]
UNITS = {"gbp_k", "count", "pct", "ppt", "weeks"}
VERIFY = {"ocr", "nil"}
FISCAL_YEARS = (2022, 2023, 2024, 2025)


@lru_cache(maxsize=1)
def load() -> pd.DataFrame:
    df = pd.read_csv(paths.LEDGER, dtype={"note": str}, keep_default_na=False)
    validate(df)
    return df


def validate(df: pd.DataFrame) -> None:
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"ledger missing columns: {sorted(missing)}")
    bad_unit = set(df["unit"]) - UNITS
    if bad_unit:
        raise ValueError(f"unknown units: {bad_unit}")
    bad_verify = set(df["verify"]) - VERIFY
    if bad_verify:
        raise ValueError(f"unknown verify flags: {bad_verify}")
    if not set(df["filing_fy"]).issubset(paths.FILINGS):
        raise ValueError("ledger cites a filing that is not in data/raw")
    if (df["period_fy"] > df["filing_fy"]).any() or (df["filing_fy"] - df["period_fy"] > 1).any():
        raise ValueError("period must be the filing year or its comparative year")
    dup = df.duplicated(["filing_fy", "period_fy", "line_item"])
    if dup.any():
        raise ValueError(f"duplicate ledger rows: {df[dup][['filing_fy','period_fy','line_item']].values.tolist()}")
    nil_nonzero = df[(df["verify"] == "nil") & (df["value"] != 0)]
    if len(nil_nonzero):
        raise ValueError("rows flagged 'nil' must have value 0")


# Accounting identities that must hold within each filing column: (total, [(sign, term), ...]).
# Terms missing from a column (not disclosed that year) are skipped only if listed in OPTIONAL.
IDENTITIES = {
    "gross_profit": [(+1, "turnover"), (-1, "cost_of_sales")],
    "operating_profit": [(+1, "gross_profit"), (-1, "admin_expenses"), (+1, "other_operating_income")],
    "profit_before_tax": [(+1, "operating_profit"), (+1, "interest_receivable"), (-1, "interest_payable")],
    "profit_after_tax": [(+1, "profit_before_tax"), (-1, "tax")],
    "other_operating_income": [(+1, "ooi_other"), (+1, "ooi_royalty"), (+1, "ooi_government_grants")],
    "staff_costs_total": [(+1, "wages_salaries"), (+1, "social_security"), (+1, "pension_cost")],
    "employees_total": [(+1, "employees_admin"), (+1, "employees_store"), (+1, "employees_directors")],
    "net_current_assets": [(+1, "stocks"), (+1, "debtors"), (+1, "current_asset_investments"), (+1, "cash"),
                           (-1, "creditors_within_1y")],
    "net_assets": [(+1, "intangible_assets"), (+1, "tangible_assets"), (+1, "investments"),
                   (+1, "net_current_assets"), (-1, "creditors_after_1y"), (-1, "deferred_tax"), (-1, "provisions")],
    "adjusted_ebitda": [(+1, "operating_profit"), (+1, "depreciation"), (+1, "amortisation"),
                        (+1, "impairment_tangible"), (+1, "fx_differences")],
    "turnover": [(+1, "turnover_uk"), (+1, "turnover_rest_of_world")],
    "pension_cost": [(+1, "pension_dc")],
}
OPTIONAL = {"ooi_government_grants", "current_asset_investments", "turnover_rest_of_world"}


def identity_results() -> list[dict]:
    """Evaluate every identity in every (filing, period) column where the total is present."""
    df = load()
    out = []
    for (filing, period), col in df.groupby(["filing_fy", "period_fy"]):
        vals = dict(zip(col.line_item, col.value.astype(float)))
        for total, terms in IDENTITIES.items():
            if total not in vals:
                continue
            present = [t for _, t in terms if t in vals]
            missing = [t for _, t in terms if t not in vals and t not in OPTIONAL]
            if missing or not present:
                continue
            rhs = sum(s * vals[t] for s, t in terms if t in vals)
            out.append(dict(filing_fy=filing, period_fy=period, total=total,
                            terms=[t for t in present], reported=vals[total], computed=rhs,
                            difference=vals[total] - rhs))
    return out


def value(item: str, period: int, filing: int | None = None) -> float:
    """Value of `item` for `period`, read from `filing` (default: the period's own filing)."""
    df = load()
    filing = period if filing is None else filing
    row = df[(df.filing_fy == filing) & (df.period_fy == period) & (df.line_item == item)]
    if row.empty:
        raise KeyError(f"{item} for FY{period} not in FY{filing} filing ledger")
    return float(row["value"].iloc[0])


def has(item: str, period: int, filing: int | None = None) -> bool:
    try:
        value(item, period, filing)
        return True
    except KeyError:
        return False


def ref(item: str, period: int, filing: int | None = None) -> str:
    """Human-readable source reference, e.g. 'FY25 accounts p.18 (printed p.15)'."""
    df = load()
    filing = period if filing is None else filing
    row = df[(df.filing_fy == filing) & (df.period_fy == period) & (df.line_item == item)].iloc[0]
    return f"FY{filing % 100:02d} accounts pdf p.{row.pdf_page} (printed p.{row.printed_page})"


def current_year_table() -> pd.DataFrame:
    """Each fiscal year's figures as originally reported in that year's own filing."""
    df = load()
    cur = df[(df.filing_fy == df.period_fy) & (df.period_fy.isin(FISCAL_YEARS))].copy()
    cur["source_file"] = cur["filing_fy"].map(lambda y: paths.FILINGS[y].name)
    cur["page_ref"] = cur.apply(lambda r: f"pdf p.{r.pdf_page} (printed p.{r.printed_page})", axis=1)
    out = cur.rename(columns={"period_fy": "fiscal_year"})
    out["value_gbp"] = out.apply(lambda r: r.value * 1000 if r.unit == "gbp_k" else None, axis=1)
    return out[["fiscal_year", "line_item", "value", "unit", "value_gbp", "page_ref",
                "source_file", "section", "note"]].sort_values(["fiscal_year", "line_item"]).reset_index(drop=True)
