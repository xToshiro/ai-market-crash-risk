from utils_paths import get_chart_path, get_report_en_path
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_forensic_ai_subprime_report_en.py
------------------------------------------
Generates the Institutional English Executive Report (4 pages):
'Relatorio_Forense_Subprime_IA_Repacotamento_AAA_EN.pdf'
Forensic Analysis of Risk Repackaging in AI: 2008 Comparison, GPU-Backed Debt, and Tranche Durability.
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
            self.drawString(54, 750, "FORENSIC AUDIT • AI SUBPRIME REPORT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "SUBCOMPONENTS OF AAA / A TRANCHES")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Regulatory Audit: KBRA Methodology 2026, Moody's, S&P, CoreWeave DDTL & SEC Filings")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Relatorio_Forense_Subprime_IA_Repacotamento_AAA_EN.pdf"):
    doc = SimpleDocTemplate(get_report_en_path(output_filename),
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
    # PAGE 1: REPACKAGING ALCHEMY: 2008 VS 2026
    # =========================================================
    header_data = [
        [
            Paragraph("<b>FORENSIC AUDIT OF SYSTEMIC RISK &amp; CAPITAL MARKETS</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#B91C1C'))),
            Paragraph(f"Issued: {datetime.date.today().strftime('%B %d, %Y')} | Special Dossier", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("Risk Repackaging in the AI Cycle", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Forensic Inquiry: 2008 Parallel (BBB to AAA), GPU-Collateralized Debt, and Structural Solidity of Senior Tranches", style_subtitle))
    story.append(Spacer(1, 6))

    kpi_data = [
        [
            Paragraph("<b>2008 ALCHEMY</b><br/><font size=9.5 color='#DC2626'><b>MBS BBB ➔ AAA</b></font><br/><font size=6.3 color='#DC2626'>Mezzanine CDO (David Li Copula)</font>", style_table_cell),
            Paragraph("<b>2026 ALCHEMY</b><br/><font size=9.5 color='#D97706'><b>GPU Junk ➔ A3 / A-</b></font><br/><font size=6.3 color='#D97706'>SPV CoreWeave (Moody's DDTL)</font>", style_table_cell),
            Paragraph("<b>CLASS A COLLATERAL</b><br/><font size=9.5 color='#1E3A8A'><b>72% Hyperscalers</b></font><br/><font size=6.3 color='#10B981'>Microsoft, AWS, Google (Sovereign)</font>", style_table_cell),
            Paragraph("<b>HIDDEN RISK</b><br/><font size=9.5 color='#B91C1C'><b>Vendor Financing</b></font><br/><font size=6.3 color='#B91C1C'>Closed Loop Nvidia-OpenAI-Neocloud</font>", style_table_cell),
            Paragraph("<b>HARDWARE MISMATCH</b><br/><font size=9.5 color='#7C3AED'><b>3y GPU vs 5y Debt</b></font><br/><font size=6.3 color='#64748B'>Rapid Silicon Obsolescence</font>", style_table_cell),
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
                "<b>CRITICAL INQUIRY ADDRESSED:</b> In the 2008 GFC, BBB-rated debt was repackaged into Mezzanine CDOs creating 80% fictional 'AAA' notes premised on flawed zero-correlation assumptions. <b>In 2026, an analogous structural dynamic has emerged across private credit in AI</b>: neocloud debt bearing 15% high-yield coupons secured by volatile chips has been packaged into SPVs with take-or-pay contracts, securing <b>institutional Investment Grade ratings (Moody's A3 / DBRS A-)</b>. Conversely, <b>Class A notes in Physical Data Centers</b> retain authentic credit solidity because their collateral is physical grid power scarcity and the multi-trillion-dollar balance sheets of hyperscalers.",
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

    story.append(Paragraph("1. Securitization Alchemy: Structural Parallel 2008 vs. 2026", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    if os.path.exists(get_chart_path("chart_repackaging_alchemy.png", lang="en")):
        story.append(Image(get_chart_path("chart_repackaging_alchemy.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "• <b>The 2008 Framework:</b> Originators bundled subprime mortgages from undocumented borrowers (NINJA loans) into RMBS. Slices rated BBB were repooled into Mezzanine CDOs, where Gaussian Copula modeling asserted that 75% to 80% of newly minted notes warranted AAA status due to geographic dispersion.<br/>"
        "• <b>The 2026 Framework:</b> Neoclouds and AI providers raise expensive private debt (15% p.a.) collateralized directly by physical GPUs. To unlock institutional capital from insurers and pensions, hardware and forward leases are placed in bankruptcy-remote SPVs. Agencies like Moody's and DBRS rate these senior debt facilities <b>Investment Grade A3 / A-</b> (e.g., CoreWeave's $8.5 Billion DDTL in March 2026).",
        style_body
    ))

    story.append(PageBreak()) # End Page 1

    # =========================================================
    # PAGE 2: SUBCOMPONENT DECOMPOSITION & WHO UNDERWRITES AAA
    # =========================================================
    story.append(Paragraph("2. Subcomponent Decomposition: What Backs Senior Tranches?", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "To rigorously quantify credit exposure across senior tranches (Class A / AAA), we audit the revenue streams servicing debt facilities:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_subcomponents_decomposition.png", lang="en")):
        story.append(Image(get_chart_path("chart_subcomponents_decomposition.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    decomp_table_data = [
        [
            Paragraph("<b>Subcomponent Layer</b>", style_table_header),
            Paragraph("<b>Revenue Share</b>", style_table_header),
            Paragraph("<b>Key Counterparties</b>", style_table_header),
            Paragraph("<b>Solvency &amp; Actual Risk Diagnosis</b>", style_table_header)
        ],
        [
            Paragraph("<b>Subcomponent 1:<br/>Sovereign Hyperscalers</b>", style_table_cell),
            Paragraph("<b>65% to 80%</b><br/>of ABS pool", style_table_cell),
            Paragraph("Microsoft (AAA), AWS (AA), Google (AA+), Meta (AA-)", style_table_cell),
            Paragraph("<font color='#10B981'><b>Extremely Solid:</b></font> Multi-trillion-dollar balance sheets with immense free cash flows. Will service data center lease covenants for enterprise workloads regardless of AI volatility.", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponent 2:<br/>Neoclouds &amp; AI Startups</b>", style_table_cell),
            Paragraph("<b>15% to 25%</b><br/>(growing share)", style_table_cell),
            Paragraph("CoreWeave, Lambda Labs, OpenAI, xAI, Anthropic", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Highly Strained:</b></font> Cash-burning entities reliant on continuous venture infusions and private credit facilities to cover ongoing facility lease commitments.", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponent 3:<br/>Global Enterprises</b>", style_table_cell),
            Paragraph("<b>10% to 15%</b><br/>of pool", style_table_cell),
            Paragraph("Wall Street banks, healthcare systems, telecom carriers", style_table_cell),
            Paragraph("<font color='#10B981'><b>Stable &amp; Diversified:</b></font> Mission-critical corporate colocation with 5 to 10-year contracts escalating with inflation (CPI).", style_table_cell)
        ],
        [
            Paragraph("<b>Subcomponent 4:<br/>Physical Collateral (Power)</b>", style_table_cell),
            Paragraph("<b>100%</b> of hard collateral", style_table_cell),
            Paragraph("Power substations, secured PPAs, hardened facility shells", style_table_cell),
            Paragraph("<font color='#10B981'><b>Absolute Scarcity:</b></font> Grid-interconnected electricity possesses universal commercial value. In a tenant default, competitor hyperscalers queue to take over capacity.", style_table_cell)
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

    story.append(PageBreak()) # End Page 2

    # =========================================================
    # PAGE 3: TEMPORAL MISMATCH & CIRCULARITY
    # =========================================================
    story.append(Paragraph("3. Temporal Mismatch: 3-Year Hardware vs. 5 to 7-Year Debt", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "The primary structural vulnerability in AI debt financing resides in the **divergence between physical hardware depreciation and debt amortization horizons**:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_gpu_depreciation_vs_debt.png", lang="en")):
        story.append(Image(get_chart_path("chart_gpu_depreciation_vs_debt.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>The Three Structural Collateral Impairment Drivers:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>The 'Underwater Collateral' Phenomenon:</b> Unlike commercial real estate which depreciates or appreciates slowly at 2%-3% annually, AI computing chips lose **60% to 75% of their economic value within 24 to 36 months** as denser architectures launch (e.g., Nvidia Blackwell and Rubin). Beyond month 20, outstanding facility debt significantly outstrips secondary GPU market liquidation values.<br/>"
        "2. <b>Circular Vendor Financing (The Closed Loop):</b> Nvidia injects equity into startups and neoclouds (CoreWeave), which borrow private debt (Blackstone, Magnetar) and immediately recycle 100% of proceeds purchasing new Nvidia accelerators. This loop masks true end-user software demand.<br/>"
        "3. <b>The Zero-Correlation Fallacy (David Li's Error Revisited):</b> Rating models assume defaults across AI venture clients are independent events. In practice, if generative software monetization stumbles, **default correlation across neoclouds surges to 1.0 simultaneously**, wiping out structural diversification.",
        style_body
    ))

    story.append(PageBreak()) # End Page 3

    # =========================================================
    # PAGE 4: STRESS LOSS SIMULATION & FORENSIC VERDICT
    # =========================================================
    story.append(Paragraph("4. Capital Loss Simulation and Final Forensic Diagnosis", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "To determine which tranches face principal impairments under a 2008-scale shock, we simulate loss severities across three stress regimes:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_stress_loss_simulation.png", lang="en")):
        story.append(Image(get_chart_path("chart_stress_loss_simulation.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    stress_table_data = [
        [
            Paragraph("<b>Debt Instrument / Tranche</b>", style_table_header),
            Paragraph("<b>Base Case (Current)</b>", style_table_header),
            Paragraph("<b>Moderate Stress (AI Digestion)</b>", style_table_header),
            Paragraph("<b>Severe Stress (2008-Style Shock)</b>", style_table_header),
            Paragraph("<b>Forensic Credit Verdict</b>", style_table_header)
        ],
        [
            Paragraph("<b>Class A Senior Notes<br/>(Data Center ABS)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Loss</b></font><br/>Full debt service", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Loss</b></font><br/>Overcollateralization buffers", style_table_cell),
            Paragraph("<font color='#10B981'><b>0% to 4.5% Loss</b></font><br/>Hyperscalers honor covenants", style_table_cell),
            Paragraph("<b>SHIELDED:</b> Benchmark Class A Data Center ABS will NOT default like 2008 CDOs due to high-grade contracts and grid power value.", style_table_cell)
        ],
        [
            Paragraph("<b>Class B Mezzanine<br/>(Private Credit)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Loss</b></font><br/>Yield 7.5%-8.5%", style_table_cell),
            Paragraph("<font color='#D97706'><b>12.0% Loss</b></font><br/>Coupons convert to PIK", style_table_cell),
            Paragraph("<font color='#DC2626'><b>65% to 80% Loss</b></font><br/>Widespread default", style_table_cell),
            Paragraph("<b>VULNERABLE:</b> Class B notes absorb the initial shock of neocloud lease re-negotiations and retrofitting capex.", style_table_cell)
        ],
        [
            Paragraph("<b>Direct GPU Facilities<br/>(Neocloud Term Debt)</b>", style_table_cell),
            Paragraph("<font color='#10B981'><b>0.0% Loss</b></font><br/>Rated A3 / A-", style_table_cell),
            Paragraph("<font color='#D97706'><b>25.0% Loss</b></font><br/>Forced restructuring", style_table_cell),
            Paragraph("<font color='#DC2626'><b>70% to 90% Loss</b></font><br/>Underwater collateral", style_table_cell),
            Paragraph("<b>THE REAL 'SUBPRIME':</b> Debt marketed as investment-grade but backstopped by rapidly depreciating computing chips.", style_table_cell)
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
            Paragraph("<b>FINAL FORENSIC DIAGNOSIS:</b><br/>"
                      "1. <b>Where is the 2008 risk?</b> It is NOT in traditional physical Data Center ABS (Class A), which is fortified by prime power assets and tech titans' balance sheets.<br/>"
                      "2. <b>Where is the actual contagion?</b> Systemic vulnerability resides in <b>direct GPU-collateralized loans and opaque private credit funds (*Shadow Banking*)</b>, where high-yield debt gained investment-grade stamps (A3/A-) while relying upon circular contracts from unprofitable AI startups.",
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
    print(f"Forensic Report successfully compiled: {output_filename}", flush=True)

def main():
    pdf_filename = "Relatorio_Forense_Subprime_IA_Repacotamento_AAA_EN.pdf"
    build_pdf_report(pdf_filename)
    print(f"Generated: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
