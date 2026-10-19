# Master Catalog of Primary Sources, Filings & Market Intelligence

**AI Infrastructure & Credit Bubble: Systemic Risk Assessment**  
*Comprehensive Documentation of All Underlying Research Material*

---

## Sovereign Debt & Macroeconomic Feeds

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **US Treasury Fiscal Data (Debt to the Penny API)** | [https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny)<br>`HTTP 200` | Official daily feed of total public debt outstanding and debt held by the public. | `Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf`, `Dossie_Macro_Geopolitica_Quebra_Mercado_2026_2028.md`, `fetch_market_pipeline.py` |
| **US Treasury - Monthly Treasury Statement (MTS)** | [https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-and-outlays-of-the-u-s-government)<br>`HTTP 200` | Monthly report detailing federal revenues, outlays, and net interest expenses ($1.16T+ p.a.). | `Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf`, `fetch_market_pipeline.py` |
| **FRED - 10-Year Treasury Constant Maturity Rate (DGS10)** | [https://fred.stlouisfed.org/series/DGS10](https://fred.stlouisfed.org/series/DGS10)<br>`ONLINE` | Federal Reserve Bank of St. Louis benchmark 10-year sovereign bond yield tracking higher-for-longer (5.10%). | `Relatorio_Mercado_Financeiro_Americano.pdf`, `fetch_market_pipeline.py`, `macro_financial_condition.csv` |
| **FRED - 2-Year Treasury Constant Maturity Rate (DGS2)** | [https://fred.stlouisfed.org/series/DGS2](https://fred.stlouisfed.org/series/DGS2)<br>`ONLINE` | Short-term policy-sensitive Treasury yield for calculating the 10Y-2Y yield curve spread. | `Relatorio_Mercado_Financeiro_Americano.pdf`, `fetch_market_pipeline.py`, `macro_financial_condition.csv` |
| **FRED - ICE BofA US High Yield Index Option-Adjusted Spread (BAMLH0A0HYM2)** | [https://fred.stlouisfed.org/series/BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)<br>`ONLINE` | Option-adjusted credit spread for US high-yield corporate bonds. | `Relatorio_Mercado_Financeiro_Americano.pdf`, `fetch_market_pipeline.py` |
| **FRED - Federal Funds Effective Rate (FEDFUNDS)** | [https://fred.stlouisfed.org/series/FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS)<br>`ONLINE` | Benchmark US monetary policy rate (3.75%-4.00% corridor). | `Relatorio_Mercado_Financeiro_Americano.pdf`, `fetch_market_pipeline.py` |
| **Treasury International Capital (TIC) System** | [https://home.treasury.gov/data/treasury-international-capital-tic-system](https://home.treasury.gov/data/treasury-international-capital-tic-system)<br>`HTTP 200` | Monthly foreign holdings of US Treasury securities (Japan, China, Gulf sovereign wealth funds). | `Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf`, `Dossie_Macro_Geopolitica_Quebra_Mercado_2026_2028.md` |
| **Congressional Budget Office (CBO) - The Budget and Economic Outlook** | [https://www.cbo.gov/topics/budget](https://www.cbo.gov/topics/budget)<br>`HTTP 403` | Non-partisan 10-year fiscal projections, statutory deficit ratios, and debt-to-GDP trajectories. | `Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf` |

---

## SEC Filings & Corporate Financial Reports

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **SEC EDGAR - NVIDIA Corporation (CIK 0001045810)** | [https://www.sec.gov/edgar/browse/?CIK=0001045810](https://www.sec.gov/edgar/browse/?CIK=0001045810)<br>`HTTP 403` | Form 10-K and 10-Q filings: Customer Concentration (Note 14), Purchase Obligations, Hardware Gross Margins (75%), Vendor Financing. | `Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf`, `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf`, `Dossie_Alavancagem_Vendor_Financing_IA.md` |
| **SEC EDGAR - Microsoft Corporation (CIK 0000789019)** | [https://www.sec.gov/edgar/browse/?CIK=0000789019](https://www.sec.gov/edgar/browse/?CIK=0000789019)<br>`HTTP 403` | Form 10-K / 10-Q: Azure CapEx run-rate, lease commitments, PPA disclosures, Nscale contract notes. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **SEC EDGAR - Alphabet Inc. (CIK 0001652044)** | [https://www.sec.gov/edgar/browse/?CIK=0001652044](https://www.sec.gov/edgar/browse/?CIK=0001652044)<br>`HTTP 403` | Form 10-K / 10-Q: Google Cloud infrastructure CapEx, TPU internal silicon investments, cash reserves ($88B+). | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **SEC EDGAR - Amazon.com, Inc. (CIK 0001018724)** | [https://www.sec.gov/edgar/browse/?CIK=0001018724](https://www.sec.gov/edgar/browse/?CIK=0001018724)<br>`HTTP 403` | Form 10-K / 10-Q: AWS infrastructure commitments, Talen Energy nuclear campus PPA, Anthropic investment agreements. | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf`, `Dossie_Alavancagem_Vendor_Financing_IA.md` |
| **SEC EDGAR - Oracle Corporation (CIK 0001341439)** | [https://www.sec.gov/edgar/browse/?CIK=0001341439](https://www.sec.gov/edgar/browse/?CIK=0001341439)<br>`HTTP 403` | Form 10-K / 10-Q: OCI data center buildout, debt leverage ratios, debt-to-equity vulnerability. | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **SEC EDGAR - Meta Platforms, Inc. (CIK 0001326801)** | [https://www.sec.gov/edgar/browse/?CIK=0001326801](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`HTTP 403` | Form 10-K / 10-Q: AI compute cluster deployment, Llama open-weight infrastructure CapEx. | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **SEC EDGAR - Broadcom Inc. (CIK 0001730168)** | [https://www.sec.gov/edgar/browse/?CIK=0001730168](https://www.sec.gov/edgar/browse/?CIK=0001730168)<br>`HTTP 403` | Form 10-K / 10-Q: Custom AI ASIC silicon accelerators, high-speed Tomahawk networking switches. | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **TSMC Investor Relations - Monthly Revenue Releases** | [https://investor.tsmc.com/english/monthly-revenue](https://investor.tsmc.com/english/monthly-revenue)<br>`HTTP 403` | Taiwan Semiconductor Manufacturing Co. monthly net revenue releases, CoWoS advanced packaging capacity reports. | `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf`, `Dossie_Macro_Geopolitica_Quebra_Mercado_2026_2028.md`, `fetch_market_pipeline.py` |

---

## Power Grid & Electrical Utilities

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **PJM Interconnection - Interconnection Queues & Transmission Planning** | [https://www.pjm.com/planning/services-requests/interconnection-queues](https://www.pjm.com/planning/services-requests/interconnection-queues)<br>`ONLINE` | Official queue database tracking 5 to 7 year interconnection delays across 13 US states and D.C. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Dossie_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.md` |
| **PJM Interconnection - Reliability Pricing Model (RPM) Capacity Market** | [https://www.pjm.com/markets-and-operations/rpm](https://www.pjm.com/markets-and-operations/rpm)<br>`ONLINE` | Base Residual Auction (BRA) clearing results showing capacity price surges from $28.92 to $269.92/MW-day. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `chart_grid_bottleneck_delays.png` |
| **National Grid UK - Electricity Transmission** | [https://www.nationalgrid.com/electricity-transmission](https://www.nationalgrid.com/electricity-transmission)<br>`HTTP 403` | UK transmission system operator documentation on connection queue deferrals to the 2030s (triggering the Essex cancellation). | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Federal Energy Regulatory Commission (FERC)** | [https://www.ferc.gov](https://www.ferc.gov)<br>`HTTP 403` | Federal regulatory agency governing interstate electric transmission and Order 2023 interconnection queue reforms. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf` |
| **International Energy Agency (IEA) - Electricity 2024 / 2026 Analysis** | [https://www.iea.org/reports/electricity-2024](https://www.iea.org/reports/electricity-2024)<br>`HTTP 403` | Comprehensive global forecasts on data center and AI power demand doubling to >1,000 TWh by 2026. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |

---

## Credit Rating Agencies & Structured ABS Methodologies

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **KBRA (Kroll Bond Rating Agency) - Structured Finance Methodologies** | [https://www.kbra.com](https://www.kbra.com)<br>`HTTP 200` | Global Data Center ABS Rating Methodology: DSCR underwriting limits, LTV stress tests, and amortization modeling. | `Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf`, `Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf`, `KBRA_Data_Center_ABS_Rating_Methodology_Dossier.md` |
| **S&P Global Ratings - Structured Finance & Data Centers** | [https://www.spglobal.com/ratings](https://www.spglobal.com/ratings)<br>`HTTP 403` | Credit criteria for esoteric digital infrastructure asset-backed securitizations and tenant concentration risk. | `Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf`, `Data_Center_ABS_Relatorio.md` |
| **Moody's Investors Service - Structured Finance** | [https://www.moodys.com](https://www.moodys.com)<br>`HTTP 200` | Rating criteria and default rate matrices for technology infrastructure and asset-backed notes. | `Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf` |
| **Bank for International Settlements (BIS) - Quarterly Review** | [https://www.bis.org/publ/qtrpdf/r_qt2403.htm](https://www.bis.org/publ/qtrpdf/r_qt2403.htm)<br>`HTTP 200` | Central bank analysis of private credit markets, non-bank financial intermediation, and digital infrastructure SPVs. | `Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Finsight - Securitized Products & ABS Deal Database** | [https://finsight.com](https://finsight.com)<br>`HTTP 200` | Market tracker for primary Data Center ABS issuances (Compass, Vantage, CyrusOne, Stack Infrastructure). | `Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf`, `Data_Center_ABS_Relatorio.md` |

---

## Investigative Journalism & News Outlets

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **Financial Times - Technology & Data Centers** | [https://www.ft.com/technology](https://www.ft.com/technology)<br>`HTTP 403` | Primary reporting on the Microsoft-Nscale Essex cancellation, AI CapEx expansion, and grid constraints. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Bloomberg Technology** | [https://www.bloomberg.com/technology](https://www.bloomberg.com/technology)<br>`HTTP 403` | Investigations into Anthropic pre-IPO secondary shares, CoreWeave debt facilities, and hyperscaler private credit. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Reuters - Technology & Energy Transition** | [https://www.reuters.com/technology](https://www.reuters.com/technology)<br>`HTTP 401` | Coverage of power transformer supply chain delays, nuclear power purchase agreements, and semiconductor export curbs. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf` |
| **The Wall Street Journal - Tech & Finance** | [https://www.wsj.com/tech](https://www.wsj.com/tech)<br>`HTTP 401` | Analysis of Big Tech off-balance-sheet debt, Blackstone $25B data center debt funds, and AI software revenue ROI. | `Relatorio_Mercado_Financeiro_Americano.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **The Information - AI & Frontier Labs** | [https://www.theinformation.com](https://www.theinformation.com)<br>`HTTP 403` | Direct financial reporting on Anthropic ARR ($16.8B Q3-2026), OpenAI compute burn rates, and secondary SPV restrictions. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Data Center Dynamics (DCD)** | [https://www.datacenterdynamics.com](https://www.datacenterdynamics.com)<br>`HTTP 403` | Global data center industry news: Nscale UK campus developments, GSU transformer shortages, PJM auction impacts. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **The Guardian - Business & Environment** | [https://www.theguardian.com/business](https://www.theguardian.com/business)<br>`HTTP 200` | Reporting on UK grid connection delays and community opposition to high-voltage lines in Essex. | `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Business Insider - Tech & Markets** | [https://www.businessinsider.com/tech](https://www.businessinsider.com/tech)<br>`HTTP 200` | Coverage of the Anthropic target valuation haircut from $2.0T to $1.5T ahead of planned IPO. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **Euronext Stock Exchange** | [https://www.euronext.com](https://www.euronext.com)<br>`HTTP 200` | European market data and institutional investor communications regarding European tech valuations. | `Fontes_Noticias_Recentes_Outubro_2026.md` |

---

## Market Data & Quantitative Pipeline Feeds

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **GitHub Repository - ai-market-crash-risk** | [https://github.com/xToshiro/ai-market-crash-risk](https://github.com/xToshiro/ai-market-crash-risk)<br>`HTTP 200` | Primary open-source institutional research repository hosting all models, data pipelines, charts, and reports. | `All Dossiers`, `All Reports`, `README.md` |
| **Yahoo Finance Market Data API (Equities & Spreads)** | [https://finance.yahoo.com](https://finance.yahoo.com)<br>`HTTP 200` | Historical price queries for NVDA, MSFT, GOOGL, AMZN, META, TSM, AVGO, ORCL, ^GSPC, ^IXIC, HYG, LQD, ^VIX. | `scripts/fetch_market_pipeline.py`, `Relatorio_Mercado_Financeiro_Americano.pdf`, `Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf` |
| **RunPod - Cloud GPU Pricing & Compute Exchange** | [https://www.runpod.io](https://www.runpod.io)<br>`HTTP 200` | Real-time spot pricing for 8x H100 SXM5 and B200 clusters to audit GPU secondary market rental yields. | `Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf`, `sources_and_apis.md` |
| **Vast.ai - Decentralized GPU Marketplace** | [https://vast.ai](https://vast.ai)<br>`HTTP 200` | Secondary GPU rental auction prices and utilization tracking. | `Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf`, `sources_and_apis.md` |
| **TensorDock - Cloud GPU Hosting** | [https://tensordock.com](https://tensordock.com)<br>`HTTP 200` | Infrastructure pricing benchmark for H100/A100 instances. | `sources_and_apis.md` |

---

## Corporate Entities, Neoclouds & Private Equity

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **Anthropic Official** | [https://www.anthropic.com](https://www.anthropic.com)<br>`HTTP 200` | Claude 3.5 Sonnet / Opus developer, ARR growth disclosures, safety covenants. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf` |
| **OpenAI Official** | [https://www.openai.com](https://www.openai.com)<br>`HTTP 403` | Frontier AI lab, compute infrastructure partnership with Microsoft Azure, equity rounds. | `Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf` |
| **CoreWeave Cloud Infrastructure** | [https://www.coreweave.com](https://www.coreweave.com)<br>`HTTP 200` | Specialized GPU cloud provider; pioneer of GPU-backed debt facilities ($10B+ with Blackstone/Magnetar). | `CoreWeave_GPU_Debt_and_Vendor_Financing_Analysis.md`, `Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf` |
| **Nscale Cloud Infrastructure** | [https://www.nscale.com](https://www.nscale.com)<br>`HTTP 200` | UK/European GPU cloud builder; partner in Microsoft Essex and Narvik Norway deployments. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Fontes_Noticias_Recentes_Outubro_2026.md` |
| **BlackRock - Global AI Infrastructure Investment Partnership (GAIIP)** | [https://www.blackrock.com](https://www.blackrock.com)<br>`HTTP 200` | Consortium with GIP, Microsoft, and MGX targeting $30B-$100B in mobilized equity and debt for AI data centers. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf` |
| **Blackstone Infrastructure & Private Credit** | [https://www.blackstone.com](https://www.blackstone.com)<br>`HTTP 403` | Leading global asset manager funding data center master trusts and private debt facilities for neoclouds. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf`, `Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf` |
| **Blue Owl Capital - Digital Infrastructure** | [https://www.blueowl.com](https://www.blueowl.com)<br>`HTTP 200` | Alternative asset manager originating direct lending and private credit for hyperscaler data center SPVs. | `Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf` |

---

## Japanese Macro Policy, Bank of Japan (BoJ) & US Treasury TIC Data

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **Bank of Japan (BoJ) Official Statistics** | [https://www.boj.or.jp](https://www.boj.or.jp)<br>`HTTP 200` | Official policy rate decisions, Uncollateralized Overnight Call Rate, and Financial System Reports. | `Relatorio_Macro_Iene_Carry_Trade_Impacto_IA.pdf`, `Report_Macro_Yen_Carry_Trade_AI_Impact.pdf` |
| **U.S. Treasury International Capital (TIC) Data** | [https://ticdata.treasury.gov/Publish/mfh.txt](https://ticdata.treasury.gov/Publish/mfh.txt)<br>`HTTP 200` | Official monthly dataset of Major Foreign Holders of U.S. Treasury Securities (Japan $1,068B portfolio). | `Relatorio_Macro_Iene_Carry_Trade_Impacto_IA.pdf`, `Report_Macro_Yen_Carry_Trade_AI_Impact.pdf` |
| **Ministry of Finance Japan (MoF)** | [https://www.mof.go.jp](https://www.mof.go.jp)<br>`HTTP 200` | Official foreign exchange intervention operations audit log (October 2022 and 2024 dollar sales). | `Relatorio_Macro_Iene_Carry_Trade_Impacto_IA.pdf`, `Report_Macro_Yen_Carry_Trade_AI_Impact.pdf` |
| **Japanese Trade Union Confederation (RENGO)** | [https://www.jtuc-rengo.org](https://www.jtuc-rengo.org)<br>`HTTP 200` | Official Spring Wage Offensive (Shunto) statistics (+5.15% in 2026, +5.28% in 2024). | `Relatorio_Macro_Iene_Carry_Trade_Impacto_IA.pdf`, `Report_Macro_Yen_Carry_Trade_AI_Impact.pdf` |

---

## Market Volatility, Fear Indices & Algorithmic Triggers (CBOE & ICE BofA)

| Source Name | Access URL | Description & Key Audited Metrics | Repository Reports & Scripts Using This Source |
|:---|:---|:---|:---|
| **CBOE (Chicago Board Options Exchange) - VIX Index** | [https://www.cboe.com/tradable_products/vix/](https://www.cboe.com/tradable_products/vix/)<br>`HTTP 200` | Real-time calculation of 30-day forward implied volatility for the S&P 500; triggers systematic Vol-Targeting fund selling at >25. | `Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf`, `Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf`, `Dossie_Indices_do_Medo_VIX_MOVE_e_Desalavancagem_Algoritmica.md` |
| **ICE Benchmark Administration - ICE BofA MOVE Index** | [https://www.theice.com/market-data/indices/ice-bofa-indices](https://www.theice.com/market-data/indices/ice-bofa-indices)<br>`HTTP 200` | Treasury bond implied volatility index (Merrill Lynch Option Volatility Estimate); benchmark for bond market stress and Data Center ABS spread widening at >120. | `Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf`, `Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf`, `Dossie_Indices_do_Medo_VIX_MOVE_e_Desalavancagem_Algoritmica.md` |
| **CBOE - SKEW Index** | [https://www.cboe.com/tradable_products/vix/skew_index/](https://www.cboe.com/tradable_products/vix/skew_index/)<br>`HTTP 200` | Measures tail risk sentiment and perceived probability of outlier negative events (Black Swan index) in US equities. | `Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf`, `Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf` |
| **CBOE - VVIX Index (Volatility of VIX)** | [https://www.cboe.com/tradable_products/vix/vvix_index/](https://www.cboe.com/tradable_products/vix/vvix_index/)<br>`HTTP 200` | Measures expected volatility of the 30-day forward price of the VIX, gauging panic hedging velocity. | `Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf`, `Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf` |
| **CBOE Futures Exchange (CFE) - VIX Term Structure** | [https://www.cboe.com/us/futures/market_statistics/](https://www.cboe.com/us/futures/market_statistics/)<br>`HTTP 200` | Futures curve tracking Contango (normal) vs Inverted Backwardation (acute margin calls and liquidity freeze). | `Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf`, `Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf`, `chart_vix_term_structure_contango_backwardation.png` |

---

