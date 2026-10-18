#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_recent_market_update_charts.py
---------------------------------------
Generates bilingual financial & technical charts for the October 2026 Market Update:
1. Data Center Grid Bottleneck & Interconnection Delays (Loughton & Global 2030s Cliff).
2. Anthropic Revenue Growth Deceleration vs IPO Valuation Haircut ($2.0T -> $1.5T).
3. Hyperscaler CapEx Supercycle ($700B Run-Rate) vs Off-Balance Sheet Private Credit.
4. Recalibrated Crash & Stress Probabilities (2026-2029) incorporating Power & Credit Friction.

Outputs to:
  - assets/charts/pt/
  - assets/charts/en/
"""

import os
import sys
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

def generate_chart_1_grid_bottlenecks():
    """Chart 1: Data Center Power Grid Bottlenecks, Lead Times & Interconnection Cliff."""
    setup_style()
    years = ['2023', '2024', '2025', '2026 (Atual)', '2027 (Proj)', '2028 (Proj)', '2029 (Proj)', '2030+']
    years_en = ['2023', '2024', '2025', '2026 (Current)', '2027 (Proj)', '2028 (Proj)', '2029 (Proj)', '2030+']
    
    # In Gigawatts (GW) - Planned vs Actually Energized Capacity in NA & Europe
    planned_gw   = [12.0, 24.5, 42.0, 68.0, 95.0, 128.0, 160.0, 195.0]
    energized_gw = [10.5, 18.0, 26.5, 36.0, 48.0,  62.0,  78.0,  96.0]
    deficit_gw   = [p - e for p, e in zip(planned_gw, energized_gw)]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        x = np.arange(len(years))
        w = 0.40
        x_labels = years if lang == 'pt' else years_en

        l_plan = 'Capacidade de IA Planejada (GW)' if lang == 'pt' else 'Planned AI Capacity (GW)'
        l_ener = 'Capacidade Efetivamente Energizada (GW)' if lang == 'pt' else 'Actually Energized Capacity (GW)'

        ax1.bar(x - w/2, planned_gw, w, label=l_plan, color='#64748B', edgecolor='#334155')
        ax1.bar(x + w/2, energized_gw, w, label=l_ener, color='#10B981', edgecolor='#047857')

        for i in range(len(years)):
            if i >= 3:
                ax1.annotate(f"-{deficit_gw[i]:.0f}GW", xy=(x[i] - w/2, planned_gw[i]),
                             xytext=(0, 2), textcoords="offset points", ha='center', va='bottom',
                             fontsize=6.2, fontweight='bold', color='#DC2626')

        t1 = "Gargalo da Rede: Demanda de IA vs Capacidade Energizada" if lang == 'pt' else "The Grid Wall: Planned AI Demand vs Energized Capacity"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("Gigawatts (GW)" if lang == 'pt' else "Gigawatts (GW)", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, fontsize=6.8, rotation=25, color='#1E293B')
        ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.5)
        ax1.grid(True, axis='y')

        # Subplot 2: Equipamentos Críticos e Prazos de Fila (Lead Times em Meses)
        equip = ['Transformadores GSU', 'Disjuntores Alta Tensão', 'Subestações Dedicadas', 'Licenciamento e Linha', 'Caso Essex (Nscale)'] if lang == 'pt' else ['GSU Transformers', 'High-Voltage Switchgear', 'Dedicated Substations', 'Grid Permitting & Lines', 'Essex Case (Nscale)']
        lead_2021 = [18, 12, 24, 24, 24]
        lead_2026 = [54, 38, 48, 60, 84]

        y = np.arange(len(equip))
        h = 0.35

        l21 = 'Tempo Médio em 2021 (Meses)' if lang == 'pt' else 'Average Lead Time 2021 (Months)'
        l26 = 'Tempo Médio em 2026 (Meses)' if lang == 'pt' else 'Average Lead Time 2026 (Months)'

        ax2.barh(y - h/2, lead_2021, h, label=l21, color='#94A3B8', edgecolor='#475569')
        ax2.barh(y + h/2, lead_2026, h, label=l26, color='#DC2626', edgecolor='#991B1B')

        for i in range(len(equip)):
            ax2.annotate(f"{lead_2026[i]}m", xy=(lead_2026[i] + 1.5, y[i] + h/2),
                         ha='left', va='center', fontsize=6.8, fontweight='bold', color='#DC2626')

        t2 = "Fila de Espera de Conexão e Equipamentos (Meses)" if lang == 'pt' else "Supply Chain Lead Times & Grid Delays (Months)"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_yticks(y)
        ax2.set_yticklabels(equip, fontsize=7.0, color='#1E293B')
        ax2.set_xlabel("Prazo de Entrega / Interconexão (Meses)" if lang == 'pt' else "Lead Time / Interconnection (Months)", fontsize=7.8, color='#475569')
        ax2.set_xlim(0, 98)
        ax2.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.5)
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_grid_bottleneck_delays.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_2_anthropic_valuation_and_revenue():
    """Chart 2: Anthropic Quarterly Revenue Deceleration and IPO Valuation Haircut."""
    setup_style()
    quarters = ['Q1-2026', 'Q2-2026', 'Q3-2026']
    rev_billions = [4.7, 11.6, 16.8]
    growth_qoq = [None, 146.8, 44.8]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        # Subplot 1: Trajetória de Receita Trimestral e Desaceleração
        x = np.arange(len(quarters))
        bars = ax1.bar(x, rev_billions, color=['#3B82F6', '#2563EB', '#1D4ED8'], width=0.48, edgecolor='#1E3A8A')
        for i, bar in enumerate(bars):
            h = bar.get_height()
            ax1.annotate(f"${h:.1f}B", xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3),
                         textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
            if growth_qoq[i] is not None:
                lbl_g = f"+{growth_qoq[i]:.1f}% QoQ"
                col_g = '#10B981' if growth_qoq[i] > 100 else '#D97706'
                ax1.annotate(lbl_g, xy=(bar.get_x() + bar.get_width()/2, h/2), ha='center', va='center',
                             fontsize=7.2, fontweight='bold', color='#FFFFFF', bbox=dict(boxstyle="round,pad=0.2", facecolor=col_g, edgecolor="none"))

        t1 = "Anthropic: Receita Trimestral e Desaceleração (QoQ)" if lang == 'pt' else "Anthropic: Quarterly Revenue & QoQ Growth Deceleration"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("US$ Bilhões" if lang == 'pt' else "USD Billions", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(quarters, fontsize=7.5, color='#1E293B')
        ax1.set_ylim(0, 21)
        ax1.grid(True, axis='y')

        # Subplot 2: Corte no Valuation-Alvo de IPO ($2.0T -> $1.5T)
        categories = ['Expectativa Inicial (Pico)', 'Avaliação Revisada (Pré-IPO)', 'Corte de Capitalização'] if lang == 'pt' else ['Peak Target Expectation', 'Revised Valuation (Pre-IPO)', 'Valuation Haircut']
        values = [2.0, 1.5, -0.5]
        colors_val = ['#64748B', '#0284C7', '#DC2626']

        y = np.arange(len(categories))
        bars2 = ax2.barh(y, [abs(v) for v in values], height=0.48, color=colors_val, edgecolor='#1E293B', linewidth=0.6)
        for i, bar in enumerate(bars2):
            w = bar.get_width()
            txt = f"${w:.1f}T" if i < 2 else f"-${w:.1f}T (-25%)"
            ax2.annotate(txt, xy=(w + 0.05, y[i]), ha='left', va='center', fontsize=7.5, fontweight='bold', color=colors_val[i])

        t2 = "Revisão do Valuation de IPO da Anthropic (Nov/2026)" if lang == 'pt' else "Anthropic IPO Target Valuation Haircut (Nov/2026)"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_yticks(y)
        ax2.set_yticklabels(categories, fontsize=7.2, color='#1E293B')
        ax2.set_xlabel("US$ Trilhões" if lang == 'pt' else "USD Trillions", fontsize=8, color='#475569')
        ax2.set_xlim(0, 2.5)
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_anthropic_growth_deceleration_valuation.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_3_capex_and_private_credit():
    """Chart 3: Hyperscaler $700B CapEx Run-Rate vs Shift to Off-Balance Private Credit & ABS."""
    setup_style()
    years = ['2023', '2024', '2025', '2026 (Atual)', '2027 (Proj)']
    
    # CapEx breakdown in USD Billions
    balance_sheet_capex = [140, 220, 310, 390, 420]
    off_balance_credit  = [ 35,  95, 185, 290, 380] # SPVs, Private Credit, Data Center ABS

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        # Subplot 1: Stacked Bar: On-Balance vs Off-Balance CapEx
        x = np.arange(len(years))
        w = 0.50
        l_on  = 'CapEx Direto no Balanço (Bonds/Caixa)' if lang == 'pt' else 'On-Balance CapEx (Corporate Debt/Cash)'
        l_off = 'Estruturação Fora de Balanço (Crédito Privado / SPVs)' if lang == 'pt' else 'Off-Balance Structuring (Private Credit / SPVs)'

        ax1.bar(x, balance_sheet_capex, w, label=l_on, color='#1E3A8A', edgecolor='#0F172A')
        ax1.bar(x, off_balance_credit, w, bottom=balance_sheet_capex, label=l_off, color='#D97706', edgecolor='#78350F')

        for i in range(len(years)):
            tot = balance_sheet_capex[i] + off_balance_credit[i]
            ax1.annotate(f"${tot:.0f}B", xy=(x[i], tot), xytext=(0, 2), textcoords="offset points",
                         ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')

        t1 = "Superciclo de CapEx: Migração para Veículos Fora de Balanço" if lang == 'pt' else "CapEx Supercycle: Migration to Off-Balance Sheet SPVs"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_ylabel("US$ Bilhões / Ano" if lang == 'pt' else "USD Billions / Year", fontsize=8, color='#475569')
        ax1.set_xticks(x)
        ax1.set_xticklabels(years, fontsize=7.0, color='#1E293B')
        ax1.set_ylim(0, 860)
        ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True, axis='y')

        # Subplot 2: Participação de Gestoras de Crédito Privado e Parcerias
        managers = ['Blackstone', 'BlackRock/GIP (GAIIP)', 'Blue Owl', 'Apollo', 'Magnetar / Coatue', 'Carlyle']
        commitments = [75.0, 100.0, 45.0, 50.0, 35.0, 28.0] # Commitments in AI Infrastructure & DC Debt ($B)
        
        y = np.arange(len(managers))
        bars2 = ax2.barh(y, commitments, height=0.52, color='#0D9488', edgecolor='#115E59')
        for i, bar in enumerate(bars2):
            w_val = bar.get_width()
            ax2.annotate(f"${w_val:.0f}B", xy=(w_val + 1.5, y[i]), ha='left', va='center',
                         fontsize=7.0, fontweight='bold', color='#0F766E')

        t2 = "Compromissos em Infraestrutura de IA e Dívida (US$ Bi)" if lang == 'pt' else "AI Infrastructure Debt Commitments ($B)"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_yticks(y)
        ax2.set_yticklabels(managers, fontsize=7.0, color='#1E293B')
        ax2.set_xlabel("US$ Bilhões Comprometidos" if lang == 'pt' else "USD Billions Committed", fontsize=7.8, color='#475569')
        ax2.set_xlim(0, 115)
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_hyperscaler_capex_vs_private_credit.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_4_updated_crash_probabilities():
    """Chart 4: Recalibrated Crash & Stress Probabilities (2026-2029) Incorporating Grid & Credit Wall."""
    setup_style()
    scenarios_pt = [
        'Cenário 1: Desaceleração Ordenada\n(CapEx modera; P/E contrai 10%)',
        'Cenário 2: Choque de Crédito & Fila da Rede\n(Gargalo elétrico + inadimplência Neoclouds)',
        'Cenário 3: Tempestade Perfeita Sistêmica\n(Tesouro US$ 40T + Taiwan + Falhas ABS)'
    ]
    scenarios_en = [
        'Scenario 1: Orderly Deceleration\n(CapEx moderates; P/E contracts 10%)',
        'Scenario 2: Credit Shock & Grid Bottleneck\n(Electrical delays + Neocloud defaults)',
        'Scenario 3: Systemic Perfect Storm\n(US $40T Debt + Taiwan + ABS Failures)'
    ]
    
    # Previous probabilities vs Updated probabilities
    prev_probs = [48.0, 34.0, 18.0]
    upd_probs  = [42.0, 40.0, 18.0] # Credit & Grid shock probability increased by 6 pp!

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        scenarios = scenarios_pt if lang == 'pt' else scenarios_en
        y = np.arange(len(scenarios))
        h = 0.32

        l_prev = 'Projeção Anterior' if lang == 'pt' else 'Previous Projection'
        l_upd  = 'Projeção Atualizada (Out/2026)' if lang == 'pt' else 'Updated Projection (Oct/2026)'

        ax1.barh(y - h/2, prev_probs, h, label=l_prev, color='#94A3B8', edgecolor='#475569')
        ax1.barh(y + h/2, upd_probs,  h, label=l_upd,  color='#DC2626', edgecolor='#991B1B')

        for i in range(len(scenarios)):
            ax1.annotate(f"{upd_probs[i]:.0f}%", xy=(upd_probs[i] + 1.0, y[i] + h/2),
                         ha='left', va='center', fontsize=7.2, fontweight='bold', color='#DC2626')
            ax1.annotate(f"{prev_probs[i]:.0f}%", xy=(prev_probs[i] + 1.0, y[i] - h/2),
                         ha='left', va='center', fontsize=6.8, color='#475569')

        t1 = "Recalibração das Probabilidades de Quebra (2026–2029)" if lang == 'pt' else "Recalibrated Market Crash Probabilities (2026–2029)"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax1.set_yticks(y)
        ax1.set_yticklabels(scenarios, fontsize=6.8, color='#1E293B')
        ax1.set_xlabel("Probabilidade Acumulada (%)" if lang == 'pt' else "Cumulative Probability (%)", fontsize=7.8, color='#475569')
        ax1.set_xlim(0, 52)
        ax1.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.5)
        ax1.grid(True, axis='x')

        # Subplot 2: Quedas Estimadas no Cenário de Choque de Crédito & Grid (Cenário 2 Atualizado)
        assets = ['Nvidia (NVDA)', 'TSMC (TSM)', 'Neoclouds / Nscale', 'Nasdaq 100', 'S&P 500', 'Private Credit Junior Tranches'] if lang == 'pt' else ['Nvidia (NVDA)', 'TSMC (TSM)', 'Neoclouds / Nscale', 'Nasdaq 100', 'S&P 500', 'Private Credit Junior Tranches']
        drawdowns = [-55.0, -42.0, -75.0, -38.0, -28.0, -45.0]

        y2 = np.arange(len(assets))
        bars2 = ax2.barh(y2, drawdowns, height=0.52, color='#B91C1C', edgecolor='#7F1D1D')
        for i, bar in enumerate(bars2):
            w_val = bar.get_width()
            ax2.annotate(f"{w_val:.0f}%", xy=(w_val - 1.2, y2[i]), ha='right', va='center',
                         fontsize=7.0, fontweight='bold', color='#FFFFFF')

        t2 = "Impacto Projetado no Cenário de Choque de Crédito/Grid" if lang == 'pt' else "Projected Impact under Credit & Grid Shock"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax2.set_yticks(y2)
        ax2.set_yticklabels(assets, fontsize=7.0, color='#1E293B')
        ax2.set_xlabel("Variação Projetada (%)" if lang == 'pt' else "Projected Drawdown (%)", fontsize=7.8, color='#475569')
        ax2.set_xlim(-85, 5)
        ax2.axvline(0, color='#64748B', linewidth=0.8, linestyle='--')
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_updated_crash_probabilities_2026_2029.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def main():
    print("=" * 70)
    print(" GENERATING BILINGUAL CHARTS FOR RECENT MARKET UPDATE REPORT")
    print("=" * 70)
    generate_chart_1_grid_bottlenecks()
    generate_chart_2_anthropic_valuation_and_revenue()
    generate_chart_3_capex_and_private_credit()
    generate_chart_4_updated_crash_probabilities()
    print("All recent update charts generated successfully!")

if __name__ == '__main__':
    main()
