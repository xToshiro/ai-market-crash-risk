# Data Sources & Official Feeds Reference

This document catalogs the institutional data sources, APIs, and periodic filings required to update the risk forecast models.

---

## 1. Sovereign Debt & Macroeconomic Feeds

| Indicator | Primary Source | Access URL / Query | Update Frequency | Target Parameters in Code |
|:---|:---|:---|:---:|:---|
| **Total US National Debt** | US Treasury (Fiscal Data) | `api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny` | Daily | `debt_total_tn`, `debt_public_tn` |
| **Federal Budget Deficit** | Congressional Budget Office (CBO) / CRFB | `cbo.gov/topics/budget` | Quarterly / Annual | `deficit_fy26_tn`, `deficit_fy26_pct` |
| **Net Interest Outlays** | US Treasury Monthly Treasury Statement (MTS) | `fiscaldata.treasury.gov` | Monthly | `net_interest_tn` |
| **10Y & 2Y Treasury Yields** | FRED (Federal Reserve Bank of St. Louis) | `fred.stlouisfed.org/series/DGS10`, `DGS2` | Daily | `yield_10y`, `yield_curve_spread` |
| **Foreign Sovereign Holdings** | Treasury International Capital (TIC) | `treasury.gov/resource-center/data-chart-center/tic` | Monthly (15th) | `japan_ust_tn`, `china_ust_tn` |

---

## 2. Hyperscalers & Silicon Supply Chain

| Entity | Filing / Source | Key Items to Audit | Target Parameters |
|:---|:---|:---|:---|
| **NVIDIA Corporation (NVDA)** | SEC EDGAR Form 10-K / 10-Q | Customer Concentration (Note 14), Purchase Obligations, Deferred Revenue, Strategic Investments. | Vendor financing ratios, hardware margins. |
| **Microsoft Corporation (MSFT)** | SEC EDGAR Form 10-K / 10-Q | Capital Expenditures (Cash Flow Statement), Long-term lease commitments for cloud infrastructure. | CapEx growth rate, PPA off-balance commitments. |
| **Alphabet / Amazon / Oracle** | SEC EDGAR Form 10-K / 10-Q | AI infrastructure commitments, contractual data center lease obligations. | Hyperscaler CapEx vs. Software ARR. |
| **TSMC (Taiwan Semiconductor)** | Monthly Revenue & Quarterly Earnings | Monthly revenue releases (10th of every month), CoWoS packaging capacity expansion figures. | Advanced silicon supply constraints, Taiwan Strait concentration. |

---

## 3. Private Credit & Neocloud Filings

| Operator | Credit Facility Partners | Monitoring Focus | Target Parameters |
|:---|:---|:---|:---|
| **CoreWeave** | Blackstone, Magnetar, Coatue, Carlyle | Debt facilities collateralized by H100/B200 clusters, UCC-1 financing statements filed in Delaware. | `debt_snowball_neoclouds`, `dscr_current`. |
| **Lambda Labs** | Macquarie, Industrial Bank | Asset-backed loan structures for GPU hardware fleets. | LTV covenant limits, haircut assumptions. |
| **Crusoe Cloud** | Upper90, Blue Owl | Energy-integrated computing facilities, debt-to-equity leverage. | Power purchase agreement pricing. |

---

## 4. Structured Finance & Data Center ABS

| Agency / Source | Platform | Criteria to Track | Target Parameters |
|:---|:---|:---|:---|
| **KBRA (Kroll Bond Rating Agency)** | `kbra.com` Structured Finance | *Global Data Center ABS Rating Methodology*: Minimum DSCR for Class A notes (typically 1.30x–1.40x), maximum LTV thresholds (typically 65%–75%), liquidation timing assumptions. | Tranche subordination percentages, credit enhancement levels. |
| **S&P Global Ratings** | `spglobal.com` | Structured finance default and transition studies for esoteric ABS. | Subordinate tranche default probabilities. |
| **Finsight** | `finsight.com` | Primary issuance pricing spreads, oversubscription levels, and covenant terms on new Data Center ABS offerings. | Spreads over benchmark Treasuries. |

---

## 5. GPU Secondary Market & Cloud Spot Pricing

| Marketplace | Scraping / Observation Target | Warning Trigger Thresholds |
|:---|:---|:---|
| **RunPod / Vast.ai / TensorDock** | Hourly spot pricing for 8x H100 SXM5 / B200 nodes. | Sustained spot rate $< \$1.50$/GPU-hour indicates negative equity for debt-financed clusters. |
| **Silicon Resale Brokers** | Secondary refurbished hardware transaction values. | Resale price $< 40\%$ of initial purchase price within 24 months. |
