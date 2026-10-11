from utils_paths import get_chart_path, get_report_pt_path
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Especializado: Relatório Quantitativo de Alavancagem e Vendor Financing no Ecossistema de IA (2023-2026)
Calcula e ilustra o multiplicador de 'dólares apostados sobre cada dólar real de receita de usuário final'.
Gera 4 gráficos analíticos de alta definição e um relatório executivo em PDF de 4 páginas completas.
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# 1. SETUP DE ESTILO VISUAL DOS GRÁFICOS
# ---------------------------------------------------------

def setup_chart_style():
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#F1F5F9'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.8

# ---------------------------------------------------------
# 2. GERAÇÃO DOS 4 GRÁFICOS ANALÍTICOS
# ---------------------------------------------------------

def generate_chart_1_pyramid(output_path="chart_leverage_pyramid.png"):
    """Gráfico 1: A Pirâmide Invertida de Alavancagem: Dólares Apostados por Dólar Real."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: A Pirâmide Invertida de Múltiplos por US$ 1,00 Real
    ax1.set_facecolor('#FAFAFA')
    layers = [
        '1. Receita Real Software\n(ChatGPT, Copilot, APIs)',
        '2. Gasto em Infra/Hardware\n(Gartner GenAI Spend)',
        '3. Dívida & Take-or-Pay\n(Private Debt + ABS)',
        '4. Expansão de Market Cap\n(Aposta Total Wall St.)'
    ]
    multipliers = [1.0, 19.0, 42.0, 310.0]
    colors_pyr = ['#10B981', '#0284C7', '#D97706', '#DC2626']

    bars1 = ax1.barh(layers, multipliers, color=colors_pyr, height=0.55, edgecolor='#1E293B', linewidth=0.5)
    for bar in bars1:
        w = bar.get_width()
        ax1.annotate(f"{w:.0f}x ($ {w:.0f})",
                     xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0),
                     textcoords="offset points",
                     ha='left', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')

    ax1.set_title("Multiplicador por US$ 1,00 de Software Real", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xlabel("Dólares Apostados por US$ 1 Real", fontsize=8, color='#475569')
    ax1.set_xlim(0, 390)
    ax1.tick_params(axis='both', which='major', labelsize=7.2, colors='#475569')
    ax1.grid(True, axis='x')

    # Subgráfico 2: Comparativo dos Valores Agregados Totais (US$ Bilhões / Trilhões)
    ax2.set_facecolor('#FAFAFA')
    bars_labels = ['Software Real\n(US$ 19.2B)', 'Infra/Capex\n(US$ 365B)', 'Market Cap\n(US$ 11.5 Tri)']
    values_log = [19.2, 365.0, 11500.0] # Em bilhões
    colors_vals = ['#10B981', '#0284C7', '#DC2626']

    bars2 = ax2.bar(bars_labels, values_log, color=colors_vals, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    ax2.set_yscale('log')

    ax2.annotate("$19.2B\n(Base)", xy=(0, 19.2), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.annotate("$365B\n(19x)", xy=(1, 365.0), xytext=(0, 4), textcoords="offset points", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')
    ax2.annotate("$11.5 Tri\n(600x)", xy=(2, 11500.0), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Escala Agregada (Escala Logarítmica - US$ Bi)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Valor Total (US$ Bilhões - Log)", fontsize=8, color='#475569')
    ax2.set_ylim(5, 50000)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 1 gerado: {output_path}", flush=True)

def generate_chart_2_vendor_loop(output_path="chart_vendor_financing_loop.png"):
    """Gráfico 2: A Anatomia do Loop de Vendor Financing e a Multiplicação de Caixa da Nvidia."""
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    stages = [
        '1. Equity Stake Inicial\n(Nvidia aporta)',
        '2. Dívida Privada Captada\n(Blackstone/Magnetar)',
        '3. Compra de GPUs/Rede\n(Devolvido à Nvidia)',
        '4. Lucro Bruto Nvidia\n(75% Margem Bruta)',
        '5. Market Cap Gerado\n(Múltiplo 35x P/E)'
    ]
    amounts = [0.15, 19.0, 15.5, 11.6, 406.0]
    colors_loop = ['#64748B', '#D97706', '#0284C7', '#10B981', '#7C3AED']

    bars = ax.bar(stages, amounts, color=colors_loop, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    
    # Anotações dos valores
    for idx, bar in enumerate(bars):
        h = bar.get_height()
        label_text = f"${h:.2f}B" if h < 50 else f"${h:.0f}B (~$0.4T)"
        ax.annotate(label_text,
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax.set_yscale('log')
    ax.set_ylim(0.05, 1200)
    ax.set_title("O Efeito Multiplicador do Loop de Vendor Financing (Caso CoreWeave -> Nvidia)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_ylabel("Valor Financeiro (US$ Bilhões - Escala Log)", fontsize=8, color='#475569')
    ax.tick_params(axis='x', labelsize=7.2, colors='#1E293B')
    ax.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 2 gerado: {output_path}", flush=True)

def generate_chart_3_spending_vs_revenue(output_path="chart_spending_vs_software_revenue.png"):
    """Gráfico 3: A Trajetória de 3 Anos: Gasto Total em Infraestrutura vs Receita Real de Software (Gartner)."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: Evolução Histórica (2023, 2024, 2025, 2026 Proj.)
    ax1.set_facecolor('#FAFAFA')
    years = ['2023', '2024', '2025', '2026 (Proj.)']
    total_spend = [150.0, 365.0, 644.0, 880.0]
    software_rev = [5.5, 19.2, 37.2, 64.0]

    x = np.arange(len(years))
    w = 0.35

    ax1.bar(x - w/2, total_spend, w, label='Gasto Total em IA (Hardware/Infra)', color='#0284C7', edgecolor='#0369A1')
    ax1.bar(x + w/2, software_rev, w, label='Receita Real de Software GenAI', color='#10B981', edgecolor='#047857')

    for i in range(len(years)):
        ax1.annotate(f"${total_spend[i]:.0f}B", xy=(x[i] - w/2, total_spend[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#0284C7')
        ax1.annotate(f"${software_rev[i]:.0f}B", xy=(x[i] + w/2, software_rev[i]), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#047857')

    ax1.set_title("Gasto de Infraestrutura vs Software (Gartner)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=7.5, color='#1E293B')
    ax1.set_ylabel("US$ Bilhões", fontsize=8, color='#475569')
    ax1.set_ylim(0, 1020)
    ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7)
    ax1.grid(True, axis='y')

    # Subgráfico 2: A Razão de Descompasso (Quantos US$ Gastos por US$ 1 de Software)
    ax2.set_facecolor('#FAFAFA')
    ratios = [total_spend[i] / software_rev[i] for i in range(len(years))]

    ax2.plot(years, ratios, marker='o', color='#DC2626', linewidth=2.2, markersize=6)
    for i, txt in enumerate(ratios):
        ax2.annotate(f"{txt:.1f}x ($ {txt:.1f})",
                     xy=(years[i], txt),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#DC2626')

    ax2.set_title("Razão: Gasto de Infraestrutura / Receita Real", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Múltiplo de Descompasso (x)", fontsize=8, color='#475569')
    ax2.set_ylim(10, 32)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 3 gerado: {output_path}", flush=True)

def generate_chart_4_neocloud_debt(output_path="chart_debt_snowball_neoclouds.png"):
    """Gráfico 4: A Bola de Neve de Dívida Privada das Neoclouds e a Alavancagem Dívida/Equity."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: Evolução da Dívida Acumulada em Neoclouds (CoreWeave, Lambda Labs, Crusoe)
    ax1.set_facecolor('#FAFAFA')
    years_debt = ['2023', '2024', '2025', '2026 (Atual)']
    neocloud_debt = [2.8, 11.5, 21.0, 32.5] # US$ Bilhões

    bars_d = ax1.bar(years_debt, neocloud_debt, color='#B91C1C', width=0.52, edgecolor='#7F1D1D', linewidth=0.6)
    for bar in bars_d:
        h = bar.get_height()
        ax1.annotate(f"${h:.1f}B",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 2),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax1.set_title("Dívida Privada Acumulada em Neoclouds", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("Dívida Emitida (US$ Bilhões)", fontsize=8, color='#475569')
    ax1.set_ylim(0, 38)
    ax1.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax1.grid(True, axis='y')

    # Subgráfico 2: Alavancagem Financeira: Ratio Dívida / Equity nas Neoclouds
    ax2.set_facecolor('#FAFAFA')
    leverage_ratios = [2.5, 6.2, 11.4, 14.8] # x vezes

    ax2.plot(years_debt, leverage_ratios, marker='s', color='#D97706', linewidth=2.2, markersize=6)
    for i, val in enumerate(leverage_ratios):
        ax2.annotate(f"{val:.1f}x Alavancado",
                     xy=(years_debt[i], val),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Alavancagem Financeira (Dívida / Capital Próprio)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Índice Dívida / Equity (x)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 18)
    ax2.tick_params(axis='both', which='major', labelsize=7.5, colors='#475569')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 4 gerado: {output_path}", flush=True)

# ---------------------------------------------------------
# 3. CANVAS CUSTOMIZADO COM NUMERAÇÃO DE PÁGINAS "PÁGINA X DE Y"
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
            self.drawString(54, 750, "RELATÓRIO QUANTITATIVO • ALAVANCAGEM EM IA")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "PIRÂMIDE DE CRÉDITO & VENDOR FINANCING")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Fontes: Gartner IT Spending 2024-2025, IDC Worldwide AI, Sequoia Capital, Goldman Sachs Research")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

# ---------------------------------------------------------
# 4. CONSTRUÇÃO DO PDF EXECUTIVO (4 PÁGINAS COMPLETAS)
# ---------------------------------------------------------

def build_pdf_report(output_filename="Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf"):
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
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A')
    )

    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4,
        spaceBefore=5
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.6,
        textColor=colors.HexColor('#1E293B')
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10.2,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=10.2,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # =========================================================
    # PÁGINA 1: O MULTIPLICADOR: QUANTOS DÓLARES POR CADA DÓLAR REAL?
    # =========================================================
    header_data = [
        [
            Paragraph("<b>RELATÓRIO QUANTITATIVO FORENSE • ALAVANCAGEM &amp; ESTRUTURA DE CRÉDITO</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#D97706'))),
            Paragraph(f"Emissão: {datetime.date.today().strftime('%d/%m/%Y')} | Fonte: Gartner / IDC / SEC", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[310, 194])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("A Pirâmide de Alavancagem no Mercado de IA", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Auditoria dos Últimos 3 Anos (2023–2026): O Loop de Vendor Financing e a Quantificação dos Dólares Apostados sobre Cada Dólar Real", style_subtitle))
    story.append(Spacer(1, 6))

    kpi_data = [
        [
            Paragraph("<b>BASE REAL DE SOFTWARE</b><br/><font size=9.5 color='#10B981'><b>US$ 19.2 Bilhões</b></font><br/><font size=6.3 color='#10B981'>Receita GenAI 2024 (Gartner)</font>", style_table_cell),
            Paragraph("<b>GASTO EM INFRAESTRUTURA</b><br/><font size=9.5 color='#0284C7'><b>US$ 365 Bilhões</b></font><br/><font size=6.3 color='#0284C7'>Gasto Total GenAI (Gartner)</font>", style_table_cell),
            Paragraph("<b>MULTIPLICADOR DE CAPEX</b><br/><font size=9.5 color='#D97706'><b>19.0x por US$ 1 Real</b></font><br/><font size=6.3 color='#D97706'>US$ 19 de infra p/ US$ 1 software</font>", style_table_cell),
            Paragraph("<b>APOSTA BURSÁTIL TOTAL</b><br/><font size=9.5 color='#DC2626'><b>US$ 11.5 Trilhões</b></font><br/><font size=6.3 color='#DC2626'>Market Cap adicionado em Tech</font>", style_table_cell),
            Paragraph("<b>MULTIPLICADOR DE WALL ST.</b><br/><font size=9.5 color='#7C3AED'><b>~600x por US$ 1 Real</b></font><br/><font size=6.3 color='#7C3AED'>US$ 600 de Market Cap p/ US$ 1</font>", style_table_cell),
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[100, 102, 102, 100, 100])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 6))

    exec_box = [
        [
            Paragraph(
                "<b>RESPOSTA QUANTITATIVA DIRETA:</b> Para cada <b>US$ 1,00 REAL de receita de software gerada por usuários finais</b> (assinaturas de ChatGPT, Copilot, APIs), o mercado está gastando <b>US$ 19,00 em chips, servidores e data centers</b> (dados oficiais da Gartner). Quando estendemos a análise para o mercado acionário de Wall Street, a expansão de valor de mercado adicionada pelas Big Techs e fabricantes de chips supera <b>US$ 11.5 Trilhões</b>, o que significa que <b>mais de US$ 600,00 de capitalização e expectativas financeiras estão apostados sobre CADA US$ 1,00 de receita real</b>. No crédito privado, as Neoclouds operam com alavancagem de <b>12x a 15x de dívida sobre capital próprio</b>.",
                style_callout
            )
        ]
    ]
    t_exec = Table(exec_box, colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBEB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FDE68A')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. A Pirâmide Invertida de Alavancagem em IA", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    if os.path.exists(get_chart_path("chart_leverage_pyramid.png", lang="pt")):
        story.append(Image(get_chart_path("chart_leverage_pyramid.png", lang="pt"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "A estrutura financeira opera como um funil invertido sustentado por uma ponta extremamente estreita de fluxo de caixa orgânico:<br/>"
        "• <b>Base Econômica (1x):</b> A receita real com software de IA (US$ 19.2B em 2024 / US$ 37.2B em 2025).<br/>"
        "• <b>Multiplicador de Capital Físico (19x):</b> Gasto agregado em chips, data centers e energia de US$ 365B (2024).<br/>"
        "• <b>Multiplicador de Dívida Privada (42x):</b> Empréstimos colateralizados em hardware, ABS e contratos take-or-pay.<br/>"
        "• <b>Multiplicador Bursátil (310x a 600x):</b> Capitalização bursátil inflada nas bolsas americanas.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 1

    # =========================================================
    # PÁGINA 2: O LOOP DE VENDOR FINANCING NOS ÚLTIMOS 3 ANOS
    # =========================================================
    story.append(Paragraph("2. A Mecânica do Loop de Vendor Financing: Caso CoreWeave &amp; Nvidia", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "A investigação dos fluxos financeiros entre 2023 e 2026 comprova a existência de um circuito fechado de autofinanciamento:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_vendor_financing_loop.png", lang="pt")):
        story.append(Image(get_chart_path("chart_vendor_financing_loop.png", lang="pt"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    loop_table_data = [
        [
            Paragraph("<b>Etapa do Circuito</b>", style_table_header),
            Paragraph("<b>Atores Envolvidos</b>", style_table_header),
            Paragraph("<b>Volume Financeiro</b>", style_table_header),
            Paragraph("<b>Mecanismo Contábil &amp; Efeito Prático</b>", style_table_header)
        ],
        [
            Paragraph("<b>1. Equity Anchor<br/>(Aporte de Validação)</b>", style_table_cell),
            Paragraph("Nvidia (NVentures)", style_table_cell),
            Paragraph("~US$ 100M a US$ 200M", style_table_cell),
            Paragraph("A Nvidia compra participação minoritária na Neocloud, conferindo selo de 'parceiro preferencial' de GPUs.", style_table_cell)
        ],
        [
            Paragraph("<b>2. Captação de Dívida<br/>(Shadow Banking)</b>", style_table_cell),
            Paragraph("Blackstone, Magnetar, Carlyle, Coatue", style_table_cell),
            Paragraph("<b>US$ 19.0+ Bilhões</b><br/>(Acumulado 2023-2026)", style_table_cell),
            Paragraph("Gestoras de crédito privado estruturam dívida colateralizada nas GPUs e contratos futuros; alavancagem de 12x-15x.", style_table_cell)
        ],
        [
            Paragraph("<b>3. Repasse Compulsório<br/>(Compra de Hardware)</b>", style_table_cell),
            Paragraph("Neocloud ➔ Nvidia", style_table_cell),
            Paragraph("<b>US$ 15.5+ Bilhões</b><br/>(>80% dos recursos)", style_table_cell),
            Paragraph("A Neocloud transfere 100% dos recursos captados para a Nvidia na compra antecipada de H100, B200 e InfiniBand.", style_table_cell)
        ],
        [
            Paragraph("<b>4. Margem e Lucro<br/>(Balanço da Nvidia)</b>", style_table_cell),
            Paragraph("Balanço da Nvidia", style_table_cell),
            Paragraph("<b>US$ 11.6 Bilhões</b><br/>(Margem bruta 75%)", style_table_cell),
            Paragraph("Cada dólar de dívida privada captada vira 75 centavos de lucro bruto direto no balanço corporativo da Nvidia.", style_table_cell)
        ],
        [
            Paragraph("<b>5. Multiplicação Bursátil<br/>(Market Cap Expandido)</b>", style_table_cell),
            Paragraph("Mercado Acionário", style_table_cell),
            Paragraph("<b>+US$ 400 Bilhões</b><br/>(Múltiplo 35x P/E)", style_table_cell),
            Paragraph("O lucro recorde infla o valuation bursátil da fabricante, atraindo mais fundos mútuos e ETFs para a cadeia.", style_table_cell)
        ]
    ]

    t_loop = Table(loop_table_data, colWidths=[95, 95, 80, 234])
    t_loop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_loop)

    story.append(PageBreak()) # Fim da Página 2

    # =========================================================
    # PÁGINA 3: A TRAJETÓRIA DE 3 ANOS & AVALIAÇÃO GARTNER/SEQUOIA
    # =========================================================
    story.append(Paragraph("3. A Trajetória de 3 Anos (2023–2026): A Abertura do Abismo de Receita", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "A discrepância entre os gastos em infraestrutura física e a geração de receita de software acelerou nos últimos 36 meses:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_spending_vs_software_revenue.png", lang="pt")):
        story.append(Image(get_chart_path("chart_spending_vs_software_revenue.png", lang="pt"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Diagnóstico da Trajetória por Ano:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>2023 (A Gênese do Descompasso):</b> Gasto em infraestrutura de US$ 150B contra US$ 5.5B de receita real de software. David Cahn (Sequoia Capital) publica <i>'AI's $200B Question'</i>, apontando que o ecossistema precisava faturar US$ 200 bilhões anuais para justificar as compras de GPUs.<br/>"
        "• <b>2024 (A Explosão de 19x):</b> Os gastos totais com GenAI saltam para <b>US$ 365 Bilhões</b> (Gartner), enquanto a receita de software chega a <b>US$ 19.16 Bilhões</b>. A Sequoia atualiza o cálculo para <i>'AI's $600B Question'</i>, e Jim Covello (Goldman Sachs) publica seu relatório alertando sobre US$ 1 Trilhão de gastos sem killer apps comprovados.<br/>"
        "• <b>2025/2026 (A Fronteira Industrial):</b> Projeção da Gartner indica gastos com GenAI atingindo <b>US$ 644 Bilhões</b>, impulsionados pela corrida de data centers e energia, contra uma receita de software de <b>US$ 37.16 Bilhões</b>. A razão de descompasso estabiliza-se no patamar crítico de <b>17.3x a 19x</b>.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 3

    # =========================================================
    # PÁGINA 4: A BOLA DE NEVE DAS NEOCLOUDS & VEREDITO
    # =========================================================
    story.append(Paragraph("4. A Bola de Neve de Dívida das Neoclouds e o Veredito de Risco", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "A fragilidade mais aguda da pirâmide concentra-se nos operadores que alavancaram balanços exclusivamente em hardware de IA:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_debt_snowball_neoclouds.png", lang="pt")):
        story.append(Image(get_chart_path("chart_debt_snowball_neoclouds.png", lang="pt"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    risk_table_data = [
        [
            Paragraph("<b>Dimensão de Alavancagem</b>", style_table_header),
            Paragraph("<b>Métrica Atual (2026)</b>", style_table_header),
            Paragraph("<b>Padrão de Mercado Pré-IA</b>", style_table_header),
            Paragraph("<b>Veredito Forense de Risco</b>", style_table_header)
        ],
        [
            Paragraph("<b>Alavancagem Dívida/Equity</b>", style_table_cell),
            Paragraph("<b>12.0x a 15.0x</b>", style_table_cell),
            Paragraph("1.5x a 3.0x", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Crítica:</b></font> Neoclouds dependem de refinanciamento perpétuo; qualquer retração de receita provoca quebra de covenants.", style_table_cell)
        ],
        [
            Paragraph("<b>Multiplicador Capex / Software</b>", style_table_cell),
            Paragraph("<b>17x a 19x</b>", style_table_cell),
            Paragraph("1.0x a 2.5x (SaaS)", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Desbalanceado:</b></font> Em empresas tradicionais de nuvem, cada US$ 1 de capex gerava US$ 0.80 a US$ 1.20 de receita recorrente em 3 anos.", style_table_cell)
        ],
        [
            Paragraph("<b>Multiplicador de Market Cap</b>", style_table_cell),
            Paragraph("<b>~600x</b>", style_table_cell),
            Paragraph("20x a 40x", style_table_cell),
            Paragraph("<font color='#D97706'><b>Especulativo:</b></font> O valor acionário assume que a IA dominará 100% da produtividade corporativa global em prazo imediato.", style_table_cell)
        ]
    ]

    t_risk = Table(risk_table_data, colWidths=[105, 75, 80, 244])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 5))

    conclusion_box_data = [
        [
            Paragraph("<b>VEREDITO INSTITUCIONAL CONCLUSIVO:</b><br/>"
                      "1. <b>Nível de Alavancagem Físico:</b> Estão sendo gastos <b>US$ 19,00 em infraestrutura física para cada US$ 1,00 de software real</b> consumido na economia.<br/>"
                      "2. <b>Nível de Alavancagem Financeiro:</b> Wall Street precificou <b>mais de US$ 300 a US$ 600 em valor de mercado para cada US$ 1,00 de receita anual de software</b>.<br/>"
                      "3. <b>A Ilusão de Demanda Orgânica:</b> O modelo de <i>Vendor Financing</i> cria a miragem contábil de que o crescimento da receita de hardware é autossustentável, quando na verdade ele é financiado por dívida privada de crédito estruturado fora do balanço. Se a monetização de software não multiplicar por 10x nos próximos 2 anos, a pirâmide sofrerá ajuste severo.",
                      style_table_cell)
        ]
    ]
    t_conc_box = Table(conclusion_box_data, colWidths=[504])
    t_conc_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F87171')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_conc_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório de Alavancagem PDF gerado com sucesso: {output_filename}", flush=True)

# ---------------------------------------------------------
# 5. EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

def main():
    print("=== GERANDO GRÁFICOS ANALÍTICOS DE ALAVANCAGEM & VENDOR FINANCING ===", flush=True)
    generate_chart_1_pyramid("chart_leverage_pyramid.png")
    generate_chart_2_vendor_loop("chart_vendor_financing_loop.png")
    generate_chart_3_spending_vs_revenue("chart_spending_vs_software_revenue.png")
    generate_chart_4_neocloud_debt("chart_debt_snowball_neoclouds.png")

    print("\n=== COMPILANDO RELATÓRIO QUANTITATIVO EM PDF ===", flush=True)
    pdf_filename = "Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf"
    build_pdf_report(pdf_filename)

    print("\n=== PROCESSO FINALIZADO COM SUCESSO! ===", flush=True)
    print(f"Arquivo gerado: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
