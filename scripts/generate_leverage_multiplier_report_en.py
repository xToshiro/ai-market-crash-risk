#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_leverage_multiplier_report_en.py
-----------------------------------------
Generates the Institutional English Executive Report (4 pages):
'Relatorio_Alavancagem_e_Vendor_Financing_IA_EN.pdf'
Quantitative Audit of Leverage and Vendor Financing in the AI Cycle (2023–2026).
"""

import os
import sys
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

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
            self.drawString(54, 750, "QUANTITATIVE AUDIT • AI LEVERAGE REPORT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "THE LEVERAGE PYRAMID & VENDOR FINANCING")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Primary Data: Gartner GenAI Spend, IDC, Sequoia Capital Research, Goldman Sachs & SEC Filings")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Relatorio_Alavancagem_e_Vendor_Financing_IA_EN.pdf"):
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
    # PAGE 1: THE MULTIPLIER: HOW MANY DOLLARS PER REAL DOLLAR?
    # =========================================================
    header_data = [
        [
            Paragraph("<b>QUANTITATIVE FORENSIC REPORT • LEVERAGE &amp; CREDIT STRUCTURES</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#D97706'))),
            Paragraph(f"Issued: {datetime.date.today().strftime('%B %d, %Y')} | Source: Gartner / IDC / SEC", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("The Leverage Pyramid in the AI Ecosystem", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Three-Year Quantitative Audit (2023–2026): The Vendor Financing Loop and Multiplier of Capital Wagered per Real Dollar", style_subtitle))
    story.append(Spacer(1, 6))

    kpi_data = [
        [
            Paragraph("<b>REAL SOFTWARE BASE</b><br/><font size=9.5 color='#10B981'><b>$19.2 Billion</b></font><br/><font size=6.3 color='#10B981'>2024 GenAI Revenue (Gartner)</font>", style_table_cell),
            Paragraph("<b>INFRASTRUCTURE SPEND</b><br/><font size=9.5 color='#0284C7'><b>$365 Billion</b></font><br/><font size=6.3 color='#0284C7'>2024 Total GenAI Spend (Gartner)</font>", style_table_cell),
            Paragraph("<b>CAPEX MULTIPLIER</b><br/><font size=9.5 color='#D97706'><b>19.0x per $1 Real</b></font><br/><font size=6.3 color='#D97706'>$19 infra spend per $1 software</font>", style_table_cell),
            Paragraph("<b>TOTAL EQUITY WAGER</b><br/><font size=9.5 color='#DC2626'><b>$11.5 Trillion</b></font><br/><font size=6.3 color='#DC2626'>Tech Market Cap Added</font>", style_table_cell),
            Paragraph("<b>WALL ST. MULTIPLIER</b><br/><font size=9.5 color='#7C3AED'><b>~600x per $1 Real</b></font><br/><font size=6.3 color='#7C3AED'>$600 market cap per $1 software</font>", style_table_cell),
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
                "<b>DIRECT QUANTITATIVE ANSWER:</b> For every <b>$1.00 of REAL software revenue generated by commercial end-users</b> (enterprise seats across ChatGPT, Copilot, and inference APIs), the tech complex is deploying <b>$19.00 into silicon, server chassis, and data center facilities</b> (official Gartner data). Across public equity markets, cumulative market value added by mega-cap technology and chipmakers exceeds <b>$11.5 Trillion</b>, indicating that <b>over $600.00 of equity valuation expectations are wagered on EACH $1.00 of actual software cash flow</b>. In private credit, specialized neoclouds operate at <b>12x to 15x debt-to-equity leverage ratios</b>.",
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

    story.append(Paragraph("1. The Inverted Pyramid of AI Financial Leverage", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    if os.path.exists("chart_leverage_pyramid.png"):
        story.append(Image("chart_leverage_pyramid.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "The financial ecosystem behaves like an inverted funnel resting upon an extraordinarily narrow base of organic cash flow:<br/>"
        "• <b>Economic Base (1x):</b> Real enterprise and consumer software receipts ($19.2B in 2024 / $37.2B projected in 2025).<br/>"
        "• <b>Physical Capital Multiplier (19x):</b> Aggregate spending in GPUs, data centers, and power capacity ($365B in 2024).<br/>"
        "• <b>Private Debt Multiplier (42x):</b> Term loans collateralized by depreciating GPUs, structured ABS, and take-or-pay facilities.<br/>"
        "• <b>Public Equity Multiplier (310x to 600x):</b> Massive valuation multiple expansion across US equity markets.",
        style_body
    ))

    story.append(PageBreak()) # End Page 1

    # =========================================================
    # PAGE 2: THE 3-YEAR VENDOR FINANCING LOOP (2023-2026)
    # =========================================================
    story.append(Paragraph("2. Mechanics of the Vendor Financing Loop: The CoreWeave &amp; Nvidia Case", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "An investigation into cash and debt transactions between 2023 and 2026 reveals a closed, self-referential capital loop:",
        style_body
    ))

    if os.path.exists("chart_vendor_financing_loop.png"):
        story.append(Image("chart_vendor_financing_loop.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    loop_table_data = [
        [
            Paragraph("<b>Financing Loop Stage</b>", style_table_header),
            Paragraph("<b>Core Participants</b>", style_table_header),
            Paragraph("<b>Capital Volume</b>", style_table_header),
            Paragraph("<b>Accounting Mechanism &amp; Market Impact</b>", style_table_header)
        ],
        [
            Paragraph("<b>1. Equity Anchor<br/>(Validation Check)</b>", style_table_cell),
            Paragraph("Nvidia (NVentures)", style_table_cell),
            Paragraph("~$100M to $200M", style_table_cell),
            Paragraph("Nvidia acquires minority equity stakes in specialized neoclouds, granting 'preferred cloud partner' status and chip allocations.", style_table_cell)
        ],
        [
            Paragraph("<b>2. Debt Financing<br/>(Shadow Banking)</b>", style_table_cell),
            Paragraph("Blackstone, Magnetar, Carlyle, Coatue", style_table_cell),
            Paragraph("<b>$19.0+ Billion</b><br/>(Cumulative 2023-2026)", style_table_cell),
            Paragraph("Private credit syndicates structure multi-billion term facilities collateralized by GPUs and customer backlog; leverage hits 12x-15x.", style_table_cell)
        ],
        [
            Paragraph("<b>3. Hardware Purchase<br/>(Compulsory Outflow)</b>", style_table_cell),
            Paragraph("Neocloud ➔ Nvidia", style_table_cell),
            Paragraph("<b>$15.5+ Billion</b><br/>(>80% of borrowings)", style_table_cell),
            Paragraph("Neocloud immediately wires 100% of loan proceeds to Nvidia to pay cash for new H100, B200, and InfiniBand purchase orders.", style_table_cell)
        ],
        [
            Paragraph("<b>4. Profit Conversion<br/>(Nvidia Income Statement)</b>", style_table_cell),
            Paragraph("Nvidia Balance Sheet", style_table_cell),
            Paragraph("<b>$11.6 Billion</b><br/>(75% Gross Margin)", style_table_cell),
            Paragraph("Every $1.00 of private credit borrowed by the neocloud converts into 75 cents of direct gross profit on Nvidia's corporate balance sheet.", style_table_cell)
        ],
        [
            Paragraph("<b>5. Multiple Expansion<br/>(Market Capitalization)</b>", style_table_cell),
            Paragraph("Public Equity Markets", style_table_cell),
            Paragraph("<b>+$400+ Billion</b><br/>(35x P/E Multiple)", style_table_cell),
            Paragraph("Record quarterly earnings inflate tech market caps, drawing billions in passive index funds and ETF flows into the loop.", style_table_cell)
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

    story.append(PageBreak()) # End Page 2

    # =========================================================
    # PAGE 3: THE 3-YEAR TRAJECTORY & THE REVENUE GAP
    # =========================================================
    story.append(Paragraph("3. The 3-Year Trajectory (2023–2026): The Widening Revenue Chasm", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "The divergence between physical capex deployment and realized software monetization has accelerated over the past 36 months:",
        style_body
    ))

    if os.path.exists("chart_spending_vs_software_revenue.png"):
        story.append(Image("chart_spending_vs_software_revenue.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Annual Trajectory Analysis:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>2023 (The Genesis of Disparity):</b> Infrastructure expenditures reached $150B against $5.5B in real software revenues. David Cahn (Sequoia Capital) published <i>'AI's $200B Question'</i>, highlighting that the ecosystem required $200B in annual revenue to justify hardware capex.<br/>"
        "• <b>2024 (The 19x Acceleration):</b> Total GenAI spend surged to <b>$365 Billion</b> (Gartner), while software revenues totaled <b>$19.16 Billion</b>. Sequoia updated its hurdle to <i>'AI's $600B Question'</i>, and Goldman Sachs' Jim Covello warned of a $1 Trillion capex buildout without validated commercial killer apps.<br/>"
        "• <b>2025/2026 (The Industrial Scale):</b> Gartner estimates project global GenAI spend reaching <b>$644 Billion</b>, driven by massive multi-gigawatt data center campuses, against software revenues of <b>$37.16 Billion</b>. The capex-to-software mismatch stabilizes at an extreme <b>17.3x to 19x</b>.",
        style_body
    ))

    story.append(PageBreak()) # End Page 3

    # =========================================================
    # PAGE 4: NEOCLOUD DEBT SNOWBALL & RISK VERDICT
    # =========================================================
    story.append(Paragraph("4. The Neocloud Debt Snowball and Final Institutional Verdict", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "Systemic leverage is concentrated among cloud operators whose balance sheets are backstopped entirely by AI computing silicon:",
        style_body
    ))

    if os.path.exists("chart_debt_snowball_neoclouds.png"):
        story.append(Image("chart_debt_snowball_neoclouds.png", width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    risk_table_data = [
        [
            Paragraph("<b>Leverage Metric Dimension</b>", style_table_header),
            Paragraph("<b>Current Level (2026)</b>", style_table_header),
            Paragraph("<b>Pre-AI Historical Standard</b>", style_table_header),
            Paragraph("<b>Forensic Institutional Verdict</b>", style_table_header)
        ],
        [
            Paragraph("<b>Debt-to-Equity Ratio</b>", style_table_cell),
            Paragraph("<b>12.0x to 15.0x</b>", style_table_cell),
            Paragraph("1.5x to 3.0x", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Critical:</b></font> Neoclouds rely upon continuous refinancings; minor revenue decelerations breach debt covenants.", style_table_cell)
        ],
        [
            Paragraph("<b>Capex-to-Software Multiplier</b>", style_table_cell),
            Paragraph("<b>17x to 19x</b>", style_table_cell),
            Paragraph("1.0x to 2.5x (SaaS)", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Imbalanced:</b></font> In mature cloud buildouts, each $1 of capex generated $0.80 to $1.20 in recurring revenue over 36 months.", style_table_cell)
        ],
        [
            Paragraph("<b>Equity Market Cap Multiplier</b>", style_table_cell),
            Paragraph("<b>~600x</b>", style_table_cell),
            Paragraph("20x to 40x", style_table_cell),
            Paragraph("<font color='#D97706'><b>Speculative:</b></font> Equity valuations assume generative AI will automate 100% of white-collar workflows over immediate horizons.", style_table_cell)
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
            Paragraph("<b>FINAL INSTITUTIONAL VERDICT:</b><br/>"
                      "1. <b>Physical Leverage Scale:</b> Capital markets are deploying <b>$19.00 in physical infrastructure for every $1.00 of software revenue</b> realized in the broader economy.<br/>"
                      "2. <b>Financial Leverage Scale:</b> Wall Street prices <b>$300 to $600 in market capitalization for every $1.00 of annualized software revenues</b>.<br/>"
                      "3. <b>The Mirage of Organic Demand:</b> The <i>Vendor Financing</i> model creates the accounting illusion that hardware revenue is self-sustaining, when in truth it is propelled by off-balance-sheet structured credit. If commercial software adoption fails to expand tenfold over the next 24 months, the pyramid will undergo an aggressive multiple de-rating.",
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
    print(f"Leverage Report successfully compiled: {output_filename}", flush=True)

def main():
    pdf_filename = "Relatorio_Alavancagem_e_Vendor_Financing_IA_EN.pdf"
    build_pdf_report(pdf_filename)
    print(f"Generated: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
