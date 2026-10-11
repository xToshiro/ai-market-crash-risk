#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_page_previews.py
-------------------------
Renders high-resolution image previews (PNG) of all pages from the 12 executive PDF reports.
Stores Portuguese report page previews in `assets/previews/pt/` and English previews in `assets/previews/en/`.
"""

import os
import sys
import glob

# UTF-8 stdout encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        print("Error: PyMuPDF is required to render page previews. Run: pip install pymupdf")
        sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
PREVIEWS_PT_DIR = os.path.join(ROOT_DIR, "assets", "previews", "pt")
PREVIEWS_EN_DIR = os.path.join(ROOT_DIR, "assets", "previews", "en")
REPORTS_PT_DIR = os.path.join(ROOT_DIR, "reports", "pt")
REPORTS_EN_DIR = os.path.join(ROOT_DIR, "reports", "en")

os.makedirs(PREVIEWS_PT_DIR, exist_ok=True)
os.makedirs(PREVIEWS_EN_DIR, exist_ok=True)

REPORT_SLUGS = {
    "Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028.pdf": "macro_geopolitics",
    "Relatorio_Macro_Geopolitica_Quebra_Mercado_2026_2028_EN.pdf": "macro_geopolitics",
    "Relatorio_Mercado_Financeiro_Americano.pdf": "us_market",
    "Relatorio_Mercado_Financeiro_Americano_EN.pdf": "us_market",
    "Relatorio_Cenarios_Quebra_Mercado_IA_2026_2029.pdf": "crash_scenarios",
    "Relatorio_Cenarios_Quebra_Mercado_IA_2026_2029_EN.pdf": "crash_scenarios",
    "Relatorio_Data_Center_ABS_Tranches_Oficiais.pdf": "data_center_abs",
    "Relatorio_Data_Center_ABS_Tranches_Oficiais_EN.pdf": "data_center_abs",
    "Relatorio_Forense_Subprime_IA_Repacotamento_AAA.pdf": "forensic_subprime",
    "Relatorio_Forense_Subprime_IA_Repacotamento_AAA_EN.pdf": "forensic_subprime",
    "Relatorio_Alavancagem_e_Vendor_Financing_IA.pdf": "leverage_multiplier",
    "Relatorio_Alavancagem_e_Vendor_Financing_IA_EN.pdf": "leverage_multiplier",
}

def render_pdf_pages(pdf_path, output_dir, slug, lang_code, dpi=130):
    if not os.path.exists(pdf_path):
        print(f"  ❌ PDF not found: {pdf_path}")
        return 0
    
    doc = fitz.open(pdf_path)
    count = len(doc)
    for idx, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=dpi)
        out_name = f"{slug}_{lang_code}_p{idx:02d}.png"
        out_path = os.path.join(output_dir, out_name)
        pix.save(out_path)
    doc.close()
    return count

def main():
    print("=" * 70)
    print("  RENDERING HIGH-RES PAGE PREVIEWS -> assets/previews/pt/ & assets/previews/en/")
    print("=" * 70)

    total_pt = 0
    total_en = 0

    # 1. Portuguese reports
    print("\n[1/2] Rendering Portuguese Report Pages (assets/previews/pt/)...")
    for pdf_name in sorted(os.listdir(REPORTS_PT_DIR)):
        if pdf_name.endswith(".pdf"):
            pdf_path = os.path.join(REPORTS_PT_DIR, pdf_name)
            slug = REPORT_SLUGS.get(pdf_name, os.path.splitext(pdf_name)[0].lower())
            p_count = render_pdf_pages(pdf_path, PREVIEWS_PT_DIR, slug, "pt")
            print(f"  ✅ {pdf_name:<50} -> {p_count} pages rendered")
            total_pt += p_count

    # 2. English reports
    print("\n[2/2] Rendering English Report Pages (assets/previews/en/)...")
    for pdf_name in sorted(os.listdir(REPORTS_EN_DIR)):
        if pdf_name.endswith(".pdf"):
            pdf_path = os.path.join(REPORTS_EN_DIR, pdf_name)
            slug = REPORT_SLUGS.get(pdf_name, os.path.splitext(pdf_name)[0].lower())
            p_count = render_pdf_pages(pdf_path, PREVIEWS_EN_DIR, slug, "en")
            print(f"  ✅ {pdf_name:<50} -> {p_count} pages rendered")
            total_en += p_count

    print("\n" + "=" * 70)
    print(f"  PREVIEWS GENERATED: {total_pt} pages (PT) + {total_en} pages (EN) = {total_pt + total_en} preview images!")
    print("=" * 70)

if __name__ == "__main__":
    main()
