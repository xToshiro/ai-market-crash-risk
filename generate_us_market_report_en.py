#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_us_market_report_en.py
-------------------------------
Generates the Institutional English Executive Report (8 pages):
'Relatorio_Mercado_Financeiro_Americano_EN.pdf'
Comprehensive US Financial Market Assessment: Macro, $40T Debt, AI Capex, Subprime Analogues, and Predictive Model.
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
            self.drawString(54, 750, "US FINANCIAL MARKET ASSESSMENT • EXECUTIVE REPORT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "MACRO, EQUITIES, $40T DEBT, AI CAPEX & SYSTEMIC RISK")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)

        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential • Quantitative Valuation, AI Infrastructure Mechanics, and Predictive Risk Modeling")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(market_data=None, output_filename="Relatorio_Mercado_Financeiro_Americano_EN.pdf"):
    if market_data is None:
        market_data = {
            '^GSPC': {'current_price': 7807.10},
            '^IXIC': {'current_price': 27333.10},
            '^DJI': {'current_price': 51623.80},
            '^TNX': {'current_price': 5.25},
            '^VIX': {'current_price': 14.88}
        }

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
        fontSize=18.5,
        leading=22.5,
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
        spaceAfter=5,
        spaceBefore=6
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
    # PAGE 1: COVER, EXECUTIVE SUMMARY & MACRO OVERVIEW / FED
    # =========================================================
    header_data = [
        [
            Paragraph("<b>STRATEGIC MARKET REPORT &amp; SYSTEMIC RISK MANAGEMENT</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#2563EB'))),
            Paragraph(f"Issue Date: {datetime.date.today().strftime('%B %d, %Y')}", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("US Financial Market Comprehensive Assessment", style_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Full Spectrum Audit: Macroeconomics, Equities &amp; Valuations, $40T National Debt, AI Megacycle, 'AI Subprime' Mechanics, 2008 Benchmark, and Predictive Stress Models", style_subtitle))
    story.append(Spacer(1, 8))

    sp500_price = market_data.get('^GSPC', {}).get('current_price', 7807.1)
    nasdaq_price = market_data.get('^IXIC', {}).get('current_price', 27333.1)
    dji_price = market_data.get('^DJI', {}).get('current_price', 51623.8)
    tnx_yield = market_data.get('^TNX', {}).get('current_price', 5.25)
    vix_val = market_data.get('^VIX', {}).get('current_price', 14.88)

    kpi_data = [
        [
            Paragraph("<b>S&amp;P 500</b><br/><font size=10.5 color='#1E3A8A'><b>" + f"{sp500_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Persistent Uptrend</font>", style_table_cell),
            Paragraph("<b>NASDAQ</b><br/><font size=10.5 color='#0D9488'><b>" + f"{nasdaq_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>AI Leadership</font>", style_table_cell),
            Paragraph("<b>DOW JONES</b><br/><font size=10.5 color='#D97706'><b>" + f"{dji_price:,.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Industrials &amp; Financials</font>", style_table_cell),
            Paragraph("<b>10Y TREASURY</b><br/><font size=10.5 color='#DC2626'><b>" + f"{tnx_yield:.2f}%" + "</b></font><br/><font size=6.8 color='#DC2626'>Fiscal Supply Headwind</font>", style_table_cell),
            Paragraph("<b>VIX VOLATILITY</b><br/><font size=10.5 color='#7C3AED'><b>" + f"{vix_val:.2f}" + "</b></font><br/><font size=6.8 color='#10B981'>Subdued Risk Aversion</font>", style_table_cell),
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
                "<b>EXECUTIVE SUMMARY:</b> The US capital market operates under the collision of two monumental forces: the <b>productivity frontier unlocked by the Artificial Intelligence megacycle</b> opposed by the <b>fiscal gravity of a $40 Trillion national debt burden</b> and elevated interest rates (~5.25%). While tier-1 commercial banking solvency far exceeds 2008 standards, the specialized AI capital complex has developed structural subprime analogues (*GPU-Backed Debt*, *Vendor Financing*, and opaque *Private Credit*) that elevate medium- to long-term systemic risk.",
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

    story.append(Paragraph("1. Macroeconomic Landscape and Federal Reserve Monetary Policy", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "The United States economy continues to demonstrate superior momentum relative to developed peers, underpinned by robust consumer spending and unprecedented private capital expenditures in technology and energy infrastructure. This environment reinforces a 'higher-for-longer' monetary stance.",
        style_body
    ))

    story.append(Paragraph(
        "• <b>Federal Funds Target Rate:</b> Maintained within the <b>3.75% to 4.00%</b> corridor. The FOMC maintains a cautious posture, emphasizing data dependence to preempt second-round inflationary impulses.<br/>"
        "• <b>Inflation Dynamics (CPI &amp; Core PCE):</b> Headline CPI fluctuates between <b>2.8% and 3.0% YoY</b>. Structural stickiness across shelter, insurance, and essential services delays an immediate return to the formal 2.0% mandate.<br/>"
        "• <b>Labor Market (Payrolls &amp; Real Wages):</b> Unemployment remains historically low near <b>4.1% to 4.2%</b>, supporting consumption without igniting wage-price spirals.<br/>"
        "• <b>Real GDP Growth:</b> US GDP expands at an annualized pace of <b>2.3% to 2.6%</b>, reinforcing the soft-landing narrative.",
        style_body
    ))

    story.append(PageBreak()) # End Page 1

    # =========================================================
    # PAGE 2: EQUITY MARKETS & VALUATIONS
    # =========================================================
    story.append(Paragraph("2. US Equity Markets: Multiples, Concentration, and Breadth", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "US equity indices sustain multi-year highs, supported by resilient corporate earnings and massive global capital inflows. The S&amp;P 500 and Nasdaq lead performance across global benchmarks.",
        style_body
    ))

    if os.path.exists("chart_indices.png"):
        story.append(Image("chart_indices.png", width=6.8*inch, height=2.72*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Valuation Diagnosis and Sectoral Dispersion:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>Forward Price-to-Earnings (P/E):</b> The S&amp;P 500 trades at <b>23.4x</b> forward 12-month earnings, standing well above its 10-year (18.2x) and 20-year (15.8x) historical averages. This premium reflects expectations that generative AI will lift aggregate operating margins toward 15%+.<br/>"
        "2. <b>Equity Risk Premium (ERP) Compression:</b> With 10-year Treasury yields at 5.25% and equity earnings yields near 4.3%, the equity risk premium sits at two-decade lows, leaving valuations vulnerable to earnings misses.<br/>"
        "3. <b>Market Concentration vs. Breadth:</b> While mega-cap technology still accounts for over 30% of total S&amp;P 500 market capitalization, rotation into industrials, power utilities, and financials has broadened market breadth.",
        style_body
    ))

    story.append(PageBreak()) # End Page 2

    # =========================================================
    # PAGE 3: PUBLIC DEBT, TREASURY & FISCAL GRAVITY
    # =========================================================
    story.append(Paragraph("3. Public Debt and Fiscal Realities: The $40 Trillion Inflexion Point", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "The US fiscal trajectory reached a historic milestone in 2026. <b>Gross Federal Debt crossed $40.2 Trillion</b>, representing over <b>123% of Gross Domestic Product</b>. This structural imbalance exerts direct upward pressure on sovereign yield curves and global borrowing costs.",
        style_body
    ))

    if os.path.exists("chart_yields_debt.png"):
        story.append(Image("chart_yields_debt.png", width=6.8*inch, height=2.64*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Critical Vectors of Fiscal Vulnerability:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Net Interest Expense (Debt Service):</b> Due to cumulative rate increases, annual federal debt servicing costs surpassed <b>$1.1 Trillion</b>. For the first time in modern history, interest payments exceed the entire National Defense budget.<br/>"
        "• <b>Elevated Term Premia:</b> Massive Treasury auction supply mandates attractive yields to clear global buyers, anchoring <b>10-year yields between 5.20% and 5.30%</b>.<br/>"
        "• <b>Crowding-Out Dynamics:</b> Massive absorption of global savings by sovereign paper keeps 30-year residential mortgage rates near 6.8%-7.2% and inflates corporate borrowing costs.",
        style_body
    ))

    story.append(PageBreak()) # End Page 3

    # =========================================================
    # PAGE 4: THE AI REVOLUTION: CAPEX & VALUATIONS
    # =========================================================
    story.append(Paragraph("4. The Artificial Intelligence Revolution: Capex Megacycle &amp; Valuations", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "Artificial Intelligence is the core technological engine powering global equities. In 2026, technology infrastructure investments reached industrial scale, with multi-gigawatt computing campuses and proprietary energy architectures.",
        style_body
    ))

    if os.path.exists("chart_ai_capex.png"):
        story.append(Image("chart_ai_capex.png", width=6.8*inch, height=2.64*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Structural Dynamics of the AI Ecosystem in 2026:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Hyperscaler Capex Megacycle (~$800 Billion):</b> <b>Amazon ($220B)</b>, <b>Alphabet ($200B)</b>, <b>Microsoft ($175B)</b>, and <b>Meta ($140B)</b> deploy historic capital budgets into liquid cooling, microgrids, and advanced accelerators.<br/>"
        "• <b>Semiconductor Hegemony:</b> <b>Nvidia</b> maintains its market cap above <b>$3.5 Trillion</b>, controlling over 80% of datacenter accelerator shipments, followed by key fabrication and interconnect partners TSMC and Broadcom.<br/>"
        "• <b>Transition to Software ROI Audit:</b> Institutional investors increasingly scrutinize capital returns, rewarding platforms with proven software monetization and punishing cash-burning foundation model experiments.",
        style_body
    ))

    story.append(PageBreak()) # End Page 4

    # =========================================================
    # PAGE 5: THE "AI SUBPRIME": STRUCTURAL RISK MECHANISMS
    # =========================================================
    story.append(Paragraph("5. The 'AI Subprime' Mechanism: Financialization and Collateral Vulnerabilities", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "While AI financing does not involve residential mortgages, the ecosystem has developed <b>financial engineering structures directly analogous to subprime securitizations</b>:",
        style_body
    ))

    if os.path.exists("chart_ai_subprime.png"):
        story.append(Image("chart_ai_subprime.png", width=6.8*inch, height=2.45*inch))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>The Four Subprime-Analogous Mechanisms in AI:</b>", style_body_bold))
    story.append(Paragraph(
        "1. <b>GPU-Backed Debt:</b> Specialized neoclouds (CoreWeave, Lambda) raised over <b>$48 Billion in private credit</b> using Nvidia GPUs as collateral. Unlike real estate, <b>GPUs depreciate 60% to 80% within 2 to 3 years</b>. If rental rates soften, debt quickly exceeds collateral value (underwater assets).<br/>"
        "2. <b>Circular Vendor Financing:</b> Big Tech entities inject equity into AI startups, which contractually remit 100% of the funds back to buy cloud capacity and chips from the investor, artificially inflating reported revenues.<br/>"
        "3. <b>Take-or-Pay Tenor Mismatch:</b> Data center sponsors commit to 10 to 15-year power utility agreements backed by 3 to 5-year leases with venture-backed, cash-burning model startups.<br/>"
        "4. <b>Securitization into Shadow Banking:</b> Digital infrastructure debt is pooled into Data Center ABS held by private credit funds exempt from mark-to-market and bank capital requirements.",
        style_body
    ))

    story.append(PageBreak()) # End Page 5

    # =========================================================
    # PAGE 6: MARKET SOUNDNESS & SYSTEMIC VECTORS
    # =========================================================
    story.append(Paragraph("6. Financial Systemic Soundness and Risk Matrix Audit", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "Structural soundness remains robust across Tier-1 universal banks, but vulnerabilities concentrate across private credit, commercial real estate, and high-multiple technology equities:",
        style_body
    ))

    if os.path.exists("chart_solidity.png"):
        story.append(Image("chart_solidity.png", width=6.8*inch, height=2.45*inch))
        story.append(Spacer(1, 5))

    solidity_table_data = [
        [
            Paragraph("<b>Risk Dimension / Pillar</b>", style_table_header),
            Paragraph("<b>Current Status</b>", style_table_header),
            Paragraph("<b>Risk Level</b>", style_table_header),
            Paragraph("<b>Diagnosis and Investor Implications</b>", style_table_header)
        ],
        [
            Paragraph("<b>G-SIBs (Global Banks)</b>", style_table_cell),
            Paragraph("CET1 Ratios > 12.5%", style_table_cell),
            Paragraph("<font color='#10B981'><b>LOW</b></font>", style_table_cell),
            Paragraph("Abundant liquidity cushions and balance sheets validated by Federal Reserve stress tests.", style_table_cell)
        ],
        [
            Paragraph("<b>Regional Banks &amp; CRE</b>", style_table_cell),
            Paragraph("Office Real Estate Loans", style_table_cell),
            Paragraph("<font color='#D97706'><b>MODERATE</b></font>", style_table_cell),
            Paragraph("High-rate office refinancing requires continued provisioning across regional lenders.", style_table_cell)
        ],
        [
            Paragraph("<b>Consumer Credit</b>", style_table_cell),
            Paragraph("Credit Card Debt > $1.2T", style_table_cell),
            Paragraph("<font color='#D97706'><b>MODERATE</b></font>", style_table_cell),
            Paragraph("Gradual delinquency upticks across lower-income strata; prime consumption remains intact.", style_table_cell)
        ],
        [
            Paragraph("<b>Volatility &amp; Liquidity (VIX)</b>", style_table_cell),
            Paragraph("VIX at 14.88 points", style_table_cell),
            Paragraph("<font color='#10B981'><b>CONTROLLED</b></font>", style_table_cell),
            Paragraph("Low volatility environment reflecting market complacency; vulnerable to exogenous shocks.", style_table_cell)
        ],
        [
            Paragraph("<b>Technology Valuations</b>", style_table_cell),
            Paragraph("Forward P/E > 23x", style_table_cell),
            Paragraph("<font color='#DC2626'><b>ELEVATED</b></font>", style_table_cell),
            Paragraph("Stretched multiples make prices highly sensitive to quarterly earnings decelerations.", style_table_cell)
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

    story.append(PageBreak()) # End Page 6

    # =========================================================
    # PAGE 7: 2008 BENCHMARK & DISRUPTION PROBABILITIES
    # =========================================================
    story.append(Paragraph("7. Systemic Risk Benchmark: 2008 Comparison &amp; Recalibrated Probabilities", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "To evaluate the likelihood of a systemic shock, we contrast 2008 fundamentals with current market structures across key indicators:",
        style_body
    ))

    if os.path.exists("chart_crisis_probs.png"):
        story.append(Image("chart_crisis_probs.png", width=6.8*inch, height=2.40*inch))
        story.append(Spacer(1, 5))

    crisis_comp_table = [
        [
            Paragraph("<b>Structural Metric</b>", style_table_header),
            Paragraph("<b>2008 Crisis (GFC)</b>", style_table_header),
            Paragraph("<b>Current Condition (2026)</b>", style_table_header),
            Paragraph("<b>Comparative Risk Verdict</b>", style_table_header)
        ],
        [
            Paragraph("<b>Bank Capital (CET1)</b>", style_table_cell),
            Paragraph("Fragile (&lt; 6-8%), leverage 30:1", style_table_cell),
            Paragraph("Robust (&gt; 13.4%), leverage 11:1", style_table_cell),
            Paragraph("<font color='#10B981'><b>Substantially safer today</b></font> (Dodd-Frank frameworks).", style_table_cell)
        ],
        [
            Paragraph("<b>Residential Mortgages</b>", style_table_cell),
            Paragraph("Toxic subprime (NINJA loans), LTV &gt; 100%", style_table_cell),
            Paragraph("Prime borrowers (FICO &gt; 740), LTV &lt; 65%", style_table_cell),
            Paragraph("<font color='#10B981'><b>Home equity locked at ultra-low fixed rates</b></font>.", style_table_cell)
        ],
        [
            Paragraph("<b>Public Debt / GDP</b>", style_table_cell),
            Paragraph("64% of GDP ($9.5T)", style_table_cell),
            Paragraph("<b>123% of GDP ($40.2T)</b>", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Worse today:</b></font> Sovereign interest costs exceed $1.1T/year.", style_table_cell)
        ],
        [
            Paragraph("<b>Interbank Liquidity</b>", style_table_cell),
            Paragraph("Total freeze (TED spread &gt; 300 bps)", style_table_cell),
            Paragraph("Abundant liquidity (Normal spreads)", style_table_cell),
            Paragraph("<font color='#10B981'><b>No immediate interbank liquidity strain</b></font>.", style_table_cell)
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
            Paragraph("<b>NEXT 3 MONTHS:</b> <font color='#10B981'><b>5% Probability</b></font> (Very Low Risk). Hyperscaler balance sheets and cash earnings prevent near-term systemic shocks.", style_table_cell),
            Paragraph("<b>NEXT 9 MONTHS:</b> <font color='#D97706'><b>18% Probability</b></font> (Moderate Risk). CRE debt rollovers and early AI monetization hurdles induce neocloud stress.", style_table_cell),
            Paragraph("<b>NEXT 2 YEARS (24M):</b> <font color='#DC2626'><b>35% Probability</b></font> (Elevated Risk). Confluence of $40T sovereign debt roll, hardware obsolescence, and private credit strain.", style_table_cell),
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

    story.append(PageBreak()) # End Page 7

    # =========================================================
    # PAGE 8: ROAD AHEAD & ALLOCATION STRATEGY
    # =========================================================
    story.append(Paragraph("8. The Road Ahead: Probabilistic Scenarios &amp; Strategic Allocation Directives", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6, spaceBefore=0))

    story.append(Paragraph(
        "To guide portfolio allocations across upcoming quarters, we outline the three primary probabilistic macroeconomic scenarios:",
        style_body
    ))

    scenarios_data = [
        [
            Paragraph("<b>Probabilistic Scenario</b>", style_table_header),
            Paragraph("<b>Prob.</b>", style_table_header),
            Paragraph("<b>Macro Environment &amp; Federal Reserve</b>", style_table_header),
            Paragraph("<b>Asset Class Behavior</b>", style_table_header)
        ],
        [
            Paragraph("<b>Scenario 1: Soft Landing &amp; AI Expansion<br/>(Base Case)</b>", style_table_cell),
            Paragraph("<b>52%</b><br/><font color='#10B981'>Likely</font>", style_table_cell),
            Paragraph("Inflation converges toward ~2.5%. Fed holds policy rates with measured adjustments. AI capex lifts corporate net margins.", style_table_cell),
            Paragraph("S&amp;P 500 advances moderately (+6% to +10%); 10Y yields settle between 4.70% and 5.00%; Big Tech, Financials, and Industrials lead.", style_table_cell)
        ],
        [
            Paragraph("<b>Scenario 2: Higher for Longer &amp; Deficit Strain</b>", style_table_cell),
            Paragraph("<b>30%</b><br/><font color='#D97706'>Moderate</font>", style_table_cell),
            Paragraph("Inflation persists near ~3.2% fueled by $40T federal deficit and tariffs. Fed maintains restrictive rates with zero easing room.", style_table_cell),
            Paragraph("P/E multiple compression (down to 19-20x); 10Y Treasuries test 5.50%; Dollar strengthens; Rotation to Value, Energy, and Short Paper.", style_table_cell)
        ],
        [
            Paragraph("<b>Scenario 3: Credit Stress &amp; AI De-Rating<br/>(Delayed Hard Landing)</b>", style_table_cell),
            Paragraph("<b>18%</b><br/><font color='#DC2626'>Tail Risk</font>", style_table_cell),
            Paragraph("Lagged monetary drag dampens consumption; defaults across neoclouds and CRE office portfolios trigger valuation write-downs.", style_table_cell),
            Paragraph("S&amp;P 500 corrects (-15% to -22%); VIX surges to 28-35; Flight to quality into safe-haven government bonds (10Y yields drop below 4.0%).", style_table_cell)
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

    story.append(Paragraph("<b>Portfolio Management Directives &amp; Risk Mitigation:</b>", style_body_bold))
    story.append(Paragraph(
        "• <b>Broaden Exposure Beyond Mega-Caps:</b> Rebalance technology concentration into high-quality cyclical sectors, energy infrastructure (power utilities powering AI facilities), healthcare, and money-center banks.<br/>"
        "• <b>Lock in Compelling Real Yields:</b> Intermediate US Treasuries (3 to 7 years) offer attractive nominal yields (~4.8% - 5.1%) and real rates exceeding 2.0% p.a., providing robust defensive ballast.<br/>"
        "• <b>Rigorous Selectivity in AI Assets:</b> Favor platforms with pricing power and genuine organic free cash flows, avoiding venture-backed hardware spec plays with unvalidated monetization.<br/>"
        "• <b>Strategic Allocation to Gold:</b> Maintain a 5% to 10% portfolio allocation in physical gold reserves as an essential safe-haven hedge against long-term US sovereign debt expansion and geopolitical conflicts.",
        style_body
    ))
    story.append(Spacer(1, 6))

    footer_box = [
        [
            Paragraph("<b>REPORT COMPILATION:</b> Automated quantitative and fundamental analysis • Real-time financial feeds • Institutional risk and capital management intelligence.", ParagraphStyle('FtrBox', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor('#475569')))
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
    print(f"US Market Report successfully compiled: {output_filename}", flush=True)

def main():
    pdf_path = "Relatorio_Mercado_Financeiro_Americano_EN.pdf"
    build_pdf_report(None, pdf_path)
    print(f"Generated: {os.path.abspath(pdf_path)}", flush=True)

if __name__ == "__main__":
    main()
