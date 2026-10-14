"""Static charts (PNG) for the README and the two-page performance review."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import bridge, market, paths, ratios, store_model  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"
UP = "#2a78d6"      # favourable (diverging pole, blue)
DOWN = "#e34948"    # adverse (diverging pole, red)
TOTAL = "#52514e"   # start/end totals (neutral ink)
S1, S2 = "#2a78d6", "#eb6834"  # categorical slots 1-2

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK, "axes.titlesize": 10,
    "axes.titleweight": "bold", "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "axes.spines.top": False, "axes.spines.right": False,
})


def _grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


SHORT = {
    "Sales effect (at prior-year contribution rate)": "Sales",
    "Other operating costs: rate effect": "Other\ncosts\n(rate)",
    "Staff costs": "Staff",
    "Operating lease rentals": "Rent",
    "Depreciation, amortisation, impairment": "D&A",
    "Exchange differences": "FX",
    "Other operating income": "Other\nincome",
    "Net finance income": "Finance",
}


def waterfall(ax, df: pd.DataFrame, prev: int, cur: int) -> None:
    sub = df[(df.basis == "nature") & (df.from_fy == prev) & (df.to_fy == cur)].sort_values("order")
    labels, bottoms, heights, colors = [], [], [], []
    running = 0.0
    for r in sub.itertuples():
        v = r.value_k / 1000
        if r.kind == "start":
            labels.append(f"PBT\nFY{prev % 100}")
            bottoms.append(0), heights.append(v), colors.append(TOTAL)
            running = v
        elif r.kind == "end":
            labels.append(f"PBT\nFY{cur % 100}")
            bottoms.append(0), heights.append(v), colors.append(TOTAL)
        else:
            labels.append(SHORT.get(r.step, r.step))
            bottoms.append(running if v >= 0 else running + v)
            heights.append(abs(v))
            colors.append(UP if v >= 0 else DOWN)
            running += v
    x = np.arange(len(labels))
    ax.bar(x, heights, bottom=bottoms, color=colors, width=0.62, edgecolor=SURFACE, linewidth=1)
    for i, r in enumerate(sub.itertuples()):
        v = r.value_k / 1000
        top = bottoms[i] + heights[i]
        txt = f"{v:,.1f}" if r.kind != "delta" else f"{v:+,.1f}"
        ax.text(x[i], top + 0.35, txt, ha="center", va="bottom", fontsize=7.5, color=INK)
    ax.set_xticks(x, labels, fontsize=7)
    ax.set_ylabel("GBP m")
    ax.set_title(f"Profit before tax bridge, FY{prev % 100} to FY{cur % 100}")
    ax.set_ylim(0, max(b + h for b, h in zip(bottoms, heights)) * 1.15)
    _grid(ax)


def bridges(df: pd.DataFrame) -> list:
    out = []
    for prev, cur in bridge.PAIRS:
        fig, ax = plt.subplots(figsize=(6.2, 3.2))
        waterfall(ax, df, prev, cur)
        fig.text(0.01, 0.01, "Blue adds to profit, red reduces it. Other costs (rate): change in costs outside staff, rent,\n"
                 "D&A and FX as a % of sales. Source: filed accounts; built from the later year's filing.",
                 fontsize=6.5, color=MUTED)
        fig.tight_layout(rect=(0, 0.07, 1, 1))
        p = paths.CHARTS / f"bridge_FY{prev % 100}_FY{cur % 100}.png"
        fig.savefig(p, dpi=200)
        plt.close(fig)
        out.append(p)
    return out


def margins(rt: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    yrs = [f"FY{y % 100}" for y in rt.fiscal_year]
    series = [("Other operating costs % sales", rt.other_cost_pct_sales, S2),
              ("Adjusted EBITDA margin", rt.adj_ebitda_margin, S1)]
    for lab, s, c in series:
        ax.plot(yrs, s * 100, color=c, linewidth=2, marker="o", markersize=5)
        ax.annotate(f"{lab}\n{s.iloc[-1] * 100:.1f}%", (len(yrs) - 1, s.iloc[-1] * 100), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=7.5, color=INK2)
        ax.annotate(f"{s.iloc[0] * 100:.1f}%", (0, s.iloc[0] * 100), xytext=(-8, 0), textcoords="offset points",
                    va="center", ha="right", fontsize=7.5, color=INK2)
    ax.set_ylabel("% of turnover")
    ax.set_xlim(-0.6, len(yrs) + 0.9)
    ax.set_ylim(0, 85)
    ax.set_title("Where the margin went: other operating costs vs adjusted EBITDA")
    _grid(ax)
    fig.tight_layout()
    p = paths.CHARTS / "margins.png"
    fig.savefig(p, dpi=200)
    plt.close(fig)
    return p


def market_chart(mk: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    yrs = [f"FY{y % 100}" for y in mk.fiscal_year]
    x = np.arange(len(yrs))
    w = 0.36
    a = mk.mint_velvet_turnover_growth * 100
    b = mk.ons_clothing_stores_value_growth * 100
    ax.bar(x - w / 2 - 0.01, a, w, color=S1, label="Mint Velvet turnover")
    ax.bar(x + w / 2 + 0.01, b, w, color=S2, label="ONS clothing & footwear stores, value (GB, SA)")
    for i in range(len(x)):
        for xx, v in ((x[i] - w / 2, a.iloc[i]), (x[i] + w / 2, b.iloc[i])):
            ax.text(xx, v + (0.6 if v >= 0 else -0.6), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top",
                    fontsize=7.5, color=INK)
    ax.axhline(0, color=BASE, linewidth=1)
    ax.set_xticks(x, yrs)
    ax.set_ylabel("growth vs prior year, %")
    ax.set_ylim(min(a.min(), b.min()) - 4, max(a.max(), b.max()) + 4)
    ax.set_title("Turnover growth vs the clothing-stores market")
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    _grid(ax)
    fig.text(0.01, 0.01, "ONS Retail Sales Index v45: GB, seasonally adjusted value, calendar-year average.\n"
             "Covers store-based clothing retailers incl. their online sales; online-only retailers sit elsewhere.",
             fontsize=6.3, color=MUTED)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    p = paths.CHARTS / "market.png"
    fig.savefig(p, dpi=200)
    plt.close(fig)
    return p


NICE = {"mature_sales_density": "Sales density", "product_gross_margin": "Product gross margin",
        "rent_per_year": "Rent", "payroll": "Payroll", "ramp_speed": "Ramp-up speed"}


def tornado(cfg: dict):
    base = store_model.run(store_model.scenario_case(cfg, "base")).npv / 1e6
    rows = {}
    for d, side, c in store_model.tornado_cases(cfg):
        rows.setdefault(d, {})[side] = store_model.run(c).npv / 1e6
    order = sorted(rows, key=lambda d: abs(rows[d]["high"] - rows[d]["low"]))
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    for i, d in enumerate(order):
        lo, hi = rows[d]["low"], rows[d]["high"]
        for v, lab in ((lo, "-20%"), (hi, "+20%")):
            ax.barh(i, v - base, left=base, color=UP if v >= base else DOWN, height=0.55, edgecolor=SURFACE)
            ax.text(v + (0.03 if v >= base else -0.03), i, f"{lab}: {v:,.2f}", va="center",
                    ha="left" if v >= base else "right", fontsize=7, color=INK2)
    ax.axvline(base, color=INK2, linewidth=1)
    ax.set_yticks(range(len(order)), [NICE[d] for d in order])
    ax.set_xlabel("NPV, GBP m (base {:,.2f})".format(base))
    ax.set_title("Store NPV: one driver moved +/-20%")
    lo_all = min(min(v.values()) for v in rows.values())
    hi_all = max(max(v.values()) for v in rows.values())
    ax.set_xlim(lo_all - 0.9, hi_all + 0.9)
    _grid(ax, "x")
    fig.tight_layout()
    p = paths.CHARTS / "tornado.png"
    fig.savefig(p, dpi=200)
    plt.close(fig)
    return p


def breakeven(cfg: dict):
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    dens = np.linspace(200, 1200, 41)
    for name, c in (("base", S1), ("downside", S2)):
        case = store_model.scenario_case(cfg, name)
        npvs = [store_model.run(store_model.Case({**case.x, "mature_sales_density": d})).npv / 1e6 for d in dens]
        be = store_model.break_even_density(case)
        ax.plot(dens, npvs, color=c, linewidth=2, label=f"{name.capitalize()} costs: break-even GBP {be:,.0f} / sq ft")
        ax.plot([be], [0], marker="o", markersize=7, color=c, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.axhline(0, color=BASE, linewidth=1)
    ax.set_xlabel("Mature sales density, GBP per sq ft per year (year-1 prices)")
    ax.set_ylabel("NPV over lease, GBP m")
    ax.set_title("What has to be true: NPV by sales density, 1,700 sq ft unit")
    _grid(ax)
    fig.tight_layout()
    p = paths.CHARTS / "breakeven.png"
    fig.savefig(p, dpi=200)
    plt.close(fig)
    return p


def run() -> list:
    paths.ensure_dirs()
    cfg = store_model.load_config()
    df = bridge.build()
    out = bridges(df)
    out.append(margins(ratios.build()))
    out.append(market_chart(market.relative_performance()))
    out.append(tornado(cfg))
    out.append(breakeven(cfg))
    return out


if __name__ == "__main__":
    run()
