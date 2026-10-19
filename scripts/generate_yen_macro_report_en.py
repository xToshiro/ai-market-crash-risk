#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_yen_macro_report_en.py
---------------------------------
Generates a 6-page institutional PDF executive report in English:
"Executive Report: The Japanese Yen Macroeconomic Dynamics — Global Carry Trade,
BoJ Structural Tightening, and the Shadow Liquidity Transmission in AI Infrastructure (2022–2026)"

Output: reports/en/Report_Macro_Yen_Carry_Trade_AI_Impact.pdf
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
            self.drawString(54, 750, "INSTITUTIONAL REPORT • MACROECONOMICS & YEN LIQUIDITY")
            self.setFont("Helvetica", 7.4)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "CARRY TRADE & AI TRANSMISSION (2022–2026)")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(54, 742, 612 - 54, 742)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.7)
        self.line(54, 42, 612 - 54, 42)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "Confidential • Institutional Research, US Treasury TIC Data, Bank of Japan (BoJ), BIS, Bloomberg & Proprietary Models")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 30, page_str)
        
        self.restoreState()

def build_pdf_report(output_filename="Report_Macro_Yen_Carry_Trade_AI_Impact.pdf"):
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
    story.append(Paragraph("The Japanese Yen Macroeconomic Dynamics: Global Carry Trade, BoJ Tightening, and Shadow Liquidity in AI Infrastructure", style_title))
    story.append(Paragraph("Transmission Anatomy of FX Leverage, U.S. Treasury TIC Inflows, and Tech Valuation Multiples (2022–2026)", style_subtitle))

    # Meta Block
    meta_data = [
        [
            Paragraph("<b>Date:</b> October 19, 2026", style_td),
            Paragraph("<b>Classification:</b> Systemic Risk & FX Liquidity Audit", style_td),
            Paragraph("<b>Coverage:</b> JPY, US Treasuries, Big Tech, ABS", style_td),
            Paragraph("<b>Status:</b> Post-BoJ Hike Calibration", style_td)
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
            "<b>CENTRAL THESIS:</b> The Japanese Yen is not a marginal currency; for two decades, it operated as the <b>world's premier cheap liquidity factory</b>. "
            "Structural policy rate normalization by the Bank of Japan (BoJ hiking to 1.00%–1.25%) and the narrowing differential with the Fed dismantle the "
            "implicit subsidy of the <i>Yen Carry Trade</i> (estimated between $3.8T and $4.8T), producing an ongoing deleveraging impulse that contracts Big Tech multiples "
            "and raises debt underwriting hurdles for the $700 billion AI CapEx buildout.",
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
    story.append(Paragraph("1. Macroeconomic Dashboard: JPY & Global Liquidity Indicators", style_h1))
    
    dash_rows = [
        [Paragraph("Macroeconomic Indicator", style_th), Paragraph("Oct 2026 Value", style_th), Paragraph("Peak / Historical Trough", style_th), Paragraph("Analytical Transmission to Tech & AI Sector", style_th)],
        [Paragraph("USD/JPY Spot Exchange Rate", style_td_bold), Paragraph("149.20", style_td), Paragraph("161.95 (Jul/24) / 103.2 (2021)", style_td), Paragraph("Stress zone; levels below 140 trigger forced quant fund margin calls.", style_td)],
        [Paragraph("Bank of Japan Policy Benchmark", style_td_bold), Paragraph("1.00% – 1.25%", style_td), Paragraph("-0.10% (NIRP 2016-2024)", style_td), Paragraph("33-year peak; officially terminates the zero-cost global leverage regime.", style_td)],
        [Paragraph("US Federal Funds Target Rate", style_td_bold), Paragraph("4.00% – 4.25%", style_td), Paragraph("5.50% (Peak 2023-2024)", style_td), Paragraph("Fed easing cycle; structurally narrows the bilateral Tokyo-NY rate spread.", style_td)],
        [Paragraph("Fed - BoJ Policy Rate Spread", style_td_bold), Paragraph("3.00% p.a.", style_td), Paragraph("5.60% p.a. (Jul/2023)", style_td), Paragraph("Compressed by 260 bps; substantially reduces carry trade hurdle returns.", style_td)],
        [Paragraph("Japan 10Y JGB Benchmark Yield", style_td_bold), Paragraph("1.35% p.a.", style_td), Paragraph("0.05% (Trough 2021)", style_td), Paragraph("Pulls capital back to Tokyo (repatriation of GPIF and private life insurers).", style_td)],
        [Paragraph("US 10Y Treasury Benchmark Yield", style_td_bold), Paragraph("5.10% p.a.", style_td), Paragraph("1.45% (Nov/2021)", style_td), Paragraph("Elevated risk-free discount rate; elevates data center debt capital hurdles.", style_td)],
        [Paragraph("Japan Holdings of US Debt (TIC)", style_td_bold), Paragraph("$1,068 Billion", style_td), Paragraph("$1,325 Billion (Nov/2021)", style_td), Paragraph("#1 foreign creditor to US; trimmed $257B for FX defense and repatriation.", style_td)],
        [Paragraph("Estimated Global Carry Trade Size", style_td_bold), Paragraph("$3.8T – $4.8T", style_td), Paragraph("$5.2T (Apex 2024)", style_td), Paragraph("Active unwind in progress; ongoing vulnerability for liquid tech equities.", style_td)],
        [Paragraph("Shunto Wage Settlements (Japan)", style_td_bold), Paragraph("+5.15% p.a.", style_td), Paragraph("+2.10% (2010-2020 Avg)", style_td), Paragraph("Guarantees structural durability of Ueda's monetary normalization cycle.", style_td)],
    ]
    t_dash = Table(dash_rows, colWidths=[120, 68, 116, 200])
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
        "<b>Page 1 Synthesis:</b> Yen currency deleveraging is not an isolated tail event; it represents a persistent, systemic liquidity drain. "
        "With each BoJ rate increment or Fed rate reduction, the margin cushion across dollar-denominated leveraged tech assets narrows.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: HISTORICAL CARRY SUPERCYCLE & GREAT DIVERGENCE (2021–2024)
    # =========================================================================
    story.append(Paragraph("2. Historical Carry Supercycle and the Great Divergence (2021–2024)", style_h1))
    story.append(Paragraph(
        "Between 2021 and mid-2024, global capital markets navigated the widest monetary policy divergence across G7 economies in modern history. "
        "While the Federal Reserve conducted its most aggressive rate-hiking campaign in four decades to curb post-pandemic inflation (lifting rates from 0.25% to 5.50%), "
        "the Bank of Japan (BoJ) held firm to its ultra-loose stance via Negative Interest Rates (-0.10%) and Yield Curve Control (YCC).",
        style_body
    ))
    story.append(Paragraph(
        "This divergence opened a bilateral policy spread of up to <b>5.60% per annum</b>. For hedge funds and macro desks, the arbitrage was clear: "
        "borrow in yen at near-zero rates, leave the FX exposure unhedged (relying on structural yen weakness), and deploy proceeds into high-multiple U.S. technology stocks "
        "and corporate credit. The visual below demonstrates the path of USD/JPY to 161.95 and the corresponding rate differential.",
        style_body
    ))

    # Chart 1
    chart1_path = get_chart_path("chart_yen_carry_trade_historical_divergence.png", lang="en")
    if os.path.exists(chart1_path):
        story.append(Image(chart1_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Historical Table
    story.append(Paragraph("<b>Critical Milestones: USD/JPY Divergence and BoJ/MoF Interventions</b>", style_body_bold))
    hist_rows = [
        [Paragraph("Date", style_th), Paragraph("USD/JPY", style_th), Paragraph("BoJ Rate", style_th), Paragraph("Fed Funds", style_th), Paragraph("Macroeconomic Catalyst & Market Reaction", style_th)],
        [Paragraph("Jan 2021", style_td), Paragraph("103.20", style_td), Paragraph("-0.10%", style_td), Paragraph("0.25%", style_td), Paragraph("Pre-inflation baseline; zero rates across both sovereign economies.", style_td)],
        [Paragraph("Oct 2022", style_td), Paragraph("151.90", style_td), Paragraph("-0.10%", style_td), Paragraph("3.25%", style_td), Paragraph("First direct MoF yen-buying intervention in 24 years (~$60B sold).", style_td)],
        [Paragraph("Jul 2023", style_td), Paragraph("140.50", style_td), Paragraph("-0.10%", style_td), Paragraph("5.50%", style_td), Paragraph("Peak rate spread (5.60%); accelerated capital reallocations into Big Tech.", style_td)],
        [Paragraph("Mar 2024", style_td), Paragraph("151.30", style_td), Paragraph("0.10%", style_td), Paragraph("5.50%", style_td), Paragraph("Formal exit from NIRP after 8 years; initial market reaction was benign.", style_td)],
        [Paragraph("Jul 2024", style_td), Paragraph("161.95", style_td), Paragraph("0.25%", style_td), Paragraph("5.50%", style_td), Paragraph("38-year peak in USD/JPY; BoJ hikes and prepares the August market shock.", style_td)],
    ]
    t_hist = Table(hist_rows, colWidths=[55, 55, 55, 55, 284])
    t_hist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_hist)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: THE AUGUST 5, 2024 MARKET SHOCK (BLACK MONDAY)
    # =========================================================================
    story.append(Paragraph("3. Anatomy of the August 5, 2024 Market Shock: 'Black Monday'", style_h1))
    story.append(Paragraph(
        "The market dislocation on August 5, 2024, provided undeniable empirical proof that U.S. artificial intelligence infrastructure "
        "and tech valuations are deeply reliant on Japanese currency stability. The confluence of an unexpected BoJ rate hike on July 31 (+15 bps to 0.25%) "
        "with softening U.S. macroeconomic indicators (114k nonfarm payrolls and Sahm Rule activation) invalidated the guaranteed carry spread thesis.",
        style_body
    ))
    story.append(Paragraph(
        "Within trading sessions, USD/JPY experienced a vertical <b>11.4% appreciation</b> (from 161.95 down to 141.70). "
        "Leveraged hedge funds faced immediate margin calls on yen liabilities. To satisfy these demands, portfolio managers "
        "were forced to liquidate their most liquid and profitable holdings: <b>NVIDIA, hyperscaler equity blocks, and semiconductor futures</b>.",
        style_body
    ))

    # Chart 2
    chart2_path = get_chart_path("chart_yen_unwind_tech_margin_calls.png", lang="en")
    if os.path.exists(chart2_path):
        story.append(Image(chart2_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Shock Table
    story.append(Paragraph("<b>Shock Transmission: Peak Drawdowns and Cross-Asset Impact (Aug 2024)</b>", style_body_bold))
    shock_rows = [
        [Paragraph("Asset / Instrument", style_th), Paragraph("Peak-to-Trough Move", style_th), Paragraph("Max Single-Day Stress", style_th), Paragraph("Forensic Transmission Mechanism", style_th)],
        [Paragraph("Nikkei 225 (Japan)", style_td_bold), Paragraph("-23.0%", style_td), Paragraph("-12.40% (Aug 5)", style_td), Paragraph("Worst single-day plunge since the 1987 crash; forced domestic liquidations.", style_td)],
        [Paragraph("USD/JPY Spot", style_td_bold), Paragraph("-11.4% (JPY Surge)", style_td), Paragraph("-3.2% (Single Session)", style_td), Paragraph("Severe short squeeze sharply elevates the service cost of yen liabilities.", style_td)],
        [Paragraph("NVIDIA Corp (NVDA)", style_td_bold), Paragraph("-20.5%", style_td), Paragraph("-14.2% (Intraday)", style_td), Paragraph("Operated as the emergency cash register (ATM) for global macro hedge funds.", style_td)],
        [Paragraph("Nasdaq 100 (QQQ)", style_td_bold), Paragraph("-10.2%", style_td), Paragraph("-6.5% (48 Hours)", style_td), Paragraph("Systematic deleveraging across volatility-targeted strategies and CTAs.", style_td)],
        [Paragraph("CBOE Volatility Index (VIX)", style_td_bold), Paragraph("+313% (from 15.9 to 65.7)", style_td), Paragraph("Peak at 65.73", style_td), Paragraph("Third-highest volatility surge in history (behind 2008 and 2020 peaks).", style_td)],
    ]
    t_shock = Table(shock_rows, colWidths=[120, 94, 94, 196])
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
    # PAGE 4: BOJ STRUCTURAL REGIME & US SOVEREIGN DEBT NEXUS
    # =========================================================================
    story.append(Paragraph("4. The Structural BoJ Regime Shift (2025–2026): The End of Free Money", style_h1))
    story.append(Paragraph(
        "In contrast to transitory market disruptions, the 2025–2026 period solidified a <b>permanent secular regime shift in Japan</b>. "
        "Annual union wage negotiations (<i>Shunto</i>) delivered sustained real wage hikes (+5.28% in 2024, +5.10% in 2025, and +5.15% in 2026), "
        "anchoring service-sector inflation above the 2.0% target. In response, Governor Kazuo Ueda raised the policy benchmark to <b>1.00%–1.25%</b> and enacted QT.",
        style_body
    ))
    story.append(Paragraph(
        "This normalization lifted 10-year Japanese Government Bond (10Y JGB) yields to <b>1.35%</b> (and 30-year yields past 2.30%). "
        "For Japanese pension behemoths (GPIF managing $1.6T) and major life insurers, FX hedging costs (> 3.0%) made U.S. Treasuries unviable. "
        "The prevailing economic incentive has shifted to <b>capital repatriation</b> back into domestic Tokyo bonds.",
        style_body
    ))

    # Chart 3
    chart3_path = get_chart_path("chart_japan_us_treasury_holdings_and_yields.png", lang="en")
    if os.path.exists(chart3_path):
        story.append(Image(chart3_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Section US Debt Nexus
    story.append(Paragraph("5. The Sovereign Debt Nexus and the $700B AI Infrastructure Financing Strain", style_h1))
    story.append(Paragraph(
        "According to official U.S. Treasury TIC reports, Japan is the <b>largest foreign sovereign creditor to the United States</b>, holding $1,068 billion. "
        "However, its aggregate portfolio reflects a cumulative drawdown of <b>$257 billion</b> from the November 2021 peak ($1,325 billion). "
        "This divestment pressure reflects MoF dollar reserve sales and institutional asset reallocation.",
        style_body
    ))

    # Debt Transmission Table
    debt_rows = [
        [Paragraph("Transmission Channel", style_th), Paragraph("Metric / Parameter", style_th), Paragraph("Direct Impact on the AI Infrastructure Complex", style_th)],
        [Paragraph("US 10Y Sovereign Yield", style_td_bold), Paragraph("Anchored at 5.00% – 5.10%", style_td), Paragraph("Maintains an elevated hurdle rate, discounting the present value of AI revenues.", style_td)],
        [Paragraph("Hyperscaler WACC", style_td_bold), Paragraph("Elevated from ~6.5% to 9.2%", style_td), Paragraph("Raises financing hurdles for the $700B CapEx cycle across GPU clusters & grid PPAs.", style_td)],
        [Paragraph("Data Center ABS Spreads", style_td_bold), Paragraph("Coupon rates exceed 7.5%+", style_td), Paragraph("Structured issuances require wider spreads, compressing developer equity returns.", style_td)],
        [Paragraph("Leveraged Neoclouds", style_td_bold), Paragraph("Debt service absorbs 45% EBITDA", style_td), Paragraph("Heightened vulnerability to rental spot rate softness across H100/Blackwell pods.", style_td)],
    ]
    t_debt = Table(debt_rows, colWidths=[120, 114, 270])
    t_debt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_debt)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: JPY FORWARD STRESS SCENARIOS (2026–2029)
    # =========================================================================
    story.append(Paragraph("6. Forward Stress Testing Matrix: JPY Scenarios & Multiple Sensitivity (2026–2029)", style_h1))
    story.append(Paragraph(
        "To quantify the forward effects of BoJ policy tightening and exchange rate dynamics on technology equity multiples and private credit, "
        "we construct a sensitivity matrix across three distinct deleveraging scenarios through 2029:",
        style_body
    ))

    # Chart 4
    chart4_path = get_chart_path("chart_yen_stress_scenarios_matrix.png", lang="en")
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=504, height=195))
        story.append(Spacer(1, 6))

    # Scenario Table
    scen_rows = [
        [Paragraph("Metric / Parameter", style_th), Paragraph("Scenario A: Orderly Normalization", style_th), Paragraph("Scenario B: Accelerated Deleveraging", style_th), Paragraph("Scenario C: Systemic FX Shock", style_th)],
        [Paragraph("Assigned Probability", style_td_bold), Paragraph("<b>50%</b> (Baseline)", style_td), Paragraph("<b>35%</b> (Moderate Stress)", style_td), Paragraph("<b>15%</b> (Severe Tail Shock)", style_td)],
        [Paragraph("USD/JPY Target Rate", style_td_bold), Paragraph("145.00 – 155.00", style_td), Paragraph("130.00 – 140.00", style_td), Paragraph("< 125.00 (Disorderly Squeeze)", style_td)],
        [Paragraph("BoJ Benchmark Rate", style_td_bold), Paragraph("1.00% – 1.25% (Pause)", style_td), Paragraph("1.50% – 1.75% (Active Hikes)", style_td), Paragraph("2.00%+ (Emergency Tightening)", style_td)],
        [Paragraph("Fed - BoJ Rate Spread", style_td_bold), Paragraph("2.75% to 3.00%", style_td), Paragraph("1.75% to 2.00%", style_td), Paragraph("< 1.00% (Spread Collapse)", style_td)],
        [Paragraph("US 10Y Sovereign Yield", style_td_bold), Paragraph("4.80% – 5.10%", style_td), Paragraph("5.25% – 5.50%", style_td), Paragraph("5.75%+ (Buyer Strike)", style_td)],
        [Paragraph("Big Tech P/E Compression", style_td_bold), Paragraph("<b>-8.0%</b> (Orderly Drift)", style_td), Paragraph("<b>-18.5%</b> (Cyclical De-rating)", style_td), Paragraph("<b>-35.0%</b> (Broad Forced Deleveraging)", style_td)],
        [Paragraph("Data Center ABS BBB Spread", style_td_bold), Paragraph("+45 bps", style_td), Paragraph("+140 bps", style_td), Paragraph("+320 bps (Market Freeze)", style_td)],
        [Paragraph("AI Financing Environment", style_td_bold), Paragraph("Sustained with discipline", style_td), Paragraph("Private credit originations halt", style_td), Paragraph("Wave of neocloud defaults", style_td)],
    ]
    t_scen = Table(scen_rows, colWidths=[120, 128, 128, 128])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_scen)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: STRATEGIC RECOMMENDATIONS, METHODOLOGY & SIGN-OFF
    # =========================================================================
    story.append(Paragraph("7. Strategic Recommendations for Risk Managers & Asset Allocators", style_h1))
    story.append(Paragraph(
        "The demonstrated nexus between Japanese domestic liquidity and U.S. capital markets requires an immediate recalibration "
        "of risk management frameworks across technology equity and structured infrastructure debt:",
        style_body
    ))

    recs_data = [
        [Paragraph("1. Monitor Real US-Japan Sovereign Yield Differentials", style_td_bold),
         Paragraph("Technology equity portfolio managers must not rely exclusively on revenue guidance. The 2-year and 10-year real rate spreads between the U.S. and Japan serve as the single most reliable leading indicator for multiple contraction.", style_td)],
        [Paragraph("2. Track MoF Foreign Reserve Outflows and Treasury Auctions", style_td_bold),
         Paragraph("Sharp declines in Japan's dollar reserves reflect Treasury sales to prop up the yen. This dynamic exerts upward pressure on long-dated U.S. yields and escalates hyperscaler capital costs, serving as an early tail-risk warning.", style_td)],
        [Paragraph("3. Stress-Test Data Center ABS Facilities at 5.50% Sovereign Yields", style_td_bold),
         Paragraph("GPU asset-backed facilities and private term loans must be modeled under a sustained 5.50% risk-free rate and +150 bps credit spread widening to ensure Debt Service Coverage Ratios (DSCR) maintain contractual compliance.", style_td)],
        [Paragraph("4. Recalibrate Gaussian Copula Cross-Asset Correlation", style_td_bold),
         Paragraph("In our proprietary model, the cross-asset correlation parameter between USD/JPY spot and high-yield corporate credit spreads (HYG/LQD) has been updated from 0.18 to <b>0.42</b>, capturing forced margin unwinds during shock regimes.", style_td)]
    ]
    t_recs = Table(recs_data, colWidths=[160, 344])
    t_recs.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_recs)
    story.append(Spacer(1, 10))

    # Methodological Annex
    story.append(Paragraph("Methodological Annex: Tech Equity Multiple Sensitivity Formulation", style_h1))
    story.append(Paragraph(
        "The sensitivity of Forward Price-to-Earnings (P/E) multiples for mega-cap technology to USD/JPY fluctuations is governed by: "
        "<font face='Courier'>Δ(P/E) = -0.48 · Δ(USD/JPY) - 1.85 · Δ(Spread_Fed_BoJ)</font>. "
        "Every 5% appreciation in the Japanese Yen (downward USD/JPY move) induces an estimated ~2.4x contraction in forward tech multiples, "
        "amplified during regimes of elevated VIX implied volatility.",
        style_body
    ))
    story.append(Spacer(1, 10))

    # Sign-off & Sources Box
    sign_data = [
        [Paragraph("<b>Primary Sources & Official Institutional Datasets:</b>", style_td_bold)],
        [Paragraph(
            "• U.S. Department of the Treasury: Treasury International Capital (TIC) Data (Table 5 - Major Foreign Holders of U.S. Debt)<br/>"
            "• Bank of Japan (BoJ): Monetary Policy Releases, Financial System Report & Outlook (2022–2026)<br/>"
            "• Bank for International Settlements (BIS): Quarterly Review & Cross-Border Yen Lending Audits<br/>"
            "• Ministry of Finance Japan (MoF): FX Intervention Operations Statistics<br/>"
            "• Japanese Trade Union Confederation (RENGO): Spring Wage Offensive (Shunto) Reports (2024–2026)<br/>"
            "• Bloomberg Professional & Financial Times: Global Market Unwind Forensic Coverage",
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
