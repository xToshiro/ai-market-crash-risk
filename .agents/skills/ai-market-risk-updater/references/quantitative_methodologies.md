# Quantitative Methodologies & Mathematical Formulations

This document provides the formal quantitative models, equations, and stress calibration rules used throughout the risk assessment engine.

---

## 1. GPU Economic Depreciation vs. Debt Amortization

### 1.1 Hyperbolic Decay Model
The secondary market value $V(t)$ of an enterprise accelerator (e.g., H100) is modeled as a compound decay function driven by calendar aging and next-generation architecture announcements:

$$V(t) = V_0 \cdot \exp\left(-\left(\lambda_{\text{base}} + \delta_{\text{next-gen}}(t)\right) \cdot t\right)$$

Where:
- $V_0$: Initial invoice purchase price per node (e.g., \$30,000 for H100 SXM5).
- $\lambda_{\text{base}}$: Baseline economic obsolescence rate ($\approx 0.28\text{ yr}^{-1}$, corresponding to a 2.5-year half-life).
- $\delta_{\text{next-gen}}(t)$: Shock parameter activated upon commercial delivery of next-generation silicon (e.g., Blackwell B200 or Rubin architecture):
  $$\delta_{\text{next-gen}}(t) = \begin{cases} 0.35 & \text{if } t \ge t_{\text{launch}} \\ 0 & \text{otherwise} \end{cases}$$

### 1.2 Loan-to-Value (LTV) and Negative Equity Point
Given initial debt $D_0$ with amortization schedule $A(t)$ and interest rate $r$:

$$\text{LTV}(t) = \frac{D(t)}{V(t)} = \frac{D_0 - \int_0^t A(\tau)\,d\tau}{V(t)}$$

- **Technical Default Covenant**: If $\text{LTV}(t) \ge 0.85$, the credit facility triggers mandatory cash sweeps.
- **Liquidation Event**: If $\text{LTV}(t) \ge 1.00$, the collateral is underwater, incentivizing strategic default by the neocloud borrower.

---

## 2. Debt Service Coverage Ratio (DSCR) Dynamics

The operating cash flow available for debt service ($\text{CFADS}$) is determined by cloud utilization and spot pricing:

$$\text{CFADS}(t) = \left( P_{\text{spot}}(t) \cdot U(t) \cdot 8760 \right) - \left( C_{\text{power}} + C_{\text{cooling}} + C_{\text{maint}} \right)$$

$$\text{DSCR}(t) = \frac{\text{CFADS}(t)}{\text{Interest}(t) + \text{Principal}(t)}$$

- **KBRA Minimum Rating Benchmark**: Class A Notes require $\text{DSCR} \ge 1.35x$.
- **Distress Boundary**: If $\text{DSCR} < 1.10x$, cash trap mechanisms capture all residual equity dividends.
- **Default Threshold**: $\text{DSCR} < 1.00x$ forces bankruptcy filing or restructuring.

---

## 3. Multi-Factor Geopolitical Vulnerability Index (GVI)

The systemic vulnerability score $S_c$ for country $c$ is computed using a 6-factor normalized weighted matrix:

$$S_c = \sum_{k \in \{E, F, X, T, M, G\}} w_k \cdot f_{k, c} + \Omega_{\text{region}}(c)$$

### 3.1 Factor Weightings ($w_k$)
| Code | Factor Name | Weight ($w_k$) | Key Metric |
|:---:|:---|:---:|:---|
| **E** | Energy & Resource Dependence | **0.20** | Net energy import ratio / LNG exposure. |
| **F** | Fiscal & Sovereign Debt Fragility | **0.20** | Debt/GDP, annual interest/tax revenues. |
| **X** | Semiconductor & Tech Exposure | **0.20** | Share of GDP linked to AI CapEx / chip supply chains. |
| **T** | Trade Choke Points & Transit | **0.15** | Vulnerability to Malacca, Hormuz, Taiwan Strait disruption. |
| **M** | Military & Geopolitical Flashpoints | **0.15** | Conflict proximity and defense mobilization risk. |
| **G** | Global Liquidity & FX Contagion | **0.10** | External debt in USD / foreign reserve coverage ratio. |

### 3.2 Regional Overlays ($\Omega_{\text{region}}$)
- **Taiwan / Strait Zone**: $+2.5$ points (high supply concentration shock).
- **Middle East Choke Point (Hormuz/Red Sea)**: $+2.0$ points.
- **Japan / East Asia**: $+1.5$ points (FX carry-trade unwind sensitivity).

---

## 4. Scenario Probability Buildup & Cascade Matrix

The market transition is simulated across three non-overlapping states:

$$\sum_{i=1}^{3} P(S_i) = 1.00$$

1. **$S_1$: Orderly Deflation ($P = 35\%$)**:
   - CapEx deceleration to organic software ARR growth.
   - S&P multiple contracts from $22x$ to $18x$ forward P/E.
2. **$S_2$: Credit Dislocation ($P = 45\%$)**:
   - Secondary GPU market crashes $>50\%$.
   - Private credit liquidity freeze; junior ABS tranches default.
3. **$S_3$: Multi-Contagion Systemic Crash ($P = 20\%$)**:
   - Simultaneous Taiwan Strait disruption + US Treasury auction failure.
   - Severe flight to liquidity; emergency central bank swap lines.

---

## 5. Japanese Yen Carry-Trade Liquidity Transmission & VaR Breakeven Thresholds

* **Source**: BIS, Bank of Japan (BoJ) & U.S. Treasury TIC Reports
* **Application**: Used in `Report_Macro_Yen_Carry_Trade_AI_Impact.pdf` and `Dossie_Macro_Iene_Carry_Trade_e_Liquidez_Global.md`.

Quantifies the net return of yen-funded leverage into dollar-denominated tech assets and establishes the critical systemic failure thresholds:

### 5.1 Net Carry Hurdle Formulation
$$R_{\text{carry}}(t) = \int_0^t \left( r_{\text{Fed}}(\tau) - r_{\text{BoJ}}(\tau) \right) d\tau - \left( \frac{S(0) - S(t)}{S(0)} \right)$$

Where $S(t)$ is the USD/JPY spot exchange rate.

### 5.2 Forensic Failure Thresholds
1. **Warning Level ($S = 140.00$)**:
   $$\text{Recent Tranche De-risking} \implies \text{VIX} \in [25, 35], \quad \Delta \text{Nasdaq} \approx -8\%$$
2. **Global Carry Breakeven ($S^* = 130.00$)**:
   $$R_{\text{carry}}(t) \le 0 \implies \text{Mandatory Voluntary Unwind / Margin Liquidation}$$
3. **Global Systemic Rupture Boundary ($S^{**} \le 125.00$)**:
   $$\text{VaR Breach Event} \implies \text{Credit Freeze}, \quad \text{ABS Spreads} > +300\text{ bps}, \quad \Delta \text{Big Tech P/E} \approx -35\%$$
4. **Dynamic Velocity Trigger**:
   $$\text{Systemic Dislocation Condition} \iff S(t) < 130.00 \quad \text{AND} \quad \left| \frac{dS}{dt} \right| \ge 1.50 \text{ JPY/day}$$

