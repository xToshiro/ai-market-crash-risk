#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils_paths.py
--------------
Centralized path resolution utility for the AI Market Crash Risk project.
Ensures seamless asset loading (charts, GeoJSON, page previews) and report saving (reports/pt, reports/en)
regardless of the current working directory.
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CHARTS_PT_DIR = os.path.join(ROOT_DIR, "assets", "charts", "pt")
CHARTS_EN_DIR = os.path.join(ROOT_DIR, "assets", "charts", "en")
PREVIEWS_PT_DIR = os.path.join(ROOT_DIR, "assets", "previews", "pt")
PREVIEWS_EN_DIR = os.path.join(ROOT_DIR, "assets", "previews", "en")
GEO_DIR = os.path.join(ROOT_DIR, "assets", "geo")
REPORTS_PT_DIR = os.path.join(ROOT_DIR, "reports", "pt")
REPORTS_EN_DIR = os.path.join(ROOT_DIR, "reports", "en")
DOCS_PT_DIR = os.path.join(ROOT_DIR, "docs", "pt")
DOCS_EN_DIR = os.path.join(ROOT_DIR, "docs", "en")

def get_chart_path(filename, lang="pt"):
    """Returns absolute path to a chart image in assets/charts/pt/ or assets/charts/en/."""
    target_dir = CHARTS_EN_DIR if lang.lower() == "en" else CHARTS_PT_DIR
    p = os.path.join(target_dir, filename)
    if os.path.exists(p):
        return p
    # Fallback checks
    p_fallback = os.path.join(ROOT_DIR, "assets", "charts", filename)
    if os.path.exists(p_fallback):
        return p_fallback
    p_here = os.path.join(SCRIPT_DIR, filename)
    if os.path.exists(p_here):
        return p_here
    return p

def get_preview_path(filename, lang="pt"):
    """Returns absolute path for report page preview in assets/previews/pt/ or assets/previews/en/."""
    target_dir = PREVIEWS_EN_DIR if lang.lower() == "en" else PREVIEWS_PT_DIR
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, filename)

def get_geo_path(filename="world_countries_110m.geojson"):
    """Returns absolute path to GeoJSON spatial dataset."""
    p = os.path.join(GEO_DIR, filename)
    if os.path.exists(p):
        return p
    p_root = os.path.join(ROOT_DIR, filename)
    if os.path.exists(p_root):
        return p_root
    return p

def get_report_pt_path(filename):
    """Returns absolute path for Portuguese PDF report in reports/pt/."""
    os.makedirs(REPORTS_PT_DIR, exist_ok=True)
    return os.path.join(REPORTS_PT_DIR, filename)

def get_report_en_path(filename):
    """Returns absolute path for English PDF report in reports/en/."""
    os.makedirs(REPORTS_EN_DIR, exist_ok=True)
    return os.path.join(REPORTS_EN_DIR, filename)
