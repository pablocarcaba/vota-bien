"""Configuración por fuente y legislatura: grupos, partidos y textos de la web.

Cada entrada genera un dataset independiente (site/data/<clave>.json) y una opción en los selectores
de la web. Los partidos cambian entre legislaturas, así que nunca se mezclan datasets.

Para añadir una legislatura: descarga sus datos (descargar_legislatura.py), añade aquí su entrada,
clasifica sus iniciativas en data/clasificacion/<clave>/ y regenera.
"""

FUENTES = {
    "congreso": "Congreso de los Diputados",
    "europarlamento": "Parlamento Europeo",
}

LEGISLATURAS = {
    "congreso_xv": {
        "fuente": "congreso",
        "leg": "XV",
        "titulo": "XV legislatura · 2023–2026",
        "periodo": "entre el 17 de agosto de 2023 y la disolución de las Cortes el 6 de octubre de 2026",
        "gobierno": "coalición PSOE–Sumar",
        # grupo parlamentario (código en las votaciones) -> partido
        "grupos": {"GS": "PSOE", "GP": "PP", "GVOX": "VOX", "GSUMAR": "Sumar", "GR": "ERC",
                   "GJxCAT": "Junts", "GEH Bildu": "Bildu", "GV (EAJ-PNV)": "PNV"},
        # partidos dentro de grupos mixtos: inicio del apellido del diputado -> partido
        "nominal": {"Belarra": "Podemos", "Sánchez Serna": "Podemos", "Velarde": "Podemos", "Santana": "Podemos",
                    "Rego": "BNG", "Valido": "CC", "Catalán": "UPN", "Micó": "Compromís"},
        "nominal_txt": "Podemos, BNG, Coalición Canaria, UPN y Compromís, integrados en el Grupo Mixto",
        # autor tal como aparece en la ficha de la iniciativa -> partido
        "autores": {"Grupo Parlamentario Socialista": "PSOE", "Grupo Parlamentario Popular en el Congreso": "PP",
                    "Grupo Parlamentario VOX": "VOX", "Grupo Parlamentario Plurinacional SUMAR": "Sumar",
                    "Grupo Parlamentario Republicano": "ERC", "Grupo Parlamentario Junts per Catalunya": "Junts",
                    "Grupo Parlamentario Euskal Herria Bildu": "Bildu", "Grupo Parlamentario Vasco (EAJ-PNV)": "PNV",
                    "Grupo Parlamentario Mixto": "Mixto"},
        # etiqueta de grupo entre paréntesis en el autor -> partido
        "etiquetas": {"GR": "ERC", "GEH Bildu": "Bildu", "GV (EAJ-PNV)": "PNV", "GSUMAR": "Sumar", "GMx": "Mixto",
                      "GS": "PSOE", "GP": "PP", "GVOX": "VOX", "GJxCAT": "Junts"},
        "partidos": ["PSOE", "PP", "VOX", "Sumar", "ERC", "Junts", "Bildu", "PNV", "Podemos", "BNG", "CC", "UPN",
                     "Compromís"],
        "autores_web": ["Gobierno", "PSOE", "PP", "VOX", "Sumar", "ERC", "Junts", "Bildu", "PNV", "Podemos", "BNG",
                        "Mixto"],
        "votos_extra": "congreso_xv_votos_extra.json",
    },
    "congreso_xiv": {
        "fuente": "congreso",
        "leg": "XIV",
        "titulo": "XIV legislatura · 2019–2023",
        "periodo": "entre el 3 de diciembre de 2019 y la disolución de las Cortes el 30 de mayo de 2023",
        "gobierno": "coalición PSOE–Unidas Podemos",
        "grupos": {"GS": "PSOE", "GP": "PP", "GVOX": "VOX", "GCUP-EC-GC": "Unidas Podemos", "GR": "ERC",
                   "GCs": "Cs", "GEH Bildu": "Bildu", "GV (EAJ-PNV)": "PNV"},
        # Grupo Plural y Grupo Mixto. Sin partido (no se cuentan): Cambronero (ex-Cs) y Pita (ex-Podemos).
        # Sayas y García Adanero figuran como UPN toda la legislatura, aunque dejaron el partido en 2022.
        "nominal": {"Nogueras": "Junts", "Borràs": "Junts", "Alonso-Cuevillas": "Junts", "Illamola": "Junts",
                    "Pagès": "Junts", "Calvo Gómez": "Junts",
                    "Bel Accensi": "PDeCAT", "Cañadell": "PDeCAT", "Miquel i Valentí": "PDeCAT", "Boadella": "PDeCAT",
                    "Errejón": "Más País", "Sabanés": "Más País", "Baldoví": "Compromís", "Picó": "Compromís",
                    "Rego": "BNG", "Vehí": "CUP", "Botran": "CUP", "Sayas": "UPN", "García Adanero": "UPN",
                    "Oramas": "CC", "Quevedo": "NC", "Fernández Pérez, María": "NC", "Martínez Oblanca": "Foro",
                    "Mazón": "PRC", "Guitarte": "Teruel Existe"},
        "nominal_txt": "Junts, PDeCAT, Más País, Compromís y BNG (Grupo Plural) y CUP, UPN, Coalición Canaria, "
                       "Nueva Canarias, PRC, Foro y Teruel Existe (Grupo Mixto)",
        "autores": {"Grupo Parlamentario Socialista": "PSOE", "Grupo Parlamentario Popular en el Congreso": "PP",
                    "Grupo Parlamentario VOX": "VOX",
                    "Grupo Parlamentario Confederal de Unidas Podemos": "Unidas Podemos",
                    "Grupo Parlamentario Republicano": "ERC", "Grupo Parlamentario Ciudadanos": "Cs",
                    "Grupo Parlamentario Euskal Herria Bildu": "Bildu", "Grupo Parlamentario Vasco (EAJ-PNV)": "PNV",
                    "Grupo Parlamentario Plural": "Plural", "Grupo Parlamentario Mixto": "Mixto"},
        "etiquetas": {"GR": "ERC", "GEH Bildu": "Bildu", "GV (EAJ-PNV)": "PNV", "GCUP-EC-GC": "Unidas Podemos",
                      "GCs": "Cs", "GPlu": "Plural", "GMx": "Mixto", "GS": "PSOE", "GP": "PP", "GVOX": "VOX"},
        "partidos": ["PSOE", "PP", "VOX", "Unidas Podemos", "ERC", "Cs", "Junts", "Bildu", "PNV", "PDeCAT",
                     "Más País", "Compromís", "BNG", "CUP", "UPN", "CC", "NC", "PRC", "Foro", "Teruel Existe"],
        "autores_web": ["Gobierno", "PSOE", "PP", "VOX", "Unidas Podemos", "ERC", "Cs", "Junts", "Bildu", "PNV",
                        "PDeCAT", "Más País", "Compromís", "BNG", "CUP", "UPN", "CC", "NC", "PRC", "Foro",
                        "Teruel Existe", "Plural", "Mixto"],
    },
    "congreso_xiii": {
        "fuente": "congreso",
        "leg": "XIII",
        "titulo": "XIII legislatura · 2019",
        "periodo": "entre el 21 de mayo de 2019 y la disolución de las Cortes el 24 de septiembre de 2019 (legislatura sin investidura)",
        "gobierno": "PSOE, en funciones",
        "grupos": {"GS": "PSOE", "GP": "PP", "GCs": "Cs", "GCUP-EC-GC": "Unidas Podemos", "GVOX": "VOX", "GR": "ERC",
                   "GV (EAJ-PNV)": "PNV"},
        # Grupo Mixto. Junqueras, Turull, Rull y Sánchez estaban suspendidos (no votan).
        "nominal": {"Nogueras": "JxCat", "Turull": "JxCat", "Sánchez Picanyol": "JxCat", "Rull": "JxCat", "Borràs": "JxCat",
                    "Alonso-Cuevillas": "JxCat", "Miquel i Valentí": "JxCat", "Junqueras": "ERC",
                    "Ruiz de Pinedo": "Bildu", "Aizpurua": "Bildu", "Matute": "Bildu", "Iñarritu": "Bildu",
                    "Oramas": "CC", "González Taño": "CC", "Sayas": "NA+", "García Adanero": "NA+",
                    "Baldoví": "Compromís", "Mazón": "PRC"},
        "nominal_txt": "JxCat, EH Bildu, Coalición Canaria, Navarra Suma, Compromís y PRC, integrados en el Grupo Mixto",
        "autores": {"Grupo Parlamentario Socialista": "PSOE", "Grupo Parlamentario Popular": "PP",
                    "Grupo Parlamentario VOX": "VOX", "Grupo Parlamentario Confederal de Unidas Podemos": "Unidas Podemos",
                    "Grupo Parlamentario Republicano": "ERC", "Grupo Parlamentario Ciudadanos": "Cs",
                    "Grupo Parlamentario Vasco (EAJ-PNV)": "PNV", "Grupo Parlamentario Mixto": "Mixto"},
        "etiquetas": {"GR": "ERC", "GV (EAJ-PNV)": "PNV", "GCUP-EC-GC": "Unidas Podemos", "GCs": "Cs", "GMx": "Mixto",
                      "GS": "PSOE", "GP": "PP", "GVOX": "VOX"},
        "partidos": ["PSOE", "PP", "Cs", "Unidas Podemos", "VOX", "ERC", "JxCat", "PNV", "Bildu", "CC", "NA+",
                     "Compromís", "PRC"],
        "autores_web": ["Gobierno", "PSOE", "PP", "Cs", "Unidas Podemos", "VOX", "ERC", "PNV", "Bildu", "JxCat", "CC",
                        "NA+", "Compromís", "PRC", "Mixto"],
    },
    "europarlamento_10": {
        "fuente": "europarlamento",
        "formato": "europarlamento",  # procedimientos + votaciones clave por partido nacional (descargar_europarlamento.py)
        "leg": "10.ª",
        "titulo": "10.ª legislatura · 2024–2029",
        "periodo": "desde el 16 de julio de 2024 (legislatura en curso)",
        "gobierno": "Comisión von der Leyen II",
        # en el Parlamento Europeo el voto ya viene agrupado por partido nacional español
        "grupos": {p: p for p in ['PP', 'PSOE', 'VOX', 'SALF', 'Sumar', 'Podemos', 'ERC', 'Bildu', 'PNV', 'BNG', 'Compromís', 'Comuns']},
        "nominal": {},
        "nominal_txt": "",
        "autores": {"Comisión Europea": "Comisión Europea", "Parlamento Europeo": "Parlamento Europeo"},
        "etiquetas": {},
        "partidos": ['PP', 'PSOE', 'VOX', 'SALF', 'Sumar', 'Podemos', 'ERC', 'Bildu', 'PNV', 'BNG', 'Compromís', 'Comuns'],
        "autores_web": ["Comisión Europea", "Parlamento Europeo"],
    },
}
