"""Rebuild data/europe.geojson from Natural Earth 1:50m (only needed if you want to change the extent
or the simplification – the committed file is ready to use).

Steps: download NE admin-0 countries + breakaway/disputed areas -> move Crimea from Russia to Ukraine,
merge Northern Cyprus into Cyprus -> clip to the map extent -> simplify with mapshaper.

Requires: pip install shapely ; npm install -g mapshaper (or npx mapshaper)
Run:      python src/build_geo.py
"""
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from shapely.geometry import box, mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
NE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
FILES = ['ne_50m_admin_0_countries.geojson', 'ne_50m_admin_0_breakaway_disputed_areas.geojson']
for name in FILES:
    if not (RAW / name).exists():
        print('downloading', name)
        urllib.request.urlretrieve(NE + name, RAW / name)

src = json.loads((RAW / FILES[0]).read_text(encoding='utf-8'))
disp = json.loads((RAW / FILES[1]).read_text(encoding='utf-8'))
crimea = next(shape(f['geometry']) for f in disp['features'] if f['properties'].get('NAME') == 'Crimea')

BBOX = box(-26, 25, 88, 72)   # lon/lat extent kept in the file (Svalbard, Greenland, far-east Russia dropped)
feats = {}
for f in src['features']:
    p = f['properties']
    iso = p.get('ISO_A2_EH') or p.get('ISO_A2')
    admin = p['ADMIN']
    if admin == 'Kosovo':
        iso = 'XK'
    if admin == 'Northern Cyprus':
        iso = 'CY'
    if admin == 'Greenland':
        continue
    g = shape(f['geometry'])
    if admin == 'Russia':
        g = g.difference(crimea.buffer(0.001))
    if admin == 'Ukraine':
        g = unary_union([g, crimea])
    if not g.intersects(BBOX):
        continue
    g = g.intersection(BBOX)
    if g.is_empty:
        continue
    feats[iso] = {'geom': unary_union([feats[iso]['geom'], g]) if iso in feats else g}

raw_out = RAW / 'europe_raw.geojson'
raw_out.write_text(json.dumps({'type': 'FeatureCollection', 'features': [
    {'type': 'Feature', 'properties': {'iso': iso}, 'geometry': mapping(v['geom'].buffer(0))}
    for iso, v in feats.items()]}), encoding='utf-8')
print(len(feats), 'features ->', raw_out)

mapshaper = shutil.which('mapshaper')
cmd = [mapshaper] if mapshaper else ['npx', '--yes', 'mapshaper']
out = ROOT / 'data' / 'europe.geojson'
subprocess.run(cmd + [str(raw_out), '-simplify', '30%', 'keep-shapes', '-o', 'precision=0.001',
                      'format=geojson', str(out)], check=True)
print('wrote', out, '- now run build_page.py (it precomputes mainland bounds when missing)')
