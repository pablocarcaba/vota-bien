"""site/template.html -> site/index.html, con el catálogo de datasets disponibles y el ámbito territorial de
los partidos (data/ambito_partidos.json) incrustados.

Los datasets (site/data/<clave>.json) los genera build_data.py y la página los carga con fetch
según la fuente y legislatura elegidas. El primero del catálogo (la legislatura más reciente) es el
que se abre por defecto.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import FUENTES, LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
catalogo = [
    {"clave": k, "fuente": c["fuente"], "fuente_txt": FUENTES[c["fuente"]], "leg": c["leg"], "titulo": c["titulo"]}
    for k, c in LEGISLATURAS.items()
    if os.path.exists(os.path.join(ROOT, "site", "data", k + ".json"))
]
if not catalogo:
    sys.exit("No hay datasets en site/data/: ejecuta antes build_data.py")
tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
out = os.path.join(ROOT, "site", "index.html")
# dónde se puede votar a cada partido en las generales (filtro por provincia del ranking)
ambitos = json.load(open(os.path.join(ROOT, "data", "ambito_partidos.json"), encoding="utf-8"))
ambitos = {k: ambitos[k] for k in ("criterio", "comunidades", "provincias", "partidos", "notas")}
html = tpl.replace("__CATALOGO__", json.dumps(catalogo, ensure_ascii=False).replace("</", "<\\/"))
html = html.replace("__AMBITOS__", json.dumps(ambitos, ensure_ascii=False).replace("</", "<\\/"))
open(out, "w", encoding="utf-8").write(html)
print("Generado", out, "con", [c["clave"] for c in catalogo])
