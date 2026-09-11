"""Rebuild data/flags.json (flag images as data URIs) from the flag-icons npm package.

Small SVGs are embedded as-is; the large, detailed ones (Serbia, Spain, Montenegro, ...) are rasterised
to 96x72 PNG so the page stays small. Only needed if you add countries – the committed file is ready.

Requires: npm install flag-icons ; pip install playwright && playwright install chromium
Run:      python src/make_flags.py
"""
import base64
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
FL = ROOT / 'node_modules' / 'flag-icons' / 'flags' / '4x3'
ISOS = ('AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE '
        'GB CH NO IS RS AL MK ME MD XK UA TR GE AM AZ KZ EU').split()

out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 96, 'height': 72})
    for iso in ISOS:
        path = FL / (iso.lower() + '.svg')
        svg = path.read_text(encoding='utf-8')
        if path.stat().st_size <= 3200:
            s = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
            s = s.replace('"', "'").replace('#', '%23').replace('<', '%3C').replace('>', '%3E')
            out[iso] = 'data:image/svg+xml;utf8,' + s
        else:
            b64 = base64.b64encode(svg.encode()).decode()
            page.set_content(f'<body style="margin:0"><img src="data:image/svg+xml;base64,{b64}" '
                             f'style="width:96px;height:72px;display:block"></body>')
            png = page.screenshot(clip={'x': 0, 'y': 0, 'width': 96, 'height': 72}, omit_background=True)
            out[iso] = 'data:image/png;base64,' + base64.b64encode(png).decode()
    browser.close()

(ROOT / 'data' / 'flags.json').write_text(json.dumps(out), encoding='utf-8')
print(len(out), 'flags,', sum(len(v) for v in out.values()), 'bytes')
