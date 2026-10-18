#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_macro_geopolitical_crash_report_en.py
----------------------------------------------
Generates the Institutional English Executive Report (10 pages):
'Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028_EN.pdf'
US Fiscal Condition, Elections, Wars, Market Crash Composition, and Global Vulnerability Map.
"""

import os
import sys
import numpy as np
import geopandas as gpd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# Import computational models, constants, and data from main module
from generate_macro_geopolitical_crash_report import (
    FACTS, SCENARIOS, ATTRIB, FACTOR_WEIGHTS, FACTOR_NAMES,
    REGION_PT, BASE_RATE_BEAR_2Y, OVERLAY,
    REPORT_DATE, HERE, GEOJSON,
    compute_derived_metrics, compute_country_scores
)

COUNTRY_EN = {
    "JPN": "Japan", "IRN": "Iran", "TWN": "Taiwan", "KOR": "South Korea",
    "PSX": "Palestine", "ISR": "Israel", "IRQ": "Iraq", "PAK": "Pakistan",
    "TUR": "Turkey", "LKA": "Sri Lanka", "EGY": "Egypt", "IND": "India",
    "CHN": "China", "FRA": "France", "GBR": "United Kingdom", "USA": "United States",
    "BGD": "Bangladesh", "SYR": "Syria", "LBN": "Lebanon", "YEM": "Yemen",
    "KWT": "Kuwait", "QAT": "Qatar", "ARG": "Argentina", "BRA": "Brazil",
    "DEU": "Germany", "ITA": "Italy", "UKR": "Ukraine", "RUS": "Russia"
}

FACTOR_NAMES_EN = {
    "E": "Energy Shock / Hormuz",
    "F": "Fiscal Stress & Sovereign Yields",
    "X": "Strong USD & External Financing",
    "T": "Tech & Taiwan Semiconductor Chain",
    "M": "US Market & Credit Contagion",
    "G": "Direct Geopolitical Conflict"
}

class NumberedCanvasEN(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(n)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.8)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(54, 750, "MACRO & GEOPOLITICS • MARKET CRASH RISK 2026-2028")
            self.setFont("Helvetica", 7.6)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "US FISCAL SPIRAL • ELECTIONS • GLOBAL VULNERABILITY MAP")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential Risk Analysis • Empirical Data as of Oct 11, 2026 • Probabilities Reflect Analytical Modeling")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

from utils_paths import get_chart_path, get_report_en_path
def _img(path, width_in):
    p = get_chart_path(os.path.basename(path), lang="en")
    iw, ih = ImageReader(p).getSize()
    w = width_in * inch
    return Image(p, width=w, height=w * ih / iw)

def build_pdf_report_en(d, rows, ranking, output_filename="Report_Macro_Geopolitics_Market_Crash_2026_2028.pdf"):
    f = FACTS
    doc = SimpleDocTemplate(get_report_en_path(output_filename), pagesize=letter, leftMargin=54, rightMargin=54,
                            topMargin=54, bottomMargin=54)
    ss = getSampleStyleSheet()
    S = {}
    S['title'] = ParagraphStyle('t', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=16.5, leading=20.5,
                                textColor=colors.HexColor('#0F172A'))
    S['sub'] = ParagraphStyle('s', parent=ss['Normal'], fontName='Helvetica', fontSize=9, leading=12.5,
                              textColor=colors.HexColor('#475569'))
    S['h1'] = ParagraphStyle('h1', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=11.5, leading=14.5,
                             textColor=colors.HexColor('#1E3A8A'), spaceAfter=4, spaceBefore=5)
    S['body'] = ParagraphStyle('b', parent=ss['Normal'], fontName='Helvetica', fontSize=8.1, leading=11.8,
                               textColor=colors.HexColor('#334155'), spaceAfter=4)
    S['bold'] = ParagraphStyle('bb', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=8.1, leading=11.8,
                               textColor=colors.HexColor('#0F172A'), spaceAfter=3)
    S['call'] = ParagraphStyle('c', parent=ss['Normal'], fontName='Helvetica-Oblique', fontSize=7.8, leading=11.2,
                               textColor=colors.HexColor('#1E293B'))
    S['th'] = ParagraphStyle('th', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=7.3, leading=9.6,
                             textColor=colors.white)
    S['td'] = ParagraphStyle('td', parent=ss['Normal'], fontName='Helvetica', fontSize=7.0, leading=9.5,
                             textColor=colors.HexColor('#1E293B'))
    S['cap'] = ParagraphStyle('cap', parent=ss['Normal'], fontName='Helvetica-Oblique', fontSize=6.8, leading=9,
                              textColor=colors.HexColor('#64748B'), spaceAfter=4)

    P = lambda t, st='body': Paragraph(t, S[st])

    def table(data, widths, header=True, valign='MIDDLE', zebra=True):
        t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
        style = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), valign),
        ]
        if header:
            style.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')))
        if zebra:
            style.append(('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]))
        t.setStyle(TableStyle(style))
        return t

    def box(text, bg, border, st='call'):
        t = Table([[Paragraph(text, S[st])]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg)), ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(border)),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7)]))
        return t

    def h1(text):
        return [P(text, 'h1'), HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'),
                                          spaceAfter=5, spaceBefore=0)]

    story = []

    # ================= PAGE 1: COVER =================
    hdr = Table([[Paragraph("<b>STRATEGIC REPORT: US FISCAL CONDITION, ELECTIONS, WARS &amp; CRASH RISK</b>",
                            ParagraphStyle('hh', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#DC2626'))),
                  Paragraph(f"Date: October 11, 2026 | Horizon: Oct/2026 - Oct/2028",
                            ParagraphStyle('hd', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))]],
                colWidths=[310, 194])
    hdr.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    story += [hdr, Spacer(1, 4)]
    story.append(P("Anatomy of a Potential Market Crash (2026-2028) &amp; Global Vulnerability Map", 'title'))
    story.append(Spacer(1, 2))
    story.append(P("US Government Financial Standing, Electoral Cycle Influences, Kinetic Wars, and Global Contagion Channels, "
                   "Synthesizing Primary Official Datasets Observed on October 11, 2026", 'sub'))
    story.append(Spacer(1, 6))

    def kpi(title, big, small, col):
        return Paragraph(f"<b>{title}</b><br/><font size=9.5 color='{col}'><b>{big}</b></font><br/>"
                         f"<font size=6.2 color='#475569'>{small}</font>", S['td'])
    k1 = [kpi("FEDERAL DEBT", f"${f['debt_total_tn']:.2f} Trillion", "Treasury, Oct 8, 2026", '#1E3A8A'),
          kpi("FY26 DEFICIT", f"${f['deficit_fy26_tn']:.1f} Trillion", f"{f['deficit_fy26_pct']}% of GDP", '#DC2626'),
          kpi("NET INTEREST", "$1.0-1.1 Trillion", "3.3-3.4% of GDP / year", '#F59E0B'),
          kpi("10Y / 30Y YIELDS", f"{f['ust10']}% / {f['ust30_auction']}%", "30Y: Highest since 2002", '#7C3AED'),
          kpi("FED FUNDS", f"{f['fed_low']:.2f}-{f['fed_high']:.2f}%", "Hiked 25 bps on Sep 16", '#475569')]
    k2 = [kpi("S&P 500 / VIX", f"{f['spx']:,.0f} / {f['vix']}", "Near All-Time Record High", '#0D9488'),
          kpi("SHILLER CAPE", f"~{f['cape']:.0f}x", "2nd Highest Ever (1999: 44x)", '#DC2626'),
          kpi("BRENT CRUDE", f"> ${f['brent']} / bbl", "US-Israel vs Iran, Month 8", '#EA580C'),
          kpi("CPI / UNEMPLOYMENT", f"{f['cpi_aug']}% / {f['unemp']}%", f"Sep Payrolls: +{f['payroll_sep_k']}k", '#B91C1C'),
          kpi("SPOT GOLD", f"${f['gold']:,.0f} / oz", "Oct 8-9, 2026 Record", '#B45309')]
    kt = Table([k1, k2], colWidths=[100.8] * 5)
    kt.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
                            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
                            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                            ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    story += [kt, Spacer(1, 6)]

    story.append(box(
        "<b>EXECUTIVE SUMMARY:</b> The US equity market trades near historic highs (VIX at "
        f"{f['vix']}) even as structural macro fundamentals have severely deteriorated: <b>(1)</b> the US government runs an annualized deficit of "
        f"{f['deficit_fy26_pct']}% of GDP outside a recession and total debt stands at ${f['debt_total_tn']:.1f}T; <b>(2)</b> the Federal Reserve is "
        "<b>hiking rates</b> amid 3.4-3.7% inflation and a softening labor market (+29k payrolls), severely limiting the traditional 'Fed put'; "
        f"<b>(3)</b> the earnings yield of the S&P 500 ({d['earnings_yield']:.2f}%) has fallen <b>below</b> 10-year Treasury yields ({f['ust10']}%); "
        "<b>(4)</b> active kinetic war impairs ~20% of global seaborne oil and LNG; and <b>(5)</b> midterm elections and an intense 4-week catalyst window "
        "cluster systemic triggers. Our consolidated model estimates a <b>probability of a 20%+ S&P 500 drawdown within 2 years of "
        f"~{d['p_ge20']:.0f}%</b> (historical Poisson base rate ~{BASE_RATE_BEAR_2Y:.0f}%), and a <b>~{SCENARIOS[3][3]:.0f}% chance</b> of a systemic crash "
        "(>35% drawdown). The most exposed economies include Japan/Korea/Taiwan, net energy-importing South Asia, Middle Eastern combatants, "
        "Turkey/Egypt, high-debt European sovereigns, and the US in absolute wealth loss.",
        '#EFF6FF', '#93C5FD'))
    story.append(Spacer(1, 6))

    story += h1("Key Methodological Evolutions vs. Prior Repository Dossiers")
    chg = [[P("<b>Prior Assumption</b>", 'th'), P("<b>Empirical Facts (10/11/2026)</b>", 'th'), P("<b>Analytical Implication</b>", 'th')],
           [P("US National Debt modeled at ~$40T", 'td'),
            P(f"<b>Confirmed:</b> ${f['debt_total_tn']:.2f}T gross ($ {f['debt_public_tn']:.2f}T held by public).", 'td'),
            P("Trajectory confirmed; higher terminal rates compound fiscal servicing.", 'td')],
           [P("'Fed Funds at 5.25%' with rapid rate-cut capacity", 'td'),
            P(f"10Y = 5.24%, but <b>Fed Funds at 3.75-4.00% following Sep 2026 HIKE</b> with CPI reaccelerating.", 'td'),
            P("The 'Fed Put' is strictly constrained by stagflation risks.", 'td')],
           [P("Immediate Treasury auction failure as Scenario 3 trigger", 'td'),
            P(f"Oct 8 30Y auction cleared with <b>solid</b> absorption (bid-to-cover {f['btc_30y']}, indirects {f['indirect_30y']}%) at {f['ust30_auction']}%.", 'td'),
            P("Auction demand clears, but at punishingly high term premia.", 'td')],
           [P("3 scenarios, all assuming market corrections", 'td'),
            P("Model incorporates S0 (benign volatile continuation) over a 2-year horizon.", 'td'),
            P("Eliminates bear bias: P(Drawdown >= 20%) over 24 months = " + f"{d['p_ge20']:.0f}%.", 'td')],
           [P("Sole analytical focus on AI / Private Credit", 'td'),
            P("Expanded vectors: Hormuz energy crisis, Yen carry trade, $13T hedge fund sector, office CRE, and European spreads.", 'td'),
            P("Risk architecture is broadly <b>macro-financial</b>, not isolated to tech.", 'td')]]
    story.append(table(chg, [130, 215, 159], valign='TOP'))
    story.append(PageBreak())

    # ================= PAGE 2: FISCAL DYNAMICS =================
    story += h1("1. US Government Financial Condition: The Debt Refinancing Spiral")
    story.append(P(
        f"The US Department of the Treasury reports total gross debt of <b>${f['debt_total_tn']:.2f} Trillion</b> (as of 10/08/2026), with "
        f"<b>${f['debt_public_tn']:.2f} Trillion</b> held by the public (~{d['debt_gdp_calc']:.0f}% of GDP; CBO baseline: "
        f"{f['debt_gdp_2026']}% in 2026, heading to {f['debt_gdp_2036']}% by 2036). The FY2026 deficit closed at ~$2.0 Trillion "
        f"(6.2% of GDP). <b>Net interest expenses ($1.0-1.1 Trillion)</b> already surpass total National Defense and Medicare expenditures.", 'body'))
    story.append(_img("chart_us_fiscal_dashboard.png", 6.8))
    story.append(P("Sources: Treasury Fiscal Data (Debt to the Penny), CBO, CRFB, American Action Forum, FOMC, YCharts/TradingEconomics.", 'cap'))
    story.append(P("<b>Macro-Fiscal Diagnosis:</b>", 'bold'))
    story.append(P(
        "• <b>Structural Deficit Outside Recessions:</b> 6.2% of GDP deficit at full employment (4.2% U-3) means the federal budget lacks counter-cyclical buffers. "
        "In a severe recession, tax receipts plunge and the deficit would breach $3 Trillion annually.<br/>"
        f"• <b>Refinancing Arithmetic:</b> The effective interest rate on debt held by the public is ~{d['effective_rate']:.1f}%, while new 30-year paper "
        f"clears at {f['ust30_auction']}%. Every sustained +100 bps shift adds ~${d['plus100bp_bn']:.0f} Billion annually to interest outlays as intermediate paper matures.<br/>"
        f"• <b>Retreat of Foreign Sovereign Buyers:</b> Japan holds ${f['japan_ust_tn']:.2f} Trillion (July 2026) and is paring holdings to defend the yen; "
        f"China reduced positions to ~${f['china_ust_tn']*1000:.0f} Billion. Custodian centers (UK, Cayman, Canada) have absorbed supply, but demand is price-sensitive.<br/>"
        "• <b>Federal Reserve Under Political Heat:</b> Kevin Warsh assumed the Chairmanship on 05/22/2026. Public friction with the administration has escalated, "
        "while Jerome Powell remains on the Board of Governors until 01/31/2028. Perceptions of institutional politicization expand sovereign term premia.<br/>"
        "• <b>Important Mitigant:</b> The October 8 30Y auction cleared with strong bid-to-cover (2.54); capital markets continue to absorb issuance at market rates.",
        'body'))
    story.append(PageBreak())

    # ================= PAGE 3: EQUITIES VS RATES =================
    story += h1("2. US Equity Markets: Valuations, Long Yields, and Concentration")
    story.append(P(
        f"The S&P 500 closed at {f['spx']:,.2f} and Nasdaq at {f['ixic']:,.2f} (10/09/2026), hovering near record highs. Fundamental valuation multiples "
        f"stand at extremes matched only in late 1999: <b>Shiller CAPE ~{f['cape']:.0f}x</b> (1999 peak: 44.2x), <b>Buffett Indicator ~{f['buffett_pct']}% of GDP</b>, and "
        f"<b>Top-10 index weighting at {f['top10_weight']}%</b> (Nvidia, Apple, and Microsoft alone represent >{f['top3_weight']}% of total capitalization).",
        'body'))
    story.append(_img("chart_valuation_vs_rates.png", 6.8))
    story.append(P("CAPE values at historic peaks reflect Yale University series (Robert Shiller). Earnings yield derived from 23.4x forward P/E.", 'cap'))
    story.append(P("<b>Three Critical Valuation Readings:</b>", 'bold'))
    story.append(P(
        f"1. <b>Negative Equity Risk Premium:</b> The forward earnings yield ({d['earnings_yield']:.2f}%) sits {abs(d['erp_vs_10y']):.2f} pp below 10-year "
        f"Treasury yields ({f['ust10']}%). Real 10Y yields stand at ~{d['real_10y']:.1f}% (10Y minus {f['cpi_aug']}% CPI). Equity allocators are earning less "
        "than risk-free paper, relying fully on unhindered forward profit expansion.<br/>"
        f"2. <b>Bear-Steepening Curve Pressures:</b> 10-year yields trade {d['curve_10y_ff']:.2f} pp above the Fed Funds midpoint. The market demands heavy term premia "
        "driven by fiscal supply and persistent inflation, operating outside direct central bank control.<br/>"
        "3. <b>Degraded Underlying Breadth:</b> A substantial share of index components trade below their 50-day moving averages with negative year-to-date returns: "
        "market gains are heavily reliant on a handful of mega-caps, leaving indices fragile to single-sector shocks.",
        'body'))
    story.append(box(
        f"<b>Interpreting the VIX at 14.84:</b> A sub-15 VIX amid active kinetic war, 30Y yields at 5.6%, and CAPE at 41x indicates that the options market prices "
        "a benign soft landing. This does not predict an immediate drop, but it strips away cheap hedging protection and intensifies downside convexity: "
        "in 2000, 2008, and 2022, equity volatility traded at subdued levels prior to the onset of severe drawdowns.",
        '#FFFBEB', '#FCD34D'))
    story.append(PageBreak())

    # ================= PAGE 4: ELECTIONS =================
    story += h1("3. The Influence of Elections and the Political Calendar")
    story.append(P(
        "Historical market data demonstrates that <b>midterm election years are the most volatile phase of the US presidential cycle</b> "
        "(S&P 500 average gain of ~3-5%, with average intra-year drawdowns of ~17-19% vs. ~12-13% in non-midterm years), typically followed by "
        "<b>strong 12-month post-election rallies</b> (averaging ~13-16%). In 2026, seasonal weakness was bypassed due to the AI capex boom. "
        "This suggests that election-related volatility was deferred into Q4, or neutralized by generative AI capex.", 'body'))
    story.append(_img("chart_triggers_timeline.png", 6.8))
    story.append(P("<b>Political Catalysts and Macro Calendar (2026–2028):</b>", 'bold'))
    el = [[P("<b>Electoral Event</b>", 'th'), P("<b>Date</b>", 'th'), P("<b>Market Transmission Channel</b>", 'th'),
           P("<b>Projected Market Impact</b>", 'th')],
          [P("US Midterm Elections", 'td'), P("11/03/2026", 'td'),
           P("Democrats favored to retake House; Senate (53-47 R) fiercely contested. Divided government halts major legislative fiscal packages, "
             "escalating oversight probes and debt ceiling brinkmanship in early 2027.", 'td'),
           P("Clearing uncertainty helps; fiscal gridlock elevates term premia", 'td')],
          [P("Pre-Election Geopolitical Escalation", 'td'), P("Oct-Nov 2026", 'td'),
           P("Reports of tactical strike planning against Iranian nodes ahead of polls; Trump-Putin diesel accord announced to curb pump prices. "
             "Energy costs remain central to voting sentiment.", 'td'),
           P("Severe oil price volatility and headline inflation shocks", 'td')],
          [P("Brazil Presidential Runoff", 'td'), P("10/25/2026", 'td'),
           P(f"Flávio Bolsonaro surprised in round 1 (Ibovespa ~+8%, Real ~+4%). Public debt at ~{f['brazil_debt_gdp']}% of GDP, "
             f"interest costs at {f['brazil_interest_gdp']}% of GDP, Selic at {f['brazil_selic']}%.", 'td'),
           P("Emerging market FX volatility and regional capital flows", 'td')],
          [P("UK Autumn Budget", 'td'), P("10/28/2026", 'td'),
           P(f"UK 30Y Gilt yield at ~{f['gilt30']}% (highest since 1998); sovereign fiscal discipline under scrutiny.", 'td'),
           P("Cross-border contagion across global sovereign bond yields", 'td')],
          [P("French Presidential Election", 'td'), P("Apr-May 2027", 'td'),
           P(f"OAT-Bund spread at ~{f['fr_bund_bp']} bps (highest since 2011-12); severe budget deficit and political polarization; ECB TPI activation untested.", 'td'),
           P("Epicenter of Eurozone sovereign debt stress", 'td')],
          [P("US Presidential Election", 'td'), P("11/07/2028", 'td'),
           P("Positions beyond 2-year horizon; however, campaign dynamics will amplify fiscal spending promises and Fed jawboning starting late 2027.", 'td'),
           P("Expansion of long-term sovereign term premia", 'td')]]
    story.append(table(el, [95, 55, 250, 104], valign='TOP'))
    story.append(PageBreak())

    # ================= PAGE 5: WARS & GEOPOLITICS =================
    story += h1("4. Geopolitical Conflicts: The Four Theaters of Systemic Risk")
    story.append(P(
        "Active kinetic conflicts impact global capital markets across four distinct vectors: <b>energy &amp; headline inflation</b> "
        "(constraining central bank easing), <b>supply-chain bottlenecks</b> (semiconductors), <b>capital repatriation</b> (flight to dollar liquidity), "
        "and <b>sovereign fiscal burdens</b> (defense appropriations).", 'body'))
    war = [[P("<b>Conflict Theater</b>", 'th'), P("<b>Operational Status (Oct 2026)</b>", 'th'), P("<b>Transmission Channel</b>", 'th'),
            P("<b>Capital Market Severity</b>", 'th')],
           [P("<b>US-Israel vs. Iran &amp; Strait of Hormuz</b>", 'td'),
            P("Kinetic war in 8th month. ~20% of global petroleum and LNG flows transit Hormuz; commercial tanker attacks at peak frequency; "
              f"Brent crude > ${f['brent']}/bbl; OECD commercial stocks at multi-decade lows; coordinated strategic reserve releases show fading impact; "
              "refinery crack spreads near historic highs.", 'td'),
            P("Energy inflation, sustained higher policy rates, corporate margin compression, and wide current-account deficits across Asia and Europe.", 'td'),
            P("<font color='#DC2626'><b>VERY HIGH</b></font><br/>(Active shock)", 'td')],
           [P("<b>Russia vs. Ukraine War</b>", 'td'),
            P("Ukrainian deep-strike drones disrupt Russian domestic refining; regional diesel crunches; Trump-Putin fuel pact met with market skepticism.", 'td'),
            P("Distillate supply constraints; European energy security; expanded Western defense budgets.", 'td'),
            P("<font color='#D97706'><b>HIGH</b></font><br/>(Chronic pressure)", 'td')],
           [P("<b>China-Taiwan Strait Tensions</b>", 'td'),
            P(f"Trump-Xi trade truce extended; China institutionalizes maritime 'quarantines'; direct military invasion assessed as unlikely before 2028. "
              f"TSMC manufactures >{f['tsmc_adv_share']}% of advanced logic (<10nm) and 73% of pure-play foundry volume.", 'td'),
            P("Complete bottleneck for AI hardware (Nvidia, Apple, cloud hyperscalers), marine insurance spikes, bilateral embargoes.", 'td'),
            P("<font color='#B91C1C'><b>TAIL RISK</b></font><br/>(Low prob, extreme severity)", 'td')],
           [P("<b>Tariff Escalations &amp; Trade Friction</b>", 'td'),
            P("US-China tariffs remain under executive discretion; bilateral trade renegotiations ongoing.", 'td'),
            P("Imported input cost inflation, margin degradation, fragmented supply redundancy costs.", 'td'),
            P("<font color='#D97706'><b>MODERATE</b></font>", 'td')]]
    story.append(table(war, [90, 190, 150, 74], valign='TOP'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Causal Transmission from Kinetic War to Financial Disruption:</b>", 'bold'))
    story.append(box(
        "<b>High Oil / Distillates</b> ➔ <b>Headline CPI Spikes</b> (projected at 3.6-3.7% in Sep) ➔ <b>Fed Hikes Rates</b> (initiated 09/16/2026) "
        "despite softening payrolls ➔ <b>Long-End Yields Breach Multi-Decade Highs</b> (10Y at 5.24%, 30Y at 5.6%) ➔ <b>Equity Multiples and CRE Values Drop</b> ➔ "
        "<b>Acute Liquidity Freezes in Private Credit, Regional Banks ($396B CRE maturities), and Leveraged Hedge Funds</b> ➔ <b>Forced Margin Liquidations</b> ➔ "
        "Federal Reserve trapped between inflation defense and financial stability. This mirrors 1973-74 and 2022 dynamics, exacerbated by a 100%+ debt-to-GDP ratio.",
        '#FEF2F2', '#F87171'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Additional Macro Contagion Vectors Identified:</b>", 'bold'))
    story.append(P(
        f"• <b>Yen Carry Trade Unwind:</b> Japanese 10Y JGB yields at {f['jgb10']:.2f}%; domestic institutional investors face incentives to repatriate capital; "
        "rapid yen appreciation triggers margin-call liquidations across tech equities and emerging markets.<br/>"
        f"• <b>Non-Bank Financial Intermediation (Hedge Funds):</b> IMF Global Financial Stability Report (Oct 2026) flags ~${f['hedge_funds_tn']} Trillion "
        "in assets with concentrated gross leverage and correlated redemption structures transacting via prime brokers.<br/>"
        f"• <b>Private Credit and Office CRE:</b> Redemption gates across semi-liquid credit funds, amend-and-extend practices in AI software; "
        f"CMBS office delinquency at {f['cmbs_office_delinq']:.1f}% (surpassing 2008 peaks); ~${f['cre_maturity_bn']}B in CRE debt maturing in 2026, ~45% held by banks.<br/>"
        f"• <b>European Sovereign Spreads:</b> France (OAT-Bund spread ~{f['fr_bund_bp']} bps) and United Kingdom (30Y Gilt ~{f['gilt30']}%).", 'body'))
    story.append(PageBreak())

    # ================= PAGE 6: PROBABILITIES =================
    story += h1("5. Anatomy of a Market Crash: Probabilities over 2 Years (2026–2028)")
    story.append(P(
        f"We model the probability of a 20%+ drawdown in the S&P 500 across the Oct/2026 to Oct/2028 window starting from the <b>historical Poisson base rate of "
        f"~{BASE_RATE_BEAR_2Y:.0f}%</b> (12-13 bear markets since 1950, ~1 every 6 years) and adding explicit, auditable macro overlays. "
        f"The resulting consolidated probability is <b>~{d['overlay_total']:.0f}%</b>. These overlays represent structured institutional judgments:", 'body'))
    story.append(_img("chart_probability_buildup.png", 6.8))
    sc_rows = [[P("<b>Scenario</b>", 'th'), P("<b>Prob.</b>", 'th'), P("<b>Macro Description and Trigger Conditions</b>", 'th')],
               [P("<b>S0</b> Volatile Continuation<br/>(Max Drawdown < 10%)", 'td'), P("<b>27%</b>", 'td'),
                P("Middle East conflict stabilizes, AI profits beat elevated expectations, inflation ebbs in 2027 allowing Fed pause. Sovereign auctions clear smoothly.", 'td')],
               [P("<b>S1</b> Cyclical Multiple De-rating<br/>(Drawdown: -10% to -20%)", 'td'), P("<b>33%</b>", 'td'),
                P("10Y yields fluctuate between 5.0% and 5.8%, high energy costs; P/E multiple compresses from 23.4x to ~20x. Midterm seasonality. No systemic banking panic.", 'td')],
               [P("<b>S2</b> Cycle Bear Market &amp; Credit Strain<br/>(Drawdown: -20% to -35%)", 'td'), P("<b>25%</b>", 'td'),
                P("AI hardware capex digestion + 10Y yields breach 6% + private credit/CRE defaults. S&P 500 earnings contract ~9%, P/E drops to ~18x.", 'td')],
               [P("<b>S3</b> Systemic Financial Crash<br/>(Drawdown > 35%; Central -48%)", 'td'), P("<b>15%</b>", 'td'),
                P("Confluence: Long Treasury auction dislocation, yen carry unwind, hedge fund margin de-grossing, regional bank CRE failures, and Taiwan escalation. EPS drops ~16%, P/E compresses to ~14.5x.", 'td')]]
    story.append(table(sc_rows, [150, 40, 314], valign='TOP'))
    story.append(P(f"P(Drawdown >= 10%) = {d['p_ge10']:.0f}%  |  P(>= 20%) = {d['p_ge20']:.0f}%  |  P(> 35%) = {SCENARIOS[3][3]:.0f}%. "
                   "For comparison, prior dossiers estimated a 52% probability of moderate to severe correction over a 3-year horizon.", 'cap'))
    story.append(PageBreak())

    # ================= PAGE 7: COMPOSITION =================
    story += h1("6. Anatomy of a Crash: Channel Transmission Breakdown")
    story.append(P(
        "Equity Market Price = Forward P/E Multiple x Earnings per Share (EPS). For each scenario, we define valuation compression and earnings contraction "
        "(right chart) and allocate total drawdown across six core transmission channels (left chart). Total <b>wealth destruction</b> evaluates US equities at "
        f"~${d['equity_cap_tn']:.0f} Trillion (Buffett Indicator {f['buffett_pct']}% x GDP of ~${d['gdp_tn']:.0f}T).", 'body'))
    story.append(_img("chart_crash_composition.png", 6.8))
    s = d["scen"]
    story.append(P(
        f"<b>Interpretation:</b> In S3, the projected wealth loss of ~${s['S3']['loss_tn']:.0f} Trillion equals the entire gross federal debt (${f['debt_total_tn']:.0f}T). "
        "Transmission channels shift dynamically with severity: in S1, multiple compression and AI capex digestion drive 55% of losses; in S3, <b>credit deleveraging and liquidity freezes</b> "
        "become the largest individual contributor (28%) because leverage transforms corrections into systemic crashes. In S2/S3, classic 60/40 Treasury hedges fail initially as long yields rise with equities.",
        'body'))
    ass = [[P("<b>Market Indicator (Illustrative)</b>", 'th'), P("<b>Current</b>", 'th'), P("<b>S1</b>", 'th'), P("<b>S2</b>", 'th'), P("<b>S3</b>", 'th')],
           [P("S&P 500 (Peak to Trough)", 'td'), P(f"{f['spx']:,.0f}", 'td'), P(f"~{f['spx']*(1+s['S1']['total']/100):,.0f}", 'td'),
            P(f"~{f['spx']*(1+s['S2']['total']/100):,.0f}", 'td'), P(f"~{f['spx']*(1+s['S3']['total']/100):,.0f}", 'td')],
           [P("Central Drawdown / Wealth Loss", 'td'), P("-", 'td'), P(f"{s['S1']['total']:.0f}% / ${s['S1']['loss_tn']:.0f}T", 'td'),
            P(f"{s['S2']['total']:.0f}% / ${s['S2']['loss_tn']:.0f}T", 'td'), P(f"{s['S3']['total']:.0f}% / ${s['S3']['loss_tn']:.0f}T", 'td')],
           [P("Cboe VIX (Peak)", 'td'), P(f"{f['vix']}", 'td'), P("25-32", 'td'), P("35-50", 'td'), P("55-75", 'td')],
           [P("10-Year Treasury Yield", 'td'), P(f"{f['ust10']}%", 'td'), P("5.0-5.8%", 'td'), P("Spikes >6.0% then drops", 'td'),
            P("Spikes >6.0%, then Fed QE/cuts (3.5-4.5%)", 'td')],
           [P("High Yield Credit Spread", 'td'), P("(N/A)", 'td'), P("+100 to 150 bps", 'td'), P("+300 to 450 bps", 'td'), P("+600 to 900 bps", 'td')],
           [P("Brent Crude Oil ($/bbl)", 'td'), P(f"> ${f['brent']}", 'td'), P("90-125", 'td'), P("70-110 (Demand contracts)", 'td'), P("60-130 (Extreme volatility)", 'td')],
           [P("Spot Gold ($/oz)", 'td'), P(f"${f['gold']:,.0f}", 'td'), P("4,000-4,600", 'td'), P("4,300-5,200", 'td'), P("4,500-6,500 (Initial liquidation risk)", 'td')]]
    story.append(table(ass, [140, 60, 90, 100, 114]))
    story.append(P("Asset ranges are illustrative, based on analogies to 2000-02, 2008, 2020, and 2022 market cycles.", 'cap'))
    story.append(PageBreak())

    # ================= PAGE 8: GLOBAL MAP 1 =================
    story += h1("7. Global Vulnerability Map: Most Impacted Regions")
    story.append(P(
        "We engineered a <b>Composite Vulnerability Index (0 to 100)</b> per sovereign nation, weighting six core risk factors (scored 0-10): "
        "Energy Shock &amp; Hormuz (25%), Fiscal &amp; Sovereign Bond Stress (20%), Strong USD &amp; External Financing (15%), Technology &amp; Taiwan Semiconductor Chain (15%), "
        "US Market &amp; Private Credit Contagion (15%), and Direct Kinetic Risk (10%); combatant zones receive war-risk overlays (up to +15). "
        "Country scoring reflects auditable analytical modeling of primary macroeconomic exposures.", 'body'))
    story.append(_img("chart_map_vulnerability.png", 6.8))
    story.append(P("Composite Vulnerability Index mapped under the systemic stress scenario (S3). Geospatial boundary data: Natural Earth 110m.", 'cap'))
    story.append(_img("chart_region_ranking.png", 6.4))
    story.append(PageBreak())

    # ================= PAGE 9: GLOBAL MAP 2 + RANKINGS =================
    story += h1("8. Transmission Channels and Most Exposed Nations")
    story.append(_img("chart_map_channels.png", 7.0))
    story.append(P("Each sovereign territory is categorized by its highest weighted transmission vector; color depth reflects overall vulnerability score.", 'cap'))
    ranked = sorted([(a3, sc, dom, f_) for a3, sc, dom, _, f_ in rows if not np.isnan(sc) and a3 in COUNTRY_EN],
                    key=lambda t: -t[1])[:14]
    top = [[P("<b>#</b>", 'th'), P("<b>Country</b>", 'th'), P("<b>Score</b>", 'th'), P("<b>Dominant Channel</b>", 'th'),
            P("<b>Core Exposure Vectors</b>", 'th')]]
    why_en = {
        "JPN": "Imports 80-90% of crude via Hormuz; top LNG importer; 10Y JGB at 3.0%; yen carry unwind; semiconductor equipment.",
        "IRN": "Direct theater of kinetic war; sanctions blockade and infrastructure destruction.",
        "TWN": "TSMC (>90% of advanced logic); military blockade risks; heavy reliance on imported LNG.",
        "KOR": "Near-total imported energy reliance; memory semiconductor champions exposed to global tech capex cuts.",
        "PSX": "Active combat zone; complete socioeconomic paralysis.",
        "ISR": "Direct combatant; tech venture ecosystem deeply tied to US capital markets.",
        "IRQ": "Oil exports routed through Persian Gulf; extreme institutional fragility.",
        "PAK": "Massive fuel importer; heavy external debt servicing; reliance on IMF facilities.",
        "TUR": "Current account energy deficit; currency pressure; compressed net FX reserves.",
        "LKA": "Net fuel importer; sovereign debt restructuring vulnerabilities.",
        "EGY": "Imports fuel and wheat; currency strains; Suez Canal security disruptions.",
        "IND": "~45% of oil and ~50% of LNG imported via Hormuz; current account widens sharply above $100/bbl.",
        "CHN": "World's largest crude importer; domestic real estate deleveraging; US technology restrictions.",
        "FRA": "Primary Eurozone sovereign stress node (spread ~150 bps); upcoming 2027 election.",
        "GBR": "30Y Gilt yield near ~6% (highest since 1998); autumn fiscal budget risks.",
        "USA": "Crisis epicenter: 6.2% GDP deficit, 10Y at 5.24%, CAPE 41x; largest absolute wealth destruction.",
        "BGD": "Imported energy dependence; compressed dollar reserves.",
        "SYR": "Active combat theater.", "LBN": "Kinetic conflict and banking collapse.", "YEM": "Active war zone.",
        "KWT": "Exports vulnerable to Hormuz chokepoints.", "QAT": "LNG exports routed through Hormuz.",
        "ARG": "Chronic external financing and dollar debt vulnerabilities.", "BRA": "Fiscal deficit (~70% debt/GDP, 7.3% interest/GDP), buffered by commodity exports.",
        "DEU": "Elevated energy costs; industrial export exposure to Asian demand.",
        "ITA": "Elevated sovereign debt ratio and energy import reliance.",
    }
    for i, (a3, sc, dom, f_) in enumerate(ranked, 1):
        top.append([P(str(i), 'td'), P(f"<b>{COUNTRY_EN[a3]}</b>", 'td'), P(f"{sc:.0f}", 'td'),
                    P(FACTOR_NAMES_EN[dom], 'td'), P(why_en.get(a3, "-"), 'td')])
    story.append(table(top, [18, 70, 36, 120, 260], valign='TOP'))
    story.append(PageBreak())

    # ================= PAGE 10: WARNING SIGNALS & SOURCES =================
    story += h1("9. Early Warning Dashboard, Methodological Limits, and Sources")
    story.append(P("<b>Quantitative Warning Thresholds for Regime Migration:</b>", 'bold'))
    sig = [[P("<b>Market Indicator</b>", 'th'), P("<b>Observed Level</b>", 'th'), P("<b>Amber Alert (S1 ➔ S2)</b>", 'th'), P("<b>Red Alert (S2 ➔ S3)</b>", 'th')],
           [P("30Y / 10Y US Treasuries", 'td'), P(f"{f['ust30_auction']}% / {f['ust10']}%", 'td'), P("30Y Yield > 5.90%", 'td'), P("10Y Yield > 6.00% with falling equities", 'td')],
           [P("US Treasury Auctions", 'td'), P(f"Bid-to-Cover {f['btc_30y']}", 'td'), P("Ratio < 2.35 or tail > 2 bps", 'td'), P("Failed auction (tail > 5 bps, indirects < 60%)", 'td')],
           [P("Brent Crude Oil", 'td'), P(f"> ${f['brent']} / bbl", 'td'), P("Sustained > $120 / bbl", 'td'), P("Spikes > $140 / bbl or full Hormuz closure", 'td')],
           [P("US CPI &amp; Fed Funds", 'td'), P("3.4% YoY (Sep: 3.6-3.7% est.)", 'td'), P("CPI > 4.0% with new rate hike", 'td'), P("Hike paired with negative payrolls (policy error)", 'td')],
           [P("10Y JGB &amp; Japanese Yen", 'td'), P(f"{f['jgb10']:.2f}%", 'td'), P("10Y JGB > 3.50%", 'td'), P("Yen appreciates >8% in 2 weeks with equity selling", 'td')],
           [P("Cboe VIX &amp; HY Spreads", 'td'), P(f"{f['vix']} / (N/A)", 'td'), P("VIX > 25 or HY spreads +150 bps", 'td'), P("VIX > 35 or HY spreads > 700 bps", 'td')],
           [P("Private Credit &amp; CRE", 'td'), P("CMBS Office at 12-13%", 'td'), P("Redemption gates across 2+ large funds", 'td'), P("Collapse of major non-bank CRE lender", 'td')],
           [P("European Sovereign Spreads", 'td'), P(f"OAT-Bund ~{f['fr_bund_bp']} bps; 30Y Gilt {f['gilt30']}%", 'td'), P("OAT-Bund > 175 bps; Gilt > 6.50%", 'td'), P("ECB initiates emergency TPI bond purchases", 'td')],
           [P("AI Capex Megacycle", 'td'), P("Annual Capex > $230B", 'td'), P("Hyperscaler trims hardware capex guidance", 'td'), P("GPU rental rates drop >60%; neocloud defaults", 'td')]]
    story.append(table(sig, [110, 100, 140, 154], valign='TOP'))
    story.append(Spacer(1, 6))

    story.append(box(
        "<b>METHODOLOGICAL TRANSPARENCY:</b> (1) Datasets compiled from web and official data feeds on October 11, 2026; high-confidence metrics "
        "derive from sovereign disclosures (US Treasury, CBO, Federal Reserve); medium-confidence metrics derive from financial media and market data providers "
        "(Shiller CAPE, Buffett ratio, daily yields, war reporting). (2) Official reports vary regarding the exact operational status of the Strait of Hormuz "
        "(partial closure vs. severe maritime attacks). (3) Probabilities, transmission weights, and regional scores reflect <b>structured analytical models</b>, "
        "not deterministic forecasts. (4) Certain micro-states (Singapore, Bahrain, Hong Kong) are aggregated due to 110m map resolution constraints. "
        "(5) This report is compiled exclusively for institutional research and <b>does not constitute investment advice</b>.",
        '#FEF2F2', '#F87171', 'td'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Primary Consulted Sources (by domain, 10/11/2026):</b> fiscaldata.treasury.gov (Debt to the Penny, TIC); cbo.gov; crfb.org; "
                   "americanactionforum.org; federalreserve.gov (FOMC minutes &amp; decisions); ycharts.com and tradingeconomics.com (sovereign yields); "
                   "imf.org (GFSR Oct 2026, WEO); trepp.com, wolfstreet.com and commercialobserver.com (CMBS/CRE); goldmansachs.com and kitco.com; "
                   "counterpointresearch.com (TSMC); un.org/UNCTAD; financial press for Japan, UK, France, and Brazil.", 'cap'))

    doc.build(story, canvasmaker=NumberedCanvasEN)
    print(f"Macro Geopolitics Report successfully compiled: {output_filename}", flush=True)

def main():
    print("=== COMPUTING DERIVED METRICS ===", flush=True)
    d = compute_derived_metrics()
    
    print("\n=== LOADING GEODATA & COMPUTING COUNTRY SCORES ===", flush=True)
    gdf = gpd.read_file(GEOJSON)
    rows = compute_country_scores(gdf)
    
    # Calculate regional rankings
    by_region = {}
    for a3, sc, dom, sub, f_ in rows:
        if not np.isnan(sc):
            by_region.setdefault(sub, []).append(sc)
    ranking = sorted(((REGION_PT.get(k, k), float(np.mean(v)), len(v)) for k, v in by_region.items()), key=lambda t: t[1])
    
    print("\n=== COMPILING 10-PAGE ENGLISH EXECUTIVE PDF REPORT ===", flush=True)
    pdf_filename = "Report_Macro_Geopolitics_Market_Crash_2026_2028.pdf"
    build_pdf_report_en(d, rows, ranking, pdf_filename)
    print(f"Generated: {os.path.abspath(pdf_filename)}", flush=True)

if __name__ == "__main__":
    main()
