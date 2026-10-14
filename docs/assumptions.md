# Store model assumptions

Source of truth: `config/assumptions.yaml`. Basis: SOURCED (public source), FILING_PROXY (derived from the filed accounts; capex, rent and stock proxies are upper bounds), ASSUMPTION (analyst assumption, to be replaced with internal data).

| Section | Input | Value | Unit | Basis | Low | High | Source / derivation |
|---|---|---:|---|---|---:|---:|---|
| store | area_sqft | 1,700 | sq ft | SOURCED | 1,700 | 1,700 | Store size in the July 2026 Meadowhall signing announcement (TheIndustry.fashion, 29 Jul 2026): https://www.theindustry.fashion/meadowhall-strengthens-fashion-line-up-with-mint-velvet-belstaff-and-michael-kors-deals/ |
| store | mature_sales_density | 850 | GBP per sq ft per year (year-1 prices) | ASSUMPTION | 600 | 1,100 | No public store-level sales. The model solves for the break-even density, which does not depend on this input; the base value only sets the illustrative NPV. |
| store | ramp_year1 | 0.8 | share of mature sales | ASSUMPTION | 0.7 | 0.9 | New-store sales build; year 3 onwards = 100%. |
| store | ramp_year2 | 0.95 | share of mature sales | ASSUMPTION | 0.9 | 1.0 | New-store sales build. |
| store | sales_growth | 0.02 | per year, nominal, from year 2 | ASSUMPTION | 0.0 | 0.04 | Like-for-like price/mix growth on the matured base. |
| store | product_gross_margin | 0.7102 | share of sales | FILING_PROXY | 0.66 | 0.74 | FY22 accounts note 6 (pdf p.34): 1 - cost of stock expensed 41,639 / turnover 143,675. The only year the filings disclose cost of stock; company-wide (all channels, after markdowns). low/high are ASSUMPTION (+/-4.5pp). |
| store | rent_per_year | 95,340 | GBP per year | FILING_PROXY | 70,000 | 200,000 | FY25 accounts: operating lease rentals 5,053k (note 6, pdf p.33) / 53 standalone stores (strategic report, pdf p.4). Upper bound for an average store: includes head office and any other leased property. low/high are ASSUMPTION; a super-regional mall unit can cost well above the estate average, so high is about 2x the proxy. |
| store | rent_review_uplift | 0.1 | one-off uplift at year 6 (five-yearly review) | ASSUMPTION | 0.0 | 0.2 | Upward-only review at year 5 anniversary. |
| store | occupancy_other_psf | 15 | GBP per sq ft per year | ASSUMPTION | 8 | 25 | Service charge, insurance, utilities. Indexed at cost_inflation. |
| store | rateable_value | 55,000 | GBP | ASSUMPTION | 40,000 | 90,000 | Replace with the unit's entry on the VOA 2026 rating list. Rates = RV x the 2026/27 RHL multiplier for its band (payroll_and_tax section). |
| store | other_opex_pct_sales | 0.1 | share of sales | ASSUMPTION | 0.06 | 0.15 | Allowance for distribution to store, shrinkage, card fees, store marketing, repairs, cleaning, security and store systems. Not a benchmark. The filings put all retail-channel costs other than staff, rent and D&A in one pool (bridge 'other operating costs'), which cannot be split to store level. |
| store | fitout_capex | 528,000 | GBP at opening | FILING_PROXY | 323,333 | 931,500 | FY24 accounts: tangible additions 2,640k (note 14, pdf p.37) / 5 projects (3 openings + 2 relocations, pdf p.4). Upper bound: additions also include refits, IT and head-office capex. low = FY22 (1,940k / 6 openings), high = FY23 (3,726k / 4 openings). |
| store | pre_opening_costs | 30,000 | GBP at opening, expensed | ASSUMPTION | 15,000 | 50,000 | Recruitment, training, launch marketing. |
| store | stock_pct_sales | 0.0996 | stock held as share of annual sales | FILING_PROXY | 0.0819 | 0.1242 | FY25 accounts: stocks 14,964k / turnover 150,240k (pdf p.20, p.18). Company-wide incl. warehouse and online stock, so an upper bound for one store. low = FY23, high = FY24. Released at lease end. |
| store | dilapidations_at_exit | 26,604 | GBP at lease end | FILING_PROXY | 8,271 | 40,000 | FY25 accounts: dilapidations provision 1,410k (note 3, pdf p.32) / 53 standalone stores. low = FY22 (397k / 48). high is ASSUMPTION. |
| store | lease_term_years | 10 | years | ASSUMPTION | 5 | 15 | No terminal value beyond the lease term. Lease-term sensitivity shows the cost of a break at year 5. |
| finance | discount_rate | 0.1 | nominal post-tax | ASSUMPTION | 0.08 | 0.14 | Hurdle rate for store capex; replace with the company's own. |
| finance | tax_rate | 0.25 | corporation tax main rate | SOURCED | 0.25 | 0.25 | UK corporation tax main rate 25% from 1 April 2023 (also stated in FY25 accounts note 11): https://www.gov.uk/corporation-tax-rates |
| finance | tax_depreciation_years | 10 | years, straight line | ASSUMPTION | 10 | 10 | Simplification: fit-out relief spread over the lease. Full expensing on qualifying plant would accelerate relief and raise NPV. Store losses assumed relieved against group profits. |
| finance | wage_inflation | 0.04 | per year | ASSUMPTION | 0.025 | 0.06 | NLW rose 4.1% in April 2026 (GOV.UK); assumed to continue near that pace. |
| finance | cost_inflation | 0.025 | per year | ASSUMPTION | 0.015 | 0.04 | Indexation of rates and other occupancy costs. |
| payroll | trading_hours_per_week | 64 | hours | ASSUMPTION | 58 | 72 | Regional mall opening hours incl. late nights and Sunday. |
| payroll | floor_cover | 2 | staff on the floor at all trading hours | ASSUMPTION | 2 | 3 | Minimum safe cover for a 1,700 sq ft unit. |
| payroll | non_trading_hours_per_week | 16 | staff hours | ASSUMPTION | 8 | 24 | Opening, closing, deliveries, replenishment. |
| payroll | managers | 2 | salaried managers (store + assistant) | ASSUMPTION | 2 | 2 | Store manager and assistant manager. |
| payroll | manager_floor_hours_per_week | 30 | hours per manager counted toward floor cover | ASSUMPTION | 25 | 35 | Contracted 40 hours, of which 30 on the floor. |
| payroll | manager_contract_hours_per_week | 40 | hours | ASSUMPTION | 40 | 40 | Used for sales per labour hour. |
| payroll | store_manager_salary | 36,000 | GBP per year | ASSUMPTION | 32,000 | 42,000 | Base salary, before employer on-costs. |
| payroll | assistant_manager_salary | 28,000 | GBP per year | ASSUMPTION | 25,000 | 31,000 | Base salary, before employer on-costs. |
| payroll | associate_contract_hours_per_week | 20 | hours | ASSUMPTION | 16 | 30 | Part-time contracts; sets earnings per head, which drives NIC and pension thresholds. |
| payroll | associate_premium_over_nlw | 0.05 | share above NLW | ASSUMPTION | 0.0 | 0.15 | Premium-brand sales associate rate. |
| payroll | variable_hours_per_k_sales | 1.5 | associate hours per GBP 1,000 of mature sales (year-1 prices) | ASSUMPTION | 1.0 | 2.0 | Hours added above minimum cover as sales volume rises. |
| payroll_and_tax | nlw_hourly | 12.71 | GBP per hour, age 21+, from 1 April 2026 | SOURCED | 12.71 | 12.71 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027 |
| payroll_and_tax | employer_nic_rate | 0.15 | Class 1 secondary rate, 2026/27 | SOURCED | 0.15 | 0.15 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027 |
| payroll_and_tax | nic_secondary_threshold | 5,000 | GBP per year, 2026/27 | SOURCED | 5,000 | 5,000 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027 |
| payroll_and_tax | employer_nic_rate_2024_25 | 0.138 | Class 1 secondary rate before 6 April 2025 (comparison only) | SOURCED | 0.138 | 0.138 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2024-to-2025 |
| payroll_and_tax | nic_secondary_threshold_2024_25 | 9,100 | GBP per year before 6 April 2025 (comparison only) | SOURCED | 9,100 | 9,100 | https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2024-to-2025 |
| payroll_and_tax | pension_employer_rate | 0.03 | minimum employer contribution on qualifying earnings | SOURCED | 0.03 | 0.03 | https://www.gov.uk/workplace-pensions/what-you-your-employer-and-the-government-pay |
| payroll_and_tax | pension_qe_lower | 6,240 | GBP per year, 2026/27 (frozen) | SOURCED | 6,240 | 6,240 | https://www.gov.uk/government/publications/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627 |
| payroll_and_tax | pension_qe_upper | 50,270 | GBP per year, 2026/27 (frozen) | SOURCED | 50,270 | 50,270 | https://www.gov.uk/government/publications/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627 |
| payroll_and_tax | pension_trigger | 10,000 | GBP per year, auto-enrolment earnings trigger 2026/27 (frozen) | SOURCED | 10,000 | 10,000 | https://www.gov.uk/government/publications/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627/review-of-the-automatic-enrolment-earnings-trigger-and-qualifying-earnings-band-for-202627 |
| payroll_and_tax | holiday_weeks | 5.6 | statutory weeks per year | SOURCED | 5.6 | 5.6 | https://www.gov.uk/holiday-entitlement-rights. Cost uplift per hour worked = 5.6 / (52 - 5.6) = 12.07%. |
| payroll_and_tax | rates_multiplier_rhl_small | 0.382 | GBP per GBP of RV, retail/hospitality/leisure, RV below 51,000, 2026/27 | SOURCED | 0.382 | 0.382 | England 2026/27 multipliers, e.g. https://www.spelthorne.gov.uk/page/661/business-rates-multipliers-20262027 |
| payroll_and_tax | rates_multiplier_rhl_standard | 0.43 | GBP per GBP of RV, RHL, RV 51,000 to 499,999, 2026/27 | SOURCED | 0.43 | 0.43 | England 2026/27 multipliers, e.g. https://www.spelthorne.gov.uk/page/661/business-rates-multipliers-20262027 |
| payroll_and_tax | rates_multiplier_high_value | 0.508 | GBP per GBP of RV, all properties RV 500,000+, 2026/27 | SOURCED | 0.508 | 0.508 | England 2026/27 multipliers, e.g. https://www.spelthorne.gov.uk/page/661/business-rates-multipliers-20262027 |

Scenarios: downside and upside move the drivers below to their documented low/high bound (all else base).

- **downside**: mature_sales_density = low, product_gross_margin = low, rent_per_year = high, fitout_capex = high, ramp_year1 = low, ramp_year2 = low
- **upside**: mature_sales_density = high, product_gross_margin = high, rent_per_year = low, fitout_capex = low, ramp_year1 = high, ramp_year2 = high
