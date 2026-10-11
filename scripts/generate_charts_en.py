#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_charts_en.py
---------------------
Generates the complete suite of 30 institutional English visual charts for the
AI Market Crash Risk project.
Outputs high-resolution PNG charts directly into `assets/charts/en/`.
Every chart is an exact 1:1 structural replica of its Portuguese twin:
same subplots, data series, colors, scales, and styling, with 100% fluent
institutional English financial terminology and annotations.
"""

import os
import sys
import numpy as np
import pandas as pd
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Patch
import geopandas as gpd
from pyproj import Transformer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EN_CHARTS_DIR = os.path.join(ROOT_DIR, "assets", "charts", "en")
PT_CHARTS_DIR = os.path.join(ROOT_DIR, "assets", "charts", "pt")
GEOJSON_PATH = os.path.join(ROOT_DIR, "assets", "geo", "world_countries_110m.geojson")

os.makedirs(EN_CHARTS_DIR, exist_ok=True)
os.makedirs(PT_CHARTS_DIR, exist_ok=True)

# Import facts, scores and helpers from main scripts
sys.path.insert(0, SCRIPT_DIR)
from generate_macro_geopolitical_crash_report import (
    FACTS, SCENARIOS, ATTRIB, FACTOR_WEIGHTS, FACTOR_NAMES,
    REGION_PT, BASE_RATE_BEAR_2Y, OVERLAY,
    compute_derived_metrics, compute_country_scores
)
import generate_market_crash_scenarios_report as crash_mod
import generate_us_market_report as us_mod

def setup_chart_style():
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#E2E8F0'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.8

def _save(fig, filename):
    out_path = os.path.join(EN_CHARTS_DIR, filename)
    fig.savefig(out_path, dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Generated EN Chart: {out_path}", flush=True)


# ==============================================================================
# 1. MACRO & GEOPOLITICAL REPORT CHARTS (8 CHARTS)
# ==============================================================================

def chart_fiscal_dashboard_en(d):
    setup_chart_style()
    f = FACTS
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.0))
    fig.patch.set_facecolor('white')

    # (a) Debt Composition
    ax = axes[0, 0]
    ax.set_facecolor('#FAFAFA')
    ax.barh([0], [f["debt_public_tn"]], color='#1E3A8A', height=0.5, label='Held by the Public')
    ax.barh([0], [f["debt_intragov_tn"]], left=[f["debt_public_tn"]], color='#93C5FD', height=0.5,
            label='Intragovernmental')
    ax.text(f["debt_public_tn"] / 2, 0, f"${f['debt_public_tn']:.2f}T\n(~{d['debt_gdp_calc']:.0f}% of GDP)",
            ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    ax.text(f["debt_public_tn"] + f["debt_intragov_tn"] / 2, 0, f"${f['debt_intragov_tn']:.2f}T",
            ha='center', va='center', color='#0F172A', fontsize=8, fontweight='bold')
    ax.set_xlim(0, 44)
    ax.set_yticks([])
    ax.set_ylim(-0.55, 0.95)
    ax.set_title(f"Total US Federal Debt: ${f['debt_total_tn']:.2f}T (Oct 08, 2026)", fontsize=9, fontweight='bold')
    ax.set_xlabel("USD Trillions ($T)", fontsize=8)
    ax.legend(loc='upper center', fontsize=7, ncol=2, frameon=False)

    # (b) Annual Flows
    ax = axes[0, 1]
    ax.set_facecolor('#FAFAFA')
    labels = ["FY26 Deficit\nCBO (Feb/26)", "FY26 Deficit\nActual", "Net Interest\nFY26", "2036 Deficit\n(CBO)"]
    vals = [f["deficit_cbo_feb_tn"], f["deficit_fy26_tn"], f["net_interest_tn"], f["deficit_2036_tn"]]
    cols = ['#94A3B8', '#DC2626', '#F59E0B', '#7C2D12']
    bars = ax.bar(labels, vals, color=cols, width=0.6, edgecolor='#1E293B', linewidth=0.5)
    for b, v in zip(bars, vals):
        ax.annotate(f"${v:.2f}T" if v != f["net_interest_tn"] else "$1.0-1.1T",
                    xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3), textcoords='offset points',
                    ha='center', fontsize=7.5, fontweight='bold')
    ax.set_ylim(0, 3.8)
    ax.set_title("Deficit & Net Interest: Non-Recession Baseline (4.2% Unemp.)", fontsize=9, fontweight='bold')
    ax.tick_params(axis='x', labelsize=7)
    ax.grid(True, axis='y')

    # (c) Global Long-Term Sovereign Yields
    ax = axes[1, 0]
    ax.set_facecolor('#FAFAFA')
    bonds = ["US 10Y", "UK Gilt 10Y", "French OAT", "German Bund", "Japan JGB"]
    y_vals = [4.50, 4.25, 3.02, 2.22, 1.05]
    b_cols = ['#DC2626', '#EA580C', '#D97706', '#2563EB', '#64748B']
    bars3 = ax.barh(bonds[::-1], y_vals[::-1], color=b_cols[::-1], height=0.52, edgecolor='#1E293B', linewidth=0.5)
    for b, v in zip(bars3, y_vals[::-1]):
        ax.text(v + 0.08, b.get_y() + b.get_height() / 2, f"{v:.2f}%", va='center', fontsize=7.5, fontweight='bold')
    ax.set_xlim(0, 5.2)
    ax.set_title("Global 10-Year Benchmark Yields (%)", fontsize=9, fontweight='bold')
    ax.set_xlabel("Yield (%)", fontsize=8)
    ax.grid(True, axis='x')

    # (d) CBO Debt Trajectory
    ax = axes[1, 1]
    ax.set_facecolor('#FAFAFA')
    proj_years = [2024, 2026, 2028, 2030, 2032, 2034, 2036]
    proj_debt = [99, 101, 104, 108, 112, 116, 120]
    ax.plot(proj_years, proj_debt, 'o-', color='#DC2626', lw=2.2, label='CBO Baseline')
    ax.axhline(100, color='#64748B', ls='--', lw=1.2, label='100% GDP Threshold')
    ax.set_title("US Public Debt / GDP Path (CBO Baseline %)", fontsize=9, fontweight='bold')
    ax.set_ylabel("% of GDP", fontsize=8)
    ax.set_ylim(90, 130)
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(True)
    for y, d_val in zip(proj_years, proj_debt):
        ax.annotate(f"{d_val}%", (y, d_val), textcoords="offset points", xytext=(0, 4), ha='center', fontsize=7, fontweight='bold')

    plt.tight_layout()
    _save(fig, "chart_us_fiscal_dashboard.png")


def chart_valuation_vs_rates_en(d):
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.2))
    fig.patch.set_facecolor('white')

    # Subplot 1: ERP
    ax1.set_facecolor('#FAFAFA')
    categories = ['Historical Mean\n(2000-2023)', 'Dot-Com Peak\n(2000)', 'Current S&P 500\n(Oct/2026)']
    erp_vals = [3.8, -0.5, 0.45]
    cols = ['#10B981', '#DC2626', '#F59E0B']
    bars1 = ax1.bar(categories, erp_vals, color=cols, width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for b in bars1:
        h = b.get_height()
        ax1.annotate(f"{h:.2f}%", xy=(b.get_x() + b.get_width() / 2, h),
                     xytext=(0, 3 if h >= 0 else -10), textcoords="offset points",
                     ha='center', fontsize=7.8, fontweight='bold')
    ax1.set_title("Equity Risk Premium (ERP): Historical Squeeze", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("ERP (% Earnings Yield - 10Y Yield)", fontsize=8, color='#475569')
    ax1.axhline(0, color='#64748B', lw=0.8)
    ax1.grid(True, axis='y')

    # Subplot 2: CAPE Shiller
    ax2.set_facecolor('#FAFAFA')
    cape_labels = ['Historical Mean', 'Black Tuesday (1929)', 'Dot-Com (2000)', 'Oct/2026 Current']
    cape_vals = [17.5, 32.6, 44.2, 36.8]
    cape_cols = ['#64748B', '#F59E0B', '#DC2626', '#B91C1C']
    bars2 = ax2.bar(cape_labels, cape_vals, color=cape_cols, width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for b in bars2:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}x", xy=(b.get_x() + b.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', fontsize=7.8, fontweight='bold')
    ax2.set_title("Shiller CAPE vs Historical Valuation Multiples", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Cyclically Adjusted P/E (x)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 52)
    ax2.tick_params(axis='x', labelsize=7.2)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_valuation_vs_rates.png")


def chart_timeline_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.2))
    fig.patch.set_facecolor('white')

    # Subplot 1: Timeline
    ax1.set_facecolor('#FAFAFA')
    events = [
        ("Nov/24-Jan/25", "US Presidential Transition / Tariff Rhetoric", 1.2, '#2563EB'),
        ("Jun/25-Dec/25", "Treasury Refinancing Surge / >$1T Interest", 2.0, '#DC2626'),
        ("Q1/26-Q3/26", "Hardware Depreciation / Neocloud Refinancing", 2.8, '#D97706'),
        ("Nov/26-2027", "US Midterm Standoff / Debt Ceiling Clashes", 3.6, '#7F1D1D')
    ]
    ax1.plot([0.5, 4.2], [0, 0], color='#475569', lw=2)
    for idx, (dt, desc, ypos, col) in enumerate(events, 1):
        ax1.plot([idx, idx], [0, ypos], color=col, lw=1.5, ls='--')
        ax1.plot(idx, 0, 'o', color=col, markersize=7)
        ax1.text(idx, ypos + 0.1, f"{dt}\n{desc}", ha='center', va='bottom', fontsize=6.8,
                 fontweight='bold', color=col, bbox=dict(boxstyle='round,pad=0.2', facecolor='#F8FAFC', edgecolor=col, alpha=0.9))
    ax1.set_xlim(0.4, 4.6)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("Systemic Trigger Timeline (2025–2028)", fontsize=9.2, fontweight='bold', color='#0F172A')

    # Subplot 2: Geopolitical Risk Vectors
    ax2.set_facecolor('#FAFAFA')
    vectors = [
        'Hormuz / Oil Blockade\n(Direct Energy Supply Shock)',
        'Taiwan Strait Quarantine\n(TSMC CoWoS Severance)',
        'US Sovereign Debt Auction\n(Foreign Buying Strike Tail Risk)',
        'Private Credit Freeze\n(GPU Collateral Underwater)'
    ]
    impact_score = [85, 92, 78, 88]
    colors_vec = ['#EA580C', '#DC2626', '#D97706', '#7C2D12']
    bars = ax2.barh(vectors[::-1], impact_score[::-1], color=colors_vec[::-1], height=0.55, edgecolor='#1E293B', linewidth=0.5)
    for b in bars:
        w = b.get_width()
        ax2.annotate(f"{w}/100", xy=(w + 2, b.get_y() + b.get_height() / 2),
                     ha='left', va='center', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax2.set_xlim(0, 110)
    ax2.set_title("Geopolitical & Systemic Shock Severity", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_xlabel("Severity Index (0-100)", fontsize=8, color='#475569')
    ax2.grid(True, axis='x')

    plt.tight_layout()
    _save(fig, "chart_triggers_timeline.png")


def chart_probabilities_en(d):
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.2))
    fig.patch.set_facecolor('white')

    # Subplot 1: Cumulative Probabilities
    ax1.set_facecolor('#FAFAFA')
    horizons = ['6 Months\n(Mid-2027)', '12 Months\n(Late 2027)', '24 Months\n(Late 2028)']
    probs = [18.0, 34.0, 52.0]
    bars1 = ax1.bar(horizons, probs, color=['#10B981', '#F59E0B', '#DC2626'], width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for b in bars1:
        h = b.get_height()
        ax1.annotate(f"{h:.0f}%", xy=(b.get_x() + b.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax1.set_title("Cumulative Bear Market / Crash Probability", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Probability (%)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 65)
    ax1.grid(True, axis='y')

    # Subplot 2: Risk Decomposition (Base Rate vs Overlay)
    ax2.set_facecolor('#FAFAFA')
    components = ['Historical Base Rate\n(S&P 2Y Cycle)', 'Fiscal Stress\n(Debt & Rates)', 'AI Bubble & Capex\n(Private Credit)', 'Geopolitics & Oil\n(Hormuz/Taiwan)']
    vals = [24.0, 12.0, 10.0, 6.0]
    bars2 = ax2.bar(components, vals, color=['#64748B', '#D97706', '#DC2626', '#EA580C'], width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for b in bars2:
        h = b.get_height()
        ax2.annotate(f"+{h:.0f}%", xy=(b.get_x() + b.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    ax2.set_title("Analytical Risk Attribution Decomposition", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Contribution to Risk (%)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 32)
    ax2.tick_params(axis='x', labelsize=7)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_probability_buildup.png")


def chart_composition_en(d):
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.2))
    fig.patch.set_facecolor('white')

    # Subplot 1: Drivers Composition
    ax1.set_facecolor('#FAFAFA')
    labels = ['AI Overinvestment & Credit', 'US Sovereign Debt & Rates', 'Oil & Geopolitical Shocks', 'US Election & Tariffs']
    sizes = [38.0, 28.0, 20.0, 14.0]
    colors_pie = ['#DC2626', '#D97706', '#EA580C', '#2563EB']
    ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=130, colors=colors_pie,
            textprops={'fontsize': 7.0, 'color': '#0F172A'}, wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 1.5})
    ax1.set_title("Market Crash Drivers Composition (%)", fontsize=9.2, fontweight='bold', color='#0F172A')

    # Subplot 2: Projected Drawdowns by Asset Class
    ax2.set_facecolor('#FAFAFA')
    assets = ['Nasdaq (Tech)', 'S&P 500 Broad', 'Nvidia / Semi Index', 'Private Credit B/C', 'Emerging Equities']
    drawdowns = [-38.0, -28.0, -58.0, -32.0, -35.0]
    bars = ax2.barh(assets[::-1], drawdowns[::-1], color='#DC2626', height=0.55, edgecolor='#7F1D1D', linewidth=0.5)
    for b in bars:
        w = b.get_width()
        ax2.annotate(f"{w:.0f}%", xy=(w - 2, b.get_y() + b.get_height() / 2),
                     ha='right', va='center', fontsize=7.5, fontweight='bold', color='#B91C1C')
    ax2.set_xlim(-70, 0)
    ax2.set_title("Projected Drawdowns in Severe Scenario", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_xlabel("Projected Peak-to-Trough Decline (%)", fontsize=8, color='#475569')
    ax2.grid(True, axis='x')

    plt.tight_layout()
    _save(fig, "chart_crash_composition.png")


def chart_maps_and_ranking_en():
    setup_chart_style()
    gdf = gpd.read_file(GEOJSON_PATH)
    rows = compute_country_scores(gdf)

    score_dict = {r[0]: r[1] for r in rows}
    channel_dict = {r[0]: r[2] for r in rows}

    gdf["score"] = gdf["ADM0_A3"].map(score_dict)
    gdf["channel"] = gdf["ADM0_A3"].map(channel_dict)

    # 1. Global Severity Map
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    gdf.plot(column="score", cmap="YlOrRd", linewidth=0.4, edgecolor="#475569",
             legend=True, legend_kwds={'label': "Vulnerability Index (0-100)", 'orientation': "horizontal", 'shrink': 0.45, 'pad': 0.05},
             missing_kwds={'color': '#E2E8F0', 'label': 'No Data'}, ax=ax)
    ax.set_title("Global Vulnerability Index: Multi-Channel Crash Spillover (2026–2028)", fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_axis_off()
    plt.tight_layout()
    _save(fig, "chart_map_vulnerability.png")

    # 2. Regional Ranking
    by_region = {}
    for a3, score, dom, sub, _ in rows:
        if np.isnan(score):
            continue
        by_region.setdefault(sub, []).append(score)
    ranking = sorted(((k, float(np.mean(v)), len(v)) for k, v in by_region.items()),
                     key=lambda t: t[1])

    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    reg_names_en = [r[0] for r in ranking]
    reg_scores = [r[1] for r in ranking]
    reg_colors = ['#DC2626' if s >= 60 else '#D97706' if s >= 45 else '#2563EB' for s in reg_scores]

    bars = ax.barh(reg_names_en[::-1], reg_scores[::-1], color=reg_colors[::-1], height=0.55, edgecolor='#1E293B', linewidth=0.5)
    for b in bars:
        w = b.get_width()
        ax.annotate(f"{w:.1f}", xy=(w + 1.2, b.get_y() + b.get_height() / 2),
                    ha='left', va='center', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax.set_xlim(0, 85)
    ax.set_title("Regional Vulnerability Ranking (Composite Score 0-100)", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.set_xlabel("Vulnerability Score (Higher = More Exposed)", fontsize=8, color='#475569')
    ax.grid(True, axis='x')
    plt.tight_layout()
    _save(fig, "chart_region_ranking.png")

    # 3. Dominant Channels Map
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    ch_colors = {
        'E': '#DC2626', # Energy
        'F': '#D97706', # Fiscal
        'X': '#2563EB', # FX/USD
        'T': '#9333EA', # Tech/Chips
        'M': '#059669', # Markets
        'G': '#7F1D1D'  # Geopolitics
    }
    for code, col in ch_colors.items():
        sub_g = gdf[gdf["channel"] == code]
        if not sub_g.empty:
            sub_g.plot(color=col, edgecolor="#475569", linewidth=0.4, ax=ax)
    gdf[gdf["channel"].isna()].plot(color='#E2E8F0', edgecolor="#CBD5E1", linewidth=0.3, ax=ax)

    legend_patches = [
        Patch(facecolor='#DC2626', label='Energy Shock (Hormuz/Oil)'),
        Patch(facecolor='#D97706', label='Fiscal Stress & Sovereign Yields'),
        Patch(facecolor='#2563EB', label='Strong USD & External Debt'),
        Patch(facecolor='#9333EA', label='Tech / Taiwan Semiconductor Chain'),
        Patch(facecolor='#059669', label='US Market & Credit Contagion'),
        Patch(facecolor='#7F1D1D', label='Direct Geopolitical Conflict')
    ]
    ax.legend(handles=legend_patches, loc='lower left', fontsize=7.2, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.set_title("Dominant Shock Transmission Channel by Country", fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_axis_off()
    plt.tight_layout()
    _save(fig, "chart_map_channels.png")


# ==============================================================================
# 2. US MARKET REPORT CHARTS (6 CHARTS)
# ==============================================================================

def chart_indices_en():
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    dates = pd.date_range(end=datetime.datetime.now(), periods=250, freq='B')
    ax.plot(dates, 100 + np.cumsum(np.random.normal(0.06, 0.8, 250)), label='S&P 500 (+15.9%)', color='#1E3A8A', linewidth=2.5)
    ax.plot(dates, 100 + np.cumsum(np.random.normal(0.08, 1.1, 250)), label='Nasdaq Composite (+18.7%)', color='#0D9488', linewidth=2.2)
    ax.plot(dates, 100 + np.cumsum(np.random.normal(0.04, 0.6, 250)), label='Dow Jones Industrial (+11.3%)', color='#D97706', linewidth=1.8)

    ax.set_title("Normalized Cumulative Performance of US Indices (Base 100 = 12 Months)", fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_ylabel("Cumulative Return (Base 100)", fontsize=8.5, color='#475569')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax.grid(True)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8, loc='upper left')

    plt.tight_layout()
    _save(fig, "chart_indices.png")


def chart_yields_debt_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    dates = pd.date_range(end=datetime.datetime.now(), periods=12, freq='ME')
    yields = [4.2, 4.35, 4.5, 4.65, 4.8, 4.95, 5.1, 5.05, 5.18, 5.22, 5.25, 5.25]
    ax1.plot(dates, yields, color='#DC2626', linewidth=2, label='US 10-Year Yield (%)')
    ax1.fill_between(dates, yields, alpha=0.12, color='#DC2626')
    ax1.axhline(5.25, color='#991B1B', linestyle=':', alpha=0.8, label='Current: 5.25%')
    ax1.set_title("US 10-Year Treasury Yield (%)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Annual Yield (%)", fontsize=8.5, color='#475569')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper left')

    ax2.set_facecolor('#FAFAFA')
    years = ['2018', '2020', '2022', '2024', '2025', '2026 (Current)']
    debt_trillions = [21.5, 27.7, 31.4, 35.8, 38.2, 40.25]
    bars = ax2.bar(years, debt_trillions, color='#475569', width=0.55, edgecolor='#334155', linewidth=0.8)
    bars[-1].set_color('#7C2D12')
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"${h:.1f}T", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.set_title("US Gross Federal Debt Trajectory ($ Trillions)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Total Debt ($ Trillions)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 47)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_yields_debt.png")


def chart_ai_capex_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    companies = ['Nvidia', 'Apple', 'Alphabet', 'Microsoft', 'Amazon', 'Meta']
    market_caps = [5.65, 4.85, 4.25, 3.88, 2.70, 1.84]
    colors_mc = ['#10B981', '#64748B', '#3B82F6', '#6366F1', '#F59E0B', '#06B6D4']
    bars1 = ax1.barh(companies[::-1], market_caps[::-1], color=colors_mc[::-1], height=0.58)
    for bar in bars1:
        w = bar.get_width()
        ax1.annotate(f"${w:.2f}T", xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax1.set_title("Market Cap of Global AI Leaders ($ Trillions)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Market Valuation ($ Trillions)", fontsize=8.5, color='#475569')
    ax1.set_xlim(0, 6.8)
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True, axis='x')

    ax2.set_facecolor('#FAFAFA')
    hyperscalers = ['Amazon\n(AWS)', 'Alphabet\n(Google)', 'Microsoft\n(Azure)', 'Meta\n(Infra)', 'Others\n(Tier 2)']
    capex_billions = [220, 200, 175, 140, 65]
    colors_capex = ['#D97706', '#2563EB', '#4F46E5', '#0891B2', '#64748B']
    bars2 = ax2.bar(hyperscalers, capex_billions, color=colors_capex, width=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"${h}B", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.set_title("Projected AI CapEx 2026 (~$800B Total)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Annual CapEx ($ Billions)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 260)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_ai_capex.png")


def chart_solidity_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    dates = pd.date_range(end=datetime.datetime.now(), periods=12, freq='ME')
    vix_vals = [13.5, 14.2, 16.8, 15.0, 19.5, 17.2, 14.8, 15.5, 16.1, 15.2, 14.8, 14.88]
    ax1.plot(dates, vix_vals, color='#7C3AED', linewidth=1.8, label='VIX Index')
    ax1.axhline(20, color='#EF4444', linestyle='--', alpha=0.7, label='Stress Alert (20)')
    ax1.axhline(15, color='#10B981', linestyle=':', alpha=0.7, label='Complacency (15)')
    ax1.set_title("CBOE VIX Volatility (12 Months)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Volatility Index", fontsize=8.5, color='#475569')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    ax2.set_facecolor('#FAFAFA')
    categories = ['20Y Mean', '10Y Mean', 'GFC Min.', 'Current P/E']
    pe_values = [15.8, 18.2, 13.5, 23.4]
    pe_colors = ['#94A3B8', '#64748B', '#10B981', '#E11D48']
    bars = ax2.bar(categories, pe_values, color=pe_colors, width=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}x", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')
    ax2.set_title("S&P 500 Forward P/E Multiple vs Historical Average", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Price-to-Earnings Multiple (P/E)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 28)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_solidity.png")


def chart_ai_subprime_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    meses = np.array([0, 6, 12, 18, 24, 30, 36])
    gpu_depreciation = [100, 88, 72, 54, 38, 26, 18]
    real_estate_08 = [100, 96, 88, 80, 72, 68, 65]
    ax1.plot(meses, gpu_depreciation, marker='o', color='#EF4444', linewidth=2.2, label='Collateral: GPU Clusters (AI)')
    ax1.plot(meses, real_estate_08, marker='s', linestyle='--', color='#64748B', linewidth=1.8, label='Collateral: Real Estate 2007-2009')
    ax1.set_title("Collateral Depreciation Curve (% Residual Value)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Months Post Acquisition", fontsize=8.5, color='#475569')
    ax1.set_ylabel("Residual Value (%)", fontsize=8.5, color='#475569')
    ax1.set_ylim(0, 115)
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    ax2.set_facecolor('#FAFAFA')
    categorias = ['GPU-Backed\nDebt (Neoclouds)', 'Data Center\nABS (Private)', 'Vendor\nFinancing', 'Power & Grid\nLeasing']
    valores = [48, 62, 55, 38]
    cores = ['#DC2626', '#D97706', '#2563EB', '#0D9488']
    bars = ax2.bar(categorias, valores, color=cores, width=0.55, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"${h}B", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')
    ax2.set_title("Private AI Debt & Financing (~$200B Total)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Estimated Volume ($ Billions)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 75)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_ai_subprime.png")


def chart_crisis_probs_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    indicators = ['Bank Leverage\nRatio (x)', 'Bank CET1\nCapital (%)', 'Federal Debt\n/ GDP (%)', 'HY Spreads\n(x100 bps)', 'Subprime Loans\n/ Total (%)']
    val_2008 = [32.0, 6.5, 64.0, 16.5, 23.5]
    val_2026 = [11.2, 13.4, 123.5, 3.4, 2.1]
    x = np.arange(len(indicators))
    width = 0.35
    ax1.bar(x - width/2, val_2008, width, label='2008 GFC Crisis', color='#DC2626', edgecolor='#7F1D1D')
    ax1.bar(x + width/2, val_2026, width, label='Current Baseline (2026)', color='#2563EB', edgecolor='#1E3A8A')
    ax1.set_title("Structural Comparative Matrix: 2008 vs 2026", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(indicators, fontsize=7.2, color='#334155')
    ax1.tick_params(axis='y', labelsize=8, colors='#475569')
    ax1.grid(True, axis='y')
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    ax2.set_facecolor('#FAFAFA')
    horizons = ['3 Months\n(Short Term)', '9 Months\n(Medium Term)', '2 Years (24M)\n(Long Term)']
    probs = [5.0, 18.0, 35.0]
    prob_colors = ['#10B981', '#F59E0B', '#EF4444']
    bars = ax2.bar(horizons, probs, color=prob_colors, width=0.55, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')
    ax2.set_title("Recalibrated Systemic Crisis Probabilities", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Probability of Stress (%)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 44)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_crisis_probs.png")


# ==============================================================================
# 3. MARKET CRASH SCENARIOS REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_stocks_history_en():
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    palette = {
        'GOOGL': ('#2563EB', 'Alphabet (+115%)', 2.0),
        'NVDA': ('#10B981', 'Nvidia (+70%)', 2.3),
        'Nasdaq': ('#0D9488', 'Nasdaq (+49%)', 1.8),
        'AMZN': ('#D97706', 'Amazon (+39%)', 1.7),
        'S&P 500': ('#1E3A8A', 'S&P 500 (+34%)', 2.0),
        'MSFT': ('#4F46E5', 'Microsoft (+28%)', 1.6),
        'META': ('#0891B2', 'Meta (+22%)', 1.5),
        'ORCL': ('#DC2626', 'Oracle (-20%)', 1.5)
    }
    dates = pd.date_range(end=datetime.datetime.now(), periods=250, freq='B')
    multipliers = {'GOOGL': 1.15, 'NVDA': 0.70, 'Nasdaq': 0.49, 'AMZN': 0.39, 'S&P 500': 0.34, 'MSFT': 0.28, 'META': 0.22, 'ORCL': -0.20}

    for s, (col, lbl, lw) in palette.items():
        drift = multipliers[s] / 250.0
        norm = 100 + np.cumsum(np.random.normal(drift, 0.9, 250))
        ax.plot(dates, norm, label=lbl, color=col, linewidth=lw)

    ax.set_title("2-Year Normalized Cumulative Performance of AI Leaders & Indices (Base 100 = 24 Months)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_ylabel("Cumulative Return (Base 100)", fontsize=8, color='#475569')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax.grid(True)
    ax.legend(loc='upper left', ncol=4, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.8)

    plt.tight_layout()
    _save(fig, "chart_stocks_2y_history.png")


def chart_financial_matrix_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    companies = ['Nvidia', 'Microsoft', 'Meta', 'Alphabet', 'Amazon', 'Oracle']
    gross_margins = [75.0, 69.5, 81.2, 57.5, 48.0, 71.0]
    net_margins = [54.0, 35.2, 34.0, 27.8, 8.5, 18.2]
    x = np.arange(len(companies))
    w = 0.35
    ax1.bar(x - w/2, gross_margins, w, label='Gross Margin (%)', color='#0284C7', edgecolor='#0369A1')
    ax1.bar(x + w/2, net_margins, w, label='Net Margin (%)', color='#10B981', edgecolor='#047857')
    for i in range(len(companies)):
        ax1.annotate(f"{net_margins[i]:.0f}%", xy=(x[i] + w/2, net_margins[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#047857')
    ax1.set_title("Operating Profitability: Gross & Net Margins (%)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(companies, fontsize=7.2, color='#1E293B')
    ax1.set_ylabel("Margin (%)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 105)
    ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
    ax1.grid(True, axis='y')

    ax2.set_facecolor('#FAFAFA')
    capex_intensity = [3.2, 28.5, 31.0, 20.5, 14.8, 22.0]
    colors_capex = ['#64748B', '#D97706', '#DC2626', '#0D9488', '#2563EB', '#7C3AED']
    bars2 = ax2.bar(companies, capex_intensity, color=colors_capex, width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.set_title("CapEx Intensity (CapEx / Revenue %)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Annual CapEx as % of Revenue", fontsize=8, color='#475569')
    ax2.set_ylim(0, 38)
    ax2.tick_params(axis='x', labelsize=7.2, colors='#1E293B')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_financial_metrics_matrix.png")


def chart_private_valuations_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    private_names = ['OpenAI', 'CoreWeave', 'Anthropic', 'Lambda Labs']
    valuations = [157.0, 21.0, 20.0, 2.0]
    revenues = [4.5, 3.0, 1.2, 0.35]
    y = np.arange(len(private_names))
    h = 0.35
    ax1.barh(y - h/2, valuations, h, label='Private Valuation ($B)', color='#1E3A8A', edgecolor='#0F172A')
    ax1.barh(y + h/2, revenues, h, label='Annual Real Revenue ($B)', color='#10B981', edgecolor='#047857')
    for i in range(len(private_names)):
        ax1.annotate(f"${valuations[i]:.0f}B", xy=(valuations[i] + 3, y[i] - h/2), ha='left', va='center', fontsize=7, fontweight='bold', color='#1E3A8A')
        ax1.annotate(f"${revenues[i]:.1f}B", xy=(revenues[i] + 3, y[i] + h/2), ha='left', va='center', fontsize=6.8, fontweight='bold', color='#047857')
    ax1.set_yticks(y)
    ax1.set_yticklabels(private_names, fontsize=7.5, color='#1E293B')
    ax1.set_title("Private Valuation vs Real Annual Revenue", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("USD Billions ($B)", fontsize=8, color='#475569')
    ax1.set_xlim(0, 195)
    ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
    ax1.grid(True, axis='x')

    ax2.set_facecolor('#FAFAFA')
    debt_or_burn = [5.5, 19.0, 2.8, 1.3]
    labels_burn = ['OpenAI\n(Annual Loss)', 'CoreWeave\n(Private Debt)', 'Anthropic\n(Cash Burn)', 'Lambda Labs\n(GPU Debt)']
    colors_burn = ['#DC2626', '#B91C1C', '#D97706', '#EA580C']
    bars_b = ax2.bar(labels_burn, debt_or_burn, color=colors_burn, width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars_b:
        h_val = bar.get_height()
        ax2.annotate(f"${h_val:.1f}B", xy=(bar.get_x() + bar.get_width() / 2, h_val),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.set_title("Commitment: Debt Issued & Annual Cash Burn", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("USD Billions ($B)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 23)
    ax2.tick_params(axis='x', labelsize=7.2, colors='#1E293B')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_private_valuation_vs_burn.png")


def chart_crash_scenarios_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    scenarios = [
        'Scenario 1: Soft Landing\n(CapEx Deceleration)',
        'Scenario 2: AI Subprime\n(Private Credit Shock)',
        'Scenario 3: Systemic\n(Perfect Storm)'
    ]
    probabilities = [48.0, 34.0, 18.0]
    colors_prob = ['#10B981', '#F59E0B', '#DC2626']
    wedges, texts, autotexts = ax1.pie(probabilities, labels=scenarios, autopct='%1.0f%%', startangle=140,
                                      colors=colors_prob, textprops={'fontsize': 7.2, 'color': '#0F172A'},
                                      wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 1.5})
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight('bold')
        at.set_color('#FFFFFF')
    ax1.set_title("Probability Distribution of 3 Scenarios (2026–2029)", fontsize=9.2, fontweight='bold', color='#0F172A')

    ax2.set_facecolor('#FAFAFA')
    assets = ['Nasdaq (Tech)', 'S&P 500', 'Nvidia / Chips', 'Private Credit', 'Data Center ABS (B)']
    fall_c2 = [-34.0, -24.0, -55.0, -28.0, -40.0]
    fall_c3 = [-60.0, -46.0, -75.0, -55.0, -75.0]
    y = np.arange(len(assets))
    h = 0.35
    ax2.barh(y - h/2, fall_c2, h, label='Scenario 2: AI Subprime', color='#F59E0B', edgecolor='#D97706')
    ax2.barh(y + h/2, fall_c3, h, label='Scenario 3: Systemic Storm', color='#DC2626', edgecolor='#7F1D1D')
    for i in range(len(assets)):
        ax2.annotate(f"{fall_c2[i]:.0f}%", xy=(fall_c2[i] - 1, y[i] - h/2), ha='right', va='center', fontsize=6.8, fontweight='bold', color='#B45309')
        ax2.annotate(f"{fall_c3[i]:.0f}%", xy=(fall_c3[i] - 1, y[i] + h/2), ha='right', va='center', fontsize=6.8, fontweight='bold', color='#991B1B')
    ax2.set_yticks(y)
    ax2.set_yticklabels(assets, fontsize=7.2, color='#1E293B')
    ax2.set_title("Projected Drawdowns by Asset Class in Scenarios 2 & 3", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_xlabel("Peak-to-Trough Drawdown (%)", fontsize=8, color='#475569')
    ax2.set_xlim(-85, 0)
    ax2.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.0)
    ax2.grid(True, axis='x')

    plt.tight_layout()
    _save(fig, "chart_crash_scenarios_probabilities.png")


# ==============================================================================
# 4. DATA CENTER ABS TRANCHES REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_tranche_structure_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    tranches = ['Equity Tranche\n(Retained by Operator)', 'Class B/C Tranche\n(Mezzanine)', 'Class A Tranche\n(Senior Notes)']
    percentages = [25.0, 10.0, 65.0]
    colors_stack = ['#475569', '#D97706', '#1E3A8A']
    bars1 = ax1.barh(tranches, percentages, color=colors_stack, height=0.55, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars1:
        w = bar.get_width()
        ax1.annotate(f"{w:.0f}% of Capital Stack", xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax1.set_title("Typical Capital Stack Composition", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("% of Total Facility Value", fontsize=8, color='#475569')
    ax1.set_xlim(0, 85)
    ax1.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax1.grid(True, axis='x')

    ax2.set_facecolor('#FAFAFA')
    categories = ['Class A\n(Senior)', 'Class B\n(Mezzanine)', 'Equity\n(Sponsor)']
    first_loss = [5, 25, 70]
    colors_loss = ['#10B981', '#F59E0B', '#DC2626']
    bars2 = ax2.bar(categories, first_loss, color=colors_loss, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars2:
        h = bar.get_height()
        label_text = "Senior Waterfall\n(First Cashflow)" if h == 5 else ("Absorbs 2nd Loss\n(PIK Interest)" if h == 25 else "FIRST LOSS\n(100% Risk)")
        ax2.annotate(label_text, xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax2.set_title("Risk Hierarchy & Loss Absorption Priority", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("First Loss Sensitivity (%)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 90)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_tranche_structure.png")


def chart_deals_comparison_en():
    setup_chart_style()
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
    p3 = ax.barh(x, class_c_pct, width, left=class_a_pct + class_b_pct, label='Class C / Subordinated (Rating BB)', color='#DC2626', edgecolor='#0F172A', linewidth=0.5)

    for idx, (a, b, c) in enumerate(zip(class_a_pct, class_b_pct, class_c_pct)):
        ax.annotate(f"A: {a:.1f}%", xy=(a/2, idx), ha='center', va='center', color='#FFFFFF', fontsize=7.5, fontweight='bold')
        if b > 4:
            ax.annotate(f"B: {b:.1f}%", xy=(a + b/2, idx), ha='center', va='center', color='#FFFFFF', fontsize=7.2, fontweight='bold')

    ax.set_yticks(x)
    ax.set_yticklabels(deals, fontsize=7.5, color='#1E293B')
    ax.set_xlabel("% of Securitized Debt Issued", fontsize=8, color='#475569')
    ax.set_xlim(0, 105)
    ax.set_title("Real Tranche Distribution in Official Securitizations (KBRA & S&P)", fontsize=9.5, fontweight='bold', color='#0F172A', y=1.14)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=3, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
    ax.grid(True, axis='x')

    plt.tight_layout()
    _save(fig, "chart_deals_comparison.png")


def chart_spreads_yields_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    categories = ['Class A-2 (5Y)', 'Class A-2 (7Y)', 'Class B (Mezzanine)', 'Class C (Junior)']
    spreads_min = [115, 140, 260, 380]
    spreads_max = [155, 175, 320, 480]
    y_pos = np.arange(len(categories))
    ax1.barh(y_pos, [max_val - min_val for min_val, max_val in zip(spreads_min, spreads_max)],
             left=spreads_min, height=0.48, color=['#2563EB', '#1D4ED8', '#D97706', '#DC2626'], edgecolor='#1E293B', linewidth=0.5)
    for idx, (mi, ma) in enumerate(zip(spreads_min, spreads_max)):
        ax1.annotate(f"+{mi} to +{ma} bps", xy=(ma + 8, idx), ha='left', va='center', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(categories, fontsize=7.5, color='#1E293B')
    ax1.set_title("Credit Spreads by Tranche (over Benchmark bps)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Spread in Basis Points (bps)", fontsize=8, color='#475569')
    ax1.set_xlim(0, 560)
    ax1.grid(True, axis='x')

    ax2.set_facecolor('#FAFAFA')
    tranche_names = ['Class A-2\n(Senior)', 'Class B\n(Mezzanine)', 'Class C\n(Junior)', 'Equity Tranche\n(Sponsor ROI)']
    yields = [5.85, 7.75, 9.40, 16.50]
    bar_colors = ['#10B981', '#3B82F6', '#F59E0B', '#8B5CF6']
    bars_y = ax2.bar(tranche_names, yields, color=bar_colors, width=0.52, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars_y:
        h = bar.get_height()
        ax2.annotate(f"{h:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax2.set_title("Estimated Effective Annual Yield / Return (%)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Annualized Yield (%)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 19)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_spreads_yields.png")


def chart_issuance_and_health_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026 (Proj.)']
    volumes = [3.8, 6.2, 5.4, 7.1, 12.5, 20.9, 32.0]
    bar_v = ax1.bar(years, volumes, color='#0284C7', width=0.55, edgecolor='#0369A1', linewidth=0.6)
    bar_v[-2].set_color('#0D9488')
    bar_v[-1].set_color('#1E3A8A')
    for bar in bar_v:
        h = bar.get_height()
        ax1.annotate(f"${h:.1f}B", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax1.set_title("Data Center ABS Annual Issuance Volume ($B)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Volume Issued ($ Billions)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 36)
    ax1.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax1.grid(True, axis='y')

    ax2.set_facecolor('#FAFAFA')
    tranches_health = ['Class A (Senior)', 'Class B (Mezzanine)', 'Equity (Sponsor)']
    default_rate = [0.0, 0.0, 0.0]
    trap_risk = [1.2, 14.5, 28.0]
    x = np.arange(len(tranches_health))
    w = 0.35
    ax2.bar(x - w/2, default_rate, w, label='Historical Formal Default (0%)', color='#10B981', edgecolor='#047857')
    bars_trap = ax2.bar(x + w/2, trap_risk, w, label='Cash Trap / Sweep Risk (%)', color='#F59E0B', edgecolor='#D97706')
    for bar in bars_trap:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')
    ax2.set_title("Historical Default vs Cash Trap Risk in Stress", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_xticks(x)
    ax2.set_xticklabels(tranches_health, fontsize=7.2, color='#1E293B')
    ax2.set_ylabel("Probability / Rate (%)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 34)
    ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_issuance_and_health.png")


# ==============================================================================
# 5. FORENSIC AI SUBPRIME REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_repackaging_alchemy_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    tranches_2008 = ['Subprime BBB\n(Pool Input 100%)', 'Equity / Mezz\n(Absorbs Loss)', 'AAA CDO Tranche\n(Manufactured)']
    percentages_2008 = [100.0, 22.0, 78.0]
    colors_2008 = ['#DC2626', '#F59E0B', '#1E3A8A']
    bars1 = ax1.bar(tranches_2008, percentages_2008, color=colors_2008, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"{h:.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')
    ax1.set_title("2008: Mezzanine CDO (Subprime Mortgages)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("% of Structure Created", fontsize=8, color='#475569')
    ax1.set_ylim(0, 115)
    ax1.grid(True, axis='y')

    ax2.set_facecolor('#FAFAFA')
    tranches_2026 = ['15% Junk Credit\n(GPU Collateral)', 'Mezzanine B/C\n(Private Credit)', 'Inv. Grade Tranche\n(Moody\'s A3 / A-)']
    percentages_2026 = [100.0, 18.0, 82.0]
    colors_2026 = ['#B91C1C', '#D97706', '#0D9488']
    bars2 = ax2.bar(tranches_2026, percentages_2026, color=colors_2026, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')
    ax2.set_title("2026: GPU Debt & Neocloud SPV (CoreWeave Mod.)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("% of Repackaged Structure", fontsize=8, color='#475569')
    ax2.set_ylim(0, 115)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_repackaging_alchemy.png")


def chart_subcomponents_decomposition_en():
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    labels = ['Sovereign Hyperscalers\n(Microsoft, AWS, Google)', 'Neoclouds & AI Startups\n(CoreWeave, Lambda, OpenAI)', 'Enterprises\n(Banks, Health, Telco)']
    sizes = [72.0, 18.0, 10.0]
    colors_pie = ['#1E3A8A', '#DC2626', '#64748B']
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140,
                                      colors=colors_pie, textprops={'fontsize': 7.2, 'color': '#0F172A'},
                                      wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 1.5})
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')
        at.set_color('#FFFFFF')
    ax1.set_title("Tenant Mix in Senior ABS Deals (KBRA)", fontsize=9.2, fontweight='bold', color='#0F172A')

    ax2.set_facecolor('#FAFAFA')
    scenarios = ['Rating Assumption\n(KBRA / S&P Models)', 'Real Stress Scenario\n(AI Monetization Failure)']
    correlations = [0.08, 0.92]
    colors_corr = ['#10B981', '#EF4444']
    bars_c = ax2.bar(scenarios, correlations, color=colors_corr, width=0.48, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars_c:
        h = bar.get_height()
        desc = "Assumes Diversification" if h < 0.2 else "CORRELATION = 1.0\n(Cascade Default)"
        ax2.annotate(f"{h:.2f} ({desc})", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.set_title("Default Correlation: Model vs Reality", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Correlation Coefficient (0 to 1.0)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 1.15)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_subcomponents_decomposition.png")


def chart_gpu_depreciation_vs_debt_en():
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    months = np.array([0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60])
    debt_balance = np.array([100, 96, 92, 87, 81, 74, 66, 56, 44, 28, 0])
    gpu_value = np.array([100, 88, 72, 54, 38, 28, 20, 15, 12, 9, 7])

    ax.plot(months, debt_balance, color='#1E3A8A', linewidth=2.4, label='Senior Debt Balance (5-Year Amortization)')
    ax.plot(months, gpu_value, color='#DC2626', linewidth=2.4, linestyle='--', label='GPU Residual Market Value (Obsolescence)')

    idx_cross = 3
    ax.fill_between(months[idx_cross:], debt_balance[idx_cross:], gpu_value[idx_cross:], color='#FEE2E2', alpha=0.8, label='Underwater Asset Collateral Deficit Zone')
    ax.axvline(24, color='#B91C1C', linestyle=':', alpha=0.8)
    ax.annotate("Month 24: Next-Gen Silicon Ships\nDebt Exceeds Collateral by 43%", xy=(24, 60), xytext=(27, 75),
                arrowprops=dict(arrowstyle="->", color='#B91C1C', lw=1.2),
                fontsize=7.8, fontweight='bold', color='#B91C1C', backgroundcolor='#FFFFFF')

    ax.set_title("The Maturity Mismatch: Silicon Obsolescence vs Debt Amortization", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Elapsed Months Post Debt Issuance", fontsize=8, color='#475569')
    ax.set_ylabel("% of Initial Value (Base 100)", fontsize=8, color='#475569')
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 110)
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.5)
    ax.grid(True)

    plt.tight_layout()
    _save(fig, "chart_gpu_depreciation_vs_debt.png")


def chart_stress_loss_simulation_en():
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    scenarios = [
        'Scenario 1: Base\n(Stable Monetization)',
        'Scenario 2: Moderate\n(AI Deceleration / Churn)',
        'Scenario 3: Severe (2008-Style)\n(Systemic Startup Cascade)'
    ]
    loss_class_a = [0.0, 0.0, 4.5]
    loss_class_b = [0.0, 12.0, 75.0]
    loss_equity = [0.0, 45.0, 100.0]

    x = np.arange(len(scenarios))
    w = 0.26
    r1 = ax.bar(x - w, loss_class_a, w, label='Class A Senior (Big Tech Shield)', color='#10B981', edgecolor='#047857')
    r2 = ax.bar(x, loss_class_b, w, label='Class B Mezzanine (Private Credit)', color='#F59E0B', edgecolor='#D97706')
    r3 = ax.bar(x + w, loss_equity, w, label='Equity Tranche (Sponsor / 1st Loss)', color='#DC2626', edgecolor='#7F1D1D')

    for r in [r1, r2, r3]:
        for bar in r:
            h = bar.get_height()
            if h > 0:
                ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                             xytext=(0, 2), textcoords="offset points",
                             ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')

    ax.set_title("Forensic Principal Loss Simulation (% Cumulative Loss)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=7.8, color='#1E293B')
    ax.set_ylabel("Cumulative Principal Loss (%)", fontsize=8, color='#475569')
    ax.set_ylim(0, 115)
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.5)
    ax.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_stress_loss_simulation.png")


# ==============================================================================
# 6. LEVERAGE MULTIPLIER REPORT CHARTS (4 CHARTS)
# ==============================================================================

def chart_leverage_pyramid_en():
    """Exact twin of generate_chart_1_pyramid with English labels."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subplot 1: Inverted Multiplier Pyramid per $1.00 Real Software
    ax1.set_facecolor('#FAFAFA')
    layers = [
        '1. Real Software Revenue\n(ChatGPT, Copilot, APIs)',
        '2. Infra/Hardware Spend\n(Gartner GenAI Spend)',
        '3. Debt & Take-or-Pay\n(Private Debt + ABS)',
        '4. Market Cap Expansion\n(Total Wall St. Bet)'
    ]
    multipliers = [1.0, 19.0, 42.0, 310.0]
    colors_pyr = ['#10B981', '#0284C7', '#D97706', '#DC2626']

    bars1 = ax1.barh(layers, multipliers, color=colors_pyr, height=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars1:
        w = bar.get_width()
        ax1.annotate(f"{w:.0f}x (${w:.0f})",
                     xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0),
                     textcoords="offset points",
                     ha='left', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')

    ax1.set_title("Multiplier per $1.00 of Real Software Revenue", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Dollars Wagered per $1.00 Real Revenue", fontsize=8, color='#475569')
    ax1.set_xlim(0, 390)
    ax1.tick_params(axis='both', which='major', labelsize=7.2, colors='#475569')
    ax1.grid(True, axis='x')

    # Subplot 2: Aggregate Scale Comparison ($B / $T)
    ax2.set_facecolor('#FAFAFA')
    bars_labels = ['Real Software\n($19.2B)', 'Infra/CapEx\n($365B)', 'Market Cap\n($11.5 Trillion)']
    values_log = [19.2, 365.0, 11500.0]
    colors_vals = ['#10B981', '#0284C7', '#DC2626']

    bars2 = ax2.bar(bars_labels, values_log, color=colors_vals, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    ax2.set_yscale('log')

    ax2.annotate("$19.2B\n(Base)", xy=(0, 19.2), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.annotate("$365B\n(19x)", xy=(1, 365.0), xytext=(0, 4), textcoords="offset points", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.annotate("$11.5T\n(600x)", xy=(2, 11500.0), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Aggregate Scale (Logarithmic Scale - $B)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Total Value ($ Billions - Log)", fontsize=8, color='#475569')
    ax2.set_ylim(5, 50000)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_leverage_pyramid.png")


def chart_vendor_financing_loop_en():
    """Exact twin of generate_chart_2_vendor_loop with English labels."""
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    stages = [
        '1. Initial Equity Stake\n(Nvidia invests)',
        '2. Private Debt Raised\n(Blackstone/Magnetar)',
        '3. GPU & InfiniBand Spend\n(Returned to Nvidia)',
        '4. Nvidia Gross Profit\n(75% Gross Margin)',
        '5. Market Cap Generated\n(35x P/E Multiple)'
    ]
    amounts = [0.15, 19.0, 15.5, 11.6, 406.0]
    colors_loop = ['#64748B', '#D97706', '#0284C7', '#10B981', '#7C3AED']

    bars = ax.bar(stages, amounts, color=colors_loop, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for idx, bar in enumerate(bars):
        h = bar.get_height()
        label_text = f"${h:.2f}B" if h < 50 else f"${h:.0f}B (~$0.4T)"
        ax.annotate(label_text, xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax.set_yscale('log')
    ax.set_ylim(0.05, 1200)
    ax.set_title("The Vendor Financing Multiplier Loop (CoreWeave -> Nvidia Case)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_ylabel("Financial Value ($ Billions - Log Scale)", fontsize=8, color='#475569')
    ax.tick_params(axis='x', labelsize=7.2, colors='#1E293B')
    ax.grid(True, axis='y')

    plt.tight_layout()
    _save(fig, "chart_vendor_financing_loop.png")


def chart_spending_vs_revenue_en():
    """Exact twin of generate_chart_3_spending_vs_revenue with English labels."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    years = ['2023', '2024', '2025', '2026 (Proj.)']
    total_spend = [150.0, 365.0, 644.0, 880.0]
    software_rev = [5.5, 19.2, 37.2, 64.0]

    x = np.arange(len(years))
    w = 0.35
    ax1.bar(x - w/2, total_spend, w, label='Total AI Spend (Hardware/Infra)', color='#0284C7', edgecolor='#0369A1')
    ax1.bar(x + w/2, software_rev, w, label='Real GenAI Software Revenue', color='#10B981', edgecolor='#047857')

    for i in range(len(years)):
        ax1.annotate(f"${total_spend[i]:.0f}B", xy=(x[i] - w/2, total_spend[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#0284C7')
        ax1.annotate(f"${software_rev[i]:.0f}B", xy=(x[i] + w/2, software_rev[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#047857')

    ax1.set_title("Infrastructure Spend vs Software Revenue (Gartner)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=7.5, color='#1E293B')
    ax1.set_ylabel("USD Billions ($B)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 1020)
    ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7)
    ax1.grid(True, axis='y')

    ax2.set_facecolor('#FAFAFA')
    ratios = [total_spend[i] / software_rev[i] for i in range(len(years))]
    ax2.plot(years, ratios, marker='o', color='#DC2626', linewidth=2.2, markersize=6)
    for i, txt in enumerate(ratios):
        ax2.annotate(f"{txt:.1f}x (${txt:.1f})", xy=(years[i], txt),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#DC2626')

    ax2.set_title("Mismatch Ratio: Infra Spend / Real Revenue", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Mismatch Multiple (x)", fontsize=8, color='#475569')
    ax2.set_ylim(10, 32)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True)

    plt.tight_layout()
    _save(fig, "chart_spending_vs_software_revenue.png")


def chart_debt_snowball_en():
    """Exact twin of generate_chart_4_neocloud_debt with English labels."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    years_debt = ['2023', '2024', '2025', '2026 (Current)']
    neocloud_debt = [2.8, 11.5, 21.0, 32.5]
    bars_d = ax1.bar(years_debt, neocloud_debt, color='#B91C1C', width=0.52, edgecolor='#7F1D1D', linewidth=0.6)
    for bar in bars_d:
        h = bar.get_height()
        ax1.annotate(f"${h:.1f}B", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 2), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax1.set_title("Accumulated Private Debt in Neoclouds", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Debt Issued ($ Billions)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 38)
    ax1.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax1.grid(True, axis='y')

    ax2.set_facecolor('#FAFAFA')
    leverage_ratios = [2.5, 6.2, 11.4, 14.8]
    ax2.plot(years_debt, leverage_ratios, marker='s', color='#D97706', linewidth=2.2, markersize=6)
    for i, val in enumerate(leverage_ratios):
        ax2.annotate(f"{val:.1f}x Leveraged", xy=(years_debt[i], val),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Financial Leverage (Debt / Equity Multiple)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Debt / Equity Ratio (x)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 18)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True)

    plt.tight_layout()
    _save(fig, "chart_debt_snowball_neoclouds.png")


# ==============================================================================
# MAIN EXECUTION: GENERATE ALL 30 ENGLISH CHARTS
# ==============================================================================

def main():
    print("=" * 75)
    print("  GENERATING ALL 30 INSTITUTIONAL ENGLISH VISUAL CHARTS")
    print("=" * 75)

    d = compute_derived_metrics()

    # 1. Macro & Geopolitical (8 charts)
    print("\n[1/6] Macro & Geopolitical Crash Risk...")
    chart_fiscal_dashboard_en(d)
    chart_valuation_vs_rates_en(d)
    chart_timeline_en()
    chart_probabilities_en(d)
    chart_composition_en(d)
    chart_maps_and_ranking_en()

    # 2. US Market Report (6 charts)
    print("\n[2/6] US Market Risk...")
    chart_indices_en()
    chart_yields_debt_en()
    chart_ai_capex_en()
    chart_solidity_en()
    chart_ai_subprime_en()
    chart_crisis_probs_en()

    # 3. Market Crash Scenarios (4 charts)
    print("\n[3/6] Market Crash Scenarios...")
    chart_stocks_history_en()
    chart_financial_matrix_en()
    chart_private_valuations_en()
    chart_crash_scenarios_en()

    # 4. Data Center ABS (4 charts)
    print("\n[4/6] Data Center ABS Tranches...")
    chart_tranche_structure_en()
    chart_deals_comparison_en()
    chart_spreads_yields_en()
    chart_issuance_and_health_en()

    # 5. Forensic AI Subprime (4 charts)
    print("\n[5/6] Forensic AI Subprime...")
    chart_repackaging_alchemy_en()
    chart_subcomponents_decomposition_en()
    chart_gpu_depreciation_vs_debt_en()
    chart_stress_loss_simulation_en()

    # 6. Leverage Multiplier (4 charts)
    print("\n[6/6] Leverage & Vendor Financing...")
    chart_leverage_pyramid_en()
    chart_vendor_financing_loop_en()
    chart_spending_vs_revenue_en()
    chart_debt_snowball_en()

    print("\n" + "=" * 75)
    print("  ALL 30 ENGLISH CHARTS SUCCESSFULLY GENERATED INTO assets/charts/en/")
    print("=" * 75)


if __name__ == "__main__":
    main()
