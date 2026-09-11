"""Build data/world.geojson from Natural Earth 1:50m admin-0 countries.

Europe (the map's home extent) is kept at higher detail than the rest of the world: the part of every
country inside the Europe box is simplified at 30 %, the part outside at 10 %, and the two parts are
unioned back into one feature per country. Crimea is moved from Russia to Ukraine and Northern Cyprus
is merged into Cyprus. Antarctica is dropped.

Requires: pip install shapely ; npm install -g mapshaper (or npx mapshaper)
Run:      python src/build_geo.py
"""
import json
import shutil
import subprocess
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

EUROPE = box(-26, 25, 88, 72)
feats = {}
for f in src['features']:
    p = f['properties']
    iso = p.get('ISO_A2_EH') or p.get('ISO_A2')
    admin = p['ADMIN']
    if admin == 'Kosovo':
        iso = 'XK'
    if admin == 'Northern Cyprus':
        iso = 'CY'
    if admin == 'Antarctica' or iso in (None, '-99'):
        continue
    g = shape(f['geometry'])
    if admin == 'Russia':
        g = g.difference(crimea.buffer(0.001))
    if admin == 'Ukraine':
        g = unary_union([g, crimea])
    feats[iso] = unary_union([feats[iso], g]) if iso in feats else g

def write_fc(path, parts):
    path.write_text(json.dumps({'type': 'FeatureCollection', 'features': [
        {'type': 'Feature', 'properties': {'iso': iso}, 'geometry': mapping(g)} for iso, g in parts if not g.is_empty]}),
        encoding='utf-8')

inside = [(iso, g.intersection(EUROPE)) for iso, g in feats.items()]
outside = [(iso, g.difference(EUROPE)) for iso, g in feats.items()]
write_fc(RAW / 'part_europe.geojson', inside)
write_fc(RAW / 'part_world.geojson', outside)

mapshaper = shutil.which('mapshaper')
cmd = [mapshaper] if mapshaper else ['npx', '--yes', 'mapshaper']
subprocess.run(cmd + [str(RAW / 'part_europe.geojson'), '-simplify', '30%', 'keep-shapes', '-o', 'precision=0.001',
                      'format=geojson', str(RAW / 'part_europe_s.geojson')], check=True)
subprocess.run(cmd + [str(RAW / 'part_world.geojson'), '-simplify', '10%', 'keep-shapes', '-filter-islands', 'min-vertices=8',
                      '-o', 'precision=0.001', 'format=geojson', str(RAW / 'part_world_s.geojson')], check=True)

merged = {}
for name in ('part_europe_s.geojson', 'part_world_s.geojson'):
    for f in json.loads((RAW / name).read_text(encoding='utf-8'))['features']:
        iso = f['properties']['iso']
        if not f.get('geometry'):
            continue  # mapshaper can null out micro-states; they stay as the other part only
        g = shape(f['geometry']).buffer(0)
        merged[iso] = unary_union([merged[iso], g]) if iso in merged else g

out = ROOT / 'data' / 'world.geojson'
write_fc(out, sorted(merged.items()))
print(len(merged), 'features ->', out, f'{out.stat().st_size / 1024:.0f} KB')
print('now run: python src/build_page.py  (it precomputes mainland bounds for countries with data)')
