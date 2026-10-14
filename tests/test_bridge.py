"""Profit bridge: reconciliation to reported PBT and the effect formulas."""

import pytest

from rcfl import bridge, ledger


@pytest.fixture(scope="module")
def df():
    return bridge.build()


@pytest.mark.parametrize("basis", ["function", "nature"])
@pytest.mark.parametrize("prev,cur", bridge.PAIRS)
def test_bridge_reconciles_to_reported_pbt_to_zero(df, basis, prev, cur):
    sub = df[(df.basis == basis) & (df.from_fy == prev) & (df.to_fy == cur)]
    start = sub[sub.kind == "start"].value_k.iloc[0]
    end = sub[sub.kind == "end"].value_k.iloc[0]
    assert start == ledger.value("profit_before_tax", prev, cur)
    assert end == ledger.value("profit_before_tax", cur, cur)
    assert abs(start + sub[sub.kind == "delta"].value_k.sum() - end) < 1e-6


def test_disclosed_bars_tie_to_notes(df):
    """Every nature-view bar except the sales and other-cost-rate effects is a straight note difference."""
    s = df[(df.basis == "nature") & (df.to_fy == 2025)].set_index("step").value_k
    v = lambda item, p: ledger.value(item, p, 2025)  # noqa: E731
    assert s["Staff costs"] == -(v("staff_costs_total", 2025) - v("staff_costs_total", 2024)) == -3452
    assert s["Operating lease rentals"] == -(5053 - 4892)
    da = lambda p: v("depreciation", p) + v("amortisation", p) + v("impairment_tangible", p)  # noqa: E731
    assert s["Depreciation, amortisation, impairment"] == -(da(2025) - da(2024)) == 455
    assert s["Exchange differences"] == -(-1211 - -818) == 393
    assert s["Other operating income"] == 1484 - 1355
    assert s["Net finance income"] == (723 - 1) - 974


def test_function_view_hand_computed_fy25(df):
    s = df[(df.basis == "function") & (df.to_fy == 2025)].set_index("step").value_k
    gm24, gm25 = 31067 / 134735, 40074 / 150240
    assert s["Sales effect (at prior-year GM rate)"] == pytest.approx((150240 - 134735) * gm24)
    assert s["Gross-margin-rate effect"] == pytest.approx((gm25 - gm24) * 150240)
    assert s["Administrative expenses"] == -(22097 - 19173)


def test_other_cost_pool_reported_and_sane():
    t = bridge.other_pool_table()
    assert (t.other_costs_k > 0).all()
    assert t.other_pct_revenue.between(0.5, 0.8).all()
    y22 = t[(t.fiscal_year == 2022)].iloc[0]
    # FY22 pool must exceed the disclosed cost of stock, which it contains.
    assert y22.other_costs_k > ledger.value("cost_of_stock_expensed", 2022)
