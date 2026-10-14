"""Repository paths. Everything is resolved relative to the repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
DATA = ROOT / "data"
RAW = DATA / "raw"
RAW_ONS = RAW / "ons"
LEDGER = DATA / "ledger" / "transcription.csv"
INTERIM = DATA / "interim"
OCR_CACHE = INTERIM / "ocr"
PROCESSED = DATA / "processed"
OUTPUTS = ROOT / "outputs"
CHARTS = OUTPUTS / "charts"
DOCS = ROOT / "docs"

# One filed accounts PDF per fiscal year (52-week periods ending late December).
FILINGS = {
    2022: RAW / "sabre_retail_fashion_07920155_FY22_2022-12-31.pdf",
    2023: RAW / "sabre_retail_fashion_07920155_FY23_2023-12-30.pdf",
    2024: RAW / "sabre_retail_fashion_07920155_FY24_2024-12-28.pdf",
    2025: RAW / "sabre_retail_fashion_07920155_FY25_2025-12-27.pdf",
}

PERIOD_END = {2021: "2022-01-01", 2022: "2022-12-31", 2023: "2023-12-30", 2024: "2024-12-28", 2025: "2025-12-27"}

ONS_RSI = RAW_ONS / "retail-sales-index-time-series-v45.xlsx"


def ensure_dirs() -> None:
    for p in (INTERIM, OCR_CACHE, PROCESSED, OUTPUTS, CHARTS, DOCS):
        p.mkdir(parents=True, exist_ok=True)
