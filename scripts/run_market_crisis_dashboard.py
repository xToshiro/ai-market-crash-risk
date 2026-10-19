#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_market_crisis_dashboard.py
-------------------------------
Institutional Real-Time Market Crisis & AI Bubble Watchdog Dashboard (Unified V3).

Major Features:
1. Unified Panoramic Layout: All critical metrics, scenarios, company stocks,
   charts, and SQLite database stats visible on a single unified cockpit screen.
2. 100% Real-Time Data from Public APIs:
   - Yahoo Finance v8 API: Tech stocks, VIX, SKEW, VVIX, USD/JPY, US 10Y Yield, HYG, LQD, Utilities.
   - US Treasury Fiscal Data API: Official Total Public Debt to the Penny.
3. Real 5-Day Historical Data Pre-Loaded:
   - Charts are immediately populated with real multi-day historical lines on startup.
   - Dynamic real-time ticks appended every 20s and persisted into SQLite.
4. Embedded Local SQLite Database (`data/crisis_dashboard.db`):
   - Persistent tick history, scenario history, company snapshots, and alert events.
5. Mathematical Approximation of the 3 Crash Scenarios:
   - Scenario 1 (Orderly Deceleration & Multiple Compression): Base ~42%
   - Scenario 2 (Credit Dislocation & Grid Bottleneck): Base ~40%
   - Scenario 3 (Systemic Global Multi-Contagion): Base ~18%
   - Soft Landing: Base ~52% (Overall Stress: ~48%)
6. AI & Power Grid Company Stock Radar (10 Key Entities):
   - Silicon (NVDA, TSM, AVGO), Hyperscalers (MSFT, GOOGL, AMZN, META, ORCL), Grid Bottleneck (CEG, VST).
7. Crisis Sirens: Web Audio API pulsing tone in browser + Windows hardware sound fallback.
8. Conflict-Free Port Detection (Auto-detects open port from 5050 to 5070).
"""

import os
import sys
import json
import time
import math
import sqlite3
import socket
import socketserver
import urllib.request
import urllib.error
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Windows stdout encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "crisis_dashboard.db")
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_PORT = 5050
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# -------------------------------------------------------------
# TRACKED ASSETS & COMPANIES ACROSS TRANSMISSION PILLARS
# -------------------------------------------------------------
TRACKED_ENTITIES = {
    # 1. Volatility & Tail Risk
    "^VIX": {"name": "CBOE VIX Spot", "category": "volatility", "group": "index", "desc": "30-Day S&P 500 Implied Volatility"},
    "^VVIX": {"name": "CBOE VVIX", "category": "volatility", "group": "index", "desc": "Volatility of VIX (Hedging Velocity)"},
    "^SKEW": {"name": "CBOE SKEW Index", "category": "volatility", "group": "index", "desc": "Out-of-the-money Put Skew (Black Swan Risk)"},
    "^TNX": {"name": "US 10-Year Treasury Yield", "category": "macro_rate", "group": "index", "desc": "Benchmark Sovereign Hurdle Rate (%)"},
    
    # 2. Currency & Carry Trade Anchor
    "USDJPY=X": {"name": "USD/JPY Spot", "category": "fx", "group": "index", "desc": "Japanese Yen Carry Trade Liquidity Conduit"},
    
    # 3. Credit Risk & ABS Spread Proxy
    "HYG": {"name": "iShares High Yield Corporate", "category": "credit", "group": "index", "desc": "Sub-investment Grade Corporate Debt"},
    "LQD": {"name": "iShares Investment Grade Corporate", "category": "credit", "group": "index", "desc": "Senior Corporate Credit Barometer"},

    # 4. AI Hardware & Silicon Anchors
    "NVDA": {"name": "NVIDIA Corporation", "category": "silicon", "group": "stock", "desc": "AI Hardware Monopoly, 75% Gross Margin, Fabless Multiple"},
    "TSM": {"name": "Taiwan Semiconductor (TSMC)", "category": "silicon", "group": "stock", "desc": "CoWoS Packaging Monopoly, Taiwan Geopolitical Chokepoint"},
    "AVGO": {"name": "Broadcom Inc.", "category": "silicon", "group": "stock", "desc": "AI Networking Switches & Custom ASICs"},

    # 5. Hyperscalers & Cloud CapEx Giants
    "MSFT": {"name": "Microsoft Corporation", "category": "hyperscaler", "group": "stock", "desc": "Azure AI CapEx, Nscale Essex Contract Counterpart"},
    "GOOGL": {"name": "Alphabet Inc.", "category": "hyperscaler", "group": "stock", "desc": "Custom TPU Silicon, $88B Net Cash Cushion"},
    "AMZN": {"name": "Amazon.com, Inc.", "category": "hyperscaler", "group": "stock", "desc": "AWS Cloud Run-rate, Talen Nuclear PPA, Anthropic Investor"},
    "META": {"name": "Meta Platforms, Inc.", "category": "hyperscaler", "group": "stock", "desc": "Llama Open-Weight Compute Infrastructure"},
    "ORCL": {"name": "Oracle Corporation", "category": "hyperscaler", "group": "stock", "desc": "OCI Data Center Buildout, High Debt-to-Equity Leverage"},

    # 6. Electrical Grid & Energy Bottlenecks
    "CEG": {"name": "Constellation Energy", "category": "energy", "group": "stock", "desc": "Nuclear PPA Operator, Three Mile Island Restart Partner"},
    "VST": {"name": "Vistra Corp", "category": "energy", "group": "stock", "desc": "PJM & ERCOT Merchant Power Producer, Capacity Auction Surge"},

    # 7. Sector Benchmarks
    "SMH": {"name": "VanEck Semiconductor ETF", "category": "benchmark", "group": "etf", "desc": "Global Chip Industry Aggregate"},
    "^GSPC": {"name": "S&P 500 Benchmark", "category": "benchmark", "group": "etf", "desc": "Broad US Equity Multiple Benchmark"},
    "^IXIC": {"name": "Nasdaq Composite", "category": "benchmark", "group": "etf", "desc": "Technology Valuation Benchmark"},
}

# -------------------------------------------------------------
# LOCAL SQLITE DATABASE ARCHITECTURE
# -------------------------------------------------------------
class LocalDatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS market_ticks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    price REAL NOT NULL,
                    prev_close REAL,
                    change_pct REAL,
                    velocity_1h REAL,
                    high_52w REAL,
                    low_52w REAL
                )
            """)
            c.execute("CREATE INDEX IF NOT EXISTS idx_ticks_ticker_time ON market_ticks(ticker, timestamp)")

            c.execute("""
                CREATE TABLE IF NOT EXISTS scenario_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    stress_overall REAL NOT NULL,
                    p_scenario_1 REAL NOT NULL,
                    p_scenario_2 REAL NOT NULL,
                    p_scenario_3 REAL NOT NULL,
                    p_soft_landing REAL NOT NULL,
                    vix REAL,
                    usdjpy REAL,
                    hyg_lqd REAL,
                    tnx_yield REAL,
                    notes TEXT
                )
            """)
            c.execute("CREATE INDEX IF NOT EXISTS idx_scenario_time ON scenario_history(timestamp)")

            c.execute("""
                CREATE TABLE IF NOT EXISTS company_snapshots (
                    ticker TEXT PRIMARY KEY,
                    updated_at TEXT NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    change_pct REAL NOT NULL,
                    high_52w REAL,
                    low_52w REAL,
                    range_pct REAL,
                    status_flag TEXT
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS alert_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    trigger_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            conn.commit()

    def record_tick(self, ticker, price, prev_close, change_pct, velocity_1h, high_52w=None, low_52w=None):
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO market_ticks (timestamp, ticker, price, prev_close, change_pct, velocity_1h, high_52w, low_52w)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (now_iso, ticker, price, prev_close, change_pct, velocity_1h, high_52w, low_52w))
            conn.commit()

    def record_scenario_probabilities(self, stress, s1, s2, s3, soft_landing, vix, usdjpy, hyg_lqd, tnx, notes=""):
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO scenario_history (timestamp, stress_overall, p_scenario_1, p_scenario_2, p_scenario_3, p_soft_landing, vix, usdjpy, hyg_lqd, tnx_yield, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (now_iso, stress, s1, s2, s3, soft_landing, vix, usdjpy, hyg_lqd, tnx, notes))
            conn.commit()

    def update_company_snapshot(self, ticker, name, category, price, change_pct, high_52w, low_52w, status_flag="NORMAL"):
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        range_pct = 50.0
        if high_52w and low_52w and high_52w > low_52w:
            range_pct = max(0.0, min(100.0, ((price - low_52w) / (high_52w - low_52w)) * 100.0))
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO company_snapshots (ticker, updated_at, name, category, price, change_pct, high_52w, low_52w, range_pct, status_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticker) DO UPDATE SET
                    updated_at=excluded.updated_at,
                    price=excluded.price,
                    change_pct=excluded.change_pct,
                    high_52w=excluded.high_52w,
                    low_52w=excluded.low_52w,
                    range_pct=excluded.range_pct,
                    status_flag=excluded.status_flag
            """, (ticker, now_iso, name, category, price, change_pct, high_52w, low_52w, round(range_pct, 1), status_flag))
            conn.commit()

    def record_alert_event(self, severity, trigger_id, title, description):
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO alert_events (timestamp, severity, trigger_id, title, description)
                VALUES (?, ?, ?, ?, ?)
            """, (now_iso, severity, trigger_id, title, description))
            conn.commit()

    def get_stats(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            ticks_count = c.execute("SELECT COUNT(*) FROM market_ticks").fetchone()[0]
            scenario_count = c.execute("SELECT COUNT(*) FROM scenario_history").fetchone()[0]
            alerts_count = c.execute("SELECT COUNT(*) FROM alert_events").fetchone()[0]
            db_size_kb = (os.path.getsize(self.db_path) / 1024) if os.path.exists(self.db_path) else 0.0
            return {
                "ticks_count": ticks_count,
                "scenario_count": scenario_count,
                "alerts_count": alerts_count,
                "db_size_kb": round(db_size_kb, 1),
                "db_path": self.db_path
            }

DB = LocalDatabaseManager()

# -------------------------------------------------------------
# GLOBAL DASHBOARD STATE CONTAINER
# -------------------------------------------------------------
class ComprehensiveDashboardState:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_updated = None
        self.poll_count = 0
        self.poll_interval = 20  # seconds
        self.active_port = DEFAULT_PORT

        # US Sovereign Debt from Treasury API
        self.us_debt_trillion = 40.388
        self.us_debt_date = "2026-10-15"

        # Baseline Live Quotes
        self.metrics = {
            "^VIX": {"price": 18.58, "prev": 18.41, "change_pct": 0.92, "velocity_1h": 0.0, "high_52w": 65.73, "low_52w": 11.52},
            "^VVIX": {"price": 105.93, "prev": 105.93, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 180.0, "low_52w": 85.0},
            "^SKEW": {"price": 168.59, "prev": 168.59, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 172.5, "low_52w": 135.0},
            "^TNX": {"price": 5.144, "prev": 5.144, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 5.35, "low_52w": 3.80},
            "USDJPY=X": {"price": 158.45, "prev": 158.47, "change_pct": -0.01, "velocity_1h": 0.0, "high_52w": 161.95, "low_52w": 139.58},
            "HYG": {"price": 76.89, "prev": 76.88, "change_pct": 0.01, "velocity_1h": 0.0, "high_52w": 80.20, "low_52w": 74.50},
            "LQD": {"price": 102.89, "prev": 102.83, "change_pct": 0.06, "velocity_1h": 0.0, "high_52w": 112.50, "low_52w": 98.80},
            "NVDA": {"price": 217.22, "prev": 217.22, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 235.0, "low_52w": 110.0},
            "TSM": {"price": 420.54, "prev": 420.54, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 435.0, "low_52w": 185.0},
            "AVGO": {"price": 334.62, "prev": 334.62, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 355.0, "low_52w": 160.0},
            "MSFT": {"price": 512.40, "prev": 512.40, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 530.0, "low_52w": 395.0},
            "GOOGL": {"price": 196.80, "prev": 196.80, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 205.0, "low_52w": 140.0},
            "AMZN": {"price": 218.60, "prev": 218.60, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 230.0, "low_52w": 165.0},
            "META": {"price": 685.20, "prev": 685.20, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 710.0, "low_52w": 450.0},
            "ORCL": {"price": 184.50, "prev": 184.50, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 198.0, "low_52w": 115.0},
            "CEG": {"price": 262.74, "prev": 262.74, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 290.0, "low_52w": 130.0},
            "VST": {"price": 149.17, "prev": 149.17, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 165.0, "low_52w": 55.0},
            "SMH": {"price": 548.99, "prev": 548.99, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 570.0, "low_52w": 280.0},
            "^GSPC": {"price": 7697.60, "prev": 7697.60, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 7800.0, "low_52w": 5400.0},
            "^IXIC": {"price": 26444.65, "prev": 26444.65, "change_pct": 0.0, "velocity_1h": 0.0, "high_52w": 27100.0, "low_52w": 17000.0},
        }

        # Derived Ratios
        self.ratios = {
            "hyg_lqd_ratio": 0.7473,
            "vix_vvix_ratio": 0.1754,
            "ten_year_yield": 5.144,
            "usdjpy_rate": 158.45,
        }

        # Mathematical Scenarios
        self.scenarios = {
            "overall_stress": 48.0,
            "soft_landing": 52.0,
            "scenario_1": 42.0,
            "scenario_2": 40.0,
            "scenario_3": 18.0,
            "attributions": {
                "s1_drivers": "Yield de 10A a 5,14% comprimindo modelos DCF e múltiplos P/L de IA.",
                "s2_drivers": "Gargalo físico de rede (PJM/Essex) e razão HYG/LQD em 0,7473.",
                "s3_drivers": "USD/JPY a 158,45; carry trade estável acima da banda crítica de 150."
            }
        }

        # Company Radar Snapshots
        self.company_radar = []

        # Real 5-Day Historical Time Series for Charts
        self.chart_series = {
            "vix": [],
            "usdjpy": [],
            "hyg_lqd": [],
            "tnx": []
        }

        # Real-Time Event Audit Log
        self.event_log = [
            {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "msg": "Dashboard V3 Unificada inicializada. Feeds de dados ao vivo e séries históricas ativas."}
        ]

        self.active_triggers = []
        self.simulated_alert = False

    def add_event(self, level, msg):
        now_str = datetime.now().strftime("%H:%M:%S")
        self.event_log.insert(0, {"time": now_str, "level": level, "msg": msg})
        if len(self.event_log) > 120:
            self.event_log.pop()
        if level in ("WARNING", "CRITICAL"):
            DB.record_alert_event(level, "MARKET_EVENT", f"Evento [{level}]", msg)

STATE = ComprehensiveDashboardState()

# -------------------------------------------------------------
# REAL HISTORICAL TIME-SERIES PRELOADER
# -------------------------------------------------------------
def fetch_historical_series(ticker, range_str="5d", interval="1h"):
    """Fetches real historical timestamp + close prices from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&range={range_str}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            res = data.get("chart", {}).get("result", [])[0]
            timestamps = res.get("timestamp", [])
            closes = res.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            points = []
            for t, c in zip(timestamps, closes):
                if c is not None:
                    time_label = datetime.fromtimestamp(t).strftime("%d/%m %H:%M")
                    points.append({"time": time_label, "val": round(c, 3)})
            return points
    except Exception:
        return []

def preload_all_chart_series():
    """Preloads 5-day real historical data for all 4 dashboard charts."""
    print("  [*] Pré-carregando séries históricas de 5 dias das APIs públicas...")
    
    # 1. VIX
    vix_points = fetch_historical_series("^VIX")
    if vix_points:
        with STATE.lock:
            STATE.chart_series["vix"] = vix_points[-45:]
            
    # 2. USD/JPY
    yen_points = fetch_historical_series("USDJPY=X")
    if yen_points:
        with STATE.lock:
            STATE.chart_series["usdjpy"] = yen_points[-45:]

    # 3. 10Y Yield
    tnx_points = fetch_historical_series("^TNX")
    if tnx_points:
        with STATE.lock:
            STATE.chart_series["tnx"] = tnx_points[-45:]

    # 4. HYG/LQD Credit Spread Ratio
    hyg_p = fetch_historical_series("HYG")
    lqd_p = fetch_historical_series("LQD")
    if hyg_p and lqd_p:
        lqd_dict = {p["time"]: p["val"] for p in lqd_p}
        ratio_points = []
        for p in hyg_p:
            t = p["time"]
            if t in lqd_dict and lqd_dict[t] > 0:
                ratio_points.append({"time": t, "val": round(p["val"] / lqd_dict[t], 4)})
        if ratio_points:
            with STATE.lock:
                STATE.chart_series["hyg_lqd"] = ratio_points[-45:]

    print(f"  [+] Séries carregadas: VIX ({len(STATE.chart_series['vix'])}), USD/JPY ({len(STATE.chart_series['usdjpy'])}), TNX ({len(STATE.chart_series['tnx'])}), Crédito ({len(STATE.chart_series['hyg_lqd'])}).")

# -------------------------------------------------------------
# REAL-TIME DATA FETCHING ROUTINES (PUBLIC APIS)
# -------------------------------------------------------------
def fetch_ticker_data(ticker):
    """Fetches real-time price, previous close, and 52-week range from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result = data.get("chart", {}).get("result", [])
            if not result:
                return None
            meta = result[0].get("meta", {})
            price = meta.get("regularMarketPrice")
            prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            
            high_52w = meta.get("fiftyTwoWeekHigh")
            low_52w = meta.get("fiftyTwoWeekLow")
            
            if not high_52w or not low_52w:
                quotes = result[0].get("indicators", {}).get("quote", [{}])[0]
                highs = [h for h in quotes.get("high", []) if h is not None]
                lows = [l for l in quotes.get("low", []) if l is not None]
                high_52w = max(highs) if highs else (price * 1.15 if price else 0)
                low_52w = min(lows) if lows else (price * 0.75 if price else 0)
            
            change_pct = ((price - prev) / prev * 100.0) if (price and prev and prev > 0) else 0.0

            return {
                "price": round(price, 3) if price else 0.0,
                "prev": round(prev, 3) if prev else 0.0,
                "change_pct": round(change_pct, 2),
                "high_52w": round(high_52w, 2) if high_52w else 0.0,
                "low_52w": round(low_52w, 2) if low_52w else 0.0,
            }
    except Exception:
        return None

def fetch_us_debt():
    """Fetches official total public debt from US Treasury Fiscal Data API."""
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&page[size]=1"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            row = data.get("data", [])[0]
            amt = float(row.get("tot_pub_debt_out_amt", 0)) / 1e12
            rec_date = row.get("record_date", "")
            return round(amt, 3), rec_date
    except Exception:
        return None, None

# -------------------------------------------------------------
# MATHEMATICAL APPROXIMATION ENGINE (3 SCENARIOS + OVERALL GAUGE)
# -------------------------------------------------------------
def compute_mathematical_scenarios():
    """Computes dynamic mathematical probabilities for the 3 crash scenarios."""
    with STATE.lock:
        vix = STATE.metrics.get("^VIX", {}).get("price", 18.58)
        usdjpy = STATE.metrics.get("USDJPY=X", {}).get("price", 158.45)
        hyg = STATE.metrics.get("HYG", {}).get("price", 76.89)
        lqd = STATE.metrics.get("LQD", {}).get("price", 102.89)
        tnx = STATE.metrics.get("^TNX", {}).get("price", 5.144)
        skew = STATE.metrics.get("^SKEW", {}).get("price", 168.59)
        vvix = STATE.metrics.get("^VVIX", {}).get("price", 105.93)
        nasdaq_chg = STATE.metrics.get("^IXIC", {}).get("change_pct", 0.0)

        # Derived Ratios
        hyg_lqd = (hyg / lqd) if lqd > 0 else 0.7473
        STATE.ratios["hyg_lqd_ratio"] = round(hyg_lqd, 4)
        STATE.ratios["ten_year_yield"] = round(tnx, 3)
        STATE.ratios["usdjpy_rate"] = round(usdjpy, 2)
        STATE.ratios["vix_vvix_ratio"] = round((vix / vvix) if vvix > 0 else 0.1754, 4)

        # Scenario 1 (Multiples Compression & Yield)
        delta_s1_yield = 14.0 * (tnx - 5.0)
        delta_s1_vix = 0.4 * (vix - 18.0)
        delta_s1_nasdaq = -0.6 * nasdaq_chg
        p_s1 = max(18.0, min(68.0, 42.0 + delta_s1_yield + delta_s1_vix + delta_s1_nasdaq))

        # Scenario 2 (Credit & Grid Shock)
        delta_s2_credit = 240.0 * (0.7480 - hyg_lqd)
        delta_s2_vix = 0.65 * max(0.0, vix - 20.0)
        delta_s2_yield = 7.0 * (tnx - 5.0)
        p_s2 = max(18.0, min(68.0, 40.0 + delta_s2_credit + delta_s2_vix + delta_s2_yield))

        # Scenario 3 (Global Systemic Multi-Contagion)
        delta_s3_yen = 1.3 * max(0.0, 153.0 - usdjpy)
        delta_s3_vix = 0.9 * max(0.0, vix - 24.0)
        delta_s3_skew = 0.12 * max(0.0, skew - 145.0)
        p_s3 = max(8.0, min(50.0, 18.0 + delta_s3_yen + delta_s3_vix + delta_s3_skew))

        # Overall Stress Index
        overall_stress = 48.0 + (0.35 * (p_s1 - 42.0)) + (0.45 * (p_s2 - 40.0)) + (0.50 * (p_s3 - 18.0))
        if STATE.simulated_alert:
            overall_stress = max(overall_stress, 78.5)
            p_s2 = max(p_s2, 62.0)
            p_s3 = max(p_s3, 41.0)

        overall_stress = max(15.0, min(95.0, overall_stress))
        soft_landing = 100.0 - overall_stress

        STATE.scenarios["overall_stress"] = round(overall_stress, 1)
        STATE.scenarios["soft_landing"] = round(soft_landing, 1)
        STATE.scenarios["scenario_1"] = round(p_s1, 1)
        STATE.scenarios["scenario_2"] = round(p_s2, 1)
        STATE.scenarios["scenario_3"] = round(p_s3, 1)

        STATE.scenarios["attributions"] = {
            "s1_drivers": f"Yield 10A a {tnx:.3f}% ({'+' if delta_s1_yield >= 0 else ''}{delta_s1_yield:.1f} pp); Nasdaq momentum {nasdaq_chg:+.2f}%.",
            "s2_drivers": f"Razão HYG/LQD em {hyg_lqd:.4f} ({'+' if delta_s2_credit >= 0 else ''}{delta_s2_credit:.1f} pp); Custo de capital elevado.",
            "s3_drivers": f"USD/JPY em {usdjpy:.2f} (estável); SKEW em {skew:.1f} indicando cautela de cauda."
        }

        # Triggers
        triggers = []
        if STATE.simulated_alert:
            triggers.append({
                "id": "SIMULATED_ALERT",
                "severity": "CRITICAL",
                "title": "🚨 TESTE DE EMERGÊNCIA DISPARADO PELO OPERADOR",
                "description": "Simulação de estresse de cauda ativada para audição da sirene e testes de transmissão."
            })
        if vix >= 32.0:
            triggers.append({
                "id": "VIX_PANIC", "severity": "CRITICAL",
                "title": "VIX EM REGIME DE PÂNICO (> 32.0)",
                "description": f"VIX atingiu {vix:.2f}. Liquidação forçada ampla em fundos sistemáticos."
            })
        elif vix >= 25.0:
            triggers.append({
                "id": "VIX_VOL_TARGETING", "severity": "WARNING",
                "title": "VIX ROMPEU GATILHO DE VOL-TARGETING (> 25.0)",
                "description": f"VIX em {vix:.2f}. Desalavancagem compulsória de CTAs e fundos de paridade de risco."
            })
        if usdjpy <= 145.0:
            triggers.append({
                "id": "YEN_CARRY_COLLAPSE", "severity": "CRITICAL",
                "title": "RUPTURA DO CARRY TRADE DO IENE (USD/JPY <= 145.0)",
                "description": f"USD/JPY caiu para {usdjpy:.2f}. Repatriação forçada de capitais japoneses desencadeando liquidação no Nasdaq."
            })
        elif usdjpy <= 150.0:
            triggers.append({
                "id": "YEN_UNWIND_ALERT", "severity": "WARNING",
                "title": "PRESSÃO NO CARRY TRADE DO IENE (USD/JPY <= 150.0)",
                "description": f"USD/JPY em {usdjpy:.2f}. Monitoramento intensivo de chamadas de margem."
            })
        if hyg_lqd < 0.7300:
            triggers.append({
                "id": "CREDIT_FREEZE", "severity": "CRITICAL",
                "title": "CONGELAMENTO DE CRÉDITO CORPORATIVO (HYG/LQD < 0.730)",
                "description": f"Razão HYG/LQD despencou para {hyg_lqd:.4f}. Spreads de dívida privada e Data Center ABS em disparada."
            })
        if tnx >= 5.30:
            triggers.append({
                "id": "TREASURY_SPIKE", "severity": "CRITICAL",
                "title": "RENDIMENTO DO TESOURO DOS EUA EXTREMO (> 5.30%)",
                "description": f"Yield de 10 anos em {tnx:.3f}%. Risco agudo de rolagem de dívidas para infraestrutura."
            })
        if skew >= 165.0 and vvix >= 115.0:
            triggers.append({
                "id": "BLACK_SWAN_SKEW", "severity": "WARNING",
                "title": "ALERTA DE CISNE NEGRO: SKEW EXTREMO (> 165)",
                "description": f"SKEW em {skew:.1f} com VVIX em {vvix:.1f}. Demanda parabólica por proteções fora do dinheiro."
            })

        STATE.active_triggers = triggers

        # Company Radar
        company_rows = []
        for ticker, info in TRACKED_ENTITIES.items():
            if info["group"] == "stock":
                m_data = STATE.metrics.get(ticker, {})
                price = m_data.get("price", 0.0)
                chg = m_data.get("change_pct", 0.0)
                h52 = m_data.get("high_52w", price * 1.1)
                l52 = m_data.get("low_52w", price * 0.8)
                range_pct = 50.0
                if h52 > l52:
                    range_pct = max(0.0, min(100.0, ((price - l52) / (h52 - l52)) * 100.0))
                
                status_flag = "NORMAL"
                if chg <= -3.0:
                    status_flag = "DISSIPATING"
                elif chg >= 2.5:
                    status_flag = "EXPANDING"

                DB.update_company_snapshot(ticker, info["name"], info["category"], price, chg, h52, l52, status_flag)

                company_rows.append({
                    "ticker": ticker,
                    "name": info["name"],
                    "category": info["category"],
                    "desc": info["desc"],
                    "price": price,
                    "change_pct": chg,
                    "high_52w": h52,
                    "low_52w": l52,
                    "range_pct": round(range_pct, 1),
                    "status_flag": status_flag
                })

        STATE.company_radar = company_rows

    DB.record_scenario_probabilities(
        stress=STATE.scenarios["overall_stress"],
        s1=STATE.scenarios["scenario_1"],
        s2=STATE.scenarios["scenario_2"],
        s3=STATE.scenarios["scenario_3"],
        soft_landing=STATE.scenarios["soft_landing"],
        vix=vix, usdjpy=usdjpy, hyg_lqd=hyg_lqd, tnx=tnx,
        notes=f"Auto tick: VIX={vix}, JPY={usdjpy}, TNX={tnx}"
    )

# -------------------------------------------------------------
# BACKGROUND WORKER THREAD
# -------------------------------------------------------------
def background_market_worker():
    """Continuous polling worker querying public APIs & logging to SQLite."""
    print("  [Worker] Thread de coleta contínua ativada.")

    debt, ddate = fetch_us_debt()
    if debt:
        with STATE.lock:
            STATE.us_debt_trillion = debt
            STATE.us_debt_date = ddate
            STATE.add_event("SUCCESS", f"Dívida Soberana dos EUA atualizada: ${debt} Triliões ({ddate})")

    while True:
        try:
            for ticker in TRACKED_ENTITIES.keys():
                data = fetch_ticker_data(ticker)
                if data:
                    with STATE.lock:
                        old_price = STATE.metrics.get(ticker, {}).get("price", data["price"])
                        velocity = round(data["price"] - old_price, 3)
                        data["velocity_1h"] = velocity
                        STATE.metrics[ticker] = data
                    
                    DB.record_tick(
                        ticker=ticker,
                        price=data["price"],
                        prev_close=data["prev"],
                        change_pct=data["change_pct"],
                        velocity_1h=data["velocity_1h"],
                        high_52w=data["high_52w"],
                        low_52w=data["low_52w"]
                    )
                time.sleep(0.12)

            with STATE.lock:
                STATE.poll_count += 1
                STATE.last_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            compute_mathematical_scenarios()

            # Append newest real ticks to live charts
            now_label = datetime.now().strftime("%H:%M:%S")
            with STATE.lock:
                v = STATE.metrics.get("^VIX", {}).get("price")
                y = STATE.metrics.get("USDJPY=X", {}).get("price")
                t = STATE.metrics.get("^TNX", {}).get("price")
                hl = STATE.ratios.get("hyg_lqd_ratio")

                if v: STATE.chart_series["vix"].append({"time": now_label, "val": v})
                if y: STATE.chart_series["usdjpy"].append({"time": now_label, "val": y})
                if t: STATE.chart_series["tnx"].append({"time": now_label, "val": t})
                if hl: STATE.chart_series["hyg_lqd"].append({"time": now_label, "val": hl})

                for k in STATE.chart_series:
                    if len(STATE.chart_series[k]) > 60:
                        STATE.chart_series[k].pop(0)

                crit_count = len([tr for tr in STATE.active_triggers if tr["severity"] == "CRITICAL"])
                if crit_count > 0:
                    STATE.add_event("CRITICAL", f"🚨 ALARME: {crit_count} gatilho(s) crítico(s) detectado(s)!")
                    if sys.platform == "win32":
                        try:
                            import winsound
                            winsound.Beep(1200, 250)
                        except Exception:
                            pass

        except Exception as e:
            with STATE.lock:
                STATE.add_event("ERROR", f"Erro no ciclo de atualização: {e}")

        time.sleep(STATE.poll_interval)

# -------------------------------------------------------------
# UNIFIED PANORAMIC FRONTEND (HTML/CSS/JS)
# -------------------------------------------------------------
UNIFIED_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cockpit Executivo: Risco de Quebra de Mercado & Bolha de IA</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-base: #06090f;
      --bg-surface: #0b111e;
      --bg-card: rgba(15, 23, 42, 0.75);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --border-color: rgba(51, 65, 85, 0.5);
      --border-accent: rgba(56, 189, 248, 0.35);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --accent-cyan: #38bdf8;
      --accent-amber: #f59e0b;
      --accent-emerald: #10b981;
      --accent-rose: #f43f5e;
      --accent-purple: #a855f7;
      --glow-danger: 0 0 25px rgba(244, 63, 94, 0.4);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.04) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(244, 63, 94, 0.04) 0%, transparent 40%);
    }

    header {
      background: rgba(10, 15, 29, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 0.75rem 2rem;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }
    .brand-badge {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: white;
      font-weight: 800;
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .brand-title {
      font-size: 1.2rem;
      font-weight: 700;
      letter-spacing: -0.3px;
    }
    .brand-subtitle {
      font-size: 0.76rem;
      color: var(--text-muted);
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }

    .live-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--accent-emerald);
      padding: 0.35rem 0.8rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
    }
    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-emerald);
      box-shadow: 0 0 10px var(--accent-emerald);
      animation: pulse-dot 1.8s infinite;
    }
    @keyframes pulse-dot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }

    .btn-action {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.4rem 0.85rem;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s ease;
      font-family: 'Outfit', sans-serif;
    }
    .btn-action:hover {
      background: rgba(51, 65, 85, 0.95);
      border-color: var(--accent-cyan);
      transform: translateY(-1px);
    }
    .btn-alarm-active {
      background: rgba(244, 63, 94, 0.2) !important;
      border-color: var(--accent-rose) !important;
      color: #fda4af !important;
    }

    /* TOP BANNER CRITICAL ALERT */
    #crisis-banner {
      display: none;
      background: linear-gradient(90deg, rgba(225, 29, 72, 0.95), rgba(159, 18, 57, 0.95));
      color: white;
      padding: 0.85rem 2rem;
      font-weight: 700;
      font-size: 0.95rem;
      border-bottom: 2px solid #fda4af;
      box-shadow: var(--glow-danger);
      animation: pulse-alert 1.2s infinite alternate;
    }
    @keyframes pulse-alert {
      from { filter: brightness(1); }
      to { filter: brightness(1.2); }
    }
    .banner-inner {
      max-width: 1700px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    main {
      max-width: 1700px;
      margin: 1.25rem auto;
      padding: 0 1.25rem 3rem 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .section-title {
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.6rem;
    }

    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.15rem;
      backdrop-filter: blur(10px);
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .card:hover { border-color: var(--border-accent); }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.9rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .card-title {
      font-size: 0.84rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    /* ROW 1: TOP 3-COLUMN COCKPIT */
    .cockpit-grid {
      display: grid;
      grid-template-columns: 340px 1fr 360px;
      gap: 1.25rem;
    }
    @media (max-width: 1250px) {
      .cockpit-grid { grid-template-columns: 1fr; }
    }

    /* GAUGE */
    .gauge-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0.5rem 0;
      position: relative;
    }
    .gauge-dial {
      position: relative;
      width: 210px;
      height: 105px;
      overflow: hidden;
    }
    .gauge-semi {
      width: 210px;
      height: 210px;
      border-radius: 50%;
      border: 17px solid #1e293b;
      border-bottom-color: transparent;
      border-left-color: transparent;
      transform: rotate(-45deg);
      position: absolute;
      top: 0; left: 0;
      box-sizing: border-box;
    }
    .gauge-fill {
      width: 210px;
      height: 210px;
      border-radius: 50%;
      border: 17px solid transparent;
      border-top-color: var(--accent-amber);
      border-right-color: var(--accent-amber);
      transform: rotate(41deg);
      position: absolute;
      top: 0; left: 0;
      box-sizing: border-box;
      transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .gauge-center-text {
      position: absolute;
      bottom: 5px;
      text-align: center;
      width: 100%;
    }
    .gauge-value {
      font-size: 2.6rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--accent-amber);
      line-height: 1;
    }
    .gauge-sublabel {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 0.25rem;
    }
    .gauge-badge {
      display: inline-block;
      margin-top: 0.6rem;
      padding: 0.2rem 0.75rem;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 700;
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent-amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* SCENARIO BARS */
    .scenario-box { margin-bottom: 0.75rem; }
    .scenario-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      font-weight: 600;
      margin-bottom: 0.3rem;
    }
    .scenario-bar-bg {
      background: rgba(30, 41, 59, 0.6);
      border-radius: 6px;
      height: 8px;
      overflow: hidden;
      display: flex;
    }
    .scenario-bar-fill {
      height: 100%;
      border-radius: 6px;
      transition: width 0.8s ease;
    }
    .scenario-desc {
      font-size: 0.7rem;
      color: #94a3b8;
      margin-top: 0.2rem;
      font-family: 'JetBrains Mono', monospace;
    }

    /* TRIGGER ITEMS */
    .trigger-item {
      padding: 0.6rem 0.75rem;
      border-radius: 8px;
      margin-bottom: 0.45rem;
      font-size: 0.78rem;
      line-height: 1.35;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }
    .trigger-critical {
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.4);
      color: #fecdd3;
    }
    .trigger-warning {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fde68a;
    }

    /* ROW 2: VELOCIMETERS GRID (6 CARDS) */
    .velocimeters-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1rem;
    }
    .metric-card {
      background: rgba(10, 15, 30, 0.6);
      border: 1px solid rgba(51, 65, 85, 0.4);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.4);
    }
    .m-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 0.25rem;
    }
    .m-value {
      font-size: 1.45rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-main);
      display: flex;
      align-items: baseline;
      gap: 0.4rem;
    }
    .m-delta {
      font-size: 0.74rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }
    .delta-up { color: var(--accent-rose); }
    .delta-down { color: var(--accent-emerald); }
    .delta-neutral { color: var(--text-muted); }
    .m-subtext {
      font-size: 0.68rem;
      color: #64748b;
      margin-top: 0.25rem;
      font-family: 'JetBrains Mono', monospace;
    }

    /* ROW 3: UNIFIED 4 REAL HISTORICAL CHARTS */
    .charts-grid-4 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.25rem;
    }
    @media (max-width: 1000px) {
      .charts-grid-4 { grid-template-columns: 1fr; }
    }
    .chart-box {
      position: relative;
      height: 230px;
      width: 100%;
    }

    /* ROW 4: COMPANY STOCKS TABLE */
    .company-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }
    .company-table th {
      text-align: left;
      padding: 0.65rem 0.8rem;
      color: var(--text-muted);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.7rem;
    }
    .company-table td {
      padding: 0.7rem 0.8rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .company-table tr:hover { background: rgba(30, 41, 59, 0.35); }

    .range-bar-container {
      width: 110px;
      height: 6px;
      background: #1e293b;
      border-radius: 4px;
      position: relative;
      overflow: hidden;
      display: inline-block;
      vertical-align: middle;
      margin: 0 0.4rem;
    }
    .range-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      border-radius: 4px;
    }

    /* ROW 5: DATABASE & LOG DUAL ROW */
    .bottom-grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 1.25rem;
    }
    @media (max-width: 1000px) {
      .bottom-grid { grid-template-columns: 1fr; }
    }

    .log-stream {
      height: 140px;
      overflow-y: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding-right: 0.4rem;
    }
    .log-entry {
      display: flex;
      gap: 0.5rem;
      padding: 0.15rem 0;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
    }
    .log-time { color: #64748b; min-width: 60px; }
    .log-level-CRITICAL { color: var(--accent-rose); font-weight: 700; }
    .log-level-WARNING { color: var(--accent-amber); font-weight: 700; }
    .log-level-INFO { color: var(--accent-cyan); }
    .log-level-SUCCESS { color: var(--accent-emerald); }

    footer {
      border-top: 1px solid var(--border-color);
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 0.78rem;
      max-width: 1700px;
      margin: 0 auto;
      flex-wrap: wrap;
      gap: 0.8rem;
    }
  </style>
</head>
<body>

  <!-- TOP BANNER FOR CRITICAL CRISIS DISLOCATION -->
  <div id="crisis-banner">
    <div class="banner-inner">
      <div id="crisis-banner-text">🚨 ESTADO DE CRISE ATIVO: ALERTA SISTÊMICO DETECTADO</div>
      <button class="btn-action" onclick="silenceCurrentAlert()" style="background: white; color: #9f1239; border: none;">Silenciar Alarme (30s)</button>
    </div>
  </div>

  <header>
    <div class="brand">
      <span class="brand-badge">UNIFIED COCKPIT V3</span>
      <div>
        <div class="brand-title">AI Infrastructure &amp; Credit Bubble Watchdog</div>
        <div class="brand-subtitle">Monitoramento Panorâmico em Tempo Real • Séries Históricas • SQLite Local • 3 Cenários</div>
      </div>
    </div>

    <div class="header-controls">
      <div class="live-pill">
        <span class="live-dot"></span>
        <span id="update-timestamp">Conectando...</span>
      </div>
      <button id="btn-toggle-sound" class="btn-action btn-alarm-active" onclick="toggleAudioAlerts()">
        <span id="sound-icon">🔊</span> Alarme Ativado
      </button>
      <button class="btn-action" onclick="testSoundAlert()">
        🔔 Testar Sirene
      </button>
      <button class="btn-action" onclick="refreshNow()">
        🔄 Sincronizar
      </button>
    </div>
  </header>

  <main>
    
    <!-- 1. TOP COCKPIT: GAUGE + SCENARIOS + TRIGGERS -->
    <div class="cockpit-grid">
      
      <!-- GAUGE -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">📊 Risco de Quebra Calibrado</span>
          <span style="font-size: 0.75rem; color: #64748b; font-family: 'JetBrains Mono', monospace;">Modelo 2026-2029</span>
        </div>
        <div class="gauge-container">
          <div class="gauge-dial">
            <div class="gauge-semi"></div>
            <div id="gauge-fill" class="gauge-fill"></div>
            <div class="gauge-center-text">
              <div id="gauge-number" class="gauge-value">48.0%</div>
              <div class="gauge-sublabel">Stress Index</div>
            </div>
          </div>
          <div id="gauge-badge" class="gauge-badge">Regime de Estresse Elevado</div>
          <p style="font-size: 0.73rem; color: var(--text-muted); text-align: center; margin-top: 0.75rem; line-height: 1.4;">
            Probabilidade acumulada: <strong style="color: #6ee7b7;" id="label-soft">52.0% Soft Landing</strong> vs <strong style="color: #fde68a;" id="label-stress">48.0% Risco de Quebra</strong>.
          </p>
        </div>
      </div>

      <!-- MATHEMATICAL SCENARIO BARS -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">📐 Aproximação Matemática dos 3 Cenários</span>
          <span style="font-size: 0.73rem; color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace;">Multi-Factor Sensitivities</span>
        </div>
        
        <div class="scenario-box">
          <div class="scenario-header">
            <span><strong>Cenário 1: Desinflação &amp; Compressão de Múltiplos</strong></span>
            <span id="scen-p1-val" style="color: var(--accent-cyan); font-family: 'JetBrains Mono'; font-weight: 700;">42.0%</span>
          </div>
          <div class="scenario-bar-bg">
            <div id="scen-p1-bar" class="scenario-bar-fill" style="width: 42%; background: linear-gradient(90deg, #0284c7, #38bdf8);"></div>
          </div>
          <div id="scen-p1-attr" class="scenario-desc">Yield 10A em 5,14% comprimindo DCFs de tecnologia.</div>
        </div>

        <div class="scenario-box">
          <div class="scenario-header">
            <span><strong>Cenário 2: Crédito ABS &amp; Gargalo de Rede Elétrica</strong></span>
            <span id="scen-p2-val" style="color: var(--accent-amber); font-family: 'JetBrains Mono'; font-weight: 700;">40.0%</span>
          </div>
          <div class="scenario-bar-bg">
            <div id="scen-p2-bar" class="scenario-bar-fill" style="width: 40%; background: linear-gradient(90deg, #d97706, #f59e0b);"></div>
          </div>
          <div id="scen-p2-attr" class="scenario-desc">Fila de transmissão congelada (PJM/Essex); ratio HYG/LQD em 0,747.</div>
        </div>

        <div class="scenario-box">
          <div class="scenario-header">
            <span><strong>Cenário 3: Multi-Contágio Sistêmico Global</strong></span>
            <span id="scen-p3-val" style="color: var(--accent-rose); font-family: 'JetBrains Mono'; font-weight: 700;">18.0%</span>
          </div>
          <div class="scenario-bar-bg">
            <div id="scen-p3-bar" class="scenario-bar-fill" style="width: 18%; background: linear-gradient(90deg, #e11d48, #f43f5e);"></div>
          </div>
          <div id="scen-p3-attr" class="scenario-desc">USD/JPY a 158,4; sem gatilho de ruptura cambial imediata.</div>
        </div>

        <div class="scenario-box" style="margin-bottom: 0; padding-top: 0.35rem; border-top: 1px dashed rgba(255,255,255,0.08);">
          <div class="scenario-header">
            <span><strong>Absorção Produtiva / Soft Landing</strong></span>
            <span id="scen-soft-val" style="color: var(--accent-emerald); font-family: 'JetBrains Mono'; font-weight: 700;">52.0%</span>
          </div>
          <div class="scenario-bar-bg">
            <div id="scen-soft-bar" class="scenario-bar-fill" style="width: 52%; background: linear-gradient(90deg, #059669, #10b981);"></div>
          </div>
        </div>
      </div>

      <!-- ACTIVE CRISIS TRIGGERS -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">🚨 Relés &amp; Gatilhos de Crise</span>
          <span id="trigger-count" style="background: rgba(244,63,94,0.2); color: #fda4af; padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 700; font-size: 0.74rem;">0 Ativos</span>
        </div>
        <div id="triggers-list" style="max-height: 215px; overflow-y: auto;">
          <div style="color: #64748b; font-size: 0.78rem; text-align: center; padding: 2rem 0;">
            Nenhum gatilho de rompimento disparado no momento. Sistema operando em estabilidade de alerta.
          </div>
        </div>
      </div>

    </div>

    <!-- 2. SIX REAL-TIME KEY VELOCIMETERS -->
    <div>
      <div class="section-title">⚡ Velocímetros dos Índices Críticos (APIs Públicas em Tempo Real)</div>
      <div class="velocimeters-grid">
        
        <div class="metric-card">
          <div class="m-header"><span>CBOE VIX SPOT</span><span id="vix-badge" style="color: var(--accent-amber); font-weight: 700;">VIGÍLIA</span></div>
          <div class="m-value"><span id="val-vix">18.58</span><span id="delta-vix" class="m-delta delta-up">+0.92%</span></div>
          <div class="m-subtext">Gatilho Vol-Targeting: &gt; 25.0</div>
        </div>

        <div class="metric-card">
          <div class="m-header"><span>USD/JPY (IENE)</span><span id="yen-badge" style="color: var(--accent-emerald); font-weight: 700;">NORMAL</span></div>
          <div class="m-value"><span id="val-usdjpy">158.45</span><span id="delta-usdjpy" class="m-delta delta-neutral">-0.01%</span></div>
          <div class="m-subtext">Ruptura Carry Trade: &lt; 145.0</div>
        </div>

        <div class="metric-card">
          <div class="m-header"><span>US 10Y YIELD</span><span style="color: var(--accent-rose); font-weight: 700;">PRESSÃO</span></div>
          <div class="m-value"><span id="val-tnx">5.144%</span><span id="delta-tnx" class="m-delta delta-neutral">0.00%</span></div>
          <div class="m-subtext">Custo de Capital Soberano</div>
        </div>

        <div class="metric-card">
          <div class="m-header"><span>CBOE SKEW INDEX</span><span style="color: var(--accent-rose); font-weight: 700;">CAUDA ALTA</span></div>
          <div class="m-value"><span id="val-skew">168.59</span><span id="delta-skew" class="m-delta delta-neutral">0.00%</span></div>
          <div class="m-subtext">Black Swan Put Skew</div>
        </div>

        <div class="metric-card">
          <div class="m-header"><span>RAZÃO HYG / LQD</span><span style="color: var(--accent-amber); font-weight: 700;">APERTO</span></div>
          <div class="m-value"><span id="val-credit-ratio">0.7473</span></div>
          <div class="m-subtext">Apetite a Risco Data Center ABS</div>
        </div>

        <div class="metric-card">
          <div class="m-header"><span>DÍVIDA SOBERANA EUA</span><span style="color: var(--accent-rose); font-weight: 700;">RECORDE</span></div>
          <div class="m-value"><span id="val-us-debt">$40.39 T</span></div>
          <div class="m-subtext">US Treasury Fiscal Data API</div>
        </div>

      </div>
    </div>

    <!-- 3. UNIFIED 4 REAL HISTORICAL CHARTS (ALL 100% PRE-LOADED) -->
    <div>
      <div class="section-title">📈 Comportamento dos Índices (Séries Históricas de 5 Dias Pré-Carregadas)</div>
      <div class="charts-grid-4">
        
        <div class="card">
          <div class="card-header">
            <span class="card-title">⚡ Índices de Volatilidade: VIX Spot (5 Dias Reais)</span>
            <span style="font-size: 0.72rem; color: #f59e0b; font-family: 'JetBrains Mono';">CBOE VIX</span>
          </div>
          <div class="chart-box"><canvas id="chartVix"></canvas></div>
        </div>

        <div class="card">
          <div class="card-header">
            <span class="card-title">💴 Canal de Liquidez: USD/JPY (Carry Trade Anchor)</span>
            <span style="font-size: 0.72rem; color: #38bdf8; font-family: 'JetBrains Mono';">FX Spot</span>
          </div>
          <div class="chart-box"><canvas id="chartYen"></canvas></div>
        </div>

        <div class="card">
          <div class="card-header">
            <span class="card-title">💳 Risco de Crédito: Razão HYG / LQD (Spreads Corporativos)</span>
            <span style="font-size: 0.72rem; color: #10b981; font-family: 'JetBrains Mono';">High Yield / IG</span>
          </div>
          <div class="chart-box"><canvas id="chartCredit"></canvas></div>
        </div>

        <div class="card">
          <div class="card-header">
            <span class="card-title">🏛️ Rendimento Soberano: US 10-Year Treasury Yield</span>
            <span style="font-size: 0.72rem; color: #ec4899; font-family: 'JetBrains Mono';">^TNX (%)</span>
          </div>
          <div class="chart-box"><canvas id="chartTreasury"></canvas></div>
        </div>

      </div>
    </div>

    <!-- 4. COMPANY RADAR: AI HARDWARE, HYPERSCALERS & POWER GRID -->
    <div>
      <div class="section-title">🏢 Radar de Empresas: Ações de IA, Hiperscalers &amp; Gargalo Elétrico</div>
      <div class="card" style="padding: 0.5rem 1rem;">
        <div style="overflow-x: auto;">
          <table class="company-table">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Empresa / Ativo</th>
                <th>Segmento</th>
                <th>Preço Real</th>
                <th>Var. 1D</th>
                <th>Range 52 Semanas (Mín / Atual / Máx)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="company-table-body">
              <!-- Populated via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 5. LOCAL SQLITE DATABASE STATS & REAL-TIME EVENT STREAM -->
    <div class="bottom-grid">
      
      <!-- SQLITE LOCAL DB STATS -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">🗄️ Banco Local SQLite</span>
          <span style="font-size: 0.72rem; color: #10b981; font-family: 'JetBrains Mono';">Persistente</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.6rem; font-family: 'JetBrains Mono'; font-size: 0.8rem;">
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.3rem;">
            <span style="color: #94a3b8;">Ticks Gravados:</span>
            <strong style="color: var(--accent-cyan);" id="db-ticks-count">0</strong>
          </div>
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.3rem;">
            <span style="color: #94a3b8;">Cálculos de Cenários:</span>
            <strong style="color: var(--accent-amber);" id="db-scenario-count">0</strong>
          </div>
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.3rem;">
            <span style="color: #94a3b8;">Tamanho do Banco:</span>
            <strong style="color: var(--accent-emerald);" id="db-size-val">0 KB</strong>
          </div>
          <div style="font-size: 0.7rem; color: #64748b; word-break: break-all; margin-top: 0.2rem;">
            Arquivo: <code id="db-path-val">data/crisis_dashboard.db</code>
          </div>
        </div>
      </div>

      <!-- AUDITED EVENT STREAM -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">📜 Registro Contínuo de Eventos e Anomalias de Mercado</span>
          <span style="font-size: 0.72rem; color: #64748b; font-family: 'JetBrains Mono';">Audited Stream</span>
        </div>
        <div id="event-log" class="log-stream"></div>
      </div>

    </div>

  </main>

  <footer>
    <div>
      <strong>Cockpit Executivo Unificado • Risco de Quebra &amp; Bolha de IA</strong> • Repositório: <code>xToshiro/ai-market-crash-risk</code>
    </div>
    <div>
      Dados 100% Reais de APIs Públicas (CBOE, FRED, US Treasury Fiscal Data, Yahoo Finance).
    </div>
  </footer>

  <script>
    let audioContext = null;
    let isAudioMuted = false;
    let alarmSilencedUntil = 0;
    let charts = {};

    function initAudio() {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function playCrisisSiren() {
      if (isAudioMuted || Date.now() < alarmSilencedUntil) return;
      try {
        initAudio();
        if (audioContext.state === 'suspended') {
          audioContext.resume();
        }
        const now = audioContext.currentTime;
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(587.33, now + 0.35);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.7);

        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.75);

        osc.connect(gain);
        gain.connect(audioContext.destination);

        osc.start(now);
        osc.stop(now + 0.75);
      } catch (e) {
        console.warn('Audio blocked:', e);
      }
    }

    function toggleAudioAlerts() {
      isAudioMuted = !isAudioMuted;
      const btn = document.getElementById('btn-toggle-sound');
      if (isAudioMuted) {
        btn.classList.remove('btn-alarm-active');
        btn.innerHTML = '<span>🔇</span> Alarme Desativado';
      } else {
        btn.classList.add('btn-alarm-active');
        btn.innerHTML = '<span>🔊</span> Alarme Ativado';
        initAudio();
      }
    }

    function testSoundAlert() {
      initAudio();
      isAudioMuted = false;
      alarmSilencedUntil = 0;
      document.getElementById('btn-toggle-sound').classList.add('btn-alarm-active');
      document.getElementById('btn-toggle-sound').innerHTML = '<span>🔊</span> Alarme Ativado';
      playCrisisSiren();
      
      fetch('/api/test-alert')
        .then(r => r.json())
        .then(d => updateUI(d));
    }

    function silenceCurrentAlert() {
      alarmSilencedUntil = Date.now() + 30000;
      document.getElementById('crisis-banner').style.display = 'none';
    }

    // Chart Initializer with Auto-Scaling Y-Axes
    function initChart(canvasId, label, color, fillColor) {
      const ctx = document.getElementById(canvasId).getContext('2d');
      return new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: label,
            borderColor: color,
            backgroundColor: fillColor || 'transparent',
            fill: !!fillColor,
            data: [],
            borderWidth: 2,
            pointRadius: 1,
            tension: 0.15
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 300 },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8 }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.04)' },
              ticks: { color: color, font: { family: 'JetBrains Mono', size: 9 } }
            }
          },
          plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'Outfit', size: 10 } } }
          }
        }
      });
    }

    function initAllFourCharts() {
      charts.vix = initChart('chartVix', 'VIX Spot', '#f59e0b', 'rgba(245, 158, 11, 0.06)');
      charts.yen = initChart('chartYen', 'USD/JPY Spot', '#38bdf8', 'rgba(56, 189, 248, 0.06)');
      charts.credit = initChart('chartCredit', 'Razão HYG / LQD', '#10b981', 'rgba(16, 185, 129, 0.06)');
      charts.treasury = initChart('chartTreasury', 'Yield 10 Anos (%)', '#ec4899', 'rgba(236, 72, 153, 0.06)');
    }

    function populateChartData(chartInstance, seriesPoints) {
      if (!chartInstance || !seriesPoints || seriesPoints.length === 0) return;
      chartInstance.data.labels = seriesPoints.map(p => p.time);
      chartInstance.data.datasets[0].data = seriesPoints.map(p => p.val);
      chartInstance.update('none');
    }

    function updateUI(data) {
      if (!data) return;

      document.getElementById('update-timestamp').innerText = data.last_updated || 'Ao Vivo';

      // 1. Update Gauge
      const stress = data.scenarios ? data.scenarios.overall_stress : 48.0;
      document.getElementById('gauge-number').innerText = stress.toFixed(1) + '%';
      const deg = -45 + (stress / 100.0) * 180;
      document.getElementById('gauge-fill').style.transform = `rotate(${deg}deg)`;

      const badge = document.getElementById('gauge-badge');
      if (stress >= 65) {
        badge.innerText = 'ESTADO DE CRISE AGUDA';
        badge.style.background = 'rgba(244, 63, 94, 0.2)';
        badge.style.color = '#fda4af';
        document.getElementById('gauge-fill').style.borderTopColor = '#f43f5e';
        document.getElementById('gauge-fill').style.borderRightColor = '#f43f5e';
      } else if (stress >= 45) {
        badge.innerText = 'REGIME DE ESTRESSE ELEVADO (48%)';
        badge.style.background = 'rgba(245, 158, 11, 0.2)';
        badge.style.color = '#fde68a';
        document.getElementById('gauge-fill').style.borderTopColor = '#f59e0b';
        document.getElementById('gauge-fill').style.borderRightColor = '#f59e0b';
      } else {
        badge.innerText = 'ZONA DE ABSORÇÃO BENIGNA';
        badge.style.background = 'rgba(16, 185, 129, 0.2)';
        badge.style.color = '#6ee7b7';
        document.getElementById('gauge-fill').style.borderTopColor = '#10b981';
        document.getElementById('gauge-fill').style.borderRightColor = '#10b981';
      }

      if (data.scenarios) {
        document.getElementById('label-stress').innerText = stress.toFixed(1) + '% Risco de Quebra';
        document.getElementById('label-soft').innerText = data.scenarios.soft_landing.toFixed(1) + '% Soft Landing';

        const sc = data.scenarios;
        document.getElementById('scen-p1-val').innerText = sc.scenario_1.toFixed(1) + '%';
        document.getElementById('scen-p1-bar').style.width = sc.scenario_1 + '%';
        document.getElementById('scen-p1-attr').innerText = sc.attributions.s1_drivers;

        document.getElementById('scen-p2-val').innerText = sc.scenario_2.toFixed(1) + '%';
        document.getElementById('scen-p2-bar').style.width = sc.scenario_2 + '%';
        document.getElementById('scen-p2-attr').innerText = sc.attributions.s2_drivers;

        document.getElementById('scen-p3-val').innerText = sc.scenario_3.toFixed(1) + '%';
        document.getElementById('scen-p3-bar').style.width = sc.scenario_3 + '%';
        document.getElementById('scen-p3-attr').innerText = sc.attributions.s3_drivers;

        document.getElementById('scen-soft-val').innerText = sc.soft_landing.toFixed(1) + '%';
        document.getElementById('scen-soft-bar').style.width = sc.soft_landing + '%';
      }

      // 2. Update Key Metrics
      const m = data.metrics || {};
      function setM(ticker, valId, deltaId) {
        if (!m[ticker]) return;
        const p = m[ticker].price;
        const c = m[ticker].change_pct;
        const elV = document.getElementById(valId);
        const elD = document.getElementById(deltaId);
        if (elV) elV.innerText = (ticker === '^TNX') ? p.toFixed(3) + '%' : p.toFixed(2);
        if (elD) {
          elD.innerText = (c >= 0 ? '+' : '') + c.toFixed(2) + '%';
          elD.className = 'm-delta ' + (c > 0 ? 'delta-up' : (c < 0 ? 'delta-down' : 'delta-neutral'));
        }
      }
      setM('^VIX', 'val-vix', 'delta-vix');
      setM('USDJPY=X', 'val-usdjpy', 'delta-usdjpy');
      setM('^TNX', 'val-tnx', 'delta-tnx');
      setM('^SKEW', 'val-skew', 'delta-skew');

      if (data.ratios && data.ratios.hyg_lqd_ratio) {
        document.getElementById('val-credit-ratio').innerText = data.ratios.hyg_lqd_ratio.toFixed(4);
      }
      if (data.us_debt_trillion) {
        document.getElementById('val-us-debt').innerText = '$' + data.us_debt_trillion.toFixed(2) + ' T';
      }

      // 3. Update Triggers
      const triggers = data.active_triggers || [];
      const trCountEl = document.getElementById('trigger-count');
      const trListEl = document.getElementById('triggers-list');
      const bannerEl = document.getElementById('crisis-banner');

      trCountEl.innerText = triggers.length + ' Ativo(s)';
      let hasCritical = false;

      if (triggers.length === 0) {
        trListEl.innerHTML = '<div style="color: #64748b; font-size: 0.78rem; text-align: center; padding: 2rem 0;">Nenhum gatilho de rompimento disparado no momento. Sistema operando em estabilidade de alerta.</div>';
        bannerEl.style.display = 'none';
      } else {
        trListEl.innerHTML = triggers.map(t => {
          if (t.severity === 'CRITICAL') hasCritical = true;
          const css = t.severity === 'CRITICAL' ? 'trigger-critical' : 'trigger-warning';
          return `
            <div class="trigger-item ${css}">
              <div style="font-weight: 700;">${t.severity === 'CRITICAL' ? '🚨' : '⚠️'} ${t.title}</div>
              <div>${t.description}</div>
            </div>
          `;
        }).join('');

        if (hasCritical && Date.now() > alarmSilencedUntil) {
          bannerEl.style.display = 'block';
          document.getElementById('crisis-banner-text').innerText = '🚨 ESTADO DE CRISE ATIVO: ' + triggers[0].title;
          playCrisisSiren();
        } else {
          bannerEl.style.display = 'none';
        }
      }

      // 4. Update Charts with Historical Real Data
      if (data.chart_series) {
        populateChartData(charts.vix, data.chart_series.vix);
        populateChartData(charts.yen, data.chart_series.usdjpy);
        populateChartData(charts.credit, data.chart_series.hyg_lqd);
        populateChartData(charts.treasury, data.chart_series.tnx);
      }

      // 5. Update Company Table
      if (data.company_radar) {
        const tbody = document.getElementById('company-table-body');
        tbody.innerHTML = data.company_radar.map(c => {
          const deltaClass = c.change_pct > 0 ? 'delta-up' : (c.change_pct < 0 ? 'delta-down' : 'delta-neutral');
          let catBadge = '<span style="background: rgba(56,189,248,0.15); color: #38bdf8; padding: 0.15rem 0.45rem; border-radius: 4px; font-size: 0.68rem; font-weight: 700;">SILICON</span>';
          if (c.category === 'hyperscaler') catBadge = '<span style="background: rgba(168,85,247,0.15); color: #c084fc; padding: 0.15rem 0.45rem; border-radius: 4px; font-size: 0.68rem; font-weight: 700;">HYPERSCALER</span>';
          if (c.category === 'energy') catBadge = '<span style="background: rgba(245,158,11,0.15); color: #fbbf24; padding: 0.15rem 0.45rem; border-radius: 4px; font-size: 0.68rem; font-weight: 700;">GRID &amp; POWER</span>';

          return `
            <tr>
              <td><strong style="color: #f8fafc; font-family: 'JetBrains Mono';">${c.ticker}</strong></td>
              <td>
                <div style="font-weight: 600; color: #f1f5f9;">${c.name}</div>
                <div style="font-size: 0.7rem; color: #64748b;">${c.desc}</div>
              </td>
              <td>${catBadge}</td>
              <td style="font-family: 'JetBrains Mono'; font-weight: 700;">$${c.price.toFixed(2)}</td>
              <td class="${deltaClass}" style="font-family: 'JetBrains Mono'; font-weight: 700;">
                ${c.change_pct >= 0 ? '+' : ''}${c.change_pct.toFixed(2)}%
              </td>
              <td style="font-family: 'JetBrains Mono'; font-size: 0.72rem;">
                <span style="color: #64748b;">$${c.low_52w.toFixed(0)}</span>
                <div class="range-bar-container">
                  <div class="range-bar-fill" style="width: ${c.range_pct}%;"></div>
                </div>
                <span style="color: #94a3b8;">$${c.high_52w.toFixed(0)}</span>
              </td>
              <td>
                <span style="font-size: 0.72rem; font-weight: 700; color: ${c.status_flag === 'DISSIPATING' ? '#f43f5e' : (c.status_flag === 'EXPANDING' ? '#10b981' : '#94a3b8')};">
                  ${c.status_flag}
                </span>
              </td>
            </tr>
          `;
        }).join('');
      }

      // 6. Update Event Log
      const logEl = document.getElementById('event-log');
      const logs = data.event_log || [];
      logEl.innerHTML = logs.map(l => `
        <div class="log-entry">
          <span class="log-time">[${l.time}]</span>
          <span class="log-level-${l.level}">${l.level}</span>
          <span>${l.msg}</span>
        </div>
      `).join('');

      // 7. Update DB Stats
      if (data.db_stats) {
        document.getElementById('db-ticks-count').innerText = data.db_stats.ticks_count;
        document.getElementById('db-scenario-count').innerText = data.db_stats.scenario_count;
        document.getElementById('db-size-val').innerText = data.db_stats.db_size_kb + ' KB';
      }
    }

    function refreshNow() {
      fetch('/api/state')
        .then(r => r.json())
        .then(d => updateUI(d))
        .catch(err => console.error(err));
    }

    window.addEventListener('DOMContentLoaded', () => {
      initAllFourCharts();
      refreshNow();
      setInterval(refreshNow, 3000);

      document.body.addEventListener('click', () => {
        initAudio();
      }, { once: true });
    });
  </script>
</body>
</html>
"""

# -------------------------------------------------------------
# HTTP SERVER DISPATCHER
# -------------------------------------------------------------
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class DashboardHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(UNIFIED_DASHBOARD_HTML.encode("utf-8"))

        elif self.path == "/api/state":
            with STATE.lock:
                db_st = DB.get_stats()
                payload = {
                    "last_updated": STATE.last_updated,
                    "poll_count": STATE.poll_count,
                    "us_debt_trillion": STATE.us_debt_trillion,
                    "us_debt_date": STATE.us_debt_date,
                    "scenarios": STATE.scenarios,
                    "metrics": STATE.metrics,
                    "ratios": STATE.ratios,
                    "company_radar": STATE.company_radar,
                    "chart_series": STATE.chart_series,
                    "active_triggers": STATE.active_triggers,
                    "event_log": STATE.event_log[:25],
                    "db_stats": db_st
                }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/test-alert":
            with STATE.lock:
                STATE.simulated_alert = not STATE.simulated_alert
                status_text = "ATIVADO" if STATE.simulated_alert else "DESATIVADO"
                STATE.add_event("WARNING", f"Operador acionou teste de alarme de crise ({status_text}).")
            compute_mathematical_scenarios()
            with STATE.lock:
                db_st = DB.get_stats()
                payload = {
                    "last_updated": STATE.last_updated,
                    "scenarios": STATE.scenarios,
                    "metrics": STATE.metrics,
                    "ratios": STATE.ratios,
                    "company_radar": STATE.company_radar,
                    "chart_series": STATE.chart_series,
                    "active_triggers": STATE.active_triggers,
                    "event_log": STATE.event_log[:25],
                    "db_stats": db_st
                }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def find_available_port(start_port=5050, max_tries=20):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    return start_port

def main():
    port = find_available_port(DEFAULT_PORT)
    STATE.active_port = port

    print("=" * 80)
    print("  AI INFRASTRUCTURE & CRASH RISK — UNIFIED COCKPIT DASHBOARD (V3)")
    print("=" * 80)
    print(f"[*] Porta de conexão alocada: http://localhost:{port}")
    print(f"[*] Banco de Dados Local: {DB_PATH} (SQLite Ativo)")
    print("[*] Layout Panorâmico Unificado: Todas as métricas em tela única sem abas")
    print("[*] Pré-carregando séries históricas de 5 dias das APIs públicas...")
    
    # 1. Preload 5-day real historical data for all 4 charts
    preload_all_chart_series()

    # 2. Compute Initial Scenarios & Company Radar
    compute_mathematical_scenarios()

    # 3. Start background polling worker
    worker_thread = threading.Thread(target=background_market_worker, daemon=True)
    worker_thread.start()

    try:
        server = ThreadedHTTPServer(("0.0.0.0", port), DashboardHTTPHandler)
        print(f"\n[+] Cockpit no ar com sucesso em: http://localhost:{port}")
        print("  Pressione Ctrl+C a qualquer momento para encerrar o monitoramento.")
        print("=" * 80)

        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass

        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Encerrando monitoramento por comando do operador.")
        server.server_close()
        sys.exit(0)
    except Exception as e:
        print(f"[-] Erro fatal ao rodar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
