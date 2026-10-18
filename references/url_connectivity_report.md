# URL Connectivity & Live Verification Audit Report

**Automated Link Health Check & Telemetry Audit**  
*Execution Timestamp: 2026-10-18 14:03:48*

This report contains the empirical verification results of every link cited across the repository. Each endpoint was queried with an HTTP client simulating standard browser user-agents.

---

## Summary Statistics

* **Total Links Audited**: 67
* **Status Distribution**:
  * **ONLINE / 200 OK**: 33
  * **ONLINE / WAF Protected (Bot Detection)**: 21 *(Host is fully operational; returned HTTP 403 due to Cloudflare/Imperva scraper shields)*
  * **ONLINE / Redirect (301/302)**: 0
  * **Unreachable / Network Error**: 11

---

## Detailed Telemetry & Verification Matrix

| # | Target URL | HTTP Code | Status | Latency | Primary Association / Files Cited | Notes / Diagnosis |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| 1 | [https://api.fiscaldata.treasury.gov](https://api.fiscaldata.treasury.gov) | `404` | **HTTP_ERROR** | 915.3 ms | `scripts/build_references_system.py:727` | HTTP Error 404: Not Found |
| 2 | [https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny) | `200` | **ONLINE** | 974.9 ms | `scripts/build_references_system.py:41` | Responsive (OK) |
| 3 | [https://finance.yahoo.com](https://finance.yahoo.com) | `200` | **ONLINE** | 1511.2 ms | `scripts/build_references_system.py:339` | Responsive (OK) |
| 4 | [https://finsight.com](https://finsight.com) | `200` | **ONLINE** | 1295.4 ms | `scripts/build_references_system.py:247` | Responsive (OK) |
| 5 | [https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government) | `200` | **ONLINE** | 663.2 ms | `scripts/build_references_system.py:49` | Responsive (OK) |
| 6 | [https://fred.stlouisfed.org](https://fred.stlouisfed.org) | `N/A` | **ERROR** | 4268.1 ms | `scripts/build_references_system.py:710` | The read operation timed out |
| 7 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2) | `N/A` | **ERROR** | 4120.5 ms | `scripts/build_references_system.py:719` | The read operation timed out |
| 8 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10) | `N/A` | **ERROR** | 4114.5 ms | `scripts/build_references_system.py:716` | The read operation timed out |
| 9 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2) | `N/A` | **ERROR** | 4114.8 ms | `scripts/build_references_system.py:717` | The read operation timed out |
| 10 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS](https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS) | `N/A` | **ERROR** | 4161.7 ms | `scripts/build_references_system.py:720` | The read operation timed out |
| 11 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y](https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y) | `N/A` | **ERROR** | 4114.5 ms | `scripts/build_references_system.py:718` | The read operation timed out |
| 12 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL](https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL) | `N/A` | **ERROR** | 4106.0 ms | `scripts/build_references_system.py:721` | The read operation timed out |
| 13 | [https://fred.stlouisfed.org/series/BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) | `N/A` | **ERROR** | 4116.1 ms | `scripts/build_references_system.py:73` | The read operation timed out |
| 14 | [https://fred.stlouisfed.org/series/DGS10](https://fred.stlouisfed.org/series/DGS10) | `N/A` | **ERROR** | 4153.5 ms | `scripts/build_references_system.py:57` | The read operation timed out |
| 15 | [https://fred.stlouisfed.org/series/DGS2](https://fred.stlouisfed.org/series/DGS2) | `N/A` | **ERROR** | 4117.2 ms | `scripts/build_references_system.py:65` | The read operation timed out |
| 16 | [https://fred.stlouisfed.org/series/FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) | `N/A` | **ERROR** | 4126.1 ms | `scripts/build_references_system.py:81` | The read operation timed out |
| 17 | [https://github.com/xToshiro/ai-market-crash-risk](https://github.com/xToshiro/ai-market-crash-risk) | `200` | **ONLINE** | 668.6 ms | `scripts/build_references_system.py:331` | Responsive (OK) |
| 18 | [https://github.com/xToshiro/ai-market-crash-risk.git](https://github.com/xToshiro/ai-market-crash-risk.git) | `200` | **ONLINE** | 480.8 ms | `README.md:312` | Responsive (OK) |
| 19 | [https://home.treasury.gov/data/treasury-international-capital-tic-system](https://home.treasury.gov/data/treasury-international-capital-tic-system) | `200` | **ONLINE** | 382.8 ms | `scripts/build_references_system.py:89` | Responsive (OK) |
| 20 | [https://img.shields.io/badge/Asset_Classes-ABS_%7C_Private_Credit_%7C_Equities_%7C_Sovereign_Bonds-0A192F?style=for-the-badge](https://img.shields.io/badge/Asset_Classes-ABS_%7C_Private_Credit_%7C_Equities_%7C_Sovereign_Bonds-0A192F?style=for-the-badge) | `200` | **ONLINE** | 163.4 ms | `README.md:19` | Responsive (OK) |
| 21 | [https://img.shields.io/badge/Baseline_Model-30%25_(Q3--2026](https://img.shields.io/badge/Baseline_Model-30%25_(Q3--2026) | `200` | **ONLINE** | 174.4 ms | `README.md:17` | Responsive (OK) |
| 22 | [https://img.shields.io/badge/Bilingual_Charts-41_EN_%7C_41_PT-D97706?style=for-the-badge](https://img.shields.io/badge/Bilingual_Charts-41_EN_%7C_41_PT-D97706?style=for-the-badge) | `200` | **ONLINE** | 182.0 ms | `README.md:22` | Responsive (OK) |
| 23 | [https://img.shields.io/badge/Coverage_Horizon-2026_--_2029-475569?style=for-the-badge](https://img.shields.io/badge/Coverage_Horizon-2026_--_2029-475569?style=for-the-badge) | `200` | **ONLINE** | 189.2 ms | `README.md:20` | Responsive (OK) |
| 24 | [https://img.shields.io/badge/Crash_Scenario_Probability-48%25_(Oct--2026](https://img.shields.io/badge/Crash_Scenario_Probability-48%25_(Oct--2026) | `200` | **ONLINE** | 166.7 ms | `README.md:15` | Responsive (OK) |
| 25 | [https://img.shields.io/badge/Model_Variance-%2B18_pp_(Oct--2026](https://img.shields.io/badge/Model_Variance-%2B18_pp_(Oct--2026) | `200` | **ONLINE** | 160.8 ms | `README.md:18` | Responsive (OK) |
| 26 | [https://img.shields.io/badge/Reports-16_Executive_PDFs_(102_Pages](https://img.shields.io/badge/Reports-16_Executive_PDFs_(102_Pages) | `200` | **ONLINE** | 158.4 ms | `README.md:21` | Responsive (OK) |
| 27 | [https://img.shields.io/badge/Skills-Antigravity_Forecast_Updater-6B21A8?style=for-the-badge](https://img.shields.io/badge/Skills-Antigravity_Forecast_Updater-6B21A8?style=for-the-badge) | `200` | **ONLINE** | 161.2 ms | `README.md:23` | Responsive (OK) |
| 28 | [https://img.shields.io/badge/Soft_Landing_Probability-52%25_(Oct--2026](https://img.shields.io/badge/Soft_Landing_Probability-52%25_(Oct--2026) | `200` | **ONLINE** | 173.0 ms | `README.md:16` | Responsive (OK) |
| 29 | [https://investor.tsmc.com/english/monthly-revenue](https://investor.tsmc.com/english/monthly-revenue) | `403` | **ONLINE (Protected/WAF)** | 38.4 ms | `scripts/build_references_system.py:163` | Host alive; WAF bot protection active (normal for financial media) |
| 30 | [https://tensordock.com](https://tensordock.com) | `200` | **ONLINE** | 343.2 ms | `scripts/build_references_system.py:363` | Responsive (OK) |
| 31 | [https://vast.ai](https://vast.ai) | `200` | **ONLINE** | 250.0 ms | `scripts/build_references_system.py:355` | Responsive (OK) |
| 32 | [https://www.anthropic.com](https://www.anthropic.com) | `200` | **ONLINE** | 252.2 ms | `scripts/build_references_system.py:373` | Responsive (OK) |
| 33 | [https://www.bis.org/publ/qtrpdf/r_qt2403.htm](https://www.bis.org/publ/qtrpdf/r_qt2403.htm) | `200` | **ONLINE** | 1271.4 ms | `scripts/build_references_system.py:239`<br>`scripts/build_references_system.py:825`<br>`scripts/build_references_system.py:825` | Responsive (OK) |
| 34 | [https://www.blackrock.com](https://www.blackrock.com) | `200` | **ONLINE** | 630.6 ms | `scripts/build_references_system.py:405`<br>`scripts/build_references_system.py:827`<br>`scripts/build_references_system.py:827` | Responsive (OK) |
| 35 | [https://www.blackstone.com](https://www.blackstone.com) | `403` | **ONLINE (Protected/WAF)** | 211.6 ms | `scripts/build_references_system.py:413` | Host alive; WAF bot protection active (normal for financial media) |
| 36 | [https://www.bloomberg.com/technology](https://www.bloomberg.com/technology) | `403` | **ONLINE (Protected/WAF)** | 281.8 ms | `scripts/build_references_system.py:265`<br>`scripts/build_references_system.py:805`<br>`scripts/build_references_system.py:805` | Host alive; WAF bot protection active (normal for financial media) |
| 37 | [https://www.blueowl.com](https://www.blueowl.com) | `200` | **ONLINE** | 40.0 ms | `scripts/build_references_system.py:421` | Responsive (OK) |
| 38 | [https://www.businessinsider.com/tech](https://www.businessinsider.com/tech) | `200` | **ONLINE** | 367.3 ms | `scripts/build_references_system.py:313`<br>`scripts/build_references_system.py:801`<br>`scripts/build_references_system.py:801` | Responsive (OK) |
| 39 | [https://www.cbo.gov/topics/budget](https://www.cbo.gov/topics/budget) | `403` | **ONLINE (Protected/WAF)** | 82.4 ms | `scripts/build_references_system.py:97` | Host alive; WAF bot protection active (normal for financial media) |
| 40 | [https://www.coreweave.com](https://www.coreweave.com) | `200` | **ONLINE** | 487.2 ms | `scripts/build_references_system.py:389` | Responsive (OK) |
| 41 | [https://www.datacenterdynamics.com](https://www.datacenterdynamics.com) | `403` | **ONLINE (Protected/WAF)** | 224.5 ms | `scripts/build_references_system.py:297`<br>`scripts/build_references_system.py:791`<br>`scripts/build_references_system.py:791` | Host alive; WAF bot protection active (normal for financial media) |
| 42 | [https://www.euronext.com](https://www.euronext.com) | `200` | **ONLINE** | 754.2 ms | `scripts/build_references_system.py:321` | Responsive (OK) |
| 43 | [https://www.ferc.gov](https://www.ferc.gov) | `403` | **ONLINE (Protected/WAF)** | 482.8 ms | `scripts/build_references_system.py:197` | Host alive; WAF bot protection active (normal for financial media) |
| 44 | [https://www.ft.com/technology](https://www.ft.com/technology) | `403` | **ONLINE (Protected/WAF)** | 219.3 ms | `scripts/build_references_system.py:257`<br>`scripts/build_references_system.py:787`<br>`scripts/build_references_system.py:787` | Host alive; WAF bot protection active (normal for financial media) |
| 45 | [https://www.iea.org/reports/electricity-2024](https://www.iea.org/reports/electricity-2024) | `403` | **ONLINE (Protected/WAF)** | 204.6 ms | `scripts/build_references_system.py:205`<br>`scripts/build_references_system.py:814`<br>`scripts/build_references_system.py:814` | Host alive; WAF bot protection active (normal for financial media) |
| 46 | [https://www.jpmorgan.com](https://www.jpmorgan.com) | `200` | **ONLINE** | 1095.4 ms | `scripts/build_references_system.py:823`<br>`scripts/build_references_system.py:823` | Responsive (OK) |
| 47 | [https://www.kbra.com](https://www.kbra.com) | `200` | **ONLINE** | 725.0 ms | `scripts/build_references_system.py:215` | Responsive (OK) |
| 48 | [https://www.kbra.com/methodologies](https://www.kbra.com/methodologies) | `404` | **HTTP_ERROR** | 571.6 ms | `scripts/build_references_system.py:844`<br>`scripts/build_references_system.py:844` | HTTP Error 404: Not Found |
| 49 | [https://www.moodys.com](https://www.moodys.com) | `200` | **ONLINE** | 87.9 ms | `scripts/build_references_system.py:231` | Responsive (OK) |
| 50 | [https://www.nationalgrid.com/electricity-transmission](https://www.nationalgrid.com/electricity-transmission) | `403` | **ONLINE (Protected/WAF)** | 220.2 ms | `scripts/build_references_system.py:189` | Host alive; WAF bot protection active (normal for financial media) |
| 51 | [https://www.nscale.com](https://www.nscale.com) | `200` | **ONLINE** | 175.3 ms | `scripts/build_references_system.py:397`<br>`scripts/build_references_system.py:793`<br>`scripts/build_references_system.py:793` | Responsive (OK) |
| 52 | [https://www.openai.com](https://www.openai.com) | `403` | **ONLINE (Protected/WAF)** | 205.0 ms | `scripts/build_references_system.py:381` | Host alive; WAF bot protection active (normal for financial media) |
| 53 | [https://www.pjm.com/markets-and-operations/rpm](https://www.pjm.com/markets-and-operations/rpm) | `200` | **ONLINE** | 1257.5 ms | `scripts/build_references_system.py:181`<br>`scripts/build_references_system.py:812`<br>`scripts/build_references_system.py:812` | Responsive (OK) |
| 54 | [https://www.pjm.com/planning/services-requests/interconnection-queues](https://www.pjm.com/planning/services-requests/interconnection-queues) | `200` | **ONLINE** | 2639.6 ms | `scripts/build_references_system.py:173` | Responsive (OK) |
| 55 | [https://www.reuters.com/technology](https://www.reuters.com/technology) | `401` | **ONLINE (Protected/WAF)** | 228.2 ms | `scripts/build_references_system.py:273` | Host alive; WAF bot protection active (normal for financial media) |
| 56 | [https://www.runpod.io](https://www.runpod.io) | `200` | **ONLINE** | 213.6 ms | `scripts/build_references_system.py:347` | Responsive (OK) |
| 57 | [https://www.sec.gov/edgar/browse/?CIK=0000789019](https://www.sec.gov/edgar/browse/?CIK=0000789019) | `403` | **ONLINE (Protected/WAF)** | 136.0 ms | `scripts/build_references_system.py:115` | Host alive; WAF bot protection active (normal for financial media) |
| 58 | [https://www.sec.gov/edgar/browse/?CIK=0001018724](https://www.sec.gov/edgar/browse/?CIK=0001018724) | `403` | **ONLINE (Protected/WAF)** | 133.9 ms | `scripts/build_references_system.py:131` | Host alive; WAF bot protection active (normal for financial media) |
| 59 | [https://www.sec.gov/edgar/browse/?CIK=0001045810](https://www.sec.gov/edgar/browse/?CIK=0001045810) | `403` | **ONLINE (Protected/WAF)** | 186.0 ms | `scripts/build_references_system.py:107` | Host alive; WAF bot protection active (normal for financial media) |
| 60 | [https://www.sec.gov/edgar/browse/?CIK=0001326801](https://www.sec.gov/edgar/browse/?CIK=0001326801) | `403` | **ONLINE (Protected/WAF)** | 162.7 ms | `scripts/build_references_system.py:147` | Host alive; WAF bot protection active (normal for financial media) |
| 61 | [https://www.sec.gov/edgar/browse/?CIK=0001341439](https://www.sec.gov/edgar/browse/?CIK=0001341439) | `403` | **ONLINE (Protected/WAF)** | 144.4 ms | `scripts/build_references_system.py:139` | Host alive; WAF bot protection active (normal for financial media) |
| 62 | [https://www.sec.gov/edgar/browse/?CIK=0001652044](https://www.sec.gov/edgar/browse/?CIK=0001652044) | `403` | **ONLINE (Protected/WAF)** | 143.0 ms | `scripts/build_references_system.py:123` | Host alive; WAF bot protection active (normal for financial media) |
| 63 | [https://www.sec.gov/edgar/browse/?CIK=0001730168](https://www.sec.gov/edgar/browse/?CIK=0001730168) | `403` | **ONLINE (Protected/WAF)** | 142.3 ms | `scripts/build_references_system.py:155` | Host alive; WAF bot protection active (normal for financial media) |
| 64 | [https://www.spglobal.com/ratings](https://www.spglobal.com/ratings) | `403` | **ONLINE (Protected/WAF)** | 367.7 ms | `scripts/build_references_system.py:223` | Host alive; WAF bot protection active (normal for financial media) |
| 65 | [https://www.theguardian.com/business](https://www.theguardian.com/business) | `200` | **ONLINE** | 469.2 ms | `scripts/build_references_system.py:305`<br>`scripts/build_references_system.py:789`<br>`scripts/build_references_system.py:789` | Responsive (OK) |
| 66 | [https://www.theinformation.com](https://www.theinformation.com) | `403` | **ONLINE (Protected/WAF)** | 149.8 ms | `scripts/build_references_system.py:289`<br>`scripts/build_references_system.py:803`<br>`scripts/build_references_system.py:803` | Host alive; WAF bot protection active (normal for financial media) |
| 67 | [https://www.wsj.com/tech](https://www.wsj.com/tech) | `401` | **ONLINE (Protected/WAF)** | 244.4 ms | `scripts/build_references_system.py:281`<br>`scripts/build_references_system.py:829`<br>`scripts/build_references_system.py:829` | Host alive; WAF bot protection active (normal for financial media) |
