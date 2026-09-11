"""Build the single-file map page from the template + data files.

Outputs
  docs/index.html   – complete standalone HTML document (GitHub Pages / any static host)
  dist/artifact.html – the same page without <html>/<head>/<body> wrapper, for republishing
                       as a Claude artifact (the artifact host adds its own skeleton)

Run from anywhere:  python src/build_page.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pisa_data import DATA, EU27  # noqa: E402

try:
    from shapely.geometry import shape
except ImportError:  # shapely is only needed to derive mainland bbox/anchor per country
    shape = None

SRC, DATA_DIR, DOCS, DIST = ROOT / 'src', ROOT / 'data', ROOT / 'docs', ROOT / 'dist'
LEAFLET_JS = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js'

geo = json.loads((DATA_DIR / 'europe.geojson').read_text(encoding='utf-8'))
flags = json.loads((DATA_DIR / 'flags.json').read_text(encoding='utf-8'))
leaflet_css = (DATA_DIR / 'leaflet.css').read_text(encoding='utf-8')
leaflet_css = re.sub(r'\s*/\*.*?\*/', '', leaflet_css, flags=re.S)  # strip comments (image refs are unused)

# Per-country mainland bbox + anchor point (largest polygon) so that e.g. the Canary Islands
# or Svalbard do not drag the "zoom to country" view out to sea.
for f in geo['features']:
    iso = f['properties']['iso']
    if iso not in DATA:
        f['properties'] = {'iso': iso}
        continue
    if 'bb' in f['properties'] and 'c' in f['properties']:
        continue  # already precomputed in data/europe.geojson
    if shape is None:
        raise SystemExit('shapely is required to compute mainland bounds: pip install shapely')
    g = shape(f['geometry'])
    polys = list(g.geoms) if g.geom_type == 'MultiPolygon' else [g]
    main = max(polys, key=lambda p: p.area)
    pt = main.representative_point()
    minx, miny, maxx, maxy = main.bounds
    f['properties'] = {
        'iso': iso,
        'c': [round(pt.y, 3), round(pt.x, 3)],
        'bb': [[round(miny, 2), round(minx, 2)], [round(maxy, 2), round(maxx, 2)]],
    }

# Short-term change 2022->2025 straight from OECD Table I.1 (Volume I executive summary), not computed
# from 2022 means: the OECD figures use unrounded means and the same territorial coverage (e.g. Ukrainian
# regions), and are withheld ('m') where the comparison is not valid (Albania limited reporting, LU/AM first
# cycle, AZ Baku-only in 2022).
oecd = json.loads((DATA_DIR / 'oecd_table_i1.json').read_text(encoding='utf-8'))
data = {}
for iso, (en, hu, de, s25, s22, note) in DATA.items():
    assert tuple(s25) == tuple(oecd[iso]['s']), f'{iso}: pisa_data.py and oecd_table_i1.json disagree'
    d = oecd[iso]['d']
    if iso == 'AL' and d is None:
        note = '*nochange'
    data[iso] = {'n': [en, hu, de], 's': list(s25), 'd': list(d) if d else None, 'note': note}

tpl = (SRC / 'template.html').read_text(encoding='utf-8')
page = (tpl
        .replace('__LEAFLET_CSS__', leaflet_css)
        .replace('__GEOJSON__', json.dumps(geo, separators=(',', ':')))
        .replace('__FLAGS__', json.dumps(flags, separators=(',', ':')))
        .replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        .replace('__EU27__', json.dumps(EU27, separators=(',', ':')))
        .replace('__BLOCS__', json.dumps(json.loads((DATA_DIR / 'blocs.json').read_text(encoding='utf-8')), ensure_ascii=False, separators=(',', ':')))
        .replace('__REGIONS__', (DATA_DIR / 'regions.json').read_text(encoding='utf-8').strip()))
assert '__' not in page.split('<div id="app">')[0][-200:], 'unfilled placeholder'

DIST.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)
(DIST / 'artifact.html').write_text(page, encoding='utf-8')

head, body = page.split('<div id="app">', 1)
standalone = (
    '<!doctype html>\n<html lang="hu">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="description" content="PISA 2025 – interaktív térkép: az európai országok összesített '
    'eredménye az EU-27 átlagához képest (OECD, 2026. szeptember 8.).">\n'
    + head + '</head>\n<body>\n<div id="app">' + body + '\n</body>\n</html>\n'
)
(DOCS / 'index.html').write_text(standalone, encoding='utf-8')

if '--local' in sys.argv:  # offline preview with a local Leaflet copy (node_modules/leaflet/dist/leaflet.js)
    local = standalone.replace(LEAFLET_JS, str(ROOT / 'node_modules/leaflet/dist/leaflet.js'))
    (DIST / 'local_preview.html').write_text(local, encoding='utf-8')

print(f'docs/index.html   {len(standalone.encode()):,} bytes')
print(f'dist/artifact.html {len(page.encode()):,} bytes')
