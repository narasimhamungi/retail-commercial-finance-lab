"""Headless recalculation of a workbook with LibreOffice, then read cached values back."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import openpyxl


def soffice() -> str | None:
    return shutil.which("soffice") or shutil.which("libreoffice")


def recalculated_copy(xlsx: Path, outdir: Path) -> Path:
    """Open `xlsx` in LibreOffice (which evaluates every formula) and save a copy with values."""
    exe = soffice()
    if exe is None:
        raise RuntimeError("LibreOffice (soffice) not found")
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [exe, f"-env:UserInstallation=file://{profile}", "--headless", "--calc",
             "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(outdir), str(xlsx)],
            check=True, capture_output=True, timeout=300,
        )
    out = outdir / xlsx.name
    if not out.exists():
        raise RuntimeError(f"LibreOffice did not write {out}")
    return out


def values(xlsx: Path) -> openpyxl.Workbook:
    with tempfile.TemporaryDirectory() as tmp:
        out = recalculated_copy(xlsx, Path(tmp))
        return openpyxl.load_workbook(out, data_only=True)
