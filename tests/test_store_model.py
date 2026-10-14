"""Store model: payroll statutory maths, cash-flow identities, returns maths, break-even."""

import numpy as np
import pytest

from rcfl import ledger, payroll, store_model as sm


def test_npv_irr_payback_hand_computed():
    cfs = np.array([-100.0, 60.0, 60.0])
    assert sm.npv(0.10, cfs) == pytest.approx(-100 + 60 / 1.1 + 60 / 1.21)
    # IRR solves 60/(1+r) + 60/(1+r)^2 = 100 -> r = 13.0662...%
    assert sm.irr(cfs) == pytest.approx(0.130662, abs=1e-6)
    # cumulative: -100, -40, +20 -> payback = 1 + 40/60 years = 20 months
    assert sm.payback_months(cfs) == pytest.approx(20.0)
    assert sm.payback_months(np.array([-100.0, 10.0, 10.0])) is None
    # -100 + 10y + 10y^2 = 0 with y = 1/(1+r): y = (-10 + sqrt(4100)) / 20
    assert sm.irr(np.array([-100.0, 10.0, 10.0])) == pytest.approx(20 / (-10 + 4100 ** 0.5) - 1, abs=1e-6)


def test_payroll_statutory_maths():
    assert payroll.holiday_uplift(5.6) == pytest.approx(5.6 / 46.4)
    assert payroll.employer_nic(15000, 0.15, 5000) == pytest.approx(1500)
    assert payroll.employer_nic(4000, 0.15, 5000) == 0
    assert payroll.employer_pension(9999, 0.03, 6240, 50270, 10000) == 0           # below trigger
    assert payroll.employer_pension(20000, 0.03, 6240, 50270, 10000) == pytest.approx(0.03 * 13760)
    assert payroll.employer_pension(60000, 0.03, 6240, 50270, 10000) == pytest.approx(0.03 * 44030)


def test_payroll_associate(cfg):
    x = sm.base_inputs(cfg)
    pr = payroll.compute(x, x)
    rate = 12.71 * 1.05
    earnings = 20 * 52 * rate * (1 + 5.6 / 46.4)
    assert pr.associate_annual_earnings == pytest.approx(earnings)
    assert pr.associate_nic == pytest.approx(0.15 * (earnings - 5000))
    assert pr.associate_nic_2024_25 == pytest.approx(0.138 * (earnings - 9100))
    assert pr.fixed_associate_hours_week == pytest.approx(64 * 2 + 16 - 2 * 30)


def test_cash_flow_identities(cfg):
    r = sm.run(sm.scenario_case(cfg, "base"))
    x = sm.base_inputs(cfg)
    assert r.wc_change.sum() == pytest.approx(0, abs=1e-6)                 # stock released at lease end
    assert r.tax.sum() == pytest.approx(x["tax_rate"] * (r.store_ebitda - r.pre_opening - r.tax_depreciation - r.dilapidations).sum())
    assert r.tax_depreciation.sum() == pytest.approx(x["fitout_capex"])
    assert r.fcf == pytest.approx(r.store_ebitda - r.pre_opening - r.tax - r.capex - r.wc_change - r.dilapidations)
    assert r.sales[0] == 0 and r.capex[0] == x["fitout_capex"]
    assert r.sales[1] == pytest.approx(x["area_sqft"] * x["mature_sales_density"] * x["ramp_year1"])
    assert r.rent[6] == pytest.approx(x["rent_per_year"] * (1 + x["rent_review_uplift"]))
    assert r.extras["rates_multiplier"] == 0.430                            # RV 55k sits in the standard RHL band


def test_npv_linear_in_density_so_secant_is_exact(cfg):
    x = sm.base_inputs(cfg)
    n = [sm.run(sm.Case({**x, "mature_sales_density": d})).npv for d in (300, 700, 1100)]
    assert n[0] - 2 * n[1] + n[2] == pytest.approx(0, abs=1e-4)


@pytest.mark.parametrize("name", ["base", "downside", "upside"])
def test_break_even_density_gives_zero_npv(cfg, name):
    case = sm.scenario_case(cfg, name)
    be = sm.break_even_density(case)
    assert sm.run(sm.Case({**case.x, "mature_sales_density": be})).npv == pytest.approx(0, abs=1e-3)


def test_scenarios_ordered(cfg):
    s = sm.summary(cfg)
    assert s["downside"]["npv"] < s["base"]["npv"] < s["upside"]["npv"]
    assert s["upside"]["break_even_density"] < s["base"]["break_even_density"] < s["downside"]["break_even_density"]


def test_tornado_directions(cfg):
    base = sm.run(sm.scenario_case(cfg, "base")).npv
    res = {(d, side): sm.run(c).npv for d, side, c in sm.tornado_cases(cfg)}
    for d in ("mature_sales_density", "product_gross_margin", "ramp_speed"):
        assert res[(d, "low")] < base < res[(d, "high")]
    for d in ("rent_per_year", "payroll"):
        assert res[(d, "high")] < base < res[(d, "low")]


def test_assumptions_have_basis_and_range(cfg):
    for sec in sm.SECTIONS:
        for k, s in cfg[sec].items():
            assert s["basis"] in {"SOURCED", "FILING_PROXY", "ASSUMPTION"}, k
            for field in ("value", "low", "high", "unit", "source"):
                assert field in s and s[field] not in (None, ""), (k, field)
            assert s["low"] <= s["value"] <= s["high"], k
            if s["basis"] == "SOURCED":
                assert s["low"] == s["value"] == s["high"], k
            if s["basis"] == "ASSUMPTION" and s["low"] == s["high"]:
                assert k in {"managers", "manager_contract_hours_per_week", "tax_depreciation_years"}, k


def test_filing_proxies_match_ledger(cfg):
    v = ledger.value
    s = cfg["store"]
    assert s["product_gross_margin"]["value"] == pytest.approx(1 - v("cost_of_stock_expensed", 2022) / v("turnover", 2022), abs=5e-5)
    assert s["rent_per_year"]["value"] == pytest.approx(v("operating_lease_rentals", 2025) * 1000 / v("standalone_stores", 2025), abs=1)
    projects24 = v("standalone_opened", 2024) + v("standalone_relocated", 2024)
    assert s["fitout_capex"]["value"] == pytest.approx(v("tangible_additions", 2024) * 1000 / projects24, abs=1)
    assert s["fitout_capex"]["low"] == pytest.approx(v("tangible_additions", 2022) * 1000 / v("standalone_opened", 2022), abs=1)
    assert s["fitout_capex"]["high"] == pytest.approx(v("tangible_additions", 2023) * 1000 / v("standalone_opened", 2023), abs=1)
    assert s["stock_pct_sales"]["value"] == pytest.approx(v("stocks", 2025) / v("turnover", 2025), abs=5e-5)
    assert s["stock_pct_sales"]["low"] == pytest.approx(v("stocks", 2023) / v("turnover", 2023), abs=5e-5)
    assert s["stock_pct_sales"]["high"] == pytest.approx(v("stocks", 2024) / v("turnover", 2024), abs=5e-5)
    assert s["dilapidations_at_exit"]["value"] == pytest.approx(v("dilapidation_provision", 2025) * 1000 / v("standalone_stores", 2025), abs=1)
    assert s["dilapidations_at_exit"]["low"] == pytest.approx(v("dilapidation_provision", 2022) * 1000 / v("standalone_stores", 2022), abs=1)
    assert s["area_sqft"]["value"] == 1700
