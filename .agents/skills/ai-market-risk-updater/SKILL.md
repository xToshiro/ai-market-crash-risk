---
name: ai-market-risk-updater
description: >-
  Use this skill whenever the user asks to update, calibrate, or refresh market crash forecasts,
  macroeconomic indicators, GPU collateral valuation models, Data Center ABS tranches, or
  regenerate institutional PDF and Markdown reports for the AI infrastructure market.
---

# AI Market Risk & Forecast Updater

This skill defines the end-to-end institutional workflow for ingesting new economic data, recalibrating financial stress models, re-simulating crash probabilities (2026–2029), and compiling both English and Portuguese executive PDF reports.

## When to Activate This Skill

- The user requests an update to US fiscal numbers (national debt, budget deficit, net interest outlays).
- New SEC filings (10-K, 10-Q) or private credit facility updates are released for NVIDIA, CoreWeave, Microsoft, Amazon, Google, or Oracle.
- Secondary market GPU pricing indexes or cloud rental spot rates (H100, B200) shift.
- KBRA, S&P, or Moody's issue new Data Center ABS rating criteria or pre-sale reports.
- Geopolitical flashpoints evolve in the Taiwan Strait, Middle East, or energy transit straits.
- The user requests re-generation of the 12 executive PDF reports or 14 Markdown dossiers.

---

## Standard Update Workflow

### Step 1: Run Automated Market Intelligence Pipeline (Numeric Ingestion)
Execute the single-command automated pipeline to fetch updated prices, multiples, yields, and investment flows:
```bash
py scripts/fetch_market_pipeline.py
```
This updates structured CSV files in `data/`:
- `data/latest_market_metrics.csv`: Unified dataset of all 45+ assets and macro indicators.
- `data/companies_valuation_metrics.csv`: AI Hyperscalers, Semis, Power/Grid utilities, Neoclouds, and Private Credit.
- `data/macro_financial_condition.csv`: 10Y/30Y/13W Treasury yields, US national debt ($36.8T+), S&P 500, Nasdaq, VIX, Oil, Gold.
- `data/investment_flows_credit.csv`: Sector ETFs (QQQ, SMH, XLU, PAVE) and credit spread proxies (HYG, LQD, HYG/LQD ratio).
- `data/ai_agent_research_brief.md`: Automated brief highlighting statistical anomalies and targeted search queries.

### Step 2: Targeted Web Research on Trusted Sources (Qualitative Synthesis)
The AI Agent **MUST** review `data/ai_agent_research_brief.md` and conduct targeted web searches to uncover the qualitative catalysts behind the numbers.

**Trusted Media Whitelist**:
- Financial Press: *Financial Times* (`site:ft.com`), *Bloomberg* (`site:bloomberg.com`), *Wall Street Journal* (`site:wsj.com`), *Reuters* (`site:reuters.com`).
- Regulatory & Official Filings: SEC EDGAR (`site:sec.gov` for 10-K, 10-Q, 8-K), Federal Reserve (`federalreserve.gov`), TreasuryDirect (`treasurydirect.gov`).
- Credit & Energy Authorities: KBRA (`kbra.com`), EIA (`eia.gov`), Regional Grid Operators (PJM, National Grid UK).

**Targeted Research Themes**:
1. *Data Center Grid Bottlenecks*: Power interconnect cancellations, utility backlog queues (7-10 years), PPA contract revisions.
2. *AI Frontier & Valuation*: Pre-IPO funding rounds, valuation discounts, compute cost vs. software revenue realization.
3. *Sovereign Fiscal Stress*: Treasury refunding announcements, foreign debt liquidation (Japan, China), interest burden ($1.16T+ run-rate).
4. *Private Credit & Vendor Financing*: GPU-backed term loans, neocloud circularity, ABS tranche structuring.

### Step 3: Recalibrate Mathematical Models
1. Consult [quantitative_methodologies.md](./references/quantitative_methodologies.md) to apply stress test formulas:
   - **GPU Depreciation vs. Amortization**: Recalculate half-life decay constants $\lambda$ and Loan-to-Value (LTV) ratios.
   - **DSCR Covenant Breaches**: Check if rental spot rates drive Debt Service Coverage below $1.10x$.
   - **Geopolitical Vulnerability Index (GVI)**: Update scores across the 6 weighted channels ($E, F, X, T, M, G$) and regional overlays.
   - **Scenario Probability Buildup**: Ensure probabilities for S1 (Orderly Deflation), S2 (Credit Dislocation), and S3 (Systemic Contagion) sum to exactly 100%.

### Step 4: Run Model Validation
Execute the verification script to ensure mathematical and file integrity before building documents:
```bash
py .agents/skills/ai-market-risk-updater/scripts/validate_models.py
```
Ensure all assertions pass (zero NaNs, probability sums equal 100%, LTV ranges within [0, 1], all 16 PDFs verified).

### Step 5: Recompile Visual Assets & PDF Reports
Refer to [update_workflow.md](./references/update_workflow.md) for execution commands:
```bash
# Rebuild all 16 executive PDF reports (EN & PT) and high-res chart assets
py scripts/build_all_reports.py
```

### Step 5: Update Synchronized Documentation
1. Update figures in English dossiers (`docs/en/*.md`).
2. Update corresponding figures in Portuguese dossiers (`docs/pt/*.md`).
3. Update summary metrics in the root [README.md](../../../README.md).

### Step 6: Git Commit & Push Protocol
Ensure all modified PDFs, markdown files, and charts are staged and pushed:
```bash
git add -A
git commit -m "Update QX-202X market risk forecasts, recalibrate ABS tranches, and rebuild PDF reports"
git push origin main
```

---

## Detailed References

- [Data Sources & APIs Reference](./references/sources_and_apis.md): Official government, credit rating, and silicon data feeds.
- [Quantitative Methodologies & Formulas](./references/quantitative_methodologies.md): Mathematical formulations for debt waterfalls, LTV triggers, and geopolitical risk scoring.
- [Update Workflow & Script Guide](./references/update_workflow.md): Step-by-step instructions on updating parameters in Python scripts.
