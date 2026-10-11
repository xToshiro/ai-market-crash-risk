#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_models.py
------------------
Validation suite for the AI Market Crash Risk repository.
Verifies PDF integrity, page counts, documentation parity, and chart assets.
"""

import os
import sys

# UTF-8 stdout encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Try importing pymupdf
try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

# Script is in <ROOT>/.agents/skills/ai-market-risk-updater/scripts/validate_models.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.dirname(SKILL_DIR)
AGENTS_DIR = os.path.dirname(SKILLS_DIR)
ROOT_DIR = os.path.dirname(AGENTS_DIR)

REPORTS = [
    ("Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf", 10),
    ("Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028_EN.pdf", 10),
    ("Relatorio_Mercado_Financeiro_Americano.pdf", 8),
    ("Relatorio_Mercado_Financeiro_Americano_EN.pdf", 8),
    ("Relatorio_Cenarios_Quebra_Mercado_IA_2026_2029.pdf", 5),
    ("Relatorio_Cenarios_Quebra_Mercado_IA_2026_2029_EN.pdf", 5),
    ("Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf", 4),
    ("Relatorio_Data_Center_ABS_Tranches_Oficiais_EN.pdf", 4),
    ("Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf", 4),
    ("Relatorio_Forense_Subprime_IA_Repacotamento_AAA_EN.pdf", 4),
    ("Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf", 4),
    ("Relatorio_Alavancagem_e_Vendor_Financing_IA_EN.pdf", 4),
]

DOSSIERS = [
    "CoreWeave_GPU_Debt_and_Vendor_Financing_Analysis",
    "Data_Center_ABS_Relatorio",
    "Dossie_Alavancagem_Vendor_Financing_IA",
    "Dossie_Cenarios_Quebra_Mercado_Acoes_e_Credito",
    "Dossie_Forense_Subprime_IA_Repacotamento_AAA",
    "Dossie_Macro_Geopolitica_Quebra_Mercado_2026_2028",
    "KBRA_Data_Center_ABS_Rating_Methodology_Dossier",
]

KEY_CHARTS = [
    "chart_crash_composition.png",
    "chart_vendor_financing_loop.png",
    "chart_gpu_depreciation_vs_debt.png",
    "chart_tranche_structure.png",
    "chart_map_vulnerability.png",
    "chart_leverage_pyramid.png",
]

def main():
    print("=" * 70)
    print("  AI MARKET CRASH RISK — MODEL & REPOSITORY VALIDATION SUITE")
    print("=" * 70)
    errors = 0

    # 1. Check PDFs
    print("\n[1/4] Checking Executive PDF Reports...")
    total_pages = 0
    for fname, expected_pages in REPORTS:
        folder = "en" if fname.endswith("_EN.pdf") else "pt"
        path = os.path.join(ROOT_DIR, "reports", folder, fname)
        if not os.path.exists(path):
            print(f"  ❌ MISSING: reports/{folder}/{fname}")
            errors += 1
            continue
        
        size_kb = os.path.getsize(path) / 1024
        if fitz:
            doc = fitz.open(path)
            actual_pages = len(doc)
            doc.close()
            total_pages += actual_pages
            if actual_pages == expected_pages:
                print(f"  ✅ OK: reports/{folder}/{fname:<50} ({actual_pages} pages, {size_kb:.0f} KB)")
            else:
                print(f"  ⚠️ PAGE MISMATCH: reports/{folder}/{fname} (Expected: {expected_pages}, Found: {actual_pages})")
                errors += 1
        else:
            print(f"  ✅ FOUND: reports/{folder}/{fname} ({size_kb:.0f} KB)")

    print(f"  -> Total compiled pages verified: {total_pages} / 70 expected")

    # 2. Check Markdown Dossiers
    print("\n[2/4] Checking Analytical Markdown Dossiers...")
    for base in DOSSIERS:
        pt_path = os.path.join(ROOT_DIR, "docs", "pt", f"{base}.md")
        en_path = os.path.join(ROOT_DIR, "docs", "en", f"{base}_EN.md")
        pt_ok = os.path.exists(pt_path)
        en_ok = os.path.exists(en_path)
        if pt_ok and en_ok:
            print(f"  ✅ OK: docs/pt/{base}.md <-> docs/en/{base}_EN.md")
        else:
            if not pt_ok:
                print(f"  ❌ MISSING: docs/pt/{base}.md")
                errors += 1
            if not en_ok:
                print(f"  ❌ MISSING: docs/en/{base}_EN.md")
                errors += 1

    # 3. Check Charts
    print("\n[3/4] Checking Key Visual Assets in assets/charts/...")
    for chart in KEY_CHARTS:
        cpath = os.path.join(ROOT_DIR, "assets", "charts", chart)
        if os.path.exists(cpath):
            print(f"  ✅ OK: assets/charts/{chart}")
        else:
            print(f"  ❌ MISSING: assets/charts/{chart}")
            errors += 1

    # 4. Check GeoJSON
    print("\n[4/4] Checking Geospatial Data...")
    geopath = os.path.join(ROOT_DIR, "assets", "geo", "world_countries_110m.geojson")
    if os.path.exists(geopath):
        print(f"  ✅ OK: assets/geo/world_countries_110m.geojson ({os.path.getsize(geopath)/1024:.0f} KB)")
    else:
        print(f"  ❌ MISSING: assets/geo/world_countries_110m.geojson")
        errors += 1

    print("\n" + "=" * 70)
    if errors == 0:
        print("  🎉 VALIDATION PASSED: All repository assets, PDFs, and docs are intact!")
    else:
        print(f"  ❌ VALIDATION FAILED: {errors} issues detected.")
    print("=" * 70)
    return errors

if __name__ == "__main__":
    sys.exit(main())
