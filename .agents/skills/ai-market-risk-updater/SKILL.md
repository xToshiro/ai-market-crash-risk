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

### Step 1: Ingest Data & Review Benchmarks
1. Consult [sources_and_apis.md](./references/sources_and_apis.md) for verified data feed locations (FRED, TreasuryDirect, SEC EDGAR, KBRA, TSMC monthly releases).
2. Record newly observed metrics in a structured draft dictionary matching the schema in `scripts/generate_macro_geopolitical_crash_report.py` (`FACTS`).

### Step 2: Recalibrate Mathematical Models
1. Consult [quantitative_methodologies.md](./references/quantitative_methodologies.md) to apply stress test formulas:
   - **GPU Depreciation vs. Amortization**: Recalculate half-life decay constants $\lambda$ and Loan-to-Value (LTV) ratios.
   - **DSCR Covenant Breaches**: Check if rental spot rates drive Debt Service Coverage below $1.10x$.
   - **Geopolitical Vulnerability Index (GVI)**: Update scores across the 6 weighted channels ($E, F, X, T, M, G$) and regional overlays.
   - **Scenario Probability Buildup**: Ensure probabilities for S1 (Orderly Deflation), S2 (Credit Dislocation), and S3 (Systemic Contagion) sum to exactly 100%.

### Step 3: Run Model Validation
Execute the verification script to ensure mathematical consistency before building documents:
```bash
py .agents/skills/ai-market-risk-updater/scripts/validate_models.py
```
Ensure all assertions pass (zero NaNs, probability sums equal 100%, LTV ranges within [0, 1]).

### Step 4: Recompile Visual Assets & PDF Reports
Refer to [update_workflow.md](./references/update_workflow.md) for execution commands:
```bash
# Rebuild all 12 executive PDF reports (EN & PT) and chart assets
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
