#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_all_reports.py
--------------------
Master build orchestration script for the AI Market Crash Risk project.
1. Generates English visual charts into `assets/charts/en/`.
2. Sequentially executes all 12 executive PDF report generators (PT & EN).
3. Renders high-resolution page previews into `assets/previews/pt/` and `assets/previews/en/`.
4. Runs automated validation suite.
"""

import os
import sys
import subprocess
import time

# UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

REPORT_SCRIPTS = [
    ("generate_macro_geopolitical_crash_report.py", "Macro Geopolítica (PT, 10 Págs)"),
    ("generate_macro_geopolitical_crash_report_en.py", "Macro Geopolitics (EN, 10 Pages)"),
    ("generate_us_market_report.py", "Mercado Americano (PT, 8 Págs)"),
    ("generate_us_market_report_en.py", "US Market (EN, 8 Pages)"),
    ("generate_market_crash_scenarios_report.py", "Cenários de Quebra (PT, 5 Págs)"),
    ("generate_market_crash_scenarios_report_en.py", "Crash Scenarios (EN, 5 Pages)"),
    ("generate_data_center_abs_tranches_report.py", "Data Center ABS (PT, 4 Págs)"),
    ("generate_data_center_abs_tranches_report_en.py", "Data Center ABS (EN, 4 Pages)"),
    ("generate_forensic_ai_subprime_report.py", "Forense Subprime IA (PT, 4 Págs)"),
    ("generate_forensic_ai_subprime_report_en.py", "Forensic AI Subprime (EN, 4 Pages)"),
    ("generate_leverage_multiplier_report.py", "Alavancagem & Vendor Financing (PT, 4 Págs)"),
    ("generate_leverage_multiplier_report_en.py", "Leverage & Vendor Financing (EN, 4 Pages)"),
    ("generate_company_financial_forecast_report.py", "Status Empresas & Previsões (PT, 8 Págs)"),
    ("generate_company_financial_forecast_report_en.py", "Company Status & Forecasts (EN, 8 Pages)"),
    ("generate_recent_market_update_report.py", "Atualização Mercado & Grid (PT, 8 Págs)"),
    ("generate_recent_market_update_report_en.py", "Market Update & Grid (EN, 8 Pages)"),
]

def run_step(cmd, desc):
    print(f"\n>>> {desc}...", flush=True)
    t0 = time.time()
    res = subprocess.run(cmd, cwd=SCRIPT_DIR, capture_output=True, text=True)
    elapsed = time.time() - t0
    if res.returncode == 0:
        print(f"    ✅ SUCCESS ({elapsed:.2f}s)")
        return True
    else:
        print(f"    ❌ FAILED ({elapsed:.2f}s)")
        print("    --- STDERR ---")
        print(res.stderr[:600])
        print("    --------------")
        return False

def main():
    start_total = time.time()
    print("=" * 75)
    print("  AI MARKET CRASH RISK — MASTER REPORT BUILDER & PIPELINE RUNNER")
    print("=" * 75)

    # Step 1: Generate charts
    ok_charts_en = run_step([sys.executable, "generate_charts_en.py"], "Step 1/4: Generating 31 English Charts (assets/charts/en/)")
    ok_charts_co = run_step([sys.executable, "generate_company_charts.py"], "Step 1/4 (cont): Generating Bilingual Company Charts (assets/charts/)")
    ok_charts_up = run_step([sys.executable, "generate_recent_market_update_charts.py"], "Step 1/4 (cont): Generating Recent Market Update Charts (assets/charts/)")

    # Step 2: Build all 16 PDFs
    print("\n>>> Step 2/4: Compiling 16 Institutional PDF Reports (102 Pages)...")
    success_count = 0
    fail_count = 0
    total_reports = len(REPORT_SCRIPTS)
    for idx, (script_name, label) in enumerate(REPORT_SCRIPTS, 1):
        script_path = os.path.join(SCRIPT_DIR, script_name)
        t0 = time.time()
        res = subprocess.run([sys.executable, script_path], cwd=SCRIPT_DIR, capture_output=True, text=True)
        elapsed = time.time() - t0
        if res.returncode == 0:
            print(f"    [{idx:02d}/{total_reports:02d}] ✅ {label:<45} ({elapsed:.2f}s)")
            success_count += 1
        else:
            print(f"    [{idx:02d}/{total_reports:02d}] ❌ {label:<45} ({elapsed:.2f}s)")
            print(res.stderr[:400])
            fail_count += 1

    # Step 3: Render Page Previews
    ok_previews = run_step([sys.executable, "generate_page_previews.py"], "Step 3/4: Rendering 102 Page Previews (assets/previews/)")

    # Step 4: Run Validation Suite
    val_path = os.path.join(ROOT_DIR, ".agents", "skills", "ai-market-risk-updater", "scripts", "validate_models.py")
    if os.path.exists(val_path):
        print("\n>>> Step 4/4: Executing Validation Suite...")
        subprocess.run([sys.executable, val_path], cwd=ROOT_DIR)

    total_time = time.time() - start_total
    print("\n" + "=" * 75)
    print(f"  Master Pipeline Completed in {total_time:.2f}s: {success_count} PDFs succeeded, {fail_count} failed.")
    print("=" * 75)

    return fail_count

if __name__ == "__main__":
    sys.exit(main())
