"""Configuración por fuente y legislatura: grupos, partidos y textos de la web.

Cada entrada genera un dataset independiente (site/data/<clave>.json) y una opción en los selectores
de la web. Los partidos cambian entre legislaturas, así que nunca se mezclan datasets.

Para añadir una legislatura: descarga sus datos (descargar_legislatura.py), añade aquí su entrada,
clasifica sus iniciativas en data/clasificacion/<clave>/ y regenera.
"""

FUENTES = {
    "congreso": "Congreso de los Diputados",
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
}
