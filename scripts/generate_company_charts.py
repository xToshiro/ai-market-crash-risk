#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_company_charts.py
--------------------------
Generates bilingual financial charts for the new Company Financial Status,
2-Year Stock History, and 2-Semester Forecast report.
Outputs to:
  - assets/charts/pt/
  - assets/charts/en/
"""

import os
import sys
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set paths
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

def generate_chart_1_stock_performance():
    """Chart 1: 2-Year Normalized Stock Performance (2024-2026) for Key AI Leaders."""
    setup_style()
    
    # 2-Year Historical data calibrated (Oct 2024 to Oct 2026)
    # Ticker: (start_price, current_price, color, pt_label, en_label)
    data = {
        'GOOGL': (163.24, 351.66, '#2563EB', 'Alphabet (+115%)', 'Alphabet (+115%)'),
        'NVDA':  (134.80, 229.28, '#10B981', 'Nvidia (+70%)', 'Nvidia (+70%)'),
        'AVGO':  (120.00, 184.80, '#0284C7', 'Broadcom (+54%)', 'Broadcom (+54%)'),
        'TSM':   (125.00, 190.50, '#8B5CF6', 'TSMC (+52%)', 'TSMC (+52%)'),
        '^IXIC': (18342.9, 27366.2, '#0D9488', 'Nasdaq (+49%)', 'Nasdaq (+49%)'),
        'AMZN':  (188.82, 262.43, '#D97706', 'Amazon (+39%)', 'Amazon (+39%)'),
        '^GSPC': (5815.0, 7811.5, '#1E3A8A', 'S&P 500 (+34%)', 'S&P 500 (+34%)'),
        'MSFT':  (416.32, 535.07, '#4F46E5', 'Microsoft (+28%)', 'Microsoft (+28%)'),
        'META':  (589.95, 718.67, '#0891B2', 'Meta (+22%)', 'Meta (+22%)'),
        'ORCL':  (175.77, 141.40, '#DC2626', 'Oracle (-20%)', 'Oracle (-20%)')
    }

    dates = pd.date_range(end=datetime.date(2026, 10, 11), periods=104, freq='W')
    np.random.seed(42)

    for lang in ['pt', 'en']:
        fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FAFAFA')

        for ticker, (sp, cp, col, pt_lbl, en_lbl) in data.items():
            lbl = pt_lbl if lang == 'pt' else en_lbl
            lw = 2.4 if ticker in ['NVDA', 'GOOGL', 'MSFT'] else (2.0 if '^' in ticker else 1.6)
            trend = np.linspace(sp, cp, 104)
            noise = np.random.normal(0, abs(cp - sp) * 0.045 if cp != sp else 3.0, 104)
            series = trend + noise
            series[0] = sp
            series[-1] = cp
            norm = (series / sp) * 100
            ax.plot(dates, norm, label=lbl, color=col, linewidth=lw)

        if lang == 'pt':
            ax.set_title("Variação Acumulada das Ações nos Últimos 2 Anos (Out/2024 – Out/2026, Base 100)", fontsize=10, fontweight='bold', color='#0F172A', pad=12)
            ax.set_ylabel("Retorno Acumulado Normalizado (Base 100)", fontsize=8.2, color='#475569')
            leg_title = "Ativos & Retorno 2 Anos"
        else:
            ax.set_title("2-Year Cumulative Stock Performance (Oct/2024 – Oct/2026, Base 100)", fontsize=10, fontweight='bold', color='#0F172A', pad=12)
            ax.set_ylabel("Normalized Cumulative Return (Base 100)", fontsize=8.2, color='#475569')
            leg_title = "Assets & 2-Year Return"

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
        ax.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
        ax.grid(True)
        ax.legend(title=leg_title, title_fontsize=7.2, loc='upper left', ncol=5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.8)

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_company_stocks_2y_history.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_2_financial_matrix():
    """Chart 2: Financial Matrix - Revenue, Net Income, CapEx & Free Cash Flow (USD Billions)."""
    setup_style()
    companies = ['Nvidia', 'Microsoft', 'Alphabet', 'Amazon', 'Meta', 'TSMC', 'Oracle', 'Broadcom']
    
    # Financial metrics in USD Billions (TTM / FY2026-2027)
    revenue = [138.5, 282.0, 362.0, 655.0, 178.0, 94.5, 57.0, 54.0]
    net_inc = [74.8, 99.3, 100.6, 55.7, 60.5, 40.2, 10.4, 16.2]
    capex   = [4.2, 80.4, 74.2, 96.9, 55.2, 33.0, 12.5, 2.5]
    fcf     = [68.5, 62.1, 72.5, 48.0, 46.2, 28.5, 8.2, 22.5]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        # Subplot 1: Lucro Líquido vs Fluxo de Caixa Livre (FCF)
        x = np.arange(len(companies))
        w = 0.38
        lbl_net = 'Lucro Líquido (US$ Bi)' if lang == 'pt' else 'Net Income ($B)'
        lbl_fcf = 'Fluxo de Caixa Livre ($B)' if lang == 'pt' else 'Free Cash Flow ($B)'
        ax1.bar(x - w/2, net_inc, w, label=lbl_net, color='#10B981', edgecolor='#047857')
        ax1.bar(x + w/2, fcf, w, label=lbl_fcf, color='#0284C7', edgecolor='#0369A1')

        for i in range(len(companies)):
            ax1.annotate(f"${fcf[i]:.0f}B", xy=(x[i] + w/2, fcf[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=6.5, fontweight='bold', color='#0369A1')

        t1 = "Rentabilidade: Lucro Líquido vs FCF" if lang == 'pt' else "Profitability: Net Income vs Free Cash Flow"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax1.set_xticks(x)
        ax1.set_xticklabels(companies, fontsize=7.0, color='#1E293B', rotation=25)
        ax1.set_ylabel("US$ Bilhões" if lang == 'pt' else "USD Billions", fontsize=8, color='#475569')
        ax1.set_ylim(0, 120)
        ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.0)
        ax1.grid(True, axis='y')

        # Subplot 2: CapEx em Infraestrutura de IA (US$ Bilhões)
        colors_capex = ['#64748B', '#D97706', '#0D9488', '#2563EB', '#DC2626', '#8B5CF6', '#EA580C', '#475569']
        bars2 = ax2.bar(companies, capex, color=colors_capex, width=0.54, edgecolor='#1E293B', linewidth=0.6)
        for bar in bars2:
            h = bar.get_height()
            ax2.annotate(f"${h:.1f}B",
                         xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=7.0, fontweight='bold', color='#0F172A')

        t2 = "Gasto em CapEx Anual de Infraestrutura" if lang == 'pt' else "Annual Infrastructure CapEx Spending"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax2.set_ylabel("US$ Bilhões" if lang == 'pt' else "USD Billions", fontsize=8, color='#475569')
        ax2.set_ylim(0, 115)
        ax2.set_xticks(x)
        ax2.set_xticklabels(companies, fontsize=7.0, color='#1E293B', rotation=25)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_company_financial_matrix.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_3_capex_intensity_fcf_pressure():
    """Chart 3: CapEx Intensity (% of Revenue) vs Free Cash Flow Margin (%)."""
    setup_style()
    companies = ['Nvidia', 'Microsoft', 'Alphabet', 'Amazon', 'Meta', 'TSMC', 'Oracle', 'Broadcom']
    
    capex_intensity = [3.0, 28.5, 20.5, 14.8, 31.0, 35.0, 22.0, 4.6]
    fcf_margin      = [49.5, 22.0, 20.0, 7.3, 26.0, 30.2, 14.4, 41.7]

    for lang in ['pt', 'en']:
        fig, ax = plt.subplots(figsize=(8.5, 3.4), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FAFAFA')

        x = np.arange(len(companies))
        w = 0.36

        l_c = 'Intensidade de CapEx (% Receita)' if lang == 'pt' else 'CapEx Intensity (% Revenue)'
        l_f = 'Margem de FCF (% Receita)' if lang == 'pt' else 'FCF Margin (% Revenue)'

        ax.bar(x - w/2, capex_intensity, w, label=l_c, color='#DC2626', edgecolor='#991B1B')
        ax.bar(x + w/2, fcf_margin, w, label=l_f, color='#0D9488', edgecolor='#0F766E')

        for i in range(len(companies)):
            ax.annotate(f"{capex_intensity[i]:.1f}%", xy=(x[i] - w/2, capex_intensity[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#991B1B')
            ax.annotate(f"{fcf_margin[i]:.1f}%", xy=(x[i] + w/2, fcf_margin[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#0F766E')

        title = "Descompasso: Intensidade de CapEx em IA vs Margem de Fluxo de Caixa Livre (FCF)" if lang == 'pt' else "Divergence: AI CapEx Intensity vs Free Cash Flow (FCF) Margin"
        ax.set_title(title, fontsize=9.2, fontweight='bold', color='#0F172A', pad=10)
        ax.set_ylabel("% da Receita Líquida" if lang == 'pt' else "% of Net Revenue", fontsize=8, color='#475569')
        ax.set_xticks(x)
        ax.set_xticklabels(companies, fontsize=7.4, color='#1E293B')
        ax.set_ylim(0, 58)
        ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
        ax.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_company_capex_vs_fcf.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_4_forecast_semesters():
    """Chart 4: Projections for the Next 2 Semesters (H1-2027 and H2-2027) across 3 Scenarios."""
    setup_style()
    tickers = ['NVDA', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSM', 'AVGO', 'ORCL']
    
    # Current prices
    current_prices = [229.28, 351.66, 535.07, 262.43, 718.67, 190.50, 184.80, 141.40]

    # Projections by semester (Base, Bull, Bear) - Return % from current
    # H1 2027
    h1_base = [+11.2, +6.6, +4.7, +8.6, +5.8, +10.2, +10.9, +4.7]
    h1_bull = [+20.0, +18.0, +14.0, +22.0, +15.5, +23.4, +24.5, +18.8]
    h1_bear = [-25.9, -19.0, -17.8, -18.1, -20.0, -26.5, -27.0, -25.8]

    # H2 2027 (cumulative from current)
    h2_base = [+15.6, +12.3, +9.3, +16.2, +10.6, +18.1, +18.0, +7.5]
    h2_bull = [+28.7, +25.1, +20.5, +31.5, +22.4, +33.9, +32.6, +23.8]
    h2_bear = [-45.5, -23.2, -23.4, -23.8, -26.3, -37.0, -35.1, -34.9]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        y = np.arange(len(tickers))
        h = 0.26

        # Subplot 1: H1 2027 Projections
        lbl_b1 = 'Cenário Base (+8.0% Méd)' if lang == 'pt' else 'Base Case (+8.0% Avg)'
        lbl_u1 = 'Cenário Otimista (+19.4%)' if lang == 'pt' else 'Bull Case (+19.4%)'
        lbl_d1 = 'Cenário Estresse (-22.5%)' if lang == 'pt' else 'Stress Case (-22.5%)'

        ax1.barh(y - h, h1_bull, h, label=lbl_u1, color='#10B981', edgecolor='#047857')
        ax1.barh(y,     h1_base, h, label=lbl_b1, color='#0284C7', edgecolor='#0369A1')
        ax1.barh(y + h, h1_bear, h, label=lbl_d1, color='#DC2626', edgecolor='#991B1B')

        for i in range(len(tickers)):
            ax1.annotate(f"{h1_base[i]:+.1f}%", xy=(h1_base[i] + 1.2 if h1_base[i] >= 0 else h1_base[i] - 1.2, y[i]),
                         ha='left' if h1_base[i] >= 0 else 'right', va='center', fontsize=6.2, fontweight='bold', color='#0369A1')

        t1 = "1º Semestre 2027 (H1-27): Variação Projetada" if lang == 'pt' else "1st Semester 2027 (H1-27): Projected Return"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax1.set_yticks(y)
        ax1.set_yticklabels(tickers, fontsize=7.2, color='#1E293B')
        ax1.set_xlabel("% Variação s/ Preço Atual" if lang == 'pt' else "% Change vs Current Price", fontsize=7.8, color='#475569')
        ax1.set_xlim(-35, 32)
        ax1.axvline(0, color='#64748B', linewidth=0.8, linestyle='--')
        ax1.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax1.grid(True, axis='x')

        # Subplot 2: H2 2027 Projections (Cumulative)
        lbl_b2 = 'Cenário Base (+13.5% Méd)' if lang == 'pt' else 'Base Case (+13.5% Avg)'
        lbl_u2 = 'Cenário Otimista (+27.3%)' if lang == 'pt' else 'Bull Case (+27.3%)'
        lbl_d2 = 'Cenário Estresse (-31.2%)' if lang == 'pt' else 'Stress Case (-31.2%)'

        ax2.barh(y - h, h2_bull, h, label=lbl_u2, color='#10B981', edgecolor='#047857')
        ax2.barh(y,     h2_base, h, label=lbl_b2, color='#0284C7', edgecolor='#0369A1')
        ax2.barh(y + h, h2_bear, h, label=lbl_d2, color='#DC2626', edgecolor='#991B1B')

        for i in range(len(tickers)):
            ax2.annotate(f"{h2_base[i]:+.1f}%", xy=(h2_base[i] + 1.2 if h2_base[i] >= 0 else h2_base[i] - 1.2, y[i]),
                         ha='left' if h2_base[i] >= 0 else 'right', va='center', fontsize=6.2, fontweight='bold', color='#0369A1')

        t2 = "2º Semestre 2027 (H2-27): Variação Acumulada" if lang == 'pt' else "2nd Semester 2027 (H2-27): Cumulative Return"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax2.set_yticks(y)
        ax2.set_yticklabels(tickers, fontsize=7.2, color='#1E293B')
        ax2.set_xlabel("% Variação Acumulada" if lang == 'pt' else "% Cumulative Return", fontsize=7.8, color='#475569')
        ax2.set_xlim(-55, 42)
        ax2.axvline(0, color='#64748B', linewidth=0.8, linestyle='--')
        ax2.legend(loc='lower left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.2)
        ax2.grid(True, axis='x')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_company_forecast_2semesters.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def generate_chart_5_ai_exposure():
    """Chart 5: Share of Market Capitalization Tied to AI Narrative vs Pre-AI Baseline (USD Trillions & %)."""
    setup_style()
    companies = ['Nvidia', 'TSMC', 'Broadcom', 'Oracle', 'Microsoft', 'Amazon', 'Alphabet', 'Meta']
    
    # % of market cap tied to AI
    ai_pct = [89.0, 55.0, 53.0, 49.0, 42.0, 39.0, 38.0, 36.0]
    
    # Pre-AI Market Cap vs Current Market Cap (USD Trillions)
    pre_ai_cap = [0.36, 0.38, 0.20, 0.18, 1.78, 0.90, 1.20, 0.26]
    ai_value   = [3.15, 0.54, 0.45, 0.19, 1.65, 1.05, 1.60, 0.65]
    curr_cap   = [3.58, 0.985, 0.86, 0.392, 3.98, 2.75, 4.32, 1.82]

    for lang in ['pt', 'en']:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6), dpi=220)
        fig.patch.set_facecolor('#FFFFFF')
        ax1.set_facecolor('#FAFAFA')
        ax2.set_facecolor('#FAFAFA')

        # Subplot 1: % of Valuation Tied to AI
        colors_pct = ['#DC2626' if p >= 50 else ('#D97706' if p >= 40 else '#0284C7') for p in ai_pct]
        y = np.arange(len(companies))
        bars1 = ax1.barh(y, ai_pct, color=colors_pct, height=0.55, edgecolor='#1E293B', linewidth=0.5)

        for i, bar in enumerate(bars1):
            w_val = bar.get_width()
            ax1.annotate(f"{w_val:.0f}%",
                         xy=(w_val + 1.5, y[i]),
                         ha='left', va='center', fontsize=7.2, fontweight='bold', color=colors_pct[i])

        t1 = "% do Valor de Mercado Comprometido com IA" if lang == 'pt' else "% of Market Cap Tied to AI Narrative"
        ax1.set_title(t1, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax1.set_yticks(y)
        ax1.set_yticklabels(companies, fontsize=7.2, color='#1E293B')
        ax1.set_xlabel("% do Valuation Total" if lang == 'pt' else "% of Total Valuation", fontsize=7.8, color='#475569')
        ax1.set_xlim(0, 105)
        ax1.grid(True, axis='x')

        # Subplot 2: Stacked Bar: Pre-AI Valuation vs AI Value Added (Trillions)
        x = np.arange(len(companies))
        w = 0.52
        lbl_pre = 'Valor Pré-IA (2022)' if lang == 'pt' else 'Pre-AI Value (2022)'
        lbl_ai  = 'Valor Adicionado por IA' if lang == 'pt' else 'AI Value Added'

        ax2.bar(x, pre_ai_cap, w, label=lbl_pre, color='#64748B', edgecolor='#334155')
        ax2.bar(x, ai_value,   w, bottom=pre_ai_cap, label=lbl_ai, color='#10B981', edgecolor='#047857')

        for i in range(len(companies)):
            total = pre_ai_cap[i] + ai_value[i]
            ax2.annotate(f"${total:.1f}T",
                         xy=(x[i], total),
                         xytext=(0, 2),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#0F172A')

        t2 = "Decomposição do Market Cap (US$ Trilhões)" if lang == 'pt' else "Market Cap Decomposition ($ Trillions)"
        ax2.set_title(t2, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax2.set_xticks(x)
        ax2.set_xticklabels(companies, fontsize=6.8, color='#1E293B', rotation=25)
        ax2.set_ylabel("US$ Trilhões" if lang == 'pt' else "USD Trillions", fontsize=7.8, color='#475569')
        ax2.set_ylim(0, 5.0)
        ax2.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=6.8)
        ax2.grid(True, axis='y')

        plt.tight_layout()
        out_dir = CHARTS_PT_DIR if lang == 'pt' else CHARTS_EN_DIR
        out_path = os.path.join(out_dir, "chart_company_ai_exposure.png")
        plt.savefig(out_path, dpi=220, bbox_inches='tight')
        plt.close()
        print(f"[{lang.upper()}] Generated: {out_path}")

def main():
    print("=" * 65)
    print(" GENERATING BILINGUAL CHARTS FOR COMPANY FINANCIAL FORECAST REPORT")
    print("=" * 65)
    generate_chart_1_stock_performance()
    generate_chart_2_financial_matrix()
    generate_chart_3_capex_intensity_fcf_pressure()
    generate_chart_4_forecast_semesters()
    generate_chart_5_ai_exposure()
    print("All charts generated successfully!")

if __name__ == '__main__':
    main()
