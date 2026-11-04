"""data/fuente/<clave>.json -> data/generado/<clave>/items.json (iniciativas normalizadas).

Uso: python3 scripts/build_items.py congreso_xv
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
clave = sys.argv[1] if len(sys.argv) > 1 else "congreso_xv"
d = json.load(open(os.path.join(ROOT, "data", "fuente", clave + ".json"), encoding="utf-8"))
out = os.path.join(ROOT, "data", "generado", clave, "items.json")
cl = lambda s: re.sub(r"\s+", " ", s or "").strip()

items = []
# Parlamento Europeo: procedimientos legislativos (descargar_europarlamento.py)
for x in d.get("procedimientos", []):
    if not x.get("legislativo"):
        continue
    items.append({"id": x["exp"], "tipo_ini": x["tipo_txt"], "titulo": cl(x["tit"]),
                  "autor": "Parlamento Europeo" if x["tipo"] == "INL" else "Comisión Europea",
                  "fecha": x["d"], "resultado": x.get("res", ""), "situacion": ""})
for x in d.get("proyectos", []) + d.get("proposiciones", []) + d.get("rdl", []):
    items.append({
        "id": x["NUMEXPEDIENTE"][:10],
        "tipo_ini": "Real Decreto-ley" if x["NUMEXPEDIENTE"].startswith("130") else x["TIPO"],
        "titulo": cl(x["OBJETO"]),
        "autor": cl(x.get("AUTOR")),
        "fecha": x.get("FECHAPRESENTACION", ""),
        "resultado": cl(x.get("RESULTADOTRAMITACION")),
        "situacion": cl(x.get("SITUACIONACTUAL")),
    })

# En la XV los reales decretos-ley no venían en el fichero de iniciativas: se toman de sus votaciones
seen = {it["id"] for it in items}
for v in d.get("votaciones", []) if "procedimientos" not in d else []:
    if v["exp"].startswith("130") and v["exp"] not in seen:
        t = cl(v["txt"])
        if t.lower().startswith("tramitación"):
            continue
        seen.add(v["exp"])
        items.append({"id": v["exp"], "tipo_ini": "Real Decreto-ley", "titulo": t, "autor": "Gobierno",
                      "fecha": v["d"], "resultado": "", "situacion": ""})

os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(items, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(clave, len(items), "iniciativas")
