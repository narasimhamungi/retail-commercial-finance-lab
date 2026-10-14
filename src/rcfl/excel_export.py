"""Excel workbooks with live formulas (no pasted results).

outputs/store_model.xlsx  Inputs, Payroll, Store P&L, Returns, Sensitivity, Engine
outputs/bridge.xlsx       Data, Bridge (function and nature views), Ratios, Checks

Conventions: blue font = input, black = formula. Every input row carries its basis and source.
The Python engine (store_model.py, bridge.py) is the source of truth; tests/test_excel_parity.py
recalculates both workbooks headlessly in LibreOffice and asserts the results match.
"""

from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as col
from openpyxl.workbook.defined_name import DefinedName

from . import bridge, ledger, paths, store_model

BLUE = Font(color="0000FF")
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14)
NOTE = Font(italic=True, color="555555", size=9)
HEAD_FILL = PatternFill("solid", fgColor="DDE5F0")
CHECK_FILL = PatternFill("solid", fgColor="E2F0D9")
THIN = Border(bottom=Side(style="thin", color="999999"))
GBP = '#,##0;(#,##0);"-"'
GBP1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
MAXY = 15  # columns for years 0..15; lease term may be 5-15

DISCLAIMER = ("Illustrative and assumption-driven. Mint Velvet store-level data is not public; "
              "outputs are not Mint Velvet's store economics. Independent analysis of public filings, "
              "not affiliated with or endorsed by Mint Velvet or Sabre Retail Fashion Limited.")


def _name(wb: Workbook, name: str, ref: str) -> None:
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


def _header(ws, row: int, labels: list[str], start_col: int = 1) -> None:
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font, c.fill = BOLD, HEAD_FILL


# --------------------------------------------------------------------------------------------
# Store model
# --------------------------------------------------------------------------------------------

SCENARIO_KEYS = ("mature_sales_density", "product_gross_margin", "rent_per_year", "fitout_capex",
                 "ramp_year1", "ramp_year2")


def _inputs_sheet(wb: Workbook, cfg: dict) -> None:
    ws = wb.active
    ws.title = "Inputs"
    ws["A1"], ws["A1"].font = "New-store appraisal: inputs", TITLE
    ws["A2"], ws["A2"].font = DISCLAIMER, NOTE
    ws["A3"], ws["A3"].font = "Blue = input. Basis: SOURCED (public source), FILING_PROXY (derived from the filed accounts; capex, rent and stock proxies are upper bounds), ASSUMPTION (analyst assumption).", NOTE
    _header(ws, 5, ["Section", "Input", "Value", "Unit", "Basis", "Low", "High", "Source / derivation"])
    r = 6
    for sec in store_model.SECTIONS:
        for key, spec in cfg[sec].items():
            ws.cell(r, 1, sec)
            ws.cell(r, 2, key)
            for c_idx, field in ((3, "value"), (6, "low"), (7, "high")):
                cell = ws.cell(r, c_idx, float(spec[field]))
                cell.font = BLUE
            ws.cell(r, 4, spec["unit"])
            ws.cell(r, 5, spec["basis"])
            ws.cell(r, 8, spec["source"]).alignment = Alignment(wrap_text=False)
            _name(wb, key, f"Inputs!$C${r}")
            _name(wb, f"{key}_low", f"Inputs!$F${r}")
            _name(wb, f"{key}_high", f"Inputs!$G${r}")
            r += 1
    for c_idx, w in zip(range(1, 9), (16, 34, 12, 44, 14, 12, 12, 120)):
        ws.column_dimensions[col(c_idx)].width = w
    ws.freeze_panes = "C6"


def _payroll_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Payroll")
    ws["A1"], ws["A1"].font = "Bottom-up store payroll (year-1 prices, 2026/27 statutory rates)", TITLE
    ws["A2"], ws["A2"].font = "Associates: part-time contracts at NLW plus premium; managers salaried. Fixed hours cover the floor across trading hours; variable hours scale with sales volume.", NOTE
    rows = [
        ("holiday_uplift", "Holiday pay uplift per hour worked", "=holiday_weeks/(52-holiday_weeks)", PCT),
        ("assoc_rate", "Associate hourly rate", "=nlw_hourly*(1+associate_premium_over_nlw)", "0.00"),
        ("assoc_earnings", "Associate annual earnings (incl. holiday pay)",
         "=associate_contract_hours_per_week*52*assoc_rate*(1+holiday_uplift)", GBP),
        ("assoc_nic", "Employer NIC per associate, 2026/27", "=employer_nic_rate*MAX(0,assoc_earnings-nic_secondary_threshold)", GBP),
        ("assoc_nic_old", "Employer NIC per associate under 2024/25 rules (comparison)",
         "=employer_nic_rate_2024_25*MAX(0,assoc_earnings-nic_secondary_threshold_2024_25)", GBP),
        ("assoc_nic_increase", "Increase in employer NIC per associate", "=assoc_nic/assoc_nic_old-1", PCT),
        ("assoc_pension", "Employer pension per associate",
         "=IF(assoc_earnings<pension_trigger,0,pension_employer_rate*MAX(0,MIN(assoc_earnings,pension_qe_upper)-pension_qe_lower))", GBP),
        ("assoc_cost_per_hour", "Associate cost per hour worked (pay, holiday, NIC, pension)",
         "=(assoc_earnings+assoc_nic+assoc_pension)/(associate_contract_hours_per_week*52)", "0.00"),
        ("sm_cost", "Store manager total cost",
         "=store_manager_salary+employer_nic_rate*MAX(0,store_manager_salary-nic_secondary_threshold)"
         "+IF(store_manager_salary<pension_trigger,0,pension_employer_rate*MAX(0,MIN(store_manager_salary,pension_qe_upper)-pension_qe_lower))", GBP),
        ("am_cost", "Assistant manager total cost",
         "=assistant_manager_salary+employer_nic_rate*MAX(0,assistant_manager_salary-nic_secondary_threshold)"
         "+IF(assistant_manager_salary<pension_trigger,0,pension_employer_rate*MAX(0,MIN(assistant_manager_salary,pension_qe_upper)-pension_qe_lower))", GBP),
        ("managers_cost", "Managers total cost", "=IF(managers>=1,sm_cost,0)+IF(managers>=2,am_cost,0)", GBP),
        ("fixed_assoc_hours_week", "Fixed associate hours per week",
         "=MAX(0,trading_hours_per_week*floor_cover+non_trading_hours_per_week-managers*manager_floor_hours_per_week)", "0.0"),
        ("fixed_payroll", "Fixed payroll per year", "=managers_cost+fixed_assoc_hours_week*52*assoc_cost_per_hour", GBP),
        ("variable_cost_per_k", "Variable payroll per GBP 1,000 of sales volume", "=variable_hours_per_k_sales*assoc_cost_per_hour", "0.00"),
    ]
    _header(ws, 4, ["Item", "Description", "Value"])
    for i, (key, desc, formula, fmt) in enumerate(rows, start=5):
        ws.cell(i, 1, key)
        ws.cell(i, 2, desc)
        c = ws.cell(i, 3, formula)
        c.number_format = fmt
        _name(wb, key, f"Payroll!$C${i}")
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width, ws.column_dimensions["C"].width = 26, 62, 14


# Block rows (offsets from block top). Each block is a full store cash-flow model for one case.
BLOCK_ROWS = [
    "year", "trading", "ramp", "volume", "growth", "sales", "gross_margin", "wage_index", "payroll", "rent",
    "cost_index", "rates", "occupancy_other", "other_opex", "store_ebitda", "pre_opening", "capex",
    "tax_depreciation", "dilapidations", "taxable", "tax", "stock_held", "wc_change", "fcf",
    "discount_factor", "pv", "cumulative", "payback_part",
]
LABELS = {
    "year": "Year", "trading": "Trading year flag", "ramp": "Ramp-up (share of mature volume)",
    "volume": "Sales volume (year-1 prices)", "growth": "Sales growth index", "sales": "Sales",
    "gross_margin": "Gross margin", "wage_index": "Wage index", "payroll": "Payroll", "rent": "Rent",
    "cost_index": "Cost index", "rates": "Business rates", "occupancy_other": "Service charge, utilities, insurance",
    "other_opex": "Other store opex", "store_ebitda": "Store EBITDA (4-wall)", "pre_opening": "Pre-opening costs",
    "capex": "Fit-out capex", "tax_depreciation": "Tax depreciation", "dilapidations": "Dilapidations",
    "taxable": "Taxable profit", "tax": "Tax (negative = group relief)", "stock_held": "Stock held",
    "wc_change": "Change in stock", "fcf": "Free cash flow", "discount_factor": "Discount factor",
    "pv": "Present value", "cumulative": "Cumulative cash flow", "payback_part": "Payback helper (months)",
}
PARAMS = ["density", "gm", "rent", "capex", "ramp1", "ramp2", "rent_mult", "payroll_mult", "ramp_mult"]
SUMMARY = ["npv", "irr", "payback_months"]


def _write_block(ws, top: int, title: str, params: dict[str, str], fmt: bool = False) -> dict[str, str]:
    """Write one case block starting at row `top`. Returns absolute refs to its summary cells."""
    ws.cell(top, 1, title).font = BOLD
    # parameters (formulas pointing at Inputs, or overrides)
    p_ref = {}
    for i, key in enumerate(PARAMS):
        r = top + 1 + i
        ws.cell(r, 1, f"param: {key}")
        ws.cell(r, 2, params[key])
        p_ref[key] = f"$B${r}"
    base = top + 1 + len(PARAMS) + 1
    rr = {name: base + i for i, name in enumerate(BLOCK_ROWS)}
    first, last = 3, 3 + MAXY  # columns C..R hold years 0..15
    for name, r in rr.items():
        ws.cell(r, 1, LABELS[name])
    for j in range(MAXY + 1):
        c = first + j
        L = col(c)
        nxt = col(c + 1)
        prv = col(c - 1)
        R = lambda name: f"{L}{rr[name]}"  # noqa: E731
        f = {
            "year": j,
            "trading": f"=IF(AND({R('year')}>=1,{R('year')}<=lease_term_years),1,0)",
            "ramp": f"=IF({R('year')}=1,1-(1-{p_ref['ramp1']})*{p_ref['ramp_mult']},IF({R('year')}=2,1-(1-{p_ref['ramp2']})*{p_ref['ramp_mult']},1))*{R('trading')}",
            "volume": f"=area_sqft*{p_ref['density']}*{R('ramp')}",
            "growth": f"=IF({R('trading')}=1,(1+sales_growth)^({R('year')}-1),0)",
            "sales": f"={R('volume')}*{R('growth')}",
            "gross_margin": f"={R('sales')}*{p_ref['gm']}",
            "wage_index": f"=IF({R('trading')}=1,(1+wage_inflation)^({R('year')}-1),0)",
            "payroll": f"=(fixed_payroll*{R('trading')}+variable_cost_per_k*{R('volume')}/1000)*{R('wage_index')}*{p_ref['payroll_mult']}",
            "rent": f"={p_ref['rent']}*(1+IF({R('year')}>=6,rent_review_uplift,0))*{R('trading')}*{p_ref['rent_mult']}",
            "cost_index": f"=IF({R('trading')}=1,(1+cost_inflation)^({R('year')}-1),0)",
            "rates": f"=rateable_value*IF(rateable_value<51000,rates_multiplier_rhl_small,IF(rateable_value<500000,rates_multiplier_rhl_standard,rates_multiplier_high_value))*{R('cost_index')}",
            "occupancy_other": f"=occupancy_other_psf*area_sqft*{R('cost_index')}",
            "other_opex": f"={R('sales')}*other_opex_pct_sales",
            "store_ebitda": f"={R('gross_margin')}-{R('payroll')}-{R('rent')}-{R('rates')}-{R('occupancy_other')}-{R('other_opex')}",
            "pre_opening": f"=IF({R('year')}=0,pre_opening_costs,0)",
            "capex": f"=IF({R('year')}=0,{p_ref['capex']},0)",
            "tax_depreciation": f"=IF(AND({R('year')}>=1,{R('year')}<=tax_depreciation_years,{R('year')}<=lease_term_years),{p_ref['capex']}/tax_depreciation_years,0)",
            "dilapidations": f"=IF({R('year')}=lease_term_years,dilapidations_at_exit,0)",
            "taxable": f"={R('store_ebitda')}-{R('pre_opening')}-{R('tax_depreciation')}-{R('dilapidations')}",
            "tax": f"={R('taxable')}*tax_rate",
            "stock_held": (f"=IF({R('year')}<lease_term_years,stock_pct_sales*{nxt}{rr['sales']},0)" if j < MAXY else "=0"),
            "wc_change": (f"={R('stock_held')}" if j == 0 else f"={R('stock_held')}-{prv}{rr['stock_held']}"),
            "fcf": f"={R('store_ebitda')}-{R('pre_opening')}-{R('tax')}-{R('capex')}-{R('wc_change')}-{R('dilapidations')}",
            "discount_factor": f"=1/(1+discount_rate)^{R('year')}",
            "pv": f"={R('fcf')}*{R('discount_factor')}",
            "cumulative": (f"={R('fcf')}" if j == 0 else f"={prv}{rr['cumulative']}+{R('fcf')}"),
            "payback_part": ("=0" if j == 0 else
                             f"=IF(AND({prv}{rr['cumulative']}<0,{R('cumulative')}>=0),({R('year')}-1+(-{prv}{rr['cumulative']})/{R('fcf')})*12,0)"),
        }
        for name, formula in f.items():
            cell = ws.cell(rr[name], c, formula)
            if fmt:
                cell.number_format = {"ramp": PCT, "growth": "0.000", "wage_index": "0.000", "cost_index": "0.000",
                                      "discount_factor": "0.000", "trading": "0", "year": "0",
                                      "payback_part": "0.0"}.get(name, GBP)
    span = f"$C${{r}}:${col(last)}${{r}}"
    s_row = rr["payback_part"] + 2
    refs = {}
    summ = {
        "npv": f"=SUM({span.format(r=rr['pv'])})",
        "irr": f"=IRR({span.format(r=rr['fcf'])})",
        "payback_months": f"=IF(SUM({span.format(r=rr['payback_part'])})=0,\"n/a\",SUM({span.format(r=rr['payback_part'])}))",
    }
    for i, (k, formula) in enumerate(summ.items()):
        ws.cell(s_row + i, 1, k).font = BOLD
        c = ws.cell(s_row + i, 2, formula)
        c.number_format = {"npv": GBP, "irr": PCT, "payback_months": "0.0"}[k]
        refs[k] = f"'{ws.title}'!$B${s_row + i}"
    refs["_rows"] = rr
    refs["_next_top"] = s_row + len(summ) + 2
    refs["_params"] = {k: f"'{ws.title}'!{v}" for k, v in p_ref.items()}
    return refs


def _base_params() -> dict[str, str]:
    return {"density": "=mature_sales_density", "gm": "=product_gross_margin", "rent": "=rent_per_year",
            "capex": "=fitout_capex", "ramp1": "=ramp_year1", "ramp2": "=ramp_year2",
            "rent_mult": 1, "payroll_mult": 1, "ramp_mult": 1}


def _scenario_params(cfg: dict, name: str) -> dict[str, str]:
    p = _base_params()
    key_map = {"mature_sales_density": "density", "product_gross_margin": "gm", "rent_per_year": "rent",
               "fitout_capex": "capex", "ramp_year1": "ramp1", "ramp_year2": "ramp2"}
    for k, which in cfg["scenarios"][name].items():
        p[key_map[k]] = f"={k}_{which}"
    return p


def build_store_workbook(cfg: dict | None = None):
    cfg = cfg or store_model.load_config()
    wb = Workbook()
    _inputs_sheet(wb, cfg)
    _payroll_sheet(wb)

    # Presentation sheet: base case.
    ws = wb.create_sheet("Store P&L")
    ws["A1"], ws["A1"].font = "Base case: store 4-wall P&L and cash flow (GBP, nominal)", TITLE
    ws["A2"], ws["A2"].font = DISCLAIMER, NOTE
    base_refs = _write_block(ws, 4, "Base case", _base_params(), fmt=True)
    ws.column_dimensions["A"].width = 38
    for c in range(2, 3 + MAXY + 1):
        ws.column_dimensions[col(c)].width = 11
    ws.freeze_panes = "C5"

    # Engine: break-even helper blocks, scenarios and tornado cases.
    eng = wb.create_sheet("Engine")
    eng["A1"], eng["A1"].font = "Engine: one full cash-flow block per case (same formulas as Store P&L)", TITLE
    top = 3
    blocks = {}

    def add(key: str, title: str, params: dict) -> None:
        nonlocal top
        refs = _write_block(eng, top, title, params)
        blocks[key] = refs
        top = refs["_next_top"]

    p = _base_params()
    p["density"] = "=mature_sales_density+100"
    add("base_plus100", "Base, density + 100 (break-even helper)", p)
    for name in ("downside", "upside"):
        add(name, f"Scenario: {name}", _scenario_params(cfg, name))
        p = _scenario_params(cfg, name)
        p["density"] = p["density"] + "+100"
        add(f"{name}_plus100", f"Scenario: {name}, density + 100", p)
    shock = float(cfg["tornado"]["shock"])
    for d in cfg["tornado"]["drivers"]:
        for side, m in (("low", 1 - shock), ("high", 1 + shock)):
            p = _base_params()
            if d == "mature_sales_density":
                p["density"] = f"=mature_sales_density*{m}"
            elif d == "product_gross_margin":
                p["gm"] = f"=product_gross_margin*{m}"
            elif d == "rent_per_year":
                p["rent_mult"] = m
            elif d == "payroll":
                p["payroll_mult"] = m
            elif d == "ramp_speed":
                p["ramp_mult"] = round(2 - m, 10)
            add(f"tornado_{d}_{side}", f"Tornado: {d} {side} ({'-' if side == 'low' else '+'}{shock:.0%})", p)
    eng.column_dimensions["A"].width = 38

    # Returns
    rt = wb.create_sheet("Returns", 3)
    rt["A1"], rt["A1"].font = "Returns, break-even and checks", TITLE
    rt["A2"], rt["A2"].font = DISCLAIMER, NOTE
    _header(rt, 4, ["Metric", "Base", "Downside", "Upside"])

    def be(npv0: str, npv1: str, d0: str) -> str:
        return f"={d0}-{npv0}*100/({npv1}-{npv0})"

    mets = [
        ("NPV (GBP)", "npv", GBP), ("IRR", "irr", PCT), ("Payback (months)", "payback_months", "0.0"),
    ]
    sc_refs = {"Base": base_refs, "Downside": blocks["downside"], "Upside": blocks["upside"]}
    for i, (lab, key, fmt) in enumerate(mets, start=5):
        rt.cell(i, 1, lab)
        for j, sc in enumerate(("Base", "Downside", "Upside"), start=2):
            c = rt.cell(i, j, f"={sc_refs[sc][key]}")
            c.number_format = fmt
    rt.cell(8, 1, "Break-even mature sales density (GBP / sq ft / yr, year-1 prices)").font = BOLD
    for j, (sc, plus) in enumerate((("Base", "base_plus100"), ("Downside", "downside_plus100"),
                                    ("Upside", "upside_plus100")), start=2):
        c = rt.cell(8, j, be(sc_refs[sc]["npv"], blocks[plus]["npv"], sc_refs[sc]["_params"]["density"]))
        c.number_format = '#,##0'
    rt.cell(9, 1, "Break-even mature sales (GBP / yr, year-1 prices)")
    for j in range(2, 5):
        rt.cell(9, j, f"={col(j)}8*area_sqft").number_format = GBP
    rt.cell(10, 1, "Assumed mature sales density")
    for j, sc in enumerate(("Base", "Downside", "Upside"), start=2):
        rt.cell(10, j, f"={sc_refs[sc]['_params']['density']}").number_format = '#,##0'
    rt.cell(11, 1, "Headroom: assumed density / break-even - 1")
    for j in range(2, 5):
        rt.cell(11, j, f"={col(j)}10/{col(j)}8-1").number_format = PCT
    rows = base_refs["_rows"]
    yr3 = f"'Store P&L'!$F${{r}}"  # year 3 = column F
    rt.cell(13, 1, "Base case at maturity (year 3)").font = BOLD
    kpis = [
        ("Sales", f"={yr3.format(r=rows['sales'])}", GBP),
        ("Store EBITDA margin (4-wall)", f"={yr3.format(r=rows['store_ebitda'])}/{yr3.format(r=rows['sales'])}", PCT),
        ("Payroll % sales", f"={yr3.format(r=rows['payroll'])}/{yr3.format(r=rows['sales'])}", PCT),
        ("Occupancy % sales (rent, rates, service charge)",
         f"=({yr3.format(r=rows['rent'])}+{yr3.format(r=rows['rates'])}+{yr3.format(r=rows['occupancy_other'])})/{yr3.format(r=rows['sales'])}", PCT),
    ]
    for i, (lab, formula, fmt) in enumerate(kpis, start=14):
        rt.cell(i, 1, lab)
        rt.cell(i, 2, formula).number_format = fmt

    rt.cell(19, 1, "Checks (all must be TRUE)").font = BOLD
    span = lambda r: f"'Store P&L'!$C${r}:$R${r}"  # noqa: E731
    checks = [
        ("Stock fully released by lease end", f"=ABS(SUM({span(rows['wc_change'])}))<0.01"),
        ("Tax = rate x taxable profit", f"=ABS(SUM({span(rows['tax'])})-tax_rate*SUM({span(rows['taxable'])}))<0.01"),
        ("FCF identity", f"=ABS(SUM({span(rows['fcf'])})-(SUM({span(rows['store_ebitda'])})-SUM({span(rows['pre_opening'])})"
                         f"-SUM({span(rows['tax'])})-SUM({span(rows['capex'])})-SUM({span(rows['dilapidations'])})))<0.01"),
        ("Downside NPV < base NPV < upside NPV", "=AND(C5<B5,B5<D5)"),
        ("IRR above discount rate exactly when NPV > 0", "=(B6>discount_rate)=(B5>0)"),
    ]
    for i, (lab, formula) in enumerate(checks, start=20):
        rt.cell(i, 1, lab)
        rt.cell(i, 2, formula)
    rt.cell(26, 1, "ALL CHECKS").font = BOLD
    c = rt.cell(26, 2, f"=AND(B20:B{19 + len(checks)})")
    c.fill, c.font = CHECK_FILL, BOLD
    rt.column_dimensions["A"].width = 62
    for L in "BCD":
        rt.column_dimensions[L].width = 16

    # Sensitivity
    st = wb.create_sheet("Sensitivity", 4)
    st["A1"], st["A1"].font = f"Tornado: NPV with one driver moved +/-{shock:.0%} (all else base)", TITLE
    st["A2"], st["A2"].font = ("Ramp-up speed +/-20% scales the year-1 and year-2 shortfall to maturity. "
                               "A +/-20% gross-margin swing (57%-85%) is a stress, far wider than the 70.0%-71.0% product margin the FY21-FY22 filings show."), NOTE
    _header(st, 4, ["Driver", "NPV low case", "NPV high case", "Base NPV", "Swing (high - low)"])
    for i, d in enumerate(cfg["tornado"]["drivers"], start=5):
        st.cell(i, 1, d)
        st.cell(i, 2, f"={blocks[f'tornado_{d}_low']['npv']}").number_format = GBP
        st.cell(i, 3, f"={blocks[f'tornado_{d}_high']['npv']}").number_format = GBP
        st.cell(i, 4, f"={base_refs['npv']}").number_format = GBP
        st.cell(i, 5, f"=C{i}-B{i}").number_format = GBP
    st.column_dimensions["A"].width = 26
    for L in "BCDE":
        st.column_dimensions[L].width = 16

    wb._sheets = [wb["Inputs"], wb["Payroll"], wb["Store P&L"], wb["Returns"], wb["Sensitivity"], wb["Engine"]]
    return wb, {"base": base_refs, **blocks}


# --------------------------------------------------------------------------------------------
# Bridge workbook
# --------------------------------------------------------------------------------------------

BRIDGE_ITEMS = [
    ("turnover", "Turnover"), ("cost_of_sales", "Cost of sales"), ("admin_expenses", "Administrative expenses"),
    ("other_operating_income", "Other operating income"), ("interest_receivable", "Interest receivable"),
    ("interest_payable", "Interest payable"), ("profit_before_tax", "Profit before tax"),
    ("staff_costs_total", "Staff costs (note 8)"), ("operating_lease_rentals", "Operating lease rentals (note 6)"),
    ("depreciation", "Depreciation (note 6)"), ("amortisation", "Amortisation (note 6)"),
    ("impairment_tangible", "Impairment of tangible assets (note 6)"),
    ("fx_differences", "Exchange differences, charge / (credit) (note 6)"),
]


def build_bridge_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "Bridge"
    ws["A1"], ws["A1"].font = "Profit bridges PBT(t-1) to PBT(t), GBP 000", TITLE
    ws["A2"], ws["A2"].font = ("Each bridge uses filing t (current and comparative columns). Blue = figure transcribed from the "
                               "filed accounts (see Data sheet for page references); black = formula. Gross margin is after all "
                               "retail-channel costs (accounts note 2.6), so it is not a product margin."), NOTE
    out_refs = {}
    r = 4
    for prev, cur in bridge.PAIRS:
        ws.cell(r, 1, f"FY{prev % 100} -> FY{cur % 100} (source: FY{cur % 100} accounts)").font = BOLD
        _header(ws, r + 1, ["Line", f"FY{prev % 100}", f"FY{cur % 100}"])
        refs = {}
        for i, (item, lab) in enumerate(BRIDGE_ITEMS, start=r + 2):
            ws.cell(i, 1, lab)
            for c, per in ((2, prev), (3, cur)):
                cell = ws.cell(i, c, ledger.value(item, per, cur))
                cell.font, cell.number_format = BLUE, GBP
            refs[item] = i
        d = r + 2 + len(BRIDGE_ITEMS)
        derived = [
            ("gm", "Gross margin rate", "=({c}{t}-{c}{cos})/{c}{t}", PCT),
            ("da", "D&A and impairment", "={c}{dep}+{c}{am}+{c}{imp}", GBP),
            ("other", "Other operating costs pool", "={c}{cos}+{c}{adm}-{c}{st}-{c}{ls}-{c}{da}-{c}{fx}", GBP),
            ("other_rate", "Other operating costs % turnover", "={c}{other}/{c}{t}", PCT),
            ("nf", "Net finance income", "={c}{ir}-{c}{ip}", GBP),
        ]
        dref = {}
        for k, (key, lab, tmpl, fmt) in enumerate(derived):
            row = d + k
            dref[key] = row
            ws.cell(row, 1, lab)
            for c in ("B", "C"):
                ws[f"{c}{row}"] = tmpl.format(c=c, t=refs["turnover"], cos=refs["cost_of_sales"],
                                             dep=refs["depreciation"], am=refs["amortisation"],
                                             imp=refs["impairment_tangible"], adm=refs["admin_expenses"],
                                             st=refs["staff_costs_total"], ls=refs["operating_lease_rentals"],
                                             da=dref.get("da", 0), fx=refs["fx_differences"],
                                             other=dref.get("other", 0), ir=refs["interest_receivable"],
                                             ip=refs["interest_payable"])
                ws[f"{c}{row}"].number_format = fmt
        T, pbt = refs["turnover"], refs["profit_before_tax"]
        func = [
            ("Sales effect (at prior-year GM rate)", f"=(C{T}-B{T})*B{dref['gm']}"),
            ("Gross-margin-rate effect", f"=(C{dref['gm']}-B{dref['gm']})*C{T}"),
            ("Administrative expenses", f"=-(C{refs['admin_expenses']}-B{refs['admin_expenses']})"),
            ("Other operating income", f"=C{refs['other_operating_income']}-B{refs['other_operating_income']}"),
            ("Net finance income", f"=C{dref['nf']}-B{dref['nf']}"),
        ]
        nat = [
            ("Sales effect (at prior-year contribution rate)", f"=(C{T}-B{T})*(1-B{dref['other_rate']})"),
            ("Other operating costs: rate effect", f"=-(C{dref['other_rate']}-B{dref['other_rate']})*C{T}"),
            ("Staff costs", f"=-(C{refs['staff_costs_total']}-B{refs['staff_costs_total']})"),
            ("Operating lease rentals", f"=-(C{refs['operating_lease_rentals']}-B{refs['operating_lease_rentals']})"),
            ("Depreciation, amortisation, impairment", f"=-(C{dref['da']}-B{dref['da']})"),
            ("Exchange differences", f"=-(C{refs['fx_differences']}-B{refs['fx_differences']})"),
            ("Other operating income", f"=C{refs['other_operating_income']}-B{refs['other_operating_income']}"),
            ("Net finance income", f"=C{dref['nf']}-B{dref['nf']}"),
        ]
        step_rows, checks = {}, {}
        b = d + len(derived) + 1
        for basis, title, steps in (("function", "Function view (face of the P&L)", func),
                                    ("nature", "Nature view (notes; other operating costs named, not plugged)", nat)):
            _header(ws, b, [title, "GBP 000"])
            ws.cell(b + 1, 1, f"PBT FY{prev % 100}")
            ws.cell(b + 1, 2, f"=B{pbt}").number_format = GBP
            step_rows[basis] = {}
            for k, (lab, formula) in enumerate(steps):
                row = b + 2 + k
                ws.cell(row, 1, lab)
                ws.cell(row, 2, formula).number_format = GBP
                step_rows[basis][lab] = row
            end = b + 2 + len(steps)
            ws.cell(end, 1, f"PBT FY{cur % 100} (bridge)").font = BOLD
            ws.cell(end, 2, f"=SUM(B{b + 1}:B{end - 1})").number_format = GBP
            ws.cell(end + 1, 1, f"PBT FY{cur % 100} (reported)")
            ws.cell(end + 1, 2, f"=C{pbt}").number_format = GBP
            ws.cell(end + 2, 1, "Reconciles to GBP 0").font = BOLD
            cell = ws.cell(end + 2, 2, f"=ABS(B{end}-B{end + 1})<0.001")
            cell.fill = CHECK_FILL
            checks[basis] = end + 2
            b = end + 4
        out_refs[(prev, cur)] = {"steps": step_rows, "checks": checks}
        end = b - 4
        r = end + 4
    ws.column_dimensions["A"].width = 70
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 16

    # Data sheet: every ledger figure with its page reference.
    data = wb.create_sheet("Data")
    data["A1"], data["A1"].font = "Source ledger: figures transcribed from the filed accounts (GBP 000 unless unit says otherwise)", TITLE
    _header(data, 3, ["Filing", "Period", "Line item", "Value", "Unit", "PDF page", "Printed page", "Section", "Note"])
    df = ledger.load()
    for i, row in enumerate(df.itertuples(index=False), start=4):
        vals = [f"FY{row.filing_fy % 100}", f"FY{row.period_fy % 100}", row.line_item, float(row.value), row.unit,
                int(row.pdf_page), int(row.printed_page), row.section, row.note]
        for j, v in enumerate(vals, start=1):
            c = data.cell(i, j, v)
            if j == 4:
                c.font = BLUE
    for j, w in enumerate((8, 8, 30, 12, 8, 9, 11, 50, 60), start=1):
        data.column_dimensions[col(j)].width = w
    data.freeze_panes = "A4"

    # Ratios: formulas over a compact year table.
    rs = wb.create_sheet("Ratios")
    rs["A1"], rs["A1"].font = "Ratios FY22-FY25 (each year from its own filing)", TITLE
    items = ["turnover", "cost_of_sales", "admin_expenses", "operating_profit", "profit_before_tax", "adjusted_ebitda",
             "staff_costs_total", "wages_salaries", "social_security", "operating_lease_rentals", "employees_total",
             "employees_store", "standalone_stores", "stocks", "stock_provision"]
    _header(rs, 3, ["Line item"] + [f"FY{y % 100}" for y in ledger.FISCAL_YEARS])
    pos = {}
    for i, item in enumerate(items, start=4):
        rs.cell(i, 1, item)
        for j, y in enumerate(ledger.FISCAL_YEARS, start=2):
            c = rs.cell(i, j, ledger.value(item, y, y))
            c.font, c.number_format = BLUE, GBP
        pos[item] = i
    rr = 4 + len(items) + 1
    _header(rs, rr, ["Ratio"] + [f"FY{y % 100}" for y in ledger.FISCAL_YEARS])
    ratio_formulas = [
        ("Gross margin (after retail-channel costs)", "=({c}{turnover}-{c}{cost_of_sales})/{c}{turnover}", PCT),
        ("Admin % sales", "={c}{admin_expenses}/{c}{turnover}", PCT),
        ("Operating margin", "={c}{operating_profit}/{c}{turnover}", PCT),
        ("PBT margin", "={c}{profit_before_tax}/{c}{turnover}", PCT),
        ("Adjusted EBITDA margin", "={c}{adjusted_ebitda}/{c}{turnover}", PCT),
        ("Staff costs % sales", "={c}{staff_costs_total}/{c}{turnover}", PCT),
        ("Employer social security % wages", "={c}{social_security}/{c}{wages_salaries}", PCT),
        ("Lease rentals % sales", "={c}{operating_lease_rentals}/{c}{turnover}", PCT),
        ("Lease rentals per standalone store (upper bound)", "={c}{operating_lease_rentals}/{c}{standalone_stores}", GBP1),
        ("Turnover per average employee (per head)", "={c}{turnover}/{c}{employees_total}", GBP1),
        ("Stock / turnover", "={c}{stocks}/{c}{turnover}", PCT),
        ("Stock cover (weeks of turnover)", "={c}{stocks}/({c}{turnover}/52)", "0.0"),
        ("Stock provision % gross stock", "={c}{stock_provision}/({c}{stocks}+{c}{stock_provision})", PCT),
    ]
    for k, (lab, tmpl, fmt) in enumerate(ratio_formulas, start=rr + 1):
        rs.cell(k, 1, lab)
        for j in range(2, 2 + len(ledger.FISCAL_YEARS)):
            c = col(j)
            rs.cell(k, j, tmpl.format(c=c, **pos)).number_format = fmt
    rs.column_dimensions["A"].width = 48
    wb._sheets = [wb["Bridge"], wb["Ratios"], wb["Data"]]
    return wb, out_refs


def run() -> None:
    paths.ensure_dirs()
    wb, _ = build_store_workbook()
    wb.save(paths.OUTPUTS / "store_model.xlsx")
    wb2, _ = build_bridge_workbook()
    wb2.save(paths.OUTPUTS / "bridge.xlsx")


if __name__ == "__main__":
    run()
