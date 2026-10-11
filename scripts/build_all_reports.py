#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_all_reports.py
--------------------
Master build orchestration script for the AI Market Crash Risk project.
Sequentially executes all 12 executive PDF report generators (PT & EN)
and validates output page counts and asset integrity.
"""

import os
import sys
import subprocess
import time

# UTF-8 encoding for console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

SCRIPTS = [
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
]

def main():
    start_total = time.time()
    print("=" * 75)
    print("  AI MARKET CRASH RISK — MASTER REPORT BUILDER & PIPELINE RUNNER")
    print("=" * 75)

    success_count = 0
    fail_count = 0

    for idx, (script_name, label) in enumerate(SCRIPTS, 1):
        script_path = os.path.join(SCRIPT_DIR, script_name)
        print(f"\n[{idx:02d}/12] Compiling: {label}...")
        t0 = time.time()
        res = subprocess.run([sys.executable, script_path], cwd=SCRIPT_DIR, capture_output=True, text=True)
        elapsed = time.time() - t0

        if res.returncode == 0:
            print(f"  -> SUCCESS ({elapsed:.2f}s)")
            success_count += 1
        else:
            print(f"  -> FAILED ({elapsed:.2f}s)")
            print("  --- ERROR STDERR ---")
            print(res.stderr[:500])
            print("  --------------------")
            fail_count += 1

    total_time = time.time() - start_total
    print("\n" + "=" * 75)
    print(f"  Build Completed in {total_time:.2f}s: {success_count} succeeded, {fail_count} failed.")
    print("=" * 75)

    # Run validator
    validator_path = os.path.join(ROOT_DIR, ".agents", "skills", "ai-market-risk-updater", "scripts", "validate_models.py")
    if os.path.exists(validator_path):
        print("\nExecuting validation suite...")
        subprocess.run([sys.executable, validator_path], cwd=ROOT_DIR)

    return fail_count

if __name__ == "__main__":
    sys.exit(main())
