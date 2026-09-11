"""Bloc averages (PISA 2025) and long-run trends. Composite = mean of maths, reading, science."""
import json, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from history import H, OECD_AVG
from pisa_data import EU27

# ---- 2025 world table (OECD Table I.1: name|sci|read|math|cps|dsci|dread|dmath) ----
W = {}
for line in open('' + str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'data' / 'oecd_table_i1_world.txt') + '', encoding='utf-8'):
    p = line.strip().split('|')
    if len(p) < 8:
        continue
    name = p[0]
    def num(x):
        return None if x in ('m', '') else int(x)
    s, r, m = num(p[1]), num(p[2]), num(p[3])
    W[name] = dict(s=s, r=r, m=m, d=(num(p[7]), num(p[6]), num(p[5])))   # d = (Δm, Δr, Δs)

def comp(e):
    if e['m'] is None or e['r'] is None or e['s'] is None:
        return None
    return (e['m'] + e['r'] + e['s']) / 3

NAME = {  # iso -> OECD table name (only the ones we need)
 'AT':'Austria','BE':'Belgium','BG':'Bulgaria','HR':'Croatia','CY':'Cyprus','CZ':'Czechia','DK':'Denmark','EE':'Estonia',
 'FI':'Finland','FR':'France','DE':'Germany','GR':'Greece','HU':'Hungary','IE':'Ireland','IT':'Italy','LV':'Latvia','LT':'Lithuania',
 'LU':'Luxembourg','MT':'Malta','NL':'Netherlands*','PL':'Poland','PT':'Portugal','RO':'Romania','SK':'Slovak Republic','SI':'Slovenia',
 'ES':'Spain','SE':'Sweden','GB':'United Kingdom','CH':'Switzerland','NO':'Norway*','IS':'Iceland','RS':'Serbia','AL':'Albania*',
 'MK':'North Macedonia','ME':'Montenegro','MD':'Moldova','XK':'Kosovo','UA':'Ukrainian regions (17 of 27)','TR':'Türkiye','GE':'Georgia',
 'AM':'Armenia','AZ':'Azerbaijan','KZ':'Kazakhstan',
 'SG':'Singapore','JP':'Japan','KR':'Korea','HK':'Hong Kong (China)','MO':'Macao (China)','TW':'Chinese Taipei','CN':'B-S-J-Z (China)',
 'US':'United States*','CA':'Canada*','AU':'Australia','NZ':'New Zealand*',
}
EUROPE43 = list(NAME)[:43]
BLOCS = {
 'EU-27': EU27,
 'Europe (43 participants)': EUROPE43,
 'East Asia (SG, JP, KR, TW, HK, MO)': ['SG','JP','KR','TW','HK','MO'],
 'B-S-J-Z (China, 4 provinces)': ['CN'],
 'United States': ['US'],
 'Anglosphere ex-EU (GB, US, CA, AU, NZ)': ['GB','US','CA','AU','NZ'],
}
BY_NAME = {
 'Latin America': ['Chile','Uruguay','Costa Rica','Mexico','Brazil','Colombia','Peru','Argentina','Paraguay','Dominican Republic','El Salvador','Guatemala','Ecuador'],
 'Middle East & Gulf': ['Israel','United Arab Emirates','Qatar','Saudi Arabia','Jordan','Lebanon','Palestinian Authority','Kurdistan Region (Iraq)'],
 'Southeast Asia': ['Viet Nam','Malaysia','Thailand','Indonesia','Philippines','Cambodia','Brunei Darussalam'],
 'Central Asia & Mongolia': ['Kazakhstan','Kyrgyzstan','Mongolia','Dushanbe (Tajikistan)'],
 'Africa': ['Morocco','Kenya','Zambia','Rwanda','Mauritius'],
}

def bloc_avg(names):
    vals = [W[n] for n in names if n in W and comp(W[n]) is not None]
    n = len(vals)
    m = sum(v['m'] for v in vals)/n; r = sum(v['r'] for v in vals)/n; s = sum(v['s'] for v in vals)/n
    dv = [v['d'] for v in vals if None not in v['d']]
    dd = [sum(x[i] for x in dv)/len(dv) for i in range(3)] if dv else None
    return dict(n=n, m=m, r=r, s=s, c=(m+r+s)/3, dcomp=(sum(dd)/3 if dd else None), ntrend=len(dv))

out = {}
print(f"{'bloc':44s} {'n':>3s} {'math':>6s} {'read':>6s} {'sci':>6s} {'comp':>6s} {'Δ22→25':>7s}")
for name, isos in BLOCS.items():
    b = bloc_avg([NAME[i] for i in isos]); out[name] = b
    print(f"{name:44s} {b['n']:3d} {b['m']:6.1f} {b['r']:6.1f} {b['s']:6.1f} {b['c']:6.1f} {b['dcomp']:+7.1f}" if b['dcomp'] is not None else f"{name:44s} {b['n']:3d} {b['m']:6.1f} {b['r']:6.1f} {b['s']:6.1f} {b['c']:6.1f}     n/a")
for name, names in BY_NAME.items():
    b = bloc_avg(names); out[name] = b
    print(f"{name:44s} {b['n']:3d} {b['m']:6.1f} {b['r']:6.1f} {b['s']:6.1f} {b['c']:6.1f} {b['dcomp']:+7.1f}")
o = W['OECD average']; print(f"{'OECD average (official)':44s} {'':3s} {o['m']:6.1f} {o['r']:6.1f} {o['s']:6.1f} {comp(o):6.1f} {sum(o['d'])/3:+7.1f}")

# ---- long-run trend 2012 -> 2025 on a constant country set per bloc ----
print('\nTrend (constant set, composite):  2012   2015   2018   2022   2025')
def trend(isos, label):
    ok = [i for i in isos if i in H and all(H[i][d][k] is not None for d in 'msr' for k in range(4)) and comp(W[NAME[i]]) is not None]
    vals = []
    for k in (3, 2, 1, 0):  # 2012, 2015, 2018, 2022
        vals.append(sum((H[i]['m'][k] + H[i]['s'][k] + H[i]['r'][k]) / 3 for i in ok) / len(ok))
    vals.append(sum(comp(W[NAME[i]]) for i in ok) / len(ok))
    print(f"{label:34s} n={len(ok):2d}  " + '  '.join(f'{v:5.1f}' for v in vals) + f"   Δ12→25 {vals[-1]-vals[0]:+5.1f}")
    return dict(n=len(ok), isos=ok, years=[2012, 2015, 2018, 2022, 2025], values=[round(v, 1) for v in vals])
tr = {}
tr['EU'] = trend(EU27, 'EU (constant 24, no CY/LU/MT/ES*)')
tr['EA'] = trend(['SG','JP','KR','TW','HK','MO'], 'East Asia 6')
tr['US'] = trend(['US'], 'United States')
tr['ANG'] = trend(['GB','US','CA','AU','NZ'], 'Anglosphere 5')
oa = [(OECD_AVG['m'][k]+OECD_AVG['s'][k]+OECD_AVG['r'][k])/3 for k in (3,2,1,0)] + [comp(o)]
print(f"{'OECD average':34s}       " + '  '.join(f'{v:5.1f}' for v in oa) + f"   Δ12→25 {oa[-1]-oa[0]:+5.1f}")
tr['OECD'] = dict(years=[2012,2015,2018,2022,2025], values=[round(v,1) for v in oa])
print('EU trend set:', tr['EU']['isos'])

# Spain 2018 reading missing -> ES drops out of the constant set; also compute EU trend with ES using 2018 = avg of 2015/2022? no: keep honest constant set.
json.dump({'blocs2025': out, 'trend': tr, 'world': W}, open('' + str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'data' / 'blocs_raw.json') + '', 'w'), indent=1)

# gap dynamics
print('\nGap East Asia 6 minus EU (constant sets):', [round(a-b,1) for a,b in zip(tr['EA']['values'], tr['EU']['values'])])
print('Gap US minus EU:', [round(a-b,1) for a,b in zip(tr['US']['values'], tr['EU']['values'])])
