#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_yen_carry_trade_charts.py
------------------------------------
Generates high-resolution bilingual financial charts for the Japanese Yen & Carry Trade Report:
1. chart_yen_carry_trade_historical_divergence.png:
   - USD/JPY exchange rate (2021-2026) vs BoJ vs US Fed interest rate differential.
2. chart_yen_unwind_tech_margin_calls.png:
   - August 2024 shock anatomy: USD/JPY, Nikkei 225, Nasdaq 100, NVIDIA drawdowns & VIX spike.
3. chart_japan_us_treasury_holdings_and_yields.png:
   - Japan TIC US Treasury holdings ($1.32T peak down to $1.07T) vs US 10Y and JGB 10Y yields.
4. chart_yen_stress_scenarios_matrix.png:
   - 2026-2029 FX and liquidity stress scenarios (Tech P/E compression, ABS spread widening).

Outputs to:
  - assets/charts/pt/
  - assets/charts/en/
"""

import os
import sys

# UTF-8 stdout encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CHARTS_PT_DIR = os.path.join(ROOT_DIR, "assets", "charts", "pt")
CHARTS_EN_DIR = os.path.join(ROOT_DIR, "assets", "charts", "en")
os.makedirs(CHARTS_PT_DIR, exist_ok=True)
os.makedirs(CHARTS_EN_DIR, exist_ok=True)

def setup_style():
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#F1F5F9'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.8

def generate_chart_1_historical_divergence():
    """Chart 1: USD/JPY Exchange Rate & Fed vs BoJ Rate Spread (2021-2026)."""
    setup_style()
    timeline = ['2021', '2022-Q1', '2022-Q4', '2023-Q2', '2023-Q4', '2024-Jul', '2024-Aug', '2025-Q2', '2025-Q4', '2026-Atual']
    timeline_en = ['2021', '2022-Q1', '2022-Q4', '2023-Q2', '2023-Q4', '2024-Jul', '2024-Aug', '2025-Q2', '2025-Q4', '2026-Current']

    usdjpy = [110.2, 116.5, 149.8, 140.5, 151.4, 161.95, 142.1, 146.5, 152.8, 149.2]
    fed_funds = [0.25, 0.50, 4.00, 5.25, 5.50, 5.50, 5.50, 4.75, 4.25, 4.00]
    boj_rate = [-0.10, -0.10, -0.10, -0.10, -0.10, 0.25, 0.25, 0.50, 0.75, 1.00]
    spread = [f - b for f, b in zip(fed_funds, boj_rate)]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(timeline))
        x_labels = timeline if lang == 'pt' else timeline_en

        # Subplot 1: USD/JPY Rate
        ax1.plot(x, usdjpy, marker='o', linewidth=2.2, color='#0284C7', label='USD/JPY (Taxa de Câmbio)' if lang == 'pt' else 'USD/JPY (Exchange Rate)')
        ax1.axhline(161.95, color='#DC2626', linestyle=':', alpha=0.7, label='Pico Histórico (161.95)' if lang == 'pt' else 'Multi-Decade High (161.95)')
        ax1.axhline(140.0, color='#10B981', linestyle=':', alpha=0.7, label='Zona de Suporte' if lang == 'pt' else 'Support Zone')

        # Annotations
        ax1.annotate('Intervenção MoF\n(Out/2022)' if lang == 'pt' else 'MoF Intervention\n(Oct/2022)',
                     xy=(2, 149.8), xytext=(2, 125),
                     arrowprops=dict(facecolor='#DC2626', arrowstyle='->', lw=1.0),
                     fontsize=6.2, ha='center', color='#991B1B', fontweight='bold')

        ax1.annotate('Pico 161.95\n(Jul/2024)' if lang == 'pt' else 'Peak 161.95\n(Jul/2024)',
                     xy=(5, 161.95), xytext=(4.3, 168),
                     arrowprops=dict(facecolor='#DC2626', arrowstyle='->', lw=1.0),
                     fontsize=6.2, ha='center', color='#DC2626', fontweight='bold')

        ax1.annotate('Desmonte Relâmpago\n(Ago/2024: 142.1)' if lang == 'pt' else 'Flash Unwind\n(Aug/2024: 142.1)',
                     xy=(6, 142.1), xytext=(6.5, 130),
                     arrowprops=dict(facecolor='#D97706', arrowstyle='->', lw=1.0),
                     fontsize=6.2, ha='center', color='#B45309', fontweight='bold')

        t1 = "Trajetória USD/JPY (2021–2026): A Alavancagem e o Ponto de Inflexão" if lang == 'pt' else "USD/JPY Trajectory (2021–2026): The Carry Supercycle & Inflection"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Cotação USD/JPY" if lang == 'pt' else "USD/JPY Spot", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.5, rotation=25, color='#1E293B')
        ax1.set_ylim(105, 175)
        ax1.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True)

        # Subplot 2: Interest Rate Differential (Fed vs BoJ)
        w = 0.35
        ax2.bar(x - w/2, fed_funds, w, label='US Federal Funds Rate' if lang == 'en' else 'Taxa Fed Funds (EUA)', color='#3B82F6', edgecolor='#1D4ED8')
        ax2.bar(x + w/2, boj_rate, w, label='Bank of Japan Policy Rate' if lang == 'en' else 'Taxa Básica BoJ (Japão)', color='#DC2626', edgecolor='#991B1B')
        ax2.plot(x, spread, color='#10B981', marker='s', linewidth=1.8, label='Diferencial (Spread Fed - BoJ)' if lang == 'pt' else 'Rate Spread (Fed - BoJ)')

        for i in range(len(timeline)):
            ax2.annotate(f"{spread[i]:.2f}%", xy=(x[i], spread[i]), xytext=(0, 4), textcoords="offset points",
                         ha='center', fontsize=5.8, fontweight='bold', color='#047857')

        t2 = "Diferencial de Juros Fed vs BoJ (% a.a.)" if lang == 'pt' else "US-Japan Policy Rate Differential (% p.a.)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Taxa de Juros (%)" if lang == 'pt' else "Interest Rate (%)", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.5, rotation=25, color='#1E293B')
        ax2.set_ylim(-0.5, 6.8)
        ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_yen_carry_trade_historical_divergence.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_2_unwind_tech_margin_calls():
    """Chart 2: August 2024 Shock Anatomy — JPY Spike, Nikkei Plunge, Tech Sell-Off, VIX Spike."""
    setup_style()
    days = ['18-Jul', '24-Jul', '30-Jul', '31-Jul (BoJ)', '01-Ago', '02-Ago (NFP)', '05-Ago (Crash)', '07-Ago', '15-Ago']
    days_en = ['Jul-18', 'Jul-24', 'Jul-30', 'Jul-31 (BoJ)', 'Aug-01', 'Aug-02 (NFP)', 'Aug-05 (Crash)', 'Aug-07', 'Aug-15']

    # Performance normalized to 100 on July 18, 2024
    perf_usdjpy = [100.0, 97.4, 96.1, 94.2, 93.5, 91.8, 88.6, 91.2, 93.4] # USD/JPY falling = JPY strengthening
    perf_nikkei = [100.0, 96.8, 94.5, 95.8, 93.4, 87.9, 77.0, 85.2, 90.1] # Nikkei dropped -12.4% on Aug 5
    perf_nasdaq = [100.0, 96.5, 95.2, 97.8, 95.5, 93.2, 89.8, 92.4, 96.1] # Nasdaq tech selling
    perf_nvda   = [100.0, 92.8, 88.5, 98.2, 91.6, 86.8, 79.5, 84.6, 92.0] # High-beta proxy

    vix_levels  = [15.9, 18.0, 17.7, 16.4, 18.6, 23.4, 65.7, 27.7, 15.2]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(days))
        x_labels = days if lang == 'pt' else days_en

        # Subplot 1: Cross-Asset Performance
        ax1.plot(x, perf_usdjpy, marker='o', linewidth=2.0, color='#0284C7', label='USD/JPY (-11.4% / Iene Forte)' if lang == 'pt' else 'USD/JPY (-11.4% / JPY Squeeze)')
        ax1.plot(x, perf_nikkei, marker='s', linewidth=2.0, color='#DC2626', label='Nikkei 225 (-23.0% / -12.4% no dia)' if lang == 'pt' else 'Nikkei 225 (-23.0% / -12.4% single day)')
        ax1.plot(x, perf_nasdaq, marker='^', linewidth=1.8, color='#64748B', label='Nasdaq 100 (-10.2%)' if lang == 'pt' else 'Nasdaq 100 (-10.2%)')
        ax1.plot(x, perf_nvda, marker='d', linewidth=2.0, color='#10B981', label='NVIDIA Corp (-20.5%)' if lang == 'pt' else 'NVIDIA Corp (-20.5%)')

        ax1.axvline(6, color='#DC2626', linestyle='--', alpha=0.8)
        ax1.annotate('Black Monday\n(05/Ago/2024)' if lang == 'pt' else 'Black Monday\n(Aug 5, 2024)',
                     xy=(6, 77.0), xytext=(4.5, 80),
                     arrowprops=dict(facecolor='#DC2626', arrowstyle='->', lw=1.0),
                     fontsize=6.2, ha='center', color='#991B1B', fontweight='bold')

        t1 = "Transmissão do Choque (Ago/2024): Desmonte Cambial e Liquidação de Tech" if lang == 'pt' else "Transmission Anatomy (Aug 2024): JPY Spike & Forced Tech Liquidation"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Índice de Preço (Base 100 = 18/Jul)" if lang == 'pt' else "Price Index (Base 100 = Jul 18)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.2, rotation=25, color='#1E293B')
        ax1.set_ylim(70, 105)
        ax1.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=5.8)
        ax1.grid(True)

        # Subplot 2: VIX Explosion
        ax2.bar(x, vix_levels, width=0.55, color='#F59E0B', edgecolor='#D97706', label='CBOE Volatility Index (^VIX)')
        ax2.axhline(20.0, color='#64748B', linestyle=':', label='Média Histórica (20.0)' if lang == 'pt' else 'Historical Mean (20.0)')
        ax2.axhline(65.73, color='#DC2626', linestyle='--', label='Pico Intraday (65.73)' if lang == 'pt' else 'Intraday Spike (65.73)')

        for i in range(len(days)):
            if i == 6:
                ax2.annotate(f"{vix_levels[i]:.1f}", xy=(x[i], vix_levels[i]), xytext=(0, 3), textcoords="offset points",
                             ha='center', fontsize=7.0, fontweight='bold', color='#DC2626')
            else:
                ax2.annotate(f"{vix_levels[i]:.1f}", xy=(x[i], vix_levels[i]), xytext=(0, 2), textcoords="offset points",
                             ha='center', fontsize=5.8, color='#475569')

        t2 = "Explosão de Volatilidade Sistêmica: VIX Intraday (Ago/2024)" if lang == 'pt' else "Systemic Volatility Surge: Intraday VIX Spike (Aug 2024)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Pontos do VIX" if lang == 'pt' else "VIX Index Points", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.2, rotation=25, color='#1E293B')
        ax2.set_ylim(0, 75)
        ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_yen_unwind_tech_margin_calls.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_3_japan_us_treasury_holdings():
    """Chart 3: Japan US Treasury Holdings (TIC Data) vs US 10Y and JGB 10Y Yields."""
    setup_style()
    years = ['2021-Nov', '2022-Out', '2023-Dez', '2024-Jul', '2024-Nov', '2025-Jun', '2025-Dez', '2026-Ago (Atual)']
    years_en = ['Nov-2021', 'Oct-2022', 'Dec-2023', 'Jul-2024', 'Nov-2024', 'Jun-2025', 'Dec-2025', 'Aug-2026 (Current)']

    holdings_billions = [1325.0, 1076.3, 1138.2, 1115.7, 1120.4, 1170.0, 1185.5, 1068.3]
    us_10y_yield      = [1.45, 4.10, 3.88, 4.40, 4.42, 4.75, 4.90, 5.10]
    jgb_10y_yield     = [0.05, 0.25, 0.65, 1.05, 1.07, 1.15, 1.25, 1.35]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(years))
        x_labels = years if lang == 'pt' else years_en

        # Subplot 1: Japan TIC Holdings
        ax1.bar(x, holdings_billions, width=0.52, color='#3B82F6', edgecolor='#1D4ED8', label='Títulos do Tesouro dos EUA detidos pelo Japão (US$ Bi)' if lang == 'pt' else 'Japan Holdings of US Treasuries (TIC $B)')
        ax1.axhline(1325.0, color='#64748B', linestyle=':', label='Pico Histórico ($1,325B)' if lang == 'pt' else 'All-Time Peak ($1,325B)')

        for i in range(len(years)):
            ax1.annotate(f"${holdings_billions[i]:.0f}B", xy=(x[i], holdings_billions[i]), xytext=(0, 2), textcoords="offset points",
                         ha='center', fontsize=6.0, fontweight='bold', color='#1E293B')

        t1 = "Japão: Carteira de Dívida dos EUA (Dados Oficiais TIC, US$ Bi)" if lang == 'pt' else "Japan US Treasury Portfolio (Official TIC Data, $B)"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Bilhões de Dólares (US$ Bi)" if lang == 'pt' else "Billions of USD ($B)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.2, rotation=25, color='#1E293B')
        ax1.set_ylim(900, 1420)
        ax1.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.0)
        ax1.grid(True, axis='y')

        # Subplot 2: Yield Comparison (US 10Y vs JGB 10Y)
        ax2.plot(x, us_10y_yield, marker='o', linewidth=2.0, color='#DC2626', label='Yield US Treasury 10 Anos' if lang == 'pt' else 'US 10Y Treasury Yield')
        ax2.plot(x, jgb_10y_yield, marker='s', linewidth=2.0, color='#10B981', label='Yield JGB Japão 10 Anos' if lang == 'pt' else 'Japan 10Y JGB Yield')

        for i in range(len(years)):
            ax2.annotate(f"{us_10y_yield[i]:.2f}%", xy=(x[i], us_10y_yield[i]), xytext=(0, 3), textcoords="offset points",
                         ha='center', fontsize=5.8, color='#991B1B', fontweight='bold')
            ax2.annotate(f"{jgb_10y_yield[i]:.2f}%", xy=(x[i], jgb_10y_yield[i]), xytext=(0, -8), textcoords="offset points",
                         ha='center', fontsize=5.8, color='#047857', fontweight='bold')

        t2 = "Pressão de Rendimentos: US 10Y vs JGB 10Y (% a.a.)" if lang == 'pt' else "Sovereign Yield Pressure: US 10Y vs Japan 10Y JGB (% p.a.)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Rendimento Anual (%)" if lang == 'pt' else "Annual Yield (%)", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.2, rotation=25, color='#1E293B')
        ax2.set_ylim(-0.2, 5.8)
        ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax2.grid(True)

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_japan_us_treasury_holdings_and_yields.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_4_yen_stress_scenarios_matrix():
    """Chart 4: Multi-Asset Stress Scenarios under JPY Normalization & Carry Deleveraging."""
    setup_style()
    scenarios = ['Cenário A: Normalização Gradual\n(USD/JPY 145–155)',
                 'Cenário B: Desmonte Acelerado\n(USD/JPY 130–140)',
                 'Cenário C: Choque Sistêmico FX\n(USD/JPY < 125)']
    scenarios_en = ['Scenario A: Orderly Normalization\n(USD/JPY 145–155)',
                    'Scenario B: Accelerated Deleveraging\n(USD/JPY 130–140)',
                    'Scenario C: Systemic FX Shock\n(USD/JPY < 125)']

    probs = [50.0, 35.0, 15.0]
    pe_compression = [-8.0, -18.5, -35.0] # Multiple contraction in Big Tech P/E (%)
    abs_spread_bps = [+45, +140, +320]    # Data Center ABS spread widening (bps)

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(scenarios))
        x_labels = scenarios if lang == 'pt' else scenarios_en

        # Subplot 1: Probabilities and Tech Valuation Compression
        w = 0.38
        b1 = ax1.bar(x - w/2, probs, w, label='Probabilidade Atribuída (%)' if lang == 'pt' else 'Assigned Probability (%)', color='#0284C7', edgecolor='#0369A1')
        b2 = ax1.bar(x + w/2, [abs(p) for p in pe_compression], w, label='Compressão Múltiplo P/E Big Tech (%)' if lang == 'pt' else 'Big Tech P/E Multiple Contraction (%)', color='#EF4444', edgecolor='#B91C1C')

        for i in range(len(scenarios)):
            ax1.annotate(f"{probs[i]:.0f}%", xy=(x[i] - w/2, probs[i]), xytext=(0, 2), textcoords="offset points",
                         ha='center', fontsize=6.5, fontweight='bold', color='#0369A1')
            ax1.annotate(f"-{abs(pe_compression[i]):.1f}%", xy=(x[i] + w/2, abs(pe_compression[i])), xytext=(0, 2), textcoords="offset points",
                         ha='center', fontsize=6.5, fontweight='bold', color='#B91C1C')

        t1 = "Matriz de Cenários JPY: Probabilidade vs Compressão de Valuation" if lang == 'pt' else "JPY Scenario Matrix: Probability vs Tech Valuation Contraction"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Percentual (%)" if lang == 'pt' else "Percentage (%)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.2, color='#1E293B')
        ax1.set_ylim(0, 60)
        ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True, axis='y')

        # Subplot 2: Spread Widening in AI Infrastructure Credit (ABS)
        colors_abs = ['#10B981', '#F59E0B', '#DC2626']
        bars_abs = ax2.bar(x, abs_spread_bps, width=0.45, color=colors_abs, edgecolor='#334155')

        for i in range(len(scenarios)):
            ax2.annotate(f"+{abs_spread_bps[i]} bps", xy=(x[i], abs_spread_bps[i]), xytext=(0, 3), textcoords="offset points",
                         ha='center', fontsize=6.8, fontweight='bold', color='#0F172A')

        t2 = "Alargamento de Spreads: Data Center ABS Tranche BBB/A (bps)" if lang == 'pt' else "Spread Widening: Data Center ABS BBB/A Tranches (bps)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Pontos-Base (bps)" if lang == 'pt' else "Basis Points (bps)", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.2, color='#1E293B')
        ax2.set_ylim(0, 380)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_yen_stress_scenarios_matrix.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def main():
    print("=" * 70)
    print("  GENERATING JAPANESE YEN & CARRY TRADE CHARTS (PT & EN)")
    print("=" * 70)
    generate_chart_1_historical_divergence()
    generate_chart_2_unwind_tech_margin_calls()
    generate_chart_3_japan_us_treasury_holdings()
    generate_chart_4_yen_stress_scenarios_matrix()
    print("=" * 70)
    print("  🎉 All 4 bilingual Yen Carry Trade charts successfully generated!")
    print("=" * 70)

if __name__ == "__main__":
    main()
