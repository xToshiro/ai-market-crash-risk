#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Relatório Macro-Geopolítico: Situação Fiscal dos EUA, Eleições, Guerras e
Anatomia de uma Possível Quebra do Mercado Financeiro (Out/2026 - Out/2028),
com Mapa Mundial de Vulnerabilidade Regional.

Gera 7 gráficos (incluindo 2 mapas) e um relatório executivo em PDF.

IMPORTANTE (método):
 - Os "fatos" abaixo (FACTS) foram coletados por busca na web em 11/10/2026 e estão
   rotulados com a fonte e o nível de confiança. Valores derivados são calculados no
   próprio script (ver compute_derived_metrics) para que fiquem auditáveis.
 - Probabilidades, atribuições de queda e o índice de vulnerabilidade por país são
   JULGAMENTOS ANALÍTICOS transparentes (pesos e notas explícitos no código), não
   previsões nem recomendações de investimento.
"""

import os
import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap, to_rgba, Normalize
from matplotlib.patches import Patch
import geopandas as gpd
from pyproj import Transformer

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

REPORT_DATE = "11/10/2026"
HERE = os.path.dirname(os.path.abspath(__file__))
from utils_paths import get_geo_path, get_chart_path, get_report_pt_path
GEOJSON = get_geo_path("world_countries_110m.geojson")

# ---------------------------------------------------------
# 0. FATOS COLETADOS (11/10/2026) - com fonte e confiança
# ---------------------------------------------------------
FACTS = {
    # Governo dos EUA
    "debt_total_tn": 40.3053162,      # Treasury Debt to the Penny (08/10/2026) - alta
    "debt_public_tn": 32.4540861,     # idem
    "debt_intragov_tn": 7.8512301,    # idem
    "deficit_fy26_tn": 2.0,           # CRFB / AAF (realizado, 6.2% PIB) - média/alta
    "deficit_fy26_pct": 6.2,
    "deficit_cbo_feb_tn": 1.9,        # CBO baseline fev/2026 (5.8% PIB) - alta
    "deficit_2036_tn": 3.1,           # CBO (6.7% PIB em 2036) - alta
    "net_interest_tn": 1.05,          # ponto médio de 1.0-1.1 tri (3.3-3.4% PIB) - alta/média
    "debt_gdp_2026": 101,             # CBO (% PIB, dívida em mãos do público)
    "debt_gdp_2036": 120,
    "japan_ust_tn": 1.1039,           # Treasury TIC (jul/2026) - alta
    "china_ust_tn": 0.618,            # idem
    # Juros / Fed / inflação / emprego
    "fed_low": 3.75, "fed_high": 4.00,  # FOMC 16/09/2026 (+25 pb, 12-0) - alta
    "ust10": 5.24,                    # 09/10/2026 - média/alta (YCharts, TradingEconomics)
    "ust30_auction": 5.62,            # leilão 08/10/2026 - média/alta
    "ust30_peak_week": 5.67,
    "btc_30y": 2.54, "indirect_30y": 72.3,
    "cpi_aug": 3.4, "cpi_sep_exp": 3.65,
    "unemp": 4.2, "payroll_sep_k": 29,
    "gdp_q2": 2.2,
    # Mercado
    "spx": 7811.54, "ixic": 27366.17, "vix": 14.84, "gold": 4205.40,
    "spx_fwd_pe": 23.4,               # dossiê anterior do repositório
    "cape": 41.0,                     # 40.7-41.6 (agregadores/Shiller) - média
    "buffett_pct": 237,               # 236-238 - média
    "top10_weight": 41, "top3_weight": 21,
    # Geopolítica / energia
    "brent": 105,
    "hormuz_share_pct": 20,           # ~20% do petróleo e do GNL
    # Crédito / bancos
    "cre_maturity_bn": 875, "cre_banks_bn": 396, "cmbs_office_delinq": 12.6,
    "hedge_funds_tn": 13,
    # Outros países
    "jgb10": 3.02, "gilt30": 6.04, "fr_bund_bp": 150,
    "brazil_selic": 13.75, "brazil_debt_gdp": 70, "brazil_interest_gdp": 7.3,
    "tsmc_adv_share": 90,
}

# Probabilidade-base de bear market (queda >= 20%) em janela de 2 anos:
# ~12-13 bear markets do S&P 500 desde 1950 (~1 a cada 6 anos) -> Poisson 2 anos ~ 27%
BASE_RATE_BEAR_2Y = 27.0
OVERLAY = [  # (rótulo, pontos percentuais) - julgamento analítico
    ("Valuations extremos\n(CAPE 41, Buffett 237%,\ntop-10 = 41%)", +5),
    ("Juros longos / prêmio de\nprazo (10Y 5.24%, ERP<0)", +3),
    ("Guerra / energia +\ninflação c/ Fed subindo", +3),
    ("Crédito: CRE, crédito\nprivado, hedge funds", +2),
    ("Política / instituições\n(Fed, teto, tarifas)", +1),
    ("Mitigantes (lucros,\nleilão 30Y sólido)", -1),
]

# Cenários (janela Out/2026 - Out/2028): (id, nome, faixa, probabilidade %)
SCENARIOS = [
    ("S0", "Continuação c/ volatilidade", "queda máx. < 10%", 27.0),
    ("S1", "Correção / estagflação branda", "queda de 10% a 20%", 33.0),
    ("S2", "Bear market de ciclo + crédito", "queda de 20% a 35%", 25.0),
    ("S3", "Crash sistêmico", "queda > 35% (central -48%)", 15.0),
]

# Decomposição preço = P/E x LPA para os cenários S1..S3
DECOMP = {
    "S1": {"pe_to": 20.0, "eps": -0.5},
    "S2": {"pe_to": 18.0, "eps": -9.0},
    "S3": {"pe_to": 14.5, "eps": -16.0},
}

# Atribuição da queda por canal (% do total) - julgamento analítico; cada coluna soma 100
CHANNELS = [
    ("Juros longos / prêmio de prazo / fiscal", "#7C3AED"),
    ("Estouro do ciclo de IA (capex, valuations)", "#0D9488"),
    ("Guerra e choque energético", "#EA580C"),
    ("Crédito e liquidez (CRE, crédito privado,\nhedge funds, carry do iene)", "#DC2626"),
    ("Política e instituições (eleições, Fed, tarifas)", "#2563EB"),
    ("Cauda geopolítica (Taiwan)", "#0F172A"),
]
ATTRIB = {
    "S1": [30, 25, 20, 10, 15, 0],
    "S2": [25, 33, 15, 15, 12, 0],
    "S3": [18, 25, 12, 28, 14, 3],
}

# ---------------------------------------------------------
# 1. ÍNDICE DE VULNERABILIDADE REGIONAL (julgamento transparente)
# ---------------------------------------------------------
# Fatores (nota 0-10) e pesos
FACTOR_KEYS = ["E", "F", "X", "T", "M", "G"]
FACTOR_NAMES = {
    "E": "Choque energético / Hormuz",
    "F": "Estresse fiscal e de títulos soberanos",
    "X": "Dólar forte e financiamento externo",
    "T": "Cadeia de tecnologia / IA / Taiwan",
    "M": "Contágio de mercados e crédito dos EUA",
    "G": "Risco geopolítico / político direto",
}
FACTOR_WEIGHTS = {"E": 0.25, "F": 0.20, "X": 0.15, "T": 0.15, "M": 0.15, "G": 0.10}
CHANNEL_COLORS = {
    "E": "#EA580C", "F": "#7C3AED", "X": "#2563EB",
    "T": "#0D9488", "M": "#DC2626", "G": "#111827",
}

# (E, F, X, T, M, G, ajuste_zona_de_guerra)
SCORES = {
    # América do Norte
    "USA": (2, 8, 1, 7, 10, 4, 0), "CAN": (1, 3, 2, 3, 7, 2, 0), "MEX": (3, 5, 6, 4, 7, 5, 0),
    # América do Sul
    "BRA": (2, 8, 6, 2, 5, 4, 0), "ARG": (2, 8, 9, 1, 4, 5, 0), "VEN": (1, 8, 9, 0, 1, 7, 0),
    # Europa
    "GBR": (5, 8, 3, 4, 8, 4, 0), "IRL": (5, 3, 2, 6, 8, 2, 0), "FRA": (5, 9, 2, 4, 7, 5, 0),
    "DEU": (7, 4, 2, 5, 7, 5, 0), "ITA": (6, 8, 2, 3, 6, 4, 0), "ESP": (5, 6, 2, 3, 6, 3, 0),
    "CHE": (4, 1, 1, 4, 7, 2, 0), "NOR": (0, 1, 1, 2, 7, 3, 0),
    "EST": (5, 3, 3, 3, 5, 6, 0), "LVA": (5, 3, 3, 3, 5, 6, 0), "LTU": (5, 3, 3, 3, 5, 6, 0),
    "FIN": (5, 3, 3, 3, 5, 6, 0),
    "UKR": (6, 10, 9, 1, 1, 10, 0), "RUS": (1, 6, 7, 2, 3, 10, 0), "BLR": (4, 6, 8, 1, 1, 8, 0),
    "POL": (5, 5, 4, 3, 5, 7, 0),
    # Oriente Médio
    "TUR": (8, 7, 9, 2, 5, 7, 0), "IRN": (6, 9, 9, 1, 1, 10, 15), "IRQ": (9, 8, 6, 0, 1, 10, 8),
    "ISR": (5, 5, 3, 7, 7, 10, 8), "KWT": (9, 3, 2, 1, 5, 9, 6), "QAT": (9, 2, 2, 1, 5, 9, 6),
    "ARE": (6, 3, 2, 2, 6, 8, 5), "SAU": (5, 3, 2, 2, 5, 8, 5), "OMN": (5, 4, 3, 1, 4, 7, 4),
    "YEM": (7, 9, 9, 0, 1, 9, 6), "SYR": (7, 9, 9, 0, 1, 9, 6), "LBN": (7, 9, 9, 0, 1, 9, 6),
    "JOR": (8, 8, 7, 0, 2, 8, 3), "PSX": (7, 9, 9, 0, 0, 10, 10),
    "CYP": (5, 5, 3, 2, 5, 5, 0), "CYN": (5, 5, 3, 2, 5, 5, 0),
    "AZE": (2, 4, 4, 1, 2, 6, 0),
    # Ásia
    "JPN": (10, 9, 4, 8, 8, 6, 0), "KOR": (9, 4, 5, 9, 8, 7, 0), "TWN": (9, 2, 3, 10, 9, 10, 0),
    "CHN": (7, 6, 3, 8, 6, 8, 0), "MNG": (6, 5, 8, 0, 1, 6, 0), "PRK": (5, 8, 8, 0, 0, 9, 0),
    "IND": (9, 6, 6, 4, 5, 5, 0), "PAK": (8, 9, 9, 1, 2, 7, 0), "BGD": (9, 8, 8, 2, 2, 5, 0),
    "LKA": (9, 9, 9, 1, 1, 4, 0), "NPL": (8, 6, 7, 0, 1, 4, 0), "AFG": (7, 9, 9, 0, 0, 8, 0),
    "IDN": (5, 4, 6, 3, 5, 3, 0), "MMR": (6, 8, 8, 0, 0, 8, 0), "MYS": (4, 3, 4, 8, 6, 3, 0),
    "VNM": (6, 4, 5, 7, 5, 5, 0), "THA": (7, 5, 5, 5, 5, 4, 0), "PHL": (8, 5, 6, 3, 5, 5, 0),
    "LAO": (7, 9, 9, 0, 0, 3, 0), "KAZ": (1, 3, 4, 1, 2, 5, 0),
    # Oceania
    "AUS": (2, 3, 3, 3, 7, 3, 0), "NZL": (4, 4, 4, 2, 6, 2, 0),
    # África
    "DZA": (1, 4, 4, 0, 1, 4, 0), "LBY": (1, 6, 6, 0, 0, 8, 0), "EGY": (7, 9, 9, 1, 2, 7, 0),
    "MAR": (7, 6, 6, 3, 3, 3, 0), "TUN": (7, 9, 8, 0, 1, 4, 0), "SDN": (7, 9, 9, 0, 0, 9, 0),
    "NGA": (3, 8, 8, 0, 2, 6, 0), "GHA": (6, 9, 9, 0, 2, 3, 0), "CIV": (5, 6, 7, 0, 2, 4, 0),
    "SOM": (7, 9, 9, 0, 0, 9, 0), "SDS": (7, 9, 9, 0, 0, 9, 0), "SOL": (7, 9, 9, 0, 0, 7, 0),
    "AGO": (2, 8, 8, 0, 1, 4, 0), "COD": (5, 9, 9, 0, 0, 9, 0), "ZAF": (5, 6, 6, 1, 4, 3, 0),
}

SUBREGION_DEFAULTS = {
    "Central America": (6, 5, 7, 1, 4, 4, 0),
    "Caribbean": (7, 6, 7, 0, 3, 4, 0),
    "South America": (3, 5, 6, 1, 4, 4, 0),
    "Western Europe": (6, 6, 2, 4, 7, 4, 0),
    "Northern Europe": (4, 2, 2, 4, 7, 4, 0),
    "Southern Europe": (6, 7, 4, 2, 5, 4, 0),
    "Eastern Europe": (6, 6, 5, 3, 4, 7, 0),
    "Western Asia": (7, 7, 6, 1, 3, 6, 0),
    "Central Asia": (3, 3, 5, 1, 2, 5, 0),
    "Southern Asia": (8, 7, 7, 2, 3, 5, 0),
    "Eastern Asia": (7, 6, 5, 6, 6, 7, 0),
    "South-Eastern Asia": (6, 4, 5, 6, 5, 4, 0),
    "Australia and New Zealand": (3, 3, 3, 3, 7, 3, 0),
    "Melanesia": (7, 6, 7, 0, 1, 3, 0),
    "Northern Africa": (6, 7, 7, 0, 2, 5, 0),
    "Western Africa": (6, 7, 8, 0, 2, 6, 0),
    "Eastern Africa": (7, 8, 9, 0, 1, 6, 0),
    "Middle Africa": (4, 8, 8, 0, 1, 6, 0),
    "Southern Africa": (6, 6, 7, 0, 2, 3, 0),
}

REGION_PT = {
    "Northern America": "América do Norte",
    "Central America": "América Central",
    "Caribbean": "Caribe",
    "South America": "América do Sul",
    "Western Europe": "Europa Ocidental",
    "Northern Europe": "Europa do Norte / Reino Unido",
    "Southern Europe": "Europa do Sul",
    "Eastern Europe": "Europa Oriental / Rússia",
    "Western Asia": "Oriente Médio / Cáucaso",
    "Central Asia": "Ásia Central",
    "Southern Asia": "Sul da Ásia",
    "Eastern Asia": "Leste Asiático",
    "South-Eastern Asia": "Sudeste Asiático",
    "Australia and New Zealand": "Austrália e N. Zelândia",
    "Melanesia": "Melanésia",
    "Northern Africa": "Norte da África",
    "Western Africa": "África Ocidental",
    "Eastern Africa": "África Oriental",
    "Middle Africa": "África Central",
    "Southern Africa": "África Austral",
}

COUNTRY_PT = {
    "USA": "EUA", "CAN": "Canadá", "MEX": "México", "BRA": "Brasil", "ARG": "Argentina",
    "VEN": "Venezuela", "GBR": "Reino Unido", "IRL": "Irlanda", "FRA": "França",
    "DEU": "Alemanha", "ITA": "Itália", "ESP": "Espanha", "CHE": "Suíça", "NOR": "Noruega",
    "UKR": "Ucrânia", "RUS": "Rússia", "TUR": "Turquia", "IRN": "Irã", "IRQ": "Iraque",
    "ISR": "Israel", "KWT": "Kuwait", "QAT": "Catar", "ARE": "Emirados", "SAU": "Arábia Saudita",
    "JPN": "Japão", "KOR": "Coreia do Sul", "TWN": "Taiwan", "CHN": "China", "IND": "Índia",
    "PAK": "Paquistão", "BGD": "Bangladesh", "LKA": "Sri Lanka", "EGY": "Egito",
    "ZAF": "África do Sul", "NGA": "Nigéria", "AUS": "Austrália", "IDN": "Indonésia",
    "VNM": "Vietnã", "THA": "Tailândia", "PHL": "Filipinas", "MYS": "Malásia",
    "POL": "Polônia", "GHA": "Gana", "SDN": "Sudão", "YEM": "Iêmen", "SYR": "Síria",
    "LBN": "Líbano", "PSX": "Palestina", "AFG": "Afeganistão", "MMR": "Mianmar",
}


def compute_country_scores(gdf):
    """Calcula o índice composto (0-100), canal dominante e região para cada país."""
    rows = []
    for _, r in gdf.iterrows():
        a3 = r["ADM0_A3"]
        sub = r["SUBREGION"]
        vals = SCORES.get(a3) or SUBREGION_DEFAULTS.get(sub)
        if vals is None:
            rows.append((a3, np.nan, None, sub, None))
            continue
        *f, adj = vals
        weighted = {k: f[i] * FACTOR_WEIGHTS[k] for i, k in enumerate(FACTOR_KEYS)}
        score = min(100.0, sum(weighted.values()) * 10 + adj)
        dominant = max(weighted, key=weighted.get)
        if adj >= 5 and f[5] >= 9:
            dominant = "G"  # zona de guerra direta
        rows.append((a3, score, dominant, sub, {k: f[i] for i, k in enumerate(FACTOR_KEYS)}))
    return rows


# ---------------------------------------------------------
# 2. MÉTRICAS DERIVADAS (auditáveis)
# ---------------------------------------------------------
def compute_derived_metrics():
    f = FACTS
    d = {}
    d["gdp_tn"] = f["deficit_fy26_tn"] / (f["deficit_fy26_pct"] / 100.0)
    d["equity_cap_tn"] = d["gdp_tn"] * f["buffett_pct"] / 100.0
    d["earnings_yield"] = 100.0 / f["spx_fwd_pe"]
    d["erp_vs_10y"] = d["earnings_yield"] - f["ust10"]
    d["real_10y"] = f["ust10"] - f["cpi_aug"]
    d["interest_per_day_bn"] = f["net_interest_tn"] * 1000 / 365
    d["deficit_per_day_bn"] = f["deficit_fy26_tn"] * 1000 / 365
    d["effective_rate"] = f["net_interest_tn"] / f["debt_public_tn"] * 100
    d["plus100bp_bn"] = f["debt_public_tn"] * 1000 * 0.01
    d["fed_mid"] = (f["fed_low"] + f["fed_high"]) / 2
    d["curve_10y_ff"] = f["ust10"] - d["fed_mid"]
    d["debt_gdp_calc"] = f["debt_public_tn"] / d["gdp_tn"] * 100
    d["scen"] = {}
    for sid, p in DECOMP.items():
        pe_chg = (p["pe_to"] / f["spx_fwd_pe"] - 1) * 100
        total = ((1 + pe_chg / 100) * (1 + p["eps"] / 100) - 1) * 100
        d["scen"][sid] = {"pe_chg": pe_chg, "eps": p["eps"], "total": total,
                          "loss_tn": -total / 100 * d["equity_cap_tn"]}
    p_ge20 = sum(s[3] for s in SCENARIOS[2:])
    d["p_ge20"] = p_ge20
    d["p_ge10"] = sum(s[3] for s in SCENARIOS[1:])
    d["overlay_total"] = BASE_RATE_BEAR_2Y + sum(v for _, v in OVERLAY)
    return d


# ---------------------------------------------------------
# 3. ESTILO E GRÁFICOS
# ---------------------------------------------------------
def setup_chart_style():
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#E2E8F0'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.8


def _finish(fig, path, label):
    pt_path = get_chart_path(os.path.basename(path), lang="pt")
    fig.savefig(pt_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"{label} gerado: {pt_path}", flush=True)


def chart_fiscal_dashboard(d, path="chart_us_fiscal_dashboard.png"):
    setup_chart_style()
    f = FACTS
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.0))
    fig.patch.set_facecolor('white')

    # (a) Composição da dívida
    ax = axes[0, 0]
    ax.set_facecolor('#FAFAFA')
    ax.barh([0], [f["debt_public_tn"]], color='#1E3A8A', height=0.5, label='Em mãos do público')
    ax.barh([0], [f["debt_intragov_tn"]], left=[f["debt_public_tn"]], color='#93C5FD', height=0.5,
            label='Intragovernamental')
    ax.text(f["debt_public_tn"] / 2, 0, f"US$ {f['debt_public_tn']:.2f} tri\n(~{d['debt_gdp_calc']:.0f}% do PIB)",
            ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    ax.text(f["debt_public_tn"] + f["debt_intragov_tn"] / 2, 0, f"{f['debt_intragov_tn']:.2f}",
            ha='center', va='center', color='#0F172A', fontsize=8, fontweight='bold')
    ax.set_xlim(0, 44)
    ax.set_yticks([])
    ax.set_ylim(-0.55, 0.95)
    ax.set_title(f"Dívida federal total: US$ {f['debt_total_tn']:.2f} tri (08/10/2026)", fontsize=9, fontweight='bold')
    ax.set_xlabel("US$ trilhões", fontsize=8)
    ax.legend(loc='upper center', fontsize=7, ncol=2, frameon=False)

    # (b) Fluxos anuais
    ax = axes[0, 1]
    ax.set_facecolor('#FAFAFA')
    labels = ["Déficit FY26\nCBO (fev/26)", "Déficit FY26\nrealizado", "Juros líquidos\nFY26", "Déficit 2036\n(CBO)"]
    vals = [f["deficit_cbo_feb_tn"], f["deficit_fy26_tn"], f["net_interest_tn"], f["deficit_2036_tn"]]
    cols = ['#94A3B8', '#DC2626', '#F59E0B', '#7C2D12']
    bars = ax.bar(labels, vals, color=cols, width=0.6, edgecolor='#1E293B', linewidth=0.5)
    for b, v in zip(bars, vals):
        ax.annotate(f"US$ {v:.2f} tri" if v != f["net_interest_tn"] else "US$ 1.0-1.1 tri",
                    xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3), textcoords='offset points',
                    ha='center', fontsize=7.5, fontweight='bold')
    ax.set_ylim(0, 3.8)
    ax.set_title("Déficit e juros: cenário já sem recessão (desemprego 4.2%)", fontsize=9, fontweight='bold')
    ax.tick_params(axis='x', labelsize=7)
    ax.grid(True, axis='y')

    # (c) Juros longos globais
    ax = axes[1, 0]
    ax.set_facecolor('#FAFAFA')
    labs = ["Fed funds\n(ponto médio)", "EUA 10Y", "EUA 30Y\n(leilão)", "Japão 10Y\n(JGB)", "Reino Unido\n30Y (gilt)"]
    ys = [d["fed_mid"], f["ust10"], f["ust30_auction"], f["jgb10"], f["gilt30"]]
    cs = ['#475569', '#1E3A8A', '#7C3AED', '#0D9488', '#B91C1C']
    bars = ax.bar(labs, ys, color=cs, width=0.6, edgecolor='#1E293B', linewidth=0.5)
    for b, v in zip(bars, ys):
        ax.annotate(f"{v:.2f}%", xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3),
                    textcoords='offset points', ha='center', fontsize=7.5, fontweight='bold')
    ax.axhline(f["cpi_aug"], color='#EA580C', linestyle='--', linewidth=1.2)
    ax.text(3.0, f["cpi_aug"] + 0.28, f"CPI EUA (ago): {f['cpi_aug']}%", color='#C2410C', fontsize=7, ha='center',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.set_ylim(0, 7.2)
    ax.set_title("Juros: a ponta longa é quem manda (maiores níveis em décadas)", fontsize=9, fontweight='bold')
    ax.tick_params(axis='x', labelsize=7)
    ax.grid(True, axis='y')

    # (d) cartões numéricos
    ax = axes[1, 1]
    ax.axis('off')
    cards = [
        (f"US$ {d['interest_per_day_bn']:.1f} bi / dia", "juros líquidos pagos pelo Tesouro", '#F59E0B'),
        (f"US$ {d['deficit_per_day_bn']:.1f} bi / dia", "déficit a ser financiado (FY26)", '#DC2626'),
        (f"+US$ {d['plus100bp_bn']:.0f} bi / ano", "por cada +100 pb (reprecificação total)", '#7C3AED'),
        (f"{d['effective_rate']:.1f}% vs {f['ust30_auction']:.2f}%", "taxa efetiva implícita vs 30Y novo", '#1E3A8A'),
    ]
    for i, (big, small, col) in enumerate(cards):
        y = 0.86 - i * 0.25
        ax.add_patch(plt.Rectangle((0.0, y - 0.105), 1.0, 0.215, transform=ax.transAxes,
                                   facecolor='#F8FAFC', edgecolor=col, linewidth=1.4))
        ax.text(0.04, y + 0.04, big, transform=ax.transAxes, fontsize=12, fontweight='bold', color=col, va='center')
        ax.text(0.04, y - 0.05, small, transform=ax.transAxes, fontsize=7, color='#475569', va='center')
    ax.set_title("A matemática do refinanciamento", fontsize=9, fontweight='bold')

    plt.tight_layout(h_pad=2.2)
    _finish(fig, path, "Gráfico 1 (dashboard fiscal)")


def chart_valuation_vs_rates(d, path="chart_valuation_vs_rates.png"):
    setup_chart_style()
    f = FACTS
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.5))
    fig.patch.set_facecolor('white')

    # CAPE nos topos vs queda subsequente (valores aproximados - Shiller/Yale)
    ax1.set_facecolor('#FAFAFA')
    periods = ["Set/1929", "Dez/1999", "Out/2007", "Jan/2022", "Hoje\n(out/2026)"]
    cape = [32.6, 44.2, 27.2, 38.6, f["cape"]]
    dd = ["-86%\n(até 1932)", "-49%\n(até 2002)", "-57%\n(até 2009)", "-25%\n(em 2022)", "?"]
    cs = ['#64748B', '#64748B', '#64748B', '#64748B', '#DC2626']
    bars = ax1.bar(periods, cape, color=cs, width=0.6, edgecolor='#1E293B', linewidth=0.5)
    for b, v, t in zip(bars, cape, dd):
        ax1.annotate(f"{v:.1f}x", xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3),
                     textcoords='offset points', ha='center', fontsize=8, fontweight='bold')
        ax1.text(b.get_x() + b.get_width() / 2, 3, t, ha='center', va='bottom', fontsize=6.6,
                 color='white', fontweight='bold')
    ax1.axhline(17.5, color='#0D9488', linestyle='--', linewidth=1.2)
    ax1.text(2.0, 20.2, "média histórica ~17-18x", fontsize=7, color='#0F766E', ha='center', zorder=5,
             bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#0D9488', lw=0.6, alpha=0.95))
    ax1.set_ylim(0, 52)
    ax1.set_title("Shiller CAPE nos topos históricos e queda seguinte", fontsize=9, fontweight='bold')
    ax1.tick_params(axis='x', labelsize=7)
    ax1.grid(True, axis='y')

    # Earnings yield vs Treasuries
    ax2.set_facecolor('#FAFAFA')
    labs = ["Rendimento de\nlucros S&P 500\n(1/P/E fwd 23.4x)", "Fed funds", "Treasury 10Y", "Treasury 30Y"]
    ys = [d["earnings_yield"], d["fed_mid"], f["ust10"], f["ust30_auction"]]
    cs = ['#0D9488', '#475569', '#1E3A8A', '#7C3AED']
    bars = ax2.bar(labs, ys, color=cs, width=0.6, edgecolor='#1E293B', linewidth=0.5)
    for b, v in zip(bars, ys):
        ax2.annotate(f"{v:.2f}%", xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3),
                     textcoords='offset points', ha='center', fontsize=8, fontweight='bold')
    ax2.annotate(f"Prêmio de risco vs 10Y:\n{d['erp_vs_10y']:+.2f} p.p.", xy=(0, d["earnings_yield"]),
                 xytext=(0.35, 6.55), fontsize=7.5, color='#B91C1C', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#B91C1C'))
    ax2.set_ylim(0, 7.6)
    ax2.set_title("Ações pagam menos que Treasuries: prêmio de risco negativo", fontsize=9, fontweight='bold')
    ax2.tick_params(axis='x', labelsize=6.8)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _finish(fig, path, "Gráfico 2 (valuation vs juros)")


def chart_timeline(path="chart_triggers_timeline.png"):
    setup_chart_style()
    D = datetime.date
    fig, (axz, axb) = plt.subplots(2, 1, figsize=(9.2, 6.2), gridspec_kw={'height_ratios': [1, 1.25]})
    fig.patch.set_facecolor('white')

    cat_col = {"Política": "#2563EB", "Monetário": "#7C3AED", "Geopolítica": "#EA580C",
               "Fiscal": "#B91C1C", "Mercado": "#0D9488"}

    # Painel superior: janela crítica Out-Nov/2026
    ev = [
        (D(2026, 10, 13), "FMI: WEO\n(Bangkok)", "Mercado", 0.55),
        (D(2026, 10, 14), "CPI de setembro\n(esp. 3.6-3.7%)", "Monetário", -0.6),
        (D(2026, 10, 25), "Brasil:\n2º turno", "Política", 0.55),
        (D(2026, 10, 28), "FOMC (27-28/10) +\nOrçamento UK (28/10)", "Monetário", -0.6),
        (D(2026, 11, 3), "EUA: eleições de\nmeio de mandato", "Política", 0.55),
    ]
    axz.set_facecolor('#FAFAFA')
    axz.axhline(0, color='#334155', linewidth=2)
    for dt, lab, cat, h in ev:
        axz.vlines(dt, 0, h * 0.8, color=cat_col[cat], linewidth=1.5)
        axz.plot(dt, 0, 'o', color=cat_col[cat], markersize=7)
        axz.text(dt, h, f"{dt.strftime('%d/%m')}\n{lab}", ha='center',
                 va='bottom' if h > 0 else 'top', fontsize=7, color='#0F172A', fontweight='bold')
    axz.set_ylim(-1.5, 1.5)
    axz.set_xlim(D(2026, 10, 9), D(2026, 11, 9))
    axz.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    axz.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    axz.tick_params(axis='x', labelsize=7)
    axz.set_yticks([])
    axz.set_title("Janela crítica: 4 semanas com FMI, inflação, Fed, orçamento britânico, Brasil e eleições dos EUA",
                  fontsize=9, fontweight='bold')

    # Painel inferior: 2 anos
    axb.set_facecolor('#FAFAFA')
    spans = [
        ("Muro de vencimentos de CRE (US$ 875 bi em 2026; extensões empurram para 2027)", D(2026, 10, 9), D(2027, 12, 31), 0, '#F87171'),
        ("Digestão do capex de IA / depreciação de GPUs / crédito privado de infraestrutura", D(2027, 1, 1), D(2028, 10, 9), 1, '#5EEAD4'),
        ("Congresso dividido (se a Câmara virar): risco de impasse orçamentário / teto da dívida", D(2027, 1, 3), D(2028, 10, 9), 2, '#C4B5FD'),
        ("Janela de risco Taiwan (avaliação EUA: invasão improvável antes de 2028)", D(2028, 1, 1), D(2028, 10, 9), 3, '#FDBA74'),
    ]
    for lab, s, e, lane, col in spans:
        axb.barh(lane, (e - s).days, left=mdates.date2num(s), height=0.55, color=col, alpha=0.85, edgecolor='#475569')
        if lane == 3:  # rótulo à esquerda da barra (a barra é curta)
            axb.text(mdates.date2num(s) - 8, lane, lab, va='center', ha='right', fontsize=6.4, color='#0F172A')
        else:
            axb.text(mdates.date2num(s) + 8, lane, lab, va='center', ha='left', fontsize=6.4, color='#0F172A')
    # (data, rótulo, categoria, alinhamento horizontal do texto)
    pts = [
        (D(2026, 12, 15), "FOMC dez/26\n(projeções)", "Monetário", 'center'),
        (D(2027, 4, 15), "França: eleição presidencial\n(abr-mai/2027)", "Política", 'center'),
        (D(2028, 1, 31), "Fim do mandato de Powell\ncomo governador do Fed", "Monetário", 'center'),
        (D(2028, 10, 9), "Fim do horizonte\n(out/2028)", "Mercado", 'right'),
        (D(2028, 11, 7), "Eleição presidencial\nEUA (07/11/2028)", "Política", 'left'),
    ]
    y_mark = 4.1
    for dt, lab, cat, ha in pts:
        axb.vlines(dt, 3.5, y_mark, color=cat_col[cat], linewidth=1.4, linestyle=':', zorder=1)
        axb.plot(dt, y_mark, 'D', color=cat_col[cat], markersize=6, zorder=4)
        dx = {'center': 0, 'right': -6, 'left': 6}[ha]
        axb.text(mdates.date2num(dt) + dx, y_mark + 0.3, lab, ha=ha, va='top', fontsize=6.6,
                 fontweight='bold', color='#0F172A')
    axb.set_xlim(D(2026, 10, 1), D(2029, 3, 1))
    axb.set_ylim(5.6, -0.7)
    axb.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    axb.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    axb.tick_params(axis='x', labelsize=7)
    axb.set_yticks([])
    axb.grid(True, axis='x')
    axb.set_title("Horizonte de 2 anos (out/2026 - out/2028): regimes e gatilhos recorrentes", fontsize=9, fontweight='bold')

    handles = [Patch(color=c, label=k) for k, c in cat_col.items()]
    fig.legend(handles=handles, loc='lower center', ncol=5, fontsize=7, frameon=False)
    plt.tight_layout(rect=[0, 0.03, 1, 1], h_pad=2.0)
    _finish(fig, path, "Gráfico 3 (calendário de gatilhos)")


def chart_probabilities(d, path="chart_probability_buildup.png"):
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0), gridspec_kw={'width_ratios': [1.35, 1]})
    fig.patch.set_facecolor('white')

    # Cascata horizontal: taxa-base -> probabilidade ajustada de queda >= 20%
    ax1.set_facecolor('#FAFAFA')
    short = ["Taxa-base histórica\n(bear market em 2 anos)",
             "Valuations extremos\n(CAPE 41, Buffett 237%)",
             "Juros longos / prêmio de prazo\n(10Y 5.24%, ERP < 0)",
             "Guerra / energia + inflação\ncom Fed subindo",
             "Crédito: CRE, crédito\nprivado, hedge funds",
             "Política / instituições\n(Fed, teto da dívida, tarifas)",
             "Mitigantes (lucros,\nleilão de 30Y sólido)",
             "P(queda >= 20%)\nem 2 anos"]
    n = len(short)
    ypos = np.arange(n)[::-1]
    cum = BASE_RATE_BEAR_2Y
    ax1.barh(ypos[0], cum, color='#64748B', height=0.62, edgecolor='#1E293B', linewidth=0.5)
    ax1.text(cum + 0.6, ypos[0], f"{cum:.0f}%", va='center', fontsize=8, fontweight='bold')
    for i, (_, v) in enumerate(OVERLAY, start=1):
        left = cum if v >= 0 else cum + v
        ax1.barh(ypos[i], abs(v), left=left, color='#DC2626' if v > 0 else '#10B981', height=0.62,
                 edgecolor='#1E293B', linewidth=0.5)
        ax1.text(max(cum, cum + v) + 0.6, ypos[i], f"{v:+d} p.p.", va='center', fontsize=7.4, fontweight='bold')
        cum += v
    ax1.barh(ypos[-1], cum, color='#7F1D1D', height=0.62, edgecolor='#1E293B', linewidth=0.5)
    ax1.text(cum + 0.6, ypos[-1], f"{cum:.0f}%", va='center', fontsize=9, fontweight='bold', color='#7F1D1D')
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(short, fontsize=6.4)
    ax1.set_xlim(0, 48)
    ax1.set_xlabel("Probabilidade (%)", fontsize=8)
    ax1.set_title("Da taxa-base histórica à probabilidade atual de bear market", fontsize=9, fontweight='bold')
    ax1.grid(True, axis='x')

    # Distribuição dos 4 cenários
    ax2.set_facecolor('#FAFAFA')
    names = ["S0\n< 10%", "S1\n10% a 20%", "S2\n20% a 35%", "S3\n> 35%"]
    probs = [s[3] for s in SCENARIOS]
    cols = ['#10B981', '#F59E0B', '#EA580C', '#7F1D1D']
    bars = ax2.bar(names, probs, color=cols, width=0.62, edgecolor='#1E293B', linewidth=0.5)
    for b, p in zip(bars, probs):
        ax2.annotate(f"{p:.0f}%", xy=(b.get_x() + b.get_width() / 2, p), xytext=(0, 3), textcoords='offset points',
                     ha='center', fontsize=9, fontweight='bold')
    ax2.set_ylim(0, 42)
    ax2.set_xlabel("Queda máxima do S&P 500 (pico a vale)", fontsize=8)
    ax2.set_title("Distribuição dos 4 cenários (2 anos)", fontsize=9, fontweight='bold')
    ax2.tick_params(axis='x', labelsize=7.2)
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _finish(fig, path, "Gráfico 4 (probabilidades)")


def chart_composition(d, path="chart_crash_composition.png"):
    setup_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.4), gridspec_kw={'width_ratios': [1.25, 1]})
    fig.patch.set_facecolor('white')

    # Esquerda: atribuição por canal (pontos percentuais de queda)
    ax1.set_facecolor('#FAFAFA')
    sids = ["S1", "S2", "S3"]
    totals = [-d["scen"][s]["total"] for s in sids]
    xl = [f"{s}\n{n}" for s, n in zip(sids, ["Correção /\nestagflação", "Bear market\nciclo + crédito", "Crash\nsistêmico"])]
    bottoms = np.zeros(3)
    for ci, (cname, ccol) in enumerate(CHANNELS):
        vals = np.array([ATTRIB[s][ci] / 100.0 * t for s, t in zip(sids, totals)])
        ax1.bar(xl, vals, bottom=bottoms, color=ccol, width=0.55, edgecolor='white', linewidth=0.8, label=cname)
        for i, v in enumerate(vals):
            if v >= 2.2:
                ax1.text(i, bottoms[i] + v / 2, f"{v:.1f}", ha='center', va='center', fontsize=7,
                         color='white', fontweight='bold')
        bottoms += vals
    for i, (s, t) in enumerate(zip(sids, totals)):
        loss = d["scen"][s]["loss_tn"]
        ax1.text(i, t + 1.2, f"-{t:.0f}%  (~US$ {loss:.0f} tri)", ha='center', fontsize=8, fontweight='bold')
    ax1.set_ylim(0, 66)
    ax1.set_ylabel("Queda do S&P 500 (pontos percentuais)", fontsize=8)
    ax1.set_title("Anatomia da queda: quem contribui com quantos pontos", fontsize=9, fontweight='bold')
    ax1.tick_params(axis='x', labelsize=7)
    ax1.legend(loc='upper left', fontsize=5.8, frameon=True, facecolor='white', edgecolor='#CBD5E1')
    ax1.grid(True, axis='y')

    # Direita: preço = P/E x lucros
    ax2.set_facecolor('#FAFAFA')
    w = 0.26
    xs = np.arange(3)
    pe = [d["scen"][s]["pe_chg"] for s in sids]
    eps = [d["scen"][s]["eps"] for s in sids]
    tot = [d["scen"][s]["total"] for s in sids]
    ax2.bar(xs - w, pe, w, label="Compressão do P/E", color='#1E3A8A', edgecolor='#0F172A', linewidth=0.5)
    ax2.bar(xs, eps, w, label="Queda dos lucros (LPA)", color='#F59E0B', edgecolor='#92400E', linewidth=0.5)
    ax2.bar(xs + w, tot, w, label="Preço (P/E x LPA)", color='#7F1D1D', edgecolor='#450A0A', linewidth=0.5)
    for i in range(3):
        for off, v in [(-w, pe[i]), (0, eps[i]), (w, tot[i])]:
            lbl = f"{v:.1f}%" if abs(v) < 1 else f"{v:.0f}%"
            ax2.text(i + off, v - 1.5, lbl, ha='center', va='top', fontsize=6.8, fontweight='bold')
    ax2.set_xticks(xs)
    ax2.set_xticklabels([f"{s}\nP/E {FACTS['spx_fwd_pe']}x -> {DECOMP[s]['pe_to']}x" for s in sids], fontsize=6.6)
    ax2.set_ylim(-62, 4)
    ax2.axhline(0, color='#334155', linewidth=0.8)
    ax2.set_title("Mecânica: múltiplo vs lucros", fontsize=9, fontweight='bold')
    ax2.legend(loc='lower left', fontsize=6.4, frameon=True, facecolor='white', edgecolor='#CBD5E1')
    ax2.grid(True, axis='y')

    plt.tight_layout()
    _finish(fig, path, "Gráfico 5 (composição do crash)")


def _prepare_map(rows, gdf):
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ADM0_A3", "score", "dom", "SUBREGION", "factors"])
    g = gdf.merge(df[["ADM0_A3", "score", "dom"]], on="ADM0_A3", how="left")
    g = g[g["ADM0_A3"] != "ATA"].to_crs("+proj=robin")
    return g


# (lon_alvo, lat_alvo, lon_texto, lat_texto): se texto != alvo, desenha chamada externa com linha
MAP_LABELS = {
    "USA": (-98, 38, -98, 38), "CAN": (-100, 58, -100, 58), "MEX": (-102, 24, -118, 17),
    "BRA": (-53, -10, -53, -10), "ARG": (-65, -37, -48, -45),
    "GBR": (-2, 53.5, -26, 58), "FRA": (2.5, 46.5, -22, 45), "DEU": (10.3, 51.2, 8, 64),
    "ITA": (12.5, 42.5, 17, 34.5), "TUR": (35, 39, 38, 43.5), "IRN": (54, 32.5, 54, 32.5),
    "SAU": (45, 24, 52, 5), "EGY": (30, 26.5, 18, 19), "IND": (79, 22, 79, 22),
    "PAK": (69, 30, 66, 16), "CHN": (103, 35, 103, 35), "JPN": (138, 37, 152, 44),
    "KOR": (128, 36.4, 148, 31), "TWN": (121, 23.7, 140, 18), "RUS": (95, 61, 95, 61),
    "AUS": (134, -25, 134, -25), "ZAF": (24.5, -29, 24.5, -29), "NGA": (8, 9, 8, 9),
    "UKR": (31, 49, 39, 53),
}


def chart_map_severity(rows, path="chart_map_vulnerability.png"):
    setup_chart_style()
    gdf = gpd.read_file(GEOJSON)
    g = _prepare_map(rows, gdf)
    cmap = LinearSegmentedColormap.from_list(
        "risk", ["#FFF7BC", "#FEC44F", "#FE9929", "#EC5E14", "#CC1F1F", "#7F0A2B", "#3B0A45"])
    norm = Normalize(vmin=20, vmax=80)

    fig, ax = plt.subplots(figsize=(11, 5.9))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#EAF2F8')
    g.plot(ax=ax, color='#D1D5DB', edgecolor='white', linewidth=0.3)
    g_valid = g.dropna(subset=["score"])
    g_valid.plot(column="score", ax=ax, cmap=cmap, norm=norm, edgecolor='white', linewidth=0.35)

    tr = Transformer.from_crs("EPSG:4326", "+proj=robin", always_xy=True)
    score_map = dict(zip(g_valid["ADM0_A3"], g_valid["score"]))
    for a3, (lon, lat, tlon, tlat) in MAP_LABELS.items():
        if a3 in score_map:
            x, y = tr.transform(lon, lat)
            tx, ty = tr.transform(tlon, tlat)
            nm = COUNTRY_PT.get(a3, a3)
            ax.annotate(f"{nm} {score_map[a3]:.0f}", xy=(x, y), xytext=(tx, ty), ha='center', va='center',
                        fontsize=5.8, fontweight='bold', color='#111827',
                        bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='#94A3B8', lw=0.4, alpha=0.92),
                        arrowprops=None if (lon, lat) == (tlon, tlat) else
                        dict(arrowstyle='-', lw=0.5, color='#334155', shrinkA=0, shrinkB=0))
    ax.set_axis_off()
    ax.set_title("Mapa de Vulnerabilidade Global a uma Quebra do Mercado Financeiro (índice composto 0-100)",
                 fontsize=11, fontweight='bold', color='#0F172A', pad=8)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.035, pad=0.02, aspect=50)
    cbar.set_label("Baixa vulnerabilidade  <--  índice composto  -->  Alta vulnerabilidade", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    ax.text(0.01, 0.02, "Cinza: sem dados (ex.: Groenlândia). Países pequenos (Singapura, Bahrein, Hong Kong) não aparecem na base 110m.",
            transform=ax.transAxes, fontsize=6.2, color='#475569')
    _finish(fig, path, "Gráfico 6 (mapa de vulnerabilidade)")
    return g_valid


def chart_map_channels(rows, path="chart_map_channels.png"):
    setup_chart_style()
    gdf = gpd.read_file(GEOJSON)
    g = _prepare_map(rows, gdf)
    fig, ax = plt.subplots(figsize=(11, 5.9))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#EAF2F8')
    g.plot(ax=ax, color='#D1D5DB', edgecolor='white', linewidth=0.3)
    cols = []
    for _, r in g.iterrows():
        if r["dom"] is None or (isinstance(r["dom"], float) and np.isnan(r["dom"])):
            cols.append(to_rgba('#D1D5DB'))
        else:
            alpha = float(np.clip(0.35 + (r["score"] - 20) / 60 * 0.65, 0.35, 1.0))
            cols.append(to_rgba(CHANNEL_COLORS[r["dom"]], alpha))
    g.plot(ax=ax, color=cols, edgecolor='white', linewidth=0.35)
    ax.set_axis_off()
    ax.set_title("Por onde o choque entra: canal de transmissão dominante por país (intensidade = gravidade)",
                 fontsize=11, fontweight='bold', color='#0F172A', pad=8)
    present = {r["dom"] for _, r in g.iterrows() if isinstance(r["dom"], str)}
    handles = [Patch(color=CHANNEL_COLORS[k], label=FACTOR_NAMES[k]) for k in FACTOR_KEYS if k in present]
    ax.legend(handles=handles, loc='lower left', fontsize=7, frameon=True, facecolor='white', edgecolor='#CBD5E1',
              title="Canal dominante", title_fontsize=7.5)
    _finish(fig, path, "Gráfico 7 (mapa de canais)")


def chart_region_ranking(rows, path="chart_region_ranking.png"):
    setup_chart_style()
    by_region = {}
    for a3, score, dom, sub, _ in rows:
        if np.isnan(score):
            continue
        by_region.setdefault(sub, []).append(score)
    items = sorted(((REGION_PT.get(k, k), float(np.mean(v)), len(v)) for k, v in by_region.items()),
                   key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#FAFAFA')
    cmap = LinearSegmentedColormap.from_list(
        "risk", ["#FFF7BC", "#FEC44F", "#FE9929", "#EC5E14", "#CC1F1F", "#7F0A2B", "#3B0A45"])
    norm = Normalize(vmin=20, vmax=80)
    names = [i[0] for i in items]
    vals = [i[1] for i in items]
    ax.barh(names, vals, color=[cmap(norm(v)) for v in vals], edgecolor='#1E293B', linewidth=0.5)
    for i, (n, v, c) in enumerate(items):
        ax.text(v + 0.6, i, f"{v:.0f}", va='center', fontsize=7.5, fontweight='bold')
    ax.set_xlim(0, 80)
    ax.set_xlabel("Índice médio de vulnerabilidade (0-100; média simples dos países da região)", fontsize=8)
    ax.set_title("Ranking regional: quem sofre mais num cenário de crash sistêmico (S3)", fontsize=10, fontweight='bold')
    ax.tick_params(axis='y', labelsize=7.5)
    ax.grid(True, axis='x')
    plt.tight_layout()
    _finish(fig, path, "Gráfico 8 (ranking regional)")
    return items


# ---------------------------------------------------------
# 4. CANVAS COM NUMERAÇÃO
# ---------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
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
            self.drawString(54, 750, "MACRO & GEOPOLÍTICA • RISCO DE QUEBRA 2026-2028")
            self.setFont("Helvetica", 7.6)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "FISCAL EUA • ELEIÇÕES • MAPA DE VULNERABILIDADE")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 612 - 54, 742)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 45, 612 - 54, 45)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Análise informativa, não é recomendação de investimento • Dados coletados em 11/10/2026 • Probabilidades = julgamento analítico")
        self.drawRightString(612 - 54, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()


# ---------------------------------------------------------
# 5. PDF
# ---------------------------------------------------------
def _img(path, width_in):
    p = get_chart_path(os.path.basename(path), lang="pt")
    iw, ih = ImageReader(p).getSize()
    w = width_in * inch
    return Image(p, width=w, height=w * ih / iw)


def build_pdf_report(d, rows, ranking, output_filename):
    f = FACTS
    pdf_out = get_report_pt_path(os.path.basename(output_filename))
    doc = SimpleDocTemplate(pdf_out, pagesize=letter, leftMargin=54, rightMargin=54,
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

    # ================= PÁGINA 1: CAPA =================
    hdr = Table([[Paragraph("<b>RELATÓRIO ESTRATÉGICO: FISCAL EUA, ELEIÇÕES, GUERRAS E RISCO DE QUEBRA</b>",
                            ParagraphStyle('hh', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#DC2626'))),
                  Paragraph(f"Data: {REPORT_DATE} | Horizonte: out/2026 - out/2028",
                            ParagraphStyle('hd', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#64748B'), alignment=2))]],
                colWidths=[310, 194])
    hdr.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    story += [hdr, Spacer(1, 4)]
    story.append(P("Anatomia de uma Possível Quebra do Mercado (2026-2028) e Mapa Mundial de Vulnerabilidade", 'title'))
    story.append(Spacer(1, 2))
    story.append(P("Situação financeira do governo dos EUA, influência das eleições, guerras e canais de contágio global, "
                   "incorporando dados de fontes oficiais coletados em 11/10/2026", 'sub'))
    story.append(Spacer(1, 6))

    def kpi(title, big, small, col):
        return Paragraph(f"<b>{title}</b><br/><font size=9.5 color='{col}'><b>{big}</b></font><br/>"
                         f"<font size=6.2 color='#475569'>{small}</font>", S['td'])
    k1 = [kpi("DÍVIDA FEDERAL", f"US$ {f['debt_total_tn']:.2f} tri", "Treasury, 08/10/26", '#1E3A8A'),
          kpi("DÉFICIT FY26", f"US$ {f['deficit_fy26_tn']:.1f} tri", f"{f['deficit_fy26_pct']}% do PIB", '#DC2626'),
          kpi("JUROS LÍQUIDOS", "US$ 1.0-1.1 tri", "3.3-3.4% do PIB / ano", '#F59E0B'),
          kpi("TREASURY 10Y / 30Y", f"{f['ust10']}% / {f['ust30_auction']}%", "30Y: maior nível desde 2002", '#7C3AED'),
          kpi("FED FUNDS", f"{f['fed_low']:.2f}-{f['fed_high']:.2f}%", "ALTA de 25 pb em 16/09", '#475569')]
    k2 = [kpi("S&P 500 / VIX", f"{f['spx']:,.0f} / {f['vix']}", "perto da máxima histórica", '#0D9488'),
          kpi("SHILLER CAPE", f"~{f['cape']:.0f}x", "2º maior da história (1999: 44x)", '#DC2626'),
          kpi("BRENT", f"> US$ {f['brent']}", "guerra EUA-Israel x Irã, mês 8", '#EA580C'),
          kpi("CPI / DESEMPREGO", f"{f['cpi_aug']}% / {f['unemp']}%", f"payroll set: +{f['payroll_sep_k']} mil", '#B91C1C'),
          kpi("OURO (spot)", f"US$ {f['gold']:,.0f}", "08-09/out/2026", '#B45309')]
    kt = Table([k1, k2], colWidths=[100.8] * 5)
    kt.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
                            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
                            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                            ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    story += [kt, Spacer(1, 6)]

    story.append(box(
        "<b>SÍNTESE EXECUTIVA:</b> o mercado acionário dos EUA negocia em máximas históricas (VIX "
        f"{f['vix']}) enquanto o pano de fundo se deteriorou: <b>(1)</b> o governo americano tem déficit de "
        f"{f['deficit_fy26_pct']}% do PIB fora de recessão e dívida de US$ {f['debt_total_tn']:.1f} tri; <b>(2)</b> o Fed está "
        "<b>subindo</b> juros com inflação de 3.4-3.7% e mercado de trabalho fraco (+29 mil vagas), o que reduz sua capacidade de "
        "'resgatar' o mercado; <b>(3)</b> o rendimento de lucros do S&P 500 "
        f"({d['earnings_yield']:.2f}%) está <b>abaixo</b> do Treasury de 10 anos ({f['ust10']}%); <b>(4)</b> há guerra ativa afetando ~20% do "
        "petróleo e do GNL do mundo; <b>(5)</b> as eleições de 3/nov e uma janela de 4 semanas com FMI, CPI, FOMC e orçamento britânico "
        "concentram gatilhos. Nossa estimativa: <b>probabilidade de uma queda de 20% ou mais no S&P 500 dentro de 2 anos de "
        f"~{d['p_ge20']:.0f}%</b> (taxa-base histórica ~{BASE_RATE_BEAR_2Y:.0f}%), e <b>~{SCENARIOS[3][3]:.0f}%</b> de um crash sistêmico "
        "(> 35%). Os mais afetados seriam Japão/Coreia/Taiwan, Sul da Ásia importador de energia, Oriente Médio em guerra, "
        "Turquia/Egito, Europa com dívida elevada e os EUA em perda absoluta de riqueza.",
        '#EFF6FF', '#93C5FD'))
    story.append(Spacer(1, 6))

    story += h1("O que mudou em relação aos relatórios anteriores do repositório")
    chg = [[P("<b>Premissa anterior</b>", 'th'), P("<b>Dados de 11/10/2026</b>", 'th'), P("<b>Implicação</b>", 'th')],
           [P("Dívida dos EUA de ~US$ 40 tri", 'td'),
            P(f"<b>Confirmada:</b> US$ {f['debt_total_tn']:.2f} tri (público: {f['debt_public_tn']:.2f}).", 'td'),
            P("Sem revisão; a dinâmica de juros agrava o peso.", 'td')],
           [P("'Juros em 5.25%' e Fed podendo cortar em emergência", 'td'),
            P("10Y = 5.24%, mas <b>Fed funds 3.75-4.00% após ALTA em set/26</b>, com CPI em 3.4% e subindo.", 'td'),
            P("O 'Fed put' está mais restrito (estagflação): eleva a cauda do cenário sistêmico.", 'td')],
           [P("Estresse nos leilões do Tesouro como gatilho do Cenário 3", 'td'),
            P(f"Leilão de 30Y de 08/10 foi <b>sólido</b> (bid-to-cover {f['btc_30y']}, indiretos {f['indirect_30y']}%), a "
              f"{f['ust30_auction']}%.", 'td'),
            P("Gatilho segue vivo, mas não disparou; monitorar caudas de leilão.", 'td')],
           [P("3 cenários, todos com correção (48/34/18% em 3 anos)", 'td'),
            P("Modelo atual inclui estado sem correção relevante (S0) e janela de 2 anos.", 'td'),
            P("Corrige viés: P(queda >= 20%) em 2 anos = " + f"{d['p_ge20']:.0f}%.", 'td')],
           [P("Foco em IA/crédito privado", 'td'),
            P("Novos vetores: guerra/energia, carry do iene, hedge funds ($13 tri, FMI), CRE de escritórios acima de 2008, "
              "França/Reino Unido.", 'td'),
            P("Risco é <b>macro-financeiro</b>, não só do ciclo de IA.", 'td')]]
    story.append(table(chg, [130, 215, 159], valign='TOP'))
    story.append(PageBreak())

    # ================= PÁGINA 2: FISCAL =================
    story += h1("1. Situação Financeira do Governo dos EUA")
    story.append(P(
        f"O Tesouro reporta dívida total de <b>US$ {f['debt_total_tn']:.2f} tri</b> (08/10/2026), dos quais "
        f"<b>US$ {f['debt_public_tn']:.2f} tri</b> em mãos do público (~{d['debt_gdp_calc']:.0f}% do PIB estimado; CBO: "
        f"{f['debt_gdp_2026']}% em 2026, rumo a {f['debt_gdp_2036']}% em 2036). O déficit do FY2026 ficou em ~US$ 2.0 tri "
        f"(6.2% do PIB), acima da linha de base do CBO de fevereiro (US$ 1.9 tri; 5.8%). Os <b>juros líquidos (US$ 1.0-1.1 tri)</b> já "
        "superam gastos com defesa ou Medicare individualmente.", 'body'))
    story.append(_img("chart_us_fiscal_dashboard.png", 6.8))
    story.append(P("Fontes: Treasury Fiscal Data (Debt to the Penny), CBO (baseline fev/2026), CRFB, American Action Forum, FOMC, YCharts/"
                   "TradingEconomics (juros), Bank of Japan/mercado (JGB), imprensa financeira (gilts). Cartões: cálculos próprios.", 'cap'))
    story.append(P("<b>Diagnóstico:</b>", 'bold'))
    story.append(P(
        "• <b>Déficit fora de recessão:</b> 6.2% do PIB com desemprego de 4.2% e PIB de 2.2% (2T26) significa que o governo não tem "
        "'gordura' para absorver uma recessão: numa queda forte, a receita cai e o déficit tende a ultrapassar US$ 3 tri.<br/>"
        f"• <b>Aritmética do refinanciamento:</b> a taxa efetiva implícita da dívida em mãos do público é de ~{d['effective_rate']:.1f}% "
        f"(juros líquidos / dívida), enquanto novas emissões de 30 anos saem a {f['ust30_auction']}%. Cada +100 pb, quando toda a dívida "
        f"for reprecificada, custa ~US$ {d['plus100bp_bn']:.0f} bi por ano (cálculo mecânico; a reprecificação é gradual).<br/>"
        f"• <b>Compradores externos em retirada gradual:</b> Japão detém US$ {f['japan_ust_tn']:.2f} tri (jul/26) e vem reduzindo, em parte "
        f"para defender o iene; a China caiu para ~US$ {f['china_ust_tn']*1000:.0f} bi. A base compradora se ampliou (Reino Unido/centros "
        "custodiantes, Canadá, Cayman), mas é mais sensível a preço.<br/>"
        "• <b>Fed sob pressão política:</b> Kevin Warsh preside o Fed desde 22/05/2026; há atritos públicos com a Casa Branca, inclusive a "
        "tentativa de afastar a governadora Lisa Cook. Powell segue como governador até 31/01/2028. Percepção de perda de independência "
        "tende a elevar o prêmio de prazo.<br/>"
        "• <b>Mitigante importante:</b> o leilão de 30Y (08/10) teve demanda forte; o sistema ainda absorve emissão, a um preço mais alto.",
        'body'))
    story.append(PageBreak())

    # ================= PÁGINA 3: MERCADO =================
    story += h1("2. Mercado Acionário: Valuation, Juros e Concentração")
    story.append(P(
        f"O S&P 500 fechou em {f['spx']:,.2f} e o Nasdaq em {f['ixic']:,.2f} (09/10/2026), perto das máximas. As métricas de avaliação estão em "
        f"níveis só comparáveis a 1999: <b>Shiller CAPE ~{f['cape']:.0f}x</b> (pico de 1999: 44.2x), <b>Indicador Buffett ~{f['buffett_pct']}% do PIB</b> e "
        f"<b>top-10 = {f['top10_weight']}% do índice</b> (Nvidia + Apple + Microsoft > {f['top3_weight']}%, a maior concentração de três ações já registrada).",
        'body'))
    story.append(_img("chart_valuation_vs_rates.png", 6.8))
    story.append(P("Valores de CAPE em topos históricos são aproximados (série de Robert Shiller/Yale). Rendimento de lucros usa o P/E forward de 23.4x "
                   "do dossiê anterior. CAPE é indicador de retorno de longo prazo, não de timing.", 'cap'))
    story.append(P("<b>Três leituras críticas:</b>", 'bold'))
    story.append(P(
        f"1. <b>Prêmio de risco de ações negativo.</b> O rendimento de lucros ({d['earnings_yield']:.2f}%) está {abs(d['erp_vs_10y']):.2f} p.p. abaixo do "
        f"Treasury de 10 anos ({f['ust10']}%). O 10Y real é de ~{d['real_10y']:.1f}% (10Y menos CPI de {f['cpi_aug']}%). Investidores aceitam menos "
        "que a renda 'sem risco' na expectativa de crescimento de lucros; se o crescimento falhar, o ajuste é via preço.<br/>"
        f"2. <b>Curva íngreme pela ponta longa.</b> 10Y está {d['curve_10y_ff']:.2f} p.p. acima do Fed funds: o mercado exige prêmio de prazo (fiscal + "
        "inflação), e não é o Fed quem controla essa taxa. É o padrão de estresse de 'bear steepening'.<br/>"
        "3. <b>Amplitude fraca sob o índice.</b> Relatos indicam que muitas ações estão abaixo da média de 50 dias e com retorno negativo no ano: "
        "o índice depende de poucos líderes. Isso torna o S&P mais frágil a uma única decepção (ex.: capex de IA).",
        'body'))
    story.append(box(
        "<b>Sobre o VIX em 14.84:</b> nível baixo diante de guerra ativa, 30Y a 5.6% e CAPE a 41x indica que o mercado precifica um desfecho benigno. "
        "Isso não prevê queda, mas reduz o 'colchão' de proteção barata e aumenta a convexidade negativa se houver choque: "
        "nos episódios de 2000, 2008 e 2022, a volatilidade era baixa/moderada antes do início das perdas.",
        '#FFFBEB', '#FCD34D'))
    story.append(PageBreak())

    # ================= PÁGINA 4: ELEIÇÕES =================
    story += h1("3. A Influência das Eleições nos Mercados")
    story.append(P(
        "A literatura histórica é consistente: o <b>ano de eleição de meio de mandato é o mais fraco do ciclo presidencial</b> (retorno médio do "
        "S&P 500 de ~3-5%, drawdown intra-ano médio de ~17-19% versus ~12-13% em outros anos), seguido de <b>recuperação forte nos 12 meses "
        "posteriores</b> (média de ~13-16%; raramente negativo desde 1946). Em 2026 o padrão sazonal não ocorreu até agora: o índice está em máxima. "
        "Isso pode significar que a 'dor sazonal' ainda está por vir, ou que o ciclo de lucros de IA a neutralizou; as séries históricas "
        "são compilações de analistas (confiança média) e amostra pequena (cerca de 20 observações).", 'body'))
    story.append(_img("chart_triggers_timeline.png", 6.8))
    story.append(P("<b>Mapa de eleições e eventos políticos relevantes:</b>", 'bold'))
    el = [[P("<b>Evento</b>", 'th'), P("<b>Data</b>", 'th'), P("<b>Por que importa para o mercado</b>", 'th'),
           P("<b>Efeito esperado</b>", 'th')],
          [P("EUA: eleições de meio de mandato", 'td'), P("03/11/2026", 'td'),
           P("Democratas bem posicionados para virar a Câmara; Senado (53-47 R) competitivo. Congresso dividido = menos legislação nova "
             "(inclusive corte de impostos), mais fiscalização e risco de impasse de orçamento/teto da dívida. Tarifas e política externa "
             "continuam com o Executivo.", 'td'),
           P("Resolução da incerteza costuma ajudar; risco é fiscal/institucional", 'td')],
          [P("Risco de evento geopolítico pré-eleitoral", 'td'), P("Out-nov/2026", 'td'),
           P("Relatos (08/10) de que a Casa Branca pediu opções de ataque ao Irã antes da eleição; acordo anunciado para importar diesel "
             "russo para baixar preços. Combustível é tema eleitoral.", 'td'),
           P("Volatilidade de petróleo e de inflação", 'td')],
          [P("Brasil: 2º turno presidencial", 'td'), P("25/10/2026", 'td'),
           P(f"Flávio Bolsonaro surpreendeu no 1º turno (Ibovespa ~+8%, real ~+4%). Dívida ~{f['brazil_debt_gdp']}% do PIB, juros "
             f"de {f['brazil_interest_gdp']}% do PIB, Selic {f['brazil_selic']}%.", 'td'),
           P("Choque local, com efeito regional na América Latina", 'td')],
          [P("Reino Unido: Orçamento", 'td'), P("28/10/2026", 'td'),
           P(f"Gilt de 30Y a ~{f['gilt30']}% (maior desde 1998); credibilidade fiscal em teste.", 'td'),
           P("Contágio em títulos globais", 'td')],
          [P("França: eleição presidencial", 'td'), P("abr-mai/2027", 'td'),
           P(f"Spread OAT-Bund ~{f['fr_bund_bp']} pb, o maior desde 2011-12; déficit alto e incerteza política; TPI do BCE de uso complicado.", 'td'),
           P("Principal ponto de estresse soberano da zona do euro", 'td')],
          [P("EUA: eleição presidencial", 'td'), P("07/11/2028", 'td'),
           P("Logo após o horizonte; mas a campanha de 2028 amplifica populismo fiscal e pressão sobre o Fed a partir de 2027.", 'td'),
           P("Risco de prêmio de prazo em alta", 'td')]]
    story.append(table(el, [95, 55, 250, 104], valign='TOP'))
    story.append(PageBreak())

    # ================= PÁGINA 5: GUERRAS =================
    story += h1("4. Guerras e Geopolítica: Os Quatro Teatros de Risco")
    story.append(P(
        "Os conflitos afetam o mercado por quatro canais: <b>energia/inflação</b> (que trava os bancos centrais), <b>cadeias de suprimento</b> "
        "(semicondutores), <b>fluxo de capital</b> (fuga para o dólar) e <b>fiscal</b> (gastos de defesa e subsídios).", 'body'))
    war = [[P("<b>Teatro</b>", 'th'), P("<b>Situação em out/2026</b>", 'th'), P("<b>Canal de transmissão</b>", 'th'),
            P("<b>Gravidade p/ mercado</b>", 'th')],
           [P("<b>EUA-Israel x Irã / Estreito de Hormuz</b>", 'td'),
            P("Guerra no 8º mês. ~20% do petróleo e do GNL mundiais transitam por Hormuz; ataques a petroleiros no pico de frequência; "
              f"Brent > US$ {f['brent']}; estoques globais nas mínimas em décadas; liberação coordenada de reservas (IEA/G7) com eficácia limitada; "
              "escassez de diesel/jet com 'crack spreads' recordes. (Fontes divergem entre 'fechamento' e 'ataques/interrupção severa'.)", 'td'),
            P("Inflação, juros altos por mais tempo, margens de empresas, déficit externo dos importadores (Ásia, Europa, Sul da Ásia). "
              "Gás: competição Europa x Ásia.", 'td'),
            P("<font color='#DC2626'><b>MUITO ALTA</b></font><br/>(já em curso)", 'td')],
           [P("<b>Rússia x Ucrânia</b>", 'td'),
            P("Drones ucranianos degradam refino russo; crise de combustíveis na Rússia; acordo de diesel Trump-Putin visto com ceticismo.", 'td'),
            P("Oferta global de derivados; segurança energética europeia; gasto fiscal em defesa.", 'td'),
            P("<font color='#D97706'><b>ALTA</b></font><br/>(crônico)", 'td')],
           [P("<b>China-Taiwan</b>", 'td'),
            P(f"Cúpula Trump-Xi estendeu a trégua comercial; China institucionalizou 'quarentenas' marítimas; EUA veem invasão improvável antes de "
              f"2028. Taiwan/TSMC produz >{f['tsmc_adv_share']}% dos chips mais avançados (73% do mercado de foundry).", 'td'),
            P("Cadeia de IA/semicondutores (Nvidia, Apple, hyperscalers), seguros marítimos, sanções cruzadas.", 'td'),
            P("<font color='#B91C1C'><b>CAUDA</b></font><br/>(baixa prob., impacto extremo)", 'td')],
           [P("<b>Guerra comercial / tarifas</b>", 'td'),
            P("Truce prorrogada com a China; política tarifária é decisão do Executivo, imune à mudança do Congresso.", 'td'),
            P("Inflação importada, margens, cadeias de suprimento, relações comerciais.", 'td'),
            P("<font color='#D97706'><b>MÉDIA</b></font>", 'td')]]
    story.append(table(war, [90, 190, 150, 74], valign='TOP'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Como a guerra se conecta ao risco financeiro (cadeia causal):</b>", 'bold'))
    story.append(box(
        "<b>Petróleo/derivados altos</b> -> <b>CPI sobe</b> (esperado 3.6-3.7% em setembro) -> <b>Fed sobe juros</b> (já subiu em 16/09) mesmo com "
        "payroll fraco -> <b>juros longos sobem</b> (10Y 5.24%, 30Y ~5.6%) -> <b>múltiplos de ações e preços de imóveis comerciais caem</b> -> "
        "<b>estresse em crédito privado, bancos regionais (US$ 396 bi de CRE vencendo) e hedge funds alavancados</b> -> <b>prejuízos e vendas "
        "forçadas</b> -> Fed preso entre inflação e estabilidade financeira. É o padrão de 1973-74 e 2022, agravado por dívida pública de 100% do PIB.",
        '#FEF2F2', '#F87171'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Vetores de contágio adicionais identificados:</b>", 'bold'))
    story.append(P(
        f"• <b>Carry do iene:</b> JGB 10Y em {f['jgb10']:.2f}%; investidores japoneses sob pressão para repatriar capital; um fortalecimento brusco do iene "
        "pode forçar liquidação de posições alavancadas em ações de tecnologia, mercados emergentes e títulos soberanos.<br/>"
        f"• <b>Hedge funds:</b> o Relatório de Estabilidade Financeira do FMI (out/2026) destaca ~US$ {f['hedge_funds_tn']} tri em ativos, alavancagem, posições "
        "concentradas e resgates correlacionados, com repasse via prime brokers.<br/>"
        f"• <b>Crédito privado e CRE:</b> restrições de resgate em veículos semilíquidos, 'amend-and-extend' em software exposto a IA; delinquência de CMBS de "
        f"escritórios em {f['cmbs_office_delinq']:.1f}% (12-13.2%), acima do pico de 2008; ~US$ {f['cre_maturity_bn']} bi vencendo em 2026, ~45% com bancos "
        "regionais/depositários.<br/>"
        f"• <b>Soberanos europeus:</b> França (spread ~{f['fr_bund_bp']} pb) e Reino Unido (gilt 30Y ~{f['gilt30']}%).", 'body'))
    story.append(PageBreak())

    # ================= PÁGINA 6: PROBABILIDADES =================
    story += h1("5. Composição de uma Possível Quebra: Probabilidades (2 anos)")
    story.append(P(
        f"Estimamos a probabilidade de queda de 20% ou mais no S&P 500 (pico a vale) no horizonte out/2026-out/2028 partindo da <b>taxa-base histórica de "
        f"~{BASE_RATE_BEAR_2Y:.0f}%</b> (cerca de 12-13 bear markets desde 1950, ~1 a cada 6 anos; Poisson para 2 anos) e somando ajustes de risco explícitos. "
        f"O resultado é <b>~{d['overlay_total']:.0f}%</b>. Os ajustes são julgamentos analíticos, não estimativas estatísticas: servem para tornar o "
        "raciocínio auditável e contestável.", 'body'))
    story.append(_img("chart_probability_buildup.png", 6.8))
    sc_rows = [[P("<b>Cenário</b>", 'th'), P("<b>Prob.</b>", 'th'), P("<b>Descrição e condição de ocorrência</b>", 'th')],
               [P("<b>S0</b> Continuação c/ volatilidade<br/>(queda máx. < 10%)", 'td'), P("<b>27%</b>", 'td'),
                P("Guerra se acalma, lucros de IA sustentam o índice, inflação cede em 2027 e o Fed pausa. Leilões continuam absorvendo emissão.", 'td')],
               [P("<b>S1</b> Correção / estagflação branda<br/>(10% a 20%)", 'td'), P("<b>33%</b>", 'td'),
                P("10Y permanece em 5-5.8%, petróleo alto; P/E comprime de 23.4x para ~20x. Sazonalidade de meio de mandato. Sem quebra de crédito.", 'td')],
               [P("<b>S2</b> Bear market de ciclo + crédito<br/>(20% a 35%)", 'td'), P("<b>25%</b>", 'td'),
                P("Digestão do capex de IA + 10Y acima de 6% + estresse no crédito privado/CRE. Lucros caem ~9%, P/E vai a ~18x.", 'td')],
               [P("<b>S3</b> Crash sistêmico<br/>(> 35%; central -48%)", 'td'), P("<b>15%</b>", 'td'),
                P("Confluência: rota nos Treasuries longos (credibilidade fiscal/Fed), desmonte do carry do iene, desalavancagem de hedge funds, "
                  "bancos regionais com CRE, crédito de IA e escalada militar (Taiwan como acelerador). Lucros caem ~16%, P/E ~14.5x.", 'td')]]
    story.append(table(sc_rows, [150, 40, 314], valign='TOP'))
    story.append(P(f"P(queda >= 10%) = {d['p_ge10']:.0f}%  |  P(>= 20%) = {d['p_ge20']:.0f}%  |  P(> 35%) = {SCENARIOS[3][3]:.0f}%. "
                   "Para comparação, o dossiê anterior estimava 52% de 'correção média a severa' em 3 anos (definição diferente).", 'cap'))
    story.append(PageBreak())

    # ================= PÁGINA 7: COMPOSIÇÃO =================
    story += h1("6. Anatomia da Queda: Quanto Cada Fator Contribui")
    story.append(P(
        "Preço = P/E x Lucro por ação. Para cada cenário definimos a compressão de múltiplo e a queda de lucros (barra direita) e atribuímos a queda "
        "total a seis canais de risco (barra esquerda). A <b>perda de riqueza</b> estima o valor de mercado total das ações dos EUA em "
        f"~US$ {d['equity_cap_tn']:.0f} tri (Buffett {f['buffett_pct']}% x PIB implícito de ~US$ {d['gdp_tn']:.0f} tri).", 'body'))
    story.append(_img("chart_crash_composition.png", 6.8))
    s = d["scen"]
    story.append(P(
        f"<b>Leitura:</b> em S3 a perda de ~US$ {s['S3']['loss_tn']:.0f} tri equivale a quase toda a dívida federal (US$ {f['debt_total_tn']:.0f} tri). "
        f"A atribuição muda com a gravidade: em S1 dominam juros longos e IA (55%); em S3, o <b>crédito e a liquidez</b> passam a ser o maior bloco "
        f"(28%) porque é a alavancagem, e não a avaliação em si, que transforma correção em crash. Em S2/S3 o 'hedge' clássico de títulos pode falhar "
        "no início (ações e Treasuries caindo juntos, como em 2022), pois o choque nasce na própria ponta longa.", 'body'))
    ass = [[P("<b>Indicador (ilustrativo)</b>", 'th'), P("<b>Hoje</b>", 'th'), P("<b>S1</b>", 'th'), P("<b>S2</b>", 'th'), P("<b>S3</b>", 'th')],
           [P("S&P 500 (pico a vale)", 'td'), P(f"{f['spx']:,.0f}", 'td'), P(f"~{f['spx']*(1+s['S1']['total']/100):,.0f}", 'td'),
            P(f"~{f['spx']*(1+s['S2']['total']/100):,.0f}", 'td'), P(f"~{f['spx']*(1+s['S3']['total']/100):,.0f}", 'td')],
           [P("Queda central / perda de riqueza", 'td'), P("-", 'td'), P(f"{s['S1']['total']:.0f}% / US$ {s['S1']['loss_tn']:.0f} tri", 'td'),
            P(f"{s['S2']['total']:.0f}% / US$ {s['S2']['loss_tn']:.0f} tri", 'td'), P(f"{s['S3']['total']:.0f}% / US$ {s['S3']['loss_tn']:.0f} tri", 'td')],
           [P("VIX (pico)", 'td'), P(f"{f['vix']}", 'td'), P("25-32", 'td'), P("35-50", 'td'), P("55-75", 'td')],
           [P("Treasury 10Y", 'td'), P(f"{f['ust10']}%", 'td'), P("5.0-5.8%", 'td'), P("sobe >6% e depois cai", 'td'),
            P("rota >6%, depois QE e corte (3.5-4.5%)", 'td')],
           [P("Spread High Yield", 'td'), P("(n/d)", 'td'), P("+100 a 150 pb", 'td'), P("+300 a 450 pb", 'td'), P("+600 a 900 pb", 'td')],
           [P("Brent", 'td'), P(f"> {f['brent']}", 'td'), P("90-125", 'td'), P("70-110 (demanda cai)", 'td'), P("60-130 (muito volátil)", 'td')],
           [P("Ouro (US$/oz)", 'td'), P(f"{f['gold']:,.0f}", 'td'), P("4,000-4,600", 'td'), P("4,300-5,200", 'td'), P("4,500-6,500 (liquidação inicial possível)", 'td')]]
    story.append(table(ass, [140, 60, 90, 100, 114]))
    story.append(P("Faixas de VIX, spreads, Brent e ouro são ilustrativas (analogias com 2000-02, 2008, 2020 e 2022), sem pretensão de previsão.", 'cap'))
    story.append(PageBreak())

    # ================= PÁGINA 8: MAPA 1 =================
    story += h1("7. Mapa Mundial: Regiões Mais Afetadas")
    story.append(P(
        "Construímos um <b>índice composto de vulnerabilidade (0-100)</b> por país, somando seis fatores (nota 0-10) ponderados: "
        "choque energético/Hormuz (25%), estresse fiscal e de títulos soberanos (20%), dólar forte e financiamento externo (15%), cadeia de "
        "tecnologia/IA/Taiwan (15%), contágio de mercados e crédito dos EUA (15%) e risco geopolítico direto (10%); países em zona de guerra recebem "
        "ajuste adicional (até +15). As notas por país são julgamento analítico baseado nos fatos da seção anterior (cada nota está no código).", 'body'))
    story.append(_img("chart_map_vulnerability.png", 6.8))
    story.append(P("Índice calculado para o cenário de estresse sistêmico (S3). Base cartográfica: Natural Earth 110m.", 'cap'))
    story.append(_img("chart_region_ranking.png", 6.4))
    story.append(PageBreak())

    # ================= PÁGINA 9: MAPA 2 + TOP PAÍSES =================
    story += h1("8. Canais de Transmissão e Países Mais Expostos")
    story.append(_img("chart_map_channels.png", 7.0))
    story.append(P("Cada país é colorido pelo fator com maior contribuição ponderada; quanto mais intensa a cor, maior a gravidade.", 'cap'))
    ranked = sorted([(a3, sc, dom, f_) for a3, sc, dom, _, f_ in rows if not np.isnan(sc) and a3 in COUNTRY_PT],
                    key=lambda t: -t[1])[:14]
    top = [[P("<b>#</b>", 'th'), P("<b>País</b>", 'th'), P("<b>Índice</b>", 'th'), P("<b>Canal dominante</b>", 'th'),
            P("<b>Por que está exposto</b>", 'th')]]
    why = {
        "JPN": "Importa 80-90% do petróleo via Hormuz; maior importador de GNL; JGB em 3.0%; carry do iene; cadeia de chips.",
        "IRN": "Zona de guerra direta; economia sob sanções e destruição de infraestrutura.",
        "TWN": "TSMC (>90% dos chips avançados); risco militar; dependência de energia importada.",
        "KOR": "Dependente de energia importada; exportador de memória/chips; mercado muito ligado à IA.",
        "PSX": "Zona de guerra; economia dependente de ajuda externa.",
        "ISR": "Participante direto do conflito; setor de tecnologia exposto a ciclo de IA.",
        "IRQ": "Exportações dependem de Hormuz; fiscal frágil; zona de instabilidade.",
        "PAK": "Importador de energia, dívida externa alta, depende de socorro do FMI.",
        "TUR": "Déficit energético, lira pressionada, reservas em queda.",
        "LKA": "Importador líquido de combustível, histórico recente de calote.",
        "EGY": "Importa energia e alimentos; fiscal e dólar pressionados; zona próxima ao conflito.",
        "IND": "~45% do petróleo e ~50% do GNL via Hormuz; déficit externo em alta.",
        "CHN": "Energia importada, setor imobiliário frágil, tecnologia e Taiwan.",
        "FRA": "Maior estresse soberano da zona do euro (spread ~150 pb); eleição 2027.",
        "GBR": "Gilt de 30Y a ~6% (máx. desde 1998); orçamento em 28/10; mercado muito ligado ao dos EUA.",
        "USA": "Epicentro: déficit 6.2% do PIB, 10Y 5.2%, CAPE 41x, concentração; maior perda absoluta em US$.",
        "BGD": "Importador de energia, reservas e dólar apertados.",
        "SYR": "Zona de conflito.", "LBN": "Zona de conflito e colapso bancário.", "YEM": "Zona de guerra.",
        "KWT": "Exportações bloqueadas por Hormuz.", "QAT": "GNL bloqueado por Hormuz.",
        "ARG": "Dívida e dólar: fragilidade externa crônica.", "BRA": "Fiscal (dívida ~70% do PIB, juros 7.3% do PIB), mas é exportador de commodities.",
        "DEU": "Energia cara e indústria exportadora; ligação com a cadeia de tecnologia.",
        "ITA": "Dívida elevada e dependência de energia.",
    }
    for i, (a3, sc, dom, f_) in enumerate(ranked, 1):
        top.append([P(str(i), 'td'), P(f"<b>{COUNTRY_PT[a3]}</b>", 'td'), P(f"{sc:.0f}", 'td'),
                    P(FACTOR_NAMES[dom], 'td'), P(why.get(a3, "-"), 'td')])
    story.append(table(top, [18, 70, 36, 120, 260], valign='TOP'))
    story.append(PageBreak())

    # ================= PÁGINA 10: SINAIS, LIMITES, FONTES =================
    story += h1("9. Painel de Sinais de Alerta, Limitações e Fontes")
    story.append(P("<b>Limiares analíticos propostos para acompanhar a migração entre cenários</b> (julgamento do autor; não são regras de mercado):", 'bold'))
    sig = [[P("<b>Sinal</b>", 'th'), P("<b>Atual</b>", 'th'), P("<b>Alerta amarelo</b>", 'th'), P("<b>Alerta vermelho</b>", 'th')],
           [P("Treasury 30Y / 10Y", 'td'), P(f"{f['ust30_auction']}% / {f['ust10']}%", 'td'), P("30Y > 5.9%", 'td'), P("10Y > 6.0% com ações caindo", 'td')],
           [P("Leilões do Tesouro (10Y/30Y)", 'td'), P(f"bid-to-cover {f['btc_30y']}", 'td'), P("< 2.35 ou cauda > 2 pb", 'td'), P("leilão 'falho' (cauda > 5 pb, indiretos < 60%)", 'td')],
           [P("Brent / diesel", 'td'), P(f"> US${f['brent']}", 'td'), P("> US$ 120 sustentado", 'td'), P("> US$ 140 ou escassez física declarada", 'td')],
           [P("CPI EUA (a/a) e Fed", 'td'), P("3.4% (set: 3.6-3.7% esp.)", 'td'), P("> 4% e nova alta", 'td'), P("Alta + payroll negativo (erro de política)", 'td')],
           [P("JGB 10Y / iene", 'td'), P(f"{f['jgb10']:.2f}%", 'td'), P("JGB > 3.5%", 'td'), P("Iene +8% em 2 semanas com queda de ações", 'td')],
           [P("VIX / spread HY", 'td'), P(f"{f['vix']} / (n/d)", 'td'), P("VIX > 25 ou HY +150 pb", 'td'), P("VIX > 35 ou HY > 700 pb", 'td')],
           [P("Crédito privado / CRE", 'td'), P("CMBS escritórios 12-13%", 'td'), P("Gates de resgate em 2+ grandes fundos", 'td'), P("Falência de banco regional ou fundo semilíquido relevante", 'td')],
           [P("Soberanos europeus", 'td'), P(f"OAT-Bund ~{f['fr_bund_bp']} pb; gilt 30Y {f['gilt30']}%", 'td'), P("OAT-Bund > 175 pb; gilt > 6.5%", 'td'), P("Uso de TPI/BoE intervém no mercado", 'td')],
           [P("Ciclo de IA", 'td'), P("capex em alta", 'td'), P("Hyperscaler corta guidance de capex", 'td'), P("Queda de preço de aluguel de GPU + inadimplência de neoclouds", 'td')]]
    story.append(table(sig, [110, 100, 140, 154], valign='TOP'))
    story.append(Spacer(1, 6))

    story.append(box(
        "<b>LIMITAÇÕES E TRANSPARÊNCIA:</b> (1) Fatos coletados via busca na web em 11/10/2026; itens de confiança <b>alta</b> vêm de fontes oficiais (Treasury, CBO, "
        "Fed); <b>média</b>, de agregadores/imprensa (CAPE, Buffett, juros diários, séries históricas de eleições, relatos de guerra); recomenda-se reconferir antes de "
        "decisões. (2) Fontes divergem sobre o status exato de Hormuz (fechamento versus ataques e interrupção severa). (3) Probabilidades, atribuições por canal, "
        "faixas de ativos e índice por país são <b>julgamentos analíticos</b>, não previsões; mercados já precificam parte dessa informação. (4) Países pequenos "
        "(Singapura, Bahrein, Hong Kong) não aparecem na base cartográfica. (5) Este material é informativo e <b>não constitui recomendação de investimento</b>.",
        '#FEF2F2', '#F87171', 'td'))
    story.append(Spacer(1, 6))
    story.append(P("<b>Fontes consultadas (por domínio, 11/10/2026):</b> fiscaldata.treasury.gov (Debt to the Penny, TIC); cbo.gov (baseline fev/2026); crfb.org e "
                   "americanactionforum.org (déficit FY26); federalreserve.gov (FOMC 15-16/09/2026, calendário); ycharts.com e tradingeconomics.com (juros); imf.org (GFSR out/2026, "
                   "WEO a ser divulgado em 13/10); trepp.com, wolfstreet.com e commercialobserver.com (CMBS/CRE); goldmansachs.com e kitco.com (30Y, ouro); "
                   "brookings.edu (liderança do Fed); counterpointresearch.com (TSMC); un.org/UNCTAD e bancos (BNP Paribas, Schroders, SSGA) para mercados emergentes; "
                   "imprensa financeira para Japão, Reino Unido, França e Brasil.", 'cap'))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório PDF gerado: {output_filename}", flush=True)


# ---------------------------------------------------------
# 6. MAIN
# ---------------------------------------------------------
def main():
    os.chdir(HERE)
    print("=== MÉTRICAS DERIVADAS ===", flush=True)
    d = compute_derived_metrics()
    for k, v in d.items():
        if k != "scen":
            print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}", flush=True)
    for sid, v in d["scen"].items():
        print(sid, {k: round(x, 2) for k, x in v.items()}, flush=True)

    # validações internas
    for sid, shares in ATTRIB.items():
        assert sum(shares) == 100, f"Atribuição {sid} não soma 100"
    assert abs(sum(s[3] for s in SCENARIOS) - 100) < 1e-9
    assert abs(d["overlay_total"] - d["p_ge20"]) < 1e-9, "Probabilidade do cascata != soma dos cenários S2+S3"

    gdf = gpd.read_file(GEOJSON)
    rows = compute_country_scores(gdf)

    print("\n=== GERANDO GRÁFICOS ===", flush=True)
    chart_fiscal_dashboard(d)
    chart_valuation_vs_rates(d)
    chart_timeline()
    chart_probabilities(d)
    chart_composition(d)
    chart_map_severity(rows)
    chart_map_channels(rows)
    ranking = chart_region_ranking(rows)

    print("\n=== TOP 15 PAÍSES POR VULNERABILIDADE ===", flush=True)
    for a3, sc, dom, sub, _ in sorted([r for r in rows if not np.isnan(r[1])], key=lambda r: -r[1])[:15]:
        print(f"{COUNTRY_PT.get(a3, a3):<18}{sc:5.1f}  {FACTOR_NAMES[dom]}", flush=True)
    print("\n=== RANKING REGIONAL ===", flush=True)
    for n, v, c in ranking[::-1]:
        print(f"{n:<34}{v:5.1f}  (n={c})", flush=True)

    print("\n=== COMPILANDO PDF ===", flush=True)
    build_pdf_report(d, rows, ranking, "Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf")
    print("\n=== PROCESSO FINALIZADO ===", flush=True)


if __name__ == "__main__":
    main()
