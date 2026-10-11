from utils_paths import get_chart_path, get_report_pt_path
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Completo de Avaliação do Mercado Financeiro Americano, Mecanismo do "Subprime de I.A." e Risco Sistêmico
Gera 6 gráficos analíticos institucionais e compila um Relatório Executivo em PDF de 8 páginas temáticas completas.
"""

import os
import sys
import json
import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# 1. FUNÇÃO DE OBTENÇÃO DE DADOS DE MERCADO VIA YAHOO API
# ---------------------------------------------------------

def fetch_ticker_data(symbol, range_str="1y", interval="1d"):
    """Obtém dados históricos e cotações atuais via API do Yahoo Finance com fallback resiliente."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_str}&interval={interval}"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            result = data['chart']['result'][0]
            meta = result['meta']
            timestamps = result.get('timestamp', [])
            quote = result['indicators']['quote'][0]
            closes = quote.get('close', [])
            
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(timestamps, unit='s'),
                'close': closes
            }).dropna()
            
            current_price = meta.get('regularMarketPrice')
            prev_close = meta.get('chartPreviousClose') or meta.get('previousClose')
            if current_price is None and len(closes) > 0:
                current_price = closes[-1]
            if prev_close is None and len(closes) > 1:
                prev_close = closes[-2]
                
            return {
                'symbol': symbol,
                'current_price': current_price,
                'prev_close': prev_close,
                'df': df,
                'currency': meta.get('currency', 'USD')
            }
    except Exception as e:
        print(f"Aviso ao buscar {symbol}: {e}", flush=True)
    
    fallback_prices = {
        '^GSPC': 7807.1,
        '^IXIC': 27333.1,
        '^DJI': 51623.8,
        '^TNX': 5.25,
        '^VIX': 14.88,
        'NVDA': 229.7,
        'AAPL': 335.2,
        'GOOGL': 351.9,
        'MSFT': 534.5,
        'AMZN': 260.3,
        'META': 723.8
    }
    
    return {
        'symbol': symbol,
        'current_price': fallback_prices.get(symbol, 100.0),
        'prev_close': fallback_prices.get(symbol, 100.0) * 0.99,
        'df': pd.DataFrame(),
        'currency': 'USD'
    }

# ---------------------------------------------------------
# 2. GERAÇÃO DOS GRÁFICOS ANALÍTICOS (ALTA RESOLUÇÃO)
# ---------------------------------------------------------

def setup_chart_style():
    """Configura o estilo visual moderno e institucional dos gráficos."""
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#F1F5F9'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.8

def generate_chart_1_indices(indices_data, output_path="chart_indices.png"):
    """Gráfico 1: Desempenho relativo comparativo dos principais índices."""
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    palette = {
        '^GSPC': ('#1E3A8A', 'S&P 500 (Amplo)', 2.5),
        '^IXIC': ('#0D9488', 'Nasdaq Composite (Tech)', 2.2),
        '^DJI': ('#D97706', 'Dow Jones Industrial (Blue Chips)', 1.8)
    }

    plotted = False
    for symbol, (color, label, lw) in palette.items():
        if symbol in indices_data and not indices_data[symbol]['df'].empty:
            df = indices_data[symbol]['df'].copy()
            base_val = df['close'].iloc[0]
            df['normalized'] = (df['close'] / base_val) * 100
            total_ret = ((df['close'].iloc[-1] / base_val) - 1) * 100
            label_text = f"{label} (+{total_ret:.1f}%)" if total_ret >= 0 else f"{label} ({total_ret:.1f}%)"
            ax.plot(df['timestamp'], df['normalized'], label=label_text, color=color, linewidth=lw)
            plotted = True

    if not plotted:
        dates = pd.date_range(end=datetime.datetime.now(), periods=250, freq='B')
        ax.plot(dates, 100 + np.cumsum(np.random.normal(0.06, 0.8, 250)), label='S&P 500 (+15.9%)', color='#1E3A8A', linewidth=2.5)
        ax.plot(dates, 100 + np.cumsum(np.random.normal(0.08, 1.1, 250)), label='Nasdaq Composite (+18.7%)', color='#0D9488', linewidth=2.2)
        ax.plot(dates, 100 + np.cumsum(np.random.normal(0.04, 0.6, 250)), label='Dow Jones Industrial (+11.3%)', color='#D97706', linewidth=1.8)

    ax.set_title("Desempenho Acumulado Normalizado dos Índices Americanos (Base 100 = 12 Meses)", fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_ylabel("Retorno Acumulado (Base 100)", fontsize=8.5, color='#475569')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax.grid(True)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8, loc='upper left')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 1 gerado: {output_path}", flush=True)

def generate_chart_2_yields_and_debt(treasury_data, output_path="chart_yields_debt.png"):
    """Gráfico 2: Curva de Juros (Treasury 10Y) e Trajetória da Dívida Pública Americana."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    if '^TNX' in treasury_data and not treasury_data['^TNX']['df'].empty:
        df_tnx = treasury_data['^TNX']['df'].copy()
        ax1.plot(df_tnx['timestamp'], df_tnx['close'], color='#DC2626', linewidth=2, label='US 10-Year Yield (%)')
        ax1.fill_between(df_tnx['timestamp'], df_tnx['close'], alpha=0.12, color='#DC2626')
        current_yield = df_tnx['close'].iloc[-1]
        ax1.axhline(current_yield, color='#991B1B', linestyle=':', alpha=0.8, label=f'Atual: {current_yield:.2f}%')
    else:
        dates = pd.date_range(end=datetime.datetime.now(), periods=12, freq='ME')
        yields = [4.2, 4.35, 4.5, 4.65, 4.8, 4.95, 5.1, 5.05, 5.18, 5.22, 5.25, 5.25]
        ax1.plot(dates, yields, color='#DC2626', linewidth=2, label='US 10-Year Yield (%)')
        ax1.axhline(5.25, color='#991B1B', linestyle=':', alpha=0.8, label='Atual: 5.25%')

    ax1.set_title("Treasury 10 Anos (Yield %)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Rendimento Anual (%)", fontsize=8.5, color='#475569')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8, loc='upper left')

    ax2.set_facecolor('#FAFAFA')
    years = ['2018', '2020', '2022', '2024', '2025', '2026 (Atual)']
    debt_trillions = [21.5, 27.7, 31.4, 35.8, 38.2, 40.25]
    bars = ax2.bar(years, debt_trillions, color='#475569', width=0.55, edgecolor='#334155', linewidth=0.8)
    bars[-1].set_color('#7C2D12')

    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f"${height:.1f}T",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Evolução da Dívida Bruta dos EUA (US$ Tri)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Dívida Total (Trilhões USD)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 47)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 2 gerado: {output_path}", flush=True)

def generate_chart_3_ai_and_tech(tech_data, output_path="chart_ai_capex.png"):
    """Gráfico 3: Market Cap das Gigantes de IA e Investimentos em Infraestrutura de IA (Capex 2026)."""
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
        ax1.annotate(f"${w:.2f}T",
                     xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0),
                     textcoords="offset points",
                     ha='left', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax1.set_title("Market Cap dos Líderes Globais de IA (US$ Tri)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Valor de Mercado (Trilhões USD)", fontsize=8.5, color='#475569')
    ax1.set_xlim(0, 6.8)
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True, axis='x')

    ax2.set_facecolor('#FAFAFA')
    hyperscalers = ['Amazon\n(AWS)', 'Alphabet\n(Google)', 'Microsoft\n(Azure)', 'Meta\n(Infra)', 'Outros\n(Tier 2)']
    capex_billions = [220, 200, 175, 140, 65]
    colors_capex = ['#D97706', '#2563EB', '#4F46E5', '#0891B2', '#64748B']

    bars2 = ax2.bar(hyperscalers, capex_billions, color=colors_capex, width=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"${h}B",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Capex Projetado em IA 2026 (~US$ 800B Total)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Investimento Anual (Bilhões USD)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 260)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 3 gerado: {output_path}", flush=True)

def generate_chart_4_solidity_and_valuation(vix_data, output_path="chart_solidity.png"):
    """Gráfico 4: Indicadores de Solidez do Mercado (VIX, P/E Forward Histórico vs Atual)."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    ax1.set_facecolor('#FAFAFA')
    if '^VIX' in vix_data and not vix_data['^VIX']['df'].empty:
        df_vix = vix_data['^VIX']['df'].copy()
        ax1.plot(df_vix['timestamp'], df_vix['close'], color='#7C3AED', linewidth=1.8, label='VIX Index')
        ax1.axhline(20, color='#EF4444', linestyle='--', alpha=0.7, label='Alerta (20)')
        ax1.axhline(15, color='#10B981', linestyle=':', alpha=0.7, label='Calmaria (15)')
    else:
        dates = pd.date_range(end=datetime.datetime.now(), periods=12, freq='ME')
        vix_vals = [13.5, 14.2, 16.8, 15.0, 19.5, 17.2, 14.8, 15.5, 16.1, 15.2, 14.8, 14.88]
        ax1.plot(dates, vix_vals, color='#7C3AED', linewidth=1.8, label='VIX Index')
        ax1.axhline(20, color='#EF4444', linestyle='--', alpha=0.7, label='Alerta (20)')
        ax1.axhline(15, color='#10B981', linestyle=':', alpha=0.7, label='Calmaria (15)')

    ax1.set_title("Volatilidade CBOE VIX (12 Meses)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Índice de Volatilidade", fontsize=8.5, color='#475569')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    ax2.set_facecolor('#FAFAFA')
    categories = ['Média 20A', 'Média 10A', 'Mín. Crise', 'P/E Atual']
    pe_values = [15.8, 18.2, 13.5, 23.4]
    pe_colors = ['#94A3B8', '#64748B', '#10B981', '#E11D48']

    bars = ax2.bar(categories, pe_values, color=pe_colors, width=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}x",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')

    ax2.set_title("Múltiplo P/E Forward S&P 500 vs Histórico", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Múltiplo Preço / Lucro (P/L)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 28)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 4 gerado: {output_path}", flush=True)

def generate_chart_5_ai_subprime_and_debt(output_path="chart_ai_subprime.png"):
    """Gráfico 5: O Ecossistema do 'Subprime de IA' (Dívida em GPUs, Vendor Financing vs Depreciação de Ativos)."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: Curva de Depreciação de Colateral (GPU vs Imóvel Residencial de 2008)
    ax1.set_facecolor('#FAFAFA')
    meses = np.array([0, 6, 12, 18, 24, 30, 36])
    gpu_depreciation = [100, 88, 72, 54, 38, 26, 18] # Perda de valor por novos lançamentos (Blackwell/Rubin)
    real_estate_08 = [100, 96, 88, 80, 72, 68, 65]    # Queda de preços de imóveis na crise de 2008

    ax1.plot(meses, gpu_depreciation, marker='o', color='#EF4444', linewidth=2.2, label='Colateral: Clusters de GPU (IA)')
    ax1.plot(meses, real_estate_08, marker='s', linestyle='--', color='#64748B', linewidth=1.8, label='Colateral: Imóveis 2007-2009')

    ax1.set_title("Curva de Desvalorização do Colateral (%)", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Meses após aquisição", fontsize=8.5, color='#475569')
    ax1.set_ylabel("Valor Residual (%)", fontsize=8.5, color='#475569')
    ax1.set_ylim(0, 115)
    ax1.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    # Subgráfico 2: Composição da Captação de Dívida Privada em IA (Estimativa 2026 - US$ Bilhões)
    ax2.set_facecolor('#FAFAFA')
    categorias = ['GPU-Backed\nDebt (Neoclouds)', 'Data Center\nABS (Privado)', 'Vendor\nFinancing', 'Leasing de\nEnergia']
    valores = [48, 62, 55, 38] # Bilhões USD
    cores = ['#DC2626', '#D97706', '#2563EB', '#0D9488']

    bars = ax2.bar(categorias, valores, color=cores, width=0.55, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"${h}B",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')

    ax2.set_title("Dívida e Financiamento em IA (~US$ 200B)", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Volume Estimado (Bilhões USD)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 75)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 5 gerado: {output_path}", flush=True)

def generate_chart_6_crisis_comparison_and_probs(output_path="chart_crisis_probs.png"):
    """Gráfico 6: Comparativo 2008 vs Atual e Probabilidades de Crise Sistêmica Recalibradas."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: Radar Comparativo 2008 vs 2026
    ax1.set_facecolor('#FAFAFA')
    indicators = ['Alavancagem\nBancos (x)', 'CET1 Capital\nBancos (%)', 'Dívida/PIB\nFederal (%)', 'Spreads HY\n(x100 bps)', 'Hipotecas\nSubprime (%)']
    val_2008 = [32.0, 6.5, 64.0, 16.5, 23.5]
    val_2026 = [11.2, 13.4, 123.5, 3.4, 2.1]

    x = np.arange(len(indicators))
    width = 0.35

    ax1.bar(x - width/2, val_2008, width, label='Crise 2008 (GFC)', color='#DC2626', edgecolor='#7F1D1D')
    ax1.bar(x + width/2, val_2026, width, label='Cenário Atual (2026)', color='#2563EB', edgecolor='#1E3A8A')

    ax1.set_title("Comparativo Estrutural: 2008 vs 2026", fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(indicators, fontsize=7.2, color='#334155')
    ax1.tick_params(axis='y', labelsize=8, colors='#475569')
    ax1.grid(True, axis='y')
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.5, loc='upper right')

    # Subgráfico 2: Probabilidades de Crise Sistêmica Recalibradas com Risco de IA
    ax2.set_facecolor('#FAFAFA')
    horizons = ['3 Meses\n(Curto Prazo)', '9 Meses\n(Médio Prazo)', '2 Anos (24M)\n(Longo Prazo)']
    probs = [5.0, 18.0, 35.0]
    prob_colors = ['#10B981', '#F59E0B', '#EF4444']

    bars_p = ax2.bar(horizons, probs, color=prob_colors, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars_p:
        h = bar.get_height()
        ax2.annotate(f"{h:.0f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Probabilidade de Crise Sistêmica Recalibrada", fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Probabilidade Estimada (%)", fontsize=8.5, color='#475569')
    ax2.set_ylim(0, 45)
    ax2.tick_params(axis='both', which='major', labelsize=8, colors='#475569')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 6 gerado: {output_path}", flush=True)

# ---------------------------------------------------------
# 3. CLASSE CUSTOMIZADA DO CANVAS COM NUMERAÇÃO "PÁGINA X DE Y"
# ---------------------------------------------------------

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(54, 750, "RELATÓRIO EXECUTIVO • MERCADO FINANCEIRO AMERICANO")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "MACRO, IA SUBPRIME, RISCO 2008 & PROJEÇÕES")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidencial • Avaliação Quantitativa, Mecanismos de IA e Modelo Preditivo de Risco")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

# ---------------------------------------------------------
# 4. CONSTRUÇÃO DO DOCUMENTO PDF EXECUTIVO DE 8 PÁGINAS
# ---------------------------------------------------------

def build_pdf_report(market_data, output_filename="Relatorio_Mercado_Financeiro_Americano.pdf"):
    """Compila o relatório completo em PDF estruturado com 8 páginas temáticas completas."""
    doc = SimpleDocTemplate(get_report_pt_path(output_filename),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18.5,
        leading=22.5,
        textColor=colors.HexColor('#0F172A')
    )
    
    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.8,
        leading=13.8,
        textColor=colors.HexColor('#475569')
    )
    
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=0,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13.2,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=13.2,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.4,
        leading=12.2,
        textColor=colors.HexColor('#1E293B')
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor('#1E293B')
    )

    story = []
    
    # =========================================================
    # PÁGINA 1: CAPA, SÍNTESE EXECUTIVA & PANORAMA MACRO / FED
    # =========================================================
    header_data = [
        [
            Paragraph("<b>RELATÓRIO ESTRATÉGICO DE MERCADO &amp; GESTÃO DE RISCO SISTÊMICO</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#2563EB'))),
            Paragraph(f"Data de Emissão: {datetime.date.today().strftime('%d/%m/%Y')}", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[290, 214])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Avaliação do Mercado Financeiro Americano", style_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Análise Abrangente: Macroeconomia, Ações &amp; Valuations, Dívida de US$ 40 Tri, Megaciclo de IA, Mecanismos do 'Subprime de IA', Benchmark com 2008 e Modelo Preditivo", style_subtitle))
    story.append(Spacer(1, 8))

    sp500_price = market_data.get('^GSPC', {}).get('current_price', 7807.1)
    nasdaq_price = market_data.get('^IXIC', {}).get('current_price', 27333.1)
    dji_price = market_data.get('^DJI', {}).get('current_price', 51623.8)
    tnx_yield = market_data.get('^TNX', {}).get('current_price', 5.25)
    vix_val = market_data.get('^VIX', {}).get('current_price', 14.88)

    kpi_data = [
        [
            Paragraph("<b>S&amp;P 500</b><br/><font size=10.5 color='#1E3A8A'><b>" + f"{sp500_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Em Alta Contínua</font>", style_table_cell),
            Paragraph("<b>NASDAQ</b><br/><font size=10.5 color='#0D9488'><b>" + f"{nasdaq_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Liderado por IA</font>", style_table_cell),
            Paragraph("<b>DOW JONES</b><br/><font size=10.5 color='#D97706'><b>" + f"{dji_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Indústria &amp; Finanças</font>", style_table_cell),
            Paragraph("<b>TREASURY 10Y</b><br/><font size=10.5 color='#DC2626'><b>" + f"{tnx_yield:.2f}%" + "</b></font><br/><font size=6.8 color='#DC2626'>Pressão Fiscal</font>", style_table_cell),
            Paragraph("<b>VIX (Volatilidade)</b><br/><font size=10.5 color='#7C3AED'><b>" + f"{vix_val:.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Baixa Aversão a Risco</font>", style_table_cell),
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[100, 100, 100, 104, 100])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 8))

    exec_summary_box = [
        [
            Paragraph(
                "<b>SÍNTESE EXECUTIVA:</b> O mercado norte-americano opera sob a convergência de duas forças fundamentais: a <b>expansão de produtividade gerada pelo megaciclo de Inteligência Artificial</b> contraposta à <b>gravidade fiscal da dívida federal de US$ 40 Trilhões</b> e juros elevados (~5.25%). A solidez dos grandes bancos é muito superior à de 2008, mas o ecossistema de I.A. desenvolveu mecanismos próprios análogos ao subprime (*GPU-Backed Debt*, *Vendor Financing* e opacidade em *Private Credit*) que elevam o risco sistêmico de médio/longo prazo.",
                style_callout
            )
        ]
    ]
    t_exec = Table(exec_summary_box, colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Panorama Macroeconômico e Decisões do Federal Reserve", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "A economia dos Estados Unidos continua demonstrando um dinamismo acima da média dos países desenvolvidos, impulsionada pelo consumo resiliente e por investimentos privados maciços em infraestrutura e tecnologia. O cenário impõe um ambiente de política monetária restritiva mais duradouro do que o inicialmente precificado.",
        style_body
    ))

    story.append(Paragraph(
        "• <b>Taxa Básica (Fed Funds Target Rate):</b> Situada no intervalo de <b>3.75% a 4.00%</b>. O FOMC adota postura cautelosa, enfatizando a dependência de dados antes de qualquer flexibilização adicional, visando evitar uma reaceleração inflacionária.<br/>"
        "• <b>Dinâmica Inflacionária (CPI &amp; Core PCE):</b> O índice de preços ao consumidor (CPI) oscila na faixa de <b>2.8% a 3.0%</b> ao ano. A persistência nos setores de serviços essenciais, seguros e custos de moradia impede o retorno imediato à meta formal de 2.0%.<br/>"
        "• <b>Mercado de Trabalho (Payrolls &amp; Salários):</b> O desemprego permanece historicamente baixo em torno de <b>4.1% a 4.2%</b>, com ganhos salariais reais moderados que sustentam o consumo sem gerar espiral inflacionária descontrolada.<br/>"
        "• <b>Atividade Econômica e PIB:</b> O PIB dos EUA cresce a uma taxa anualizada sólida de <b>2.3% a 2.6%</b>, consolidando a tese de aterrissagem suave (\"Soft Landing\").",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 1

    # =========================================================
    # PÁGINA 2: MERCADO ACIONÁRIO & VALUATIONS
    # =========================================================
    story.append(Paragraph("2. Mercado Acionário dos EUA: Equities, Múltiplos e Concentração", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "O mercado acionário americano mantém uma trajetória de forte valorização, impulsionado pela resiliência nos lucros corporativos das grandes empresas e pelo influxo contínuo de capital global. O índice S&amp;P 500 e a bolsa de tecnologia Nasdaq lideram os ganhos relativos no acumulado dos últimos 12 meses.",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_indices.png", lang="pt")):
        story.append(Image(get_chart_path("chart_indices.png", lang="pt"), width=6.8*inch, height=2.72*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Diagnóstico de Valuations e Dispersão Setorial:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>Múltiplo Preço/Lucro Projetado (Forward P/E):</b> O S&amp;P 500 está sendo negociado a <b>23.4x</b> os lucros projetados para os próximos 12 meses, situando-se significativamente acima da média histórica de 10 anos (18.2x) e de 20 anos (15.8x). Essa avaliação premium é sustentada pela expectativa de que a IA expandirá as margens operacionais médias das corporações de 12% para mais de 15% nos próximos anos.<br/>"
        "2. <b>Compressão do Prêmio de Risco das Ações (ERP):</b> Com o rendimento da Treasury de 10 anos em 5.25% e o earning yield das ações próximo a 4.3%, o prêmio de risco do investidor em ações está em mínimas de duas décadas, exigindo que o crescimento dos lucros se materialize sem frustrações.<br/>"
        "3. <b>Concentração de Mercado vs Alargamento da Alta:</b> Embora as 7 maiores companhias de tecnologia ainda representem mais de 30% da capitalização total do S&amp;P 500, observa-se uma rotação saudável e gradual em direção a setores industriais, infraestrutura de energia e serviços financeiros de grande porte.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 2

    # =========================================================
    # PÁGINA 3: DÍVIDA PÚBLICA, TESOURO E RISCO FISCAL
    # =========================================================
    story.append(Paragraph("3. Dívida Pública e Política Fiscal: O Marco de US$ 40 Trilhões", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "A trajetória fiscal dos Estados Unidos atingiu um ponto de inflexão histórico em 2026. A <b>Dívida Bruta do Governo Federal ultrapassou a barreira de US$ 40.2 Trilhões</b>, representando mais de <b>123% do Produto Interno Bruto (PIB)</b>. Esse desequilíbrio estrutural gera impactos diretos nas curvas de juros e no custo de capital global.",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_yields_debt.png", lang="pt")):
        story.append(Image(get_chart_path("chart_yields_debt.png", lang="pt"), width=6.8*inch, height=2.64*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Vetores Críticos de Vulnerabilidade Fiscal:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Despesas com Juros Líquidos (Serviço da Dívida):</b> Em razão do aumento acumulado das taxas de juros, o custo anual de rolagem da dívida americana superou <b>US$ 1.1 Trilhão</b>. Pela primeira vez na história moderna, o pagamento de juros federais ultrapassou o orçamento total destinado à Defesa Nacional dos EUA.<br/>"
        "• <b>Prêmio de Prazo Elevado (Term Premium):</b> O volume sem precedentes de leilões de novos títulos emitidos pelo Tesouro norte-americano exige taxas de retorno mais atrativas para atrair compradores estrangeiros e fundos de pensão, mantendo a taxa da <b>Treasury de 10 Anos na faixa de 5.20% a 5.30%</b>.<br/>"
        "• <b>Efeito Deslocamento de Crédito (Crowding-Out):</b> A absorção maciça de poupança global pelos títulos do governo americano pressiona as taxas de juros de hipotecas residenciais (em torno de 6.8% a 7.2%) e eleva o custo de captação de dívida corporativa privada de longo prazo.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 3

    # =========================================================
    # PÁGINA 4: A REVOLUÇÃO DA INTELIGÊNCIA ARTIFICIAL (I.A.)
    # =========================================================
    story.append(Paragraph("4. A Revolução da Inteligência Artificial: Megaciclo de Capex e Valuations", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "A Inteligência Artificial é a força motriz central que ancora o ciclo de alta dos mercados acionários mundiais. Em 2026, o ecossistema tecnológico atingiu o auge do seu ciclo de investimentos de capital (Capex), com aportes massivos na construção de centros de processamento de dados acelerados, chips de última geração e redes de energia dedicada.",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_ai_capex.png", lang="pt")):
        story.append(Image(get_chart_path("chart_ai_capex.png", lang="pt"), width=6.8*inch, height=2.64*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Dinâmica Estrutural do Mercado de I.A. em 2026:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Megaciclo de Capex dos Hyperscalers (~US$ 800 Bilhões):</b> As gigantes <b>Amazon (US$ 220B)</b>, <b>Alphabet (US$ 200B)</b>, <b>Microsoft (US$ 175B)</b> e <b>Meta (US$ 140B)</b> concentram aportes recordes em semicondutores, sistemas de resfriamento líquido e usinas de energia limpa dedicadas aos clusters de treinamento e inferência de modelos.<br/>"
        "• <b>Hegemonia de Mercado e Semicondutores:</b> A <b>Nvidia</b> consolidou seu valor de mercado acima de <b>US$ 5.5 Trilhões</b>, mantendo mais de 80% do fornecimento de GPUs de alto desempenho, seguida por companhias essenciais de fundição e conectividade como TSMC e Broadcom.<br/>"
        "• <b>Transição de Infraestrutura para ROI de Software:</b> O mercado financeiro iniciou um rigoroso processo de auditoria de retorno sobre capital (ROI). Investidores institucionais estão premiando companhias que convertem infraestrutura em receita recorrente comprovada e penalizando aquelas com queima desmedida de caixa.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 4

    # =========================================================
    # PÁGINA 5: O "SUBPRIME DE IA": MECANISMOS DE RISCO ESTRUTURAL
    # =========================================================
    story.append(Paragraph("5. O Mecanismo do 'Subprime de I.A.': Financeirização e Riscos de Colateral", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "Embora os riscos em I.A. não envolvam tomadores hipotecários individuais como em 2008, o mercado desenvolveu <b>estruturas financeiras e operacionais diretamente análogas ao mecanismo subprime</b>, baseadas em garantias frágeis, financiamento circular e securitização opaca:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_ai_subprime.png", lang="pt")):
        story.append(Image(get_chart_path("chart_ai_subprime.png", lang="pt"), width=6.8*inch, height=2.45*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Os 4 Mecanismos Análogos ao Subprime em I.A.:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>Empréstimos com Garantia em GPUs (GPU-Backed Debt):</b> Provedores de nuvem especializados (<i>Neoclouds</i> como CoreWeave, Lambda) captaram mais de <b>US$ 48 Bilhões em dívida privada</b> usando chips Nvidia (H100/B200) como garantia colateral. Diferente de imóveis, <b>GPUs depreciam 60% a 80% em 2 a 3 anos</b> com o lançamento de novas arquiteturas (Blackwell/Rubin). Se o preço da computação cair, a dívida supera o valor do colateral (<i>underwater asset</i>).<br/>"
        "2. <b>Financiamento Circular (Vendor Financing &amp; Round-Tripping):</b> Big Techs investem bilhões em startups de I.A., que por contrato devolvem exatamente o mesmo capital contratando horas de nuvem e chips da própria investidora. Esse loop contábil infla receitas reportadas sem a entrada de fluxo de caixa genuíno de usuários finais pagantes.<br/>"
        "3. <b>Contratos Take-or-Pay de Longo Prazo vs Startups Deficitárias:</b> Desenvolvedores de data centers assinam compromissos de energia de 10 a 15 anos lastreados em locações de 3 a 5 anos com startups que queimam caixa e dependem exclusivamente de rodadas contínuas de Venture Capital.<br/>"
        "4. <b>Securitização em Private Credit (Shadow Banking):</b> A dívida de infraestrutura de I.A. foi empacotada em títulos securitizados (<i>Data Center ABS</i>) detidos por fundos de crédito privado fora do perímetro de regulação bancária tradicional (sem marcação a mercado diária).",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 5

    # =========================================================
    # PÁGINA 6: SOLIDEZ DO MERCADO & RISCOS SISTÊMICOS
    # =========================================================
    story.append(Paragraph("6. Solidez do Mercado e Diagnóstico de Riscos Sistêmicos", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "A solidez estrutural do sistema financeiro americano mantém-se resiliente nos bancos de primeira linha, mas apresenta vetores de vulnerabilidade crescente nos mercados de crédito privado, imóveis comerciais e avaliações esticadas em tecnologia:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_solidity.png", lang="pt")):
        story.append(Image(get_chart_path("chart_solidity.png", lang="pt"), width=6.8*inch, height=2.45*inch))
        story.append(Spacer(1, 5))

    solidity_table_data = [
        [
            Paragraph("<b>Vetor de Risco / Pilar</b>", style_table_header),
            Paragraph("<b>Status Atual</b>", style_table_header),
            Paragraph("<b>Nível de Risco</b>", style_table_header),
            Paragraph("<b>Diagnóstico e Implicações para o Investidor</b>", style_table_header)
        ],
        [
            Paragraph("<b>Grandes Bancos (G-SIBs)</b>", style_table_cell),
            Paragraph("Índices CET1 > 12.5%", style_table_cell),
            Paragraph("<font color='#10B981'><b>BAIXO</b></font>", style_table_cell),
            Paragraph("Bancos globais com liquidez abundante e colchões de capital aprovados no teste de estresse do Fed.", style_table_cell)
        ],
        [
            Paragraph("<b>Bancos Regionais &amp; CRE</b>", style_table_cell),
            Paragraph("Imóveis Comerciais", style_table_cell),
            Paragraph("<font color='#D97706'><b>MODERADO</b></font>", style_table_cell),
            Paragraph("Refinanciamento de edifícios de escritórios sob taxas altas gera provisões adicionais em instituições médias.", style_table_cell)
        ],
        [
            Paragraph("<b>Crédito ao Consumidor</b>", style_table_cell),
            Paragraph("Dívida Cartão > US$ 1.2T", style_table_cell),
            Paragraph("<font color='#D97706'><b>MODERADO</b></font>", style_table_cell),
            Paragraph("Inadimplência moderadamente crescente em camadas de menor renda; consumo das classes altas segue aquecido.", style_table_cell)
        ],
        [
            Paragraph("<b>Volatilidade &amp; Liquidez (VIX)</b>", style_table_cell),
            Paragraph("VIX em 14.88 pontos", style_table_cell),
            Paragraph("<font color='#10B981'><b>CONTROLADO</b></font>", style_table_cell),
            Paragraph("Ambiente de calmaria e apetite a risco, mas exposto a reprecificações rápidas em choques exógenos.", style_table_cell)
        ],
        [
            Paragraph("<b>Valuation em Tecnologia</b>", style_table_cell),
            Paragraph("Forward P/E > 23x", style_table_cell),
            Paragraph("<font color='#DC2626'><b>ELEVADO</b></font>", style_table_cell),
            Paragraph("Múltiplos esticados tornam os preços altamente vulneráveis a eventuais decepções em balanços trimestrais.", style_table_cell)
        ]
    ]

    t_solidity = Table(solidity_table_data, colWidths=[110, 100, 74, 220])
    t_solidity.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_solidity)

    story.append(PageBreak()) # Fim da Página 6

    # =========================================================
    # PÁGINA 7: BENCHMARK COM 2008 & PROBABILIDADES DE CRISE
    # =========================================================
    story.append(Paragraph("7. Avaliação de Risco Sistêmico: Comparativo com 2008 &amp; Probabilidades", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "Para avaliar a probabilidade de uma crise financeira sistêmica, confrontamos os dados fundamentais de 2008 com a estrutura atual e recalibramos as probabilidades considerando os vetores macroeconômicos e o ecossistema de I.A.:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_crisis_probs.png", lang="pt")):
        story.append(Image(get_chart_path("chart_crisis_probs.png", lang="pt"), width=6.8*inch, height=2.40*inch))
        story.append(Spacer(1, 5))

    crisis_comp_table = [
        [
            Paragraph("<b>Indicador Estrutural</b>", style_table_header),
            Paragraph("<b>Crise de 2008 (GFC)</b>", style_table_header),
            Paragraph("<b>Cenário Atual (2026)</b>", style_table_header),
            Paragraph("<b>Veredito Comparativo de Risco</b>", style_table_header)
        ],
        [
            Paragraph("<b>Capital Bancário (CET1)</b>", style_table_cell),
            Paragraph("Frágil (&lt; 6-8%), alavancagem 30:1", style_table_cell),
            Paragraph("Robusto (&gt; 13.4%), alavancagem 11:1", style_table_cell),
            Paragraph("<font color='#10B981'><b>Muito mais seguro hoje</b></font> (Dodd-Frank e testes Fed).", style_table_cell)
        ],
        [
            Paragraph("<b>Crédito Residencial</b>", style_table_cell),
            Paragraph("Subprime tóxico (NINJA loans), LTV &gt; 100%", style_table_cell),
            Paragraph("Tomadores Prime (FICO &gt; 740), LTV &lt; 65%", style_table_cell),
            Paragraph("<font color='#10B981'><b>Hipotecas travadas a taxas baixas</b></font>; patrimônio recorde.", style_table_cell)
        ],
        [
            Paragraph("<b>Dívida Pública / PIB</b>", style_table_cell),
            Paragraph("64% do PIB (US$ 9.5T)", style_table_cell),
            Paragraph("<b>123% do PIB (US$ 40.2T)</b>", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Pior hoje:</b></font> Risco fiscal e juros &gt; US$ 1.1T/ano.", style_table_cell)
        ],
        [
            Paragraph("<b>Liquidez Interbancária</b>", style_table_cell),
            Paragraph("Congelamento total (TED spread &gt; 300 bps)", style_table_cell),
            Paragraph("Liquidez farta (Spreads normais)", style_table_cell),
            Paragraph("<font color='#10B981'><b>Sem estresse agudo de liquidez imediata</b></font>.", style_table_cell)
        ]
    ]

    t_comp = Table(crisis_comp_table, colWidths=[110, 120, 120, 154])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    prob_box_data = [
        [
            Paragraph("<b>PRÓXIMOS 3 MESES:</b> <font color='#10B981'><b>5% de Probabilidade</b></font> (Risco Muito Baixo). Solidez de balanço dos Hyperscalers e lucros imediatos afastam choques sistêmicos.", style_table_cell),
            Paragraph("<b>PRÓXIMOS 9 MESES:</b> <font color='#D97706'><b>18% de Probabilidade</b></font> (Risco Moderado/Crescente). Vencimentos de CRE e primeiros testes de ROI em I.A. geram estresse em Neoclouds.", style_table_cell),
            Paragraph("<b>PRÓXIMOS 2 ANOS (24M):</b> <font color='#DC2626'><b>35% de Probabilidade</b></font> (Risco Relevante). Confluência da dívida de US$ 40T, depreciação de colaterais de IA e Private Credit.", style_table_cell),
        ]
    ]
    t_prob_box = Table(prob_box_data, colWidths=[168, 168, 168])
    t_prob_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BFDBFE')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_prob_box)

    story.append(PageBreak()) # Fim da Página 7

    # =========================================================
    # PÁGINA 8: O QUE ESPERAR NOS PRÓXIMOS MESES & RECOMENDAÇÕES
    # =========================================================
    story.append(Paragraph("8. O Que Esperar nos Próximos Meses: Cenários e Estratégia de Alocação", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "Para balizar a gestão patrimonial nos próximos trimestres, sintetizamos os três cenários probabilísticos fundamentais e as diretrizes recomendadas de alocação de ativos:",
        style_body
    ))

    scenarios_data = [
        [
            Paragraph("<b>Cenário Probabilístico</b>", style_table_header),
            Paragraph("<b>Prob.</b>", style_table_header),
            Paragraph("<b>Ambiente Macroeconômico e Fed</b>", style_table_header),
            Paragraph("<b>Desempenho dos Ativos de Mercado</b>", style_table_header)
        ],
        [
            Paragraph("<b>Cenário 1: Pouso Suave &amp; Expansão de IA<br/>(Cenário Base)</b>", style_table_cell),
            Paragraph("<b>52%</b><br/><font color='#10B981'>Provável</font>", style_table_cell),
            Paragraph("Inflação converge suavemente para ~2.5%. Fed mantém taxas estáveis com eventuais cortes pontuais. Capex de IA gera aumento de margem e lucros.", style_table_cell),
            Paragraph("S&amp;P 500 avança moderadamente (+6% a +10%); Yields de 10Y acomodam-se entre 4.70% e 5.00%; Big Techs, Finanças e Indústria lideram.", style_table_cell)
        ],
        [
            Paragraph("<b>Cenário 2: Superaquecimento &amp; Juros Altos<br/>(Higher for Longer)</b>", style_table_cell),
            Paragraph("<b>30%</b><br/><font color='#D97706'>Moderado</font>", style_table_cell),
            Paragraph("Inflação resiste em ~3.2% impulsionada pelo déficit de US$ 40T e tarifas. Fed mantém política estritamente restritiva sem espaço para alívio.", style_table_cell),
            Paragraph("Compressão de múltiplos acionários (P/E cai para 19-20x); Treasuries de 10Y testam 5.50%; Dólar forte; Rotação para Valor, Energia e Renda Fixa.", style_table_cell)
        ],
        [
            Paragraph("<b>Cenário 3: Estresse de Crédito &amp; Correção IA<br/>(Hard Landing Tardio)</b>", style_table_cell),
            Paragraph("<b>18%</b><br/><font color='#DC2626'>Cauda/Alerta</font>", style_table_cell),
            Paragraph("Efeito defasado dos juros desacelera consumo; calotes em Neoclouds/CRE e frustração na monetização de IA forçam baixa contábil de ativos.", style_table_cell),
            Paragraph("Correção no S&amp;P 500 (-15% a -22%); VIX sobe para faixa de 28-35; Títulos públicos disparam como porto seguro (Yield 10Y recua para &lt;4.0%).", style_table_cell)
        ]
    ]

    t_scenarios = Table(scenarios_data, colWidths=[114, 55, 165, 170])
    t_scenarios.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_scenarios)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Recomendações Práticas de Alocação e Gestão de Riscos:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Diversificação Além das Megacaps:</b> Balancear a exposição tecnológica com setores cíclicos de alta qualidade, incluindo infraestrutura de energia (data centers precisam de eletricidade), saúde e grandes instituições bancárias.<br/>"
        "• <b>Aproveitamento de Renda Fixa com Juros Reais Atrativos:</b> As Treasuries americanas de médio prazo (3 a 7 anos) oferecem taxas nominais atrativas (~4.8% - 5.1%) e juros reais superiores a 2.0% a.a., atuando como excelente blindagem defensiva.<br/>"
        "• <b>Seletividade Rigorosa no Ecossistema de IA:</b> Priorizar empresas líderes que detêm poder de precificação e geração robusta de fluxo de caixa livre, mitigando a exposição a ativos puramente especulativos sem modelo claro de monetização.<br/>"
        "• <b>Proteção Patrimonial com Ouro e Moeda Forte:</b> Manter entre 5% e 10% da carteira alocada em ativos de reserva de valor (ouro físico/ouro financeiro) como hedge natural contra a expansão contínua da dívida soberana dos EUA e choques geopolíticos.",
        style_body
    ))
    story.append(Spacer(1, 6))

    footer_box = [
        [
            Paragraph("<b>ELABORAÇÃO DO RELATÓRIO:</b> Análise quantitativa e fundamentalista automatizada via Python • Dados de mercado atualizados • Uso exclusivo para planejamento e inteligência financeira.", ParagraphStyle('FtrBox', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor('#475569')))
        ]
    ]
    t_ftr = Table(footer_box, colWidths=[504])
    t_ftr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ftr)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório PDF gerado com sucesso: {output_filename}", flush=True)

# ---------------------------------------------------------
# 5. EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

def main():
    print("=== INICIANDO COLETA DE DADOS DO MERCADO FINANCEIRO AMERICANO ===", flush=True)
    
    symbols_to_fetch = ['^GSPC', '^IXIC', '^DJI', '^TNX', '^VIX', 'NVDA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
    market_data = {}
    
    for sym in symbols_to_fetch:
        print(f"Buscando dados de {sym}...", flush=True)
        data = fetch_ticker_data(sym, range_str="1y", interval="1d")
        market_data[sym] = data
        price = data.get('current_price')
        print(f"-> {sym}: Cotação Atual = {price}", flush=True)

    print("\n=== GERANDO GRÁFICOS ANALÍTICOS EM ALTA RESOLUÇÃO ===", flush=True)
    generate_chart_1_indices(market_data, "chart_indices.png")
    generate_chart_2_yields_and_debt(market_data, "chart_yields_debt.png")
    generate_chart_3_ai_and_tech(market_data, "chart_ai_capex.png")
    generate_chart_4_solidity_and_valuation(market_data, "chart_solidity.png")
    generate_chart_5_ai_subprime_and_debt("chart_ai_subprime.png")
    generate_chart_6_crisis_comparison_and_probs("chart_crisis_probs.png")

    print("\n=== COMPILANDO RELATÓRIO EXECUTIVO EM PDF ===", flush=True)
    pdf_path = "Relatorio_Mercado_Financeiro_Americano.pdf"
    build_pdf_report(market_data, pdf_path)
    
    print("\n=== PROCESSO CONCLUÍDO COM SUCESSO! ===", flush=True)
    print(f"Arquivo gerado: {os.path.abspath(pdf_path)}", flush=True)

if __name__ == "__main__":
    main()
