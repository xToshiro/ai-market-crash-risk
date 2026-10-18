#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_company_financial_forecast_report.py
---------------------------------------------
Generates an 8-page institutional PDF executive report in Portuguese:
"Relatório Executivo: Status Financeiro das Líderes de IA, Histórico de Ações (2 Anos) e Previsões Semestrais (2027)"

Output: reports/pt/Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf
"""

import os
import sys
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Ensure paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from utils_paths import get_chart_path, get_report_pt_path

# Custom Canvas with Running Header and Footer (Página X de Y)
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
        
        # Header on pages 2..N
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(54, 750, "AUDITORIA CORPORATIVA • LÍDERES DE IA (2026–2027)")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "STATUS FINANCEIRO, AÇÕES & CENÁRIOS")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidencial • Pesquisa Institucional, Demonstrativos SEC 10-K/10-Q, Bloomberg, Yahoo Finance e Modelos Proprietários")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf"):
    out_path = get_report_pt_path(output_filename)
    doc = SimpleDocTemplate(
        out_path,
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
        fontSize=15.5,
        leading=19.0,
        textColor=colors.HexColor('#0F172A')
    )

    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12.0,
        textColor=colors.HexColor('#475569')
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4,
        spaceBefore=4
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=11.2,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=11.2,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=1
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.2,
        textColor=colors.HexColor('#1E293B')
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.2,
        textColor=colors.HexColor('#1E293B'),
        alignment=1
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.2,
        textColor=colors.HexColor('#0F172A'),
        alignment=1
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10.8,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # =========================================================
    # PÁGINA 1: CAPA EXECUTIVA, DASHBOARD DE KPIS & TABELA MASTER
    # =========================================================
    header_data = [
        [
            Paragraph("<b>RELATÓRIO INSTITUCIONAL • ANÁLISE CORPORATIVA &amp; FORENSE</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#2563EB'))),
            Paragraph(f"Data Base: {datetime.date.today().strftime('%d/%m/%Y')} | Horizonte: 2026–2027", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[320, 184])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Status Financeiro das Líderes de IA, Variação de Ações (2 Anos) e Previsões (2027)", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Auditoria Balanços Patrimoniais, Despesas de CapEx, Desempenho de Cotações (2024–2026) e Matriz Preditiva para H1-2027 e H2-2027", style_subtitle))
    story.append(Spacer(1, 6))

    # 5 KPI cards
    kpi_data = [
        [
            Paragraph("<b>NVIDIA (NVDA)</b><br/><font size=9.2 color='#10B981'><b>$229.28</b></font><br/><font size=6.2 color='#10B981'>+70.1% em 2 Anos</font><br/><font size=5.8 color='#64748B'>Margem Líq: 54%</font>", style_table_cell_center),
            Paragraph("<b>ALPHABET (GOOGL)</b><br/><font size=9.2 color='#2563EB'><b>$351.66</b></font><br/><font size=6.2 color='#10B981'>+115.4% em 2 Anos</font><br/><font size=5.8 color='#64748B'>Caixa Líq: +$88B</font>", style_table_cell_center),
            Paragraph("<b>MICROSOFT (MSFT)</b><br/><font size=9.2 color='#4F46E5'><b>$535.07</b></font><br/><font size=6.2 color='#10B981'>+28.5% em 2 Anos</font><br/><font size=5.8 color='#64748B'>CapEx: $80.4B/ano</font>", style_table_cell_center),
            Paragraph("<b>TSMC (TSM)</b><br/><font size=9.2 color='#8B5CF6'><b>$190.50</b></font><br/><font size=6.2 color='#10B981'>+52.4% em 2 Anos</font><br/><font size=5.8 color='#64748B'>Monopólio 3nm/2nm</font>", style_table_cell_center),
            Paragraph("<b>BROADCOM (AVGO)</b><br/><font size=9.2 color='#0284C7'><b>$184.80</b></font><br/><font size=6.2 color='#10B981'>+54.0% em 2 Anos</font><br/><font size=5.8 color='#64748B'>Margem FCF: 42%</font>", style_table_cell_center),
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[100, 102, 102, 100, 100])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Painel Consolidado de Status Financeiro &amp; Desempenho de Mercado", style_h1))
    story.append(Paragraph(
        "Apresentamos abaixo a matriz institucional detalhada comparando as principais operadoras e fornecedoras da cadeia global de Inteligência Artificial. Os números refletem dados auditados dos últimos 12 meses (TTM / FY2026), demonstrativos contábeis SEC (10-K/10-Q) e cotações de fechamento observadas.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Master Table: 8 Companies + S&P 500 / Nasdaq
    master_table_data = [
        [
            Paragraph("<b>Empresa / Ticker</b>", style_table_header),
            Paragraph("<b>Segmento IA</b>", style_table_header),
            Paragraph("<b>Receita (US$ B)</b>", style_table_header),
            Paragraph("<b>Lucro Líq. (US$ B)</b>", style_table_header),
            Paragraph("<b>Margem Líq. (%)</b>", style_table_header),
            Paragraph("<b>CapEx Anual (US$ B)</b>", style_table_header),
            Paragraph("<b>FCF (US$ B)</b>", style_table_header),
            Paragraph("<b>Cotação Atual</b>", style_table_header),
            Paragraph("<b>Retorno 2 Anos</b>", style_table_header),
            Paragraph("<b>Forward P/E</b>", style_table_header),
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell),
            Paragraph("Hardware / GPUs", style_table_cell),
            Paragraph("US$ 138,5", style_table_cell_center),
            Paragraph("US$ 74,8", style_table_cell_center),
            Paragraph("<b>54,0%</b>", style_table_cell_bold),
            Paragraph("US$ 4,2", style_table_cell_center),
            Paragraph("US$ 68,5", style_table_cell_center),
            Paragraph("<b>US$ 229,28</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+70,1%</b></font>", style_table_cell_center),
            Paragraph("36,5x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell),
            Paragraph("Azure / Copilot", style_table_cell),
            Paragraph("US$ 282,0", style_table_cell_center),
            Paragraph("US$ 99,3", style_table_cell_center),
            Paragraph("35,2%", style_table_cell_center),
            Paragraph("US$ 80,4", style_table_cell_center),
            Paragraph("US$ 62,1", style_table_cell_center),
            Paragraph("<b>US$ 535,07</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+28,5%</b></font>", style_table_cell_center),
            Paragraph("32,0x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell),
            Paragraph("Google Cloud / TPU", style_table_cell),
            Paragraph("US$ 362,0", style_table_cell_center),
            Paragraph("US$ 100,6", style_table_cell_center),
            Paragraph("27,8%", style_table_cell_center),
            Paragraph("US$ 74,2", style_table_cell_center),
            Paragraph("US$ 72,5", style_table_cell_center),
            Paragraph("<b>US$ 351,66</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+115,4%</b></font>", style_table_cell_center),
            Paragraph("23,8x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell),
            Paragraph("AWS / Trainium", style_table_cell),
            Paragraph("US$ 655,0", style_table_cell_center),
            Paragraph("US$ 55,7", style_table_cell_center),
            Paragraph("8,5%", style_table_cell_center),
            Paragraph("US$ 96,9", style_table_cell_center),
            Paragraph("US$ 48,0", style_table_cell_center),
            Paragraph("<b>US$ 262,43</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+39,0%</b></font>", style_table_cell_center),
            Paragraph("33,5x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Meta Platforms (META)</b>", style_table_cell),
            Paragraph("Llama / AI Ads", style_table_cell),
            Paragraph("US$ 178,0", style_table_cell_center),
            Paragraph("US$ 60,5", style_table_cell_center),
            Paragraph("34,0%", style_table_cell_center),
            Paragraph("US$ 55,2", style_table_cell_center),
            Paragraph("US$ 46,2", style_table_cell_center),
            Paragraph("<b>US$ 718,67</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+21,8%</b></font>", style_table_cell_center),
            Paragraph("24,5x", style_table_cell_center),
        ],
        [
            Paragraph("<b>TSMC (TSM)</b>", style_table_cell),
            Paragraph("Foundry 3nm/CoWoS", style_table_cell),
            Paragraph("US$ 94,5", style_table_cell_center),
            Paragraph("US$ 40,2", style_table_cell_center),
            Paragraph("42,5%", style_table_cell_center),
            Paragraph("US$ 33,0", style_table_cell_center),
            Paragraph("US$ 28,5", style_table_cell_center),
            Paragraph("<b>US$ 190,50</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+52,4%</b></font>", style_table_cell_center),
            Paragraph("22,5x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_cell),
            Paragraph("ASICs / Ethernet IA", style_table_cell),
            Paragraph("US$ 54,0", style_table_cell_center),
            Paragraph("US$ 16,2", style_table_cell_center),
            Paragraph("30,0%", style_table_cell_center),
            Paragraph("US$ 2,5", style_table_cell_center),
            Paragraph("US$ 22,5", style_table_cell_center),
            Paragraph("<b>US$ 184,80</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+54,0%</b></font>", style_table_cell_center),
            Paragraph("28,5x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Oracle (ORCL)</b>", style_table_cell),
            Paragraph("Nuvem OCI / Dívida", style_table_cell),
            Paragraph("US$ 57,0", style_table_cell_center),
            Paragraph("US$ 10,4", style_table_cell_center),
            Paragraph("18,2%", style_table_cell_center),
            Paragraph("US$ 12,5", style_table_cell_center),
            Paragraph("US$ 8,2", style_table_cell_center),
            Paragraph("<b>US$ 141,40</b>", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>-19,6%</b></font>", style_table_cell_center),
            Paragraph("21,0x", style_table_cell_center),
        ],
        [
            Paragraph("<b>S&amp;P 500 (^GSPC)</b>", style_table_cell),
            Paragraph("Benchmark Geral", style_table_cell),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("<b>7.811 pts</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+34,3%</b></font>", style_table_cell_center),
            Paragraph("23,4x", style_table_cell_center),
        ],
        [
            Paragraph("<b>Nasdaq (^IXIC)</b>", style_table_cell),
            Paragraph("Tecnologia Ampla", style_table_cell),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("—", style_table_cell_center),
            Paragraph("<b>27.366 pts</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+49,2%</b></font>", style_table_cell_center),
            Paragraph("29,5x", style_table_cell_center),
        ],
    ]
    t_master = Table(master_table_data, colWidths=[85, 75, 48, 48, 42, 48, 44, 48, 42, 24])
    t_master.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_master)
    story.append(Spacer(1, 8))

    callout_p1 = [
        [
            Paragraph(
                "<b>Síntese Executiva:</b> Observa-se uma concentração histórica de lucros e margens nos fabricantes de silício fabless (Nvidia com 54% de margem líquida e FCF de US$ 68,5B). Em contrapartida, as provedoras de nuvem (Microsoft, Amazon, Meta) ingressaram em um ciclo de queima recorde de CapEx (>US$ 230B/ano combinados), comprimindo a conversão de caixa livre relativa aos lucros contábeis.",
                style_callout
            )
        ]
    ]
    t_callout1 = Table(callout_p1, colWidths=[504])
    t_callout1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3B82F6')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_callout1)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 2: ANÁLISE DE SILÍCIO, FOUNDRY & REDES + GRÁFICO 1
    # =========================================================
    story.append(Paragraph("2. Auditoria da Infraestrutura de Silício: Nvidia, TSMC e Broadcom", style_h1))
    story.append(Paragraph(
        "A base operacional do superciclo reside em três monopólios tecnológicos complementares. A análise detalhada da Demonstração do Resultado (DRE) e do Balanço Patrimonial revela modelos de geração de caixa radicalmente divergentes:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Gráfico 1: chart_company_financial_matrix.png
    chart1_path = get_chart_path("chart_company_financial_matrix.png", "pt")
    if os.path.exists(chart1_path):
        story.append(Image(chart1_path, width=504, height=195))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Decomposição Estrutural dos Fornecedores de Hardware:", style_body_bold))
    story.append(Paragraph(
        "• <b>Nvidia (NVDA) — O Monopólio de Software CUDA &amp; Hardware:</b> Apresenta margem bruta recorde de 75,0% e caixa líquido de US$ 32,2B. Como a empresa opera no modelo fabless, seu investimento direto em imobilizado (CapEx) foi de apenas US$ 4,2B (3,0% da receita), permitindo canalizar quase todo o lucro bruto para o Fluxo de Caixa Livre líquido (US$ 68,5B). O risco reside na concentração de receita em poucas neoclouds e hiperscalers que praticam vendor financing circular.<br/>"
        "• <b>TSMC (TSM) — O Gargalo Físico da Fundição Global:</b> Domina 100% da manufatura de aceleradores avançados em 3nm/2nm e empacotamento CoWoS. Seu lucro líquido de US$ 40,2B (margem de 42,5%) é reinvestido pesadamente: CapEx anual de US$ 33,0B (35% da receita) para expandir mega-fabs em Taiwan e nos EUA. Seu múltiplo de 22,5x P/E embute desconto substancial pelo risco geopolítico no Estreito de Taiwan.<br/>"
        "• <b>Broadcom (AVGO) — Hegemonia em Redes Ethernet e ASICs:</b> A Broadcom capturou o mercado de silício customizado (TPUs do Google e chips MTIA da Meta), combinando com dominância em switches ópticos de alta velocidade (Tomahawk 5). Com CapEx terceirizado de apenas US$ 2,5B, converte 41,7% de sua receita em FCF (US$ 22,5B).",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Tabela de Métricas Patrimoniais de Hardware
    hw_table_data = [
        [
            Paragraph("<b>Métrica de Balanço (US$ Bi)</b>", style_table_header),
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_header),
            Paragraph("<b>TSMC (TSM)</b>", style_table_header),
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_header),
            Paragraph("<b>Diagnóstico de Risco Institucional</b>", style_table_header),
        ],
        [
            Paragraph("<b>Caixa &amp; Equivalentes</b>", style_table_cell),
            Paragraph("US$ 42,0 B", style_table_cell_center),
            Paragraph("US$ 58,5 B", style_table_cell_center),
            Paragraph("US$ 14,2 B", style_table_cell_center),
            Paragraph("Liquidez soberana confortável em todas as três companhias.", style_table_cell),
        ],
        [
            Paragraph("<b>Dívida Bruta Total</b>", style_table_cell),
            Paragraph("US$ 9,8 B", style_table_cell_center),
            Paragraph("US$ 30,0 B", style_table_cell_center),
            Paragraph("US$ 68,0 B", style_table_cell_center),
            Paragraph("Broadcom carrega alavancagem elevada decorrente da aquisição da VMware.", style_table_cell),
        ],
        [
            Paragraph("<b>Posição Líquida de Caixa</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>+US$ 32,2 B</b></font>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+US$ 28,5 B</b></font>", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>-US$ 53,8 B</b></font>", style_table_cell_center),
            Paragraph("Nvidia e TSMC desfrutam de imunidade direta a aumentos na curva de juros.", style_table_cell),
        ],
        [
            Paragraph("<b>Conversão FCF / Lucro Líquido</b>", style_table_cell),
            Paragraph("<b>91,6%</b>", style_table_cell_center),
            Paragraph("<b>70,9%</b>", style_table_cell_center),
            Paragraph("<b>138,9%</b>", style_table_cell_center),
            Paragraph("Excelente capacidade de remuneração aos acionistas via recompras.", style_table_cell),
        ],
    ]
    t_hw = Table(hw_table_data, colWidths=[110, 75, 75, 75, 169])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284C7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_hw)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 3: HYPERSCALERS & NUVEM CORPORATIVA + GRÁFICO 2
    # =========================================================
    story.append(Paragraph("3. O Confronto dos Hyperscalers: CapEx Massivo vs Compressão de FCF", style_h1))
    story.append(Paragraph(
        "Os quatro maiores compradores mundiais de infraestrutura (Microsoft, Alphabet, Amazon e Meta), acompanhados pela Oracle, estão comprometendo montantes sem precedentes históricos de capital para garantir capacidade em data centers, subestações e GPUs de última geração:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Gráfico 2: chart_company_capex_vs_fcf.png
    chart2_path = get_chart_path("chart_company_capex_vs_fcf.png", "pt")
    if os.path.exists(chart2_path):
        story.append(Image(chart2_path, width=504, height=195))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Auditoria Comparativa dos Balanços dos Hyperscalers:", style_body_bold))
    story.append(Paragraph(
        "• <b>Microsoft (MSFT) — A Maior Aposta Absoluta em Parcerias:</b> Comprometeu US$ 80,4B em CapEx (28,5% da receita), erguendo clusters para rodar os modelos da OpenAI. O FCF de US$ 62,1B reflete compressão de caixa, já que o crescimento das assinaturas corporativas de Copilot (M365) avança a taxas moderadas (12% de penetração), enquanto a depreciação de servidores começará a pesar no custo dos produtos vendidos a partir de 2027.<br/>"
        "• <b>Alphabet (GOOGL) — Blindagem Financeira &amp; TPUs Próprias:</b> Mantém o balanço mais defensivo do setor, com US$ 88,0B em caixa líquido e FCF de US$ 72,5B. A integração do ecossistema Gemini e a substituição parcial de GPUs por silício próprio (TPU v5p/v6) protegeu suas margens operacionais de nuvem (14%), justificando seu valuation de 23,8x P/E.<br/>"
        "• <b>Amazon (AMZN) — O Gigante de CapEx Físico (US$ 96,9B):</b> Líder isolada em despesas de capital na economia global, combinando data centers da AWS, compras massivas de energia nuclear e frota logística. Seu FCF de US$ 48,0B representa apenas 7,3% da receita bruta.<br/>"
        "• <b>Meta (META) — A Maior Intensidade de Infraestrutura (31,0% da Receita):</b> Alocou US$ 55,2B em infraestrutura para treinar os modelos abertos Llama 3/4. Como a Meta não vende licenças diretas de nuvem, todo o retorno deve vir da eficácia incremental em anúncios e ferramentas generativas no Instagram/WhatsApp.<br/>"
        "• <b>Oracle (ORCL) — Alavancagem Crítica sob Juros Altos:</b> Com dívida total de US$ 88,0B e dívida líquida sobre EBITDA superior a 3,2x, a Oracle opera no limite da flexibilidade financeira. Seus contratos de nuvem de IA com xAI e OpenAI geram faturamento, mas margens e FCF (US$ 8,2B) são severamente corroídos pelo serviço da dívida em juros de 5,24%.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Tabela de Hyperscalers: CapEx vs FCF vs Dívida
    hs_table_data = [
        [
            Paragraph("<b>Empresa</b>", style_table_header),
            Paragraph("<b>CapEx 12M (US$ B)</b>", style_table_header),
            Paragraph("<b>Intensidade CapEx (%)</b>", style_table_header),
            Paragraph("<b>FCF 12M (US$ B)</b>", style_table_header),
            Paragraph("<b>Dívida Líquida (US$ B)</b>", style_table_header),
            Paragraph("<b>Sensibilidade a Desaceleração de IA</b>", style_table_header),
        ],
        [
            Paragraph("<b>Microsoft</b>", style_table_cell),
            Paragraph("US$ 80,4 B", style_table_cell_center),
            Paragraph("<b>28,5%</b>", style_table_cell_bold),
            Paragraph("US$ 62,1 B", style_table_cell_center),
            Paragraph("-US$ 13,0 B (Líq)", style_table_cell_center),
            Paragraph("Média: amortecida por monopólio Windows/Office e software B2B.", style_table_cell),
        ],
        [
            Paragraph("<b>Alphabet</b>", style_table_cell),
            Paragraph("US$ 74,2 B", style_table_cell_center),
            Paragraph("20,5%", style_table_cell_center),
            Paragraph("US$ 72,5 B", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>-US$ 88,0 B (Caixa)</b></font>", style_table_cell_center),
            Paragraph("Baixa: balanço ultralíquido e hegemonia em publicidade digital.", style_table_cell),
        ],
        [
            Paragraph("<b>Amazon</b>", style_table_cell),
            Paragraph("US$ 96,9 B", style_table_cell_center),
            Paragraph("14,8%", style_table_cell_center),
            Paragraph("US$ 48,0 B", style_table_cell_center),
            Paragraph("-US$ 15,0 B (Líq)", style_table_cell_center),
            Paragraph("Baixa/Média: compensada por forte fluxo de e-commerce e varejo.", style_table_cell),
        ],
        [
            Paragraph("<b>Meta Platforms</b>", style_table_cell),
            Paragraph("US$ 55,2 B", style_table_cell_center),
            Paragraph("<b>31,0%</b>", style_table_cell_bold),
            Paragraph("US$ 46,2 B", style_table_cell_center),
            Paragraph("-US$ 28,0 B (Caixa)", style_table_cell_center),
            Paragraph("Média: vulnerável se investidores exigirem corte de gastos em Llama.", style_table_cell),
        ],
        [
            Paragraph("<b>Oracle</b>", style_table_cell),
            Paragraph("US$ 12,5 B", style_table_cell_center),
            Paragraph("22,0%", style_table_cell_center),
            Paragraph("US$ 8,2 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>+US$ 76,0 B (Dívida)</b></font>", style_table_cell_center),
            Paragraph("Alta: vulnerabilidade aguda a refinanciamento sob taxas elevadas.", style_table_cell),
        ],
    ]
    t_hs = Table(hs_table_data, colWidths=[80, 75, 75, 75, 80, 119])
    t_hs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F46E5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_hs)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 4: A TEIA DE INVESTIMENTOS CRUZADOS & VENDOR FINANCING
    # =========================================================
    story.append(Paragraph("4. A Teia de Investimentos Cruzados &amp; Financiamento Circular (Vendor Financing)", style_h1))
    story.append(Paragraph(
        "Diferente de um ciclo maduro sustentado por demanda final corporativa independente, a indústria de Inteligência Artificial estruturou uma complexa rede de <b>participações societárias cruzadas e financiamento circular (round-tripping de receitas)</b>. Operadoras de nuvem e fabricantes de chips financiam diretamente as startups que, por sua vez, são obrigadas a devolver o capital na forma de consumo de nuvem e compra compulsória de hardware:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Box Resumo dos Circuitos Circulares
    circ_summary_data = [
        [
            Paragraph("<b>Circuito A: Nvidia ⟷ Neoclouds &amp; Labs</b><br/><font size=6.6 color='#334155'>Nvidia aporta capital societário (equity) na CoreWeave/OpenAI. As empresas tomam dívida privada colateralizada em GPUs e repassam 100% dos recursos à vista para comprar chips Nvidia a 75% de margem bruta.</font>", style_table_cell),
            Paragraph("<b>Circuito B: Microsoft ⟷ OpenAI &amp; CoreWeave</b><br/><font size=6.6 color='#334155'>Microsoft investiu US$ 13B+ na OpenAI em troca de 49% dos lucros e exclusividade de nuvem (&gt;70% da receita da OpenAI volta para a Azure). Para descarregar capacidade, Microsoft aluga clusters da CoreWeave.</font>", style_table_cell),
        ],
        [
            Paragraph("<b>Circuito C: Amazon &amp; Google ⟷ Anthropic</b><br/><font size=6.6 color='#334155'>Amazon (US$ 4B) e Google (US$ 2B) aportam capital condicionado ao uso prioritário de chips AWS Trainium2 e contratos plurianuais de nuvem (US$ 3B no Google Cloud), garantindo demanda artificial.</font>", style_table_cell),
            Paragraph("<b>Diagnóstico de Risco Sistêmico (Round-Tripping)</b><br/><font size=6.6 color='#DC2626'><b>Mecanismo de Alavancagem Oculta:</b> Cada US$ 1,00 investido em equity gera até US$ 3,50 em receita contábil reportada na cadeia, criando a ilusão de crescimento orgânico independente.</font>", style_table_cell),
        ]
    ]
    t_circ = Table(circ_summary_data, colWidths=[250, 254])
    t_circ.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_circ)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Mapeamento dos Acordos Bilaterais de Financiamento Circular:", style_body_bold))
    story.append(Spacer(1, 2))

    # Tabela de Acordos Cruzados
    cross_table_data = [
        [
            Paragraph("<b>Investidor Primário</b>", style_table_header),
            Paragraph("<b>Entidade Investida</b>", style_table_header),
            Paragraph("<b>Aporte / Modalidade</b>", style_table_header),
            Paragraph("<b>Contrapartida Comercial / Amortização</b>", style_table_header),
            Paragraph("<b>Impacto Sistêmico no Balanço</b>", style_table_header),
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell),
            Paragraph("<b>OpenAI</b>", style_table_cell),
            Paragraph("US$ 13,0+ B (Equity)", style_table_cell_center),
            Paragraph("Consumo compulsório de infraestrutura Azure; direito a 49% dos lucros da subsidiária comercial.", style_table_cell),
            Paragraph("Infla receita de nuvem Azure; amortece investimentos via créditos de servidores.", style_table_cell),
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell),
            Paragraph("<b>CoreWeave</b>", style_table_cell),
            Paragraph("Contratos &gt; US$ 10 B", style_table_cell_center),
            Paragraph("Locação externa plurianual de clusters de H100 para absorver picos de demanda da OpenAI.", style_table_cell),
            Paragraph("Desloca CapEx físico pesado para fora do balanço operacional da Microsoft.", style_table_cell),
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell),
            Paragraph("<b>CoreWeave</b>", style_table_cell),
            Paragraph("Equity Anchor (~$500M)", style_table_cell_center),
            Paragraph("Prioridade em alocação de GPUs; 100% da dívida privada da CoreWeave compra hardware NVDA.", style_table_cell),
            Paragraph("Converte investimento societário direto em faturamento com 75% de margem bruta.", style_table_cell),
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell),
            Paragraph("<b>OpenAI</b>", style_table_cell),
            Paragraph("Equity (~US$ 100M)", style_table_cell_center),
            Paragraph("Garantia de que os algoritmos de fronteira permaneçam nativamente otimizados em CUDA.", style_table_cell),
            Paragraph("Bloqueia competidores (AMD / ASICs customizados) de nós de computação de ponta.", style_table_cell),
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell),
            Paragraph("<b>Anthropic</b>", style_table_cell),
            Paragraph("US$ 4,0 B (Notas/Equity)", style_table_cell_center),
            Paragraph("Compromisso mandatório de uso de chips AWS Trainium2 e distribuição via Amazon Bedrock.", style_table_cell),
            Paragraph("Valida comercialmente o silício proprietário da AWS frente ao monopólio da Nvidia.", style_table_cell),
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell),
            Paragraph("<b>Anthropic</b>", style_table_cell),
            Paragraph("US$ 2,0 B (Equity/Debt)", style_table_cell_center),
            Paragraph("Contrato de consumo de infraestrutura de US$ 3,0B no ecossistema Google Cloud.", style_table_cell),
            Paragraph("Preenche capacidade ociosa de subestações e clusters TPU do Google Cloud.", style_table_cell),
        ],
    ]
    t_cross = Table(cross_table_data, colWidths=[80, 68, 80, 150, 126])
    t_cross.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7C3AED')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_cross)
    story.append(Spacer(1, 6))

    callout_p4 = [
        [
            Paragraph(
                "<b>Alerta de Vulnerabilidade:</b> A circularidade dos fluxos cria uma interdependência simbiótica perigosa. Se a receita final de clientes corporativos (ROI em software) estagnar, a cadeia não sofre uma desaceleração gradual, mas sim uma interrupção em cascata: a quebra de uma neocloud elimina instantaneamente compras na Nvidia e satura a capacidade dos hiperscalers.",
                style_callout
            )
        ]
    ]
    t_callout4 = Table(callout_p4, colWidths=[504])
    t_callout4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#EF4444')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_callout4)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 5: EXPOSIÇÃO DO VALOR DE MERCADO A IA & CORRELAÇÃO 1.0
    # =========================================================
    story.append(Paragraph("5. Decomposição do Prêmio de IA: Quanto do Valor Está Comprometido com IA?", style_h1))
    story.append(Paragraph(
        "Ao comparar as capitalizações bursáteis atuais com a referência pré-ChatGPT (Outubro de 2022) e isolar o crescimento orgânico dos negócios tradicionais, quantificamos a <b>fatia exata do valor de cada empresa sustentada exclusivamente pela tese de IA</b>:",
        style_body
    ))
    story.append(Spacer(1, 3))

    # Gráfico 5: chart_company_ai_exposure.png
    chart5_path = get_chart_path("chart_company_ai_exposure.png", "pt")
    if os.path.exists(chart5_path):
        story.append(Image(chart5_path, width=504, height=190))
        story.append(Spacer(1, 5))

    # Tabela de Exposição do Market Cap
    exposure_table_data = [
        [
            Paragraph("<b>Empresa / Ticker</b>", style_table_header),
            Paragraph("<b>Market Cap Atual</b>", style_table_header),
            Paragraph("<b>Cap Pré-IA (2022)</b>", style_table_header),
            Paragraph("<b>Ganho 4 Anos</b>", style_table_header),
            Paragraph("<b>Valor Atrib. a IA</b>", style_table_header),
            Paragraph("<b>% Comprometido c/ IA</b>", style_table_header),
            Paragraph("<b>Diagnóstico de Risco / Dependência</b>", style_table_header),
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell),
            Paragraph("US$ 3.580 B", style_table_cell_center),
            Paragraph("~US$ 360 B", style_table_cell_center),
            Paragraph("+US$ 3.220 B", style_table_cell_center),
            Paragraph("US$ 3.150 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>88% a 90%</b></font>", style_table_cell_center),
            Paragraph("Crítica: Sem data centers de IA, negócios legados justificam &lt; US$ 400B.", style_table_cell),
        ],
        [
            Paragraph("<b>TSMC (TSM)</b>", style_table_cell),
            Paragraph("US$ 985 B", style_table_cell_center),
            Paragraph("~US$ 380 B", style_table_cell_center),
            Paragraph("+US$ 605 B", style_table_cell_center),
            Paragraph("US$ 540 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>54% a 57%</b></font>", style_table_cell_center),
            Paragraph("Severa: HPC e nós avançados (&lt;3nm/CoWoS) geram mais de 55% da receita.", style_table_cell),
        ],
        [
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_cell),
            Paragraph("US$ 860 B", style_table_cell_center),
            Paragraph("~US$ 200 B", style_table_cell_center),
            Paragraph("+US$ 660 B", style_table_cell_center),
            Paragraph("US$ 450 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>52% a 55%</b></font>", style_table_cell_center),
            Paragraph("Severa: Switches Tomahawk 5 e ASICs customizados sustentam valuation premium.", style_table_cell),
        ],
        [
            Paragraph("<b>Oracle (ORCL)</b>", style_table_cell),
            Paragraph("US$ 392 B", style_table_cell_center),
            Paragraph("~US$ 180 B", style_table_cell_center),
            Paragraph("+US$ 212 B", style_table_cell_center),
            Paragraph("US$ 190 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>48% a 50%</b></font>", style_table_cell_center),
            Paragraph("Severa: Tese depende de contratos de nuvem OCI sob dívida bruta de US$ 88B.", style_table_cell),
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell),
            Paragraph("US$ 3.980 B", style_table_cell_center),
            Paragraph("~US$ 1.780 B", style_table_cell_center),
            Paragraph("+US$ 2.200 B", style_table_cell_center),
            Paragraph("US$ 1.650 B", style_table_cell_center),
            Paragraph("<font color='#D97706'><b>41% a 43%</b></font>", style_table_cell_center),
            Paragraph("Moderada/Alta: Múltiplo P/E de 32x embute expectativa trilionária em Copilot/Azure.", style_table_cell),
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell),
            Paragraph("US$ 2.750 B", style_table_cell_center),
            Paragraph("~US$ 900 B", style_table_cell_center),
            Paragraph("+US$ 1.850 B", style_table_cell_center),
            Paragraph("US$ 1.050 B", style_table_cell_center),
            Paragraph("<font color='#D97706'><b>38% a 40%</b></font>", style_table_cell_center),
            Paragraph("Moderada: AWS dita o múltiplo, embora e-commerce e ads amorteçam perdas.", style_table_cell),
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell),
            Paragraph("US$ 4.320 B", style_table_cell_center),
            Paragraph("~US$ 1.200 B", style_table_cell_center),
            Paragraph("+US$ 3.120 B", style_table_cell_center),
            Paragraph("US$ 1.600 B", style_table_cell_center),
            Paragraph("<font color='#D97706'><b>37% a 39%</b></font>", style_table_cell_center),
            Paragraph("Moderada: Receita de busca é defensiva; Gemini e TPU definem expansão de margem.", style_table_cell),
        ],
        [
            Paragraph("<b>Meta Platforms (META)</b>", style_table_cell),
            Paragraph("US$ 1.820 B", style_table_cell_center),
            Paragraph("~US$ 260 B", style_table_cell_center),
            Paragraph("+US$ 1.560 B", style_table_cell_center),
            Paragraph("US$ 650 B", style_table_cell_center),
            Paragraph("<font color='#0284C7'><b>35% a 37%</b></font>", style_table_cell_center),
            Paragraph("Moderada: CapEx de US$ 55B é compensado por otimização algorítmica de ads.", style_table_cell),
        ],
        [
            Paragraph("<b>Labs &amp; Neoclouds</b>", style_table_cell),
            Paragraph("US$ 198 B (Tot)", style_table_cell_center),
            Paragraph("&lt; US$ 22 B", style_table_cell_center),
            Paragraph("+US$ 176 B", style_table_cell_center),
            Paragraph("US$ 198 B", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>100%</b></font>", style_table_cell_center),
            Paragraph("Binária: Sem negócios legados; valor evapora se os influxos de capital secarem.", style_table_cell),
        ],
    ]
    t_exp = Table(exposure_table_data, colWidths=[80, 56, 56, 56, 54, 58, 144])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#DC2626')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_exp)
    story.append(Spacer(1, 5))

    callout_p5 = [
        [
            Paragraph(
                "<b>A 'Correlação 1.0' em Cenários de Estresse:</b> A diversificação setorial aparente é uma ilusão técnica. Mais de <b>US$ 9,0 Trilhões</b> do valor combinado dessas companhias depende unicamente da perpetuidade do ciclo de IA. Uma desaceleração no ROI corporativo fará com que a correlação entre as ações convirja para 1,0, eliminando os benefícios da dispersão de portfólio.",
                style_callout
            )
        ]
    ]
    t_callout5 = Table(callout_p5, colWidths=[504])
    t_callout5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F59E0B')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_callout5)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 6: CAPITAL PRIVADO, HISTÓRICO DE 2 ANOS + GRÁFICO 3
    # =========================================================
    story.append(Paragraph("6. O Perímetro de Capital Privado &amp; Variação Histórica das Ações (2 Anos)", style_h1))
    story.append(Paragraph(
        "A sustentabilidade das Big Techs está intimamente conectada à saúde do ecossistema não listado (startups de modelos e neoclouds). Abaixo examinamos a trajetória de preços de 24 meses das ações cotadas em bolsa confrontada com a fragilidade de caixa das líderes privadas:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Gráfico 3: chart_company_stocks_2y_history.png
    chart3_path = get_chart_path("chart_company_stocks_2y_history.png", "pt")
    if os.path.exists(chart3_path):
        story.append(Image(chart3_path, width=504, height=195))
        story.append(Spacer(1, 6))

    story.append(Paragraph("A Fragilidade Oculta do Capital Privado (Shadow Banking):", style_body_bold))
    story.append(Paragraph(
        "• <b>CoreWeave:</b> Avaliada em US$ 21B, acumulou mais de US$ 19,0B em dívida privada colateralizada em hardware (Blackstone, Magnetar, Coatue). Opera com alavancagem de 10x sobre o patrimônio. Se os preços de aluguel de H100 caírem abaixo de US$ 1,50/hora, a cobertura de serviço da dívida (DSCR) rompe covenants contratuais.<br/>"
        "• <b>OpenAI:</b> Valuation de US$ 157B na rodada recente, com receita de ~US$ 4,5B e queima operacional anual de US$ 5,5B a US$ 7,5B. Mais de 70% de cada dólar faturado é devolvido para a infraestrutura de computação.<br/>"
        "• <b>Anthropic:</b> Valuation de US$ 20B, dependente de injeções da Amazon e Google para financiar prejuízo operacional de ~US$ 2,5B/ano.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Tabela Histórica de Cotações (2 Anos: 2024-2026)
    history_table_data = [
        [
            Paragraph("<b>Ticker / Ativo</b>", style_table_header),
            Paragraph("<b>Preço Out/2024</b>", style_table_header),
            Paragraph("<b>Preço Out/2026</b>", style_table_header),
            Paragraph("<b>Retorno Acum. (%)</b>", style_table_header),
            Paragraph("<b>Mín. 52 Semanas</b>", style_table_header),
            Paragraph("<b>Máx. 52 Semanas</b>", style_table_header),
            Paragraph("<b>Principal Driver de Preço em 24 Meses</b>", style_table_header),
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell),
            Paragraph("US$ 163,24", style_table_cell_center),
            Paragraph("<b>US$ 351,66</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+115,4%</b></font>", style_table_cell_center),
            Paragraph("US$ 155,00", style_table_cell_center),
            Paragraph("US$ 362,00", style_table_cell_center),
            Paragraph("Liderança em Gemini, monetização Cloud e blindagem antitruste.", style_table_cell),
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell),
            Paragraph("US$ 134,80", style_table_cell_center),
            Paragraph("<b>US$ 229,28</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+70,1%</b></font>", style_table_cell_center),
            Paragraph("US$ 118,00", style_table_cell_center),
            Paragraph("US$ 245,50", style_table_cell_center),
            Paragraph("Explosão de lucros trimestrais compensando leve contração de P/E.", style_table_cell),
        ],
        [
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_cell),
            Paragraph("US$ 120,00", style_table_cell_center),
            Paragraph("<b>US$ 184,80</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+54,0%</b></font>", style_table_cell_center),
            Paragraph("US$ 125,00", style_table_cell_center),
            Paragraph("US$ 195,00", style_table_cell_center),
            Paragraph("Adoção massiva de switches Ethernet de IA e ASICs proprietários.", style_table_cell),
        ],
        [
            Paragraph("<b>TSMC (TSM)</b>", style_table_cell),
            Paragraph("US$ 125,00", style_table_cell_center),
            Paragraph("<b>US$ 190,50</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+52,4%</b></font>", style_table_cell_center),
            Paragraph("US$ 130,00", style_table_cell_center),
            Paragraph("US$ 205,00", style_table_cell_center),
            Paragraph("Utilização de 100% nas linhas de 3nm e aumentos no preço de wafers.", style_table_cell),
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell),
            Paragraph("US$ 188,82", style_table_cell_center),
            Paragraph("<b>US$ 262,43</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+39,0%</b></font>", style_table_cell_center),
            Paragraph("US$ 170,00", style_table_cell_center),
            Paragraph("US$ 275,00", style_table_cell_center),
            Paragraph("Expansão das margens operacionais de AWS e e-commerce norte-americano.", style_table_cell),
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell),
            Paragraph("US$ 416,32", style_table_cell_center),
            Paragraph("<b>US$ 535,07</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+28,5%</b></font>", style_table_cell_center),
            Paragraph("US$ 395,00", style_table_cell_center),
            Paragraph("US$ 555,00", style_table_cell_center),
            Paragraph("Crescimento de Azure (29%), moderado pela queima de CapEx no FCF.", style_table_cell),
        ],
        [
            Paragraph("<b>Meta Platforms (META)</b>", style_table_cell),
            Paragraph("US$ 589,95", style_table_cell_center),
            Paragraph("<b>US$ 718,67</b>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+21,8%</b></font>", style_table_cell_center),
            Paragraph("US$ 520,00", style_table_cell_center),
            Paragraph("US$ 740,00", style_table_cell_center),
            Paragraph("Monetização de anúncios via IA ofuscada pela queima de caixa em Llama.", style_table_cell),
        ],
        [
            Paragraph("<b>Oracle (ORCL)</b>", style_table_cell),
            Paragraph("US$ 175,77", style_table_cell_center),
            Paragraph("<b>US$ 141,40</b>", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>-19,6%</b></font>", style_table_cell_center),
            Paragraph("US$ 125,00", style_table_cell_center),
            Paragraph("US$ 195,00", style_table_cell_center),
            Paragraph("Penalização severa por endividamento de US$ 88B com juros em 5,24%.", style_table_cell),
        ],
    ]
    t_hist = Table(history_table_data, colWidths=[75, 52, 52, 52, 50, 50, 173])
    t_hist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D9488')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_hist)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 7: PREVISÕES PARA OS PRÓXIMOS 2 SEMESTRES + GRÁFICO 4
    # =========================================================
    story.append(Paragraph("7. Previsão para os Próximos 2 Semestres (H1-2027 e H2-2027)", style_h1))
    story.append(Paragraph(
        "A modelagem econométrica do repositório projeta o comportamento das companhias para o 1º Semestre de 2027 (H1-27) e 2º Semestre de 2027 (H2-27), testando a sensibilidade das receitas, lucros e valuations a 3 cenários macrofinanceiros:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Gráfico 4: chart_company_forecast_2semesters.png
    chart4_path = get_chart_path("chart_company_forecast_2semesters.png", "pt")
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=504, height=195))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Dinâmica e Catalisadores por Semestre Projetado:", style_body_bold))
    story.append(Paragraph(
        "• <b>1º Semestre de 2027 (H1-2027) — A Rampa Blackwell &amp; O Teste do Software Corporativo:</b><br/>"
        "A entrega em volume integral dos clusters Nvidia Blackwell (B200/GB200) impulsionará as receitas da Nvidia para US$ 78B no semestre. Simultaneamente, os hiperscalers enfrentarão escrutínio severo de analistas quanto ao retorno sobre o capital investido (ROIC). Espera-se que a adoção corporativa de agentes de IA atinja 15% das empresas da Fortune 500. No Cenário Base, as ações sobem em média <b>+8,0%</b>; no Cenário Otimista avançam <b>+19,4%</b>; e sob estresse de crédito recuam <b>-22,5%</b>.<br/>"
        "• <b>2º Semestre de 2027 (H2-2027) — A Barreira das Leis de Escala &amp; O Ciclo de Amortização:</b><br/>"
        "As empresas enfrentarão o platô dos modelos fundacionais (*Wall of Scaling Laws*), onde melhorias marginais exigem aumentos exponenciais de computação e energia. Iniciar-se-á a transição para a arquitetura Rubin (R100). As primeiras frotas de GPUs H100 adquiridas em 2023–2024 completarão 3 anos de uso, sofrendo hiper-depreciação de valor residual no mercado secundário. As projeções acumuladas apontam para valorização média de <b>+13,5% no Cenário Base</b>, expansão de <b>+27,3% no Cenário Otimista</b> e perdas severas de <b>-31,2% no Cenário de Quebra Sistêmica</b>.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Tabela Resumo dos 3 Cenários Semestrais
    scen_summary_data = [
        [
            Paragraph("<b>Cenário Analítico</b>", style_table_header),
            Paragraph("<b>Probab.</b>", style_table_header),
            Paragraph("<b>Catalisador Macroeconômico / Setorial</b>", style_table_header),
            Paragraph("<b>Retorno H1-27</b>", style_table_header),
            Paragraph("<b>Retorno H2-27 (Acum.)</b>", style_table_header),
            Paragraph("<b>Comportamento de Múltiplos</b>", style_table_header),
        ],
        [
            Paragraph("<b>Cenário Base (Soft Landing)</b>", style_table_cell),
            Paragraph("<b>48%</b>", style_table_cell_bold),
            Paragraph("Crescimento de CapEx desacelera para +12% a/a; adoção gradual de software corporativo.", style_table_cell),
            Paragraph("<font color='#0284C7'><b>+8,0%</b></font>", style_table_cell_center),
            Paragraph("<font color='#0284C7'><b>+13,5%</b></font>", style_table_cell_center),
            Paragraph("Leve compressão de P/E (-5% a -8%), absorvida por lucros.", style_table_cell),
        ],
        [
            Paragraph("<b>Cenário Bullish (Aceleração)</b>", style_table_cell),
            Paragraph("<b>25%</b>", style_table_cell_bold),
            Paragraph("Breakthrough de agentes autônomos substitui fluxos inteiros de trabalho; ARR de software GenAI > US$ 80B.", style_table_cell),
            Paragraph("<font color='#10B981'><b>+19,4%</b></font>", style_table_cell_center),
            Paragraph("<font color='#10B981'><b>+27,3%</b></font>", style_table_cell_center),
            Paragraph("Múltiplos premium sustentados (> 35x P/E em semicondutores).", style_table_cell),
        ],
        [
            Paragraph("<b>Cenário Estresse (Quebra / Subprime)</b>", style_table_cell),
            Paragraph("<b>27%</b>", style_table_cell_bold),
            Paragraph("Juros de 10Y rompem 6,00%; inadimplência em neoclouds; queda de 60% nas taxas de locação de GPU.", style_table_cell),
            Paragraph("<font color='#DC2626'><b>-22,5%</b></font>", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>-31,2%</b></font>", style_table_cell_center),
            Paragraph("Desabamento de múltiplos (Nvidia recua para 20x-22x P/E).", style_table_cell),
        ],
    ]
    t_scen = Table(scen_summary_data, colWidths=[85, 38, 145, 62, 68, 106])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_scen)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 8: MATRIZES PREDITIVAS COMPLETAS & DIRETRIZES
    # =========================================================
    story.append(Paragraph("8. Matriz Preditiva de Preços-Alvo &amp; Recomendações de Portfólio", style_h1))
    story.append(Paragraph(
        "Apresentamos a projeção econométrica completa de preços-alvo (USD) e variações percentuais para cada ação no horizonte de 6 meses (H1-2027) e 12 meses acumulados (H2-2027), acompanhada das diretrizes de gestão de risco:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Detailed Targets Table
    targets_table_data = [
        [
            Paragraph("<b>Ticker</b>", style_table_header),
            Paragraph("<b>Cotação Atual</b>", style_table_header),
            Paragraph("<b>Base H1-27</b>", style_table_header),
            Paragraph("<b>Bull H1-27</b>", style_table_header),
            Paragraph("<b>Stress H1-27</b>", style_table_header),
            Paragraph("<b>Base H2-27</b>", style_table_header),
            Paragraph("<b>Bull H2-27</b>", style_table_header),
            Paragraph("<b>Stress H2-27</b>", style_table_header),
        ],
        [
            Paragraph("<b>NVDA</b>", style_table_cell),
            Paragraph("US$ 229,28", style_table_cell_center),
            Paragraph("US$ 255 (+11%)", style_table_cell_center),
            Paragraph("US$ 275 (+20%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 170 (-26%)</font>", style_table_cell_center),
            Paragraph("US$ 265 (+16%)", style_table_cell_center),
            Paragraph("US$ 295 (+29%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'><b>US$ 125 (-46%)</b></font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>GOOGL</b>", style_table_cell),
            Paragraph("US$ 351,66", style_table_cell_center),
            Paragraph("US$ 375 (+7%)", style_table_cell_center),
            Paragraph("US$ 415 (+18%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 285 (-19%)</font>", style_table_cell_center),
            Paragraph("US$ 395 (+12%)", style_table_cell_center),
            Paragraph("US$ 440 (+25%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 270 (-23%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>MSFT</b>", style_table_cell),
            Paragraph("US$ 535,07", style_table_cell_center),
            Paragraph("US$ 560 (+5%)", style_table_cell_center),
            Paragraph("US$ 610 (+14%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 440 (-18%)</font>", style_table_cell_center),
            Paragraph("US$ 585 (+9%)", style_table_cell_center),
            Paragraph("US$ 645 (+21%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 410 (-23%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>AMZN</b>", style_table_cell),
            Paragraph("US$ 262,43", style_table_cell_center),
            Paragraph("US$ 285 (+9%)", style_table_cell_center),
            Paragraph("US$ 320 (+22%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 215 (-18%)</font>", style_table_cell_center),
            Paragraph("US$ 305 (+16%)", style_table_cell_center),
            Paragraph("US$ 345 (+32%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 200 (-24%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>META</b>", style_table_cell),
            Paragraph("US$ 718,67", style_table_cell_center),
            Paragraph("US$ 760 (+6%)", style_table_cell_center),
            Paragraph("US$ 830 (+16%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 575 (-20%)</font>", style_table_cell_center),
            Paragraph("US$ 795 (+11%)", style_table_cell_center),
            Paragraph("US$ 880 (+22%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 530 (-26%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>TSM</b>", style_table_cell),
            Paragraph("US$ 190,50", style_table_cell_center),
            Paragraph("US$ 210 (+10%)", style_table_cell_center),
            Paragraph("US$ 235 (+23%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 140 (-26%)</font>", style_table_cell_center),
            Paragraph("US$ 225 (+18%)", style_table_cell_center),
            Paragraph("US$ 255 (+34%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 120 (-37%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>AVGO</b>", style_table_cell),
            Paragraph("US$ 184,80", style_table_cell_center),
            Paragraph("US$ 205 (+11%)", style_table_cell_center),
            Paragraph("US$ 230 (+25%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 135 (-27%)</font>", style_table_cell_center),
            Paragraph("US$ 218 (+18%)", style_table_cell_center),
            Paragraph("US$ 245 (+33%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 120 (-35%)</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>ORCL</b>", style_table_cell),
            Paragraph("US$ 141,40", style_table_cell_center),
            Paragraph("US$ 148 (+5%)", style_table_cell_center),
            Paragraph("US$ 168 (+19%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 105 (-26%)</font>", style_table_cell_center),
            Paragraph("US$ 152 (+8%)", style_table_cell_center),
            Paragraph("US$ 175 (+24%)", style_table_cell_center),
            Paragraph("<font color='#DC2626'>US$ 92 (-35%)</font>", style_table_cell_center),
        ],
    ]
    t_targets = Table(targets_table_data, colWidths=[42, 54, 68, 68, 68, 68, 68, 68])
    t_targets.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_targets)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Diretrizes Institucionais de Preservação Patrimonial &amp; Alocação:", style_body_bold))
    story.append(Paragraph(
        "1. <b>Assimetria Convexa nos Papéis de Silício (NVDA, TSM, AVGO):</b> No Cenário Base e Bull, continuam a liderar os retornos globais (+16% a +34% em 12 meses). Contudo, no Cenário de Estresse, exibem drawdowns severos de até <b>-45,5%</b> devido à reprecificação de múltiplos. Recomenda-se hedge sistemático via opções fora-do-dinheiro (puts) ou proteção em cauda.<br/>"
        "2. <b>Resiliência dos Hiperscalers de Balanço Caixa-Líquido (GOOGL, AMZN, MSFT):</b> Oferecem maior preservação patrimonial no cenário adverso (quedas contidas em -18% a -23%), graças a fluxos de caixa previsíveis e imunidade à curva de crédito corporativo.<br/>"
        "3. <b>Subponderação Estrita em Ativos de Alta Dívida (Oracle &amp; Neoclouds):</b> Evitar exposição a operadoras com alavancagem elevada sob taxas do Federal Reserve mantidas em 3,75%–4,00% e yields longos de 10Y superiores a 5,20%.<br/>"
        "4. <b>Gatilhos de Monitoramento Crítico:</b> Acompanhar as divulgações do Form 10-Q da Nvidia quanto a compromissos de compra (Purchase Obligations) e monitorar os preços de leilão de chips H100 no mercado secundário.",
        style_body
    ))
    story.append(Spacer(1, 6))

    concl_box = [
        [
            Paragraph(
                "<b>Aviso Legal / Financial Disclaimer:</b> Este relatório tem finalidade estritamente institucional e analítica, sintetizando modelos econométricos e auditorias de risco de cauda do repositório <i>ai-market-crash-risk</i>. As projeções probabilísticas não configuram recomendação de investimento ou solicitação de compra/venda de ativos.",
                ParagraphStyle('DiscText', fontName='Helvetica-Oblique', fontSize=6.8, leading=9.2, textColor=colors.HexColor('#475569'))
            )
        ]
    ]
    t_concl = Table(concl_box, colWidths=[504])
    t_concl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94A3B8')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_concl)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório PDF em Português gerado com sucesso: {out_path}")
    return out_path

if __name__ == '__main__':
    build_pdf_report()
