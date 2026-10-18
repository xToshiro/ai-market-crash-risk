#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_recent_market_update_report_en.py
--------------------------------------------
Generates an 8-page institutional PDF executive report in English:
"Executive Report: Market Update (October 2026) — Microsoft-Nscale Termination,
Anthropic IPO Valuation Haircut, The Power Grid Wall, and Recalibrated Projections (2026–2029)"

Output: reports/en/Report_Market_Update_Oct2026_Grid_Anthropic.pdf
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
from utils_paths import get_chart_path, get_report_en_path

# Custom Canvas with Running Header and Footer (Page X of Y)
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
            self.drawString(54, 750, "SPECIAL RISK UPDATE • OCTOBER 2026")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "GRID CHOKE POINT & RECALIBRATED SCENARIOS")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential • Institutional Research, SEC Filings, FT, National Grid UK, Euronext, and Proprietary Models")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Report_Market_Update_Oct2026_Grid_Anthropic.pdf"):
    out_path = get_report_en_path(output_filename)
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
    # PAGE 1: EXECUTIVE COVER, KPI DASHBOARD & MASTER TABLE
    # =========================================================
    header_data = [
        [
            Paragraph("<b>INSTITUTIONAL RESEARCH • SPECIAL RISK UPDATE DOSSIER</b>", ParagraphStyle('HdrTag', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#DC2626'))),
            Paragraph(f"Base Date: {datetime.date.today().strftime('%B %d, %Y')} | Horizon: 2026–2029", ParagraphStyle('HdrDate', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))
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

    story.append(Paragraph("Strategic Market Update: Microsoft-Nscale Termination, Anthropic IPO Haircut, The Power Grid Wall, and Recalibrated Projections (2026–2029)", style_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Audit of critical October 2026 empirical developments: the definitive transition from silicon shortages to physical electrical transmission bottlenecks, pre-IPO growth deceleration, and increased credit dislocation risk.", style_subtitle))
    story.append(Spacer(1, 8))

    # Alert Banner
    box_alert = [
        [
            Paragraph("<b>CYCLICAL INFLECTION NOTICE (OCTOBER 2026):</b> Microsoft's formal termination of its anchor tenant lease at Nscale's flagship Essex (UK) campus—triggered by National Grid projections deferring power connection to the 2030s—alongside a $500 billion haircut in Anthropic's pre-IPO target valuation confirms that the AI infrastructure supercycle has hit both physical and financial friction. The cumulative probability of Scenario 2 (Credit Dislocation & Grid Bottlenecks) is recalibrated upward from 34% to 40%.", style_callout)
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

    story.append(Paragraph("<b>Consolidated Dashboard of Critical Findings & Recalibrated Indicators (October 2026)</b>", style_h1))
    
    kpi_table_data = [
        [
            Paragraph("Critical Event / Indicator", style_table_header),
            Paragraph("Observed Metric", style_table_header),
            Paragraph("Technical Finding", style_table_header),
            Paragraph("Systemic Risk Implication", style_table_header)
        ],
        [
            Paragraph("<b>Microsoft & Nscale Contract</b>", style_table_cell_bold),
            Paragraph("Essex Lease Terminated (50–90 MW)", style_table_cell_center),
            Paragraph("Grid connection deferred to 2030s", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Critical:</b></font> Depresses neocloud valuations & IPOs", style_table_cell)
        ],
        [
            Paragraph("<b>Anthropic IPO Target Valuation</b>", style_table_cell_bold),
            Paragraph("Cut from $2.0T to ~$1.5T", style_table_cell_center),
            Paragraph("$500B Valuation Haircut (-25%)", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Severe:</b></font> Rejection of perpetual exponential multiples", style_table_cell)
        ],
        [
            Paragraph("<b>Anthropic Q3 Quarterly Revenue</b>", style_table_cell_bold),
            Paragraph("$16.8B (+44.8% QoQ)", style_table_cell_center),
            Paragraph("Sharp deceleration from +146% QoQ", style_table_cell),
            Paragraph("<font color='#D97706'><b>Moderate/High:</b></font> Rising enterprise acquisition costs", style_table_cell)
        ],
        [
            Paragraph("<b>GSU Transformer Lead Times</b>", style_table_cell_bold),
            Paragraph("36 to 60 Months (3–5 Years)", style_table_cell_center),
            Paragraph("Severe grain-oriented electrical steel shortage", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Physical:</b></font> 30% to 50% of campuses cannot energize", style_table_cell)
        ],
        [
            Paragraph("<b>Consolidated Annual AI CapEx</b>", style_table_cell_bold),
            Paragraph("$650B to $700B / Year Run-Rate", style_table_cell_center),
            Paragraph("Historically unprecedented capital intensity", style_table_cell),
            Paragraph("<font color='#D97706'><b>Financial:</b></font> Migration to off-balance private credit", style_table_cell)
        ],
        [
            Paragraph("<b>Credit & Grid Shock Probability (S2)</b>", style_table_cell_bold),
            Paragraph("Raised from 34% to 40%", style_table_cell_center),
            Paragraph("+6 pp increase in credit dislocation risk", style_table_cell),
            Paragraph("<font color='#DC2626'><b>Systemic:</b></font> Impairment of underwater GPU collateral", style_table_cell)
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

    story.append(Paragraph("<b>Structure of the Four Core Analytical Pillars in this Report:</b>", style_body_bold))
    story.append(Paragraph("<b>1. The Rigid Physics of Electric Transmission:</b> How utility grid queue freezes are compelling tech giants to terminate multi-billion-dollar commitments.<br/>"
                           "<b>2. Pre-IPO Valuation Realism:</b> The compression of frontier model lab multiples driven by massive computing liabilities and sequential revenue deceleration.<br/>"
                           "<b>3. Off-Balance-Sheet Risk Migration:</b> How hyperscalers are leveraging private credit funds (Blackstone, GAIIP, Blue Owl) to fund power infrastructure without bloating corporate balance sheets.<br/>"
                           "<b>4. Recalibrated Asset Pricing & Systemic Risk:</b> Updated loss severity models for leading tech equities (NVDA, TSM, MSFT, ORCL) and structured Data Center ABS tranches.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PAGE 2: THE MICROSOFT-NSCALE CASE AND THE ESSEX COLLAPSE
    # =========================================================
    story.append(Paragraph("The Microsoft & Nscale Case: The Essex Fracture and The Physical Grid Choke Point", style_h1))
    story.append(Paragraph("In October 2026, UK-based AI neocloud and high-density infrastructure operator Nscale—backed by Nvidia equity and linked to major European compute initiatives—suffered the formal termination by Microsoft of its anchor lease agreement at the planned Loughton campus in Essex, UK.", style_body))
    story.append(Spacer(1, 4))

    chart_grid = get_chart_path("chart_grid_bottleneck_delays.png", lang="en")
    if os.path.exists(chart_grid):
        story.append(Image(chart_grid, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Anatomy of the Loughton Project and the Catalysts for Termination:</b>", style_body_bold))
    story.append(Paragraph("• <b>Original Project Scope:</b> Engineered for an initial 50 MW (scalable to 90 MW), the facility was designed to host roughly 23,000 Nvidia GB300 (Blackwell Ultra) GPUs, championed by UK officials as the country's flagship sovereign AI supercomputer.<br/>"
                           "• <b>National Grid UK Assessment:</b> Transmission system operators formally notified developers that local substations and high-voltage corridors were fully congested. The estimated energization delivery date was pushed back into the <b>2030s</b> (a 5-to-7-year operational delay!).<br/>"
                           "• <b>Microsoft's Decision to Terminate:</b> Unwilling to carry idle capital expenditure in hardware that cannot be energized during this GPU product generation, Microsoft rescinded its anchor tenant commitment.<br/>"
                           "• <b>Corporate Ramifications for Nscale:</b> Nscale relies on Microsoft and Anthropic for the vast majority of its forward revenue pipeline. This loss delivers an acute blow to the valuation targets and timeline of its planned New York Stock Exchange IPO.", style_body))
    story.append(Spacer(1, 4))

    box_nscale = [
        [
            Paragraph("<b>CRITICAL FORENSIC TAKEAWAY:</b> The Essex precedent empirically confirms this repository's core thesis: no volume of financial capital can compress the physical timeline of high-voltage transmission lines and transformer manufacturing. Digital acceleration has collided with utility inertia.", style_callout)
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
    # PAGE 3: ANTHROPIC: GROWTH DECELERATION & VALUATION HAIRCUT
    # =========================================================
    story.append(Paragraph("Anthropic: Q3 Financial Audit and the $500 Billion Pre-IPO Valuation Discount", style_h1))
    story.append(Paragraph("During a confidential investor day in San Francisco ahead of its anticipated November 2026 public share sale, Anthropic disclosed financial metrics that demonstrate both remarkable top-line scale and the first concrete signs of sequential growth deceleration.", style_body))
    story.append(Spacer(1, 4))

    chart_anth = get_chart_path("chart_anthropic_growth_deceleration_valuation.png", lang="en")
    if os.path.exists(chart_anth):
        story.append(Image(chart_anth, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Financial Breakdown of Disclosed Metrics and Valuation Drivers:</b>", style_body_bold))
    story.append(Paragraph("1. <b>Sequential Growth Deceleration (QoQ):</b> Anthropic's quarterly revenue expanded from <b>$4.7 Billion in Q1-2026</b> to <b>$11.6 Billion in Q2-2026 (+146.8%)</b>. However, Q3 revenue came in at <b>$16.8 Billion (+44.8%)</b>. While top-line run-rate exceeds $60B, the deceleration from 146% to 45% prompted fund managers to recalibrate terminal growth rates.<br/>"
                           "2. <b>The Pre-IPO Valuation Haircut:</b> Institutional underwriters and crossover funds who had discussed valuation targets approaching <b>$2.0 Trillion</b> revised their targets down to approximately <b>$1.5 Trillion</b>, representing an immediate $500 billion valuation discount (-25%).<br/>"
                           "3. <b>Mounting Take-or-Pay Compute Liabilities:</b> Supporting $16.8B in quarterly gross revenue requires Anthropic to honor multi-year cloud infrastructure commitments with AWS, Google Cloud, and private data centers exceeding <b>$30 billion in forward contractual liabilities</b>.<br/>"
                           "4. <b>Enforcement Against Unauthorized SPVs:</b> Management explicitly voided secondary market transactions via unauthorized special-purpose vehicles, curbing speculative retail run-ups ahead of institutional bookbuilding.", style_body))
    story.append(Spacer(1, 4))

    box_anth = [
        [
            Paragraph("<b>INSTITUTIONAL DIAGNOSIS:</b> The multiple compression from 40x forward revenue down to ~25x highlights Wall Street's demand for proven free cash flow conversion and adequate margin protection against massive cloud compute overhead.", style_callout)
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
    # PAGE 4: THE GLOBAL POWER GRID WALL
    # =========================================================
    story.append(Paragraph("The Global Power Grid Wall: Critical Hardware Scarcity and Interconnection Freezes", style_h1))
    story.append(Paragraph("The primary constraint facing accelerated computing expansion in 2026 is no longer silicon fab capacity, but the physical inability of electric power grids to transmit and energize multi-hundred-megawatt campuses.", style_body))
    story.append(Spacer(1, 6))

    grid_table_data = [
        [
            Paragraph("Supply Chain / Grid Variable", style_table_header),
            Paragraph("Baseline (2021)", style_table_header),
            Paragraph("Current Lead Time (2026)", style_table_header),
            Paragraph("Operational Impact on Data Centers", style_table_header)
        ],
        [
            Paragraph("<b>Generator Step-Up (GSU) Transformers</b>", style_table_cell_bold),
            Paragraph("14 to 18 Months", style_table_cell_center),
            Paragraph("<b>36 to 60 Months (3–5 Yrs)</b>", style_table_cell_center),
            Paragraph("Paralyzes high-voltage substation commissioning", style_table_cell)
        ],
        [
            Paragraph("<b>High-Voltage Circuit Breakers</b>", style_table_cell_bold),
            Paragraph("10 to 12 Months", style_table_cell_center),
            Paragraph("<b>30 to 42 Months</b>", style_table_cell_center),
            Paragraph("Shortage of 500 kV gas-insulated switchgear", style_table_cell)
        ],
        [
            Paragraph("<b>Utility Queue Studies (FERC / PJM)</b>", style_table_cell_bold),
            Paragraph("2 to 3 Years", style_table_cell_center),
            Paragraph("<b>5 to 7 Years</b>", style_table_cell_center),
            Paragraph("Transmission engineering impact analyses frozen", style_table_cell)
        ],
        [
            Paragraph("<b>PJM Base Residual Auction Clearing</b>", style_table_cell_bold),
            Paragraph("$28.92 / MW-day", style_table_cell_center),
            Paragraph("<b>$269.92 / MW-day</b>", style_table_cell_center),
            Paragraph("Nearly 10x surge in firm capacity procurement costs", style_table_cell)
        ],
        [
            Paragraph("<b>Project Delay & Cancellation Rate</b>", style_table_cell_bold),
            Paragraph("< 10% of Projects", style_table_cell_center),
            Paragraph("<b>30% to 50% of Projects</b>", style_table_cell_center),
            Paragraph("Developers abandon shells lacking binding power contracts", style_table_cell)
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

    story.append(Paragraph("<b>Three Structural Consequences of the Electric Power Squeeze:</b>", style_body_bold))
    story.append(Paragraph("1. <b>Stranded Clusters & Unproductive Depreciation:</b> Neoclouds and labs that received GPU allocations prior to securing energized utility feeds face ongoing debt service on hardware sitting idle in unpowered buildings.<br/>"
                           "2. <b>The Nuclear & Behind-the-Meter Race:</b> The grid bottleneck has triggered massive bilateral utility contracts, such as Constellation's Three Mile Island restart for Microsoft, Google's SMR agreements with Kairos Power, and Amazon's Talen Energy nuclear campus. However, commercial output will not scale until the 2028–2032 window.<br/>"
                           "3. <b>Geographic Capital Flight:</b> Confronting grid congestion across the US Mid-Atlantic and Western Europe, developers are redirecting compute capital to energy-abundant regions (Norway, Finland, Sweden, and the Gulf states).", style_body))

    story.append(PageBreak())

    # =========================================================
    # PAGE 5: $700B CAPEX SUPERCYCLE & PRIVATE CREDIT
    # =========================================================
    story.append(Paragraph("The $700 Billion CapEx Supercycle and Off-Balance-Sheet Engineering", style_h1))
    story.append(Paragraph("To sustain unprecedented capital expenditures in power and data centers without threatening their pristine investment-grade corporate debt ratings (AAA/AA), hyperscalers have aggressively turned to off-balance-sheet SPVs and private credit partnerships.", style_body))
    story.append(Spacer(1, 4))

    chart_capex = get_chart_path("chart_hyperscaler_capex_vs_private_credit.png", lang="en")
    if os.path.exists(chart_capex):
        story.append(Image(chart_capex, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Mechanics of Master Trusts and Digital Infrastructure SPVs:</b>", style_body_bold))
    story.append(Paragraph("• <b>Balance Sheet Insulation:</b> Rather than absorbing mega-campus construction liabilities directly, hyperscalers establish bankruptcy-remote Special Purpose Vehicles co-sponsored by private infrastructure managers (BlackRock/GIP, Blackstone, Blue Owl, Apollo, Magnetar).<br/>"
                           "• <b>Private Debt Leverage:</b> The SPV issues non-recourse private loans and Data Center Asset-Backed Securities (ABS). The Big Tech sponsor enters a long-term triple-net operating lease, classifying the obligation as off-balance-sheet capacity.<br/>"
                           "• <b>The GAIIP Consortium:</b> The partnership between BlackRock, Global Infrastructure Partners (GIP), Microsoft, and MGX targets $30B to $100B in mobilized equity and debt, transferring direct capital absorption away from Microsoft's treasury.<br/>"
                           "• <b>The Illusion of Disconnection:</b> While kept off core balance sheets, contractual lease commitments remain rigid fixed charges. Any material deceleration in end-user enterprise software monetization will challenge the private credit ecosystem funding these structures.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PAGE 6: RECALIBRATION OF CRASH SCENARIOS (2026-2029)
    # =========================================================
    story.append(Paragraph("Formal Recalibration of Market Crash Scenarios (2026–2029)", style_h1))
    story.append(Paragraph("Incorporating October 2026 empirical shocks necessitates a formal recalibration of scenario probability distributions and stress-test loss parameters:", style_body))
    story.append(Spacer(1, 4))

    chart_probs = get_chart_path("chart_updated_crash_probabilities_2026_2029.png", lang="en")
    if os.path.exists(chart_probs):
        story.append(Image(chart_probs, width=504, height=205))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Detailed Recalibrated Scenario Matrix:</b>", style_body_bold))
    story.append(Paragraph("• <b>Scenario 1: Orderly Deceleration (Probability reduced from 48% to 42%):</b> CapEx growth moderates to ~10% YoY; enterprise agent workflows ramp steadily; equity valuation multiples contract mildly (S&P drops 10%–15%, Nasdaq 18%–22%); senior Class A ABS notes remain fully unimpaired.<br/>"
                           "• <b>Scenario 2: Credit Dislocation & Grid Bottleneck (Probability raised from 34% to 40%):</b> Triggered by the cancellation of unpowered data center campuses, neocloud covenant breaches ($DSCR < 1.10x$), steep valuation discounts in pre-IPO rounds, and a secondary market collapse in older GPU hardware. S&P 500 declines 25%–32%, Nasdaq 35%–45%, with severe losses concentrated in subordinated Class B and equity ABS tranches.<br/>"
                           "• <b>Scenario 3: Systemic Multi-Contagion (Probability maintained at 18%):</b> Coincidental rupture involving the AI credit unwind, acute US Treasury refinancing friction ($40T Debt at >5.5% yields), and geopolitical friction in the Taiwan Strait. Nasdaq plunges >55% and S&P >45%, requiring emergency Federal Reserve liquidity facilities.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PAGE 7: RECALIBRATED STOCK TARGET PRICES (H2-2027)
    # =========================================================
    story.append(Paragraph("Recalibrated Predictive Target Price Matrix for AI Leaders (H2-2027)", style_h1))
    story.append(Paragraph("The following matrix presents updated target prices and downside severity across the 8 industry leaders and benchmark indices, incorporating the heightened probability of the Credit & Grid Shock Scenario:", style_body))
    story.append(Spacer(1, 6))

    stock_target_data = [
        [
            Paragraph("Asset / Ticker", style_table_header),
            Paragraph("Current Price", style_table_header),
            Paragraph("Base Target (H2)", style_table_header),
            Paragraph("Base Return", style_table_header),
            Paragraph("Stress Target (Grid/Credit)", style_table_header),
            Paragraph("Stress Drawdown", style_table_header)
        ],
        [
            Paragraph("<b>Nvidia (NVDA)</b>", style_table_cell_bold),
            Paragraph("$229.28", style_table_cell_center),
            Paragraph("$255.00", style_table_cell_center),
            Paragraph("+11.2%", style_table_cell_center),
            Paragraph("<b>$115.00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-49.8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>TSMC (TSM)</b>", style_table_cell_bold),
            Paragraph("$190.50", style_table_cell_center),
            Paragraph("$218.00", style_table_cell_center),
            Paragraph("+14.4%", style_table_cell_center),
            Paragraph("<b>$110.00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-42.3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Broadcom (AVGO)</b>", style_table_cell_bold),
            Paragraph("$184.80", style_table_cell_center),
            Paragraph("$210.00", style_table_cell_center),
            Paragraph("+13.6%", style_table_cell_center),
            Paragraph("<b>$115.00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-37.8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Oracle (ORCL)</b>", style_table_cell_bold),
            Paragraph("$141.40", style_table_cell_center),
            Paragraph("$148.00", style_table_cell_center),
            Paragraph("+4.7%", style_table_cell_center),
            Paragraph("<b>$85.00</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-39.9%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Meta Platforms (META)</b>", style_table_cell_bold),
            Paragraph("$718.67", style_table_cell_center),
            Paragraph("$780.00", style_table_cell_center),
            Paragraph("+8.5%", style_table_cell_center),
            Paragraph("<b>$510.00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-29.0%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Amazon (AMZN)</b>", style_table_cell_bold),
            Paragraph("$262.43", style_table_cell_center),
            Paragraph("$295.00", style_table_cell_center),
            Paragraph("+12.4%", style_table_cell_center),
            Paragraph("<b>$195.00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-25.7%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Microsoft (MSFT)</b>", style_table_cell_bold),
            Paragraph("$535.07", style_table_cell_center),
            Paragraph("$575.00", style_table_cell_center),
            Paragraph("+7.5%", style_table_cell_center),
            Paragraph("<b>$405.00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-24.3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Alphabet (GOOGL)</b>", style_table_cell_bold),
            Paragraph("$351.66", style_table_cell_center),
            Paragraph("$385.00", style_table_cell_center),
            Paragraph("+9.5%", style_table_cell_center),
            Paragraph("<b>$275.00</b>", style_table_cell_bold),
            Paragraph("<font color='#D97706'><b>-21.8%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>Nasdaq 100 (^NDX)</b>", style_table_cell_bold),
            Paragraph("27,366 pts", style_table_cell_center),
            Paragraph("29,500 pts", style_table_cell_center),
            Paragraph("+7.8%", style_table_cell_center),
            Paragraph("<b>17,700 pts</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-35.3%</b></font>", style_table_cell_center)
        ],
        [
            Paragraph("<b>S&P 500 (^GSPC)</b>", style_table_cell_bold),
            Paragraph("7,811 pts", style_table_cell_center),
            Paragraph("8,200 pts", style_table_cell_center),
            Paragraph("+5.0%", style_table_cell_center),
            Paragraph("<b>5,600 pts</b>", style_table_cell_bold),
            Paragraph("<font color='#DC2626'><b>-28.3%</b></font>", style_table_cell_center)
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

    story.append(Paragraph("<b>Key Risk Asymmetries:</b><br/>"
                           "• <b>Acute Hardware Scarcity Reversal:</b> Nvidia (-49.8%) and TSMC (-42.3%) experience the highest drawdown vulnerability, as any delay in energizing clusters directly suspends secondary and tertiary silicon purchase orders.<br/>"
                           "• <b>Defensive Solvency of Alphabet (-21.8%) and Microsoft (-24.3%):</b> Robust net cash reserves ($88B net cash for Alphabet) and legacy enterprise software cash flows protect sovereign hyperscalers from balance sheet default.", style_body))

    story.append(PageBreak())

    # =========================================================
    # PAGE 8: RISK MANAGEMENT DIRECTIVES & DISCLAIMER
    # =========================================================
    story.append(Paragraph("Institutional Risk Management Directives and Final Conclusions", style_h1))
    story.append(Paragraph("The empirical evidence consolidated in October 2026 mandates structural revisions across portfolio risk management and credit underwriting:", style_body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Mandatory Physical Grid Interconnection Audits:</b>", style_body_bold))
    story.append(Paragraph("Institutional lenders must reject speculative interconnection letters of intent. Debt facilities should require verified utility substations with energized transformers already delivered on-site prior to capital disbursement.", style_body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2. Subordination Buffers in Structured Data Center ABS:</b>", style_body_bold))
    story.append(Paragraph("Credit rating agencies (KBRA, S&P, Moody's) must adjust KNCF cash flow hair-cuts to reflect correlated neocloud default risk. Mezzanine and junior equity tranches should expand subordination buffers to at least <b>25% to 30%</b> of aggregate debt to protect investment-grade notes.", style_body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3. Tactical Equity Rebalancing:</b>", style_body_bold))
    story.append(Paragraph("Trim exposure to pure-play hardware vendors trading at extreme multiples (>35x P/E) and rotate toward diversified hyperscalers with self-secured energy solutions (Google with proprietary TPUs, Amazon with behind-the-meter nuclear PPAs).", style_body))
    story.append(Spacer(1, 10))

    box_disc = [
        [
            Paragraph("<b>INSTITUTIONAL DISCLAIMER:</b> This research report has been prepared solely for institutional analytical, educational, and forensic research purposes. The projections, predictive price targets, probability distributions, and stress-test scenarios represent econometric tail-risk simulations and do not constitute investment advice, financial planning, or a solicitation to buy or sell any securities or financial derivatives. Historical asset performance does not guarantee future financial outcomes.", ParagraphStyle('DiscTxt', fontName='Helvetica-Oblique', fontSize=6.8, leading=9.5, textColor=colors.HexColor('#64748B')))
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
    print(f"[OK] Generated English Report: {out_path}")

def main():
    build_pdf_report()

if __name__ == '__main__':
    main()
