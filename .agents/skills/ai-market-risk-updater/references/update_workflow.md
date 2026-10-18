# Update Workflow & Script Guide

This document describes how to execute the automated market intelligence pipeline, update parameters in code, re-generate charts, and compile reports.

---

## 1. Automated Market Intelligence Pipeline (Data Ingestion)

Before editing code parameters, run the automated pipeline to refresh live financial metrics across 45+ tickers, US sovereign yields, and credit spreads:

```bash
# Execute pipeline from repository root
py scripts/fetch_market_pipeline.py
```

### Generated CSV Deliverables in `data/`:
1. `data/latest_market_metrics.csv`: Consolidated snapshot of all equities, macro indicators, and flows.
2. `data/companies_valuation_metrics.csv`: Detailed valuation multiples (P/E, EV/EBITDA, P/S), market cap, and 2-year trajectory.
3. `data/macro_financial_condition.csv`: 10Y/30Y/13W yields, dollar index, commodities, and US fiscal debt run-rate.
4. `data/investment_flows_credit.csv`: Thematic ETF flows (SMH, XLU, PAVE) and credit appetite ratio (`HYG / LQD`).
5. `data/snapshots/snapshot_YYYYMMDD_HHMM.csv`: Time-stamped archival history.
6. `data/ai_agent_research_brief.md`: Curated brief with suggested web search queries for the AI Agent.

---

## 2. Parameter Locations in Python Scripts

| File | Target Dictionary / Array | Variables to Update |
|:---|:---|:---|
| `scripts/generate_macro_geopolitical_crash_report.py` | `FACTS` (Lines 48–65) | `debt_total_tn`, `deficit_fy26_tn`, `net_interest_tn`, `japan_ust_tn`. |
| `scripts/generate_macro_geopolitical_crash_report.py` | `SCENARIOS` (Lines 68–74) | Probabilities and impact metrics for S1, S2, S3. |
| `scripts/generate_macro_geopolitical_crash_report.py` | `OVERLAY` (Lines 110–135) | Regional geopolitical overlay modifiers. |
| `scripts/generate_us_market_report.py` | `DATA_INDICES`, `DATA_TREASURIES` | S&P 500, Nasdaq, 10Y Yields, CapEx totals. |
| `scripts/generate_market_crash_scenarios_report.py` | `DATA_VALUATION`, `SCENARIO_PROBS` | P/E multiples, private tech valuations, default rates. |
| `scripts/generate_data_center_abs_tranches_report.py` | `TRANCHES` | KBRA Class A / Class B tranche spreads, LTV, and credit enhancement. |
| `scripts/generate_leverage_multiplier_report.py` | `DEBT_FACILITIES` | CoreWeave, Lambda Labs loan amounts, interest rates, and GPU collateral counts. |
| `scripts/generate_recent_market_update_report.py` | `UPDATE_METRICS`, `GRID_STATUS` | Nscale Essex status, Anthropic valuation haircut, PJM queue. |

---

## 2. Re-Building All Reports

A master runner script is available to compile all 12 PDF reports (both Portuguese and English) and generate all 30+ visual assets:

```bash
# Execute master build script from repository root
py scripts/build_all_reports.py
```

### Running Individual Reports
```bash
# Macro Geopolitical Report (10 Pages)
py scripts/generate_macro_geopolitical_crash_report.py      # PT -> reports/pt/
py scripts/generate_macro_geopolitical_crash_report_en.py   # EN -> reports/en/

# US Financial Market Report (8 Pages)
py scripts/generate_us_market_report.py                    # PT -> reports/pt/
py scripts/generate_us_market_report_en.py                 # EN -> reports/en/

# Crash Scenarios Report (5 Pages)
py scripts/generate_market_crash_scenarios_report.py        # PT -> reports/pt/
py scripts/generate_market_crash_scenarios_report_en.py     # EN -> reports/en/

# Data Center ABS Tranches Report (4 Pages)
py scripts/generate_data_center_abs_tranches_report.py      # PT -> reports/pt/
py scripts/generate_data_center_abs_tranches_report_en.py   # EN -> reports/en/

# Forensic AI Subprime Report (4 Pages)
py scripts/generate_forensic_ai_subprime_report.py          # PT -> reports/pt/
py scripts/generate_forensic_ai_subprime_report_en.py       # EN -> reports/en/

# Leverage Multiplier & Vendor Financing Report (4 Pages)
py scripts/generate_leverage_multiplier_report.py           # PT -> reports/pt/
py scripts/generate_leverage_multiplier_report_en.py        # EN -> reports/en/
```

---

## 3. Post-Build Verification

Run the validation suite to inspect generated PDFs:
```bash
py .agents/skills/ai-market-risk-updater/scripts/validate_models.py
```

The script verifies:
1. All 12 PDF files exist in `reports/pt/` and `reports/en/`.
2. Page count matches exactly:
   - Macro: 10 pages
   - US Market: 8 pages
   - Crash Scenarios: 5 pages
   - Data Center ABS: 4 pages
   - Forensic Subprime: 4 pages
   - Leverage: 4 pages
3. Total compiled pages = 35 (PT) + 35 (EN) = 70 pages.
4. No broken image links or NaN rendering artifacts.
