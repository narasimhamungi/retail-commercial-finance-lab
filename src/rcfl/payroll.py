"""Bottom-up store payroll from statutory 2026/27 rates and staffing assumptions.

All hours and costs are in year-1 prices. Labour hours have two parts:
- fixed: floor cover across trading hours plus non-trading hours, less the managers' floor hours
- variable: associate hours per GBP 1,000 of sales volume (mature sales x ramp, year-1 prices)
Everything is linear in sales, so store NPV is linear in sales density (see store_model).
"""

from __future__ import annotations

from dataclasses import dataclass

WEEKS = 52


def holiday_uplift(holiday_weeks: float) -> float:
    """Extra pay per hour worked to fund statutory holiday: 5.6 / (52 - 5.6)."""
    return holiday_weeks / (WEEKS - holiday_weeks)


def employer_nic(earnings: float, rate: float, threshold: float) -> float:
    return rate * max(0.0, earnings - threshold)


def employer_pension(earnings: float, rate: float, lower: float, upper: float, trigger: float) -> float:
    """Minimum auto-enrolment contribution; jobholders below the trigger are not enrolled."""
    if earnings < trigger:
        return 0.0
    return rate * max(0.0, min(earnings, upper) - lower)


@dataclass(frozen=True)
class PayrollResult:
    associate_hourly_rate: float
    associate_annual_earnings: float
    associate_nic: float
    associate_pension: float
    associate_cost_per_hour_worked: float
    associate_nic_2024_25: float
    manager_costs: tuple[float, ...]
    fixed_associate_hours_week: float
    fixed_payroll: float              # GBP per year, year-1 prices
    variable_cost_per_k_sales: float  # GBP per GBP 1,000 of sales volume


def compute(p: dict, t: dict) -> PayrollResult:
    """p: `payroll` inputs, t: `payroll_and_tax` inputs (plain values)."""
    h = holiday_uplift(t["holiday_weeks"])
    rate = t["nlw_hourly"] * (1 + p["associate_premium_over_nlw"])
    earnings = p["associate_contract_hours_per_week"] * WEEKS * rate * (1 + h)
    nic = employer_nic(earnings, t["employer_nic_rate"], t["nic_secondary_threshold"])
    nic_old = employer_nic(earnings, t["employer_nic_rate_2024_25"], t["nic_secondary_threshold_2024_25"])
    pension = employer_pension(earnings, t["pension_employer_rate"], t["pension_qe_lower"],
                               t["pension_qe_upper"], t["pension_trigger"])
    cost_per_hour = (earnings + nic + pension) / (p["associate_contract_hours_per_week"] * WEEKS)

    managers = []
    for salary in (p["store_manager_salary"], p["assistant_manager_salary"])[: int(p["managers"])]:
        managers.append(salary
                        + employer_nic(salary, t["employer_nic_rate"], t["nic_secondary_threshold"])
                        + employer_pension(salary, t["pension_employer_rate"], t["pension_qe_lower"],
                                           t["pension_qe_upper"], t["pension_trigger"]))

    fixed_hours = max(0.0, p["trading_hours_per_week"] * p["floor_cover"] + p["non_trading_hours_per_week"]
                      - p["managers"] * p["manager_floor_hours_per_week"])
    fixed_payroll = sum(managers) + fixed_hours * WEEKS * cost_per_hour
    variable_per_k = p["variable_hours_per_k_sales"] * cost_per_hour
    return PayrollResult(rate, earnings, nic, pension, cost_per_hour, nic_old, tuple(managers),
                         fixed_hours, fixed_payroll, variable_per_k)


def labour_hours(p: dict, res: PayrollResult, sales_volume: float) -> float:
    """Annual labour hours (associates + managers' contracted hours) at a given sales volume."""
    associate = res.fixed_associate_hours_week * WEEKS + p["variable_hours_per_k_sales"] * sales_volume / 1000
    return associate + p["managers"] * p["manager_contract_hours_per_week"] * WEEKS
