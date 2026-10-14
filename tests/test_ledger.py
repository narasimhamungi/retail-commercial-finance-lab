"""The transcription ledger: schema, accounting identities, and the OCR check against the raw PDFs."""

import pandas as pd
import pytest

from rcfl import extract, ledger, paths, report


def test_schema_and_files():
    df = ledger.load()
    assert set(ledger.COLUMNS) <= set(df.columns)
    for y in ledger.FISCAL_YEARS:
        assert paths.FILINGS[y].exists(), f"missing filed accounts for FY{y}"
    assert (df.pdf_page - df.printed_page == 3).all()


def test_every_fiscal_year_has_core_lines():
    core = ["turnover", "cost_of_sales", "gross_profit", "admin_expenses", "other_operating_income",
            "operating_profit", "profit_before_tax", "tax", "profit_after_tax", "staff_costs_total",
            "operating_lease_rentals", "depreciation", "amortisation", "impairment_tangible", "fx_differences",
            "stocks", "employees_total", "adjusted_ebitda", "standalone_stores", "concession_stores", "weeks_in_period"]
    for y in ledger.FISCAL_YEARS:
        for item in core:
            assert ledger.has(item, y), f"{item} missing for FY{y}"


def test_all_periods_are_52_weeks():
    for y in ledger.FISCAL_YEARS:
        assert ledger.value("weeks_in_period", y) == 52
    days = pd.Series(pd.to_datetime(list(paths.PERIOD_END.values()))).diff().dropna().dt.days
    assert (days == 364).all()


def test_accounting_identities_hold_fy22_to_fy25():
    res = [r for r in ledger.identity_results() if r["period_fy"] in ledger.FISCAL_YEARS]
    assert len(res) >= 80
    bad = [r for r in res if abs(r["difference"]) > 0.5]
    assert not bad, bad


def test_known_fy21_inconsistency_is_the_only_identity_break():
    bad = [r for r in ledger.identity_results() if abs(r["difference"]) > 0.5]
    assert [(r["period_fy"], r["total"], r["difference"]) for r in bad] == [(2021, "adjusted_ebitda", -2.0)]


def test_every_ledger_figure_confirmed_against_raw_pdf():
    ver = extract.verify_ledger()
    assert (ver.status != "NOT_FOUND").all(), ver[ver.status == "NOT_FOUND"]
    counts = ver.status.value_counts()
    assert counts.get("verified", 0) >= 380
    assert counts.get("verified_by_identity", 0) <= 10


@pytest.mark.parametrize("text,value,hit", [
    ("Profit for the period 10,595 19;790.", 19790, True),
    ("Profit 19, 790k", 19790, True),
    ("119,790", 19790, False),
    ("Other operating income 1,426 4,213", 1213, False),
    ("(1,211) (818)", -1211, True),
    ("increased by 5.4 percentage points", 5.4, True),
    ("trading -13.5% on the prior year", -13.5, True),
])
def test_number_pattern(text, value, hit):
    assert bool(extract.number_pattern(value).search(text)) is hit


def test_discrepancies_detected():
    d = extract.find_discrepancies()
    keys = set(zip(d.fiscal_year, d.line_item))
    assert {(2024, "wages_salaries"), (2024, "social_security"), (2022, "lease_commitments_total"),
            (2022, "inventory_impairment")} <= keys
    pl = {"turnover", "cost_of_sales", "admin_expenses", "operating_profit", "profit_before_tax", "profit_after_tax"}
    assert not (set(d.line_item) & pl), "P&L comparatives should match the original filings"


def test_store_rollforward_flags_fy25_concessions():
    rf = {(r["fy"], r["kind"]): r for r in report.store_rollforward()}
    assert rf[(2025, "concession")]["reported"] - rf[(2025, "concession")]["implied"] == 2
    for key, r in rf.items():
        if key != (2025, "concession"):
            assert r["reported"] == r["implied"], key


def test_press_figures_agree_with_filings():
    for label, press, fn in report.PRESS:
        dp = 0 if "stores" in label else 1
        assert round(fn(), dp) == round(press, dp), label
