"""Ratio table, FY22-FY25, each year from its own filing.

Every ratio is a documented formula over ledger figures (see RATIO_DEFINITIONS). Ratios that
need a figure the accounts do not disclose for a year are left blank, never estimated.
"""

from __future__ import annotations

import math

import pandas as pd

from . import bridge, ledger

YEARS = ledger.FISCAL_YEARS

RATIO_DEFINITIONS = {
    "revenue_growth": "turnover(t) / turnover(t-1) - 1, both from filing t",
    "gm_rate": "gross profit / turnover (after retail-channel costs, note 2.6)",
    "admin_pct_sales": "administrative expenses / turnover",
    "op_margin": "operating profit / turnover",
    "pbt_margin": "profit before tax / turnover",
    "adj_ebitda_margin": "management adjusted EBITDA (strategic report) / turnover",
    "staff_pct_sales": "staff costs (note 8) / turnover",
    "lease_pct_sales": "operating lease rentals (note 6) / turnover",
    "other_cost_pct_sales": "other operating costs pool (see bridge.py) / turnover",
    "employer_ss_pct_wages": "social security costs / wages and salaries (note 8)",
    "revenue_per_head_k": "turnover / average monthly employees (per head, not FTE)",
    "staff_cost_per_head_k": "staff costs / average monthly employees (per head, not FTE)",
    "store_staff_share": "store staff / average monthly employees",
    "lease_per_standalone_k": "operating lease rentals / standalone stores at year end "
                              "(upper bound: includes head office and any other leased property)",
    "stock_to_sales": "stock at year end / turnover",
    "stock_cover_weeks": "stock / (turnover / 52) - weeks of turnover; stock at cost vs sales at selling price",
    "stock_provision_pct_gross": "stock obsolescence provision / (stock + provision)",
    "product_gross_margin": "1 - cost of stock expensed / turnover (disclosed in the FY22 filing only)",
    "stock_days_on_cogs": "stock / cost of stock expensed x 364 (FY22 only)",
    "tangible_capex_per_project_k": "tangible additions / (standalone openings + relocations); upper bound, "
                                    "includes refits, IT and head-office capex",
    "op_change_per_revenue_change": "d operating profit / d turnover vs prior year (decremental margin when sales fall)",
}


def _safe(fn):
    try:
        x = fn()
        return None if x is None or (isinstance(x, float) and math.isnan(x)) else x
    except (KeyError, ZeroDivisionError):
        return None


def year_ratios(y: int) -> dict:
    v = lambda item, per=y: ledger.value(item, per, y)  # noqa: E731
    rev = v("turnover")
    pools = bridge.pools(y)
    out = {
        "fiscal_year": y,
        "turnover_k": rev,
        "revenue_growth": _safe(lambda: rev / v("turnover", y - 1) - 1),
        "gm_rate": (rev - v("cost_of_sales")) / rev,
        "admin_pct_sales": v("admin_expenses") / rev,
        "op_margin": v("operating_profit") / rev,
        "pbt_margin": v("profit_before_tax") / rev,
        "adj_ebitda_k": v("adjusted_ebitda"),
        "adj_ebitda_margin": v("adjusted_ebitda") / rev,
        "staff_pct_sales": pools["staff"] / rev,
        "lease_pct_sales": pools["lease"] / rev,
        "other_cost_pct_sales": pools["other_rate"],
        "employer_ss_pct_wages": v("social_security") / v("wages_salaries"),
        "revenue_per_head_k": rev / v("employees_total"),
        "staff_cost_per_head_k": v("staff_costs_total") / v("employees_total"),
        "store_staff_share": v("employees_store") / v("employees_total"),
        "standalone_stores": v("standalone_stores"),
        "concession_stores": v("concession_stores"),
        "lease_per_standalone_k": pools["lease"] / v("standalone_stores"),
        "stock_k": v("stocks"),
        "stock_to_sales": v("stocks") / rev,
        "stock_cover_weeks": v("stocks") / (rev / 52),
        "stock_provision_k": v("stock_provision"),
        "stock_provision_pct_gross": v("stock_provision") / (v("stocks") + v("stock_provision")),
        "product_gross_margin": _safe(lambda: 1 - v("cost_of_stock_expensed") / rev),
        "stock_days_on_cogs": _safe(lambda: v("stocks") / v("cost_of_stock_expensed") * 364),
        "tangible_additions_k": v("tangible_additions"),
        "tangible_capex_per_project_k": _safe(
            lambda: v("tangible_additions") / ((ledger.value("standalone_opened", y) if ledger.has("standalone_opened", y) else 0)
                                               + (ledger.value("standalone_relocated", y) if ledger.has("standalone_relocated", y) else 0))),
        "cash_k": v("cash") + (v("current_asset_investments") if ledger.has("current_asset_investments", y) else 0),
        "dividends_paid_k": v("dividends_paid"),
        "net_assets_k": v("net_assets"),
        "op_change_per_revenue_change": _safe(
            lambda: (v("operating_profit") - v("operating_profit", y - 1)) / (rev - v("turnover", y - 1))),
    }
    return out


def build() -> pd.DataFrame:
    return pd.DataFrame([year_ratios(y) for y in YEARS])


def ebitda_check() -> pd.DataFrame:
    """Rebuild management adjusted EBITDA from statutory lines: OP + D&A + impairment + FX charge."""
    rows = []
    for y in YEARS:
        v = lambda item: ledger.value(item, y, y)  # noqa: E731
        rebuilt = (v("operating_profit") + v("depreciation") + v("amortisation") + v("impairment_tangible")
                   + v("fx_differences"))
        rows.append(dict(fiscal_year=y, operating_profit_k=v("operating_profit"),
                         depreciation_k=v("depreciation"), amortisation_k=v("amortisation"),
                         impairment_k=v("impairment_tangible"), fx_charge_k=v("fx_differences"),
                         rebuilt_adj_ebitda_k=rebuilt, reported_adj_ebitda_k=v("adjusted_ebitda"),
                         difference_k=rebuilt - v("adjusted_ebitda")))
    return pd.DataFrame(rows)
