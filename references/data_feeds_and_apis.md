# Quantitative Data Feeds & Automated Ingestion APIs

This technical manual documents the specific API endpoints, ticker symbols, series codes, and ingestion routines utilized by `scripts/fetch_market_pipeline.py`.

---

## 1. Federal Reserve Economic Data (FRED) API

* **Host**: `https://fred.stlouisfed.org`
* **Protocol**: HTTPS GET (CSV direct endpoint or JSON REST)
* **Ingestion Script**: `scripts/fetch_market_pipeline.py`

| Indicator | FRED Series ID | Direct CSV Query URL | Target CSV Output |
| :--- | :--- | :--- | :--- |
| **US 10-Year Treasury Yield** | `DGS10` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10` | `data/macro_financial_condition.csv` (`yield_10y`) |
| **US 2-Year Treasury Yield** | `DGS2` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2` | `data/macro_financial_condition.csv` (`yield_2y`) |
| **10Y-2Y Treasury Yield Spread** | `T10Y2Y` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y` | `data/macro_financial_condition.csv` (`yield_curve_spread`) |
| **US High Yield Option-Adjusted Spread**| `BAMLH0A0HYM2` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2` | `data/macro_financial_condition.csv` (`hy_credit_spread_bps`) |
| **Federal Funds Effective Rate** | `FEDFUNDS` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS` | `data/macro_financial_condition.csv` (`fed_funds_rate`) |
| **Fed Total Balance Sheet Assets** | `WALCL` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL` | `data/macro_financial_condition.csv` (`fed_total_assets_tn`) |

---

## 2. US Department of the Treasury Fiscal Data API

* **Host**: `https://api.fiscaldata.treasury.gov`
* **Endpoint**: `/services/api/fiscal_service/v2/accounting/od/debt_to_penny`
* **Query Format**: `?sort=-record_date&page[size]=1`
* **Returned Fields**:
  * `record_date`: Latest accounting business date.
  * `tot_pub_debt_out_amt`: Total public debt outstanding ($36.85+ Trillion).
  * `debt_held_public_amt`: Debt held by the public ($28.9+ Trillion).
  * `intragov_hold_amt`: Intragovernmental holdings.

---

## 3. Financial Markets & Equity Leaders (Yahoo Finance Feed)

* **Host**: `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}`
* **Interval**: Daily / Monthly (`interval=1d&range=2y`)

| Company / Asset | Ticker | Parameter Role |
| :--- | :--- | :--- |
| **Nvidia Corporation** | `NVDA` | Hardware pricing anchor, gross margin tracking (75%), fabless multiple. |
| **Microsoft Corporation** | `MSFT` | Hyperscaler CapEx pace, Azure enterprise ARR, Nscale Essex lease counterparty. |
| **Alphabet Inc.** | `GOOGL` | Defensive cash cushion ($88B net cash), TPU custom silicon, cloud margins. |
| **Amazon.com, Inc.** | `AMZN` | AWS cloud run-rate, Talen Energy nuclear PPA, Anthropic primary investor. |
| **Meta Platforms, Inc.** | `META` | Open-source model compute driver (Llama), consumer ad-funded CapEx. |
| **Taiwan Semiconductor (TSMC)**| `TSM` | Physical silicon foundry monopoly, CoWoS packaging capacity limit. |
| **Broadcom Inc.** | `AVGO` | High-speed AI cluster switching infrastructure, custom ASICs. |
| **Oracle Corporation** | `ORCL` | OCI data center debt leverage, high exposure to neoclouds. |
| **S&P 500 Benchmark** | `^GSPC` | Broad equity multiple benchmark (P/E ~23.4x). |
| **Nasdaq 100 Index** | `^IXIC` | Tech concentration benchmark (P/E ~29.5x). |
| **High Yield Corporate ETF** | `HYG` | Risk appetite barometer in sub-investment-grade corporate debt. |
| **Investment Grade Corporate**| `LQD` | Senior corporate credit spread benchmark (`HYG/LQD` ratio: 0.7433). |
| **CBOE Volatility Index** | `^VIX` | Implied equity market volatility index. |

---

## 4. SEC EDGAR CIK Central Registry

* **Host**: `https://www.sec.gov/edgar/browse/?CIK={cik}`

| Entity | CIK Code | Mandatory Audit Sections |
| :--- | :--- | :--- |
| **NVIDIA Corporation** | `0001045810` | Item 7 (MD&A), Note 14 (Customer Concentration > 10%), Purchase Commitments. |
| **Microsoft Corporation** | `0000789019` | Statement of Cash Flows (Additions to PP&E), Note 13 (Leases & Cloud Facilities). |
| **Alphabet Inc.** | `0001652044` | Segment Reporting (Google Cloud Operating Income), Capital Expenditures. |
| **Amazon.com, Inc.** | `0001018724` | AWS Segment Financials, Lease Liabilities (Operating vs. Financing). |
| **Oracle Corporation** | `0001341439` | Debt Maturity Schedule, Cloud Infrastructure Obligations. |
