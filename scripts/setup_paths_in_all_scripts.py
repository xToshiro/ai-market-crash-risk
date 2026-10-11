#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_paths_in_all_scripts.py
-----------------------------
Cleanly updates all 12 PDF generator scripts to load language-specific charts:
- Portuguese scripts -> assets/charts/pt/ and reports/pt/
- English scripts -> assets/charts/en/ and reports/en/
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_CHARTS = [
    "chart_indices.png",
    "chart_yields_debt.png",
    "chart_ai_capex.png",
    "chart_ai_subprime.png",
    "chart_solidity.png",
    "chart_crisis_probs.png",
    "chart_stocks_2y_history.png",
    "chart_financial_metrics_matrix.png",
    "chart_private_valuation_vs_burn.png",
    "chart_crash_scenarios_probabilities.png",
    "chart_tranche_structure.png",
    "chart_deals_comparison.png",
    "chart_spreads_yields.png",
    "chart_issuance_and_health.png",
    "chart_spending_vs_software_revenue.png",
    "chart_repackaging_alchemy.png",
    "chart_crisis_comparison.png",
    "chart_gpu_depreciation_vs_debt.png",
    "chart_stress_loss_simulation.png",
    "chart_subcomponents_decomposition.png",
    "chart_leverage_pyramid.png",
    "chart_vendor_financing_loop.png",
    "chart_debt_snowball_neoclouds.png",
    "chart_us_fiscal_dashboard.png",
    "chart_valuation_vs_rates.png",
    "chart_triggers_timeline.png",
    "chart_probability_buildup.png",
    "chart_crash_composition.png",
    "chart_map_vulnerability.png",
    "chart_map_channels.png",
    "chart_region_ranking.png",
]

def update_macro_scripts():
    # 1. Macro PT
    pt_path = os.path.join(SCRIPT_DIR, "generate_macro_geopolitical_crash_report.py")
    with open(pt_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    code = re.sub(
        r'GEOJSON = os\.path\.join\(HERE, "world_countries_110m\.geojson"\)',
        'from utils_paths import get_geo_path, get_chart_path, get_report_pt_path\nGEOJSON = get_geo_path("world_countries_110m.geojson")',
        code
    )
    code = re.sub(
        r'def _finish\(fig, path, label\):\s+fig\.savefig\(path, dpi=200, bbox_inches=\'tight\', facecolor=\'white\'\)',
        'def _finish(fig, path, label):\n    pt_path = get_chart_path(os.path.basename(path), lang="pt")\n    fig.savefig(pt_path, dpi=200, bbox_inches=\'tight\', facecolor=\'white\')',
        code
    )
    code = re.sub(
        r'def _img\(path, width_in\):\s+p = os\.path\.join\(HERE, path\)',
        'def _img(path, width_in):\n    p = get_chart_path(os.path.basename(path), lang="pt")',
        code
    )
    code = re.sub(
        r'build_pdf_report\(d, rows, ranking, output_filename\):\s+f = FACTS\s+doc = SimpleDocTemplate\(output_filename,',
        'build_pdf_report(d, rows, ranking, output_filename):\n    f = FACTS\n    doc = SimpleDocTemplate(get_report_pt_path(output_filename),',
        code
    )
    with open(pt_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated generate_macro_geopolitical_crash_report.py")

    # 2. Macro EN
    en_path = os.path.join(SCRIPT_DIR, "generate_macro_geopolitical_crash_report_en.py")
    with open(en_path, "r", encoding="utf-8") as f:
        code = f.read()

    code = re.sub(
        r'def _img\(path, width_in\):\s+p = os\.path\.join\(HERE, path\)',
        'from utils_paths import get_chart_path, get_report_en_path\ndef _img(path, width_in):\n    p = get_chart_path(os.path.basename(path), lang="en")',
        code
    )
    code = re.sub(
        r'build_pdf_report_en\(d, rows, ranking, output_filename="Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028_EN\.pdf"\):\s+f = FACTS\s+doc = SimpleDocTemplate\(output_filename,',
        'build_pdf_report_en(d, rows, ranking, output_filename="Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028_EN.pdf"):\n    f = FACTS\n    doc = SimpleDocTemplate(get_report_en_path(output_filename),',
        code
    )
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated generate_macro_geopolitical_crash_report_en.py")


def update_standard_script(script_name, lang="pt"):
    path = os.path.join(SCRIPT_DIR, script_name)
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    import_helper = "get_report_pt_path" if lang == "pt" else "get_report_en_path"
    if "from utils_paths import" not in code:
        code = f"from utils_paths import get_chart_path, {import_helper}\n" + code

    # Replace os.path.exists("chart_foo.png") -> os.path.exists(get_chart_path("chart_foo.png", lang="..."))
    for chart in ALL_CHARTS:
        # replace existence check
        code = code.replace(
            f'os.path.exists("{chart}")',
            f'os.path.exists(get_chart_path("{chart}", lang="{lang}"))'
        )
        # replace Image creation
        code = code.replace(
            f'Image("{chart}",',
            f'Image(get_chart_path("{chart}", lang="{lang}"),'
        )

    # Replace SimpleDocTemplate output path
    code = re.sub(
        r'doc = SimpleDocTemplate\(\s*(output_filename|output_path|pdf_filename),',
        f'doc = SimpleDocTemplate({import_helper}(\\1),',
        code
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Updated {script_name} ({lang.upper()})")


def main():
    update_macro_scripts()

    pt_scripts = [
        "generate_us_market_report.py",
        "generate_market_crash_scenarios_report.py",
        "generate_data_center_abs_tranches_report.py",
        "generate_forensic_ai_subprime_report.py",
        "generate_leverage_multiplier_report.py",
    ]
    en_scripts = [
        "generate_us_market_report_en.py",
        "generate_market_crash_scenarios_report_en.py",
        "generate_data_center_abs_tranches_report_en.py",
        "generate_forensic_ai_subprime_report_en.py",
        "generate_leverage_multiplier_report_en.py",
    ]

    for s in pt_scripts:
        update_standard_script(s, lang="pt")
    for s in en_scripts:
        update_standard_script(s, lang="en")

    print("\nAll 12 generator scripts successfully configured for bilingual charts & report paths!")

if __name__ == "__main__":
    main()
