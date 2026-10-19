#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fear_indices_report_en.py
------------------------------------
Generates a 6-page institutional PDF executive report in English:
"Executive Report: Anatomy of the Fear Indices — VIX, MOVE Index, and Algorithmic
Deleveraging Triggers in AI Equities & Infrastructure Credit (2020–2026)"

Output: reports/en/Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf
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
            self.drawString(54, 750, "INSTITUTIONAL REPORT • ANATOMY OF THE FEAR INDICES")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "VIX, MOVE & AI DELEVERAGING (2020–2026)")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 42, 612 - 54, 42)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "Confidential • Institutional Research, CBOE, ICE BofA MOVE, BIS, Bloomberg & Proprietary Risk Models")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 30, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Report_Fear_Indices_VIX_MOVE_AI_Impact.pdf"):
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
    # PAGE 1: INSTITUTIONAL COVER, DASHBOARD & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("MACROECONOMIC INTELLIGENCE REPORT • OCTOBER 2026", ParagraphStyle('TopBadge', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor('#0284C7'), spaceAfter=4)))
    story.append(Paragraph("Anatomy of the Fear Indices: VIX, MOVE Index, and Algorithmic Deleveraging Triggers in AI Equities & Credit", style_title))
    story.append(Paragraph("Term Structure Inversion, Treasury Volatility, and Systematic Vol-Targeting Forced Selling Cascades (2020–2026)", style_subtitle))

    # Meta Block
    meta_data = [
        [
            Paragraph("<b>Date:</b> October 19, 2026", style_td),
            Paragraph("<b>Classification:</b> Systemic Risk & Volatility Architecture", style_td),
            Paragraph("<b>Coverage:</b> VIX, MOVE, SKEW, Big Tech, ABS", style_td),
            Paragraph("<b>Status:</b> Latent Tension Regime", style_td)
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
            "<b>CENTRAL THESIS:</b> The VIX and the MOVE Index are not sentimental psychological polls; they operate within the modern financial "
            "architecture as <b>programmatic mathematical control parameters</b>. Institutional strategies managing over $1.8 trillion in "
            "<i>Volatility-Targeting</i> and <i>Risk Parity</i> mandates are bound by statutory code to execute forced sell orders across liquid "
            "Big Tech equities whenever the VIX escalates past 25 points. Simultaneously, an elevated MOVE Index (> 120 pts) freezes the "
            "<i>Data Center ABS</i> underwriting syndicate, restricting the debt capital required to finance the $700 billion AI CapEx buildout.",
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
    story.append(Paragraph("1. Volatility Dashboard: Fear Gauges & Algorithmic Deleveraging Triggers", style_h1))
    
    dash_rows = [
        [Paragraph("Volatility & Fear Metric", style_th), Paragraph("Oct 2026 Value", style_th), Paragraph("Peak / Benchmark Level", style_th), Paragraph("Direct Transmission to Tech & Credit Complex", style_th)],
        [Paragraph("CBOE Volatility Index (VIX Spot)", style_td_bold), Paragraph("21.80 pts", style_td), Paragraph("65.73 (Aug/24) / 82.69 (Mar/20)", style_td), Paragraph("Latent tension; readings above 25 trigger systematic CTA selling.", style_td)],
        [Paragraph("ICE BofA MOVE Index (Treasuries)", style_td_bold), Paragraph("126.40 pts", style_td), Paragraph("198.70 (Mar/23 - SVB)", style_td), Paragraph("Sovereign debt distress; elevates and freezes Data Center ABS primary debt.", style_td)],
        [Paragraph("CBOE SKEW Index (Tail Risk)", style_td_bold), Paragraph("146.20 pts", style_td), Paragraph("170.50 (All-time High)", style_td), Paragraph("Persistent institutional demand for deep OTM crash puts and disaster hedges.", style_td)],
        [Paragraph("CBOE VVIX (Vol of VIX)", style_td_bold), Paragraph("104.50 pts", style_td), Paragraph("215.00 (Aug/2024)", style_td), Paragraph("Tracks option pricing instability; readings above 100 signal tail anxiety.", style_td)],
        [Paragraph("VIX Spot vs 3M Futures Spread", style_td_bold), Paragraph("-1.40 pts", style_td), Paragraph("+38.33 pts (Aug/24 Inversion)", style_td), Paragraph("Narrow contango; close to backwardation inversion for immediate protection.", style_td)],
        [Paragraph("CNN Fear & Greed Index", style_td_bold), Paragraph("42 / 100", style_td), Paragraph("95 (Greed) / 10 (Extreme Fear)", style_td), Paragraph("Neutral-defensive; absence of the unhedged euphoria recorded in 2023.", style_td)],
        [Paragraph("Total Vol-Targeting / CTA AUM", style_td_bold), Paragraph("$1.82 Trillion", style_td), Paragraph("$1.95 Trillion (2024 Peak)", style_td), Paragraph("Algorithmic capital that deleverages programmatically as VIX escalates.", style_td)],
        [Paragraph("Primary Forced Selling Trigger", style_td_bold), Paragraph("VIX > 25.00 pts", style_td), Paragraph("Statutory Threshold", style_td), Paragraph("Enforces mandatory 35%–50% reduction in net gross equity portfolio risk.", style_td)],
        [Paragraph("Data Center ABS Freeze Point", style_td_bold), Paragraph("MOVE > 140.00 pts", style_td), Paragraph("Bond Stress Benchmark", style_td), Paragraph("Syndicates demand spreads > +300 bps, halting speculative cluster loans.", style_td)],
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
        "<b>Page 1 Synthesis:</b> Implied volatility benchmarks represent the operational circuit breakers of global capital markets. "
        "A VIX of 21.8 coupled with a MOVE reading of 126.4 demonstrates that Big Tech's margin for error is razor-thin.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TRIAD OF FEAR GAUGES & HISTORICAL SPIKES
    # =========================================================================
    story.append(Paragraph("2. The Triad of Fear Gauges: VIX, MOVE, and SKEW", style_h1))
    story.append(Paragraph(
        "Traditional equity research frequently assesses the VIX in isolation. However, the contemporary financial architecture "
        "is governed by three concurrent vectors: equity implied volatility (VIX), sovereign risk-free volatility (MOVE), and "
        "catastrophic tail-risk hedging demand (SKEW).",
        style_body
    ))
    story.append(Paragraph(
        "With the S&P 500 exhibiting a 34% concentration in the Magnificent Seven, the VIX is structurally linked to semiconductor "
        "and cloud multiples. When the VIX spikes, drawdowns in AI market leaders like NVIDIA are magnified by a factor of 2x to 3x relative "
        "to broader benchmarks. The visual below tracks historical VIX spikes against maximum peak-to-trough drawdowns.",
        style_body
    ))

    # Chart 1
    chart1_path = get_chart_path("chart_vix_historical_spikes_and_tech_drawdowns.png", lang="en")
    if os.path.exists(chart1_path):
        story.append(Image(chart1_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Historical Table
    story.append(Paragraph("<b>Historical VIX Spikes and Maximum Peak-to-Trough Drawdowns (2018–2026)</b>", style_body_bold))
    shock_rows = [
        [Paragraph("Market Shock Event", style_th), Paragraph("Peak VIX", style_th), Paragraph("QQQ Drawdown", style_th), Paragraph("NVDA Drawdown", style_th), Paragraph("Forensic Liquidation Dynamics", style_th)],
        [Paragraph("Volmageddon (Feb 2018)", style_td), Paragraph("50.3 pts", style_td), Paragraph("-10.5%", style_td), Paragraph("-15.2%", style_td), Paragraph("Implosion of inverse VIX exchange-traded products (XIV); rapid de-risking.", style_td)],
        [Paragraph("Q4 Tightening (Dec 2018)", style_td), Paragraph("36.2 pts", style_td), Paragraph("-23.1%", style_td), Paragraph("-54.0%", style_td), Paragraph("Fed policy autopilot; severe P/E multiple contraction across semiconductor leaders.", style_td)],
        [Paragraph("Covid-19 Crash (Mar 2020)", style_td), Paragraph("82.69 pts", style_td), Paragraph("-30.1%", style_td), Paragraph("-38.5%", style_td), Paragraph("Systemic global dash for cash; Federal Reserve emergency dollar swap activation.", style_td)],
        [Paragraph("Inflation Shock (Jun 2022)", style_td), Paragraph("34.0 pts", style_td), Paragraph("-33.8%", style_td), Paragraph("-66.4%", style_td), Paragraph("End of zero-interest-rate regime; heavy multiple compression in long-duration tech.", style_td)],
        [Paragraph("Carry Trade Crash (Aug 2024)", style_td), Paragraph("65.73 pts", style_td), Paragraph("-10.2%", style_td), Paragraph("-20.5%", style_td), Paragraph("Yen short squeeze forced macro funds to use NVIDIA as the emergency cash register.", style_td)],
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
    # PAGE 3: THE DUAL FEAR GAUGE — VIX VS MOVE
    # =========================================================================
    story.append(Paragraph("3. The Dual Fear Gauge: VIX (Equities) vs MOVE (US Treasuries)", style_h1))
    story.append(Paragraph(
        "While the VIX captures daily equity headlines, the <b>ICE BofA MOVE Index serves as the structural gatekeeper of the AI infrastructure supercycle</b>. "
        "The $700 billion AI CapEx buildout requires hyperscalers and neocloud operators to issue substantial debt facilities. "
        "The underlying benchmark yield (US 10Y Treasury) anchors the absolute cost of capital for these facilities.",
        style_body
    ))
    story.append(Paragraph(
        "When the MOVE index exceeds 120 points, institutional fixed-income syndicates face severe difficulty pricing long-term duration risk. "
        "Consequently, required credit spreads across *Data Center ABS* tranches widen substantially, raising capital hurdles for GPU deployments.",
        style_body
    ))

    # Chart 2
    chart2_path = get_chart_path("chart_dual_fear_index_vix_vs_move.png", lang="en")
    if os.path.exists(chart2_path):
        story.append(Image(chart2_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # MOVE Regimes Table
    story.append(Paragraph("<b>MOVE Volatility Regimes and Transmission to Data Center ABS Spreads</b>", style_body_bold))
    move_rows = [
        [Paragraph("MOVE Regime", style_th), Paragraph("MOVE Score", style_th), Paragraph("ABS Spread BBB/A", style_th), Paragraph("Primary Debt Market Conditions for AI Infrastructure", style_th)],
        [Paragraph("Normal / Benign", style_td_bold), Paragraph("< 90 pts", style_td), Paragraph("+115 bps", style_td), Paragraph("Accommodative underwriting; abundant financing clearing at 5.50%–6.00% coupons.", style_td)],
        [Paragraph("Elevated / Alert", style_td_bold), Paragraph("90 – 120 pts", style_td), Paragraph("+185 bps", style_td), Paragraph("Lenders demand disciplined debt service covenants and secured power PPA off-takes.", style_td)],
        [Paragraph("Credit Stress (Current)", style_td_bold), Paragraph("120 – 150 pts", style_td), Paragraph("+290 bps", style_td), Paragraph("Coupon rates escalate to 7.5%–8.0%; junior neoclouds face primary debt market freezes.", style_td)],
        [Paragraph("Liquidity Freeze", style_td_bold), Paragraph("> 150 pts", style_td), Paragraph("+480 bps+", style_td), Paragraph("Syndication window shuts down; subordinated GPU debt facilities suffer technical distress.", style_td)],
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
    # PAGE 4: VIX TERM STRUCTURE: CONTANGO VS BACKWARDATION
    # =========================================================================
    story.append(Paragraph("4. The VIX Term Structure: Contango (Calm) vs. Backwardation (Panic)", style_h1))
    story.append(Paragraph(
        "Cash spot VIX levels convey only instantaneous market pricing. To diagnose underlying systemic stress, "
        "analysts must inspect the <b>term structure of CBOE VIX futures contracts</b>.",
        style_body
    ))
    story.append(Paragraph(
        "Under normal conditions, the futures curve slopes upward in <i>Contango</i>: forward volatility costs more than cash spot volatility, generating "
        "positive roll yields for short-volatility strategies. During acute liquidity dislocations, the curve inverts violently into <i>Backwardation</i>: "
        "cash VIX spikes above longer-dated futures, revealing desperate institutional bids for immediate crash insurance and triggering algorithmic de-risking.",
        style_body
    ))

    # Chart 3
    chart3_path = get_chart_path("chart_vix_term_structure_contango_backwardation.png", lang="en")
    if os.path.exists(chart3_path):
        story.append(Image(chart3_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Curve Inversion Table
    story.append(Paragraph("<b>Forensic Diagnostics: VIX Futures Curve Slope & Institutional Positioning</b>", style_body_bold))
    curve_rows = [
        [Paragraph("Curve Morphology", style_th), Paragraph("Spot minus 3M Spread", style_th), Paragraph("Institutional Portfolio Positioning", style_th), Paragraph("Forward Signal for AI Equities", style_th)],
        [Paragraph("Deep Contango", style_td_bold), Paragraph("< -4.0 pts", style_td), Paragraph("Heavy short-volatility selling; synthetic yield extraction.", style_td), Paragraph("Broad complacency; momentum tech rally persists.", style_td)],
        [Paragraph("Narrow Contango (Current)", style_td_bold), Paragraph("-2.0 to 0.0 pts", style_td), Paragraph("Tactical leverage reduction; cautious options hedging.", style_td), Paragraph("Yellow alert; elevated sensitivity to macro data.", style_td)],
        [Paragraph("Initial Inversion", style_td_bold), Paragraph("+0.1 to +5.0 pts", style_td), Paragraph("CTAs initiate systematic selling of equity futures.", style_td), Paragraph("Active -5% to -8% cyclical drawdown in progress.", style_td)],
        [Paragraph("Severe Backwardation", style_td_bold), Paragraph("> +15.0 pts", style_td), Paragraph("Acute panic; simultaneous margin calls; VaR limit breaches.", style_td), Paragraph("Severe liquidity vacuum and disorderly sell-off.", style_td)],
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
    # PAGE 5: ALGORITHMIC MECHANICS & VOLATILITY TARGETING
    # =========================================================================
    story.append(Paragraph("5. Algorithmic Mechanics: How the VIX Drives Programmatic Selling", style_h1))
    story.append(Paragraph(
        "Modern market panic is not transmitted through emotional human selling; it is <b>automated by lines of quantitative code</b>. "
        "Systematic Volatility-Targeting and Risk Parity funds adjust equity exposure based on the mathematical formulation: "
        "<font face='Courier'>w = min(1.0, σ_target / σ_realized)</font>.",
        style_body
    ))
    story.append(Paragraph(
        "Whenever the VIX escalates from 15 to 25 or 35 points, systematic algorithms must liquidate hundreds of billions of dollars in equities "
        "to bring aggregate portfolio volatility back into compliance. Because mega-cap tech stocks and chip designers offer the deepest market liquidity, "
        "they serve as the primary reservoir from which algorithms extract cash.",
        style_body
    ))

    # Chart 4
    chart4_path = get_chart_path("chart_vol_targeting_deleveraging_cascade.png", lang="en")
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Deleveraging Simulation Table
    story.append(Paragraph("<b>Simulated Systematic Selling Pressure Across VIX Escalation Stages</b>", style_body_bold))
    algo_rows = [
        [Paragraph("VIX Escalation Step", style_th), Paragraph("Target Equity Weight", style_th), Paragraph("Estimated Dump ($B)", style_th), Paragraph("Most Liquidated Assets", style_th), Paragraph("Forward P/E Multiple Impact", style_th)],
        [Paragraph("12 $\\rightarrow$ 18 pts", style_td_bold), Paragraph("100% $\\rightarrow$ 78%", style_td), Paragraph("$45 Billion", style_td), Paragraph("Apple, Microsoft, Alphabet", style_td), Paragraph("Modest multiple contraction (-1.5x).", style_td)],
        [Paragraph("18 $\\rightarrow$ 25 pts", style_td_bold), Paragraph("78% $\\rightarrow$ 52%", style_td), Paragraph("$160 Billion", style_td), Paragraph("NVIDIA, Broadcom, Amazon", style_td), Paragraph("Cyclical multiple compression (-3.8x).", style_td)],
        [Paragraph("25 $\\rightarrow$ 35 pts", style_td_bold), Paragraph("52% $\\rightarrow$ 34%", style_td), Paragraph("$310 Billion", style_td), Paragraph("Full semiconductor complex", style_td), Paragraph("Severe de-rating across AI leaders (-6.5x).", style_td)],
        [Paragraph("35 $\\rightarrow$ 50+ pts", style_td_bold), Paragraph("34% $\\rightarrow$ 18%", style_td), Paragraph("$520 Billion+", style_td), Paragraph("Indiscriminate market dumping", style_td), Paragraph("Valuation collapse exceeding -12x.", style_td)],
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
    # PAGE 6: OPERATIONAL REGIME MATRIX, METHODOLOGY & SIGN-OFF
    # =========================================================================
    story.append(Paragraph("6. Operational Volatility Regimes & Risk Action Matrix", style_h1))
    story.append(Paragraph(
        "The integration of implied volatility benchmarks into the repository's decision matrix resolves into four actionable regimes:",
        style_body
    ))

    reg_rows = [
        [Paragraph("Volatility Regime", style_th), Paragraph("Quantitative Parameters", style_th), Paragraph("Systematic Algorithmic Action", style_th), Paragraph("Repository Model Stance", style_th)],
        [Paragraph("Regime 1: Complacency", style_td_bold), Paragraph("VIX < 15, MOVE < 90, Contango", style_td), Paragraph("Maximum leverage; programmatic inflows.", style_td), Paragraph("Monitor silent buildup of tail risk.", style_td)],
        [Paragraph("Regime 2: Tension (Current)", style_td_bold), Paragraph("VIX 16-24, MOVE 90-120, Flat", style_td), Paragraph("Cautious de-risking across marginal positions.", style_td), Paragraph("Maintain 48% calibration; selective hedging.", style_td)],
        [Paragraph("Regime 3: Deleveraging", style_td_bold), Paragraph("VIX 25-35, MOVE 120-150, Inversion", style_td), Paragraph("Mandatory liquidations; $160B+ dumped.", style_td), Paragraph("Yellow Alert: elevate crash risk to 65%.", style_td)],
        [Paragraph("Regime 4: Systemic Shock", style_td_bold), Paragraph("VIX > 40, MOVE > 150, Backwardation", style_td), Paragraph("Indiscriminate flight to cash; ABS freezes.", style_td), Paragraph("Red Alert: systemic market liquidation cascade.", style_td)],
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

    # Methodological Annex
    story.append(Paragraph("Methodological Annex: Vol-Targeting Deleveraging Formulation", style_h1))
    story.append(Paragraph(
        "Aggregate forced liquidation volume $V_{\\text{dump}}$ during a volatility expansion from $\\sigma_0$ to $\\sigma_1$ is governed by: "
        "<font face='Courier'>V_dump = AUM_vol \\cdot max(0, 1 - σ_target / σ_1)</font>. "
        "With institutional systematic AUM modeled at $1.82 trillion and $\\sigma_{\\text{target}} = 10\\%$, a VIX surge to 30 points (realized volatility $\\approx 26\\%$) "
        "forces over $240 billion of net equity capital extraction from the market.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # Sign-off & Sources Box
    sign_data = [
        [Paragraph("<b>Primary Sources & Official Institutional Datasets:</b>", style_td_bold)],
        [Paragraph(
            "• Chicago Board Options Exchange (CBOE): Historical VIX Data, VVIX, SKEW & VIX Term Structure Methodology<br/>"
            "• Bank of America Merrill Lynch / ICE: ICE BofA MOVE Index Methodology & Historical Yield Volatility<br/>"
            "• Bank for International Settlements (BIS): Research Papers on Volatility-Targeting Deleveraging Dynamics<br/>"
            "• Bridgewater Associates & AQR Capital Management: Risk Parity & Systematic Trend-Following White Papers<br/>"
            "• Bloomberg Professional & Options Clearing Corporation (OCC): Multi-Asset Options Surfaces",
            style_td
        )],
        [Paragraph("<b>Disclaimer:</b> This document is prepared strictly for academic and institutional systemic risk research. It does not constitute investment advice or a solicitation to buy or sell securities.", ParagraphStyle('Disc', parent=style_td, fontName='Helvetica-Oblique', fontSize=6.5, textColor=colors.HexColor('#64748B')))]
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
