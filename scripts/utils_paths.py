#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils_paths.py
--------------
Centralized path resolution utility for the AI Market Crash Risk project.
Ensures seamless asset loading (charts, GeoJSON) and report saving (reports/pt, reports/en)
regardless of the current working directory.
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CHARTS_DIR = os.path.join(ROOT_DIR, "assets", "charts")
GEO_DIR = os.path.join(ROOT_DIR, "assets", "geo")
REPORTS_PT_DIR = os.path.join(ROOT_DIR, "reports", "pt")
REPORTS_EN_DIR = os.path.join(ROOT_DIR, "reports", "en")
DOCS_PT_DIR = os.path.join(ROOT_DIR, "docs", "pt")
DOCS_EN_DIR = os.path.join(ROOT_DIR, "docs", "en")

def get_chart_path(filename):
    """Returns absolute path to a chart image, searching in assets/charts first."""
    p = os.path.join(CHARTS_DIR, filename)
    if os.path.exists(p):
        return p
    p_here = os.path.join(SCRIPT_DIR, filename)
    if os.path.exists(p_here):
        return p_here
    p_root = os.path.join(ROOT_DIR, filename)
    if os.path.exists(p_root):
        return p_root
    return p  # return intended path for creation

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
