#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_recent_market_update_report.py
-----------------------------------------
Generates an 8-page institutional PDF executive report in Portuguese:
"Relatório Executivo: Atualização de Mercado (Outubro 2026) — Cancelamento Microsoft-Nscale,
Desconto de IPO da Anthropic, O Abismo da Rede Elétrica e Recalibração de Projeções (2026–2029)"

Output: reports/pt/Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf
"""

import os
import sys
import datetime

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
            self.drawString(54, 750, "RELATÓRIO INSTITUCIONAL • ATUALIZAÇÃO OUT/2026")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "GARGALO DA REDE & CENÁRIOS RECALIBRADOS")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidencial • Pesquisa Institucional, Demonstrativos SEC, FT, National Grid UK, Euronext e Modelos Proprietários")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf"):
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
        fontSize=15.0,
        leading=18.5,
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
    # PÁGINA 1: CAPA EXECUTIVA, DASHBOARD DE INDICADORES & TABELA MASTER
    # =========================================================
    header_data = [
        [
            Paragraph("<b>RELATÓRIO INSTITUCIONAL • ATUALIZAÇÃO EXTRAORDINÁRIA DE RISCO</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#DC2626'))),
            Paragraph(f"Data Base: {datetime.date.today().strftime('%d/%m/%Y')} | Horizonte: 2026–2029", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[330, 174])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Atualização Estratégica: Acordo Microsoft-Nscale, Desconto de IPO da Anthropic, o Abismo da Rede Elétrica e Recalibração de Projeções (2026–2029)", style_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Auditoria dos fatos recentes de outubro de 2026: a transição definitiva do gargalo de silício para a escassez física de energia, a desaceleração de receitas no pré-IPO e o aumento da probabilidade de choque de crédito.", style_subtitle))
    story.append(Spacer(1, 8))

    # Banner de Alerta Crítico
    box_alert = [
        [
            Paragraph("<b>AVISO DE INFLEXÃO CÍCLICA (OUTUBRO DE 2026):</b> O cancelamento pela Microsoft do contrato de locação do megacampus da Nscale em Essex (UK) — devido à impossibilidade de energização da rede antes dos anos 2030 — somado ao corte de US$ 500 bilhões no valuation de IPO da Anthropic confirmam o início da compressão física e financeira da infraestrutura de IA. A probabilidade de ocorrência do Cenário de Choque de Crédito e Fila da Rede é elevada de 34% para 40%.", style_callout)
        ]
    ]
    t_alert = Table(box_alert, colWidths=[504])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor('#DC2626')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_alert)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Painel Consolidado de Fatos e Indicadores Reavaliados (Outubro de 2026)</b>", style_h1))
    
    kpi_table_data = [
        [
            Paragraph("Evento / Indicador Chave", style_table_header),
            Paragraph("Métrica Observada", style_table_header),
            Paragraph("Diagnóstico Técnico", style_table_header),
            Paragraph("Impacto no Risco Sistêmico", style_table_header)
        ],
        [
            Paragraph("<b>Acordo Microsoft & Nscale</b>", style_table_cell_bold),
            Paragraph("Rescisão em Essex (50–90 MW)", style_table_cell_center),
            Paragraph("Rede elétrica adiada para 2030s", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Crítico:</b></font> Desvaloriza Neoclouds e atrasa IPOs", style_table_cell)
        ],
        [
            Paragraph("<b>Valuation de IPO da Anthropic</b>", style_table_cell_bold),
            Paragraph("Corte de $2,0T para ~$1,5T", style_table_cell_center),
            Paragraph("Desconto de US$ 500B (-25%)", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Severo:</b></font> Fim da precificação puramente exponencial", style_table_cell)
        ],
        [
            Paragraph("<b>Receita Trimestral Anthropic (Q3)</b>", style_table_cell_bold),
            Paragraph("US$ 16,8B (+44,8% QoQ)", style_table_cell_center),
            Paragraph("Desaceleração de 146% para 45%", style_table_cell),
            Paragraph("<font color='#D97706'><b>Moderado/Alto:</b></font> Aumento do custo de aquisição", style_table_cell)
        ],
        [
            Paragraph("<b>Fila de Transformadores GSU</b>", style_table_cell_bold),
            Paragraph("36 a 60 Meses de Espera", style_table_cell_center),
            Paragraph("Escassez crônica de aço silício GOES", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Físico:</b></font> 30% a 50% dos campi não energizam", style_table_cell)
        ],
        [
            Paragraph("<b>CapEx Anualizado em IA</b>", style_table_cell_bold),
            Paragraph("US$ 650 a US$ 700 Bilhões / Ano", style_table_cell_center),
            Paragraph("Pico de intensidade de capital", style_table_cell),
            Paragraph("<font color='#D97706'><b>Financeiro:</b></font> Fuga para crédito privado fora de balanço", style_table_cell)
        ],
        [
            Paragraph("<b>Probabilidade de Choque (Cenário 2)</b>", style_table_cell_bold),
            Paragraph("Elevada de 34% para 40%", style_table_cell_center),
            Paragraph("Aumento de 6 p.p. no risco de calote", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Sistêmico:</b></font> Quebra de garantias colaterais de GPUs", style_table_cell)
        ]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[130, 114, 135, 125])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Síntese dos Quatro Eixos de Análise Deste Relatório:</b>", style_body_bold))
    story.append(Paragraph("<b>1. A Física Inflexível da Rede Elétrica:</b> Como a saturação das linhas de transmissão está forçando gigantes de tecnologia a cancelar compromissos contratuais de bilhões de dólares.<br/>"
                           "<b>2. O Realismo dos Valuations Pré-IPO:</b> A compressão dos múltiplos de laboratórios fundacionais diante de pesados custos de computação e desaceleração sequencial.<br/>"
                           "<b>3. A Migração para Veículos Fora de Balanço:</b> Como os hyperscalers estão utilizando gestoras de crédito privado (Blackstone, GAIIP, Blue Owl) para financiar transformadores e data centers sem inflar seu passivo direto.<br/>"
                           "<b>4. Recalibração de Preços-Alvo e Risco:</b> A nova modelagem de perdas para ações líderes (NVDA, TSM, MSFT, ORCL) e a reavaliação dos títulos estruturados de data centers.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 2: O CASO MICROSOFT-NSCALE E O COLAPSO EM ESSEX
    # =========================================================
    story.append(Paragraph("O Caso Microsoft & Nscale: A Fratura em Essex e o Limite Físico da Rede Elétrica", style_h1))
    story.append(Paragraph("Em outubro de 2026, a operadora britânica de nuvem e infraestrutura Nscale — apoiada financeiramente pela Nvidia e associada a megaprojetos na Europa — sofreu o cancelamento formal por parte da Microsoft de seu contrato de locação e reserva de processamento no campus de Loughton (Essex, Reino Unido).", style_body))
    story.append(Spacer(1, 4))

    chart_grid = get_chart_path("chart_grid_bottleneck_delays.png", lang="pt")
    if os.path.exists(chart_grid):
        story.append(Image(chart_grid, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>A Anatomia do Projeto Loughton e a Causa da Ruptura:</b>", style_body_bold))
    story.append(Paragraph("• <b>A Ambição do Projeto:</b> Planejado com 50 MW iniciais e expansão para 90 MW, o campus visava abrigar aproximadamente 23.000 GPUs Nvidia GB300 (Blackwell Ultra), posicionado pelo governo do Reino Unido como o maior supercomputador soberano de inteligência artificial da Europa.<br/>"
                           "• <b>O Veredito da National Grid UK:</b> A distribuidora oficial notificou formalmente os desenvolvedores de que a subestação regional e os corredores de alta tensão estão completamente saturados. O prazo estimado para entrega da carga elétrica necessária foi deslocado para a <b>década de 2030</b> (um atraso operacional de 5 a 7 anos!).<br/>"
                           "• <b>A Decisão da Microsoft:</b> Diante da impossibilidade de operar o hardware neste ciclo tecnológico, a Microsoft rescindiu o acordo de cliente-âncora, evitando imobilizar capital em infraestrutura que ficaria ociosa.<br/>"
                           "• <b>O Impacto Corporativo na Nscale:</b> A Nscale depende da Microsoft e da Anthropic para a grande maioria do seu pipeline de receitas. Esse rompimento coloca em xeque a avaliação de mercado e o cronograma do seu planejado IPO na Bolsa de Nova York (NYSE).", style_body))
    story.append(Spacer(1, 4))

    box_nscale = [
        [
            Paragraph("<b>LIÇÃO FORENSE FUNDAMENTAL:</b> O episódio de Essex prova empiricamente a tese central deste repositório: não há capital financeiro capaz de acelerar a manufatura de transformadores e a construção de linhas de transmissão. A computação acelerada colidiu com a inércia do setor elétrico.", style_callout)
        ]
    ]
    t_box_nscale = Table(box_nscale, colWidths=[504])
    t_box_nscale.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor('#94A3B8')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_box_nscale)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 3: ANTHROPIC: DESACELERAÇÃO E CORTE DE VALUATION
    # =========================================================
    story.append(Paragraph("Anthropic: Auditoria dos Resultados de Q3 e o Desconto de US$ 500 Bilhões no Valuation", style_h1))
    story.append(Paragraph("Durante a apresentação confidencial a investidores institucionais em São Francisco antes de sua estreia pública prevista para novembro de 2026, a Anthropic expôs dados financeiros que revelam tanto sua escala vertiginosa quanto os primeiros sintomas de arrefecimento da curva marginal de crescimento.", style_body))
    story.append(Spacer(1, 4))

    chart_anth = get_chart_path("chart_anthropic_growth_deceleration_valuation.png", lang="pt")
    if os.path.exists(chart_anth):
        story.append(Image(chart_anth, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Decomposição Financeira dos Resultados e Drivers do Desconto:</b>", style_body_bold))
    story.append(Paragraph("1. <b>Desaceleração Sequencial (QoQ):</b> A receita da Anthropic saltou de <b>US$ 4,7 Bilhões no Q1-2026</b> para <b>US$ 11,6 Bilhões no Q2-2026 (+146,8%)</b>. No entanto, o terceiro trimestre fechou em <b>US$ 16,8 Bilhões (+44,8%)</b>. Embora a escala seja gigantesca, o arrefecimento da taxa marginal alertou os gestores para a maturação da adoção empresarial inicial.<br/>"
                           "2. <b>O Corte no Valuation de Abertura:</b> Fundos que anteriormente discutiam valuations próximos a <b>US$ 2,0 Trilhões</b> passaram a exigir um teto de precificação em torno de <b>US$ 1,5 Trilhão</b> — eliminando US$ 500 bilhões em valor esperado (-25%).<br/>"
                           "3. <b>O Peso dos Compromissos de Computação (Take-or-Pay):</b> Para sustentar seu volume operacional, a Anthropic assumiu compromissos plurianuais de infraestrutura com AWS, Google Cloud e data centers que ultrapassam <b>US$ 30 bilhões em passivos contratuais</b>.<br/>"
                           "4. <b>Combate a SPVs Secundários:</b> A companhia invalidou formalmente negociações em veículos de propósito específico não autorizados no mercado secundário, estancando a especulação desregulada antes da precificação oficial.", style_body))
    story.append(Spacer(1, 4))

    box_anth = [
        [
            Paragraph("<b>DIAGNÓSTICO INSTITUCIONAL:</b> A transição do múltiplo de valuation da Anthropic de 40x receita projetada para ~25x reflete a exigência de Wall Street por rentabilidade comprovada e cobertura segura dos pesados custos fixos de processamento em nuvem.", style_callout)
        ]
    ]
    t_box_anth = Table(box_anth, colWidths=[504])
    t_box_anth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_box_anth)

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 4: O ABISMO DA REDE ELÉTRICA GLOBAL (THE GRID WALL)
    # =========================================================
    story.append(Paragraph("O Abismo da Rede Elétrica Global: Equipamentos Críticos, Filas e Cancelamento de Obras", style_h1))
    story.append(Paragraph("A restrição primária à expansão da Inteligência Artificial em 2026 não é a disponibilidade de semicondutores, mas sim a capacidade dos sistemas elétricos de transmitir e fornecer gigawatts contínuos com alta estabilidade.", style_body))
    story.append(Spacer(1, 6))

    grid_table_data = [
        [
            Paragraph("Componente / Variável", style_table_header),
            Paragraph("Prazo Normal (2021)", style_table_header),
            Paragraph("Prazo Atual (2026)", style_table_header),
            Paragraph("Impacto Operacional nos Projetos", style_table_header)
        ],
        [
            Paragraph("<b>Transformadores Step-Up (GSU)</b>", style_table_cell_bold),
            Paragraph("14 a 18 Meses", style_table_cell_center),
            Paragraph("<b>36 a 60 Meses (3-5 Anos)</b>", style_table_cell_center),
            Paragraph("Paralisação de entrega de subestações dedicadas", style_table_cell)
        ],
        [
            Paragraph("<b>Disjuntores de Alta Tensão</b>", style_table_cell_bold),
            Paragraph("10 a 12 Meses", style_table_cell_center),
            Paragraph("<b>30 a 42 Meses</b>", style_table_cell_center),
            Paragraph("Falta de equipamentos de manobra em 500 kV", style_table_cell)
        ],
        [
            Paragraph("<b>Fila de Interconexão (FERC / PJM)</b>", style_table_cell_bold),
            Paragraph("2 a 3 Anos", style_table_cell_center),
            Paragraph("<b>5 a 7 Anos</b>", style_table_cell_center),
            Paragraph("Estudos de impacto de rede travados em concessionárias", style_table_cell)
        ],
        [
            Paragraph("<b>Preço de Capacidade (PJM Auction)</b>", style_table_cell_bold),
            Paragraph("US$ 28,92 / MW-dia", style_table_cell_center),
            Paragraph("<b>US$ 269,92 / MW-dia</b>", style_table_cell_center),
            Paragraph("Aumento de quase 10x no custo de garantia de potência", style_table_cell)
        ],
        [
            Paragraph("<b>Taxa de Atraso / Cancelamento</b>", style_table_cell_bold),
            Paragraph("< 10% dos Projetos", style_table_cell_center),
            Paragraph("<b>30% a 50% dos Projetos</b>", style_table_cell_center),
            Paragraph("Desistência de operadoras por falta de ponto de conexão", style_table_cell)
        ]
    ]
    t_grid_detail = Table(grid_table_data, colWidths=[130, 95, 110, 169])
    t_grid_detail.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_grid_detail)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>As Três Implicações Estruturais do Choque Elétrico:</b>", style_body_bold))
    story.append(Paragraph("1. <b>Clusters Afundados e Depreciação Ociosa:</b> Operadoras que encomendaram clusters de GPUs Blackwell antes de assegurar o contrato de energia final enfrentam despesas de amortização e juros sobre equipamentos que permanecem encaixotados em armazéns.<br/>"
                           "2. <b>A Corrida por Energia Nuclear e Contratos Behind-the-Meter:</b> O estrangulamento da rede pública acelerou acordos dedicados fora da rede, como a reativação de Three Mile Island pela Constellation para a Microsoft, os acordos de reatores modulares (SMR) da Google com a Kairos Power e o campus nuclear da Amazon com a Talen Energy. Contudo, esses reatores só fornecem potência comercial no horizonte 2028–2032.<br/>"
                           "3. <b>Repatriação de Projetos para Nórdicos e Golfo:</b> Diante da paralisia na Europa Ocidental e no litoral leste dos EUA, os investimentos migram para locais com energia hídrica ou gás abundante (Noruega, Finlândia, Suécia e Emirados Árabes).", style_body))

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 5: SUPERCICLO DE CAPEX ($700B) E CRÉDITO PRIVADO
    # =========================================================
    story.append(Paragraph("O Superciclo de CapEx de US$ 700 Bilhões e a Engenharia Fora de Balanço", style_h1))
    story.append(Paragraph("Para sustentar o ritmo alucinante de gastos em data centers e energia sem colocar em risco seus ratings de crédito corporativo grau de investimento (AAA/AA), os maiores hyperscalers mundiais recorreram massivamente a estruturas de financiamento fora de balanço e fundos de crédito privado.", style_body))
    story.append(Spacer(1, 4))

    chart_capex = get_chart_path("chart_hyperscaler_capex_vs_private_credit.png", lang="pt")
    if os.path.exists(chart_capex):
        story.append(Image(chart_capex, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>A Mecânica dos Master Trusts e Veículos SPV em Infraestrutura:</b>", style_body_bold))
    story.append(Paragraph("• <b>Isolamento Contábil:</b> Em vez de financiar a construção civil de mega-campi diretamente no balanço matriz, hyperscalers criam Joint Ventures e Entidades de Propósito Específico (SPVs) controladas por gestoras de infraestrutura (BlackRock/GIP, Blackstone, Blue Owl, Apollo, Magnetar).<br/>"
                           "• <b>Alavancagem de Crédito Privado:</b> O SPV capta centenas de bilhões de dólares emitindo dívida privada e títulos estruturados (Data Center ABS). A Big Tech atua apenas como locatária via contratos operacionais (*triple net leases*).<br/>"
                           "• <b>O Fundo GAIIP (Global AI Infrastructure Investment Partnership):</b> A aliança entre BlackRock, Global Infrastructure Partners (GIP), Microsoft e MGX visa mobilizar entre US$ 30 e US$ 100 bilhões em capital privado para energia e data centers, aliviando o passivo direto da Microsoft.<br/>"
                           "• <b>A Ilusão de Descolamento:</b> Embora o passivo não conste como dívida financeira na matriz, os compromissos de pagamento de aluguel representam passivos fixos inescapáveis. Uma frustração nas receitas de IA comprometerá a capacidade do ecossistema de honrar essas obrigações.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 6: RECALIBRAÇÃO DOS 3 CENÁRIOS DE QUEBRA (2026-2029)
    # =========================================================
    story.append(Paragraph("Recalibração Formal dos Cenários de Quebra de Mercado (2026–2029)", style_h1))
    story.append(Paragraph("A inclusão dos choques observados em outubro de 2026 exige a reconfiguração dos pesos probabilísticos e dos parâmetros de estresse do modelo econométrico:", style_body))
    story.append(Spacer(1, 4))

    chart_probs = get_chart_path("chart_updated_crash_probabilities_2026_2029.png", lang="pt")
    if os.path.exists(chart_probs):
        story.append(Image(chart_probs, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Detalhamento da Matriz de Cenários Recalibrada:</b>", style_body_bold))
    story.append(Paragraph("• <b>Cenário 1: Desaceleração Ordenada (Probabilidade reduzida de 48% para 42%):</b> O crescimento do CapEx acomoda-se em torno de +10% a/a; a monetização corporativa de software avança de forma estável; os múltiplos de avaliação sofrem compressão moderada (S&P cai 10% a 15%, Nasdaq 18% a 22%); tranches seniores Classe A de ABS permanecem integralmente preservadas.<br/>"
                           "• <b>Cenário 2: Choque de Crédito e Fila da Rede (Probabilidade elevada de 34% para 40%):</b> O gatilho é acionado pelo cancelamento em massa de contratos de data centers sem energia, quebra de covenants de dívida em Neoclouds ($DSCR < 1,10x$), descontos severos de valuation em rodadas de IPO e colapso no mercado secundário de GPUs usadas. Queda projetada de 25% a 32% no S&P 500 e 35% a 45% no Nasdaq, com liquidação de tranches de crédito mezanino e equity de ABS.<br/>"
                           "• <b>Cenário 3: Tempestade Perfeita Sistêmica (Probabilidade mantida em 18%):</b> Ruptura simultânea combinando o colapso do crédito de IA com estresse nos leilões do Tesouro dos EUA (Dívida de US$ 40T a juros >5,5%) e atritos militares no Estreito de Taiwan. O Nasdaq despenca mais de 55% e o S&P mais de 45%, exigindo linhas de liquidez emergenciais do Fed.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 7: MATRIZ RECALIBRADA DE PREÇOS-ALVO DAS AÇÕES (H2-2027)
    # =========================================================
    story.append(Paragraph("Matriz Preditiva Recalibrada de Preços-Alvo para Ações Líderes (H2-2027)", style_h1))
    story.append(Paragraph("Abaixo é apresentada a tabela de preços-alvo e severidade de perda para as 8 empresas líderes e índices consolidados, incorporando o aumento da probabilidade do Cenário de Choque de Crédito e Fila da Rede:", style_body))
    story.append(Spacer(1, 6))

    stock_target_data = [
        [
            Paragraph("Ativo / Ticker", style_table_header),
            Paragraph("Preço Atual", style_table_header),
            Paragraph("Alvo Base (H2)", style_table_header),
            Paragraph("Retorno Base", style_table_header),
            Paragraph("Alvo Estresse (Grid/Créd)", style_table_header),
            Paragraph("Queda Estresse", style_table_header)
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell_bold),
            Paragraph("US$ 229,28", style_table_cell_center),
            Paragraph("US$ 255,00", style_table_cell_center),
            Paragraph("+11,2%", style_table_cell_center),
            Paragraph("<b>US$ 115,00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-49,8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>TSMC (TSM)</b>", style_table_cell_bold),
            Paragraph("US$ 190,50", style_table_cell_center),
            Paragraph("US$ 218,00", style_table_cell_center),
            Paragraph("+14,4%", style_table_cell_center),
            Paragraph("<b>US$ 110,00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-42,3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_cell_bold),
            Paragraph("US$ 184,80", style_table_cell_center),
            Paragraph("US$ 210,00", style_table_cell_center),
            Paragraph("+13,6%", style_table_cell_center),
            Paragraph("<b>US$ 115,00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-37,8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Oracle (ORCL)</b>", style_table_cell_bold),
            Paragraph("US$ 141,40", style_table_cell_center),
            Paragraph("US$ 148,00", style_table_cell_center),
            Paragraph("+4,7%", style_table_cell_center),
            Paragraph("<b>US$ 85,00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-39,9%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Meta Platforms (META)</b>", style_table_cell_bold),
            Paragraph("US$ 718,67", style_table_cell_center),
            Paragraph("US$ 780,00", style_table_cell_center),
            Paragraph("+8,5%", style_table_cell_center),
            Paragraph("<b>US$ 510,00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-29,0%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell_bold),
            Paragraph("US$ 262,43", style_table_cell_center),
            Paragraph("US$ 295,00", style_table_cell_center),
            Paragraph("+12,4%", style_table_cell_center),
            Paragraph("<b>US$ 195,00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-25,7%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell_bold),
            Paragraph("US$ 535,07", style_table_cell_center),
            Paragraph("US$ 575,00", style_table_cell_center),
            Paragraph("+7,5%", style_table_cell_center),
            Paragraph("<b>US$ 405,00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-24,3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell_bold),
            Paragraph("US$ 351,66", style_table_cell_center),
            Paragraph("US$ 385,00", style_table_cell_center),
            Paragraph("+9,5%", style_table_cell_center),
            Paragraph("<b>US$ 275,00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-21,8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Nasdaq 100 (^NDX)</b>", style_table_cell_bold),
            Paragraph("27.366 pts", style_table_cell_center),
            Paragraph("29.500 pts", style_table_cell_center),
            Paragraph("+7,8%", style_table_cell_center),
            Paragraph("<b>17.700 pts</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-35,3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>S&P 500 (^GSPC)</b>", style_table_cell_bold),
            Paragraph("7.811 pts", style_table_cell_center),
            Paragraph("8.200 pts", style_table_cell_center),
            Paragraph("+5,0%", style_table_cell_center),
            Paragraph("<b>5.600 pts</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-28,3%</b></font>", style_table_cell_center)
        ]
    ]
    t_target = Table(stock_target_data, colWidths=[120, 75, 75, 68, 96, 70])
    t_target.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_target)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Destaques de Assimetria:</b><br/>"
                           "• <b>Vulnerabilidade Aguda de Hardware:</b> Nvidia (-49,8%) e TSMC (-42,3%) sofrem o maior impacto relativo, pois qualquer adiamento na conexão de data centers comprime imediatamente novas ordens de chips.<br/>"
                           "• <b>Resiliência Relativa de Alphabet (-21,8%) e Microsoft (-24,3%):</b> Balanços massivos em caixa líquido e fluxos de caixa legados protegem os hyperscalers soberanos contra insolvência direta.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PÁGINA 8: DIRETRIZES DE GESTÃO DE RISCO E DISCLAIMER
    # =========================================================
    story.append(Paragraph("Diretrizes de Gestão de Risco Institucional e Conclusões Finais", style_h1))
    story.append(Paragraph("As evidências consolidadas em outubro de 2026 exigem uma revisão abrangente nas estratégias de alocação de ativos e subscrição de dívida estruturada:", style_body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Auditoria Física Obrigatória de Interconexão Elétrica (Grid Audit):</b>", style_body_bold))
    story.append(Paragraph("Investidores em dívida de infraestrutura não devem aceitar promessas ou cartas de intenção não vinculantes de concessionárias de energia. Somente contratos com subestações energizadas e transformadores já entregues possuem viabilidade de fluxo de caixa garantido.", style_body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2. Sobredotação de Colateral em Data Center ABS:</b>", style_body_bold))
    story.append(Paragraph("As agências de rating (KBRA, S&P, Moody's) precisam recalcular seus modelos KNCF assumindo que Neoclouds (como Nscale, CoreWeave e Lambda) apresentam risco de calote correlacionado. Tranches subordinadas Classe B e Equity devem absorver colchões de proteção de no mínimo 25% a 30% do saldo total da dívida.", style_body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3. Rotação Tática em Carteiras Acionárias:</b>", style_body_bold))
    story.append(Paragraph("Reduzir exposição em fornecedores de hardware puro negociados a múltiplos esticados (>35x P/E) e aumentar a ponderação em hyperscalers diversificados com acesso direto a energia proprietária (Google com TPUs, Amazon com AWS Trainium e contratos de energia nuclear).", style_body))
    story.append(Spacer(1, 10))

    box_disc = [
        [
            Paragraph("<b>DISCLAIMER INSTITUCIONAL / AVISO LEGAL:</b> Este documento foi preparado exclusivamente para fins analíticos, educacionais e de pesquisa forense de mercado financeiro. As estimativas, preços-alvo, distribuições probabilísticas e cenários de estresse constituem simulações econométricas de cauda e não configuram recomendação de investimento, aconselhamento financeiro, oferta ou solicitação de compra e venda de quaisquer títulos mobiliários. O desempenho histórico de ativos não garante rentabilidade futura.", ParagraphStyle('DiscTxt', fontName='Helvetica-Oblique', fontSize=6.8, leading=9.5, textColor=colors.HexColor('#64748B')))
        ]
    ]
    t_disc = Table(box_disc, colWidths=[504])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_disc)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated Portuguese Report: {out_path}")

def main():
    build_pdf_report()

if __name__ == '__main__':
    main()
