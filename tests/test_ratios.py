"""Ratio formulas against hand calculations."""

import pytest

from rcfl import market, ratios


@pytest.fixture(scope="module")
def rt():
    return ratios.build().set_index("fiscal_year")


def test_margins(rt):
    assert rt.loc[2025, "gm_rate"] == pytest.approx(40074 / 150240)
    assert rt.loc[2024, "pbt_margin"] == pytest.approx(14223 / 134735)
    assert rt.loc[2023, "adj_ebitda_margin"] == pytest.approx(25851 / 139806)


def test_decremental_margin(rt):
    assert rt.loc[2024, "op_change_per_revenue_change"] == pytest.approx((13249 - 22752) / (134735 - 139806))
    assert rt.loc[2025, "op_change_per_revenue_change"] == pytest.approx((19461 - 13249) / (150240 - 134735))


def test_stock_and_people(rt):
    assert rt.loc[2024, "stock_cover_weeks"] == pytest.approx(16739 / (134735 / 52))
    assert rt.loc[2025, "revenue_per_head_k"] == pytest.approx(150240 / 862)
    assert rt.loc[2025, "employer_ss_pct_wages"] == pytest.approx(1847 / 19175)
    assert rt.loc[2025, "lease_per_standalone_k"] == pytest.approx(5053 / 53)


def test_product_margin_only_where_disclosed(rt):
    assert rt.loc[2022, "product_gross_margin"] == pytest.approx(1 - 41639 / 143675)
    assert rt.loc[[2023, 2024, 2025], "product_gross_margin"].isna().all()


def test_adjusted_ebitda_rebuilds_exactly():
    chk = ratios.ebitda_check()
    assert (chk.difference_k.abs() < 0.5).all()


def test_market_series_and_alignment():
    a = market.annual()
    assert list(a.index) == [2021, 2022, 2023, 2024, 2025]
    m = market.load_monthly()
    y25 = m[m.index.year == 2025].tcf_value.mean() / m[m.index.year == 2024].tcf_value.mean() - 1
    rp = market.relative_performance().set_index("fiscal_year")
    assert rp.loc[2025, "ons_clothing_stores_value_growth"] == pytest.approx(y25)
    assert rp.loc[2025, "relative_to_clothing_stores_ppt"] == pytest.approx(
        (rp.loc[2025, "mint_velvet_turnover_growth"] - y25) * 100)
