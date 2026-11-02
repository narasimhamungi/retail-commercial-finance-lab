"""Generate CSV outputs, the docs (registry, discrepancies, assumptions, findings) and the
two-page performance review PDF. All numbers in the prose are computed here, not typed."""

from __future__ import annotations

import hashlib

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from PIL import Image as PILImage
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from . import bridge, extract, ledger, market, paths, ratios, store_model

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history"
ONS_URL = "https://www.ons.gov.uk/datasets/retail-sales-index/editions/time-series/versions/45"
FILING_LINKS = {
    2022: "MzM4ODI5NzQzOWFkaXF6a2N4", 2023: "MzQyOTM0MTA4MGFkaXF6a2N4",
    2024: "MzQ4MDQzNDYxMmFkaXF6a2N4", 2025: "MzUzNzU1NTE3MGFkaXF6a2N4",
}
# Press figures supplied in the build brief, used only as a cross-check (the filing wins).
PRESS = [
    ("FY22 turnover (GBP m)", 143.7, lambda: ledger.value("turnover", 2022) / 1000),
    ("FY22 turnover growth (%)", 22.0, lambda: (ledger.value("turnover", 2022) / ledger.value("turnover", 2021, 2022) - 1) * 100),
    ("FY23 turnover (GBP m)", 139.8, lambda: ledger.value("turnover", 2023) / 1000),
    ("FY23 turnover growth (%)", -2.7, lambda: (ledger.value("turnover", 2023) / ledger.value("turnover", 2022, 2023) - 1) * 100),
    ("FY24 turnover (GBP m)", 134.7, lambda: ledger.value("turnover", 2024) / 1000),
    ("FY24 turnover growth (%)", -3.6, lambda: (ledger.value("turnover", 2024) / ledger.value("turnover", 2023, 2024) - 1) * 100),
    ("FY24 PBT (GBP m)", 14.2, lambda: ledger.value("profit_before_tax", 2024) / 1000),
    ("FY24 PBT growth (%)", -40.0, lambda: (ledger.value("profit_before_tax", 2024) / ledger.value("profit_before_tax", 2023, 2024) - 1) * 100),
    ("FY24 PAT (GBP m)", 10.6, lambda: ledger.value("profit_after_tax", 2024) / 1000),
    ("FY24 adjusted EBITDA (GBP m)", 15.9, lambda: ledger.value("adjusted_ebitda", 2024) / 1000),
    ("FY24 standalone stores", 54, lambda: ledger.value("standalone_stores", 2024)),
    ("FY24 concession stores", 48, lambda: ledger.value("concession_stores", 2024)),
]
# Inconsistencies inside a single filing, found while transcribing (not detectable from comparatives).
INTERNAL = [
    ("FY23", "Provisions on the balance sheet are 1,043k (pdf p.19); note 3 gives the dilapidations provision as 1,044k (pdf p.31). "
             "GBP 1k rounding difference; the balance-sheet figure is used."),
    ("FY21 (out of scope)", "FY22 accounts show FY21 exchange differences as (237) in note 6 (pdf p.34) but (239) in the KPI "
                            "reconciliation (pdf p.5), so FY21 adjusted EBITDA (28,007) does not rebuild exactly (28,009). "
                            "FY21 is outside the FY22-FY25 scope and not used."),
    ("FY22", "Employee categories are labelled 'Support staff' and 'Client service staff' (pdf p.35); from FY23 they are "
             "'Administrative staff' and 'Store staff'. Treated as the same categories."),
]


def m(x: float, dp: int = 1) -> str:
    return f"GBP {x / 1000:,.{dp}f}m"


def pct(x: float, dp: int = 1) -> str:
    return f"{x * 100:.{dp}f}%"


def sha256(p) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --------------------------------------------------------------------------------------------
# Numbers used in the prose
# --------------------------------------------------------------------------------------------

def facts() -> dict:
    v = ledger.value
    rt = ratios.build().set_index("fiscal_year")
    br = bridge.build()
    mk = market.relative_performance().set_index("fiscal_year")
    cfg = store_model.load_config()
    sm = store_model.summary(cfg)

    def step(to_fy, name, basis="nature"):
        s = br[(br.basis == basis) & (br.to_fy == to_fy) & (br.step == name)]
        return float(s.value_k.iloc[0])

    d_pbt = {y: v("profit_before_tax", y, y) - v("profit_before_tax", y - 1, y) for y in (2023, 2024, 2025)}
    other = "Other operating costs: rate effect"
    pr = store_model.run(store_model.scenario_case(cfg, "base")).extras["payroll"]
    f = dict(
        rev22=v("turnover", 2022), rev24=v("turnover", 2024), rev25=v("turnover", 2025),
        pbt22=v("profit_before_tax", 2022), pbt24=v("profit_before_tax", 2024), pbt25=v("profit_before_tax", 2025),
        rev_chg_22_24=v("turnover", 2024) / v("turnover", 2022) - 1,
        pbt_chg_22_24=v("profit_before_tax", 2024) / v("profit_before_tax", 2022) - 1,
        rev_g25=rt.loc[2025, "revenue_growth"],
        pbt_g25=v("profit_before_tax", 2025) / v("profit_before_tax", 2024, 2025) - 1,
        dec23=rt.loc[2023, "op_change_per_revenue_change"], dec24=rt.loc[2024, "op_change_per_revenue_change"],
        inc25=rt.loc[2025, "op_change_per_revenue_change"],
        oth22=rt.loc[2022, "other_cost_pct_sales"], oth24=rt.loc[2024, "other_cost_pct_sales"],
        oth25=rt.loc[2025, "other_cost_pct_sales"],
        oth_eff23=step(2023, other), oth_eff24=step(2024, other), oth_eff25=step(2025, other),
        share23=step(2023, other) / d_pbt[2023], share24=step(2024, other) / d_pbt[2024],
        dpbt23=d_pbt[2023], dpbt24=d_pbt[2024], dpbt25=d_pbt[2025],
        cogs_pct22=v("cost_of_stock_expensed", 2022) / v("turnover", 2022),
        pgm22=rt.loc[2022, "product_gross_margin"],
        conc24=v("concession_sales_growth_pct", 2024), owned24=v("owned_mix_change_ppt", 2024),
        online25=v("online_mix_change_ppt", 2025),
        staff24c=v("staff_costs_total", 2024, 2025), staff25=v("staff_costs_total", 2025),
        store_staff24=v("employees_store", 2024), store_staff25=v("employees_store", 2025),
        ss24_orig=rt.loc[2024, "employer_ss_pct_wages"], ss25=rt.loc[2025, "employer_ss_pct_wages"],
        ss24_rest=v("social_security", 2024, 2025) / v("wages_salaries", 2024, 2025),
        nic_old=pr.associate_nic_2024_25, nic_new=pr.associate_nic,
        stock23=v("stocks", 2023), stock24=v("stocks", 2024), stock25=v("stocks", 2025),
        cover23=rt.loc[2023, "stock_cover_weeks"], cover24=rt.loc[2024, "stock_cover_weeks"],
        cover25=rt.loc[2025, "stock_cover_weeks"],
        prov22=rt.loc[2022, "stock_provision_pct_gross"], prov25=rt.loc[2025, "stock_provision_pct_gross"],
        prov25k=v("stock_provision", 2025),
        rev_g24=rt.loc[2024, "revenue_growth"],
        mk=mk, rt=rt, sm=sm, cfg=cfg,
        fx25=v("fx_differences", 2025), fx24=v("fx_differences", 2024), fx23=v("fx_differences", 2023),
        adj25=v("adjusted_ebitda", 2025),
    )
    f["staff_g25"] = f["staff25"] / f["staff24c"] - 1
    f["pool22"], f["pool24"] = bridge.pools(2022)["other_costs"], bridge.pools(2024)["other_costs"]
    base_run = store_model.run(store_model.scenario_case(cfg, "base"))
    f["fourwall_base"] = base_run.extras["four_wall_margin_maturity"]
    return f


def nic_weeks_fy25() -> int:
    # 6 April 2025 to 27 December 2025 inclusive of the period end.
    return int((pd.Timestamp("2025-12-27") - pd.Timestamp("2025-04-06")).days / 7 + 0.5)


# --------------------------------------------------------------------------------------------
# Markdown docs
# --------------------------------------------------------------------------------------------

def findings_md(f: dict) -> str:
    mk, sm = f["mk"], f["sm"]
    b, d = sm["base"], sm["downside"]
    cfg = f["cfg"]
    dn = cfg["scenarios"]["downside"]
    bnd = lambda k: store_model.bound(cfg, k, dn[k])  # noqa: E731
    wk = nic_weeks_fy25()
    return f"""# Findings: Mint Velvet (Sabre Retail Fashion Ltd), FY22-FY25

Independent analysis of public filings. Figures in GBP; page references are to the filed PDFs in `data/raw/` (pdf page; printed page in `docs/source_registry.md`).

**1. Each pound of lost sales cost about two pounds of operating profit.** Turnover fell {pct(-f['rev_chg_22_24'])} from FY22 to FY24 ({m(f['rev22'])} to {m(f['rev24'])}) while PBT fell {pct(-f['pbt_chg_22_24'])} ({m(f['pbt22'])} to {m(f['pbt24'])}). Each GBP 1 of lost turnover cost GBP {f['dec23']:.2f} of operating profit in FY23 and GBP {f['dec24']:.2f} in FY24, because costs kept rising as sales fell. In FY25 turnover rose {pct(f['rev_g25'])} to {m(f['rev25'])} and PBT {pct(f['pbt_g25'])} to {m(f['pbt25'])}: GBP {f['inc25']:.2f} of operating profit per extra GBP 1 of sales. (P&L: FY23 accounts p.17, FY24 p.17, FY25 p.18.)

**2. The fall came from the 'other operating costs' pool, not payroll or rent.** Costs outside staff, rent, D&A and FX rose from {pct(f['oth22'])} of turnover in FY22 to {pct(f['oth24'])} in FY24. The rate change took {m(-f['oth_eff23'])} off PBT in FY23 ({pct(f['share23'], 0)} of a {m(-f['dpbt23'])} fall) and {m(-f['oth_eff24'])} in FY24 ({pct(f['share24'], 0)} of {m(-f['dpbt24'])}); it added back {m(f['oth_eff25'])} in FY25 as the ratio eased to {pct(f['oth25'])}. This is not just fixed costs spread over lower sales: the pool grew by {m(f['pool24'] - f['pool22'])} in absolute terms from FY22 to FY24 while turnover fell by {m(f['rev22'] - f['rev24'])}. Staff costs moved by less than GBP 1m in either falling year. The filings do not split this pool. FY22 is the only year that discloses cost of stock ({pct(f['cogs_pct22'])} of turnover, a {pct(f['pgm22'])} product margin; FY22 p.34), so the rest of the pool (concession commissions, marketing, distribution and similar) was {pct(f['oth22'] - f['cogs_pct22'])} of turnover that year. The FY24 strategic report gives concession sales {f['conc24']:+.1f}% and owned-channel mix +{f['owned24']:.1f}pp (FY24 p.4). That fits a mix shift toward online, with its fulfilment and returns costs, but it does not prove one.

**3. Payroll is now the main cost headwind.** FY25 staff costs rose {pct(f['staff_g25'])} ({m(f['staff24c'])} to {m(f['staff25'])}) against {pct(f['rev_g25'])} turnover growth; average store staff rose from {f['store_staff24']:.0f} to {f['store_staff25']:.0f} (FY25 p.34). Employer social security rose to {pct(f['ss25'])} of wages from {pct(f['ss24_orig'])} in FY24 as originally filed (FY24 p.33). The FY25 filing restates the FY24 split to {pct(f['ss24_rest'])}; see `docs/discrepancies.md`. The April 2025 employer NIC change (15% above GBP 5,000, previously 13.8% above GBP 9,100) covered about {wk} of FY25's 52 weeks, so FY26 carries the full-year effect (inference). For a 20-hour associate at NLW plus 5%, employer NIC rises from GBP {f['nic_old']:,.0f} to GBP {f['nic_new']:,.0f} a year ({pct(f['nic_new'] / f['nic_old'] - 1, 0)}).

**4. Stock built up as sales fell, then ran down.** Year-end stock rose {pct(f['stock24'] / f['stock23'] - 1, 0)} to {m(f['stock24'])} in FY24 while turnover fell {pct(-f['rev_g24'])}: cover went from {f['cover23']:.1f} to {f['cover24']:.1f} weeks of turnover. In FY25 stock was {m(f['stock25'])} ({f['cover25']:.1f} weeks) on {pct(f['rev_g25'])} higher sales. The obsolescence provision reached {m(f['prov25k'], 2)}, {pct(f['prov25'])} of gross stock, up from {pct(f['prov22'])} in FY22 (FY25 p.32, p.40; FY24 p.19).

**5. Against the market: behind in FY23, ahead in FY25.** Turnover growth against the ONS clothing and footwear stores value index (GB): FY23 {mk.loc[2023, 'mint_velvet_turnover_growth'] * 100:+.1f}% vs {mk.loc[2023, 'ons_clothing_stores_value_growth'] * 100:+.1f}% ({mk.loc[2023, 'relative_to_clothing_stores_ppt']:+.1f}ppt); FY24 {mk.loc[2024, 'mint_velvet_turnover_growth'] * 100:+.1f}% vs {mk.loc[2024, 'ons_clothing_stores_value_growth'] * 100:+.1f}% ({mk.loc[2024, 'relative_to_clothing_stores_ppt']:+.1f}ppt); FY25 {mk.loc[2025, 'mint_velvet_turnover_growth'] * 100:+.1f}% vs {mk.loc[2025, 'ons_clothing_stores_value_growth'] * 100:+.1f}% ({mk.loc[2025, 'relative_to_clothing_stores_ppt']:+.1f}ppt). The comparison is indicative: calendar-year averages are set against 52-week fiscal years, and the ONS category average mixes value and premium retailers.

**New-store appraisal (illustrative).** Base costs: a 1,700 sq ft regional-mall unit needs mature sales of GBP {b['break_even_density']:,.0f} per sq ft a year (GBP {b['break_even_density'] * 1700 / 1e6:.2f}m) to return the {pct(store_model.base_inputs(cfg)['discount_rate'], 0)} hurdle over a 10-year lease. Downside costs (rent GBP {bnd('rent_per_year'):,.0f}, fit-out GBP {bnd('fitout_capex'):,.0f}, product margin {pct(bnd('product_gross_margin'), 0)}, slower ramp-up) raise that to GBP {d['break_even_density']:,.0f} per sq ft. The base case implies a {pct(f['fourwall_base'], 0)} four-wall margin at maturity. If internal store P&Ls run lower, the gap most likely sits in the two inputs to replace first: other store opex (an assumed 10% of sales) and rent (an estate-average proxy). The inputs are labelled assumptions or filing proxies (`config/assumptions.yaml`). These are not Mint Velvet's store economics.

**What the data cannot show.** There is no store, channel or like-for-like split, and no product margin after FY22. There is no budget, so there is no variance against budget or forecast. There is no marketing spend, so there is no marketing ROI. Note 2.6 puts all retail-channel costs in cost of sales, so the reported gross margin (FY22 {pct(f['rt'].loc[2022, 'gm_rate'])}, FY25 {pct(f['rt'].loc[2025, 'gm_rate'])}) is a channel contribution margin, not a product margin.
"""


def registry_md(ver: pd.DataFrame) -> str:
    lines = ["# Source registry", "",
             "Every figure used is transcribed from Sabre Retail Fashion Limited's filed accounts (company 07920155, "
             f"trading as Mint Velvet), downloaded from Companies House: {CH_URL}", "",
             "The PDFs are scanned page images with no text layer. Each figure was read off the page image and "
             "recorded in `data/ledger/transcription.csv`. `make extract` then OCRs the cited page (Tesseract, "
             "300 dpi native images) and fails if the number is not on that page. Status key:", "",
             "- `verified`: number found on the cited page by OCR",
             "- `verified_weak`: single-digit number found (any page has single digits; read visually)",
             "- `verified_by_identity`: OCR misread the page (e.g. italic '1' read as '4'), but the figure is the "
             "only unconfirmed term of an accounting identity that holds exactly",
             "- `nil_not_checked`: shown as '-' or not presented; zero cannot be located by OCR", "",
             "## Files", "", "| FY | Period end | File | Pages | SHA-256 | Document link |", "|---|---|---|---|---|---|"]
    for y, p in paths.FILINGS.items():
        n = ledger.load()
        lines.append(f"| FY{y % 100} | {paths.PERIOD_END[y]} | `{p.name}` | 52 weeks | `{sha256(p)[:16]}...` | "
                     f"[PDF]({CH_URL.rsplit('/', 1)[0]}/filing-history/{FILING_LINKS[y]}/document?format=pdf&download=0) |")
    lines += ["", f"ONS Retail Sales Index, time series v45 ({ONS_URL}): `{paths.ONS_RSI.name}`, "
              f"SHA-256 `{sha256(paths.ONS_RSI)[:16]}...`. Open Government Licence v3.0.", "",
              "## Status summary", ""]
    counts = ver.status.value_counts()
    for k, c in counts.items():
        lines.append(f"- {k}: {c}")
    lines += ["", f"Total figures: {len(ver)}.", "", "## Figures", "",
              "| Filing | Period | Line item | Value | Unit | PDF p. | Printed p. | Section | Status |",
              "|---|---|---|---:|---|---:|---:|---|---|"]
    for r in ver.itertuples():
        val = f"{r.value:,.0f}" if float(r.value).is_integer() else f"{r.value}"
        lines.append(f"| FY{r.filing_fy % 100} | FY{r.period_fy % 100} | {r.line_item} | {val} | {r.unit} | "
                     f"{r.pdf_page} | {r.printed_page} | {r.section} | {r.status} |")
    return "\n".join(lines) + "\n"


def store_rollforward() -> list[dict]:
    out = []
    for y in (2023, 2024, 2025):
        for kind in ("standalone", "concession"):
            g = lambda item: ledger.value(item, y) if ledger.has(item, y) else 0.0  # noqa: E731
            implied = ledger.value(f"{kind}_stores", y - 1) + g(f"{kind}_opened") - g(f"{kind}_closed")
            out.append(dict(fy=y, kind=kind, opening=ledger.value(f"{kind}_stores", y - 1),
                            opened=g(f"{kind}_opened"), closed=g(f"{kind}_closed"), implied=implied,
                            reported=ledger.value(f"{kind}_stores", y)))
    return out


def discrepancies_md() -> str:
    d = extract.find_discrepancies()
    lines = ["# Discrepancies", "", "The filed accounts are the source of truth. This file lists every place where "
             "sources disagree.", "", "## 1. Comparatives that differ from the figure originally reported",
             "", "Each bridge uses the later filing's comparative (consistent basis within one set of accounts).", "",
             "| FY | Line item | Originally reported | Comparative next year | Difference | Original | Comparative |",
             "|---|---|---:|---:|---:|---|---|"]
    for r in d.itertuples():
        lines.append(f"| FY{r.fiscal_year % 100} | {r.line_item} | {r.originally_reported:,.0f} | "
                     f"{r.comparative_in_next_filing:,.0f} | {r.difference:+,.0f} | {r.original_ref} | {r.comparative_ref} |")
    lines += ["", "Notes:",
              "- FY24 staff costs: the total (18,074) is unchanged; GBP 205k moves from social security to wages. "
              "On the restated split, employer social security falls to 6.8% of wages in FY24 (8.2% as filed), "
              "which overstates the FY25 step-up. The findings quote both.",
              "- FY22 lease commitments: the FY23 accounts restate the comparative to payments up to break clauses "
              "(note 29 footnote, FY23 pdf p.45). Lease commitments are not compared across the FY22/FY23 boundary.",
              "- FY22 inventory impairment: the FY22 accounts say a GBP 58k net reversal (note 3, pdf p.33); the FY23 "
              "comparative shows (74). Immaterial; inside the bridge's 'other operating costs' pool either way.",
              "", "## 2. Store count roll-forward", "",
              "| FY | Type | Opening | Opened | Closed | Implied closing | Reported closing | Status |",
              "|---|---|---:|---:|---:|---:|---:|---|"]
    for r in store_rollforward():
        ok = "ties" if r["implied"] == r["reported"] else f"does not tie ({r['reported'] - r['implied']:+.0f})"
        lines.append(f"| FY{r['fy'] % 100} | {r['kind']} | {r['opening']:.0f} | {r['opened']:.0f} | {r['closed']:.0f} | "
                     f"{r['implied']:.0f} | {r['reported']:.0f} | {ok} |")
    lines += ["", "FY25 reports 51 concessions with one opening and no closures disclosed, against 48 at the FY24 "
              "year end (FY25 pdf p.4, FY24 pdf p.4). The two-store gap is unexplained in the filings; counts are "
              "used as reported.", "", "## 3. Inconsistencies inside a single filing", ""]
    for fy, txt in INTERNAL:
        lines.append(f"- **{fy}**: {txt}")
    lines += ["", "## 4. Press figures (cross-check only)", "",
              "Press figures quoted in the build brief, compared with the filings at the press figure's rounding.", "",
              "| Figure | Press | Filing | Agrees |", "|---|---:|---:|---|"]
    for lab, press, fn in PRESS:
        val = fn()
        dp = 0 if float(press).is_integer() and "stores" in lab else 1
        agrees = round(val, dp) == round(press, dp)
        lines.append(f"| {lab} | {press:,.{dp}f} | {val:,.{dp + 1}f} | {'yes' if agrees else 'NO'} |")
    return "\n".join(lines) + "\n"


def assumptions_md(cfg: dict) -> str:
    lines = ["# Store model assumptions", "", "Source of truth: `config/assumptions.yaml`. Basis: SOURCED (public "
             "source), FILING_PROXY (derived from the filed accounts; capex, rent and stock proxies are upper bounds), "
             "ASSUMPTION (analyst assumption, to be replaced with internal data).", "",
             "| Section | Input | Value | Unit | Basis | Low | High | Source / derivation |",
             "|---|---|---:|---|---|---:|---:|---|"]
    for sec in store_model.SECTIONS:
        for k, s in cfg[sec].items():
            lines.append(f"| {sec} | {k} | {s['value']:,} | {s['unit']} | {s['basis']} | {s['low']:,} | {s['high']:,} | {s['source']} |")
    lines += ["", "Scenarios: downside and upside move the drivers below to their documented low/high bound "
              "(all else base).", ""]
    for name, ov in cfg["scenarios"].items():
        lines.append(f"- **{name}**: " + ", ".join(f"{k} = {w}" for k, w in ov.items()))
    return "\n".join(lines) + "\n"



def readme_md(f: dict, ver: pd.DataFrame) -> str:
    sm, cfg, rt, mk = f["sm"], f["cfg"], f["rt"], f["mk"]
    b, d = sm["base"], sm["downside"]
    x = store_model.base_inputs(cfg)
    keys = ["mature_sales_density", "ramp_year1", "product_gross_margin", "rent_per_year", "rateable_value",
            "other_opex_pct_sales", "fitout_capex", "stock_pct_sales", "dilapidations_at_exit", "lease_term_years",
            "discount_rate", "nlw_hourly", "employer_nic_rate"]

    def fmtv(k, val):
        if k in ("ramp_year1", "product_gross_margin", "other_opex_pct_sales", "stock_pct_sales", "discount_rate",
                 "employer_nic_rate"):
            return f"{val * 100:.1f}%"
        if k == "nlw_hourly":
            return f"GBP {val:.2f}"
        if k in ("lease_term_years",):
            return f"{val:.0f} years"
        if k == "mature_sales_density":
            return f"GBP {val:,.0f}/sq ft"
        return f"GBP {val:,.0f}"

    rows = []
    for k in keys:
        sec = next(sx for sx in store_model.SECTIONS if k in cfg[sx])
        spec = cfg[sec][k]
        rng = "-" if spec["low"] == spec["high"] else f"{fmtv(k, spec['low'])} to {fmtv(k, spec['high'])}"
        rows.append(f"| {k} | {fmtv(k, spec['value'])} | {rng} | {spec['basis']} |")
    table = "\n".join(rows)
    return f"""# retail-commercial-finance-lab

Commercial finance analysis of Mint Velvet built on its filed accounts. It has two parts: a profit bridge from FY22 to FY25 that reconciles to reported profit before tax to the pound, and a new-store appraisal model. Each part comes with a live-formula Excel workbook that is recalculated in CI and must match the Python engine.

> Independent analysis of public filings. Not affiliated with or endorsed by Mint Velvet or Sabre Retail Fashion Limited. The store model is illustrative: Mint Velvet's store-level data is not public, so its outputs are not Mint Velvet's store economics.

| Deliverable | File |
|---|---|
| Two-page review: FY22-FY25 performance and a 1,700 sq ft store appraisal | [`outputs/performance_review.pdf`](outputs/performance_review.pdf) |
| Profit bridges (function and nature views), ratios and the full source ledger, in live formulas | [`outputs/bridge.xlsx`](outputs/bridge.xlsx) |
| Store appraisal: Inputs, Payroll, Store P&L, Returns, Sensitivity | [`outputs/store_model.xlsx`](outputs/store_model.xlsx) |
| Findings with page references | [`docs/findings.md`](docs/findings.md) |
| Every figure with its PDF page and verification status | [`docs/source_registry.md`](docs/source_registry.md) |
| Restatements, internal inconsistencies, press cross-check | [`docs/discrepancies.md`](docs/discrepancies.md) |

## Key findings

1. **Each pound of lost sales cost about two pounds of operating profit.** Turnover fell {pct(-f['rev_chg_22_24'])} from FY22 to FY24 and PBT fell {pct(-f['pbt_chg_22_24'])} ({m(f['pbt22'])} to {m(f['pbt24'])}). FY25 recovered: turnover +{pct(f['rev_g25'])}, PBT +{pct(f['pbt_g25'])}.
2. **The 'other operating costs' pool drove the fall, not payroll or rent.** Costs outside staff, rent, D&A and FX went from {pct(f['oth22'])} to {pct(f['oth24'])} of turnover, which explains {pct(f['share24'], 0)} of the FY24 profit fall. The filings do not split this pool after FY22, the only year with a disclosed product margin ({pct(f['pgm22'])}).
3. **Payroll is the next pressure.** FY25 staff costs rose {pct(f['staff_g25'])} against {pct(f['rev_g25'])} sales growth. Employer social security reached {pct(f['ss25'])} of wages, and the April 2025 NIC change covered only about {nic_weeks_fy25()} of FY25's 52 weeks.
4. **New store, what has to be true.** A 1,700 sq ft regional-mall unit needs **GBP {b['break_even_density']:,.0f} per sq ft a year** (GBP {b['break_even_density'] * 1700 / 1e6:.2f}m) to return a {pct(x['discount_rate'], 0)} hurdle over a 10-year lease under base costs. Under downside costs it needs GBP {d['break_even_density']:,.0f} per sq ft.

![FY23 to FY24 profit bridge](outputs/charts/bridge_FY23_FY24.png)

Turnover growth against the ONS clothing and footwear stores index: {mk.loc[2023, 'relative_to_clothing_stores_ppt']:+.1f}ppt in FY23, {mk.loc[2024, 'relative_to_clothing_stores_ppt']:+.1f}ppt in FY24, {mk.loc[2025, 'relative_to_clothing_stores_ppt']:+.1f}ppt in FY25 ([`outputs/charts/market.png`](outputs/charts/market.png)). The full set of five findings is in [`docs/findings.md`](docs/findings.md).

## Data

- **Filed accounts, FY22-FY25.** Sabre Retail Fashion Limited (company 07920155, trades as Mint Velvet), from [Companies House]({CH_URL}). The four 52-week periods end on 31 Dec 2022, 30 Dec 2023, 28 Dec 2024 and 27 Dec 2025, all under FRS 102. The PDFs are scanned page images with no text layer and no iXBRL version. Every figure is transcribed into [`data/ledger/transcription.csv`](data/ledger/transcription.csv) with its PDF page; `make extract` then OCRs each cited page and fails if a number is not on it. All {len(ver)} figures are confirmed: by OCR on the cited page or, where OCR misreads the scan, by an exact accounting identity (status per figure in the source registry).
- **Market:** [ONS Retail Sales Index v45]({ONS_URL}): Great Britain, seasonally adjusted value and volume, textile, clothing and footwear stores (Open Government Licence).
- **Statutory rates:** 2026/27 NLW, employer NIC and threshold, auto-enrolment, holiday entitlement and business-rates multipliers, linked in [`config/assumptions.yaml`](config/assumptions.yaml).

## Method

Bridges are exact identities built from each year's own filing (function view from the P&L face; nature view from the notes, with the residual 'other operating costs' pool named and sized, not plugged). The store model is a 10-year lease cash flow with bottom-up payroll from 2026/27 statutory rates and a break-even density solved exactly. Details, including how the workbooks are recalculated and checked against Python: [`docs/method.md`](docs/method.md).

## Store model inputs (base case)

Every input has a basis. SOURCED means a public source; FILING_PROXY means derived from the filed accounts (company-wide averages, and upper bounds for rent, capex and stock); ASSUMPTION means an analyst assumption to be replaced with internal data. The full list of {sum(len(cfg[sx]) for sx in store_model.SECTIONS)} inputs is in [`docs/assumptions.md`](docs/assumptions.md).

| Input | Base | Range | Basis |
|---|---|---|---|
{table}

## What this does not show

- Store-level, channel or like-for-like performance. None of it is disclosed.
- Variance against budget or forecast. No budget is public.
- Product margin after FY22. FY22 is the only filing that discloses cost of stock.
- Marketing ROI. No marketing spend is disclosed.
- Mint Velvet's actual store economics. The store model's outputs depend on labelled assumptions.

## Run it

Requires Python 3.11+, Tesseract and Poppler (OCR check), and LibreOffice (workbook parity test).

```bash
sudo apt-get install tesseract-ocr poppler-utils libreoffice-calc   # or the platform equivalent
pip install -e ".[dev]"
make all     # verify the ledger against the PDFs, build workbooks, charts, docs and the PDF
make test
```

To appraise a real site, edit [`config/assumptions.yaml`](config/assumptions.yaml) (or the blue cells in the workbook's Inputs sheet) with the heads-of-terms rent, the VOA rateable value, the fit-out quote and the staffing plan, then rerun `make all`.

## Layout

```
config/assumptions.yaml        store model inputs: value, unit, basis, low, high, source
data/raw/                      filed accounts (4 PDFs) and the ONS workbook
data/ledger/transcription.csv  every figure used, with PDF page and printed page
data/processed/                financials.csv, verification.csv, discrepancies.csv (generated)
src/rcfl/                      extract (OCR check), bridge, ratios, market, payroll, store_model,
                               excel_export, charts, report
tests/                         pytest suite, incl. LibreOffice parity tests
outputs/                       workbooks, CSVs, charts, performance_review.pdf (generated)
docs/                          findings, source registry, discrepancies, assumptions (generated)
```

MIT licence (code). README, docs and outputs are generated by `make all` from the ledger and `config/assumptions.yaml`.
"""


METHOD_BODY = '''- **Bridge.** Each year's bridge is built from that year's filing, using its current and comparative columns. Both views are exact identities with no plug. The *function view* uses the face of the P&L (sales effect at the prior-year gross-margin rate, gross-margin-rate effect, admin, other income, finance). The *nature view* uses the notes: staff costs, lease rentals, D&A and impairment, and FX are each a straight note difference. Everything else in cost of sales and admin is one named pool, 'other operating costs', whose size is reported in [`outputs/other_cost_pool.csv`](outputs/other_cost_pool.csv). The pool is treated as variable with sales. Note 2.6 of the accounts puts all retail-channel costs in cost of sales, so the reported gross margin is a channel contribution margin, not a product margin.
- **Adjusted EBITDA.** Management's figure (FY25 {adj25}) rebuilds exactly as operating profit + D&A + impairment, excluding exchange differences. It is a post-rent measure, because FRS 102 operating leases are expensed. The FRS 102 lease amendments bind for periods beginning on or after 1 Jan 2026, so FY27 is the first affected year (FY26 began on 28 Dec 2025, before the effective date); that is a comparability break to flag.
- **Source verification.** The filed accounts are scans, so each figure is transcribed into the ledger with its PDF page. `extract.py` pulls the cited page image losslessly (`pdfimages`), OCRs it with Tesseract (three page-segmentation modes) and looks for the number, tolerating OCR separator noise ("19;790"). OCR is a second, independent read of the page, never the value source. Where OCR misreads a figure (italic comparatives, where '1' reads as '4'), the figure must be the only unconfirmed term of an accounting identity that holds exactly. Any figure confirmed neither way fails the build.
- **Market context.** The ONS Retail Sales Index for textile, clothing and footwear stores (GB, seasonally adjusted value, 2019=100) is averaged by calendar year and compared with fiscal-year turnover growth (52-week years ending in the last days of December). The ONS category covers store-based clothing retailers including their online sales; the result is indicative only.
- **Store model.** Cash flows run over 10 years with no terminal value. Payroll is built bottom-up: floor cover across trading hours, salaried managers, part-time associates at NLW plus a premium, statutory holiday pay, employer NIC and pension. Business rates come from the 2026/27 RHL multipliers. Stock is bought at opening and released at lease end, and dilapidations are paid at exit. NPV is linear in sales density, so the break-even density is solved exactly. The scenarios move six drivers to their documented bounds, and the tornado moves each of five drivers by +/-20%.
- **Checks.** The tests cover: bridge reconciliation to GBP 0, every accounting identity in the ledger, OCR confirmation of every figure, ratio formulas against hand calculations, the cash-flow identities, NPV/IRR/payback on a hand-computed case, NPV = 0 at the break-even density, every assumption carrying a basis and range, and filing proxies re-derived from the ledger. LibreOffice recalculates both workbooks headlessly, and the results must match Python for every scenario and tornado case. CI fails rather than skips if LibreOffice or Tesseract is missing.
'''


def method_md(f: dict) -> str:
    return f"""# Method

""" + METHOD_BODY.format(adj25=m(f["adj25"]))

# --------------------------------------------------------------------------------------------
# PDF
# --------------------------------------------------------------------------------------------

def _styles():
    base = dict(fontName="Helvetica", fontSize=8.2, leading=10.4, textColor=colors.HexColor("#0b0b0b"), alignment=TA_LEFT)
    return {
        "h1": ParagraphStyle("h1", **{**base, "fontName": "Helvetica-Bold", "fontSize": 13, "leading": 16}),
        "h2": ParagraphStyle("h2", **{**base, "fontName": "Helvetica-Bold", "fontSize": 9.5, "leading": 12,
                                      "spaceBefore": 4, "spaceAfter": 2}),
        "body": ParagraphStyle("body", **base),
        "small": ParagraphStyle("small", **{**base, "fontSize": 6.6, "leading": 8.2, "textColor": colors.HexColor("#52514e")}),
    }


def _img(name: str, width: float) -> Image:
    with PILImage.open(paths.CHARTS / name) as im:
        w, h = im.size
    return Image(str(paths.CHARTS / name), width=width, height=width * h / w)


def _table(data, widths, header=True, font=7.2):
    t = Table(data, colWidths=widths)
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", font), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
             ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#c3c2b7"))]
    if header:
        style += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", font),
                  ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#52514e"))]
    t.setStyle(TableStyle(style))
    return t


def payback_text(r: dict) -> str:
    if r["payback_months"] is None:
        return "does not pay back within the lease"
    return f"takes {r['payback_months']:.0f} months"


def build_pdf(f: dict) -> None:
    S = _styles()
    rt, mk, sm, cfg = f["rt"], f["mk"], f["sm"], f["cfg"]
    doc = SimpleDocTemplate(str(paths.OUTPUTS / "performance_review.pdf"), pagesize=A4, leftMargin=14 * mm,
                            rightMargin=14 * mm, topMargin=11 * mm, bottomMargin=10 * mm,
                            title="Mint Velvet performance review and store appraisal",
                            author="retail-commercial-finance-lab")
    W = A4[0] - 28 * mm
    el = []
    # ---- Page 1
    el.append(Paragraph("Mint Velvet: FY22-FY25 performance review", S["h1"]))
    el.append(Paragraph("Sabre Retail Fashion Ltd (07920155), filed accounts, 52-week years to late December. "
                        "Independent analysis of public filings; not affiliated with or endorsed by Mint Velvet or Sabre "
                        "Retail Fashion Ltd.", S["small"]))
    el.append(Spacer(1, 3))
    yrs = list(rt.index)
    rows = [["GBP m unless stated"] + [f"FY{y % 100}" for y in yrs]]
    spec = [("Turnover", lambda y: f"{rt.loc[y, 'turnover_k'] / 1000:,.1f}"),
            ("Growth", lambda y: f"{rt.loc[y, 'revenue_growth'] * 100:+.1f}%"),
            ("Gross margin (after retail-channel costs)", lambda y: f"{rt.loc[y, 'gm_rate'] * 100:.1f}%"),
            ("Other operating costs % turnover", lambda y: f"{rt.loc[y, 'other_cost_pct_sales'] * 100:.1f}%"),
            ("Staff costs % turnover", lambda y: f"{rt.loc[y, 'staff_pct_sales'] * 100:.1f}%"),
            ("Adjusted EBITDA (management, post-rent)", lambda y: f"{rt.loc[y, 'adj_ebitda_k'] / 1000:,.1f}"),
            ("Adjusted EBITDA margin", lambda y: f"{rt.loc[y, 'adj_ebitda_margin'] * 100:.1f}%"),
            ("Profit before tax", lambda y: f"{ledger.value('profit_before_tax', y) / 1000:,.1f}"),
            ("Change in op. profit / change in turnover", lambda y: f"{rt.loc[y, 'op_change_per_revenue_change']:.2f}"),
            ("Year-end stock (weeks of turnover)", lambda y: f"{rt.loc[y, 'stock_k'] / 1000:,.1f} ({rt.loc[y, 'stock_cover_weeks']:.1f})"),
            ("Standalone / concession stores", lambda y: f"{rt.loc[y, 'standalone_stores']:.0f} / {rt.loc[y, 'concession_stores']:.0f}"),
            ("Turnover growth vs ONS clothing stores (ppt)", lambda y: f"{mk.loc[y, 'relative_to_clothing_stores_ppt']:+.1f}")]
    for lab, fn in spec:
        rows.append([lab] + [fn(y) for y in yrs])
    el.append(_table(rows, [W * 0.44] + [W * 0.14] * 4))
    el.append(Spacer(1, 4))
    img_w = W / 2 - 2 * mm
    imgs = [_img("bridge_FY23_FY24.png", img_w),
            _img("bridge_FY24_FY25.png", img_w)]
    t = Table([imgs], colWidths=[W / 2, W / 2])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    el.append(t)
    imgs2 = [_img("margins.png", img_w),
             _img("market.png", img_w)]
    t2 = Table([imgs2], colWidths=[W / 2, W / 2])
    t2.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    el.append(t2)
    el.append(Paragraph("What the numbers say", S["h2"]))
    bullets = [
        f"<b>Operating leverage.</b> Turnover fell {pct(-f['rev_chg_22_24'])} from FY22 to FY24 and PBT fell {pct(-f['pbt_chg_22_24'])}: "
        f"GBP {f['dec23']:.2f} and GBP {f['dec24']:.2f} of operating profit were lost per GBP 1 of lost sales in FY23 and FY24. "
        f"FY25 gained GBP {f['inc25']:.2f} per extra GBP 1 (turnover {pct(f['rev_g25'])}, PBT {pct(f['pbt_g25'])}).",
        f"<b>Other operating costs drove it.</b> Costs outside staff, rent, D&amp;A and FX went from {pct(f['oth22'])} to {pct(f['oth24'])} of "
        f"turnover from FY22 to FY24, {pct(f['share24'], 0)} of the FY24 profit fall. The pool mixes product cost with commissions, "
        f"marketing and distribution, and the filings do not split it after FY22.",
        f"<b>Payroll is the next pressure.</b> FY25 staff costs rose {pct(f['staff_g25'])} against turnover {pct(f['rev_g25'])}; "
        f"employer social security reached {pct(f['ss25'])} of wages, with the April 2025 NIC change in only about {nic_weeks_fy25()} of 52 weeks.",
        f"<b>Stock.</b> Cover peaked at {f['cover24']:.1f} weeks of turnover in FY24 ({m(f['stock24'])}) and was back to {f['cover25']:.1f} in FY25; "
        f"the obsolescence provision is {pct(f['prov25'])} of gross stock.",
    ]
    for b_ in bullets:
        el.append(Paragraph("&bull; " + b_, S["body"]))
    el.append(Spacer(1, 3))
    el.append(Paragraph("Bridge method: each bridge is built from the later year's filing and reconciles to reported PBT to GBP 0. "
                        "'Other costs (rate)' = change in [cost of sales + admin - staff - rent - D&amp;A - FX] as % of turnover, "
                        "times current turnover. Reported gross margin is after retail-channel costs (accounts note 2.6). "
                        "Adjusted EBITDA is management's measure: operating profit + D&amp;A + impairment, excluding exchange "
                        "differences (rebuilt exactly each year). FRS 102 throughout; the FRS 102 lease amendments apply to "
                        "periods beginning on or after 1 Jan 2026, so FY27 is the first year they bind (FY26 began 28 Dec 2025): "
                        "a comparability break to flag. Source pages: docs/source_registry.md.", S["small"]))
    el.append(PageBreak())

    # ---- Page 2
    b, d, u = sm["base"], sm["downside"], sm["upside"]
    x = store_model.base_inputs(cfg)
    el.append(Paragraph("New-store appraisal: 1,700 sq ft regional-mall unit (illustrative)", S["h1"]))
    el.append(Paragraph("Store-level data for Mint Velvet is not public. Every input below is a labelled assumption, a filing proxy "
                        "(company-wide average, upper bound) or a public statutory rate. The output is what has to be true, "
                        "not a forecast.", S["small"]))
    el.append(Spacer(1, 3))
    el.append(Paragraph(
        f"<b>Break-even: GBP {b['break_even_density']:,.0f} per sq ft a year</b> (mature sales GBP {b['break_even_density'] * 1700 / 1e6:.2f}m) "
        f"returns the {pct(x['discount_rate'], 0)} hurdle over a {x['lease_term_years']:.0f}-year lease under base costs. Under downside "
        f"costs it needs GBP {d['break_even_density']:,.0f} per sq ft. At the assumed GBP {x['mature_sales_density']:,.0f} per sq ft the base case "
        f"pays back in {b['payback_months']:.0f} months; the downside case (GBP {store_model.bound(cfg, 'mature_sales_density', 'low'):,.0f} per sq ft) "
        f"{payback_text(d)} and has NPV "
        f"GBP {d['npv'] / 1e6:,.2f}m.", S["body"]))
    el.append(Spacer(1, 3))
    imgs3 = [_img("breakeven.png", img_w),
             _img("tornado.png", img_w)]
    t3 = Table([imgs3], colWidths=[W / 2, W / 2])
    t3.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                            ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    el.append(t3)
    sc = [["Scenario", "NPV (GBP m)", "IRR", "Payback (months)", "Break-even GBP/sq ft", "4-wall margin, yr 3", "Payroll % sales, yr 3"]]
    for name, r in (("Base", b), ("Downside", d), ("Upside", u)):
        sc.append([name, f"{r['npv'] / 1e6:,.2f}", "n/a" if r["irr"] is None else f"{r['irr'] * 100:.0f}%",
                   "n/a" if r["payback_months"] is None else f"{r['payback_months']:.0f}",
                   f"{r['break_even_density']:,.0f}", f"{r['four_wall_margin_maturity'] * 100:.0f}%",
                   f"{r['payroll_pct_sales_maturity'] * 100:.1f}%"])
    el.append(_table(sc, [W * 0.13, W * 0.13, W * 0.09, W * 0.15, W * 0.17, W * 0.16, W * 0.17]))
    el.append(Spacer(1, 4))
    el.append(Paragraph("Key inputs", S["h2"]))
    keys = ["area_sqft", "mature_sales_density", "product_gross_margin", "rent_per_year", "rateable_value", "fitout_capex",
            "stock_pct_sales", "other_opex_pct_sales", "dilapidations_at_exit", "lease_term_years", "discount_rate",
            "nlw_hourly", "employer_nic_rate", "nic_secondary_threshold"]
    tab = [["Input", "Base", "Low", "High", "Basis"]]
    for k in keys:
        def fmt(val, k=k):
            if k in ("product_gross_margin", "stock_pct_sales", "other_opex_pct_sales", "discount_rate", "employer_nic_rate"):
                return f"{val * 100:.1f}%"
            if k == "nlw_hourly":
                return f"{val:.2f}"
            return f"{val:,.0f}"
        tab.append([k.replace("_", " "), fmt(x[k]), fmt(store_model.bound(cfg, k, "low")),
                    fmt(store_model.bound(cfg, k, "high")),
                    next(cfg[s][k]["basis"] for s in store_model.SECTIONS if k in cfg[s])])
    el.append(_table(tab, [W * 0.34, W * 0.16, W * 0.16, W * 0.16, W * 0.18], font=7))
    el.append(Spacer(1, 3))
    el.append(Paragraph("Using it on a real site", S["h2"]))
    for b_ in ["Replace the proxies with the site's own numbers: heads-of-terms rent and incentives, the unit's VOA rateable value, "
               "the fit-out quote and the expected staffing plan (config/assumptions.yaml, or the blue cells in the workbook).",
               "Set the density from comparable stores' trading, then read the headroom: assumed density over break-even density, "
               "under base and downside costs.",
               "Approve on the downside case, not the base: the decision is whether comparable stores trade above the downside break-even."]:
        el.append(Paragraph("&bull; " + b_, S["body"]))
    el.append(Spacer(1, 3))
    pr = store_model.run(store_model.scenario_case(cfg, "base")).extras
    el.append(Paragraph(
        f"Payroll is built bottom-up: {x['floor_cover']:.0f} staff on the floor for {x['trading_hours_per_week']:.0f} trading hours, "
        f"2 salaried managers, part-time associates at NLW GBP {x['nlw_hourly']:.2f} plus {pct(x['associate_premium_over_nlw'], 0)}, statutory holiday pay "
        f"(12.07%), employer NIC at 15% above GBP 5,000 and 3% auto-enrolment pension. At maturity: about {pr['labour_hours_per_week_maturity']:.0f} labour "
        f"hours a week, {pr['headcount_maturity']:.1f} heads, GBP {pr['sales_per_labour_hour_yr1_prices']:.0f} sales per labour hour. "
        "Business rates use the 2026/27 retail, hospitality and leisure multipliers on an assumed rateable value. "
        "Store losses are relieved against group profits; there is no terminal value beyond the lease. The Python engine is the "
        "source of truth; outputs/store_model.xlsx carries the same model in live formulas, recalculated in CI to match. "
        "The tornado's +/-20% gross-margin case (57%-85%) is a stress, far wider than the 70.0%-71.0% product margin in the FY21-FY22 filings.", S["small"]))
    doc.build(el)


# --------------------------------------------------------------------------------------------

def _csv(df: pd.DataFrame, path, **kw) -> None:
    """Write a CSV with floats rounded to 10 decimal places: the last binary digit of a float sum differs
    between platforms and Python versions, and unrounded output would then differ from run to run."""
    out = df.copy()
    floats = out.select_dtypes("float").columns
    out[floats] = out[floats].round(10) + 0.0          # + 0.0 turns a rounded -0.0 into 0.0
    out.to_csv(path, **kw)


def run(verify: bool = True) -> None:
    paths.ensure_dirs()
    cfg = store_model.load_config()
    ver = extract.verify_ledger() if verify else ledger.load().assign(status="not_run", detail="")
    br = bridge.build()
    _csv(br, paths.OUTPUTS / "bridge.csv", index=False)
    with open(paths.OUTPUTS / "bridge_table.csv", "w", encoding="utf-8") as fh:
        for basis in ("nature", "function"):
            fh.write(f"# {basis} view, GBP 000\n")
            bridge.pivot(br, basis).round(1).to_csv(fh)
    _csv(bridge.other_pool_table(), paths.OUTPUTS / "other_cost_pool.csv", index=False)
    _csv(ratios.build(), paths.OUTPUTS / "ratios.csv", index=False)
    _csv(ratios.ebitda_check(), paths.OUTPUTS / "adjusted_ebitda_reconciliation.csv", index=False)
    _csv(market.relative_performance(), paths.OUTPUTS / "market_context.csv", index=False)
    sm = store_model.summary(cfg)
    _csv(pd.DataFrame(sm).T, paths.OUTPUTS / "store_model_summary.csv")
    r = store_model.run(store_model.scenario_case(cfg, "base"))
    _csv(pd.DataFrame({k: getattr(r, k) for k in ("years", "sales", "gross_margin", "payroll", "rent", "rates", "occupancy_other",
                                                  "other_opex", "store_ebitda", "pre_opening", "tax", "capex", "wc_change",
                                                  "dilapidations", "fcf")}), paths.OUTPUTS / "store_pnl_base.csv", index=False)
    f = facts()
    (paths.DOCS / "findings.md").write_text(findings_md(f), encoding="utf-8")
    (paths.DOCS / "source_registry.md").write_text(registry_md(ver), encoding="utf-8")
    (paths.DOCS / "discrepancies.md").write_text(discrepancies_md(), encoding="utf-8")
    (paths.DOCS / "assumptions.md").write_text(assumptions_md(cfg), encoding="utf-8")
    (paths.ROOT / "README.md").write_text(readme_md(f, ver), encoding="utf-8")
    (paths.DOCS / "method.md").write_text(method_md(f), encoding="utf-8")
    build_pdf(f)


if __name__ == "__main__":
    run()
