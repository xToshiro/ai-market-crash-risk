#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fear_indices_charts.py
---------------------------------
Generates high-resolution bilingual financial charts for the Fear Indices (VIX, MOVE, Vol-Targeting) Report:
1. chart_vix_historical_spikes_and_tech_drawdowns.png:
   - Historical VIX spikes (2018–2026) vs Tech & Semi drawdown severity.
2. chart_dual_fear_index_vix_vs_move.png:
   - Dual Volatility Matrix: CBOE VIX (Equity) vs ICE BofA MOVE (Treasury/Bond Volatility).
3. chart_vix_term_structure_contango_backwardation.png:
   - VIX Futures Curve: Normal Contango vs Acute Panic Backwardation (August 2024 & Stress).
4. chart_vol_targeting_deleveraging_cascade.png:
   - Algorithmic Deleveraging: Vol-Targeting Equity Allocation & Forced Big Tech Selling ($B).

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

def generate_chart_1_vix_historical_spikes():
    """Chart 1: Historical VIX Spikes (2018–2026) vs Tech & Semiconductor Drawdowns."""
    setup_style()
    events = [
        'Volmageddon\n(Fev/2018)',
        'Q4 Tightening\n(Dez/2018)',
        'Covid-19 Crash\n(Mar/2020)',
        'Ciclo Inflacionário\n(Jun/2022)',
        'Crise Bancos SVB\n(Mar/2023)',
        'Carry Trade Unwind\n(Ago/2024)',
        'Outubro 2026\n(Atual)'
    ]
    events_en = [
        'Volmageddon\n(Feb 2018)',
        'Q4 Tightening\n(Dec 2018)',
        'Covid-19 Crash\n(Mar 2020)',
        'Inflation Tightening\n(Jun 2022)',
        'SVB Banking Shock\n(Mar 2023)',
        'Carry Trade Unwind\n(Aug 2024)',
        'October 2026\n(Current)'
    ]

    vix_peaks = [50.3, 36.2, 82.69, 34.0, 30.8, 65.73, 21.8]
    nasdaq_drawdowns = [-10.5, -23.1, -30.1, -33.8, -12.4, -10.2, -6.5]
    nvda_drawdowns = [-15.2, -54.0, -38.5, -66.4, -18.2, -20.5, -12.0]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(events))
        x_labels = events if lang == 'pt' else events_en

        # Subplot 1: VIX Peak Levels
        colors_vix = ['#F59E0B', '#F59E0B', '#DC2626', '#F59E0B', '#F59E0B', '#DC2626', '#0284C7']
        bars1 = ax1.bar(x, vix_peaks, width=0.52, color=colors_vix, edgecolor='#1E293B')
        ax1.axhline(20.0, color='#64748B', linestyle=':', label='Média Histórica (20.0)' if lang == 'pt' else 'Historical Mean (20.0)')
        ax1.axhline(40.0, color='#DC2626', linestyle='--', label='Limiar de Pânico Sistêmico (40.0)' if lang == 'pt' else 'Systemic Panic Threshold (40.0)')

        for i in range(len(events)):
            ax1.annotate(f"{vix_peaks[i]:.1f}", xy=(x[i], vix_peaks[i]), xytext=(0, 3), textcoords="offset points",
                         ha='center', fontsize=6.5, fontweight='bold', color='#0F172A')

        t1 = "Picos Históricos do Índice de Volatilidade CBOE VIX (2018–2026)" if lang == 'pt' else "Historical Spikes of the CBOE Volatility Index (VIX) (2018–2026)"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Pontos do VIX" if lang == 'pt' else "VIX Index Points", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.0, color='#1E293B')
        ax1.set_ylim(0, 95)
        ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True, axis='y')

        # Subplot 2: QQQ vs NVDA Drawdowns during VIX Spikes
        w = 0.35
        b_qqq = ax2.bar(x - w/2, [abs(d) for d in nasdaq_drawdowns], w, label='Drawdown Nasdaq 100 (QQQ)' if lang == 'pt' else 'Nasdaq 100 Drawdown (QQQ)', color='#3B82F6', edgecolor='#1D4ED8')
        b_nvd = ax2.bar(x + w/2, [abs(d) for d in nvda_drawdowns], w, label='Drawdown NVIDIA Corp (NVDA)' if lang == 'pt' else 'NVIDIA Corp Drawdown (NVDA)', color='#10B981', edgecolor='#047857')

        for i in range(len(events)):
            ax2.annotate(f"-{abs(nasdaq_drawdowns[i]):.1f}%", xy=(x[i] - w/2, abs(nasdaq_drawdowns[i])), xytext=(0, 2), textcoords="offset points",
                         ha='center', fontsize=5.5, fontweight='bold', color='#1D4ED8')
            ax2.annotate(f"-{abs(nvda_drawdowns[i]):.1f}%", xy=(x[i] + w/2, abs(nvda_drawdowns[i])), xytext=(0, 2), textcoords="offset points",
                         ha='center', fontsize=5.5, fontweight='bold', color='#047857')

        t2 = "Severidade de Queda: Nasdaq 100 vs NVIDIA durante Choques do VIX" if lang == 'pt' else "Drawdown Severity: Nasdaq 100 vs NVIDIA during VIX Spikes"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Queda Máxima (%)" if lang == 'pt' else "Max Peak-to-Trough Drawdown (%)", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.0, color='#1E293B')
        ax2.set_ylim(0, 75)
        ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_vix_historical_spikes_and_tech_drawdowns.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_2_dual_fear_index_vix_vs_move():
    """Chart 2: Dual Volatility Index — CBOE VIX (Equities) vs ICE BofA MOVE (Treasury Bonds)."""
    setup_style()
    timeline = ['2021-Dez', '2022-Jun', '2022-Out', '2023-Mar (SVB)', '2023-Out', '2024-Ago (Carry)', '2025-Dez', '2026-Out (Atual)']
    timeline_en = ['Dec 2021', 'Jun 2022', 'Oct 2022', 'Mar 2023 (SVB)', 'Oct 2023', 'Aug 2024 (Carry)', 'Dec 2025', 'Oct 2026 (Current)']

    vix_series  = [18.6, 31.2, 33.5, 26.5, 21.7, 65.7, 16.4, 21.8]
    move_series = [77.1, 138.2, 160.7, 198.7, 142.5, 134.8, 108.2, 126.4]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(timeline))
        x_labels = timeline if lang == 'pt' else timeline_en

        # Subplot 1: Normalized trajectory (Base 100 = Dec 2021)
        norm_vix = [v / vix_series[0] * 100 for v in vix_series]
        norm_move = [m / move_series[0] * 100 for m in move_series]

        ax1.plot(x, norm_vix, marker='o', linewidth=2.0, color='#0284C7', label='CBOE VIX (Volatilidade Ações EUA)' if lang == 'pt' else 'CBOE VIX (US Equity Volatility)')
        ax1.plot(x, norm_move, marker='s', linewidth=2.0, color='#DC2626', label='ICE BofA MOVE (Volatilidade Dívida Pública EUA)' if lang == 'pt' else 'ICE BofA MOVE (US Treasury Volatility)')

        ax1.axhline(100.0, color='#64748B', linestyle=':', label='Base Inicial (Dez/2021 = 100)' if lang == 'pt' else 'Baseline (Dec 2021 = 100)')

        for i in range(len(timeline)):
            if i in [3, 5, 7]:
                ax1.annotate(f"MOVE: {move_series[i]:.0f}", xy=(x[i], norm_move[i]), xytext=(0, 4), textcoords="offset points",
                             ha='center', fontsize=5.8, fontweight='bold', color='#991B1B')

        t1 = "O Índice Duplo do Medo: VIX (Ações) vs MOVE (Tesouro Americano)" if lang == 'pt' else "The Dual Fear Gauge: VIX (Equities) vs MOVE (US Treasuries)"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Índice Normalizado (Base 100 = Dez/2021)" if lang == 'pt' else "Normalized Index (Dec 2021 = 100)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.0, rotation=25, color='#1E293B')
        ax1.set_ylim(60, 280)
        ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True)

        # Subplot 2: MOVE Index Levels and ABS Spread Widening
        move_regimes = ['Normal\n(< 90 pts)', 'Elevado\n(90–120 pts)', 'Estresse de Crédito\n(120–150 pts)', 'Congelamento\n(> 150 pts)']
        move_regimes_en = ['Normal\n(< 90 pts)', 'Elevated\n(90–120 pts)', 'Credit Stress\n(120–150 pts)', 'Market Freeze\n(> 150 pts)']
        abs_spreads_bps = [115, 185, 290, 480]

        colors_regimes = ['#10B981', '#3B82F6', '#F59E0B', '#DC2626']
        x2 = np.arange(len(move_regimes))
        x2_labels = move_regimes if lang == 'pt' else move_regimes_en

        ax2.bar(x2, abs_spreads_bps, width=0.48, color=colors_regimes, edgecolor='#1E293B')

        for i in range(len(move_regimes)):
            ax2.annotate(f"+{abs_spreads_bps[i]} bps", xy=(x2[i], abs_spreads_bps[i]), xytext=(0, 3), textcoords="offset points",
                         ha='center', fontsize=6.5, fontweight='bold', color='#0F172A')

        t2 = "Transmissão do MOVE no Custo de Emissão de Data Center ABS (bps)" if lang == 'pt' else "Transmission of MOVE Volatility to Data Center ABS Spreads (bps)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Spread de Crédito BBB/A (bps)" if lang == 'pt' else "Credit Spread BBB/A (bps)", fontsize=8, color='#475569')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(x2_labels, fontsize=6.2, color='#1E293B')
        ax2.set_ylim(0, 560)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_dual_fear_index_vix_vs_move.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_3_vix_term_structure():
    """Chart 3: VIX Term Structure — Contango (Normal Calm) vs Backwardation (Acute Panic)."""
    setup_style()
    maturities = ['Spot (À Vista)', '1 Mês (Fut)', '2 Meses (Fut)', '3 Meses (Fut)', '4 Meses (Fut)', '6 Meses (Fut)']
    maturities_en = ['Spot Cash', '1M Futures', '2M Futures', '3M Futures', '4M Futures', '6M Futures']

    curve_calm = [13.2, 14.8, 16.1, 17.2, 18.0, 19.1]     # Textbook Contango (upward sloping)
    curve_current = [21.8, 22.4, 22.9, 23.2, 23.5, 24.0]  # Flat Contango (October 2026 tension)
    curve_panic = [65.7, 38.5, 30.2, 27.4, 25.8, 24.5]    # Severe Backwardation (Aug 5, 2024 inversion)

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(maturities))
        x_labels = maturities if lang == 'pt' else maturities_en

        # Subplot 1: Curves
        ax1.plot(x, curve_calm, marker='o', linewidth=2.0, color='#10B981', label='Regime Complacente (Contango Normal: Spot 13.2)' if lang == 'pt' else 'Complacent Regime (Normal Contango: Spot 13.2)')
        ax1.plot(x, curve_current, marker='s', linewidth=2.0, color='#0284C7', label='Regime Atual Out/2026 (Contango Estreito: Spot 21.8)' if lang == 'pt' else 'Current Regime Oct 2026 (Flat Contango: Spot 21.8)')
        ax1.plot(x, curve_panic, marker='^', linewidth=2.2, color='#DC2626', linestyle='--', label='Choque de Pânico (Backwardation Invertida: Spot 65.7)' if lang == 'pt' else 'Acute Panic Shock (Inverted Backwardation: Spot 65.7)')

        ax1.annotate('Backwardation Extrema:\nCorrida por Proteção Imediata' if lang == 'pt' else 'Severe Backwardation:\nPanic Demand for Immediate Hedges',
                     xy=(0, 65.7), xytext=(1.2, 58),
                     arrowprops=dict(facecolor='#DC2626', arrowstyle='->', lw=1.0),
                     fontsize=6.2, ha='left', color='#991B1B', fontweight='bold')

        t1 = "Curva a Termo do VIX: Contango (Ordem) vs Backwardation (Pânico)" if lang == 'pt' else "VIX Futures Term Structure: Contango (Calm) vs Backwardation (Panic)"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Volatilidade Implícita Anualizada (%)" if lang == 'pt' else "Implied Volatility Annualized (%)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.2, rotation=20, color='#1E293B')
        ax1.set_ylim(10, 75)
        ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.0)
        ax1.grid(True)

        # Subplot 2: Spread Spot minus 3M (Inversion Indicator)
        spread_inversion = [c[0] - c[3] for c in [curve_calm, curve_current, curve_panic]]
        regime_names = ['Mercado Calmo\n(Contango)', 'Atual Out/2026\n(Tensão Neutra)', 'Choque Ago/2024\n(Pânico Sistêmico)']
        regime_names_en = ['Calm Market\n(Contango)', 'Current Oct 2026\n(Neutral Tension)', 'Aug 2024 Shock\n(Systemic Panic)']
        x_reg = np.arange(3)
        x_reg_labels = regime_names if lang == 'pt' else regime_names_en

        colors_spread = ['#10B981', '#0284C7', '#DC2626']
        bars2 = ax2.bar(x_reg, spread_inversion, width=0.45, color=colors_spread, edgecolor='#1E293B')
        ax2.axhline(0, color='#64748B', linestyle='-', lw=0.8)

        for i in range(3):
            val_txt = f"{spread_inversion[i]:+.1f} pts"
            y_pos = spread_inversion[i] + 1.2 if spread_inversion[i] >= 0 else spread_inversion[i] - 3.5
            ax2.annotate(val_txt, xy=(x_reg[i], y_pos), ha='center', fontsize=6.8, fontweight='bold',
                         color='#0F172A')

        t2 = "Diferencial de Inversão da Curva (VIX Spot - Futuro 3M)" if lang == 'pt' else "Curve Inversion Spread (VIX Spot minus 3M Futures)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Diferencial (Pontos do VIX)" if lang == 'pt' else "Spread (VIX Points)", fontsize=8, color='#475569')
        ax2.set_xticks(x_reg)
        ax2.set_xticklabels(x_reg_labels, fontsize=6.2, color='#1E293B')
        ax2.set_ylim(-8, 45)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_vix_term_structure_contango_backwardation.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def generate_chart_4_vol_targeting_deleveraging():
    """Chart 4: Systematic Vol-Targeting Deleveraging & Forced Big Tech Selling Volume."""
    setup_style()
    vix_scenarios = ['VIX = 12\n(Complacência)', 'VIX = 18\n(Equilíbrio)', 'VIX = 25\n(Gatilho Alerta)', 'VIX = 35\n(Desalavancagem)', 'VIX = 50+\n(Liquidação Total)']
    vix_scenarios_en = ['VIX = 12\n(Complacency)', 'VIX = 18\n(Neutral)', 'VIX = 25\n(Warning Trigger)', 'VIX = 35\n(Deleveraging)', 'VIX = 50+\n(Forced Liquidations)']

    equity_exposure_pct = [100.0, 78.5, 52.0, 34.0, 18.5] # Weight allocated to equities by systematic vol-targeters
    forced_selling_billions = [0.0, 45.0, 160.0, 310.0, 520.0] # Aggregate institutional forced liquidations in USD Billions

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(vix_scenarios))
        x_labels = vix_scenarios if lang == 'pt' else vix_scenarios_en

        # Subplot 1: Equity Exposure
        ax1.plot(x, equity_exposure_pct, marker='o', linewidth=2.2, color='#3B82F6', label='Exposição Máxima a Ações (%)' if lang == 'pt' else 'Target Equity Exposure (%)')
        ax1.axhline(50.0, color='#DC2626', linestyle=':', label='Linha de Corte Crítica (50%)' if lang == 'pt' else 'Critical Cutoff Line (50%)')

        for i in range(len(vix_scenarios)):
            ax1.annotate(f"{equity_exposure_pct[i]:.1f}%", xy=(x[i], equity_exposure_pct[i]), xytext=(0, 3), textcoords="offset points",
                         ha='center', fontsize=6.5, fontweight='bold', color='#1D4ED8')

        t1 = "Modelo Vol-Targeting: Exposição Algorítmica a Ações vs VIX" if lang == 'pt' else "Vol-Targeting Allocation: Systematic Equity Exposure vs VIX"
        ax1.set_title(t1, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Alocação em Ações (%)" if lang == 'pt' else "Target Equity Allocation (%)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.0, color='#1E293B')
        ax1.set_ylim(10, 115)
        ax1.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True)

        # Subplot 2: Forced Selling in Billions
        colors_sell = ['#94A3B8', '#38BDF8', '#F59E0B', '#EF4444', '#7F1D1D']
        ax2.bar(x, forced_selling_billions, width=0.48, color=colors_sell, edgecolor='#1E293B')

        for i in range(len(vix_scenarios)):
            if i > 0:
                ax2.annotate(f"${forced_selling_billions[i]:.0f}B", xy=(x[i], forced_selling_billions[i]), xytext=(0, 3), textcoords="offset points",
                             ha='center', fontsize=6.8, fontweight='bold', color='#0F172A')

        t2 = "Volume Estimado de Venda Forçada Algorítmica em Big Techs (US$ Bi)" if lang == 'pt' else "Estimated Systematic Forced Selling Volume in Big Tech ($B)"
        ax2.set_title(t2, fontsize=8.8, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_ylabel("Volume de Liquidação Compulsória (US$ Bi)" if lang == 'pt' else "Forced Liquidation Volume ($B)", fontsize=8, color='#475569')
        ax2.set_xticks(x)
        ax2.set_xticklabels(x_labels, fontsize=6.0, color='#1E293B')
        ax2.set_ylim(0, 580)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_vol_targeting_deleveraging_cascade.png")
        plt.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  ✅ Saved: {out_path}")

def main():
    print("=" * 70)
    print("  GENERATING FEAR INDICES & VOLATILITY CHARTS (PT & EN)")
    print("=" * 70)
    generate_chart_1_vix_historical_spikes()
    generate_chart_2_dual_fear_index_vix_vs_move()
    generate_chart_3_vix_term_structure()
    generate_chart_4_vol_targeting_deleveraging()
    print("=" * 70)
    print("  🎉 All 4 bilingual Fear Indices charts successfully generated!")
    print("=" * 70)

if __name__ == "__main__":
    main()
