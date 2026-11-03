import json, re, sys

d = json.load(open(sys.argv[1]))
out = sys.argv[2]
cl = lambda s: re.sub(r"\s+", " ", s or "").strip()

items = []
for x in d["proyectos"] + d["proposiciones"]:
    items.append({
        "id": x["NUMEXPEDIENTE"][:10],
        "tipo_ini": x["TIPO"],
        "titulo": cl(x["OBJETO"]),
        "autor": cl(x.get("AUTOR")),
        "fecha": x.get("FECHAPRESENTACION",""),
        "resultado": cl(x.get("RESULTADOTRAMITACION")),
        "situacion": cl(x.get("SITUACIONACTUAL")),
    })

seen = set()
for v in d["votaciones"]:
    if v["exp"].startswith("130") and v["exp"] not in seen:
        t = cl(v["txt"])
        if t.lower().startswith("tramitación"):
            continue
        seen.add(v["exp"])
        items.append({
            "id": v["exp"],
            "tipo_ini": "Real Decreto-ley",
            "titulo": t,
            "autor": "Gobierno",
            "fecha": v["d"],
            "resultado": "",
            "situacion": "",
        })

json.dump(items, open(out, "w"), ensure_ascii=False, indent=0)
print(len(items))
