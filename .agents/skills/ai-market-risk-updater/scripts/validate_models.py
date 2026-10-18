#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_models.py
------------------
Validation suite for the AI Market Crash Risk repository.
Verifies PDF integrity, page counts, documentation parity, bilingual charts, and page previews.
"""

import os
import sys
import glob

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
    # Portuguese reports (reports/pt/)
    ("Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf", 10),
    ("Relatorio_Mercado_Financeiro_Americano.pdf", 8),
    ("Relatorio_Cenarios_Quebra_Mercado_IA_2026_2029.pdf", 5),
    ("Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf", 4),
    ("Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf", 4),
    ("Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf", 4),
    ("Relatorio_Status_Financeiro_Acoes_Previsao_Empresas_IA.pdf", 8),
    ("Relatorio_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid.pdf", 8),

    # English reports (reports/en/)
    ("Report_Macro_Geopolitics_Market_Crash_2026_2028.pdf", 10),
    ("Report_US_Financial_Market_AI_Bubble.pdf", 8),
    ("Report_AI_Market_Crash_Scenarios_2026_2029.pdf", 5),
    ("Report_Data_Center_ABS_Official_Tranches.pdf", 4),
    ("Report_Forensic_AI_Subprime_AAA_Repackaging.pdf", 4),
    ("Report_AI_Leverage_and_Vendor_Financing.pdf", 4),
    ("Report_AI_Leaders_Financial_Status_2027_Forecasts.pdf", 8),
    ("Report_Market_Update_Oct2026_Grid_Anthropic.pdf", 8),
]

DOSSIERS = [
    "CoreWeave_GPU_Debt_and_Vendor_Financing_Analysis",
    "Data_Center_ABS_Relatorio",
    "Dossie_Alavancagem_Vendor_Financing_IA",
    "Dossie_Cenarios_Quebra_Mercado_Acoes_e_Credito",
    "Dossie_Forense_Subprime_IA_Repacotamento_AAA",
    "Dossie_Macro_Geopolitica_Quebra_Mercado_2026_2028",
    "Dossie_Status_Financeiro_Acoes_Previsao_Empresas_IA",
    "Dossie_Atualizacao_Mercado_Outubro_2026_Nscale_Anthropic_Grid",
    "KBRA_Data_Center_ABS_Rating_Methodology_Dossier",
]

def main():
    print("=" * 70)
    print("  AI MARKET CRASH RISK — MODEL & REPOSITORY VALIDATION SUITE")
    print("=" * 70)
    errors = 0

    # 1. Check PDFs
    print("\n[1/6] Checking Executive PDF Reports (reports/pt & reports/en)...")
    total_pages = 0
    for fname, expected_pages in REPORTS:
        folder = "en" if fname.startswith("Report_") or fname.endswith("_EN.pdf") else "pt"
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

    print(f"  -> Total compiled pages verified: {total_pages} / 102 expected")

    # 2. Check Markdown Dossiers
    print("\n[2/6] Checking Analytical Markdown Dossiers (docs/pt & docs/en)...")
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

    # 3. Check Bilingual Charts
    print("\n[3/6] Checking Bilingual Visual Charts (assets/charts/pt & assets/charts/en)...")
    pt_charts = glob.glob(os.path.join(ROOT_DIR, "assets", "charts", "pt", "*.png"))
    en_charts = glob.glob(os.path.join(ROOT_DIR, "assets", "charts", "en", "*.png"))
    print(f"  ✅ Portuguese Charts: {len(pt_charts)} found in assets/charts/pt/")
    print(f"  ✅ English Charts:    {len(en_charts)} found in assets/charts/en/")
    if len(pt_charts) < 41 or len(en_charts) < 41:
        errors += 1

    # 4. Check Page Previews
    print("\n[4/6] Checking Page Previews (assets/previews/pt & assets/previews/en)...")
    pt_prevs = glob.glob(os.path.join(ROOT_DIR, "assets", "previews", "pt", "*.png"))
    en_prevs = glob.glob(os.path.join(ROOT_DIR, "assets", "previews", "en", "*.png"))
    print(f"  ✅ Portuguese Page Previews: {len(pt_prevs)} / 51 found in assets/previews/pt/")
    print(f"  ✅ English Page Previews:    {len(en_prevs)} / 51 found in assets/previews/en/")
    if len(pt_prevs) < 51 or len(en_prevs) < 51:
        print("  ⚠️ Page previews count is lower than expected. Run scripts/generate_page_previews.py")
        errors += 1

    # 5. Check GeoJSON
    print("\n[5/6] Checking Geospatial Data...")
    geopath = os.path.join(ROOT_DIR, "assets", "geo", "world_countries_110m.geojson")
    if os.path.exists(geopath):
        print(f"  ✅ OK: assets/geo/world_countries_110m.geojson ({os.path.getsize(geopath)/1024:.0f} KB)")
    else:
        print(f"  ❌ MISSING: assets/geo/world_countries_110m.geojson")
        errors += 1

    # 6. Check References Suite
    print("\n[6/6] Checking Institutional References Suite (references/)...")
    REFERENCE_FILES = [
        "README.md",
        "master_sources_catalog.md",
        "url_connectivity_report.md",
        "data_feeds_and_apis.md",
        "institutional_news_and_dossiers.md",
        "methodologies_and_rating_frameworks.md",
        "verify_all_links.py",
    ]
    for rfile in REFERENCE_FILES:
        ref_path = os.path.join(ROOT_DIR, "references", rfile)
        if os.path.exists(ref_path) and os.path.getsize(ref_path) > 0:
            print(f"  ✅ OK: references/{rfile:<40} ({os.path.getsize(ref_path)/1024:.1f} KB)")
        else:
            print(f"  ❌ MISSING OR EMPTY: references/{rfile}")
            errors += 1

    print("\n" + "=" * 70)
    if errors == 0:
        print("  🎉 VALIDATION PASSED: All repository assets, bilingual charts, PDFs, previews, and references are intact!")
    else:
        print(f"  ❌ VALIDATION FAILED: {errors} issues detected.")
    print("=" * 70)
    return errors

if __name__ == "__main__":
    sys.exit(main())
