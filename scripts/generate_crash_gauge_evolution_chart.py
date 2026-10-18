#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_crash_gauge_evolution_chart.py
-----------------------------------------
Generates the bilingual timeline chart tracking the evolution of the
AI Market Crash Risk Probability Gauge (Baseline Q3-2026 vs. October 2026).

Outputs:
  - assets/charts/pt/chart_crash_probability_evolution.png
  - assets/charts/en/chart_crash_probability_evolution.png
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def generate_evolution_chart():
    setup_style()

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        # -------------------------------------------------------------
        # PANEL 1: Comparative Gauge by Scenario & Overall Risk
        # -------------------------------------------------------------
        if lang == 'pt':
            categories = [
                'Pouso Suave / Sem Quebra\n(Cenário Benigno)',
                'Cenário 1: Deflação Ordenada\n(Corte de Múltiplos)',
                'Cenário 2: Choque de Crédito & Rede\n(Gargalo de Data Centers)',
                'Cenário 3: Contágio Sistêmico\n(Dívida EUA + Taiwan)',
                'PROBABILIDADE TOTAL DE QUEBRA\n(Risco Acumulado de Estresse)'
            ]
            l_prev = 'Versão 1: Baseline Inicial (Q3-2026)'
            l_curr = 'Versão 2: Calibração Atual (Out/2026)'
            title1 = 'Evolução do Barômetro de Risco: Antes vs. Agora'
            xlabel1 = 'Probabilidade Estimada (%)'
        else:
            categories = [
                'Soft Landing / No Crash\n(Benign Scenario)',
                'Scenario 1: Orderly Deflation\n(Multiple Compression)',
                'Scenario 2: Credit & Grid Shock\n(Data Center Choke Point)',
                'Scenario 3: Systemic Contagion\n(US Debt + Taiwan Shock)',
                'OVERALL CRASH PROBABILITY\n(Cumulative Stress Risk)'
            ]
            l_prev = 'Version 1: Initial Baseline (Q3-2026)'
            l_curr = 'Version 2: Current Calibration (Oct-2026)'
            title1 = 'Risk Gauge Evolution: Baseline vs. Current'
            xlabel1 = 'Estimated Probability (%)'

        v1_probs = [70.0, 35.0, 20.0, 15.0, 30.0]
        v2_probs = [25.0, 40.0, 45.0, 30.0, 75.0]

        y = np.arange(len(categories))
        h = 0.36

        # Colors: Highlight overall risk differently
        colors_v1 = ['#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#64748B']
        colors_v2 = ['#10B981', '#F59E0B', '#EF4444', '#DC2626', '#B91C1C']

        # Plot bars
        ax1.barh(y - h/2, v1_probs, h, label=l_prev, color='#CBD5E1', edgecolor='#94A3B8')
        bars_v2 = ax1.barh(y + h/2, v2_probs, h, label=l_curr, color=colors_v2, edgecolor='#1E293B')

        # Annotations
        for i in range(len(categories)):
            ax1.annotate(f"{v1_probs[i]:.0f}%", xy=(v1_probs[i] + 1.2, y[i] - h/2),
                         ha='left', va='center', fontsize=7.5, color='#64748B', fontweight='bold')
            delta = v2_probs[i] - v1_probs[i]
            delta_str = f" ({delta:+.0f} pp)" if i != 0 else f" ({delta:+.0f} pp)"
            color_txt = '#B91C1C' if delta > 0 else '#047857'
            ax1.annotate(f"{v2_probs[i]:.0f}%{delta_str}", xy=(v2_probs[i] + 1.2, y[i] + h/2),
                         ha='left', va='center', fontsize=7.8, color=color_txt, fontweight='bold')

        ax1.set_yticks(y)
        ax1.set_yticklabels(categories, fontsize=7.2, color='#0F172A', fontweight='bold')
        ax1.set_xlim(0, 95)
        ax1.set_xlabel(xlabel1, fontsize=8.2, color='#475569', fontweight='bold')
        ax1.set_title(title1, fontsize=9.8, fontweight='bold', color='#0F172A', pad=12)
        ax1.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.0)
        ax1.grid(True, axis='x')

        # -------------------------------------------------------------
        # PANEL 2: Waterfall / Attribution of the Jump (30% -> 75%)
        # -------------------------------------------------------------
        if lang == 'pt':
            steps = [
                '1. Baseline Anterior',
                '+ Gargalo da Rede (Essex/PJM)',
                '+ Desconto Anthropic (-60%)',
                '+ CapEx $700B & Crédito Privado',
                '+ Juros Altos (10Y > 5,10%)',
                '= Probabilidade Atual'
            ]
            title2 = 'Decomposição do Aumento de Risco (+45 pp)'
            xlabel2 = 'Impacto Cumulativo na Probabilidade (%)'
        else:
            steps = [
                '1. Initial Baseline',
                '+ Grid Transmission Wall (Essex)',
                '+ Anthropic Haircut (-60%)',
                '+ $700B CapEx & Shadow Credit',
                '+ Higher-for-Longer (10Y > 5.1%)',
                '= Current Risk Gauge'
            ]
            title2 = 'Attribution of the Risk Gauge Surge (+45 pp)'
            xlabel2 = 'Cumulative Probability Impact (%)'

        step_values = [30.0, 15.0, 12.0, 10.0, 8.0, 75.0]
        cumulative  = [30.0, 45.0, 57.0, 67.0, 75.0, 75.0]
        starts      = [0.0,  30.0, 45.0, 57.0, 67.0, 0.0]

        y2 = np.arange(len(steps))
        step_colors = ['#64748B', '#F59E0B', '#EF4444', '#DC2626', '#B91C1C', '#7F1D1D']

        # Waterfall horizontal bars
        for i in range(len(steps)):
            width = step_values[i]
            left = starts[i]
            ax2.barh(y2[i], width, left=left, height=0.48, color=step_colors[i], edgecolor='#1E293B')
            
            # Label inside or next to bar
            if i == 0:
                ax2.annotate(f"30%", xy=(width/2, y2[i]), ha='center', va='center',
                             fontsize=7.8, fontweight='bold', color='#FFFFFF')
            elif i == len(steps) - 1:
                ax2.annotate(f"75% (ALERTA ELEVADO)", xy=(width/2, y2[i]), ha='center', va='center',
                             fontsize=7.8, fontweight='bold', color='#FFFFFF')
            else:
                ax2.annotate(f"+{width:.0f} pp (-> {cumulative[i]:.0f}%)", xy=(left + width + 1.2, y2[i]),
                             ha='left', va='center', fontsize=7.2, fontweight='bold', color='#B91C1C')

        ax2.set_yticks(y2)
        ax2.set_yticklabels(steps, fontsize=7.5, color='#0F172A', fontweight='bold')
        ax2.set_xlim(0, 95)
        ax2.set_xlabel(xlabel2, fontsize=8.2, color='#475569', fontweight='bold')
        ax2.set_title(title2, fontsize=9.8, fontweight='bold', color='#0F172A', pad=12)
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_crash_probability_evolution.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def main():
    print("=" * 70)
    print(" GENERATING BILINGUAL CRASH PROBABILITY EVOLUTION GAUGE CHARTS")
    print("=" * 70)
    generate_evolution_chart()
    print("Done!")

if __name__ == '__main__':
    main()
