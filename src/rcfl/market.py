"""Market context: ONS Retail Sales Index (Great Britain, 2019=100, seasonally adjusted).

Mint Velvet's fiscal years are 52-week periods ending in the last days of December, so each
fiscal year is compared with the calendar-year average of the monthly index (alignment within
a few days). Annual averages of a seasonally adjusted index approximate the non-seasonally
adjusted annual total; the version-45 dataset publishes the SA series only.

Caveats (stated in the outputs): the RSI classifies each business by its main activity, so the
"textile, clothing and footwear stores" category covers store-based clothing retailers including
their online sales, but not online-only retailers; ONS covers Great Britain, Mint Velvet reports
UK turnover; and the category average mixes value and premium retailers.
"""

from __future__ import annotations

import openpyxl
import pandas as pd

from . import ledger, paths

SERIES = {
    ("Textile, clothing and footwear stores", "Value of retail sales at current prices"): "tcf_value",
    ("Textile, clothing and footwear stores", "Chained volume of retail sales"): "tcf_volume",
    ("All retailing excluding automotive fuel", "Value of retail sales at current prices"): "all_ex_fuel_value",
}
YEARS = range(2021, 2026)


def load_monthly() -> pd.DataFrame:
    wb = openpyxl.load_workbook(paths.ONS_RSI, read_only=True)
    ws = wb["Dataset"]
    rows = ws.iter_rows(values_only=True)
    header = None
    out = {}
    for row in rows:
        if row and row[0] == "Geography":
            header = row
            continue
        if header is None or not row or row[0] != "Great Britain":
            continue
        key = (row[2], row[3])
        if key in SERIES and row[4] == "Seasonally Adjusted":
            vals = {}
            for col, val in zip(header[5:], row[5:]):
                if isinstance(col, str) and not col.startswith("Data Marking") and val not in ("", None):
                    vals[pd.to_datetime(col, format="%b-%y")] = float(val)
            out[SERIES[key]] = pd.Series(vals)
    missing = set(SERIES.values()) - set(out)
    if missing:
        raise RuntimeError(f"ONS series not found in {paths.ONS_RSI.name}: {missing}")
    return pd.DataFrame(out).sort_index()


def annual() -> pd.DataFrame:
    m = load_monthly()
    m = m[(m.index.year >= min(YEARS)) & (m.index.year <= max(YEARS))]
    counts = m.groupby(m.index.year).size()
    if (counts != 12).any():
        raise RuntimeError(f"incomplete ONS years: {counts[counts != 12].to_dict()}")
    a = m.groupby(m.index.year).mean()
    a.index.name = "year"
    a["tcf_price"] = a["tcf_value"] / a["tcf_volume"] * 100  # implied deflator, 2019=100
    return a


def relative_performance() -> pd.DataFrame:
    a = annual()
    rows = []
    for y in ledger.FISCAL_YEARS:
        mv = ledger.value("turnover", y, y) / ledger.value("turnover", y - 1, y) - 1
        tcf = a.loc[y, "tcf_value"] / a.loc[y - 1, "tcf_value"] - 1
        rows.append(dict(
            fiscal_year=y,
            mint_velvet_turnover_growth=mv,
            ons_clothing_stores_value_growth=tcf,
            ons_clothing_stores_volume_growth=a.loc[y, "tcf_volume"] / a.loc[y - 1, "tcf_volume"] - 1,
            ons_clothing_stores_price_growth=a.loc[y, "tcf_price"] / a.loc[y - 1, "tcf_price"] - 1,
            ons_all_retail_ex_fuel_value_growth=a.loc[y, "all_ex_fuel_value"] / a.loc[y - 1, "all_ex_fuel_value"] - 1,
            relative_to_clothing_stores_ppt=(mv - tcf) * 100,
        ))
    return pd.DataFrame(rows)
