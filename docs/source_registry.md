# Source registry

Every figure used is transcribed from Sabre Retail Fashion Limited's filed accounts (company 07920155, trading as Mint Velvet), downloaded from Companies House: https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history

The PDFs are scanned page images with no text layer. Each figure was read off the page image and recorded in `data/ledger/transcription.csv`. `make extract` then OCRs the cited page (Tesseract, 300 dpi native images) and fails if the number is not on that page. Status key:

- `verified`: number found on the cited page by OCR
- `verified_weak`: single-digit number found (any page has single digits; read visually)
- `verified_by_identity`: OCR misread the page (e.g. italic '1' read as '4'), but the figure is the only unconfirmed term of an accounting identity that holds exactly
- `nil_not_checked`: shown as '-' or not presented; zero cannot be located by OCR

## Files

| FY | Period end | File | Pages | SHA-256 | Document link |
|---|---|---|---|---|---|
| FY22 | 2022-12-31 | `sabre_retail_fashion_07920155_FY22_2022-12-31.pdf` | 52 weeks | `5feee043aababb29...` | [PDF](https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history/MzM4ODI5NzQzOWFkaXF6a2N4/document?format=pdf&download=0) |
| FY23 | 2023-12-30 | `sabre_retail_fashion_07920155_FY23_2023-12-30.pdf` | 52 weeks | `217fa712ba664a6a...` | [PDF](https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history/MzQyOTM0MTA4MGFkaXF6a2N4/document?format=pdf&download=0) |
| FY24 | 2024-12-28 | `sabre_retail_fashion_07920155_FY24_2024-12-28.pdf` | 52 weeks | `10857ea31ed9c34c...` | [PDF](https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history/MzQ4MDQzNDYxMmFkaXF6a2N4/document?format=pdf&download=0) |
| FY25 | 2025-12-27 | `sabre_retail_fashion_07920155_FY25_2025-12-27.pdf` | 52 weeks | `cc79228a67b0e9fa...` | [PDF](https://find-and-update.company-information.service.gov.uk/company/07920155/filing-history/MzUzNzU1NTE3MGFkaXF6a2N4/document?format=pdf&download=0) |

ONS Retail Sales Index, time series v45 (https://www.ons.gov.uk/datasets/retail-sales-index/editions/time-series/versions/45): `retail-sales-index-time-series-v45.xlsx`, SHA-256 `35ca5ce528a104db...`. Open Government Licence v3.0.

## Status summary

- verified: 390
- verified_weak: 38
- nil_not_checked: 21
- verified_by_identity: 5

Total figures: 454.

## Figures

| Filing | Period | Line item | Value | Unit | PDF p. | Printed p. | Section | Status |
|---|---|---|---:|---|---:|---:|---|---|
| FY25 | FY25 | turnover | 150,240 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | turnover | 134,735 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | cost_of_sales | 110,166 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | cost_of_sales | 103,668 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | gross_profit | 40,074 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | gross_profit | 31,067 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | admin_expenses | 22,097 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | admin_expenses | 19,173 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | other_operating_income | 1,484 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | other_operating_income | 1,355 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | operating_profit | 19,461 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | operating_profit | 13,249 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | interest_receivable | 723 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | interest_receivable | 974 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | interest_payable | 1 | gbp_k | 18 | 15 | Profit and loss account | verified_weak |
| FY25 | FY24 | interest_payable | 0 | gbp_k | 18 | 15 | Profit and loss account | nil_not_checked |
| FY25 | FY25 | profit_before_tax | 20,183 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | profit_before_tax | 14,223 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | tax | 4,604 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | tax | 3,628 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | profit_after_tax | 15,579 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY24 | profit_after_tax | 10,595 | gbp_k | 18 | 15 | Profit and loss account | verified |
| FY25 | FY25 | turnover_uk | 150,240 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | turnover_uk | 134,735 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | ooi_other | 1,426 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | ooi_other | 1,213 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified_by_identity |
| FY25 | FY25 | ooi_royalty | 58 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | ooi_royalty | 142 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | fx_differences | -1,211 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | fx_differences | -818 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | operating_lease_rentals | 5,053 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | operating_lease_rentals | 4,892 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | inventory_impairment | 211 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | inventory_impairment | 192 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | depreciation | 1,719 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | depreciation | 1,865 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | amortisation | 1,126 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified_by_identity |
| FY25 | FY24 | amortisation | 1,132 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | impairment_tangible | 135 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | impairment_tangible | 438 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | pension_dc | 504 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY24 | pension_dc | 471 | gbp_k | 33 | 30 | Note 4-6 turnover, other operating income, operating profit | verified |
| FY25 | FY25 | wages_salaries | 19,175 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | wages_salaries | 16,476 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | social_security | 1,847 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | social_security | 1,127 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | pension_cost | 504 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | pension_cost | 471 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | staff_costs_total | 21,526 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | staff_costs_total | 18,074 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | employees_admin | 165 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | employees_admin | 162 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | employees_store | 692 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | employees_store | 623 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | employees_directors | 5 | count | 34 | 31 | Note 8 employees | verified_weak |
| FY25 | FY24 | employees_directors | 5 | count | 34 | 31 | Note 8 employees | verified_weak |
| FY25 | FY25 | employees_total | 862 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY24 | employees_total | 790 | count | 34 | 31 | Note 8 employees | verified |
| FY25 | FY25 | adjusted_ebitda | 21,230 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY25 | FY24 | adjusted_ebitda | 15,866 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY25 | FY25 | intangible_assets | 2,598 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | intangible_assets | 2,889 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | tangible_assets | 5,554 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | tangible_assets | 6,498 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | investments | 1 | gbp_k | 20 | 17 | Balance sheet | verified_weak |
| FY25 | FY24 | investments | 1 | gbp_k | 20 | 17 | Balance sheet | verified_weak |
| FY25 | FY25 | stocks | 14,964 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | stocks | 16,739 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | debtors | 11,311 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | debtors | 10,777 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | cash | 38,997 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | cash | 28,993 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | creditors_within_1y | 27,213 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | creditors_within_1y | 25,009 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | net_current_assets | 38,059 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | net_current_assets | 31,500 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | creditors_after_1y | 855 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | creditors_after_1y | 1,136 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | deferred_tax | 610 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | deferred_tax | 886 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | provisions | 1,410 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | provisions | 874 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | net_assets | 43,337 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY24 | net_assets | 37,992 | gbp_k | 20 | 17 | Balance sheet | verified |
| FY25 | FY25 | tangible_additions | 910 | gbp_k | 39 | 36 | Note 14 tangible fixed assets | verified |
| FY25 | FY25 | intangible_additions | 835 | gbp_k | 38 | 35 | Note 13 intangible assets | verified |
| FY25 | FY25 | dilapidation_provision | 1,410 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY24 | dilapidation_provision | 874 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY25 | dilapidation_utilised | 249 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY24 | dilapidation_utilised | 195 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY25 | dilapidation_charge | 785 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY24 | dilapidation_charge | 26 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY25 | returns_provision | 3,320 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY24 | returns_provision | 3,105 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY25 | stock_provision | 1,225 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY24 | stock_provision | 1,014 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY25 | FY25 | lease_commitments_total | 14,786 | gbp_k | 44 | 41 | Note 27 commitments | verified |
| FY25 | FY24 | lease_commitments_total | 16,123 | gbp_k | 44 | 41 | Note 27 commitments | verified |
| FY25 | FY25 | lease_commitments_within_1y | 5,034 | gbp_k | 44 | 41 | Note 27 commitments | verified |
| FY25 | FY24 | lease_commitments_within_1y | 4,836 | gbp_k | 44 | 41 | Note 27 commitments | verified |
| FY25 | FY25 | standalone_stores | 53 | count | 4 | 1 | Strategic report business review | verified |
| FY25 | FY25 | concession_stores | 51 | count | 4 | 1 | Strategic report business review | verified |
| FY25 | FY25 | websites | 7 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY25 | FY25 | concession_opened | 1 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY25 | FY25 | standalone_closed | 1 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY25 | FY25 | online_mix_change_ppt | 5.4 | ppt | 4 | 1 | Strategic report business review | verified |
| FY25 | FY25 | dividends_paid | 10,000 | gbp_k | 8 | 5 | Directors' report | verified |
| FY25 | FY24 | dividends_paid | 25,875 | gbp_k | 8 | 5 | Directors' report | verified |
| FY25 | FY25 | weeks_in_period | 52 | weeks | 14 | 11 | Auditor's report | verified |
| FY24 | FY24 | turnover | 134,735 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | turnover | 139,806 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | cost_of_sales | 103,668 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | cost_of_sales | 96,574 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | gross_profit | 31,067 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | gross_profit | 43,232 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | admin_expenses | 19,173 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | admin_expenses | 22,633 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | other_operating_income | 1,355 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | other_operating_income | 2,153 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | operating_profit | 13,249 | gbp_k | 17 | 14 | Profit and loss account | verified_by_identity |
| FY24 | FY23 | operating_profit | 22,752 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | interest_receivable | 974 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | interest_receivable | 953 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | interest_payable | 0 | gbp_k | 17 | 14 | Profit and loss account | nil_not_checked |
| FY24 | FY23 | interest_payable | 0 | gbp_k | 17 | 14 | Profit and loss account | nil_not_checked |
| FY24 | FY24 | profit_before_tax | 14,223 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | profit_before_tax | 23,705 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | tax | 3,628 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | tax | 3,915 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | profit_after_tax | 10,595 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY23 | profit_after_tax | 19,790 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY24 | FY24 | turnover_uk | 134,735 | gbp_k | 31 | 28 | Note 4 turnover | verified |
| FY24 | FY23 | turnover_uk | 139,806 | gbp_k | 31 | 28 | Note 4 turnover | verified |
| FY24 | FY24 | ooi_other | 1,213 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | ooi_other | 1,933 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | ooi_royalty | 142 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified_by_identity |
| FY24 | FY23 | ooi_royalty | 220 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | fx_differences | -818 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | fx_differences | 797 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | operating_lease_rentals | 4,892 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | operating_lease_rentals | 4,198 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | inventory_impairment | 192 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | inventory_impairment | 67 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | loss_on_disposal | 0 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | nil_not_checked |
| FY24 | FY23 | loss_on_disposal | 5 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified_weak |
| FY24 | FY24 | depreciation | 1,865 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | depreciation | 1,284 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | amortisation | 1,132 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | amortisation | 1,018 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | impairment_tangible | 438 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | impairment_tangible | 0 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | nil_not_checked |
| FY24 | FY24 | pension_dc | 471 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY23 | pension_dc | 467 | gbp_k | 32 | 29 | Note 5-6 other operating income, operating profit | verified |
| FY24 | FY24 | wages_salaries | 16,271 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | wages_salaries | 17,177 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | social_security | 1,332 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | social_security | 1,363 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | pension_cost | 471 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | pension_cost | 467 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | staff_costs_total | 18,074 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | staff_costs_total | 19,007 | gbp_k | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | employees_admin | 162 | count | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | employees_admin | 147 | count | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | employees_store | 623 | count | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | employees_store | 655 | count | 33 | 30 | Note 8 employees | verified |
| FY24 | FY24 | employees_directors | 5 | count | 33 | 30 | Note 8 employees | verified_weak |
| FY24 | FY23 | employees_directors | 5 | count | 33 | 30 | Note 8 employees | verified_weak |
| FY24 | FY24 | employees_total | 790 | count | 33 | 30 | Note 8 employees | verified |
| FY24 | FY23 | employees_total | 807 | count | 33 | 30 | Note 8 employees | verified_by_identity |
| FY24 | FY24 | adjusted_ebitda | 15,866 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY24 | FY23 | adjusted_ebitda | 25,851 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY24 | FY24 | intangible_assets | 2,889 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | intangible_assets | 3,187 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | tangible_assets | 6,498 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | tangible_assets | 6,192 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY24 | FY23 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY24 | FY24 | stocks | 16,739 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | stocks | 11,451 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | debtors | 10,777 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | debtors | 14,550 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | cash | 28,993 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | cash | 40,865 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | creditors_within_1y | 25,009 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | creditors_within_1y | 20,643 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | net_current_assets | 31,500 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | net_current_assets | 46,223 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | creditors_after_1y | 1,136 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | creditors_after_1y | 898 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | deferred_tax | 886 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | deferred_tax | 659 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | provisions | 874 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | provisions | 1,043 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | net_assets | 37,992 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY23 | net_assets | 53,003 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY24 | FY24 | tangible_additions | 2,640 | gbp_k | 37 | 34 | Note 14 tangible fixed assets | verified |
| FY24 | FY24 | intangible_additions | 836 | gbp_k | 36 | 33 | Note 13 intangible assets | verified |
| FY24 | FY24 | dilapidation_provision | 874 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY23 | dilapidation_provision | 1,044 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY24 | dilapidation_utilised | 195 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY23 | dilapidation_utilised | 48 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY24 | dilapidation_charge | 26 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY23 | dilapidation_charge | 694 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY24 | returns_provision | 3,105 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY23 | returns_provision | 3,191 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY24 | stock_provision | 1,014 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY23 | stock_provision | 822 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY24 | FY24 | lease_commitments_total | 16,123 | gbp_k | 43 | 40 | Note 27 commitments | verified |
| FY24 | FY23 | lease_commitments_total | 12,730 | gbp_k | 43 | 40 | Note 27 commitments | verified |
| FY24 | FY24 | lease_commitments_within_1y | 4,836 | gbp_k | 43 | 40 | Note 27 commitments | verified |
| FY24 | FY23 | lease_commitments_within_1y | 4,194 | gbp_k | 43 | 40 | Note 27 commitments | verified |
| FY24 | FY24 | standalone_stores | 54 | count | 4 | 1 | Strategic report business review | verified |
| FY24 | FY24 | concession_stores | 48 | count | 4 | 1 | Strategic report business review | verified |
| FY24 | FY24 | websites | 7 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY24 | FY24 | standalone_opened | 3 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY24 | FY24 | concession_opened | 0 | count | 4 | 1 | Strategic report business review | nil_not_checked |
| FY24 | FY24 | standalone_closed | 1 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY24 | FY24 | concession_closed | 1 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY24 | FY24 | standalone_relocated | 2 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY24 | FY24 | concession_sales_growth_pct | -13.5 | pct | 4 | 1 | Strategic report business review | verified |
| FY24 | FY24 | owned_mix_change_ppt | 2.9 | ppt | 4 | 1 | Strategic report business review | verified |
| FY24 | FY24 | dividends_paid | 25,875 | gbp_k | 8 | 5 | Directors' report | verified |
| FY24 | FY23 | dividends_paid | 20,000 | gbp_k | 8 | 5 | Directors' report | verified |
| FY24 | FY24 | weeks_in_period | 52 | weeks | 13 | 10 | Auditor's report | verified |
| FY23 | FY23 | turnover | 139,806 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | turnover | 143,675 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | cost_of_sales | 96,574 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | cost_of_sales | 93,244 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | gross_profit | 43,232 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | gross_profit | 50,431 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | admin_expenses | 22,633 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | admin_expenses | 21,048 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | other_operating_income | 2,153 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | other_operating_income | 1,177 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | operating_profit | 22,752 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | operating_profit | 30,560 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | interest_receivable | 953 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | interest_receivable | 151 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | interest_payable | 0 | gbp_k | 17 | 14 | Profit and loss account | nil_not_checked |
| FY23 | FY22 | interest_payable | 2 | gbp_k | 17 | 14 | Profit and loss account | verified_weak |
| FY23 | FY23 | profit_before_tax | 23,705 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | profit_before_tax | 30,709 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | tax | 3,915 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | tax | 5,251 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | profit_after_tax | 19,790 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY22 | profit_after_tax | 25,458 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY23 | FY23 | turnover_uk | 139,806 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY22 | turnover_uk | 143,593 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY23 | turnover_rest_of_world | 0 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | nil_not_checked |
| FY23 | FY22 | turnover_rest_of_world | 82 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY23 | ooi_other | 1,933 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY22 | ooi_other | 965 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY23 | ooi_royalty | 220 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY22 | ooi_royalty | 212 | gbp_k | 32 | 29 | Note 4-5 turnover, other operating income | verified |
| FY23 | FY23 | fx_differences | 797 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | fx_differences | -32 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | operating_lease_rentals | 4,198 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | operating_lease_rentals | 3,864 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | inventory_impairment | 67 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | inventory_impairment | -74 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | loss_on_disposal | 5 | gbp_k | 33 | 30 | Note 6 operating profit | verified_weak |
| FY23 | FY22 | loss_on_disposal | 0 | gbp_k | 33 | 30 | Note 6 operating profit | nil_not_checked |
| FY23 | FY23 | depreciation | 1,284 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | depreciation | 1,034 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | amortisation | 1,018 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | amortisation | 850 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | impairment_tangible | 0 | gbp_k | 33 | 30 | Note 6 operating profit | nil_not_checked |
| FY23 | FY22 | impairment_tangible | 21 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | pension_dc | 467 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY22 | pension_dc | 375 | gbp_k | 33 | 30 | Note 6 operating profit | verified |
| FY23 | FY23 | wages_salaries | 17,177 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | wages_salaries | 16,856 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | social_security | 1,363 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | social_security | 1,374 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | pension_cost | 467 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | pension_cost | 375 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | staff_costs_total | 19,007 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | staff_costs_total | 18,605 | gbp_k | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | employees_admin | 147 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | employees_admin | 132 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | employees_store | 655 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | employees_store | 565 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | employees_directors | 5 | count | 34 | 31 | Note 8 employees | verified_weak |
| FY23 | FY22 | employees_directors | 5 | count | 34 | 31 | Note 8 employees | verified_weak |
| FY23 | FY23 | employees_total | 807 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY22 | employees_total | 702 | count | 34 | 31 | Note 8 employees | verified |
| FY23 | FY23 | adjusted_ebitda | 25,851 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY23 | FY22 | adjusted_ebitda | 32,433 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY23 | FY23 | intangible_assets | 3,187 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | intangible_assets | 2,840 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | tangible_assets | 6,192 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | tangible_assets | 3,751 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY23 | FY22 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY23 | FY23 | stocks | 11,451 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | stocks | 14,206 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | debtors | 14,550 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | debtors | 11,147 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | current_asset_investments | 0 | gbp_k | 19 | 16 | Balance sheet | nil_not_checked |
| FY23 | FY22 | current_asset_investments | 10,000 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | cash | 40,865 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | cash | 41,139 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | creditors_within_1y | 20,643 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | creditors_within_1y | 28,200 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | net_current_assets | 46,223 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | net_current_assets | 48,292 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | creditors_after_1y | 898 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | creditors_after_1y | 1,081 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | deferred_tax | 659 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | deferred_tax | 283 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | provisions | 1,043 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | provisions | 397 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | net_assets | 53,003 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY22 | net_assets | 53,123 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY23 | FY23 | tangible_additions | 3,726 | gbp_k | 38 | 35 | Note 15 tangible fixed assets | verified |
| FY23 | FY23 | intangible_additions | 1,395 | gbp_k | 37 | 34 | Note 14 intangible assets | verified |
| FY23 | FY23 | dilapidation_provision | 1,044 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY22 | dilapidation_provision | 397 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY23 | dilapidation_utilised | 48 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY22 | dilapidation_utilised | 92 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY23 | dilapidation_charge | 694 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY22 | dilapidation_charge | 0 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | nil_not_checked |
| FY23 | FY23 | returns_provision | 3,191 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY22 | returns_provision | 3,680 | gbp_k | 31 | 28 | Note 3 estimation uncertainty | verified |
| FY23 | FY23 | stock_provision | 822 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY23 | FY22 | stock_provision | 662 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY23 | FY23 | lease_commitments_total | 12,730 | gbp_k | 45 | 42 | Note 29 commitments | verified |
| FY23 | FY22 | lease_commitments_total | 8,927 | gbp_k | 45 | 42 | Note 29 commitments | verified |
| FY23 | FY23 | lease_commitments_within_1y | 4,194 | gbp_k | 45 | 42 | Note 29 commitments | verified |
| FY23 | FY22 | lease_commitments_within_1y | 3,250 | gbp_k | 45 | 42 | Note 29 commitments | verified |
| FY23 | FY23 | standalone_stores | 52 | count | 4 | 1 | Strategic report business review | verified |
| FY23 | FY23 | concession_stores | 49 | count | 4 | 1 | Strategic report business review | verified |
| FY23 | FY23 | websites | 7 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY23 | FY23 | standalone_opened | 4 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY23 | FY23 | concession_opened | 1 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY23 | FY23 | concession_closed | 8 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY23 | FY23 | dividends_paid | 20,000 | gbp_k | 8 | 5 | Directors' report | verified |
| FY23 | FY22 | dividends_paid | 0 | gbp_k | 8 | 5 | Directors' report | nil_not_checked |
| FY23 | FY23 | weeks_in_period | 52 | weeks | 13 | 10 | Auditor's report | verified |
| FY22 | FY22 | turnover | 143,675 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | turnover | 117,761 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | cost_of_sales | 93,244 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | cost_of_sales | 78,374 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | gross_profit | 50,431 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | gross_profit | 39,387 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | admin_expenses | 21,048 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | admin_expenses | 15,511 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | other_operating_income | 1,177 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | other_operating_income | 2,612 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | operating_profit | 30,560 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | operating_profit | 26,488 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | interest_receivable | 151 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | interest_receivable | 0 | gbp_k | 17 | 14 | Profit and loss account | nil_not_checked |
| FY22 | FY22 | interest_payable | 2 | gbp_k | 17 | 14 | Profit and loss account | verified_weak |
| FY22 | FY21 | interest_payable | 99 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | profit_before_tax | 30,709 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | profit_before_tax | 26,389 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | tax | 5,251 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | tax | 4,899 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | profit_after_tax | 25,458 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY21 | profit_after_tax | 21,490 | gbp_k | 17 | 14 | Profit and loss account | verified |
| FY22 | FY22 | ooi_other | 965 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | ooi_other | 962 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | ooi_royalty | 212 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | ooi_royalty | 46 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | ooi_government_grants | 0 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | nil_not_checked |
| FY22 | FY21 | ooi_government_grants | 1,604 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | cost_of_stock_expensed | 41,639 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | cost_of_stock_expensed | 35,299 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | fx_differences | -32 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | fx_differences | -237 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | operating_lease_rentals | 3,864 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | operating_lease_rentals | 3,457 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | loss_on_disposal | 0 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | nil_not_checked |
| FY22 | FY21 | loss_on_disposal | 183 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | depreciation | 1,034 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | depreciation | 1,063 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | amortisation | 850 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | amortisation | 695 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | impairment_tangible | 21 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | impairment_tangible | 0 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | nil_not_checked |
| FY22 | FY22 | pension_dc | 375 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY21 | pension_dc | 298 | gbp_k | 34 | 31 | Note 5-6 other operating income, operating profit | verified |
| FY22 | FY22 | wages_salaries | 16,856 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | wages_salaries | 12,590 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | social_security | 1,374 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | social_security | 809 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | pension_cost | 375 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | pension_cost | 298 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | staff_costs_total | 18,605 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | staff_costs_total | 13,697 | gbp_k | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | employees_admin | 132 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | employees_admin | 114 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | employees_store | 565 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | employees_store | 527 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | employees_directors | 5 | count | 35 | 32 | Note 8 employees | verified_weak |
| FY22 | FY21 | employees_directors | 4 | count | 35 | 32 | Note 8 employees | verified_weak |
| FY22 | FY22 | employees_total | 702 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY21 | employees_total | 645 | count | 35 | 32 | Note 8 employees | verified |
| FY22 | FY22 | adjusted_ebitda | 32,433 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY22 | FY21 | adjusted_ebitda | 28,007 | gbp_k | 5 | 2 | Strategic report KPI | verified |
| FY22 | FY22 | intangible_assets | 2,840 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | intangible_assets | 2,441 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | tangible_assets | 3,751 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | tangible_assets | 3,115 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY22 | FY21 | investments | 1 | gbp_k | 19 | 16 | Balance sheet | verified_weak |
| FY22 | FY22 | stocks | 14,206 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | stocks | 9,974 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | debtors | 11,147 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | debtors | 9,249 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | current_asset_investments | 10,000 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | current_asset_investments | 0 | gbp_k | 19 | 16 | Balance sheet | nil_not_checked |
| FY22 | FY22 | cash | 41,139 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | cash | 26,328 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | creditors_within_1y | 28,200 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | creditors_within_1y | 21,465 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | net_current_assets | 48,292 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | net_current_assets | 24,086 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | creditors_after_1y | 1,081 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | creditors_after_1y | 1,186 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | deferred_tax | 283 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | deferred_tax | 12 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | provisions | 397 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | provisions | 523 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | net_assets | 53,123 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY21 | net_assets | 27,922 | gbp_k | 19 | 16 | Balance sheet | verified |
| FY22 | FY22 | tangible_additions | 1,940 | gbp_k | 40 | 37 | Note 15 tangible fixed assets | verified |
| FY22 | FY22 | intangible_additions | 1,001 | gbp_k | 39 | 36 | Note 14 intangible assets | verified |
| FY22 | FY22 | dilapidation_provision | 397 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY22 | FY21 | dilapidation_provision | 489 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY22 | FY22 | dilapidation_utilised | 92 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY22 | FY21 | dilapidation_utilised | 0 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | nil_not_checked |
| FY22 | FY22 | dilapidation_charge | 0 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | nil_not_checked |
| FY22 | FY21 | dilapidation_charge | 241 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY22 | FY22 | returns_provision | 3,680 | gbp_k | 32 | 29 | Note 3 estimation uncertainty | verified |
| FY22 | FY22 | stock_provision | 662 | gbp_k | 33 | 30 | Note 3 estimation uncertainty | verified |
| FY22 | FY21 | stock_provision | 720 | gbp_k | 33 | 30 | Note 3 estimation uncertainty | verified |
| FY22 | FY22 | inventory_impairment | -58 | gbp_k | 33 | 30 | Note 3 estimation uncertainty | verified |
| FY22 | FY21 | inventory_impairment | 211 | gbp_k | 33 | 30 | Note 3 estimation uncertainty | verified |
| FY22 | FY22 | lease_commitments_total | 20,067 | gbp_k | 47 | 44 | Note 29 commitments | verified |
| FY22 | FY21 | lease_commitments_total | 21,162 | gbp_k | 47 | 44 | Note 29 commitments | verified |
| FY22 | FY22 | lease_commitments_within_1y | 4,105 | gbp_k | 47 | 44 | Note 29 commitments | verified |
| FY22 | FY21 | lease_commitments_within_1y | 3,825 | gbp_k | 47 | 44 | Note 29 commitments | verified |
| FY22 | FY22 | standalone_stores | 48 | count | 4 | 1 | Strategic report business review | verified |
| FY22 | FY22 | concession_stores | 56 | count | 4 | 1 | Strategic report business review | verified |
| FY22 | FY22 | websites | 8 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY22 | FY22 | standalone_opened | 6 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY22 | FY22 | concession_opened | 2 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY22 | FY22 | standalone_closed | 2 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY22 | FY22 | concession_closed | 4 | count | 4 | 1 | Strategic report business review | verified_weak |
| FY22 | FY22 | dividends_paid | 0 | gbp_k | 8 | 5 | Directors' report | nil_not_checked |
| FY22 | FY21 | dividends_paid | 25,000 | gbp_k | 8 | 5 | Directors' report | verified |
| FY22 | FY22 | weeks_in_period | 52 | weeks | 13 | 10 | Auditor's report | verified |
