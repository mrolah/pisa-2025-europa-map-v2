"""PISA 2025 mean scores for the 43 European / wider-European participants shown on the map.

Source: OECD, PISA 2025 Results (Volume I), Table I.1 (published 8 Sep 2026) - the same figures are kept
machine-readably in data/oecd_table_i1.json together with the OECD's official 2022->2025 change, which is
what the page displays as the trend. build_page.py asserts that the two files agree.

Tuple order for scores: (mathematics, reading, science). The PISA 2022 tuple is kept for reference only.
note: '*' = OECD flags that one or more sampling standards were not met; 'partial' = territorial coverage
note (Ukraine, 17 of 27 regions); 'no2022' = did not take part in 2022; 'baku2022' = only Baku in 2022.

Run `python src/pisa_data.py` to print the composite ranking and EU-27 averages.
"""

OECD_AVG_2025 = dict(math=463, read=461, sci=482)
OECD_AVG_2022 = dict(math=472, read=476, sci=485)

EU27 = ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE"]

# iso2: (name_en, name_hu, name_de, 2025 (m,r,s), 2022 (m,r,s) or None, note)
DATA = {
    "AT": ("Austria", "Ausztria", "Österreich", (477,467,497), (487,480,491), ""),
    "BE": ("Belgium", "Belgium", "Belgien", (480,466,490), (489,479,491), ""),
    "BG": ("Bulgaria", "Bulgária", "Bulgarien", (405,387,421), (417,404,421), ""),
    "HR": ("Croatia", "Horvátország", "Kroatien", (455,453,476), (463,475,483), ""),
    "CY": ("Cyprus", "Ciprus", "Zypern", (412,379,411), (418,381,411), ""),
    "CZ": ("Czechia", "Csehország", "Tschechien", (477,468,490), (487,489,498), ""),
    "DK": ("Denmark", "Dánia", "Dänemark", (471,460,478), (489,489,494), ""),
    "EE": ("Estonia", "Észtország", "Estland", (508,499,527), (510,511,526), ""),
    "FI": ("Finland", "Finnország", "Finnland", (469,474,504), (484,490,511), ""),
    "FR": ("France", "Franciaország", "Frankreich", (458,456,483), (474,474,487), ""),
    "DE": ("Germany", "Németország", "Deutschland", (464,465,486), (475,480,492), ""),
    "GR": ("Greece", "Görögország", "Griechenland", (424,423,434), (430,438,441), ""),
    "HU": ("Hungary", "Magyarország", "Ungarn", (459,452,480), (473,473,486), ""),
    "IE": ("Ireland", "Írország", "Irland", (480,500,500), (492,516,504), ""),
    "IT": ("Italy", "Olaszország", "Italien", (468,474,483), (471,482,477), ""),
    "LV": ("Latvia", "Lettország", "Lettland", (460,430,468), (483,475,494), ""),
    "LT": ("Lithuania", "Litvánia", "Litauen", (470,464,488), (475,472,484), ""),
    "LU": ("Luxembourg", "Luxemburg", "Luxemburg", (458,443,474), None, "no2022"),
    "MT": ("Malta", "Málta", "Malta", (439,415,453), (466,445,466), ""),
    "NL": ("Netherlands", "Hollandia", "Niederlande", (483,441,485), (493,459,488), "*"),
    "PL": ("Poland", "Lengyelország", "Polen", (484,482,495), (489,489,499), ""),
    "PT": ("Portugal", "Portugália", "Portugal", (460,462,482), (472,477,484), ""),
    "RO": ("Romania", "Románia", "Rumänien", (419,413,425), (428,428,428), ""),
    "SK": ("Slovakia", "Szlovákia", "Slowakei", (469,448,475), (464,447,462), ""),
    "SI": ("Slovenia", "Szlovénia", "Slowenien", (460,445,484), (485,469,500), ""),
    "ES": ("Spain", "Spanyolország", "Spanien", (457,451,477), (473,474,485), ""),
    "SE": ("Sweden", "Svédország", "Schweden", (464,466,485), (482,487,494), ""),
    # non-EU Europe
    "GB": ("United Kingdom", "Egyesült Királyság", "Vereinigtes Königreich", (488,494,511), (489,494,500), ""),
    "CH": ("Switzerland", "Svájc", "Schweiz", (499,470,501), (508,483,503), ""),
    "NO": ("Norway", "Norvégia", "Norwegen", (452,453,470), (468,477,478), "*"),
    "IS": ("Iceland", "Izland", "Island", (450,422,441), (459,436,447), ""),
    "RS": ("Serbia", "Szerbia", "Serbien", (417,415,429), (440,440,447), ""),
    "AL": ("Albania", "Albánia", "Albanien", (433,408,435), (368,358,376), "*"),
    "MK": ("North Macedonia", "Észak-Macedónia", "Nordmazedonien", (380,357,378), (389,359,380), ""),
    "ME": ("Montenegro", "Montenegró", "Montenegro", (411,418,435), (406,405,403), ""),
    "MD": ("Moldova", "Moldova", "Moldau", (410,404,422), (414,411,417), ""),
    "XK": ("Kosovo", "Koszovó", "Kosovo", (350,340,357), (355,342,357), ""),
    "UA": ("Ukraine", "Ukrajna", "Ukraine", (431,418,448), (441,428,450), "partial"),
    "TR": ("Türkiye", "Törökország", "Türkei", (462,472,494), (453,456,476), ""),
    "GE": ("Georgia", "Grúzia", "Georgien", (416,384,422), (390,374,384), ""),
    "AM": ("Armenia", "Örményország", "Armenien", (376,348,369), None, "no2022"),
    "AZ": ("Azerbaijan", "Azerbajdzsán", "Aserbaidschan", (422,374,409), None, "baku2022"),
    "KZ": ("Kazakhstan", "Kazahsztán", "Kasachstan", (414,385,420), (425,386,423), ""),
}

def composite(t):
    return sum(t)/3.0

if __name__ == "__main__":
    eu = {k: v for k, v in DATA.items() if k in EU27}
    assert len(eu) == 27, len(eu)
    eu_avg = {
        "math": sum(v[3][0] for v in eu.values())/27,
        "read": sum(v[3][1] for v in eu.values())/27,
        "sci":  sum(v[3][2] for v in eu.values())/27,
    }
    eu_avg["comp"] = (eu_avg["math"]+eu_avg["read"]+eu_avg["sci"])/3
    print("EU-27 unweighted averages 2025:", {k: round(v,1) for k,v in eu_avg.items()})
    rows = sorted(((composite(v[3]), k, v[0]) for k, v in DATA.items()), reverse=True)
    print("\nAll (composite, dev from EU avg):")
    for c, k, n in rows:
        flag = "EU" if k in EU27 else "  "
        print(f"{flag} {k} {n:22s} {c:6.1f} {c-eu_avg['comp']:+6.1f}")
    eu_rows = [r for r in rows if r[1] in EU27]
    print("\nTop3 EU:", eu_rows[:3])
    print("Bottom3 EU:", eu_rows[-3:])
    # 2022 EU avg for the countries with 2022 data (26, without LU)
    eu22 = [v[4] for k, v in eu.items() if v[4]]
    print("\nEU 2022 avg (26 countries):", [round(sum(x[i] for x in eu22)/len(eu22),1) for i in range(3)])
