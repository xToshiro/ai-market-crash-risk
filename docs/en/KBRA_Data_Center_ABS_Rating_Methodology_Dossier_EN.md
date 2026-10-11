# Technical Dossier: Official Data Center ABS Rating Methodology (KBRA & S&P)
**Reference:** KBRA Data Center ABS Global Rating Methodology (2026 Updated Edition) and S&P Global Structured Finance Criteria.

---

## 1. Overview of the KBRA Methodology

Kroll Bond Rating Agency (KBRA) is the pioneer and leading rating agency evaluating **Data Center Asset-Backed Securities (ABS)**. Unlike traditional residential or commercial mortgages (RMBS/CMBS), data center securitization represents a hybrid between **commercial real estate credit, mission-critical infrastructure operational risk, and advanced technology**.

### The Four Analytical Pillars of KBRA:
1. **Physical Collateral Quality (Critical Facility & Power):** Power redundancy (N+1, 2N architectures), energy efficiency (PUE - *Power Usage Effectiveness*), utility supply agreements (*PPAs - Power Purchase Agreements*), and mission-critical cooling topologies.
2. **Cash Flow Durability (KNCF - KBRA Net Cash Flow):** Audited operational cash flows adjusted for severe stress haircuts: non-recoverable operating expenses, ongoing maintenance capital expenditures (*Replacement Capex*), and baseline structural vacancy allowances.
3. **Tenant Credit Quality & Lease Concentration:** Credit ratings of each counterparty, weighted average lease term (*WALT*), and multi-tenant default/turnover simulation models (*Tenant Default & Rollover Simulation*).
4. **Structural Mechanics & Liquidity Covenants:** Subordination levels across debt classes (Class B and C notes), dedicated liquidity reserves (*Debt Service Reserve Accounts - DSRA*), coverage ratios (*DSCR*), and cash trap / rapid amortization triggers (*Cash Sweep Events*).

---

## 2. The KNCF Formula and Stress Tests for "AAA / A" Rated Tranches

For a Senior Tranche to achieve an investment-grade rating of **AAA (sf)** or **A / A- (sf)**, KBRA subjects cash flows to severe stress scenarios:

$$KNCF = Gross\ Contracted\ Revenue - (Operating\ Expenses + Maintenance\ Capex + Forced\ Vacancy\ Haircut)$$

### Key Stress Parameters Applied:
* **AAA / A Stress Scenarios:**
  * Immediate bankruptcy simulation of the top two portfolio tenants without any replacement revenue for a **12 to 24-month period (*Dark Period*)**.
  * A 15% to 30% markdown on contractual rent per kW/month upon renewal or releasing (*Mark-to-Market Rent Haircut*).
  * A 10% to 20% spike in ongoing energy utility and facility operating expenses.
  * The stressed residual cash flow must still cover 100% of Class A debt service requirements (DSCR $\ge$ 1.0x under peak stress).

---

## 3. The Critical Factor: Tenant Concentration and "Binary Risk"

KBRA bifurcates the Data Center ABS universe into two foundational segments with radically distinct risk architectures:

| Segment | Tenant Characteristics | Typical Concentration | KBRA Credit Risk Assessment | Representative Issuances |
| :--- | :--- | :--- | :--- | :--- |
| **Hyperscale ABS / Single-Asset** | 1 to 3 tech titans (Microsoft, AWS, Google, Oracle, Meta). Long-term (10 to 15-year) *Triple Net (NNN)* leases. | **80% to 95%** concentrated across Top 2 off-takers. | **Binary Default Risk:** Debt rating is tied directly to the sovereign-like balance sheet of the Hyperscaler. If the tenant vacates or terminates, the facility loses virtually all income. | CONE 2026-DFW3, Lohrasp Enterprise II, STACK Issuer. |
| **Colocation (Colo) Master Trust** | Dozens to hundreds of enterprise tenants, telecom carriers, neoclouds, and software companies. | Top 1 tenant typically accounts for **< 15%**; highly diversified portfolio. | **Operational Churn Risk:** Low binary credit risk, but heightened vulnerability to customer turnover (*churn*), SME credit cycles, and unhedged variable power tariffs. | DataBank Issuer (Series 2021/2024/2026 with ~1,750 tenants), TierPoint, Centersquare. |

---

## 4. Where Hidden Fragility Resides: The AI Cycle Nexus

While the mathematical rating framework appears robust under historical conditions, recent credit surveillance highlights **three structural vulnerabilities not captured in standard 2018–2022 rating models**:

1. **Hidden Systemic Correlation:** Rating agency models treat customer default probabilities as independent variables. However, with the generative AI buildout, the revenue streams of neoclouds and retail colocation providers depend heavily on the commercial viability of foundation models developed by a small cluster of companies (OpenAI, Anthropic, Meta, Microsoft).
2. **Cooling Infrastructure Obsolescence:** Data centers engineered prior to 2023 were designed for thermal power densities of 8 kW to 15 kW per rack. Next-generation AI clusters (Nvidia H100, B200, GB200) require **40 kW to 120 kW per rack supported by direct liquid cooling**. Facilities unable to undergo structural retrofits face severe collateral markdown (*LTV degradation*).
3. **Grid Interconnection Delays:** KBRA criteria mandate secured power allocations. However, transmission interconnection delays of 24 to 36 months by regional electric utilities can postpone lease commencement dates, squeezing liquidity in junior mezzanine tranches before cash flow stabilization.

---
*Document compiled from official KBRA Data Center Rating Methodologies, S&P Global Structured Finance criteria, and institutional regulatory filings.*
