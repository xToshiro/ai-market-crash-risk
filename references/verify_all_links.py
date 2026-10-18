#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
references/verify_all_links.py
------------------------------
Independent script to re-test all repository links anytime and regenerate
the connectivity report 'references/url_connectivity_report.md'.
"""

import os
import sys
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

try:
    from build_references_system import scan_repository_urls, test_url, CURATED_SOURCES, generate_markdown_docs
    print("[*] Successfully imported repository reference definitions.")
    
    # Run audit
    scanned = scan_repository_urls()
    all_urls = {}
    for item in CURATED_SOURCES:
        u = item["url"]
        all_urls[u] = {
            "curated": item,
            "files_cited": scanned.get(u, ["Project Documentation / Core Reference"])
        }
    for u, files in scanned.items():
        if u not in all_urls:
            all_urls[u] = {
                "curated": {
                    "category": "Discovered Project URL",
                    "name": u.split('//')[-1].split('/')[0],
                    "url": u,
                    "description": "URL referenced in repository code/docs.",
                    "reports_used": ["Repository Codebase"],
                    "api_endpoint": False
                },
                "files_cited": files
            }
            
    print(f"[*] Testing {len(all_urls)} URLs...")
    results = {}
    for idx, (url, info) in enumerate(all_urls.items(), 1):
        res = test_url(url)
        results[url] = res
        print(f"  [{idx:02d}/{len(all_urls):02d}] {res['status']:<22} | HTTP {str(res['code']):<4} | {url[:55]}")
        time.sleep(0.04)

    generate_markdown_docs(all_urls, results)
    print("[+] Live audit report refreshed successfully in 'references/url_connectivity_report.md'!")

except Exception as e:
    print(f"[-] Error executing verify_all_links: {e}")
    sys.exit(1)
