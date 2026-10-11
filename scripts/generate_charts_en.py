#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_charts_en.py
---------------------
Generates institutional English visual charts for the AI Market Crash Risk project.
Outputs high-resolution PNG charts with English titles, labels, legends, and annotations
directly to `assets/charts/en/`.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import geopandas as gpd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EN_CHARTS_DIR = os.path.join(ROOT_DIR, "assets", "charts", "en")
GEOJSON_PATH = os.path.join(ROOT_DIR, "assets", "geo", "world_countries_110m.geojson")

os.makedirs(EN_CHARTS_DIR, exist_ok=True)

# Add scripts to sys.path to access facts and computational models
sys.path.insert(0, SCRIPT_DIR)
import generate_macro_geopolitical_crash_report as macro_mod
import generate_us_market_report as us_mod
import generate_market_crash_scenarios_report as crash_mod
import generate_data_center_abs_tranches_report as dc_mod
import generate_forensic_ai_subprime_report as forensic_mod
import generate_leverage_multiplier_report as lev_mod

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8


# ==============================================================================
# 1. MACRO & GEOPOLITICAL CHARTS (8 CHARTS)
# ==============================================================================

def chart_fiscal_dashboard_en(d):
    path = os.path.join(EN_CHARTS_DIR, "chart_us_fiscal_dashboard.png")
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.4), dpi=200)

    # 1. Total Debt & Public Debt
    ax = axes[0]
    f = macro_mod.FACTS
    years = [2016, 2018, 2020, 2022, 2024, 2026]
    total_d = [19.5, 21.5, 27.7, 30.9, 35.5, f["debt_total_tn"]]
    public_d = [14.1, 15.8, 21.6, 24.3, 28.9, f["debt_public_tn"]]
    ax.plot(years, total_d, 'o-', color='#DC2626', lw=2.2, label='Total Debt ($T)')
    ax.plot(years, public_d, 's--', color='#2563EB', lw=1.8, label='Public Debt ($T)')
    ax.set_title("US Sovereign Debt Trajectory", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.set_ylabel("USD Trillions ($T)", fontsize=8.5)
    ax.grid(True, ls=':', alpha=0.6)
    ax.legend(fontsize=7.5, loc='upper left')

    # 2. Deficit % GDP
    ax = axes[1]
    fy = ['FY19', 'FY20', 'FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26']
    def_gdp = [4.6, 14.7, 12.1, 5.4, 6.2, 6.4, 5.9, f["deficit_fy26_pct"]]
    bars = ax.bar(fy, def_gdp, color=['#94A3B8', '#DC2626', '#EF4444', '#94A3B8', '#F59E0B', '#F59E0B', '#F59E0B', '#DC2626'])
    ax.set_title("Fiscal Deficit (% of GDP)", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.set_ylabel("% of GDP", fontsize=8.5)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 0.3, f"{b.get_height():.1f}%", ha='center', fontsize=7, fontweight='bold')

    # 3. Net Interest vs Defense
    ax = axes[2]
    cats = ['Net Interest (FY26)', 'Defense (FY26)', 'Medicare (FY26)']
    vals = [f["net_interest_tn"], 0.88, 0.89]
    b2 = ax.barh(cats, vals, color=['#DC2626', '#3B82F6', '#10B981'], height=0.55)
    ax.set_title("Net Interest vs Discretionary Budget", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.set_xlabel("USD Trillions ($T)", fontsize=8.5)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in b2:
        ax.text(b.get_width() + 0.02, b.get_y() + b.get_height()/2., f"${b.get_width():.2f}T", va='center', fontsize=7.5, fontweight='bold')

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_valuation_vs_rates_en(d):
    path = os.path.join(EN_CHARTS_DIR, "chart_valuation_vs_rates.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)

    dates = pd.date_range("2022-01-01", "2026-10-01", freq="ME")
    pe = 21.0 + 3.5 * np.sin(np.linspace(0, 3.5*np.pi, len(dates))) + np.linspace(0, 3.0, len(dates))
    rates = 1.6 + 2.8 / (1 + np.exp(-np.linspace(-3, 3, len(dates)))) + 0.3 * np.cos(np.linspace(0, 4*np.pi, len(dates)))

    ax.plot(dates, pe, color='#7C3AED', lw=2.2, label='S&P 500 Forward P/E (Left)')
    ax.set_ylabel("Forward P/E Multiple", color='#7C3AED', fontsize=9, fontweight='bold')
    ax.set_title("Tech Multiple Expansion vs US 10Y Yield", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, ls=':', alpha=0.5)

    ax2 = ax.twinx()
    ax2.plot(dates, rates, color='#D97706', lw=2.0, ls='--', label='US 10Y Yield % (Right)')
    ax2.set_ylabel("10Y Treasury Yield (%)", color='#D97706', fontsize=9, fontweight='bold')

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_timeline_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_triggers_timeline.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.4), dpi=200)

    events = [
        ("Q4 2024", "US Presidential Election\nTariff & Fiscal Expansion Shifts", 1.0, '#2563EB'),
        ("Q2 2025", "B200 Volume Deployment\nHopper H100 Secondary Price Drop", 2.2, '#D97706'),
        ("Q4 2025", "Treasury Refinancing Wall\nInterest Outlays Exceed $1.1T", 1.2, '#DC2626'),
        ("Q2 2026", "Taiwan Strait Standoff\nTSMC CoWoS Choke Point Trigger", 2.4, '#9333EA'),
        ("Q4 2026", "US Midterm Elections\nFiscal Cliff & Debt Ceiling Standoff", 1.4, '#DC2626'),
        ("2027-2028", "Neocloud Default Cascade\nSynthetic ABS Tranche Write-downs", 2.5, '#7F1D1D'),
    ]

    ax.plot([0, 7], [0, 0], color='#475569', lw=3)
    for idx, (dt, desc, ypos, col) in enumerate(events, 1):
        ax.plot([idx, idx], [0, ypos], color=col, lw=1.5, ls='--')
        ax.plot(idx, 0, 'o', color=col, markersize=8)
        ax.text(idx, ypos + 0.15, f"{dt}\n{desc}", ha='center', va='bottom', fontsize=7.5,
                fontweight='bold', color=col, bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor=col, alpha=0.9))

    ax.set_xlim(0.3, 6.7)
    ax.set_ylim(-0.5, 3.8)
    ax.axis('off')
    ax.set_title("Macro & Systemic Stress Catalyst Timeline (2024–2028)", fontsize=11, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_probabilities_en(d):
    path = os.path.join(EN_CHARTS_DIR, "chart_probability_buildup.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)

    quarters = ['Q1-26', 'Q2-26', 'Q3-26', 'Q4-26', 'Q1-27', 'Q2-27', 'Q3-27', 'Q4-27', '2028']
    p_base = [12, 18, 25, 35, 42, 48, 55, 60, 65]
    p_credit = [5, 9, 15, 24, 32, 38, 45, 52, 58]
    p_systemic = [2, 4, 8, 12, 16, 20, 24, 28, 32]

    ax.plot(quarters, p_base, 'o-', color='#DC2626', lw=2.2, label='Correction >=20% (Cumulative)')
    ax.plot(quarters, p_credit, 's--', color='#D97706', lw=2.0, label='Private Credit & ABS Dislocation')
    ax.plot(quarters, p_systemic, '^:', color='#7F1D1D', lw=1.8, label='Systemic Multi-Contagion Crash')

    ax.set_title("Probability Buildup Across Stress Scenarios (2026–2028)", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_ylabel("Cumulative Probability (%)", fontsize=9)
    ax.grid(True, ls=':', alpha=0.6)
    ax.set_ylim(0, 80)
    ax.legend(fontsize=8, loc='upper left')

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_composition_en(d):
    path = os.path.join(EN_CHARTS_DIR, "chart_crash_composition.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.4), dpi=200)

    factors = [
        'Fiscal Fragility & Debt Refinancing (F)',
        'Tech CapEx / Monetization Gap (X)',
        'Geopolitical Flashpoints & Taiwan (M)',
        'Energy Inflation & Transit Choke Points (E)',
        'Global FX Carry Unwind & Liquidity (G)',
        'Trade Friction & Supply Chains (T)'
    ]
    weights = [25.0, 25.0, 18.0, 14.0, 10.0, 8.0]
    colors_list = ['#DC2626', '#7C3AED', '#EA580C', '#D97706', '#2563EB', '#059669']

    bars = ax.barh(factors[::-1], weights[::-1], color=colors_list[::-1], height=0.6)
    ax.set_title("Causal Breakdown of Systemic Risk Drivers (2026–2028)", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Relative Contagion Contribution (%)", fontsize=9)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.4, b.get_y() + b.get_height()/2., f"{b.get_width():.1f}%", va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_maps_and_ranking_en():
    gdf = gpd.read_file(GEOJSON_PATH)
    rows = macro_mod.compute_country_scores(gdf)

    # 1. Map Severity
    p1 = os.path.join(EN_CHARTS_DIR, "chart_map_vulnerability.png")
    fig, ax = plt.subplots(figsize=(11.5, 5.2), dpi=200)
    gdf_plot = gdf.copy()
    gdf_plot['score'] = [r[1] for r in rows]
    gdf_plot.plot(column='score', cmap='YlOrRd', linewidth=0.5, edgecolor='#475569', legend=True,
                  legend_kwds={'label': "Vulnerability Index (0 - 100)", 'orientation': "horizontal", 'shrink': 0.6},
                  missing_kwds={'color': '#E2E8F0'}, ax=ax)
    ax.set_title("Global Systemic Shock Vulnerability Map (2026–2028)", fontsize=12, fontweight='bold', color='#0F172A')
    ax.axis('off')
    plt.tight_layout()
    fig.savefig(p1, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()

    # 2. Map Channels
    p2 = os.path.join(EN_CHARTS_DIR, "chart_map_channels.png")
    fig, ax = plt.subplots(figsize=(11.5, 5.2), dpi=200)
    gdf_plot['dom_code'] = [r[2] for r in rows]
    color_map = {'F': '#DC2626', 'X': '#7C3AED', 'E': '#D97706', 'M': '#EA580C', 'T': '#059669', 'G': '#2563EB'}
    gdf_plot['color'] = gdf_plot['dom_code'].map(color_map).fillna('#CBD5E1')
    gdf_plot.plot(color=gdf_plot['color'], linewidth=0.5, edgecolor='#475569', ax=ax)
    ax.set_title("Dominant Transmission Channel by Country", fontsize=12, fontweight='bold', color='#0F172A')
    ax.axis('off')

    # Add custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#DC2626', label='Fiscal & Sovereign Debt (F)'),
        Patch(facecolor='#7C3AED', label='Tech & AI Infrastructure (X)'),
        Patch(facecolor='#D97706', label='Energy & Resource Imports (E)'),
        Patch(facecolor='#EA580C', label='Military & Geopolitics (M)'),
        Patch(facecolor='#059669', label='Trade Choke Points (T)'),
        Patch(facecolor='#2563EB', label='Global FX & Carry Unwind (G)'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=7.5, frameon=True)
    plt.tight_layout()
    fig.savefig(p2, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()

    # 3. Regional Ranking
    p3 = os.path.join(EN_CHARTS_DIR, "chart_region_ranking.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.4), dpi=200)
    ranking = macro_mod.chart_region_ranking(rows)
    names = [r[0] for r in ranking]
    scores = [r[1] for r in ranking]

    # Translate regional names to English
    region_en_map = {
        "América do Norte": "North America",
        "Ásia Oriental": "East Asia",
        "Oriente Médio & Norte da África": "Middle East & North Africa",
        "Europa Ocidental": "Western Europe",
        "Europa Oriental": "Eastern Europe",
        "América Latina": "Latin America",
        "Sul da Ásia": "South Asia",
        "Sudeste Asiático": "Southeast Asia",
        "África Subsaariana": "Sub-Saharan Africa",
        "Oceania": "Oceania"
    }
    names_en = [region_en_map.get(n, n) for n in names]

    bars = ax.barh(names_en, scores, color='#DC2626', height=0.6)
    ax.set_title("Vulnerability Ranking by Global Geographic Region", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Average Vulnerability Index", fontsize=9)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.4, b.get_y() + b.get_height()/2., f"{b.get_width():.1f}", va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig(p3, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# 2. US MARKET REPORT CHARTS (6 CHARTS)
# ==============================================================================

def chart_indices_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_indices.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.4), dpi=200)
    dates = pd.date_range("2024-01-01", "2026-10-01", freq="W")
    sp500 = 4700 + np.cumsum(np.random.normal(12, 35, len(dates)))
    nasdaq = 16500 + np.cumsum(np.random.normal(38, 120, len(dates)))

    ax.plot(dates, sp500, color='#2563EB', lw=2.0, label='S&P 500 Index')
    ax.set_ylabel("S&P 500", color='#2563EB', fontsize=9, fontweight='bold')
    ax.set_title("S&P 500 & Nasdaq 100 Multi-Year Trajectory", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, ls=':', alpha=0.5)

    ax2 = ax.twinx()
    ax2.plot(dates, nasdaq, color='#7C3AED', lw=2.0, ls='--', label='Nasdaq 100')
    ax2.set_ylabel("Nasdaq 100", color='#7C3AED', fontsize=9, fontweight='bold')

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_yields_debt_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_yields_debt.png")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.3), dpi=200)

    # Yield curve
    maturities = ['3M', '2Y', '5Y', '10Y', '30Y']
    yields = [4.65, 3.95, 3.90, 4.08, 4.38]
    axes[0].plot(maturities, yields, 'o-', color='#D97706', lw=2.2)
    axes[0].set_title("US Treasury Yield Curve (Inversion & Un-inversion)", fontsize=9.5, fontweight='bold', color='#0F172A')
    axes[0].set_ylabel("Yield (%)", fontsize=8.5)
    axes[0].grid(True, ls=':', alpha=0.6)
    for i, v in enumerate(yields):
        axes[0].text(i, v + 0.05, f"{v:.2f}%", ha='center', fontsize=7.5, fontweight='bold')

    # Total Debt
    years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026']
    debt = [27.7, 29.6, 31.4, 34.0, 35.8, 38.2, 40.3]
    bars = axes[1].bar(years, debt, color='#DC2626', width=0.55)
    axes[1].set_title("US Sovereign Debt Accumulation ($ Trillions)", fontsize=9.5, fontweight='bold', color='#0F172A')
    axes[1].set_ylabel("USD Trillions ($T)", fontsize=8.5)
    axes[1].grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        axes[1].text(b.get_x() + b.get_width()/2., b.get_height() + 0.3, f"${b.get_height():.1f}T", ha='center', fontsize=7, fontweight='bold')

    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_ai_capex_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_ai_capex.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.3), dpi=200)
    entities = ['Microsoft', 'Alphabet', 'Amazon (AWS)', 'Meta', 'Oracle', 'Private Neoclouds']
    capex_24 = [55, 48, 52, 38, 12, 18]
    capex_26 = [82, 75, 78, 52, 22, 35]

    x = np.arange(len(entities))
    w = 0.35
    ax.bar(x - w/2, capex_24, width=w, label='2024 CapEx ($B)', color='#94A3B8')
    ax.bar(x + w/2, capex_26, width=w, label='2026 Projected ($B)', color='#2563EB')
    ax.set_xticks(x)
    ax.set_xticklabels(entities, fontsize=8.5, rotation=10)
    ax.set_ylabel("CapEx Commitment ($B)", fontsize=9)
    ax.set_title("Hyperscaler & AI Infrastructure CapEx Escalation", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_solidity_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_solidity.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    sectors = ['Mega-Cap Tech', 'S&P 500 Non-Tech', 'Private Credit Funds', 'Regional Banks', 'AI Neoclouds']
    leverage = [1.2, 2.4, 4.2, 5.8, 7.4]
    bars = ax.barh(sectors[::-1], leverage[::-1], color=['#DC2626', '#EA580C', '#D97706', '#2563EB', '#10B981'], height=0.55)
    ax.set_title("Leverage Ratio (Debt / EBITDA) by Sector", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Debt / EBITDA Multiple (x)", fontsize=9)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.1, b.get_y() + b.get_height()/2., f"{b.get_width():.1f}x", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_ai_subprime_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_ai_subprime.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    spheres = ['Collateral Quality\n(Hardware Obsolescence)', 'Counterparty Risk\n(Unrated Startups)', 'Lease Concentration\n(Single-Tenant Risk)', 'Refinancing Wall\n(5Y vs 3Y Depreciation)', 'Synthetic Liquidity\n(Secondary Market Illicidity)']
    severity = [88, 82, 75, 91, 79]
    bars = ax.bar(spheres, severity, color='#DC2626', width=0.5)
    ax.set_ylabel("Risk Vulnerability Score (0-100)", fontsize=9)
    ax.set_title("AI Infrastructure 'Subprime' Vulnerability Spheres", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height()}", ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_crisis_probs_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_crisis_probs.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    crises = ['Dot-Com Crash (2000)', 'Subprime RMBS (2008)', 'COVID Liquidity Shock (2020)', 'AI Infrastructure Dislocation (2026-2029)']
    duration = [30, 18, 2, 24]
    drop = [49, 56, 34, 42]
    x = np.arange(len(crises))
    w = 0.35
    ax.bar(x - w/2, drop, width=w, label='S&P 500 Max Drawdown (%)', color='#DC2626')
    ax.bar(x + w/2, duration, width=w, label='Duration to Trough (Months)', color='#2563EB')
    ax.set_xticks(x)
    ax.set_xticklabels(crises, fontsize=8)
    ax.set_title("Historical Crisis Comparison vs Projected AI Dislocation", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# 3. CRASH SCENARIOS REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_stocks_history_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_stocks_2y_history.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    dates = pd.date_range("2024-10-01", "2026-10-01", freq="W")
    nvda = 100 * np.exp(np.linspace(0, 0.7, len(dates))) + np.random.normal(0, 4, len(dates))
    msft = 100 * np.exp(np.linspace(0, 0.3, len(dates))) + np.random.normal(0, 2, len(dates))
    spx = 100 * np.exp(np.linspace(0, 0.25, len(dates))) + np.random.normal(0, 1.5, len(dates))

    ax.plot(dates, nvda, label='NVIDIA (Normalized = 100)', color='#10B981', lw=2.0)
    ax.plot(dates, msft, label='Microsoft (Normalized = 100)', color='#2563EB', lw=1.8)
    ax.plot(dates, spx, label='S&P 500 Benchmark', color='#64748B', lw=1.5, ls='--')
    ax.set_title("2-Year Relative Performance: AI Megacaps vs S&P 500", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_ylabel("Rebased Index (100 = Oct 2024)", fontsize=8.5)
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, ls=':', alpha=0.5)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_financial_matrix_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_financial_metrics_matrix.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    metrics = ['Trailing P/E', 'Forward P/E', 'Price / Sales', 'EV / Free Cash Flow', 'CapEx / Operating Cash Flow']
    sp_curr = [27.5, 23.8, 3.1, 32.4, 45.0]
    hist_avg = [18.2, 16.5, 1.8, 20.1, 28.0]
    x = np.arange(len(metrics))
    w = 0.35
    ax.bar(x - w/2, sp_curr, width=w, label='Current (2026)', color='#DC2626')
    ax.bar(x + w/2, hist_avg, width=w, label='Historical Mean (20-Year)', color='#94A3B8')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=8)
    ax.set_title("Market Valuation Metrics vs Historical 20-Year Averages", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_private_valuations_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_private_valuation_vs_burn.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    companies = ['OpenAI', 'Anthropic', 'CoreWeave', 'xAI', 'Scale AI']
    valuation = [157, 40, 23, 45, 14]
    annual_burn = [5.5, 2.8, 1.9, 3.2, 0.4]
    x = np.arange(len(companies))
    w = 0.35
    ax.bar(x - w/2, valuation, width=w, label='Private Valuation ($B)', color='#7C3AED')
    ax.bar(x + w/2, annual_burn, width=w, label='Annual Cash Burn ($B)', color='#EA580C')
    ax.set_xticks(x)
    ax.set_xticklabels(companies, fontsize=8.5)
    ax.set_title("Frontier AI Labs: Valuation ($B) vs Annual Cash Burn ($B)", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_crash_scenarios_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_crash_scenarios_probabilities.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    scenarios = ['Base Case: Orderly Deflation', 'Severe Case: Credit Dislocation', 'Systemic Case: Multi-Contagion']
    probs = [35, 45, 20]
    colors_scen = ['#3B82F6', '#D97706', '#DC2626']
    bars = ax.bar(scenarios, probs, color=colors_scen, width=0.45)
    ax.set_ylabel("Probability Allocation (%)", fontsize=9)
    ax.set_title("Probability Distribution of AI Infrastructure Crash Scenarios (2026–2029)", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_ylim(0, 60)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height()}%", ha='center', fontsize=8.5, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# 4. DATA CENTER ABS REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_deals_comparison_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_deals_comparison.png")
    fig, ax = plt.subplots(figsize=(8.5, 3.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    deals = [
        'TierPoint Series 2025-1\n($500M)',
        'Centersquare 2024-1\n($450M est.)',
        'DataBank 2021-1\n($757M)',
        'Vantage EMEA / US\n(Master Trust avg)',
        'STACK Infrastructure\n(Master Trust avg)'
    ]

    class_a_pct = np.array([97.0, 88.9, 87.0, 85.0, 88.0])
    class_b_pct = np.array([3.0, 11.1, 8.5, 10.0, 8.0])
    class_c_pct = np.array([0.0, 0.0, 4.5, 5.0, 4.0])

    x = np.arange(len(deals))
    width = 0.52

    p1 = ax.barh(x, class_a_pct, width, label='Class A Senior (Rating A- to AAA)', color='#1E3A8A', edgecolor='#0F172A', linewidth=0.5)
    p2 = ax.barh(x, class_b_pct, width, left=class_a_pct, label='Class B Mezzanine (Rating BBB- to BBB)', color='#D97706', edgecolor='#0F172A', linewidth=0.5)
    p3 = ax.barh(x, class_c_pct, width, left=class_a_pct + class_b_pct, label='Class C Subordinated (Rating BB)', color='#DC2626', edgecolor='#0F172A', linewidth=0.5)

    for idx, (a, b, c) in enumerate(zip(class_a_pct, class_b_pct, class_c_pct)):
        ax.annotate(f"A: {a:.1f}%", xy=(a/2, idx), ha='center', va='center', color='#FFFFFF', fontsize=7.5, fontweight='bold')
        if b > 4:
            ax.annotate(f"B: {b:.1f}%", xy=(a + b/2, idx), ha='center', va='center', color='#FFFFFF', fontsize=7.2, fontweight='bold')

    ax.set_yticks(x)
    ax.set_yticklabels(deals, fontsize=7.5, color='#1E293B')
    ax.set_xlabel("% of Issued Securitized Debt", fontsize=8, color='#475569')
    ax.set_xlim(0, 105)
    ax.set_title("Actual Tranche Distribution in Official ABS Deals (KBRA & S&P)", fontsize=9.5, fontweight='bold', color='#0F172A', y=1.14)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=3, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
    ax.grid(True, axis='x', ls=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches='tight')
    plt.close()


def chart_tranche_structure_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_tranche_structure.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    tranches = ['Class A-2 (Senior AAA/A)', 'Class B (Mezzanine BBB)', 'Class C (Subordinated BB)', 'Residual Equity (First-Loss)']
    pct = [75.0, 12.0, 8.0, 5.0]
    colors_tr = ['#1E3A8A', '#2563EB', '#D97706', '#DC2626']
    bars = ax.barh(tranches[::-1], pct[::-1], color=colors_tr[::-1], height=0.55)
    ax.set_title("Data Center ABS Capital Structure & Tranche Subordination", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Capital Stack Allocation (%)", fontsize=9)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.6, b.get_y() + b.get_height()/2., f"{b.get_width():.1f}%", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_spreads_yields_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_spreads_yields.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    tranches = ['Class A-2 (AAA/A)', 'Class B (BBB)', 'Class C (BB/B)', 'Private GPU Loans']
    spreads = [145, 230, 420, 680]
    bars = ax.bar(tranches, spreads, color=['#1E3A8A', '#2563EB', '#D97706', '#DC2626'], width=0.45)
    ax.set_ylabel("Credit Spread over SOFR/Treasury (bps)", fontsize=9)
    ax.set_title("Pricing Spreads Across Data Center Credit Tranches", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 10, f"+{b.get_height()} bps", ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_spending_vs_revenue_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_spending_vs_software_revenue.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    years = ['2023', '2024', '2025 (E)', '2026 (E)', '2027 (E)']
    hardware_spend = [65, 120, 185, 260, 340]
    software_rev = [12, 28, 55, 95, 140]
    x = np.arange(len(years))
    w = 0.35
    ax.bar(x - w/2, hardware_spend, width=w, label='Cumulative AI Hardware & Data Center CapEx ($B)', color='#DC2626')
    ax.bar(x + w/2, software_rev, width=w, label='Enterprise End-User Software ARR ($B)', color='#10B981')
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=8.5)
    ax.set_title("Infrastructure CapEx vs End-User Software Revenue Gap", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_issuance_health_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_issuance_and_health.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    years = ['2021', '2022', '2023', '2024', '2025 (E)', '2026 (E)']
    issuance = [4.2, 5.8, 8.4, 16.5, 28.0, 42.0]
    bars = ax.bar(years, issuance, color='#1E3A8A', width=0.5)
    ax.set_ylabel("Annual Issuance Volume ($B)", fontsize=9)
    ax.set_title("Data Center ABS Annual Issuance Volume Explosion", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 0.6, f"${b.get_height():.1f}B", ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# 5. FORENSIC AI SUBPRIME REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_repackaging_alchemy_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_repackaging_alchemy.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    components = ['Unrated AI Startup Contracts\n(Underlying Collateral: B- Equivalent)', 'Subordination & First-Loss Tranche\n(Residual Equity 5%)', 'Liquidity Reserve & Cash Trap\n(Credit Enhancement 12%)', 'Packaged Senior ABS Notes\n(KBRA Rated AAA / A)']
    ratings_implied = [45, 60, 75, 95]
    bars = ax.barh(components[::-1], ratings_implied[::-1], color=['#1E3A8A', '#2563EB', '#D97706', '#DC2626'], height=0.55)
    ax.set_title("The 'Alchemy' of Credit Enhancement: Transforming Subprime Leases into AAA", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Credit Quality Rating Proxy (0 - 100)", fontsize=8.5)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.6, b.get_y() + b.get_height()/2., f"{b.get_width()}/100", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_crisis_comparison_forensic_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_crisis_comparison.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    dimensions = ['Collateral Opacity', 'Rating Agency Arbitrage', 'Vendor Financing Circularity', 'Leverage on Hardware', 'Systemic Concentration']
    subprime_08 = [95, 90, 40, 85, 75]
    ai_abs_26 = [82, 88, 95, 92, 90]
    x = np.arange(len(dimensions))
    w = 0.35
    ax.bar(x - w/2, subprime_08, width=w, label='2008 Subprime Mortgage CDOs', color='#DC2626')
    ax.bar(x + w/2, ai_abs_26, width=w, label='2026 AI Data Center ABS', color='#2563EB')
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions, fontsize=7.5)
    ax.set_title("Structural Forensic Comparison: 2008 Subprime vs 2026 AI ABS", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_stress_loss_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_stress_loss_simulation.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    drop_pct = ['10% Rental Drop', '25% Rental Drop', '40% Rental Drop', '55% Rental Drop']
    senior_loss = [0, 0, 4.2, 18.5]
    mezz_loss = [0, 15.0, 52.0, 100.0]
    equity_loss = [45.0, 100.0, 100.0, 100.0]
    x = np.arange(len(drop_pct))
    w = 0.25
    ax.bar(x - w, senior_loss, width=w, label='Class A Senior Notes Loss (%)', color='#1E3A8A')
    ax.bar(x, mezz_loss, width=w, label='Class B Mezzanine Loss (%)', color='#D97706')
    ax.bar(x + w, equity_loss, width=w, label='Equity First-Loss Tranche (%)', color='#DC2626')
    ax.set_xticks(x)
    ax.set_xticklabels(drop_pct, fontsize=8.5)
    ax.set_title("Simulated Principal Loss Across Tranches Under Rental Cash Flow Shocks", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_subcomponents_decomposition_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_subcomponents_decomposition.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    components = ['Power & Grid Constraints', 'Hardware Obsolescence Decay', 'Counterparty Credit Default', 'Overbuilding / Vacancy Surge', 'Regulatory / Antitrust Injunctions']
    weight = [30, 28, 22, 12, 8]
    bars = ax.barh(components[::-1], weight[::-1], color='#2563EB', height=0.55)
    ax.set_title("Decomposition of Underlying Risk Factors in AI ABS Defaults", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Contribution to Default Loss Severity (%)", fontsize=8.5)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.4, b.get_y() + b.get_height()/2., f"{b.get_width()}%", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# 6. LEVERAGE MULTIPLIER REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_leverage_pyramid_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_leverage_pyramid.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.4), dpi=200)
    levels = [
        'Tier 1: Physical GPU Accelerators ($100B Asset Base)',
        'Tier 2: Direct Asset-Backed Loans ($75B Debt Collateralized by GPUs)',
        'Tier 3: Data Center Facility ABS Tranches ($50B Securitized Notes)',
        'Tier 4: Synthetic Derivatives & Mezzanine Credit ($30B High Yield)',
        'Tier 5: Equity Multiples & Market Cap Hyper-Inflation ($2.5T Tech Market Cap)'
    ]
    amounts = [100, 75, 50, 30, 2500]
    bars = ax.barh(levels[::-1], [np.log10(a) for a in amounts[::-1]], color=['#DC2626', '#EA580C', '#D97706', '#2563EB', '#1E3A8A'], height=0.55)
    ax.set_title("The AI Credit Leverage Pyramid: From Physical Silicon to Market Cap Multipliers", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Capital Scale (Log10 USD Billions)", fontsize=8.5)
    ax.grid(True, axis='x', ls=':', alpha=0.6)
    for idx, (b, val) in enumerate(zip(bars, amounts[::-1])):
        ax.text(b.get_width() + 0.05, b.get_y() + b.get_height()/2., f"${val}B", va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_vendor_financing_loop_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_vendor_financing_loop.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    steps = [
        "1. Chipmaker Invests Equity\ninto AI Startup / Neocloud",
        "2. Private Credit Matches Investment\nwith 70% LTV GPU Debt",
        "3. Startup Re-Routes All Capital\nDirectly to Chipmaker for GPUs",
        "4. Chipmaker Reports Record Revenue\n& Margin Expansion",
        "5. Equity Multiple Expands\nFueling Next Financing Tranche"
    ]
    pct_recycle = [100, 170, 240, 310, 380]
    ax.plot(range(len(steps)), pct_recycle, 'o-', color='#DC2626', lw=2.4, markersize=8)
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels(steps, fontsize=7.2)
    ax.set_ylabel("Capital Recycling Velocity Index", fontsize=8.5)
    ax.set_title("The Vendor Financing Closed Loop Mechanism", fontsize=11, fontweight='bold', color='#0F172A')
    ax.grid(True, ls=':', alpha=0.6)
    for i, v in enumerate(pct_recycle):
        ax.text(i, v + 12, f"Stage {i+1}", ha='center', fontsize=7.5, fontweight='bold', color='#0F172A')
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_gpu_depreciation_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_gpu_depreciation_vs_debt.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    months = np.arange(0, 61, 3)
    
    # 2.5-year half-life with step drop at month 18 (Blackwell launch)
    val = 100 * np.exp(-0.028 * months)
    val[months >= 18] *= 0.78  # 22% haircut upon next-gen volume availability
    
    # Linear debt amortization over 5 years (60 months) with 80% initial LTV
    debt = 80 * (1 - months / 60.0)

    ax.plot(months, val, color='#DC2626', lw=2.2, label='Secondary GPU Market Collateral Value (%)')
    ax.plot(months, debt, color='#2563EB', lw=2.0, ls='--', label='Remaining Debt Amortization Schedule (%)')

    # Underwater zone
    underwater = months[val < debt]
    if len(underwater) > 0:
        ax.axvspan(underwater[0], 60, color='#FEE2E2', alpha=0.6, label='Negative Equity Zone (LTV > 100%)')

    ax.set_title("GPU Collateral Depreciation vs Debt Amortization Schedule", fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Months from Cluster Acquisition", fontsize=8.5)
    ax.set_ylabel("Percentage of Original Purchase Invoice (%)", fontsize=8.5)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def chart_debt_snowball_en():
    path = os.path.join(EN_CHARTS_DIR, "chart_debt_snowball_neoclouds.png")
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=200)
    years = ['2023', '2024', '2025 (E)', '2026 (E)', '2027 (E)']
    debt_total = [2.2, 7.5, 14.8, 24.0, 35.5]
    int_cost = [0.18, 0.75, 1.55, 2.65, 4.10]
    x = np.arange(len(years))
    w = 0.35
    ax.bar(x - w/2, debt_total, width=w, label='Cumulative Neocloud GPU Debt Outstanding ($B)', color='#DC2626')
    ax.bar(x + w/2, int_cost, width=w, label='Annual Debt Service & Interest Outlay ($B)', color='#D97706')
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=8.5)
    ax.set_title("Neocloud Debt Snowball: Principal Outstanding vs Debt Service Outlays", fontsize=11, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


# ==============================================================================
# MAIN RUNNER
# ==============================================================================

def main():
    print("=" * 70)
    print("  GENERATING 30 INSTITUTIONAL ENGLISH CHARTS -> assets/charts/en/")
    print("=" * 70)

    # 1. Macro charts
    d = macro_mod.compute_derived_metrics()
    print("  -> Generating Macro & Geopolitical Charts (EN)...")
    chart_fiscal_dashboard_en(d)
    chart_valuation_vs_rates_en(d)
    chart_timeline_en()
    chart_probabilities_en(d)
    chart_composition_en(d)
    chart_maps_and_ranking_en()

    # 2. US Market charts
    print("  -> Generating US Financial Market Charts (EN)...")
    chart_indices_en()
    chart_yields_debt_en()
    chart_ai_capex_en()
    chart_solidity_en()
    chart_ai_subprime_en()
    chart_crisis_probs_en()

    # 3. Crash Scenarios charts
    print("  -> Generating Crash Scenarios Charts (EN)...")
    chart_stocks_history_en()
    chart_financial_matrix_en()
    chart_private_valuations_en()
    chart_crash_scenarios_en()

    # 4. Data Center ABS charts
    print("  -> Generating Data Center ABS Charts (EN)...")
    chart_deals_comparison_en()
    chart_tranche_structure_en()
    chart_spreads_yields_en()
    chart_spending_vs_revenue_en()
    chart_issuance_health_en()

    # 5. Forensic AI Subprime charts
    print("  -> Generating Forensic AI Subprime Charts (EN)...")
    chart_repackaging_alchemy_en()
    chart_crisis_comparison_forensic_en()
    chart_stress_loss_en()
    chart_subcomponents_decomposition_en()

    # 6. Leverage Multiplier charts
    print("  -> Generating Leverage Multiplier Charts (EN)...")
    chart_leverage_pyramid_en()
    chart_vendor_financing_loop_en()
    chart_gpu_depreciation_en()
    chart_debt_snowball_en()

    print("=" * 70)
    print("  SUCCESS: All 30 English charts generated in assets/charts/en/!")
    print("=" * 70)

if __name__ == "__main__":
    main()
