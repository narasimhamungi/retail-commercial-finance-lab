"""Profit bridges PBT(t-1) -> PBT(t), FY22 to FY25.

Each bridge is built from a single filing (year t's accounts, which present t and t-1 on a
consistent basis). Where a comparative differs from the figure originally reported a year
earlier, the difference is logged in docs/discrepancies.md; the bridge uses the comparative.

Two views, both exact identities (no plug):

1. Function view (face of the P&L)
   sales effect          = dRevenue x GM%(t-1)
   gross-margin-rate     = (GM%(t) - GM%(t-1)) x Revenue(t)
   admin, other operating income, net finance = changes in those lines
   Note 2.6 of the accounts: all retail-channel operating costs sit in cost of sales, so
   "gross margin" here is a channel contribution margin, not a product margin.

2. Nature view (notes 6 and 8)
   Disclosed cost pools: staff costs (note 8), operating lease rentals, D&A and impairment,
   exchange differences (note 6). Everything else in cost of sales + admin is one named pool,
   "other operating costs" (product cost, concession commissions, marketing, distribution,
   business rates, utilities and the like; the accounts do not split it). It is treated as
   variable with sales:
   sales effect            = dRevenue x (1 - other%(t-1))
   other-cost-rate effect  = -(other%(t) - other%(t-1)) x Revenue(t)
   staff / lease / D&A / FX = -(change in the disclosed cost)
   other operating income, net finance = changes in those lines
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from . import ledger

PAIRS = ((2022, 2023), (2023, 2024), (2024, 2025))


@dataclass(frozen=True)
class Year:
    revenue: float
    cost_of_sales: float
    admin: float
    ooi: float
    interest_receivable: float
    interest_payable: float
    pbt: float
    staff: float
    lease: float
    da: float
    fx: float

    @property
    def gross_profit(self) -> float:
        return self.revenue - self.cost_of_sales

    @property
    def gm_rate(self) -> float:
        return self.gross_profit / self.revenue

    @property
    def net_finance(self) -> float:
        return self.interest_receivable - self.interest_payable

    @property
    def other_costs(self) -> float:
        return self.cost_of_sales + self.admin - self.staff - self.lease - self.da - self.fx

    @property
    def other_rate(self) -> float:
        return self.other_costs / self.revenue


def load_year(period: int, filing: int) -> Year:
    v = lambda item: ledger.value(item, period, filing)  # noqa: E731
    return Year(
        revenue=v("turnover"), cost_of_sales=v("cost_of_sales"), admin=v("admin_expenses"),
        ooi=v("other_operating_income"), interest_receivable=v("interest_receivable"),
        interest_payable=v("interest_payable"), pbt=v("profit_before_tax"),
        staff=v("staff_costs_total"), lease=v("operating_lease_rentals"),
        da=v("depreciation") + v("amortisation") + v("impairment_tangible"),
        fx=v("fx_differences"),
    )


def function_bridge(p: Year, c: Year) -> list[tuple[str, float]]:
    return [
        ("Sales effect (at prior-year GM rate)", (c.revenue - p.revenue) * p.gm_rate),
        ("Gross-margin-rate effect", (c.gm_rate - p.gm_rate) * c.revenue),
        ("Administrative expenses", -(c.admin - p.admin)),
        ("Other operating income", c.ooi - p.ooi),
        ("Net finance income", c.net_finance - p.net_finance),
    ]


def nature_bridge(p: Year, c: Year) -> list[tuple[str, float]]:
    return [
        ("Sales effect (at prior-year contribution rate)", (c.revenue - p.revenue) * (1 - p.other_rate)),
        ("Other operating costs: rate effect", -(c.other_rate - p.other_rate) * c.revenue),
        ("Staff costs", -(c.staff - p.staff)),
        ("Operating lease rentals", -(c.lease - p.lease)),
        ("Depreciation, amortisation, impairment", -(c.da - p.da)),
        ("Exchange differences", -(c.fx - p.fx)),
        ("Other operating income", c.ooi - p.ooi),
        ("Net finance income", c.net_finance - p.net_finance),
    ]


def build() -> pd.DataFrame:
    """Long-format bridge table: one row per (basis, year pair, step), in GBP 000."""
    rows = []
    for prev, cur in PAIRS:
        p, c = load_year(prev, cur), load_year(cur, cur)
        for basis, steps in (("function", function_bridge(p, c)), ("nature", nature_bridge(p, c))):
            rows.append(dict(basis=basis, from_fy=prev, to_fy=cur, order=0, step=f"PBT FY{prev % 100}",
                             kind="start", value_k=p.pbt))
            for i, (name, val) in enumerate(steps, start=1):
                rows.append(dict(basis=basis, from_fy=prev, to_fy=cur, order=i, step=name, kind="delta", value_k=val))
            residual = p.pbt + sum(v for _, v in steps) - c.pbt
            rows.append(dict(basis=basis, from_fy=prev, to_fy=cur, order=len(steps) + 1, step=f"PBT FY{cur % 100}",
                             kind="end", value_k=c.pbt, residual_k=residual))
    df = pd.DataFrame(rows)
    df["source_filing"] = df["to_fy"].map(lambda y: f"FY{y % 100} accounts (current + comparative columns)")
    return df


def pools(period: int, filing: int | None = None) -> dict[str, float]:
    """Cost pools for one year, for the ratio table and the bridge notes."""
    filing = period if filing is None else filing
    y = load_year(period, filing)
    return {"revenue": y.revenue, "staff": y.staff, "lease": y.lease, "da": y.da, "fx": y.fx,
            "other_costs": y.other_costs, "other_rate": y.other_rate, "gm_rate": y.gm_rate,
            "total_costs": y.cost_of_sales + y.admin}


def other_pool_table() -> pd.DataFrame:
    """Size of the residual 'other operating costs' pool in each bridge year (reported, not hidden)."""
    rows = []
    for prev, cur in PAIRS:
        for period in (prev, cur):
            y = load_year(period, cur)
            rows.append(dict(bridge=f"FY{prev % 100}->FY{cur % 100}", fiscal_year=period,
                             other_costs_k=y.other_costs, revenue_k=y.revenue,
                             other_pct_revenue=y.other_rate,
                             other_pct_total_costs=y.other_costs / (y.cost_of_sales + y.admin)))
    return pd.DataFrame(rows)


def pivot(df: pd.DataFrame, basis: str) -> pd.DataFrame:
    """Steps as rows, year pairs as columns (GBP 000)."""
    sub = df[df.basis == basis].copy()
    sub["pair"] = sub.apply(lambda r: f"FY{r.from_fy % 100}->FY{r.to_fy % 100}", axis=1)
    sub["label"] = sub.apply(lambda r: "PBT start" if r.kind == "start" else ("PBT end" if r.kind == "end" else r.step), axis=1)
    order = sub.drop_duplicates("label").sort_values("order")["label"].tolist()
    return sub.pivot(index="label", columns="pair", values="value_k").reindex(order)
