"""All PISA 2025 participants outside the European set (src/pisa_data.py covers the 43 European ones).

iso: ISO 3166-1 alpha-2 of the polygon to colour; for entities without a national polygon the key is a
pseudo-code and `pt` gives the marker position (lat, lon). Scores are read from data/oecd_table_i1_world.txt
by build_page.py (this file only carries identity: OECD table name, names in EN/HU/DE, marker, notes).
'*' = OECD sampling-standards caveat (as printed in Table I.1). 'sub' = sub-national entity, not the country.
"""
WORLD = {
 # iso : (OECD name, EN, HU, DE, note, pt)
 'CN4': ('B-S-J-Z (China)', 'B‑S‑J‑Z (China)', 'B‑S‑J‑Z (Kína)', 'B‑S‑J‑Z (China)', 'sub', (33.5, 119.5)),
 'SG': ('Singapore', 'Singapore', 'Szingapúr', 'Singapur', '', (1.35, 103.8)),
 'MO': ('Macao (China)', 'Macao (China)', 'Makaó (Kína)', 'Macau (China)', '', (22.2, 113.55)),
 'TW': ('Chinese Taipei', 'Chinese Taipei', 'Tajvan', 'Chinesisch‑Taipeh', '', None),
 'JP': ('Japan', 'Japan', 'Japán', 'Japan', '', None),
 'KR': ('Korea', 'Korea', 'Dél‑Korea', 'Südkorea', '', None),
 'CA': ('Canada*', 'Canada', 'Kanada', 'Kanada', '*', None),
 'NZ': ('New Zealand*', 'New Zealand', 'Új‑Zéland', 'Neuseeland', '*', None),
 'AU': ('Australia', 'Australia', 'Ausztrália', 'Australien', '', None),
 'US': ('United States*', 'United States', 'Egyesült Államok', 'USA', '*', None),
 'HK': ('Hong Kong (China)', 'Hong Kong (China)', 'Hongkong (Kína)', 'Hongkong (China)', '', (22.35, 114.15)),
 'AE': ('United Arab Emirates', 'United Arab Emirates', 'Egyesült Arab Emírségek', 'Vereinigte Arabische Emirate', '', None),
 'VN': ('Viet Nam', 'Viet Nam', 'Vietnám', 'Vietnam', 'nochange', None),
 'UY': ('Uruguay', 'Uruguay', 'Uruguay', 'Uruguay', '', None),
 'CL': ('Chile', 'Chile', 'Chile', 'Chile', '', None),
 'IL': ('Israel', 'Israel', 'Izrael', 'Israel', '', None),
 'BN': ('Brunei Darussalam', 'Brunei', 'Brunei', 'Brunei', '', None),
 'MU': ('Mauritius', 'Mauritius', 'Mauritius', 'Mauritius', 'no2022', (-20.3, 57.55)),
 'QA': ('Qatar', 'Qatar', 'Katar', 'Katar', '', None),
 'TH': ('Thailand', 'Thailand', 'Thaiföld', 'Thailand', '', None),
 'MN': ('Mongolia', 'Mongolia', 'Mongólia', 'Mongolei', '', None),
 'CR': ('Costa Rica', 'Costa Rica', 'Costa Rica', 'Costa Rica', '', None),
 'MY': ('Malaysia', 'Malaysia', 'Malajzia', 'Malaysia', '', None),
 'CO': ('Colombia', 'Colombia', 'Kolumbia', 'Kolumbien', '', None),
 'MX': ('Mexico', 'Mexico', 'Mexikó', 'Mexiko', '', None),
 'SA': ('Saudi Arabia', 'Saudi Arabia', 'Szaúd‑Arábia', 'Saudi‑Arabien', '', None),
 'BR': ('Brazil', 'Brazil', 'Brazília', 'Brasilien', '', None),
 'JO': ('Jordan', 'Jordan', 'Jordánia', 'Jordanien', '', None),
 'PE': ('Peru', 'Peru', 'Peru', 'Peru', '', None),
 'EC': ('Ecuador', 'Ecuador', 'Ecuador', 'Ecuador', 'no2022', None),
 'AR': ('Argentina', 'Argentina', 'Argentína', 'Argentinien', '', None),
 'ID': ('Indonesia', 'Indonesia', 'Indonézia', 'Indonesien', '', None),
 'SV': ('El Salvador', 'El Salvador', 'Salvador', 'El Salvador', '', None),
 'KH': ('Cambodia', 'Cambodia', 'Kambodzsa', 'Kambodscha', '', None),
 'PH': ('Philippines', 'Philippines', 'Fülöp‑szigetek', 'Philippinen', '', None),
 'LB': ('Lebanon', 'Lebanon', 'Libanon', 'Libanon', 'no2022', None),
 'KG': ('Kyrgyzstan', 'Kyrgyzstan', 'Kirgizisztán', 'Kirgisistan', 'no2022', None),
 'DO': ('Dominican Republic', 'Dominican Republic', 'Dominikai Köztársaság', 'Dominikanische Republik', '', None),
 'PS': ('Palestinian Authority', 'Palestinian Authority', 'Palesztin Hatóság', 'Palästinensische Autonomiebehörde', '', None),
 'MA': ('Morocco', 'Morocco', 'Marokkó', 'Marokko', '', None),
 'PY': ('Paraguay', 'Paraguay', 'Paraguay', 'Paraguay', '', None),
 'IQK': ('Kurdistan Region (Iraq)', 'Kurdistan Region (Iraq)', 'Kurdisztán régió (Irak)', 'Region Kurdistan (Irak)', 'sub', (36.2, 44.0)),
 'GT': ('Guatemala', 'Guatemala', 'Guatemala', 'Guatemala', '', None),
 'ZM': ('Zambia', 'Zambia', 'Zambia', 'Sambia', 'no2022', None),
 'KE': ('Kenya', 'Kenya', 'Kenya', 'Kenia', 'no2022', None),
 'TJD': ('Dushanbe (Tajikistan)', 'Dushanbe (Tajikistan)', 'Dusanbe (Tádzsikisztán)', 'Duschanbe (Tadschikistan)', 'sub', (38.56, 68.79)),
 'RW': ('Rwanda', 'Rwanda', 'Ruanda', 'Ruanda', 'no2022', None),
 # Uzbekistan reported a science mean only (no reading/mathematics) - no composite, so it stays unmapped.
}
