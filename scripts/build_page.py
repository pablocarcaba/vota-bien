"""site/template.html -> site/index.html, con el catálogo de datasets disponibles incrustado.

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
open(out, "w", encoding="utf-8").write(tpl.replace("__CATALOGO__", json.dumps(catalogo, ensure_ascii=False).replace("</", "<\\/")))
print("Generado", out, "con", [c["clave"] for c in catalogo])
