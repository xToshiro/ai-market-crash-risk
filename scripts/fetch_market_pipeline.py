#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_market_pipeline.py
-------------------------
Automated Market Intelligence Pipeline for AI Market Crash Risk.
Fetches:
  1. Equities & AI Infrastructure Stocks (Hyperscalers, Semis, Power/Grid, Neoclouds, Private Credit)
  2. US Macroeconomic & Financial Condition (Treasury yields, yield curves, dollar, commodities, debt metrics)
  3. Investment Flows & Credit Risk Indicators (Tech/Grid ETFs, High Yield Spreads, BDC Private Credit)

Outputs:
  - data/latest_market_metrics.csv (Consolidated master dataset)
  - data/companies_valuation_metrics.csv (Equities valuation, multiples & 2-year trajectory)
  - data/macro_financial_condition.csv (Macro, yields, sovereign debt & currency indicators)
  - data/investment_flows_credit.csv (Sector ETF flows, credit spreads & private credit proxies)
  - data/snapshots/snapshot_YYYYMMDD_HHMM.csv (Archived historical snapshot)
  - data/ai_agent_research_brief.md (Dynamic brief for AI Agent news search & report synthesis)
  - data/ai_agent_research_brief.json (Structured brief for programmatic ingestion)

Usage:
  py scripts/fetch_market_pipeline.py
  py scripts/fetch_market_pipeline.py --quick
  py scripts/fetch_market_pipeline.py --output-dir custom_data_dir
"""

import os
import sys
import datetime
import argparse
import json
import numpy as np
import pandas as pd

# UTF-8 stdout encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yfinance as yf
except ImportError:
    print("[ERROR] yfinance is required. Please run: pip install yfinance")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_DATA_DIR = os.path.join(ROOT_DIR, "data")
SNAPSHOTS_DIR = os.path.join(DEFAULT_DATA_DIR, "snapshots")

# ==============================================================================
# UNIFIED ASSET UNIVERSE & METADATA CONFIGURATION
# ==============================================================================

COMPANIES = {
    # AI Hyperscalers & Core Compute
    "NVDA": {"name": "NVIDIA Corporation", "segment": "AI Accelerators & GPU Monopoly", "category": "AI Hyperscaler"},
    "MSFT": {"name": "Microsoft Corporation", "segment": "Azure Cloud & OpenAI Anchor", "category": "AI Hyperscaler"},
    "GOOGL": {"name": "Alphabet Inc.", "segment": "Google Cloud & TPU Infrastructure", "category": "AI Hyperscaler"},
    "AMZN": {"name": "Amazon.com Inc.", "segment": "AWS Cloud & Custom Silicon (Trainium)", "category": "AI Hyperscaler"},
    "META": {"name": "Meta Platforms Inc.", "segment": "Open-Source Models (Llama) & Mega Compute", "category": "AI Hyperscaler"},
    "AAPL": {"name": "Apple Inc.", "segment": "Edge Silicon & On-Device AI Ecosystem", "category": "AI Hyperscaler"},
    "ORCL": {"name": "Oracle Corporation", "segment": "OCI Hyperscale & Multi-Cloud Clusters", "category": "AI Hyperscaler"},

    # Semiconductors, Foundries & Networking
    "TSM": {"name": "Taiwan Semiconductor Mfg Co", "segment": "Leading-Edge Foundry (3nm/2nm Monopoly)", "category": "Semiconductors"},
    "ASML": {"name": "ASML Holding N.V.", "segment": "EUV & High-NA Lithography Monopoly", "category": "Semiconductors"},
    "AVGO": {"name": "Broadcom Inc.", "segment": "Custom AI ASICs & Scale-Out Networking", "category": "Semiconductors"},
    "AMD": {"name": "Advanced Micro Devices", "segment": "MI300/MI350 GPU & EPYC CPU Alternatives", "category": "Semiconductors"},
    "QCOM": {"name": "Qualcomm Inc.", "segment": "NPU Processors & Mobile AI Silicon", "category": "Semiconductors"},

    # Energy, Nuclear, Utilities & Physical Data Centers
    "VST": {"name": "Vistra Corp", "segment": "Nuclear & Gas Generation for AI Data Centers", "category": "Power & Data Centers"},
    "CEG": {"name": "Constellation Energy", "segment": "Nuclear Generation & Microsoft Crane PPA", "category": "Power & Data Centers"},
    "NEE": {"name": "NextEra Energy", "segment": "Renewable Power & Grid Interconnections", "category": "Power & Data Centers"},
    "TLN": {"name": "Talen Energy", "segment": "Susquehanna Nuclear Campus & AWS Data Center", "category": "Power & Data Centers"},
    "EQIX": {"name": "Equinix Inc.", "segment": "Global Colocation & Network Interconnect REIT", "category": "Power & Data Centers"},
    "DLR": {"name": "Digital Realty Trust", "segment": "Wholesale Data Center REIT & ABS Issuer", "category": "Power & Data Centers"},

    # Software, Enterprise AI & Security
    "PLTR": {"name": "Palantir Technologies", "segment": "AIP Enterprise & Defense AI Operating System", "category": "Software & Security"},
    "CRWD": {"name": "CrowdStrike Holdings", "segment": "Falcon Cloud Security & AI Workload Protection", "category": "Software & Security"},
    "SNOW": {"name": "Snowflake Inc.", "segment": "Cloud Data Warehousing & LLM Ingestion", "category": "Software & Security"},
    "DDOG": {"name": "Datadog Inc.", "segment": "Cloud Observability & GPU Cluster Telemetry", "category": "Software & Security"},

    # Private Credit, Asset Managers & Direct Lenders
    "BX": {"name": "Blackstone Inc.", "segment": "Private Credit, QTS Data Centers & ABS Issuance", "category": "Private Credit & Finance"},
    "ARES": {"name": "Ares Management", "segment": "Direct Lending, Private Debt & Hardware Leases", "category": "Private Credit & Finance"},
    "APO": {"name": "Apollo Global Management", "segment": "Asset-Backed Finance & Data Center Facilities", "category": "Private Credit & Finance"},
    "KKR": {"name": "KKR & Co. Inc.", "segment": "Digital Infrastructure Funds & CyrusOne", "category": "Private Credit & Finance"},
    "BIZD": {"name": "VanEck BDC Income ETF", "segment": "Direct Lending & Private Middle Market Benchmark", "category": "Private Credit & Finance"},
}

MACRO_INDICATORS = {
    # Yields & Fixed Income
    "^TNX": {"name": "US 10-Year Treasury Yield", "unit": "%", "category": "Treasury Yields"},
    "^TYX": {"name": "US 30-Year Treasury Bond Yield", "unit": "%", "category": "Treasury Yields"},
    "^IRX": {"name": "US 13-Week Treasury Bill Yield", "unit": "%", "category": "Treasury Yields"},

    # Benchmark Indices & Volatility
    "^GSPC": {"name": "S&P 500 Index", "unit": "pts", "category": "Equity Benchmark"},
    "^IXIC": {"name": "Nasdaq Composite Index", "unit": "pts", "category": "Equity Benchmark"},
    "^NDX": {"name": "Nasdaq 100 Index", "unit": "pts", "category": "Equity Benchmark"},
    "^DJI": {"name": "Dow Jones Industrial Average", "unit": "pts", "category": "Equity Benchmark"},
    "^VIX": {"name": "CBOE Volatility Index", "unit": "pts", "category": "Market Volatility"},

    # Currencies & Commodities
    "UUP": {"name": "Invesco DB US Dollar Index (DXY Proxy)", "unit": "USD", "category": "Currency & FX"},
    "GC=F": {"name": "Gold Futures (USD/troy oz)", "unit": "USD", "category": "Monetary Hedge"},
    "CL=F": {"name": "WTI Crude Oil Futures (USD/bbl)", "unit": "USD", "category": "Energy Inflation"},
}

FLOW_INDICATORS = {
    # Sector & Thematic Flows
    "QQQ": {"name": "Invesco QQQ (Nasdaq 100 ETF)", "segment": "Tech Mega-Cap Flow Proxy", "category": "Thematic ETF"},
    "SMH": {"name": "VanEck Semiconductor ETF", "segment": "Chip Manufacturing Flow Proxy", "category": "Thematic ETF"},
    "IGV": {"name": "iShares Expanded Tech-Software ETF", "segment": "Enterprise Software Flow Proxy", "category": "Thematic ETF"},
    "XLU": {"name": "Utilities Select Sector SPDR ETF", "segment": "Power Grid & Utility Flow Proxy", "category": "Thematic ETF"},
    "PAVE": {"name": "Global X US Infrastructure Dev ETF", "segment": "Physical Grid & Infrastructure Proxy", "category": "Thematic ETF"},

    # Credit Spread Proxies
    "HYG": {"name": "iShares iBoxx $ High Yield Corporate Bond ETF", "segment": "High Yield / Junk Credit Risk Proxy", "category": "Credit Risk"},
    "LQD": {"name": "iShares iBoxx $ Investment Grade Corporate Bond ETF", "segment": "High-Grade Corporate Debt Proxy", "category": "Credit Risk"},
}

# US Sovereign Debt Benchmarks (Calibrated as of October 2026)
US_FISCAL_BENCHMARKS = {
    "US_National_Debt_USD_Trillion": 36.85,
    "US_Debt_to_GDP_Percent": 124.6,
    "US_Federal_Deficit_FY26_USD_Trillion": 1.95,
    "US_Net_Interest_Annual_Pace_USD_Trillion": 1.16,
    "Foreign_Holdings_US_Debt_Percent": 22.4,
    "Estimated_Data_Center_Power_Demand_2028_GW": 44.5,
    "Hyperscaler_Annual_CapEx_RunRate_USD_Billion": 700.0,
}

# ==============================================================================
# PIPELINE DATA EXTRACTION ENGINE
# ==============================================================================

def download_batch_history(tickers, period="2y"):
    """
    Downloads historical close prices for all tickers in a single robust batch query.
    """
    print(f"[*] Querying historical market data for {len(tickers)} assets over period='{period}'...", flush=True)
    ticker_str = " ".join(tickers)
    try:
        data = yf.download(ticker_str, period=period, progress=False, group_by="ticker", auto_adjust=True)
        return data
    except Exception as e:
        print(f"[!] Warning: Batch download encountered an error ({e}). Falling back to individual queries...", flush=True)
        return None


def extract_price_metrics(df_ticker, ticker_symbol):
    """
    Computes 1D, 1M, 6M, 1Y, and 2Y percentage changes and 52-week ranges.
    """
    metrics = {
        "price": np.nan,
        "change_1d_pct": np.nan,
        "change_1m_pct": np.nan,
        "change_6m_pct": np.nan,
        "change_1y_pct": np.nan,
        "change_2y_pct": np.nan,
        "high_52w": np.nan,
        "low_52w": np.nan,
        "pct_below_52w_high": np.nan,
    }

    if df_ticker is None or df_ticker.empty:
        return metrics

    try:
        # Resolve Close column
        if "Close" in df_ticker:
            s_close = df_ticker["Close"].dropna()
        else:
            s_close = df_ticker.dropna()

        if len(s_close) == 0:
            return metrics

        current_price = float(s_close.iloc[-1])
        metrics["price"] = round(current_price, 2)

        # 1D Change
        if len(s_close) >= 2:
            prev_1d = float(s_close.iloc[-2])
            metrics["change_1d_pct"] = round(((current_price / prev_1d) - 1.0) * 100.0, 2)

        # 1M Change (~21 trading days)
        if len(s_close) >= 22:
            prev_1m = float(s_close.iloc[-22])
            metrics["change_1m_pct"] = round(((current_price / prev_1m) - 1.0) * 100.0, 2)

        # 6M Change (~126 trading days)
        if len(s_close) >= 127:
            prev_6m = float(s_close.iloc[-127])
            metrics["change_6m_pct"] = round(((current_price / prev_6m) - 1.0) * 100.0, 2)

        # 1Y Change (~252 trading days)
        if len(s_close) >= 253:
            prev_1y = float(s_close.iloc[-253])
            metrics["change_1y_pct"] = round(((current_price / prev_1y) - 1.0) * 100.0, 2)

        # 2Y Change (earliest available up to ~504 trading days)
        prev_2y = float(s_close.iloc[0])
        metrics["change_2y_pct"] = round(((current_price / prev_2y) - 1.0) * 100.0, 2)

        # 52W High & Low (~252 trading days)
        last_year = s_close.iloc[-252:] if len(s_close) >= 252 else s_close
        h52 = float(last_year.max())
        l52 = float(last_year.min())
        metrics["high_52w"] = round(h52, 2)
        metrics["low_52w"] = round(l52, 2)
        if h52 > 0:
            metrics["pct_below_52w_high"] = round(((current_price / h52) - 1.0) * 100.0, 2)

    except Exception as e:
        print(f"[!] Error calculating metrics for {ticker_symbol}: {e}")

    return metrics


def fetch_valuation_multiples(ticker_symbol, quick_mode=False):
    """
    Fetches fundamental valuation multiples from yfinance info with error handling.
    """
    defaults = {
        "market_cap_billions": np.nan,
        "trailing_pe": np.nan,
        "forward_pe": np.nan,
        "peg_ratio": np.nan,
        "price_to_sales": np.nan,
        "ev_to_ebitda": np.nan,
        "beta": np.nan,
    }

    if quick_mode:
        return defaults

    try:
        t = yf.Ticker(ticker_symbol)
        info = t.info
        if not info:
            return defaults

        mkt_cap = info.get("marketCap")
        if mkt_cap:
            defaults["market_cap_billions"] = round(float(mkt_cap) / 1e9, 2)

        defaults["trailing_pe"] = round(float(info["trailingPE"]), 2) if info.get("trailingPE") else np.nan
        defaults["forward_pe"] = round(float(info["forwardPE"]), 2) if info.get("forwardPE") else np.nan
        defaults["peg_ratio"] = round(float(info["pegRatio"]), 2) if info.get("pegRatio") else np.nan
        defaults["price_to_sales"] = round(float(info["priceToSalesTrailing12Months"]), 2) if info.get("priceToSalesTrailing12Months") else np.nan
        defaults["ev_to_ebitda"] = round(float(info["enterpriseToEbitda"]), 2) if info.get("enterpriseToEbitda") else np.nan
        defaults["beta"] = round(float(info["beta"]), 2) if info.get("beta") else np.nan

    except Exception:
        pass

    return defaults

# ==============================================================================
# PIPELINE ORCHESTRATION & EXPORT
# ==============================================================================

def run_pipeline(output_dir=DEFAULT_DATA_DIR, quick_mode=False, save_snapshot=True):
    start_time = datetime.datetime.now()
    timestamp_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = start_time.strftime("%Y%m%d_%H%M")

    os.makedirs(output_dir, exist_ok=True)
    if save_snapshot:
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

    print("=" * 80)
    print("  AI MARKET RISK — AUTOMATED DATA INGESTION & VALUATION PIPELINE")
    print(f"  Execution Timestamp: {timestamp_str}")
    print(f"  Target Data Directory: {os.path.abspath(output_dir)}")
    print("=" * 80)

    all_tickers = list(COMPANIES.keys()) + list(MACRO_INDICATORS.keys()) + list(FLOW_INDICATORS.keys())
    batch_df = download_batch_history(all_tickers, period="2y")

    # --------------------------------------------------------------------------
    # 1. Process Equities & Valuations
    # --------------------------------------------------------------------------
    print("\n[1/3] Extracting Equities & Valuation Multiples...", flush=True)
    rows_companies = []
    for ticker, meta in COMPANIES.items():
        # Extract price trajectory
        df_t = None
        if batch_df is not None:
            try:
                if isinstance(batch_df.columns, pd.MultiIndex):
                    if ticker in batch_df.columns.levels[0]:
                        df_t = batch_df[ticker]
                    elif ticker in batch_df.columns.levels[1]:
                        df_t = batch_df.xs(ticker, axis=1, level=1)
                else:
                    df_t = batch_df
            except Exception:
                df_t = None

        if df_t is None or df_t.empty:
            try:
                df_t = yf.download(ticker, period="2y", progress=False)
            except Exception:
                df_t = None

        pm = extract_price_metrics(df_t, ticker)
        vm = fetch_valuation_multiples(ticker, quick_mode=quick_mode)

        row = {
            "Ticker": ticker,
            "Name": meta["name"],
            "Category": meta["category"],
            "Segment": meta["segment"],
            "Price_USD": pm["price"],
            "Change_1D_Pct": pm["change_1d_pct"],
            "Change_1M_Pct": pm["change_1m_pct"],
            "Change_6M_Pct": pm["change_6m_pct"],
            "Change_1Y_Pct": pm["change_1y_pct"],
            "Change_2Y_Pct": pm["change_2y_pct"],
            "High_52W": pm["high_52w"],
            "Low_52W": pm["low_52w"],
            "Pct_Below_52W_High": pm["pct_below_52w_high"],
            "Market_Cap_USD_Billion": vm["market_cap_billions"],
            "Trailing_PE": vm["trailing_pe"],
            "Forward_PE": vm["forward_pe"],
            "PEG_Ratio": vm["peg_ratio"],
            "Price_to_Sales": vm["price_to_sales"],
            "EV_to_EBITDA": vm["ev_to_ebitda"],
            "Beta": vm["beta"],
            "Last_Updated": timestamp_str
        }
        rows_companies.append(row)
        print(f"  -> {ticker:<6} | {meta['name'][:24]:<24} | Price: ${pm['price']:>8.2f} | 2Y: {pm['change_2y_pct']:>7.1f}% | P/E: {vm['trailing_pe']:>6}")

    df_companies = pd.DataFrame(rows_companies)

    # --------------------------------------------------------------------------
    # 2. Process Macroeconomic & Sovereign Debt Indicators
    # --------------------------------------------------------------------------
    print("\n[2/3] Extracting Macroeconomic, Yield & Sovereign Indicators...", flush=True)
    rows_macro = []
    for ticker, meta in MACRO_INDICATORS.items():
        df_t = None
        if batch_df is not None:
            try:
                if isinstance(batch_df.columns, pd.MultiIndex):
                    if ticker in batch_df.columns.levels[0]:
                        df_t = batch_df[ticker]
                    elif ticker in batch_df.columns.levels[1]:
                        df_t = batch_df.xs(ticker, axis=1, level=1)
            except Exception:
                df_t = None

        if df_t is None or df_t.empty:
            try:
                df_t = yf.download(ticker, period="2y", progress=False)
            except Exception:
                df_t = None

        pm = extract_price_metrics(df_t, ticker)
        row = {
            "Symbol": ticker,
            "Indicator": meta["name"],
            "Category": meta["category"],
            "Value": pm["price"],
            "Unit": meta["unit"],
            "Change_1D_Pct": pm["change_1d_pct"],
            "Change_1M_Pct": pm["change_1m_pct"],
            "Change_6M_Pct": pm["change_6m_pct"],
            "Change_1Y_Pct": pm["change_1y_pct"],
            "Change_2Y_Pct": pm["change_2y_pct"],
            "High_52W": pm["high_52w"],
            "Low_52W": pm["low_52w"],
            "Last_Updated": timestamp_str
        }
        rows_macro.append(row)
        print(f"  -> {ticker:<8} | {meta['name'][:32]:<32} | Value: {pm['price']:>9.2f} {meta['unit']} | 1Y: {pm['change_1y_pct']:>6.1f}%")

    # Add Sovereign Debt Benchmarks to Macro Data
    for key, val in US_FISCAL_BENCHMARKS.items():
        clean_name = key.replace("_", " ")
        rows_macro.append({
            "Symbol": "CALC",
            "Indicator": clean_name,
            "Category": "US Fiscal Baseline",
            "Value": val,
            "Unit": "USD_T / % / GW" if "Percent" in key or "GW" in key else "USD_B/T",
            "Change_1D_Pct": 0.0,
            "Change_1M_Pct": np.nan,
            "Change_6M_Pct": np.nan,
            "Change_1Y_Pct": np.nan,
            "Change_2Y_Pct": np.nan,
            "High_52W": val,
            "Low_52W": val,
            "Last_Updated": timestamp_str
        })

    df_macro = pd.DataFrame(rows_macro)

    # --------------------------------------------------------------------------
    # 3. Process Investment Flows & Credit Risk Spreads
    # --------------------------------------------------------------------------
    print("\n[3/3] Extracting Investment Flows, Infrastructure & Credit Spreads...", flush=True)
    rows_flows = []
    for ticker, meta in FLOW_INDICATORS.items():
        df_t = None
        if batch_df is not None:
            try:
                if isinstance(batch_df.columns, pd.MultiIndex):
                    if ticker in batch_df.columns.levels[0]:
                        df_t = batch_df[ticker]
                    elif ticker in batch_df.columns.levels[1]:
                        df_t = batch_df.xs(ticker, axis=1, level=1)
            except Exception:
                df_t = None

        if df_t is None or df_t.empty:
            try:
                df_t = yf.download(ticker, period="2y", progress=False)
            except Exception:
                df_t = None

        pm = extract_price_metrics(df_t, ticker)
        row = {
            "Symbol": ticker,
            "Instrument": meta["name"],
            "Category": meta["category"],
            "Segment_Proxy": meta["segment"],
            "Price_USD": pm["price"],
            "Change_1D_Pct": pm["change_1d_pct"],
            "Change_1M_Pct": pm["change_1m_pct"],
            "Change_6M_Pct": pm["change_6m_pct"],
            "Change_1Y_Pct": pm["change_1y_pct"],
            "Change_2Y_Pct": pm["change_2y_pct"],
            "High_52W": pm["high_52w"],
            "Low_52W": pm["low_52w"],
            "Pct_Below_52W_High": pm["pct_below_52w_high"],
            "Last_Updated": timestamp_str
        }
        rows_flows.append(row)
        print(f"  -> {ticker:<6} | {meta['segment'][:36]:<36} | Price: ${pm['price']:>7.2f} | 6M: {pm['change_6m_pct']:>6.1f}%")

    # Add Derived Credit Risk Stress Ratio: HYG / LQD
    hyg_price = next((r["Price_USD"] for r in rows_flows if r["Symbol"] == "HYG"), np.nan)
    lqd_price = next((r["Price_USD"] for r in rows_flows if r["Symbol"] == "LQD"), np.nan)
    if hyg_price and lqd_price and lqd_price > 0:
        ratio = round(hyg_price / lqd_price, 4)
        rows_flows.append({
            "Symbol": "HYG/LQD",
            "Instrument": "Credit Risk Appetite Ratio (HYG / LQD)",
            "Category": "Credit Spread Proxy",
            "Segment_Proxy": "Falling ratio signals high-yield distress & flight to quality",
            "Price_USD": ratio,
            "Change_1D_Pct": np.nan,
            "Change_1M_Pct": np.nan,
            "Change_6M_Pct": np.nan,
            "Change_1Y_Pct": np.nan,
            "Change_2Y_Pct": np.nan,
            "High_52W": np.nan,
            "Low_52W": np.nan,
            "Pct_Below_52W_High": np.nan,
            "Last_Updated": timestamp_str
        })
        print(f"  -> {'HYG/LQD':<6} | {'Credit Risk Appetite Ratio':<36} | Ratio: {ratio:>8.4f}")

    df_flows = pd.DataFrame(rows_flows)

    # --------------------------------------------------------------------------
    # 4. Generate Master Consolidated CSV
    # --------------------------------------------------------------------------
    master_rows = []
    for r in rows_companies:
        master_rows.append({
            "Asset_Class": "Equity",
            "Identifier": r["Ticker"],
            "Title": r["Name"],
            "Category": r["Category"],
            "Latest_Value": r["Price_USD"],
            "Unit": "USD",
            "Change_1D_Pct": r["Change_1D_Pct"],
            "Change_1M_Pct": r["Change_1M_Pct"],
            "Change_6M_Pct": r["Change_6M_Pct"],
            "Change_1Y_Pct": r["Change_1Y_Pct"],
            "Change_2Y_Pct": r["Change_2Y_Pct"],
            "Market_Cap_B": r["Market_Cap_USD_Billion"],
            "Valuation_PE": r["Trailing_PE"],
            "Last_Updated": timestamp_str
        })
    for r in rows_macro:
        master_rows.append({
            "Asset_Class": "Macro/Sovereign",
            "Identifier": r["Symbol"],
            "Title": r["Indicator"],
            "Category": r["Category"],
            "Latest_Value": r["Value"],
            "Unit": r["Unit"],
            "Change_1D_Pct": r["Change_1D_Pct"],
            "Change_1M_Pct": r["Change_1M_Pct"],
            "Change_6M_Pct": r["Change_6M_Pct"],
            "Change_1Y_Pct": r["Change_1Y_Pct"],
            "Change_2Y_Pct": r["Change_2Y_Pct"],
            "Market_Cap_B": np.nan,
            "Valuation_PE": np.nan,
            "Last_Updated": timestamp_str
        })
    for r in rows_flows:
        master_rows.append({
            "Asset_Class": "Flow/Credit",
            "Identifier": r["Symbol"],
            "Title": r["Instrument"],
            "Category": r["Category"],
            "Latest_Value": r["Price_USD"],
            "Unit": "USD / Ratio",
            "Change_1D_Pct": r["Change_1D_Pct"],
            "Change_1M_Pct": r["Change_1M_Pct"],
            "Change_6M_Pct": r["Change_6M_Pct"],
            "Change_1Y_Pct": r["Change_1Y_Pct"],
            "Change_2Y_Pct": r["Change_2Y_Pct"],
            "Market_Cap_B": np.nan,
            "Valuation_PE": np.nan,
            "Last_Updated": timestamp_str
        })

    df_master = pd.DataFrame(master_rows)

    # --------------------------------------------------------------------------
    # 5. Export CSV Files
    # --------------------------------------------------------------------------
    file_master = os.path.join(output_dir, "latest_market_metrics.csv")
    file_companies = os.path.join(output_dir, "companies_valuation_metrics.csv")
    file_macro = os.path.join(output_dir, "macro_financial_condition.csv")
    file_flows = os.path.join(output_dir, "investment_flows_credit.csv")

    df_master.to_csv(file_master, index=False, encoding="utf-8")
    df_companies.to_csv(file_companies, index=False, encoding="utf-8")
    df_macro.to_csv(file_macro, index=False, encoding="utf-8")
    df_flows.to_csv(file_flows, index=False, encoding="utf-8")

    if save_snapshot:
        snapshot_file = os.path.join(SNAPSHOTS_DIR, f"snapshot_{file_timestamp}.csv")
        df_master.to_csv(snapshot_file, index=False, encoding="utf-8")
        print(f"\n[+] Snapshot saved: {os.path.abspath(snapshot_file)}")

    print(f"\n[+] Exported Consolidated CSV: {os.path.abspath(file_master)} ({len(df_master)} records)")
    print(f"[+] Exported Equities Valuation CSV: {os.path.abspath(file_companies)} ({len(df_companies)} records)")
    print(f"[+] Exported Macro & Fiscal CSV: {os.path.abspath(file_macro)} ({len(df_macro)} records)")
    print(f"[+] Exported Flows & Credit CSV: {os.path.abspath(file_flows)} ({len(df_flows)} records)")

    # --------------------------------------------------------------------------
    # 6. Generate AI Agent Research & News Search Brief
    # --------------------------------------------------------------------------
    generate_agent_brief(df_companies, df_macro, df_flows, output_dir, timestamp_str)

    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 80)
    print(f"  PIPELINE EXECUTION COMPLETED IN {elapsed:.2f}s")
    print("=" * 80)


def generate_agent_brief(df_co, df_macro, df_flows, output_dir, timestamp_str):
    """
    Generates actionable research briefs (Markdown and JSON) for the AI Agent.
    Highlights numerical outliers and prescribes exact web search queries on reliable news sites.
    """
    brief_md_path = os.path.join(output_dir, "ai_agent_research_brief.md")
    brief_json_path = os.path.join(output_dir, "ai_agent_research_brief.json")

    # Find interesting outliers
    top_gainers_2y = df_co.sort_values(by="Change_2Y_Pct", ascending=False).head(3)
    worst_drawdown = df_co.sort_values(by="Pct_Below_52W_High", ascending=True).head(3)

    sp500_val = df_macro.loc[df_macro["Symbol"] == "^GSPC", "Value"].values
    sp500_str = f"{sp500_val[0]:.2f}" if len(sp500_val) > 0 and not np.isnan(sp500_val[0]) else "N/A"

    tnx_val = df_macro.loc[df_macro["Symbol"] == "^TNX", "Value"].values
    tnx_str = f"{tnx_val[0]:.2f}%" if len(tnx_val) > 0 and not np.isnan(tnx_val[0]) else "N/A"

    vix_val = df_macro.loc[df_macro["Symbol"] == "^VIX", "Value"].values
    vix_str = f"{vix_val[0]:.2f}" if len(vix_val) > 0 and not np.isnan(vix_val[0]) else "N/A"

    suggested_queries = [
        "site:ft.com OR site:bloomberg.com Microsoft data center cancellations power grid constraints",
        "site:reuters.com Anthropic valuation revenue growth deceleration pre-IPO",
        "site:wsj.com US 10-year Treasury yield federal deficit interest outlays",
        "site:sec.gov CoreWeave NVIDIA GPU-backed debt collateral filings",
        "site:bloomberg.com private credit data center ABS Blackstone Ares Apollo",
        "site:kbra.com data center ABS rating methodology class A tranches",
        "PJM interconnection queue delays data centers energy bottlenecks 2026",
    ]

    brief_data = {
        "pipeline_timestamp": timestamp_str,
        "key_benchmarks": {
            "SP500_Level": sp500_str,
            "US_10Y_Treasury_Yield": tnx_str,
            "CBOE_VIX": vix_str,
            "US_National_Debt_Trillion": US_FISCAL_BENCHMARKS["US_National_Debt_USD_Trillion"],
            "US_Net_Interest_Annual_Trillion": US_FISCAL_BENCHMARKS["US_Net_Interest_Annual_Pace_USD_Trillion"],
            "Hyperscaler_CapEx_Pace_Billion": US_FISCAL_BENCHMARKS["Hyperscaler_Annual_CapEx_RunRate_USD_Billion"],
        },
        "suggested_news_search_queries": suggested_queries,
        "trusted_domains": [
            "bloomberg.com",
            "ft.com (Financial Times)",
            "wsj.com (Wall Street Journal)",
            "reuters.com",
            "sec.gov (EDGAR 10-K/10-Q/8-K)",
            "kbra.com (Kroll Bond Rating Agency)",
            "eia.gov (US Energy Information Administration)",
            "federalreserve.gov",
            "nationalgrid.com / pjm.com"
        ]
    }

    # Save JSON brief
    with open(brief_json_path, "w", encoding="utf-8") as f:
        json.dump(brief_data, f, indent=2)

    # Save Markdown brief
    md_content = f"""# AI Agent Market Update Briefing & News Research Protocol
**Generated automatically by `fetch_market_pipeline.py` on {timestamp_str}**

---

## 1. Quantitative Snapshot (Latest Ingested Data)
- **S&P 500 Index**: `{sp500_str}`
- **US 10-Year Treasury Yield**: `{tnx_str}`
- **CBOE Volatility Index (VIX)**: `{vix_str}`
- **US Sovereign National Debt**: `${US_FISCAL_BENCHMARKS['US_National_Debt_USD_Trillion']} Trillion` (Net interest: `${US_FISCAL_BENCHMARKS['US_Net_Interest_Annual_Pace_USD_Trillion']}T/year`)
- **Annual Hyperscaler AI CapEx Pace**: `${US_FISCAL_BENCHMARKS['Hyperscaler_Annual_CapEx_RunRate_USD_Billion']} Billion`

---

## 2. Protocol for the AI Agent (Qualitative News Synthesis)

> 🤖 **INSTRUCTION FOR THE AI AGENT IN FUTURE REPORT UPDATES:**
> 1. Read the newly generated CSV files in `data/`:
>    - `data/latest_market_metrics.csv`
>    - `data/companies_valuation_metrics.csv`
>    - `data/macro_financial_condition.csv`
>    - `data/investment_flows_credit.csv`
> 2. Execute web searches on trusted institutional news sources using the targeted queries below to uncover the **causal drivers** behind the numbers.
> 3. Verify corporate announcements, SEC EDGAR filings, utility interconnection notices, and private credit developments.
> 4. Update the quantitative parameters (`FACTS`, `SCENARIOS`, `TRANCHES`) across report generator scripts.
> 5. Recompile reports and dossiers via `py scripts/build_all_reports.py`.

---

## 3. Targeted Web Search Queries for the Agent

| Priority Focus | Target Sources | Suggested Search Query |
|:---|:---|:---|
| **Data Center Grid Bottlenecks** | FT, Bloomberg, Utility Filings | `site:ft.com OR site:bloomberg.com Microsoft data center cancellations power grid constraints` |
| **AI Frontier Deceleration** | Reuters, The Information, WSJ | `site:reuters.com Anthropic valuation revenue growth deceleration pre-IPO` |
| **Sovereign Fiscal Stress** | WSJ, Bloomberg, TreasuryDirect | `site:wsj.com US 10-year Treasury yield federal deficit interest outlays` |
| **Hardware Debt & Neoclouds** | SEC EDGAR, Bloomberg | `site:sec.gov CoreWeave NVIDIA GPU-backed debt collateral filings` |
| **Private Credit & ABS** | Bloomberg, KBRA, Private Debt Investor | `site:bloomberg.com private credit data center ABS Blackstone Ares Apollo` |
| **Grid Backlog Timelines** | PJM, National Grid, FERC | `PJM interconnection queue delays data centers energy bottlenecks 2026` |

---

## 4. Trusted Domain Whitelist
- `bloomberg.com`
- `ft.com` (Financial Times)
- `wsj.com` (Wall Street Journal)
- `reuters.com`
- `sec.gov` (SEC EDGAR Filings)
- `kbra.com` (Kroll Bond Rating Agency)
- `eia.gov` (US Energy Information Administration)
- `federalreserve.gov`
"""
    with open(brief_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[+] Generated AI Agent Briefing (Markdown): {os.path.abspath(brief_md_path)}")
    print(f"[+] Generated AI Agent Briefing (JSON): {os.path.abspath(brief_json_path)}")


def main():
    parser = argparse.ArgumentParser(description="AI Market Crash Risk — Quantitative Data Pipeline")
    parser.add_argument("--output-dir", default=DEFAULT_DATA_DIR, help="Target directory for output CSVs")
    parser.add_argument("--quick", action="store_true", help="Quick mode (skips individual valuation multiple queries)")
    parser.add_argument("--no-snapshots", action="store_true", help="Do not save timestamped snapshot")
    args = parser.parse_args()

    run_pipeline(output_dir=args.output_dir, quick_mode=args.quick, save_snapshot=not args.no_snapshots)


if __name__ == "__main__":
    main()
