"""New-store appraisal engine (source of truth; the Excel workbook mirrors it with live formulas).

Illustrative and assumption-driven. Mint Velvet's store-level data is not public; outputs are
not Mint Velvet's store economics. The headline is the break-even sales density: the mature
sales per sq ft at which NPV over the lease is zero.

Timeline: year 0 = opening (fit-out capex, pre-opening costs, opening stock); years 1..N trade;
at the end of year N the lease ends, stock is released and dilapidations are paid. No terminal
value beyond the lease. Store losses are assumed relieved against group profits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

from . import paths, payroll

SECTIONS = ("store", "finance", "payroll", "payroll_and_tax")


def load_config(path: Path | None = None) -> dict:
    with open(path or paths.CONFIG / "assumptions.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def base_inputs(cfg: dict) -> dict:
    """Flat {name: value} for every input."""
    out = {}
    for sec in SECTIONS:
        for k, spec in cfg[sec].items():
            out[k] = float(spec["value"])
    return out


def bound(cfg: dict, name: str, which: str) -> float:
    for sec in SECTIONS:
        if name in cfg[sec]:
            return float(cfg[sec][name][which])
    raise KeyError(name)


@dataclass
class Case:
    """Inputs plus the multipliers used by the tornado (1.0 = base)."""
    x: dict
    payroll_mult: float = 1.0
    rent_mult: float = 1.0
    ramp_shortfall_mult: float = 1.0
    label: str = "base"


@dataclass
class Result:
    years: np.ndarray
    sales: np.ndarray
    gross_margin: np.ndarray
    payroll: np.ndarray
    rent: np.ndarray
    rates: np.ndarray
    occupancy_other: np.ndarray
    other_opex: np.ndarray
    store_ebitda: np.ndarray
    pre_opening: np.ndarray
    tax_depreciation: np.ndarray
    tax: np.ndarray
    capex: np.ndarray
    working_capital: np.ndarray
    wc_change: np.ndarray
    dilapidations: np.ndarray
    fcf: np.ndarray
    npv: float
    irr: float | None
    payback_months: float | None
    extras: dict = field(default_factory=dict)


def rates_multiplier(x: dict) -> float:
    rv = x["rateable_value"]
    if rv < 51000:
        return x["rates_multiplier_rhl_small"]
    if rv < 500000:
        return x["rates_multiplier_rhl_standard"]
    return x["rates_multiplier_high_value"]


def npv(rate: float, cfs: np.ndarray) -> float:
    t = np.arange(len(cfs))
    return float(np.sum(cfs / (1 + rate) ** t))


def irr(cfs: np.ndarray) -> float | None:
    """IRR by bisection on [-0.99, 10]; None if NPV does not change sign."""
    lo, hi = -0.99, 10.0
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    if f_lo * f_hi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cfs)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def payback_months(cfs: np.ndarray) -> float | None:
    """Months from opening until cumulative undiscounted cash flow turns positive (linear within year)."""
    cum = np.cumsum(cfs)
    for t in range(1, len(cfs)):
        if cum[t - 1] < 0 <= cum[t]:
            return (t - 1 + (-cum[t - 1]) / cfs[t]) * 12
    return None


def ramp(x: dict, t: int, shortfall_mult: float) -> float:
    if t == 1:
        return 1 - (1 - x["ramp_year1"]) * shortfall_mult
    if t == 2:
        return 1 - (1 - x["ramp_year2"]) * shortfall_mult
    return 1.0


def run(case: Case) -> Result:
    x = case.x
    n = int(x["lease_term_years"])
    yrs = np.arange(n + 1)
    pr = payroll.compute(x, x)
    mature = x["area_sqft"] * x["mature_sales_density"]

    volume = np.array([0.0] + [mature * ramp(x, t, case.ramp_shortfall_mult) for t in range(1, n + 1)])
    growth = np.array([0.0] + [(1 + x["sales_growth"]) ** (t - 1) for t in range(1, n + 1)])
    wage = np.array([0.0] + [(1 + x["wage_inflation"]) ** (t - 1) for t in range(1, n + 1)])
    cost = np.array([0.0] + [(1 + x["cost_inflation"]) ** (t - 1) for t in range(1, n + 1)])
    trading = (yrs >= 1).astype(float)

    sales = volume * growth
    gm = sales * x["product_gross_margin"]
    pay = (pr.fixed_payroll * trading + pr.variable_cost_per_k_sales * volume / 1000) * wage * case.payroll_mult
    rent = np.array([0.0] + [x["rent_per_year"] * (1 + (x["rent_review_uplift"] if t >= 6 else 0.0))
                             for t in range(1, n + 1)]) * case.rent_mult
    rates = x["rateable_value"] * rates_multiplier(x) * cost
    occ = x["occupancy_other_psf"] * x["area_sqft"] * cost
    opex = sales * x["other_opex_pct_sales"]
    ebitda = gm - pay - rent - rates - occ - opex

    pre = np.zeros(n + 1)
    pre[0] = x["pre_opening_costs"]
    capex = np.zeros(n + 1)
    capex[0] = x["fitout_capex"]
    tax_years = int(x["tax_depreciation_years"])
    tax_dep = np.array([0.0] + [x["fitout_capex"] / tax_years if t <= tax_years else 0.0 for t in range(1, n + 1)])
    dilaps = np.zeros(n + 1)
    dilaps[n] = x["dilapidations_at_exit"]
    taxable = ebitda - pre - tax_dep - dilaps
    tax = taxable * x["tax_rate"]

    # Stock: held at stock_pct x the year's sales, bought at opening for year 1, released at lease end.
    wc = np.zeros(n + 1)
    for t in range(0, n):
        wc[t] = x["stock_pct_sales"] * sales[t + 1]
    wc_change = np.diff(np.concatenate([[0.0], wc]))

    fcf = ebitda - pre - tax - capex - wc_change - dilaps
    res = Result(yrs, sales, gm, pay, rent, rates, occ, opex, ebitda, pre, tax_dep, tax, capex, wc, wc_change,
                 dilaps, fcf, npv(x["discount_rate"], fcf), irr(fcf), payback_months(fcf))
    mat = min(3, n)
    hours = payroll.labour_hours(x, pr, volume[mat])
    res.extras = {
        "payroll_pct_sales_maturity": pay[mat] / sales[mat],
        "four_wall_margin_maturity": ebitda[mat] / sales[mat],
        "sales_per_labour_hour_yr1_prices": volume[mat] / hours,
        "labour_hours_per_week_maturity": hours / payroll.WEEKS,
        "headcount_maturity": x["managers"] + (hours / payroll.WEEKS - x["managers"] * x["manager_contract_hours_per_week"])
        / x["associate_contract_hours_per_week"],
        "rent_pct_sales_maturity": rent[mat] / sales[mat],
        "occupancy_pct_sales_maturity": (rent[mat] + rates[mat] + occ[mat]) / sales[mat],
        "rates_multiplier": rates_multiplier(x),
        "mature_sales_yr1_prices": mature,
        "payroll": pr,
    }
    return res


def break_even_density(case: Case) -> float:
    """Density with NPV = 0. NPV is linear in density, so a secant through two points is exact."""
    d0 = case.x["mature_sales_density"]
    d1 = d0 + 100.0
    c0 = Case({**case.x, "mature_sales_density": d0}, case.payroll_mult, case.rent_mult, case.ramp_shortfall_mult)
    c1 = Case({**case.x, "mature_sales_density": d1}, case.payroll_mult, case.rent_mult, case.ramp_shortfall_mult)
    n0, n1 = run(c0).npv, run(c1).npv
    return d0 - n0 * (d1 - d0) / (n1 - n0)


def scenario_case(cfg: dict, name: str) -> Case:
    x = base_inputs(cfg)
    if name != "base":
        for k, which in cfg["scenarios"][name].items():
            x[k] = bound(cfg, k, which)
    return Case(x, label=name)


def tornado_cases(cfg: dict) -> list[tuple[str, str, Case]]:
    """(driver, 'low'/'high', case) with +/- shock applied to one driver at a time."""
    s = float(cfg["tornado"]["shock"])
    base = base_inputs(cfg)
    out = []
    for d in cfg["tornado"]["drivers"]:
        for side, m in (("low", 1 - s), ("high", 1 + s)):
            x = dict(base)
            c = Case(x, label=f"{d} {side}")
            if d in ("mature_sales_density", "product_gross_margin", "rent_per_year"):
                if d == "rent_per_year":
                    c.rent_mult = m
                else:
                    x[d] = base[d] * m
            elif d == "payroll":
                c.payroll_mult = m
            elif d == "ramp_speed":
                # Faster ramp-up = smaller shortfall to maturity.
                c.ramp_shortfall_mult = 2 - m
            else:
                raise KeyError(d)
            out.append((d, side, c))
    return out


def summary(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    out = {}
    for name in ("base", "downside", "upside"):
        c = scenario_case(cfg, name)
        r = run(c)
        out[name] = dict(npv=r.npv, irr=r.irr, payback_months=r.payback_months,
                         break_even_density=break_even_density(c), **{k: v for k, v in r.extras.items() if k != "payroll"})
    return out
