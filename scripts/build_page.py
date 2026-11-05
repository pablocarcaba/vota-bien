"""site/template.html -> site/index.html, con el catálogo de datasets disponibles y el ámbito territorial de
los partidos (data/ambito_partidos.json) incrustados. Cada entrada del catálogo lleva la versión de la rúbrica con la que
está clasificada (y su fecha) y, si la legislatura tuvo dos Gobiernos, sus fechas de inicio.

Los datasets (site/data/<clave>.json) los genera build_data.py y la página los carga con fetch
según la fuente y legislatura elegidas. El primero del catálogo (la legislatura más reciente) es el
que se abre por defecto.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import FUENTES, LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CLAS = os.path.join(ROOT, "data", "clasificacion")


def fecha_rubrica_vigente():
    """Versión y fecha de la cabecera de RUBRICA.md («Versión 3 (fecha 04/11/2026)»)."""
    try:
        txt = open(os.path.join(CLAS, "RUBRICA.md"), encoding="utf-8").read(2000)
    except OSError:
        return None, None
    m = re.search(r"Versión (\d+) \((?:fecha )?(\d{2}/\d{2}/\d{4})\)", txt)
    return ("v" + m.group(1), m.group(2)) if m else (None, None)


# la v2 ya no está en la cabecera de RUBRICA.md: su fecha sale del historial (git log de RUBRICA.md, «Versión 2 (03/11/2026)»)
FECHAS_RUBRICA = {"v2": "03/11/2026"}
v_act, f_act = fecha_rubrica_vigente()
if v_act:
    FECHAS_RUBRICA[v_act] = f_act


def rubrica(clave):
    """v3 si la legislatura se ha reclasificado por tres lecturas (data/clasificacion/<clave>/lectura_v3), si no v2."""
    v = "v3" if os.path.isdir(os.path.join(CLAS, clave, "lectura_v3")) else "v2"
    return {"version": v, "fecha": FECHAS_RUBRICA.get(v)}


catalogo = []
for k, c in LEGISLATURAS.items():
    if not os.path.exists(os.path.join(ROOT, "site", "data", k + ".json")):
        continue
    e = {"clave": k, "fuente": c["fuente"], "fuente_txt": FUENTES[c["fuente"]], "leg": c["leg"], "titulo": c["titulo"],
         "rubrica": rubrica(k)}
    if c.get("gobiernos"):
        e["gobiernos"] = c["gobiernos"]
    catalogo.append(e)
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
