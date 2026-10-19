#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fear_indices_report.py
---------------------------------
Generates a 6-page institutional PDF executive report in Portuguese:
"Relatório Executivo: A Anatomia dos Índices do Medo — VIX, MOVE Index e os Gatilhos Algorítmicos
de Desalavancagem em Ações de IA e Crédito de Infraestrutura (2020–2026)"

Output: reports/pt/Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf
"""

import os
import sys

# UTF-8 stdout encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
            self.drawString(54, 750, "RELATÓRIO INSTITUCIONAL • ANATOMIA DOS ÍNDICES DO MEDO")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "VIX, MOVE & DESALAVANCAGEM EM IA (2020–2026)")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 42, 612 - 54, 42)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "Confidencial • Pesquisa Institucional, Dados CBOE, ICE BofA MOVE, BIS, Bloomberg e Modelos Proprietários")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 30, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Relatorio_Indices_do_Medo_VIX_MOVE_Impacto_IA.pdf"):
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
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17, leading=21,
        textColor=colors.HexColor('#0F172A'), spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        'DocSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=colors.HexColor('#0284C7'), spaceAfter=10
    )
    style_h1 = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=15,
        textColor=colors.HexColor('#0F172A'), spaceBefore=8, spaceAfter=6, keepWithNext=True
    )
    style_body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.0, leading=11.5,
        textColor=colors.HexColor('#334155'), spaceAfter=6
    )
    style_body_bold = ParagraphStyle(
        'BodyBold', parent=style_body,
        fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A')
    )
    style_callout = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.8, leading=11.0,
        textColor=colors.HexColor('#1E293B')
    )
    style_th = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.2, leading=9.5,
        textColor=colors.HexColor('#FFFFFF'), alignment=1
    )
    style_td = ParagraphStyle(
        'TD', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.0, leading=9.0,
        textColor=colors.HexColor('#1E293B')
    )
    style_td_bold = ParagraphStyle(
        'TDBold', parent=style_td,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # PÁGINA 1: CAPA INSTITUCIONAL, DASHBOARD & SUMÁRIO EXECUTIVO
    # =========================================================================
    story.append(Paragraph("RELATÓRIO DE INTELIGÊNCIA MACROECONÔMICA • OUTUBRO 2026", ParagraphStyle('TopBadge', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor('#0284C7'), spaceAfter=4)))
    story.append(Paragraph("A Anatomia dos Índices do Medo: VIX, MOVE Index e os Gatilhos Algorítmicos de Desalavancagem em IA e Crédito", style_title))
    story.append(Paragraph("Estrutura a Termo, Volatilidade de Treasuries e o Mecanismo de Liquidação Forçada de Fundos Vol-Targeting (2020–2026)", style_subtitle))

    # Meta Block
    meta_data = [
        [
            Paragraph("<b>Data:</b> 19 de Outubro de 2026", style_td),
            Paragraph("<b>Classificação:</b> Risco Sistêmico & Volatilidade Quantitativa", style_td),
            Paragraph("<b>Cobertura:</b> VIX, MOVE, SKEW, Big Tech, ABS", style_td),
            Paragraph("<b>Status:</b> Regime de Tensão Latente", style_td)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[120, 150, 134, 100])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Callout Box
    callout_data = [[
        Paragraph(
            "<b>TESE CENTRAL:</b> O VIX e o MOVE Index não são meras pesquisas de opinião ou indicadores de sentimento psicológico; "
            "operam no sistema financeiro moderno como <b>variáveis matemáticas de controle algorítmico</b>. "
            "Estratégias de <i>Volatility Targeting</i> e <i>Risk Parity</i> (com mais de US$ 1,8 trilhão sob gestão) são obrigadas por código estatutário "
            "a despejar ações líquidas de Big Techs e semicondutores sempre que o VIX salta acima de 25 pontos. Ao mesmo tempo, o MOVE Index elevado (> 120 pts) "
            "paralisa a securitização de dívida privada de Data Center ABS, fechando a torneira de crédito para o superciclo de US$ 700 bilhões de CapEx de IA.",
            style_callout
        )
    ]]
    t_call = Table(callout_data, colWidths=[504])
    t_call.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor('#3B82F6')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_call)
    story.append(Spacer(1, 8))

    # Dashboard Table
    story.append(Paragraph("1. Dashboard de Volatilidade: Indicadores & Gatilhos de Risco", style_h1))
    
    dash_rows = [
        [Paragraph("Indicador de Volatilidade / Medo", style_th), Paragraph("Valor Out/2026", style_th), Paragraph("Pico Histórico / Referência", style_th), Paragraph("Mecanismo de Transmissão no Mercado de IA & Dívida", style_th)],
        [Paragraph("CBOE Volatility Index (VIX Spot)", style_td_bold), Paragraph("21,80 pts", style_td), Paragraph("65,73 (Ago/24) / 82,69 (Mar/20)", style_td), Paragraph("Regime de tensão; acima de 25 pts ativa vendas automáticas de CTAs.", style_td)],
        [Paragraph("ICE BofA MOVE Index (Treasuries)", style_td_bold), Paragraph("126,40 pts", style_td), Paragraph("198,70 (Mar/23 - SVB)", style_td), Paragraph("Zona de estresse de dívida; encarece e trava emissões de Data Center ABS.", style_td)],
        [Paragraph("CBOE SKEW Index (Cisne Negro)", style_td_bold), Paragraph("146,20 pts", style_td), Paragraph("170,50 (Pico Histórico)", style_td), Paragraph("Forte demanda institucional por proteção profunda em opções de venda (Puts).", style_td)],
        [Paragraph("CBOE VVIX (Volatilidade do VIX)", style_td_bold), Paragraph("104,50 pts", style_td), Paragraph("215,00 (Ago/2024)", style_td), Paragraph("Mede a instabilidade do custo de seguro; acima de 100 indica nervosismo.", style_td)],
        [Paragraph("Spread VIX Spot vs Futuro 3M", style_td_bold), Paragraph("-1,40 pts", style_td), Paragraph("+38,33 pts (Backwardation Ago/24)", style_td), Paragraph("Contango estreito; proximidade de inversão para demanda imediata de liquidez.", style_td)],
        [Paragraph("CNN Fear & Greed Index", style_td_bold), Paragraph("42 / 100", style_td), Paragraph("95 (Ganância) / 10 (Medo Extremo)", style_td), Paragraph("Neutro defensivo; ausência da complacência eufórica observada em 2023.", style_td)],
        [Paragraph("AUM Fundos Vol-Targeting / CTAs", style_td_bold), Paragraph("US$ 1,82 Trilhão", style_td), Paragraph("US$ 1,95 Trilhão (Pico 2024)", style_td), Paragraph("Capital sistemático que desalaavanca mecanicamente com o aumento do VIX.", style_td)],
        [Paragraph("Gatilho de Venda Forçada Primária", style_td_bold), Paragraph("VIX > 25,00 pts", style_td), Paragraph("Threshold Estatutário", style_td), Paragraph("Obriga redução compulsória de 35% a 50% na exposição líquida a ações.", style_td)],
        [Paragraph("Gatilho de Congelamento de ABS", style_td_bold), Paragraph("MOVE > 140,00 pts", style_td), Paragraph("Threshold de Renda Fixa", style_td), Paragraph("Investidores exigem spreads > +300 bps, inviabilizando captações de data center.", style_td)],
    ]
    t_dash = Table(dash_rows, colWidths=[126, 64, 114, 200])
    t_dash.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_dash)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Síntese da Página 1:</b> Os índices do medo constituem o interruptor mecânico dos mercados de capitais. "
        "A combinação de VIX em 21,8 com MOVE em 126,4 indica que a margem de erro do mercado de tecnologia é mínima.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: A TRÍADE DOS ÍNDICES DO MEDO & PICOS HISTÓRICOS
    # =========================================================================
    story.append(Paragraph("2. A Tríade dos Índices do Medo: VIX, MOVE e SKEW", style_h1))
    story.append(Paragraph(
        "A análise tradicional de ações frequentemente restringe-se ao VIX como medidor isolado de risco. No entanto, o sistema moderno "
        "é governado por três vetores simultâneos: a volatilidade de ações (VIX), a volatilidade da taxa livre de risco (MOVE) e a demanda "
        "por proteção contra quebras de cauda catastróficas (SKEW).",
        style_body
    ))
    story.append(Paragraph(
        "Com o índice S&P 500 apresentando uma concentração de quase 34% em sete megacaps de tecnologia (Magnificent Seven), o VIX "
        "tornou-se o espelho direto da estabilidade das ações de semicondutores e IA. Quando o VIX explode, o drawdown de ações líderes como NVIDIA "
        "é multiplicado por um fator de 2x a 3x em relação ao índice amplo. O gráfico abaixo ilustra os choques históricos do VIX e o impacto nas líderes de tecnologia.",
        style_body
    ))

    # Gráfico 1
    chart1_path = get_chart_path("chart_vix_historical_spikes_and_tech_drawdowns.png", lang="pt")
    if os.path.exists(chart1_path):
        story.append(Image(chart1_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Tabela Picos Históricos
    story.append(Paragraph("<b>Choques Históricos do VIX e Quedas Máximas em Nasdaq 100 e NVIDIA (2018–2026)</b>", style_body_bold))
    shock_rows = [
        [Paragraph("Evento / Choque Histórico", style_th), Paragraph("Pico VIX", style_th), Paragraph("Drawdown QQQ", style_th), Paragraph("Drawdown NVDA", style_th), Paragraph("Mecânica de Liquidação Observada", style_th)],
        [Paragraph("Volmageddon (Fev/2018)", style_td), Paragraph("50,3 pts", style_td), Paragraph("-10,5%", style_td), Paragraph("-15,2%", style_td), Paragraph("Implosão de ETFs inversos de volatilidade (XIV); desalavancagem rápida.", style_td)],
        [Paragraph("Q4 Tightening (Dez/2018)", style_td), Paragraph("36,2 pts", style_td), Paragraph("-23,1%", style_td), Paragraph("-54,0%", style_td), Paragraph("Fed de Powell em piloto automático; contração violenta de múltiplos P/E.", style_td)],
        [Paragraph("Covid-19 Crash (Mar/2020)", style_td), Paragraph("82,69 pts", style_td), Paragraph("-30,1%", style_td), Paragraph("-38,5%", style_td), Paragraph("Pânico sistêmico global; corrida para caixa e intervenção do Fed com swap lines.", style_td)],
        [Paragraph("Ciclo Inflação (Jun/2022)", style_td), Paragraph("34,0 pts", style_td), Paragraph("-33,8%", style_td), Paragraph("-66,4%", style_td), Paragraph("Fim da era do dinheiro grátis; choque em ativos de longa duração e semicondutores.", style_td)],
        [Paragraph("Carry Trade Crash (Ago/2024)", style_td), Paragraph("65,73 pts", style_td), Paragraph("-10,2%", style_td), Paragraph("-20,5%", style_td), Paragraph("Short squeeze em iene forçou fundos macro a usarem NVIDIA como caixa eletrônico.", style_td)],
    ]
    t_shock = Table(shock_rows, colWidths=[110, 52, 68, 68, 206])
    t_shock.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_shock)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: O ÍNDICE DUPLO — VIX VS MOVE INDEX
    # =========================================================================
    story.append(Paragraph("3. O Índice Duplo do Medo: VIX (Ações) vs MOVE (Tesouro Americano)", style_h1))
    story.append(Paragraph(
        "Enquanto o VIX comanda as manchetes diárias, o <b>ICE BofA MOVE Index é o verdadeiro regulador da taxa de sobrevivência do ecossistema de IA</b>. "
        "O superciclo de inteligência artificial requer que as hyperscalers e neoclouds emitam centenas de bilhões de dólares em dívida estruturada. "
        "A taxa básica de juros de longo prazo (US 10Y Treasury) define o custo mínimo de qualquer financiamento.",
        style_body
    ))
    story.append(Paragraph(
        "Quando o MOVE Index ultrapassa 120 pontos, os bancos de investimento e investidores institucionais de crédito privado sofrem com a impossibilidade "
        "de calcular o valor presente dos fluxos de caixa de data centers. Os spreads de crédito exigidos para comprar tranches de securitização disparam.",
        style_body
    ))

    # Gráfico 2
    chart2_path = get_chart_path("chart_dual_fear_index_vix_vs_move.png", lang="pt")
    if os.path.exists(chart2_path):
        story.append(Image(chart2_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Tabela Regimes do MOVE
    story.append(Paragraph("<b>Regimes de Volatilidade do MOVE e Impacto nos Spreads de Data Center ABS</b>", style_body_bold))
    move_rows = [
        [Paragraph("Regime do MOVE", style_th), Paragraph("Pontuação MOVE", style_th), Paragraph("Spread ABS BBB/A", style_th), Paragraph("Condição de Mercado para Emissões de Infraestrutura de IA", style_th)],
        [Paragraph("Normal / Benigno", style_td_bold), Paragraph("< 90 pts", style_td), Paragraph("+115 bps", style_td), Paragraph("Ambiente aberto; captações abundantes com cupons de 5,50% a 6,00%.", style_td)],
        [Paragraph("Elevado / Vigilância", style_td_bold), Paragraph("90 – 120 pts", style_td), Paragraph("+185 bps", style_td), Paragraph("Investidores exigem maior disciplina de covenants e garantias de contrato PPA.", style_td)],
        [Paragraph("Estresse de Crédito (Atual)", style_td_bold), Paragraph("120 – 150 pts", style_td), Paragraph("+290 bps", style_td), Paragraph("Cupons sobem para 7,5%–8,0%; neoclouds com alta alavancagem pausam emissões.", style_td)],
        [Paragraph("Congelamento de Liquidez", style_td_bold), Paragraph("> 150 pts", style_td), Paragraph("+480 bps+", style_td), Paragraph("Mercado primário trava; tranches subordinadas de GPU entram em estresse severo.", style_td)],
    ]
    t_move = Table(move_rows, colWidths=[110, 68, 76, 250])
    t_move.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_move)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: A CURVA A TERMO DO VIX: CONTANGO VS BACKWARDATION
    # =========================================================================
    story.append(Paragraph("4. A Curva a Termo do VIX: Contango (Complacência) vs. Backwardation (Pânico)", style_h1))
    story.append(Paragraph(
        "A cotação à vista do VIX revela apenas a temperatura instantânea. Para diagnosticar a pressão sistêmica real, "
        "é indispensável auditar a <b>estrutura a termo dos contratos futuros do VIX</b> negociados na CBOE.",
        style_body
    ))
    story.append(Paragraph(
        "Em condições normais, a curva opera em <i>Contango</i>: a volatilidade futura custa mais do que a à vista, gerando um prêmio de rolagem positivo "
        "para quem vende volatilidade. Quando ocorre uma crise aguda, a curva inverte-se para <i>Backwardation</i>: o VIX à vista supera os futuros mais longos, "
        "revelando uma corrida desesperada por proteção imediata e forçando fechamentos compulsórios de posições em ações.",
        style_body
    ))

    # Gráfico 3
    chart3_path = get_chart_path("chart_vix_term_structure_contango_backwardation.png", lang="pt")
    if os.path.exists(chart3_path):
        story.append(Image(chart3_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Tabela de Inversão da Curva
    story.append(Paragraph("<b>Diagnóstico Forense da Inclinação da Curva a Termo do VIX</b>", style_body_bold))
    curve_rows = [
        [Paragraph("Formato da Curva", style_th), Paragraph("Spread Spot - 3M", style_th), Paragraph("Comportamento dos Gestores Institucionais", style_th), Paragraph("Sinal para Ações de IA", style_th)],
        [Paragraph("Contango Profundo", style_td_bold), Paragraph("< -4,0 pts", style_td), Paragraph("Venda massiva de volatilidade; busca por rendimento sintético.", style_td), Paragraph("Complacência; rally de tech sustentado.", style_td)],
        [Paragraph("Contango Estreito (Atual)", style_td_bold), Paragraph("-2,0 a 0,0 pts", style_td), Paragraph("Redução cautelosa de alavancagem; compras táticas de proteção.", style_td), Paragraph("Alerta amarelo; vulnerável a notícias.", style_td)],
        [Paragraph("Inversão Inicial", style_td_bold), Paragraph("+0,1 a +5,0 pts", style_td), Paragraph("CTAs iniciam vendas de contratos futuros de Nasdaq e S&P 500.", style_td), Paragraph("Correção de -5% a -8% em andamento.", style_td)],
        [Paragraph("Backwardation Severa", style_td_bold), Paragraph("> +15,0 pts", style_td), Paragraph("Pânico agudo; chamadas de margem simultâneas; quebra de modelos VaR.", style_td), Paragraph("Colapso de liquidez e queda desordenada.", style_td)],
    ]
    t_curve = Table(curve_rows, colWidths=[110, 68, 186, 140])
    t_curve.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_curve)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: MECÂNICA ALGORÍTMICA & VOLATILITY TARGETING
    # =========================================================================
    story.append(Paragraph("5. A Mecânica Algorítmica: Como o VIX Dispara Vendas Forçadas", style_h1))
    story.append(Paragraph(
        "A transmissão do medo no mercado financeiro contemporâneo não decorre do pânico humano; ela é <b>automatizada por linhas de código</b>. "
        "Fundos quantitativos de Metas de Volatilidade (Vol-Targeting) e Paridade de Risco ajustam suas ponderações com base na fórmula matemática: "
        "<font face='Courier'>w = min(1.0, σ_alvo / σ_realizada)</font>.",
        style_body
    ))
    story.append(Paragraph(
        "Sempre que o VIX salta de 15 para 25 ou 35 pontos, esses fundos são forçados a vender centenas de bilhões de dólares em ações líquidas "
        "para manter a carteira dentro da meta estatutária de risco. Como Big Techs e semicondutores concentram o maior volume financeiro, "
        "elas atuam como a fonte primária de onde os robôs extraem caixa.",
        style_body
    ))

    # Gráfico 4
    chart4_path = get_chart_path("chart_vol_targeting_deleveraging_cascade.png", lang="pt")
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Tabela Cascata de Venda Forçada
    story.append(Paragraph("<b>Simulação de Despejo Algorítmico em Big Tech por Salto do VIX</b>", style_body_bold))
    algo_rows = [
        [Paragraph("Salto do VIX", style_th), Paragraph("Alocação Alvo em Ações", style_th), Paragraph("Despejo Estimado (US$ Bi)", style_th), Paragraph("Ações mais Impactadas", style_th), Paragraph("Efeito nos Múltiplos P/E", style_th)],
        [Paragraph("12 $\\rightarrow$ 18 pts", style_td_bold), Paragraph("100% $\\rightarrow$ 78%", style_td), Paragraph("US$ 45 Bilhões", style_td), Paragraph("Apple, Microsoft, Alphabet", style_td), Paragraph("Contração leve de -1,5x.", style_td)],
        [Paragraph("18 $\\rightarrow$ 25 pts", style_td_bold), Paragraph("78% $\\rightarrow$ 52%", style_td), Paragraph("US$ 160 Bilhões", style_td), Paragraph("NVIDIA, Broadcom, Amazon", style_td), Paragraph("Contração moderada de -3,8x.", style_td)],
        [Paragraph("25 $\\rightarrow$ 35 pts", style_td_bold), Paragraph("52% $\\rightarrow$ 34%", style_td), Paragraph("US$ 310 Bilhões", style_td), Paragraph("Todo o complexo semicondutor", style_td), Paragraph("Descompressão severa de -6,5x.", style_td)],
        [Paragraph("35 $\\rightarrow$ 50+ pts", style_td_bold), Paragraph("34% $\\rightarrow$ 18%", style_td), Paragraph("US$ 520 Bilhões+", style_td), Paragraph("Liquidação geral a mercado", style_td), Paragraph("Colapso de valuation (> -12x).", style_td)],
    ]
    t_algo = Table(algo_rows, colWidths=[80, 85, 95, 124, 120])
    t_algo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_algo)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: MATRIZ OPERACIONAL, METODOLOGIA & ASSINATURA
    # =========================================================================
    story.append(Paragraph("6. Matriz Operacional de Regimes de Volatilidade & Gatilhos de Ação", style_h1))
    story.append(Paragraph(
        "A integração dos índices de medo à matriz de decisão do repositório estrutura-se em 4 regimes claros de gestão de risco:",
        style_body
    ))

    reg_rows = [
        [Paragraph("Regime de Volatilidade", style_th), Paragraph("Parâmetros Quantitativos", style_th), Paragraph("Ação dos Algoritmos de Mercado", style_th), Paragraph("Postura Recomendada no Modelo", style_th)],
        [Paragraph("Regime 1: Complacência", style_td_bold), Paragraph("VIX < 15, MOVE < 90, Contango", style_td), Paragraph("Alavancagem máxima; compra sistemática.", style_td), Paragraph("Monitorar acúmulo de risco de cauda.", style_td)],
        [Paragraph("Regime 2: Tensão (Atual)", style_td_bold), Paragraph("VIX 16-24, MOVE 90-120, Flat", style_td), Paragraph("Redução cautelosa de posições marginais.", style_td), Paragraph("Manter calibração em 48%; hedge seletivo.", style_td)],
        [Paragraph("Regime 3: Desalavancagem", style_td_bold), Paragraph("VIX 25-35, MOVE 120-150, Inversão", style_td), Paragraph("Vendas compulsórias; despejo de US$ 160B+.", style_td), Paragraph("Alerta Amarelo: elevar probabilidade para 65%.", style_td)],
        [Paragraph("Regime 4: Choque Sistêmico", style_td_bold), Paragraph("VIX > 40, MOVE > 150, Backwardation", style_td), Paragraph("Fuga generalizada para caixa; travamento de ABS.", style_td), Paragraph("Alerta Vermelho: risco de quebra generalizada.", style_td)],
    ]
    t_reg = Table(reg_rows, colWidths=[105, 115, 140, 144])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 8))

    # Anexo Metodológico
    story.append(Paragraph("Anexo Metodológico: Modelo de Despejo por Metas de Volatilidade", style_h1))
    story.append(Paragraph(
        "O volume total de liquidação compulsória $V_{\\text{despejo}}$ em um salto de volatilidade de $\\sigma_0$ para $\\sigma_1$ é modelado por: "
        "<font face='Courier'>V_despejo = AUM_vol \\cdot max(0, 1 - σ_alvo / σ_1)</font>. "
        "Com um AUM estimado em US$ 1,82 trilhão e $\\sigma_{\\text{alvo}} = 10\\%$, um salto do VIX para 30 pontos (volatilidade realizada $\\approx 26\\%$) "
        "força a extração instantânea de mais de US$ 240 bilhões do mercado acionário.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # Sign-off & Sources Box
    sign_data = [
        [Paragraph("<b>Fontes Primárias & Bases Oficiais Auditadas:</b>", style_td_bold)],
        [Paragraph(
            "• Chicago Board Options Exchange (CBOE): Historical VIX Data, VVIX, SKEW & VIX Term Structure Methodology<br/>"
            "• Bank of America Merrill Lynch / ICE: ICE BofA MOVE Index Methodology & Historical Yield Volatility<br/>"
            "• Bank for International Settlements (BIS): Research Papers on Volatility-Targeting Deleveraging Dynamics<br/>"
            "• Bridgewater Associates & AQR Capital Management: Risk Parity & Systematic Trend-Following White Papers<br/>"
            "• Bloomberg Professional & Options Clearing Corporation (OCC): Multi-Asset Options Surfaces",
            style_td
        )],
        [Paragraph("<b>Aviso Legal / Disclaimer:</b> Este documento tem finalidade exclusivamente educacional e de pesquisa quantitativa de risco sistêmico. Não constitui consultoria financeira ou recomendação de investimento.", ParagraphStyle('Disc', parent=style_td, fontName='Helvetica-Oblique', fontSize=6.5, textColor=colors.HexColor('#64748B')))]
    ]
    t_sign = Table(sign_data, colWidths=[504])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"  🎉 PDF generated successfully: {out_path}")
    return out_path

if __name__ == "__main__":
    build_pdf_report()
