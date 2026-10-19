# URL Connectivity & Live Verification Audit Report

**Automated Link Health Check & Telemetry Audit**  
*Execution Timestamp: 2026-10-19 14:09:38*

This report contains the empirical verification results of every link cited across the repository. Each endpoint was queried with an HTTP client simulating standard browser user-agents.

---

## Summary Statistics

* **Total Links Audited**: 72
* **Status Distribution**:
  * **ONLINE / 200 OK**: 36
  * **ONLINE / WAF Protected (Bot Detection)**: 21 *(Host is fully operational; returned HTTP 403 due to Cloudflare/Imperva scraper shields)*
  * **ONLINE / Redirect (301/302)**: 0
  * **Unreachable / Network Error**: 13

---

## Detailed Telemetry & Verification Matrix

| # | Target URL | HTTP Code | Status | Latency | Primary Association / Files Cited | Notes / Diagnosis |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| 1 | [https://api.fiscaldata.treasury.gov](https://api.fiscaldata.treasury.gov) | `404` | **HTTP_ERROR** | 1035.7 ms | `scripts/build_references_system.py:759` | HTTP Error 404: Not Found |
| 2 | [https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny) | `200` | **ONLINE** | 991.9 ms | `scripts/build_references_system.py:41` | Responsive (OK) |
| 3 | [https://finance.yahoo.com](https://finance.yahoo.com) | `200` | **ONLINE** | 1296.6 ms | `scripts/build_references_system.py:339` | Responsive (OK) |
| 4 | [https://finsight.com](https://finsight.com) | `200` | **ONLINE** | 972.0 ms | `scripts/build_references_system.py:247` | Responsive (OK) |
| 5 | [https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government) | `200` | **ONLINE** | 1012.7 ms | `scripts/build_references_system.py:49` | Responsive (OK) |
| 6 | [https://fred.stlouisfed.org](https://fred.stlouisfed.org) | `N/A` | **ERROR** | 4158.8 ms | `scripts/build_references_system.py:742` | The read operation timed out |
| 7 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2) | `N/A` | **ERROR** | 4099.0 ms | `scripts/build_references_system.py:751` | The read operation timed out |
| 8 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10) | `N/A` | **ERROR** | 4100.1 ms | `scripts/build_references_system.py:748` | The read operation timed out |
| 9 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2) | `N/A` | **ERROR** | 4110.4 ms | `scripts/build_references_system.py:749` | The read operation timed out |
| 10 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS](https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS) | `N/A` | **ERROR** | 4195.1 ms | `scripts/build_references_system.py:752` | The read operation timed out |
| 11 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y](https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y) | `N/A` | **ERROR** | 4096.9 ms | `scripts/build_references_system.py:750` | The read operation timed out |
| 12 | [https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL](https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL) | `N/A` | **ERROR** | 4103.9 ms | `scripts/build_references_system.py:753` | The read operation timed out |
| 13 | [https://fred.stlouisfed.org/series/BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) | `N/A` | **ERROR** | 4110.0 ms | `scripts/build_references_system.py:73` | The read operation timed out |
| 14 | [https://fred.stlouisfed.org/series/DGS10](https://fred.stlouisfed.org/series/DGS10) | `N/A` | **ERROR** | 4149.1 ms | `scripts/build_references_system.py:57` | The read operation timed out |
| 15 | [https://fred.stlouisfed.org/series/DGS2](https://fred.stlouisfed.org/series/DGS2) | `N/A` | **ERROR** | 4100.3 ms | `scripts/build_references_system.py:65` | The read operation timed out |
| 16 | [https://fred.stlouisfed.org/series/FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) | `N/A` | **ERROR** | 4099.7 ms | `scripts/build_references_system.py:81` | The read operation timed out |
| 17 | [https://github.com/xToshiro/ai-market-crash-risk](https://github.com/xToshiro/ai-market-crash-risk) | `200` | **ONLINE** | 995.7 ms | `scripts/build_references_system.py:331` | Responsive (OK) |
| 18 | [https://github.com/xToshiro/ai-market-crash-risk.git](https://github.com/xToshiro/ai-market-crash-risk.git) | `200` | **ONLINE** | 488.9 ms | `README.md:314` | Responsive (OK) |
| 19 | [https://home.treasury.gov/data/treasury-international-capital-tic-system](https://home.treasury.gov/data/treasury-international-capital-tic-system) | `200` | **ONLINE** | 526.5 ms | `scripts/build_references_system.py:89` | Responsive (OK) |
| 20 | [https://img.shields.io/badge/Asset_Classes-ABS_%7C_Private_Credit_%7C_Equities_%7C_Sovereign_Bonds-0A192F?style=for-the-badge](https://img.shields.io/badge/Asset_Classes-ABS_%7C_Private_Credit_%7C_Equities_%7C_Sovereign_Bonds-0A192F?style=for-the-badge) | `200` | **ONLINE** | 174.8 ms | `README.md:21` | Responsive (OK) |
| 21 | [https://img.shields.io/badge/Baseline_Model-30%25_(Q3--2026](https://img.shields.io/badge/Baseline_Model-30%25_(Q3--2026) | `200` | **ONLINE** | 165.1 ms | `README.md:18` | Responsive (OK) |
| 22 | [https://img.shields.io/badge/Bilingual_Charts-41_EN_%7C_41_PT-D97706?style=for-the-badge](https://img.shields.io/badge/Bilingual_Charts-41_EN_%7C_41_PT-D97706?style=for-the-badge) | `200` | **ONLINE** | 212.6 ms | `README.md:24` | Responsive (OK) |
| 23 | [https://img.shields.io/badge/Coverage_Horizon-2026_--_2029-475569?style=for-the-badge](https://img.shields.io/badge/Coverage_Horizon-2026_--_2029-475569?style=for-the-badge) | `200` | **ONLINE** | 168.4 ms | `README.md:22` | Responsive (OK) |
| 24 | [https://img.shields.io/badge/Crash_Scenario_Probability-48%25_(Oct--2026](https://img.shields.io/badge/Crash_Scenario_Probability-48%25_(Oct--2026) | `200` | **ONLINE** | 216.2 ms | `README.md:16` | Responsive (OK) |
| 25 | [https://img.shields.io/badge/Model_Variance-%2B18_pp_(Oct--2026](https://img.shields.io/badge/Model_Variance-%2B18_pp_(Oct--2026) | `200` | **ONLINE** | 167.0 ms | `README.md:19` | Responsive (OK) |
| 26 | [https://img.shields.io/badge/References-Audited_&_Online-0284C7?style=for-the-badge](https://img.shields.io/badge/References-Audited_&_Online-0284C7?style=for-the-badge) | `200` | **ONLINE** | 353.2 ms | `README.md:20` | Responsive (OK) |
| 27 | [https://img.shields.io/badge/Reports-16_Executive_PDFs_(102_Pages](https://img.shields.io/badge/Reports-16_Executive_PDFs_(102_Pages) | `200` | **ONLINE** | 234.6 ms | `README.md:23` | Responsive (OK) |
| 28 | [https://img.shields.io/badge/Skills-Antigravity_Forecast_Updater-6B21A8?style=for-the-badge](https://img.shields.io/badge/Skills-Antigravity_Forecast_Updater-6B21A8?style=for-the-badge) | `200` | **ONLINE** | 229.7 ms | `README.md:25` | Responsive (OK) |
| 29 | [https://img.shields.io/badge/Soft_Landing_Probability-52%25_(Oct--2026](https://img.shields.io/badge/Soft_Landing_Probability-52%25_(Oct--2026) | `200` | **ONLINE** | 165.3 ms | `README.md:17` | Responsive (OK) |
| 30 | [https://investor.tsmc.com/english/monthly-revenue](https://investor.tsmc.com/english/monthly-revenue) | `403` | **ONLINE (Protected/WAF)** | 217.9 ms | `scripts/build_references_system.py:163` | Host alive; WAF bot protection active (normal for financial media) |
| 31 | [https://tensordock.com](https://tensordock.com) | `200` | **ONLINE** | 574.5 ms | `scripts/build_references_system.py:363` | Responsive (OK) |
| 32 | [https://ticdata.treasury.gov/Publish/mfh.txt](https://ticdata.treasury.gov/Publish/mfh.txt) | `200` | **ONLINE** | 941.8 ms | `scripts/build_references_system.py:437` | Responsive (OK) |
| 33 | [https://vast.ai](https://vast.ai) | `200` | **ONLINE** | 272.3 ms | `scripts/build_references_system.py:355` | Responsive (OK) |
| 34 | [https://www.anthropic.com](https://www.anthropic.com) | `200` | **ONLINE** | 332.5 ms | `scripts/build_references_system.py:373` | Responsive (OK) |
| 35 | [https://www.bis.org/publ/qtrpdf/r_qt2403.htm](https://www.bis.org/publ/qtrpdf/r_qt2403.htm) | `200` | **ONLINE** | 1127.6 ms | `scripts/build_references_system.py:239`<br>`scripts/build_references_system.py:857`<br>`scripts/build_references_system.py:857` | Responsive (OK) |
| 36 | [https://www.blackrock.com](https://www.blackrock.com) | `200` | **ONLINE** | 590.7 ms | `scripts/build_references_system.py:405`<br>`scripts/build_references_system.py:859`<br>`scripts/build_references_system.py:859` | Responsive (OK) |
| 37 | [https://www.blackstone.com](https://www.blackstone.com) | `403` | **ONLINE (Protected/WAF)** | 332.5 ms | `scripts/build_references_system.py:413` | Host alive; WAF bot protection active (normal for financial media) |
| 38 | [https://www.bloomberg.com/technology](https://www.bloomberg.com/technology) | `403` | **ONLINE (Protected/WAF)** | 270.9 ms | `scripts/build_references_system.py:265`<br>`scripts/build_references_system.py:837`<br>`scripts/build_references_system.py:837` | Host alive; WAF bot protection active (normal for financial media) |
| 39 | [https://www.blueowl.com](https://www.blueowl.com) | `200` | **ONLINE** | 669.7 ms | `scripts/build_references_system.py:421` | Responsive (OK) |
| 40 | [https://www.boj.or.jp](https://www.boj.or.jp) | `200` | **ONLINE** | 612.5 ms | `scripts/build_references_system.py:429` | Responsive (OK) |
| 41 | [https://www.businessinsider.com/tech](https://www.businessinsider.com/tech) | `200` | **ONLINE** | 100.0 ms | `scripts/build_references_system.py:313`<br>`scripts/build_references_system.py:833`<br>`scripts/build_references_system.py:833` | Responsive (OK) |
| 42 | [https://www.cbo.gov/topics/budget](https://www.cbo.gov/topics/budget) | `403` | **ONLINE (Protected/WAF)** | 171.5 ms | `scripts/build_references_system.py:97` | Host alive; WAF bot protection active (normal for financial media) |
| 43 | [https://www.coreweave.com](https://www.coreweave.com) | `200` | **ONLINE** | 526.1 ms | `scripts/build_references_system.py:389` | Responsive (OK) |
| 44 | [https://www.datacenterdynamics.com](https://www.datacenterdynamics.com) | `403` | **ONLINE (Protected/WAF)** | 225.6 ms | `scripts/build_references_system.py:297`<br>`scripts/build_references_system.py:823`<br>`scripts/build_references_system.py:823` | Host alive; WAF bot protection active (normal for financial media) |
| 45 | [https://www.euronext.com](https://www.euronext.com) | `200` | **ONLINE** | 791.0 ms | `scripts/build_references_system.py:321` | Responsive (OK) |
| 46 | [https://www.ferc.gov](https://www.ferc.gov) | `403` | **ONLINE (Protected/WAF)** | 540.8 ms | `scripts/build_references_system.py:197` | Host alive; WAF bot protection active (normal for financial media) |
| 47 | [https://www.ft.com/technology](https://www.ft.com/technology) | `403` | **ONLINE (Protected/WAF)** | 208.2 ms | `scripts/build_references_system.py:257`<br>`scripts/build_references_system.py:819`<br>`scripts/build_references_system.py:819` | Host alive; WAF bot protection active (normal for financial media) |
| 48 | [https://www.iea.org/reports/electricity-2024](https://www.iea.org/reports/electricity-2024) | `403` | **ONLINE (Protected/WAF)** | 219.0 ms | `scripts/build_references_system.py:205`<br>`scripts/build_references_system.py:846`<br>`scripts/build_references_system.py:846` | Host alive; WAF bot protection active (normal for financial media) |
| 49 | [https://www.jpmorgan.com](https://www.jpmorgan.com) | `200` | **ONLINE** | 1006.4 ms | `scripts/build_references_system.py:855`<br>`scripts/build_references_system.py:855` | Responsive (OK) |
| 50 | [https://www.jtuc-rengo.org](https://www.jtuc-rengo.org) | `200` | **ONLINE** | 1193.9 ms | `scripts/build_references_system.py:453` | Responsive (OK) |
| 51 | [https://www.kbra.com](https://www.kbra.com) | `200` | **ONLINE** | 714.4 ms | `scripts/build_references_system.py:215` | Responsive (OK) |
| 52 | [https://www.kbra.com/methodologies](https://www.kbra.com/methodologies) | `404` | **HTTP_ERROR** | 442.3 ms | `scripts/build_references_system.py:876`<br>`scripts/build_references_system.py:876` | HTTP Error 404: Not Found |
| 53 | [https://www.mof.go.jp](https://www.mof.go.jp) | `200` | **ONLINE** | 1919.6 ms | `scripts/build_references_system.py:445` | Responsive (OK) |
| 54 | [https://www.moodys.com](https://www.moodys.com) | `200` | **ONLINE** | 164.3 ms | `scripts/build_references_system.py:231` | Responsive (OK) |
| 55 | [https://www.nationalgrid.com/electricity-transmission](https://www.nationalgrid.com/electricity-transmission) | `403` | **ONLINE (Protected/WAF)** | 245.5 ms | `scripts/build_references_system.py:189` | Host alive; WAF bot protection active (normal for financial media) |
| 56 | [https://www.nscale.com](https://www.nscale.com) | `200` | **ONLINE** | 444.1 ms | `scripts/build_references_system.py:397`<br>`scripts/build_references_system.py:825`<br>`scripts/build_references_system.py:825` | Responsive (OK) |
| 57 | [https://www.openai.com](https://www.openai.com) | `403` | **ONLINE (Protected/WAF)** | 148.8 ms | `scripts/build_references_system.py:381` | Host alive; WAF bot protection active (normal for financial media) |
| 58 | [https://www.pjm.com/markets-and-operations/rpm](https://www.pjm.com/markets-and-operations/rpm) | `N/A` | **UNREACHABLE** | 4001.9 ms | `scripts/build_references_system.py:181`<br>`scripts/build_references_system.py:844`<br>`scripts/build_references_system.py:844` | timed out |
| 59 | [https://www.pjm.com/planning/services-requests/interconnection-queues](https://www.pjm.com/planning/services-requests/interconnection-queues) | `N/A` | **UNREACHABLE** | 7880.7 ms | `scripts/build_references_system.py:173` | timed out |
| 60 | [https://www.reuters.com/technology](https://www.reuters.com/technology) | `401` | **ONLINE (Protected/WAF)** | 252.2 ms | `scripts/build_references_system.py:273` | Host alive; WAF bot protection active (normal for financial media) |
| 61 | [https://www.runpod.io](https://www.runpod.io) | `200` | **ONLINE** | 350.6 ms | `scripts/build_references_system.py:347` | Responsive (OK) |
| 62 | [https://www.sec.gov/edgar/browse/?CIK=0000789019](https://www.sec.gov/edgar/browse/?CIK=0000789019) | `403` | **ONLINE (Protected/WAF)** | 179.8 ms | `scripts/build_references_system.py:115` | Host alive; WAF bot protection active (normal for financial media) |
| 63 | [https://www.sec.gov/edgar/browse/?CIK=0001018724](https://www.sec.gov/edgar/browse/?CIK=0001018724) | `403` | **ONLINE (Protected/WAF)** | 185.9 ms | `scripts/build_references_system.py:131` | Host alive; WAF bot protection active (normal for financial media) |
| 64 | [https://www.sec.gov/edgar/browse/?CIK=0001045810](https://www.sec.gov/edgar/browse/?CIK=0001045810) | `403` | **ONLINE (Protected/WAF)** | 433.4 ms | `scripts/build_references_system.py:107` | Host alive; WAF bot protection active (normal for financial media) |
| 65 | [https://www.sec.gov/edgar/browse/?CIK=0001326801](https://www.sec.gov/edgar/browse/?CIK=0001326801) | `403` | **ONLINE (Protected/WAF)** | 303.5 ms | `scripts/build_references_system.py:147` | Host alive; WAF bot protection active (normal for financial media) |
| 66 | [https://www.sec.gov/edgar/browse/?CIK=0001341439](https://www.sec.gov/edgar/browse/?CIK=0001341439) | `403` | **ONLINE (Protected/WAF)** | 311.3 ms | `scripts/build_references_system.py:139` | Host alive; WAF bot protection active (normal for financial media) |
| 67 | [https://www.sec.gov/edgar/browse/?CIK=0001652044](https://www.sec.gov/edgar/browse/?CIK=0001652044) | `403` | **ONLINE (Protected/WAF)** | 197.5 ms | `scripts/build_references_system.py:123` | Host alive; WAF bot protection active (normal for financial media) |
| 68 | [https://www.sec.gov/edgar/browse/?CIK=0001730168](https://www.sec.gov/edgar/browse/?CIK=0001730168) | `403` | **ONLINE (Protected/WAF)** | 174.2 ms | `scripts/build_references_system.py:155` | Host alive; WAF bot protection active (normal for financial media) |
| 69 | [https://www.spglobal.com/ratings](https://www.spglobal.com/ratings) | `403` | **ONLINE (Protected/WAF)** | 253.7 ms | `scripts/build_references_system.py:223` | Host alive; WAF bot protection active (normal for financial media) |
| 70 | [https://www.theguardian.com/business](https://www.theguardian.com/business) | `200` | **ONLINE** | 1182.9 ms | `scripts/build_references_system.py:305`<br>`scripts/build_references_system.py:821`<br>`scripts/build_references_system.py:821` | Responsive (OK) |
| 71 | [https://www.theinformation.com](https://www.theinformation.com) | `403` | **ONLINE (Protected/WAF)** | 217.7 ms | `scripts/build_references_system.py:289`<br>`scripts/build_references_system.py:835`<br>`scripts/build_references_system.py:835` | Host alive; WAF bot protection active (normal for financial media) |
| 72 | [https://www.wsj.com/tech](https://www.wsj.com/tech) | `401` | **ONLINE (Protected/WAF)** | 275.6 ms | `scripts/build_references_system.py:281`<br>`scripts/build_references_system.py:861`<br>`scripts/build_references_system.py:861` | Host alive; WAF bot protection active (normal for financial media) |
