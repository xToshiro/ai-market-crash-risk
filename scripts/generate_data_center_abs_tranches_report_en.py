from utils_paths import get_chart_path, get_report_en_path
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_data_center_abs_tranches_report_en.py
---------------------------------------------
Generates the Institutional English Executive Report (4 pages):
'Report_Data_Center_ABS_Official_Tranches.pdf'
Analyzing Data Center ABS Capital Structures: Class A, Class B, and Equity Tranches.
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
            self.drawString(54, 750, "TECHNICAL REPORT • DATA CENTER ABS")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "TRANCHE STRUCTURE: CLASS A, CLASS B & EQUITY")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Primary Sources: KBRA Rating Methodology, S&P Global, SEC 10-K/D Filings, TierPoint, DataBank, Centersquare")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Report_Data_Center_ABS_Official_Tranches.pdf"):
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
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )

    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#475569')
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4,
        spaceBefore=6
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # =========================================================
    # PAGE 1: INTRODUCTION, ANATOMY OF TRANCHES & CAPITAL STACK
    # =========================================================
    header_data = [
        [
            Paragraph("<b>OFFICIAL TECHNICAL REPORT • CAPITAL MARKETS & SECURITIZATION</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#2563EB'))),
            Paragraph(f"Date: {datetime.date.today().strftime('%B %d, %Y')} | Source: KBRA / S&P / SEC", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("Data Center ABS Tranche Structure Analysis", style_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Official Capital Stack Examination: Class A, Class B, and Equity Tranches in AI Digital Infrastructure Financing", style_subtitle))
    story.append(Spacer(1, 6))

    kpi_data = [
        [
            Paragraph("<b>TOTAL ISSUANCE VOLUME</b><br/><font size=10 color='#1E3A8A'><b>$20.9 Billion</b></font><br/><font size=6.5 color='#10B981'>All-Time High (AI Capex)</font>", style_table_cell),
            Paragraph("<b>CLASS A TRANCHE</b><br/><font size=10 color='#0D9488'><b>A- to AAA (sf)</b></font><br/><font size=6.5 color='#10B981'>75% to 95% of Debt Stack</font>", style_table_cell),
            Paragraph("<b>CLASS B TRANCHE</b><br/><font size=10 color='#D97706'><b>BBB- to BBB</b></font><br/><font size=6.5 color='#D97706'>3% to 12% Subordinated Mezz</font>", style_table_cell),
            Paragraph("<b>EQUITY TRANCHE</b><br/><font size=10 color='#7C3AED'><b>25% to 40% (Overcoll.)</b></font><br/><font size=6.5 color='#64748B'>First-Loss Retained by Sponsor</font>", style_table_cell),
            Paragraph("<b>HISTORICAL DEFAULTS</b><br/><font size=10 color='#10B981'><b>0.00% (Class A)</b></font><br/><font size=6.5 color='#10B981'>Zero defaults since 2018</font>", style_table_cell),
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[100, 102, 102, 100, 100])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 6))

    exec_box = [
        [
            Paragraph(
                "<b>REGULATORY OVERVIEW (KBRA &amp; S&amp;P):</b> In a Data Center ABS issuance structured under a <i>Master Trust</i>, tranche division establishes the <b>strict priority of cash disbursements (*Cash Flow Waterfall*)</b> and <b>sequential loss absorption</b>. Class A is engineered to achieve senior Investment Grade ratings, heavily protected by the structural credit enhancement provided by subordinated Class B notes and equity capital retained by the sponsor (Overcollateralization).",
                style_callout
            )
        ]
    ]
    t_exec = Table(exec_box, colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Detailed Anatomy of the Capital Stack Tranches", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    if os.path.exists(get_chart_path("chart_tranche_structure.png", lang="en")):
        story.append(Image(get_chart_path("chart_tranche_structure.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    tranche_table_data = [
        [
            Paragraph("<b>Tranche / Class</b>", style_table_header),
            Paragraph("<b>Typical Rating</b>", style_table_header),
            Paragraph("<b>Debt Share</b>", style_table_header),
            Paragraph("<b>Investor Profile</b>", style_table_header),
            Paragraph("<b>Credit Enhancement &amp; Risk Mechanics</b>", style_table_header)
        ],
        [
            Paragraph("<b>Class A-1 (VFN)<br/>Class A-2 (Term)</b>", style_table_cell),
            Paragraph("<b>A- to AAA (sf)</b><br/>(KBRA / S&amp;P)", style_table_cell),
            Paragraph("<b>75% to 95%</b><br/>of debt stack", style_table_cell),
            Paragraph("Life insurers, pension funds, bank treasuries", style_table_cell),
            Paragraph("Senior-most priority on principal and coupon receipts. Protected by Debt Service Reserve Accounts (DSRA) and full subordination of B and Equity.", style_table_cell)
        ],
        [
            Paragraph("<b>Class B<br/>(Mezzanine)</b>", style_table_cell),
            Paragraph("<b>BBB- to BBB</b><br/>(KBRA)", style_table_cell),
            Paragraph("<b>3% to 12%</b><br/>of debt stack", style_table_cell),
            Paragraph("Private credit funds, absolute return managers", style_table_cell),
            Paragraph("Subordinated to Class A. Absorbs second losses. Under severe stress, coupons may convert to Payment-in-Kind (PIK), capitalizing into principal.", style_table_cell)
        ],
        [
            Paragraph("<b>Equity Tranche<br/>(Sponsor)</b>", style_table_cell),
            Paragraph("<b>Unrated</b><br/>(Residual)", style_table_cell),
            Paragraph("<b>25% to 40%</b><br/>of asset value (LTV 60-75%)", style_table_cell),
            Paragraph("Data Center Operator (Vantage, DataBank, STACK)", style_table_cell),
            Paragraph("Absorbs <b>first loss (100%)</b>. Receives purely residual cash flow. Subject to <i>Cash Trap</i> (100% dividend freeze if DSCR drops below ~1.30x).", style_table_cell)
        ]
    ]

    t_tranches = Table(tranche_table_data, colWidths=[90, 75, 75, 114, 150])
    t_tranches.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tranches)

    story.append(PageBreak()) # End Page 1

    # =========================================================
    # PAGE 2: EMPIRICAL BENCHMARKS & OFFICIAL ISSUANCES
    # =========================================================
    story.append(Paragraph("2. Empirical Evidence and Official Rating Agency Deal Track", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "A review of <b>KBRA</b> and <b>S&amp;P</b> New Issue Reports and public SEC offering circulars reveals real-world debt structuring parameters across benchmark issuers:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_deals_comparison.png", lang="en")):
        story.append(Image(get_chart_path("chart_deals_comparison.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    deals_table_data = [
        [
            Paragraph("<b>Issuer &amp; Official Series</b>", style_table_header),
            Paragraph("<b>Tranche / Class</b>", style_table_header),
            Paragraph("<b>Issuance Amount</b>", style_table_header),
            Paragraph("<b>Official Rating</b>", style_table_header),
            Paragraph("<b>Tenor (ARD)</b>", style_table_header),
            Paragraph("<b>Underlying Collateral Pool</b>", style_table_header)
        ],
        [
            Paragraph("<b>TierPoint Issuer LLC</b><br/>(Series 2025-1 • Apr 2025)", style_table_cell),
            Paragraph("Class A (4Y / 7Y)<br/>Class B (4Y Mezz)", style_table_cell),
            Paragraph("$485.0M<br/>$15.0M", style_table_cell),
            Paragraph("<b>A-</b> (KBRA)<br/><b>BBB-</b> (KBRA)", style_table_cell),
            Paragraph("4 &amp; 7 years<br/>4 years", style_table_cell),
            Paragraph("33 enterprise colocation data centers across US. $1.81B cumulative platform debt.", style_table_cell)
        ],
        [
            Paragraph("<b>DataBank Issuer LLC</b><br/>(Series 2021-1 / 2024-1)", style_table_cell),
            Paragraph("Class A-2 (Term)<br/>Class B / Class C", style_table_cell),
            Paragraph("$658.0M<br/>$99.0M", style_table_cell),
            Paragraph("<b>A-</b> (KBRA)<br/><b>BBB / BB</b> (KBRA)", style_table_cell),
            Paragraph("5 years<br/>5 years", style_table_cell),
            Paragraph("Portfolio of 35 colocation campuses. Subordinated B/C notes amortized in 2026.", style_table_cell)
        ],
        [
            Paragraph("<b>Centersquare Issuer LLC</b><br/>(Series 2024-1 / 2025-1)", style_table_cell),
            Paragraph("Class A-2<br/>Class B (Mezz)", style_table_cell),
            Paragraph("$400.0M<br/>$50.0M est.", style_table_cell),
            Paragraph("<b>A-</b> (KBRA)<br/><b>BBB-</b> (KBRA)", style_table_cell),
            Paragraph("5 years<br/>5 years", style_table_cell),
            Paragraph("21 multi-tenant campuses; secured against annualized monthly recurring revenue.", style_table_cell)
        ],
        [
            Paragraph("<b>STACK Infrastructure</b><br/>(Series 2024-1 / 2025-1)", style_table_cell),
            Paragraph("Class A-2 Senior<br/>Retained Equity", style_table_cell),
            Paragraph("$1.2+ Billion<br/>~$500M (OC)", style_table_cell),
            Paragraph("<b>A- (sf)</b> (S&amp;P)<br/>Unrated", style_table_cell),
            Paragraph("5 &amp; 10 years<br/>Residual", style_table_cell),
            Paragraph("Hyperscale wholesale campuses dedicated to Microsoft, AWS, and Oracle.", style_table_cell)
        ]
    ]

    t_deals = Table(deals_table_data, colWidths=[105, 80, 68, 65, 62, 124])
    t_deals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_deals)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Key Findings from Official Deal Data:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>Overwhelming Dominance of Class A:</b> Across benchmark issuances, Class A notes represent <b>85% to 97% of total debt placed</b>. Issuers actively maximize senior notes to secure the lowest weighted average cost of capital (A- / A+ ratings).<br/>"
        "2. <b>Tactical Deployment of Class B:</b> Mezzanine tranches remain lean (3% to 12% of the facility). They are primarily subscribed by private credit managers seeking enhanced yield (~7.5% to 8.5%) in exchange for absorbing transient cash flow volatility.<br/>"
        "3. <b>Substantial Overcollateralization:</b> In virtually all KBRA-rated trusts, asset LTVs range between 55% and 70%, ensuring a robust structural equity cushion of <b>30% to 45% retained by the sponsor</b>.",
        style_body
    ))

    story.append(PageBreak()) # End Page 2

    # =========================================================
    # PAGE 3: WATERFALL MECHANICS, SPREADS & COVENANTS
    # =========================================================
    story.append(Paragraph("3. Payment Waterfall Mechanics and Spread Pricing", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "Coupon pricing directly mirrors structural seniority within the legal trust indenture (*Cash Flow Waterfall*):",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_spreads_yields.png", lang="en")):
        story.append(Image(get_chart_path("chart_spreads_yields.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Strict Priority of Monthly Cash Flow Disbursements:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Tier 1 (Mission-Critical Costs):</b> Facility Operations &amp; Maintenance expenses (utility power, on-site security) and trust servicing fees (*Master &amp; Backup Servicer*).<br/>"
        "• <b>Tier 2 (Senior Debt Service):</b> Scheduled interest and principal amortization on <b>Class A-1 and Class A-2</b> notes.<br/>"
        "• <b>Tier 3 (Mezzanine Debt Service):</b> Scheduled interest on <b>Class B</b> notes (subject to deferral/PIK if liquidity hurdles are breached).<br/>"
        "• <b>Tier 4 (Reserve Replenishment):</b> Funding of the Debt Service Reserve Account (DSRA, typically 6 months of debt service) and replacement capex escrows.<br/>"
        "• <b>Tier 5 (Residual Equity Distribution):</b> Unencumbered residual cash is distributed to sponsor equity holders (Vantage, DataBank, STACK).",
        style_body
    ))

    covenant_table = [
        [
            Paragraph("<b>Contractual Trigger Event</b>", style_table_header),
            Paragraph("<b>Typical DSCR Hurdle</b>", style_table_header),
            Paragraph("<b>Waterfall Enforcement Action</b>", style_table_header),
            Paragraph("<b>Impact on Equity and Class B Tranches</b>", style_table_header)
        ],
        [
            Paragraph("<b>Standard Operation</b>", style_table_cell),
            Paragraph("DSCR &gt; 1.60x", style_table_cell),
            Paragraph("Unrestricted dividend distribution to sponsor.", style_table_cell),
            Paragraph("<font color='#10B981'><b>Full distributions:</b></font> Sponsor realizes 14% to 18% ROE.", style_table_cell)
        ],
        [
            Paragraph("<b>Cash Trap Event<br/>(Preventative Sweep)</b>", style_table_cell),
            Paragraph("DSCR &lt; 1.30x to 1.40x", style_table_cell),
            Paragraph("100% of residual cash flow trapped in trust custody account.", style_table_cell),
            Paragraph("<font color='#D97706'><b>Zero dividends:</b></font> Operator distributions frozen until coverage ratio restores.", style_table_cell)
        ],
        [
            Paragraph("<b>Rapid Amortization Event<br/>(Accelerated Paydown)</b>", style_table_cell),
            Paragraph("DSCR &lt; 1.15x to 1.20x", style_table_cell),
            Paragraph("Subordinated payments suspended; all net cash amortizes Class A principal.", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Senior Shield:</b></font> Class A paid down rapidly; equity value severely impaired.", style_table_cell)
        ]
    ]

    t_cov = Table(covenant_table, colWidths=[114, 85, 145, 160])
    t_cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cov)

    story.append(PageBreak()) # End Page 3

    # =========================================================
    # PAGE 4: CURRENT STATUS IN THE AI BOOM & VERDICT
    # =========================================================
    story.append(Paragraph("4. Current Market Assessment: The AI Capex Boom and Structural Stress Vectors", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5, spaceBefore=0))

    story.append(Paragraph(
        "In 2025/2026, the generative AI race catalyzed unprecedented issuance volume in Data Center ABS, altering risk profiles across each tranche:",
        style_body
    ))

    if os.path.exists(get_chart_path("chart_issuance_and_health.png", lang="en")):
        story.append(Image(get_chart_path("chart_issuance_and_health.png", lang="en"), width=6.8*inch, height=2.4*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>2026 Diagnosis Across Tranche Classes:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Class A Senior Notes (Extremely Resilient):</b> Credit risk remains virtually nil. Over <b>75% of underlying contracted revenues</b> are underwritten by investment-grade hyperscalers (Microsoft, Amazon/AWS, Alphabet/Google, Oracle). Even in an AI startup bankruptcy, 25% to 35% overcollateralization cushions senior noteholders from principal loss.<br/>"
        "• <b>Class B Mezzanine Notes (Surveillance Point):</b> Mezzanine debt issued to fund liquid-cooling retrofits has increased exposure to specialized neoclouds (CoreWeave, Lambda Labs). Investors demand wider spreads (+280 to +350 bps) to compensate for potential contract restructurings that could trigger PIK coupon deferrals.<br/>"
        "• <b>Retained Equity Tranche (Cost-of-Capital Squeeze):</b> With US benchmark yields anchored between 4.5% and 5.25%, elevated interest expense has compressed residual cash distributions to sponsors. Furthermore, transmission interconnection delays by electric utilities risk pushing facility DSCRs into <i>Cash Trap</i> territory.",
        style_body
    ))

    summary_box_data = [
        [
            Paragraph("<b>INSTITUTIONAL VERDICT ACROSS CAPITAL TRANCHES:</b><br/>"
                      "1. <b>For Conservative Fixed Income / Pension Allocators:</b> <b>Class A</b> Data Center ABS represents one of the most reliable securitization assets globally, offering attractive spreads (~5.8% to 6.2% yield) supported by a flawless track record of zero defaults and blue-chip counterparty risk.<br/>"
                      "2. <b>For Private Credit &amp; Mezzanine Managers:</b> <b>Class B</b> offers compelling yields (~7.5% to 8.5%), but mandates strict due diligence on facility power densities (kW/rack) and tenant solvency across AI venture workloads.",
                      style_table_cell)
        ]
    ]
    t_summary_box = Table(summary_box_data, colWidths=[504])
    t_summary_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_summary_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled: {output_filename}", flush=True)

def main():
    pdf_filename = "Report_Data_Center_ABS_Official_Tranches.pdf"
    build_pdf_report(pdf_filename)
    print(f"Generated: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
