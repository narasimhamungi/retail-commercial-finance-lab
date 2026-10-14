"""Recalculate both workbooks headlessly in LibreOffice and compare with the Python engine.

This test does not skip: it fails if LibreOffice is missing (CI installs it)."""

import pytest

from rcfl import bridge, excel_export, recalc, store_model as sm


@pytest.fixture(scope="module")
def store_wb(tmp_path_factory, cfg):
    assert recalc.soffice(), "LibreOffice (soffice) is required for the parity test"
    wb, refs = excel_export.build_store_workbook(cfg)
    p = tmp_path_factory.mktemp("xl") / "store_model.xlsx"
    wb.save(p)
    return recalc.values(p), refs


def _cell(wb, ref):
    sheet, addr = ref.split("!")
    return wb[sheet.strip("'")][addr.replace("$", "")].value


def _check(wb, refs, key, case):
    r = sm.run(case)
    assert _cell(wb, refs[key]["npv"]) == pytest.approx(r.npv, rel=1e-9, abs=1e-4)
    assert _cell(wb, refs[key]["irr"]) == pytest.approx(r.irr, abs=1e-7)
    pb = _cell(wb, refs[key]["payback_months"])
    if r.payback_months is None:
        assert pb == "n/a"
    else:
        assert pb == pytest.approx(r.payback_months, abs=1e-6)


@pytest.mark.parametrize("name", ["base", "downside", "upside"])
def test_scenarios_match(store_wb, cfg, name):
    wb, refs = store_wb
    _check(wb, refs, name, sm.scenario_case(cfg, name))


def test_tornado_cases_match(store_wb, cfg):
    wb, refs = store_wb
    for d, side, case in sm.tornado_cases(cfg):
        _check(wb, refs, f"tornado_{d}_{side}", case)


def test_break_even_and_checks(store_wb, cfg):
    wb, _ = store_wb
    rt = wb["Returns"]
    s = sm.summary(cfg)
    for col, name in (("B", "base"), ("C", "downside"), ("D", "upside")):
        assert rt[f"{col}8"].value == pytest.approx(s[name]["break_even_density"], rel=1e-9)
    assert rt["B26"].value is True


def test_bridge_workbook_matches(tmp_path):
    assert recalc.soffice(), "LibreOffice (soffice) is required for the parity test"
    wb, refs = excel_export.build_bridge_workbook()
    p = tmp_path / "bridge.xlsx"
    wb.save(p)
    vals = recalc.values(p)["Bridge"]
    df = bridge.build()
    for (prev, cur), r in refs.items():
        for basis in ("function", "nature"):
            assert vals.cell(r["checks"][basis], 2).value is True
            py = df[(df.basis == basis) & (df.to_fy == cur) & (df.kind == "delta")].value_k.tolist()
            xl = [vals.cell(row, 2).value for row in r["steps"][basis].values()]
            assert xl == pytest.approx(py, abs=1e-6)
