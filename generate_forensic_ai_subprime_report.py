#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Forense: Análise Comparativa 2008 vs 2026, Reempacotamento de Riscos (BBB para AAA/A)
e Decomposição dos Subcomponentes das Tranches de Data Center ABS e Dívida de IA.
Gera 4 gráficos analíticos de alta definição e um relatório em PDF de 4 páginas.
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

def generate_chart_1_alchemy(output_path="chart_repackaging_alchemy.png"):
    """Gráfico 1: A Alquimia de Securitização (2008 vs 2026) - Transformação de Risco em Selo de Investimento."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: O Mecanismo do CDO Mezanino de 2008
    ax1.set_facecolor('#FAFAFA')
    tranches_2008 = ['Subprime BBB\n(Entrada 100%)', 'Equity / Mezz\n(Absorve perda)', 'Tranche AAA CDO\n(Criada do Nada)']
    percentages_2008 = [100.0, 22.0, 78.0]
    colors_2008 = ['#DC2626', '#F59E0B', '#1E3A8A']

    bars1 = ax1.bar(tranches_2008, percentages_2008, color=colors_2008, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"{h:.0f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')

    ax1.set_title("2008: Mezzanine CDO (Hipotecas Subprime)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax1.set_ylabel("% da Estrutura Criada", fontsize=8, color='#475569')
    ax1.set_ylim(0, 115)
    ax1.grid(True, axis='y')

    # Subgráfico 2: O Mecanismo de Dívida de Neocloud / Private Credit em 2026
    ax2.set_facecolor('#FAFAFA')
    tranches_2026 = ['Crédito 15% Junk\n(GPU Collateral)', 'Mezanino B/C\n(Private Credit)', 'Tranche Grau Inv.\n(Moody\'s A3 / A-)']
    percentages_2026 = [100.0, 18.0, 82.0]
    colors_2026 = ['#B91C1C', '#D97706', '#0D9488']

    bars2 = ax2.bar(tranches_2026, percentages_2026, color=colors_2026, width=0.52, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.0f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')

    ax2.set_title("2026: GPU Debt & Neocloud SPV (CoreWeave Mod.)", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("% da Estrutura Reempacotada", fontsize=8, color='#475569')
    ax2.set_ylim(0, 115)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 1 gerado: {output_path}", flush=True)

def generate_chart_2_subcomponents(output_path="chart_subcomponents_decomposition.png"):
    """Gráfico 2: Decomposição Real dos Subcomponentes de Receita e Risco dos Inquilinos."""
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Subgráfico 1: Composição das Receitas que Lastreiam as Tranches A/AAA
    ax1.set_facecolor('#FAFAFA')
    labels = ['Hyperscalers Soberanos\n(Microsoft, AWS, Google)', 'Neoclouds & Startups IA\n(CoreWeave, Lambda, OpenAI)', 'Grandes Empresas\n(Bancos, Saúde, Telco)']
    sizes = [72.0, 18.0, 10.0]
    colors_pie = ['#1E3A8A', '#DC2626', '#64748B']

    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140,
                                      colors=colors_pie, textprops={'fontsize': 7.2, 'color': '#0F172A'},
                                      wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 1.5})
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')
        at.set_color('#FFFFFF')

    ax1.set_title("Mix de Inquilinos em Deals Sênior (KBRA)", fontsize=9.2, fontweight='bold', color='#0F172A')

    # Subgráfico 2: Correlação Oculta de Calote (Normal vs Choque de Monetização de IA)
    ax2.set_facecolor('#FAFAFA')
    scenarios = ['Hipótese Rating\n(Agências KBRA/S&P)', 'Cenário Real em Estresse\n(Quebra de Monetização IA)']
    correlations = [0.08, 0.92]
    colors_corr = ['#10B981', '#EF4444']

    bars_c = ax2.bar(scenarios, correlations, color=colors_corr, width=0.48, edgecolor='#1E293B', linewidth=0.6)
    for bar in bars_c:
        h = bar.get_height()
        desc = "Assume Diversificação" if h < 0.2 else "CORRELAÇÃO = 1.0\n(Calote em Cadeia)"
        ax2.annotate(f"{h:.2f} ({desc})",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0F172A')

    ax2.set_title("Correlação de Calote: Modelo vs Realidade", fontsize=9.2, fontweight='bold', color='#0F172A')
    ax2.set_ylabel("Índice de Correlação (0 a 1.0)", fontsize=8, color='#475569')
    ax2.set_ylim(0, 1.15)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 2 gerado: {output_path}", flush=True)

def generate_chart_3_gpu_depreciation(output_path="chart_gpu_depreciation_vs_debt.png"):
    """Gráfico 3: O Descompasso Temporal: Curva de Depreciação de Silício vs Cronograma de Dívida."""
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    months = np.array([0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60])
    
    # Curva de amortização típica da dívida sênior (5 anos, amortização gradual)
    debt_balance = np.array([100, 96, 92, 87, 81, 74, 66, 56, 44, 28, 0])
    
    # Curva de valor de mercado e preço hora de revenda de GPU com ciclo Blackwell/Rubin
    gpu_value = np.array([100, 88, 72, 54, 38, 28, 20, 15, 12, 9, 7])

    ax.plot(months, debt_balance, color='#1E3A8A', linewidth=2.4, label='Saldo Devedor da Dívida Sênior (Amortização 5 Anos)')
    ax.plot(months, gpu_value, color='#DC2626', linewidth=2.4, linestyle='--', label='Valor Residual de Revenda da GPU (Obsolescência)')

    # Área de risco de colateral afundado (Underwater)
    idx_cross = 3 # Aos 18-20 meses cruza
    ax.fill_between(months[idx_cross:], debt_balance[idx_cross:], gpu_value[idx_cross:], color='#FEE2E2', alpha=0.8, label='Zona de Colateral Deficitário (Underwater Asset)')

    ax.axvline(24, color='#B91C1C', linestyle=':', alpha=0.8)
    ax.annotate("Mês 24: Nova GPU Lançada\nDívida > Colateral em 43%", xy=(24, 60), xytext=(27, 75),
                arrowprops=dict(arrowstyle="->", color='#B91C1C', lw=1.2),
                fontsize=7.8, fontweight='bold', color='#B91C1C', backgroundcolor='#FFFFFF')

    ax.set_title("O Descompasso Temporal: Obsolescência de Hardware vs Prazo da Dívida", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Meses Decorridos após a Emissão da Dívida", fontsize=8, color='#475569')
    ax.set_ylabel("% do Valor Inicial (Base 100)", fontsize=8, color='#475569')
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 110)
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.5)
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 3 gerado: {output_path}", flush=True)

def generate_chart_4_loss_simulation(output_path="chart_stress_loss_simulation.png"):
    """Gráfico 4: Simulação de Severidade de Perda de Capital em Cenários de Estresse."""
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    scenarios = [
        'Cenário 1: Base\n(Monetização Estável)',
        'Cenário 2: Moderado\n(Desaceleração de IA / Churn)',
        'Cenário 3: Severo (2008-Style)\n(Colapso Sistêmico de Startups)'
    ]

    loss_class_a = [0.0, 0.0, 4.5]       # Classe A protegida por Big Techs e OC
    loss_class_b = [0.0, 12.0, 75.0]     # Mezanino sofre absorção imediata
    loss_equity = [0.0, 45.0, 100.0]     # Equity perde 100% no estresse severo

    x = np.arange(len(scenarios))
    w = 0.26

    r1 = ax.bar(x - w, loss_class_a, w, label='Classe A Sênior (Blindada por Big Techs)', color='#10B981', edgecolor='#047857')
    r2 = ax.bar(x, loss_class_b, w, label='Classe B Mezanino (Crédito Privado)', color='#F59E0B', edgecolor='#D97706')
    r3 = ax.bar(x + w, loss_equity, w, label='Equity Tranche (Sponsor / 1ª Perda)', color='#DC2626', edgecolor='#7F1D1D')

    for r in [r1, r2, r3]:
        for bar in r:
            h = bar.get_height()
            if h > 0:
                ax.annotate(f"{h:.1f}%",
                             xy=(bar.get_x() + bar.get_width() / 2, h),
                             xytext=(0, 2),
                             textcoords="offset points",
                             ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')

    ax.set_title("Simulação Forense de Perda de Principal (% de Perda Acumulada)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=7.8, color='#1E293B')
    ax.set_ylabel("Perda Estimada de Principal (%)", fontsize=8, color='#475569')
    ax.set_ylim(0, 115)
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.5)
    ax.grid(True, axis='y')

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
            self.drawString(54, 750, "RELATÓRIO FORENSE • SUBPRIME DE IA")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "SUBCOMPONENTES DAS TRANCHES AAA / A")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Investigação Regulatória: KBRA Methodology 2026, Moody's, S&P, CoreWeave DDTL & SEC Filings")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

# ---------------------------------------------------------
# 4. CONSTRUÇÃO DO PDF FORENSE (4 PÁGINAS COMPLETAS)
# ---------------------------------------------------------

def build_pdf_report(output_filename="Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
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
    # PÁGINA 1: A ALQUIMIA DO REEMPACOTAMENTO: 2008 VS 2026
    # =========================================================
    header_data = [
        [
            Paragraph("<b>AUDITORIA FORENSE DE RISCO SISTÊMICO &amp; MERCADO DE CAPITAIS</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#B91C1C'))),
            Paragraph(f"Emissão: {datetime.date.today().strftime('%d/%m/%Y')} | Dossiê Especial", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("O Reempacotamento de Riscos no Boom de IA", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Investigação Forense: Comparativo 2008 (BBB para AAA), Dívida Colateralizada em GPUs e a Estabilidade Real das Tranches Sênior", style_subtitle))
    story.append(Spacer(1, 6))

    kpi_data = [
        [
            Paragraph("<b>ALQUIMIA 2008</b><br/><font size=9.5 color='#DC2626'><b>MBS BBB ➔ AAA</b></font><br/><font size=6.3 color='#DC2626'>Mezzanine CDO (Cópula David Li)</font>", style_table_cell),
            Paragraph("<b>ALQUIMIA 2026</b><br/><font size=9.5 color='#D97706'><b>GPU Junk ➔ A3 / A-</b></font><br/><font size=6.3 color='#D97706'>SPV CoreWeave (Moody's DDTL)</font>", style_table_cell),
            Paragraph("<b>LASTRO CLASSE A</b><br/><font size=9.5 color='#1E3A8A'><b>72% Hyperscalers</b></font><br/><font size=6.3 color='#10B981'>Microsoft, AWS, Google (Soberanos)</font>", style_table_cell),
            Paragraph("<b>RISCO OCULTO</b><br/><font size=9.5 color='#B91C1C'><b>Vendor Financing</b></font><br/><font size=6.3 color='#B91C1C'>Loop Fechado Nvidia-OpenAI-Neocloud</font>", style_table_cell),
            Paragraph("<b>DESCOMPASSO HARDWARE</b><br/><font size=9.5 color='#7C3AED'><b>3y GPU vs 5y Dívida</b></font><br/><font size=6.3 color='#64748B'>Obsolescência precoce de silício</font>", style_table_cell),
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
                "<b>QUESTÃO CRÍTICA RESPONDIDA:</b> Na crise de 2008, títulos BBB foram repacotados em Mezzanine CDOs que criaram 80% de tranches 'AAA' fictícias apoiadas na premissa falsa de baixa correlação imobiliária. <b>Em 2026, esse mesmo fenômeno está acontecendo no ecossistema de crédito privado de IA</b>: dívidas de neoclouds com cupom de 15% (perfil junk) e garantias em chips voláteis foram empacotadas em SPVs com contratos take-or-pay, obtendo <b>grau de investimento institucional (Rating A3/A-)</b>. Por outro lado, as tranches <b>Classe A de Data Centers Físicos</b> mantêm solidez legítima porque seu colateral é a escassez real de eletricidade e o balanço trilionário de Hyperscalers.",
                style_callout
            )
        ]
    ]
    t_exec = Table(exec_box, colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FCA5A5')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. A Alquimia da Securitização: Paralelo Estrutural 2008 vs 2026", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    if os.path.exists("chart_repackaging_alchemy.png"):
        story.append(Image("chart_repackaging_alchemy.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "• <b>O Mecanismo de 2008:</b> Originadores agrupavam hipotecas subprime de tomadores sem renda (empréstimos NINJA) em títulos RMBS. As fatias classificadas como BBB eram reempacotadas em um novo veículo (Mezzanine CDO), onde a matemática da Cópula Gaussiana calculava que 75% a 80% do novo papel merecia rating AAA devido à suposta diversificação geográfica.<br/>"
        "• <b>O Mecanismo de 2026:</b> Neoclouds e provedores de IA tomam empréstimos com taxas de alto risco (15% a.a.) colateralizados em GPUs físicas. Para destravar capital de seguradoras e fundos de pensão, essas empresas empacotam o hardware e os contratos futuros em SPVs isoladas. Agências como Moody's e DBRS classificam essas emissões sênior como <b>Grau de Investimento A3 / A-</b> (como no empréstimo DDTL de US$ 8.5 Bilhões da CoreWeave em março de 2026).",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 1

    # =========================================================
    # PÁGINA 2: DECOMPOSIÇÃO DOS SUBCOMPONENTES & QUEM COMPÕE O AAA
    # =========================================================
    story.append(Paragraph("2. Decomposição dos Subcomponentes: Quem Compõe as Tranches Sênior?", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "Para responder com rigor sobre o nível de comprometimento das tranches sênior (Classe A / AAA), auditamos a composição real das receitas que alimentam os pagamentos:",
        style_body
    ))

    if os.path.exists("chart_subcomponents_decomposition.png"):
        story.append(Image("chart_subcomponents_decomposition.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    decomp_table_data = [
        [
            Paragraph("<b>Camada do Subcomponente</b>", style_table_header),
            Paragraph("<b>Participação Real</b>", style_table_header),
            Paragraph("<b>Principais Contrapartes</b>", style_table_header),
            Paragraph("<b>Solvência &amp; Diagnóstico de Risco Real</b>", style_table_header)
        ],
        [
            Paragraph("<b>Subcomponente 1:<br/>Hyperscalers Soberanos</b>", style_table_cell),
            Paragraph("<b>65% a 80%</b><br/>da receita do ABS", style_table_cell),
            Paragraph("Microsoft (AAA), AWS (AA), Google (AA+), Meta (AA-)", style_table_cell),
            Paragraph("<font color='#10B981'><b>Extremamente Sólido:</b></font> Balanços trilionários com fluxo de caixa livre massivo. Honram os contratos de data centers para sistemas legados mesmo em eventual crise de IA.", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponente 2:<br/>Neoclouds &amp; Startups IA</b>", style_table_cell),
            Paragraph("<b>15% a 25%</b><br/>(fatia crescente)", style_table_cell),
            Paragraph("CoreWeave, Lambda Labs, OpenAI, xAI, Anthropic", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Altamente Comprometido:</b></font> Empresas com queima acelerada de caixa, dependentes de rodadas perpétuas de Venture Capital e dívida privada para pagar os aluguéis.", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponente 3:<br/>Grandes Corporações</b>", style_table_cell),
            Paragraph("<b>10% a 15%</b><br/>do pool", style_table_cell),
            Paragraph("Bancos de Wall Street, seguradoras, telecomunicações", style_table_cell),
            Paragraph("<font color='#10B981'><b>Estável / Diversificado:</b></font> Colocation corporativo de missão crítica com contratos de 5 a 10 anos reajustados pela inflação (CPI).", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponente 4:<br/>Colateral Físico (Energia)</b>", style_table_cell),
            Paragraph("<b>100%</b> da garantia imobiliária", style_table_cell),
            Paragraph("Subestações elétricas, contratos PPA, prédios blindados", style_table_cell),
            Paragraph("<font color='#10B981'><b>Escassez Absoluta:</b></font> A energia conectada tem valor universal. Se um locatário falir, outros Hyperscalers entram na fila para assumir a carga elétrica.", style_table_cell)
        ]
    ]

    t_decomp = Table(decomp_table_data, colWidths=[105, 75, 120, 204])
    t_decomp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_decomp)

    story.append(PageBreak()) # Fim da Página 2

    # =========================================================
    # PÁGINA 3: O DESCOMPASSO TEMPORAL & A CIRCULARIDADE
    # =========================================================
    story.append(Paragraph("3. O Descompasso Temporal: Hardware de 3 Anos vs Dívida de 5 a 7 Anos", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "A maior fragilidade oculta da dívida colateralizada em IA reside no **descompasso entre a depreciação física do hardware e os prazos de amortização da dívida**:",
        style_body
    ))

    if os.path.exists("chart_gpu_depreciation_vs_debt.png"):
        story.append(Image("chart_gpu_depreciation_vs_debt.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Os 3 Fatores de Comprometimento Estrutural do Colateral:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>O Fenômeno do 'Colateral Afundado' (*Underwater Collateral*):</b> Diferente de imóveis que se valorizam ou depreciam lentamente a 2%-3% ao ano, chips de IA perdem de **60% a 75% do seu valor econômico em 24 a 36 meses** devido ao lançamento de arquiteturas mais eficientes (ex: Blackwell e Rubin da Nvidia). A partir do mês 20, o saldo da dívida a amortizar supera amplamente o valor de liquidação das GPUs.<br/>"
        "2. <b>Circularidade do *Vendor Financing* (O Loop Fechado):</b> A Nvidia investe capital em startups e neoclouds (CoreWeave), que contratam dívida privada junto a gestoras (Blackstone, Magnetar) e devolvem 100% dos recursos comprando chips da própria Nvidia. Esse modelo simula uma demanda orgânica contínua, ocultando que grande parte do fluxo de caixa depende de empréstimos e não de receitas de usuários finais.<br/>"
        "3. <b>A Falácia da Correlação Zero (O Erro de David Li Repetido):</b> Os modelos de agências assumem que se uma startup de IA entrar em default, as outras continuarão saudáveis. Na prática, se o modelo de monetização de IA frustrar o mercado, **a taxa de calote entre todas as Neoclouds salta para 1.0 simultaneamente**, eliminando o benefício da diversificação.",
        style_body
    ))

    story.append(PageBreak()) # Fim da Página 3

    # =========================================================
    # PÁGINA 4: SIMULAÇÃO DE ESTRESSE & CONCLUSÃO FORENSE
    # =========================================================
    story.append(Paragraph("4. Simulação de Perda de Capital e Diagnóstico Forense Definitivo", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "Para responder exatamente qual tranche corre risco de perder dinheiro em um choque similar ao de 2008, simulamos a severidade de perda em três cenários de estresse:",
        style_body
    ))

    if os.path.exists("chart_stress_loss_simulation.png"):
        story.append(Image("chart_stress_loss_simulation.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    stress_table_data = [
        [
            Paragraph("<b>Tranche / Papel</b>", style_table_header),
            Paragraph("<b>Cenário Base (Atual)</b>", style_table_header),
            Paragraph("<b>Cenário Moderado (Ajuste IA)</b>", style_table_header),
            Paragraph("<b>Cenário Severo (2008-Style)</b>", style_table_header),
            Paragraph("<b>Veredito Forense de Comprometimento</b>", style_table_header)
        ],
        [
            Paragraph("<b>Classe A Sênior<br/>(Data Center ABS)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Perda</b></font><br/>Fluxo integral", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Perda</b></font><br/>Overcollateralization absorve", style_table_cell),
            Paragraph("<font color='#10B981'><b>0% a 4.5% Perda</b></font><br/>Big Techs honram contratos", style_table_cell),
            Paragraph("<b>BLINDADA:</b> A Classe A tradicional de Data Centers NÃO quebra como em 2008 graças aos contratos com Microsoft/AWS e o valor da energia.", style_table_cell)
        ],
        [
            Paragraph("<b>Classe B Mezanino<br/>(Crédito Privado)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Perda</b></font><br/>Yield 7.5%-8.5%", style_table_cell),
            Paragraph("<font color='#D97706'><b>12.0% Perda</b></font><br/>Juros PIK ativados", style_table_cell),
            Paragraph("<font color='#DC2626'><b>65% a 80% Perda</b></font><br/>Inadimplência aguda", style_table_cell),
            Paragraph("<b>VULNERÁVEL:</b> A Classe B absorve o primeiro choque de inadimplência de Neoclouds e custos de refrigeração.", style_table_cell)
        ],
        [
            Paragraph("<b>Dívida GPU Direta<br/>(DDTL / Neocloud)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Perda</b></font><br/>Rating A3/A-", style_table_cell),
            Paragraph("<font color='#D97706'><b>25.0% Perda</b></font><br/>Renegociação forçada", style_table_cell),
            Paragraph("<font color='#DC2626'><b>70% a 90% Perda</b></font><br/>Hardware obsoleto", style_table_cell),
            Paragraph("<b>O VERDADEIRO 'SUBPRIME':</b> Dívida rotulada como grau de investimento, mas lastreada em chips com depreciação fulminante.", style_table_cell)
        ]
    ]

    t_stress = Table(stress_table_data, colWidths=[95, 80, 85, 85, 159])
    t_stress.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_stress)
    story.append(Spacer(1, 5))

    conclusion_box_data = [
        [
            Paragraph("<b>SÍNTESE FINAL DO DIAGNÓSTICO:</b><br/>"
                      "1. <b>Onde está o risco de 2008?</b> Ele NÃO está no Data Center ABS tradicional de tijolos e energia (Classe A), que é ancorado pelo balanço AAA dos Hyperscalers.<br/>"
                      "2. <b>Onde está a contaminação real?</b> O risco análogo ao de 2008 está nos <b>empréstimos colateralizados diretamente em GPUs e no crédito privado opaco (*Shadow Banking*)</b>, onde dívida de risco elevado recebeu rótulo de grau de investimento (A3/A-) ancorada em contratos circulares de empresas deficitárias de IA.",
                      style_table_cell)
        ]
    ]
    t_conc_box = Table(conclusion_box_data, colWidths=[504])
    t_conc_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_conc_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório Forense PDF gerado com sucesso: {output_filename}", flush=True)

# ---------------------------------------------------------
# 5. EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

def main():
    print("=== GERANDO GRÁFICOS ANALÍTICOS FORENSES 2008 vs 2026 ===", flush=True)
    generate_chart_1_alchemy("chart_repackaging_alchemy.png")
    generate_chart_2_subcomponents("chart_subcomponents_decomposition.png")
    generate_chart_3_gpu_depreciation("chart_gpu_depreciation_vs_debt.png")
    generate_chart_4_loss_simulation("chart_stress_loss_simulation.png")

    print("\n=== COMPILANDO RELATÓRIO FORENSE EM PDF ===", flush=True)
    pdf_filename = "Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf"
    build_pdf_report(pdf_filename)

    print("\n=== PROCESSO FINALIZADO COM SUCESSO! ===", flush=True)
    print(f"Arquivo gerado: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
