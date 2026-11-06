"""Une, lector a lector, la ronda 1 (primeros 60.000 caracteres) y los bloques de la ronda 2 (segunda parte del texto),
con la misma regla que data/clasificacion/lectura_omnibus/combinar.py. Escribe final/ para consolidar_medidas.py."""
import json, os
SP = os.path.dirname(os.path.abspath(__file__))
lote = json.load(open(f"{SP}/lotes/lote_0.json"))
def union(med):
    u = {}
    for m in med:
        for k, v in m["imp"].items(): u.setdefault(k, set()).add(v)
    return {k: next(iter(s)) for k, s in sorted(u.items()) if len(s) == 1}
os.makedirs(f"{SP}/final/lotes", exist_ok=True)
json.dump([{"clave": e["clave"], "id": e["id"]} for e in lote], open(f"{SP}/final/lotes/final.json", "w"), ensure_ascii=False)
for L in "CDE":
    r1 = json.load(open(f"{SP}/salida/{L}/lote_0.json"))
    r2 = {x["id"]: x.get("bloques", []) for x in json.load(open(f"{SP}/r2/salida/{L}/lote_0.json"))}
    fin = []
    for lec in r1:
        lec = json.loads(json.dumps(lec))
        extra = r2.get(lec["id"], [])
        if extra:
            med = lec.get("medidas") or ([{"d": "Medida principal", "imp": lec["imp"], "peso": lec["peso"]}] if lec.get("imp") else [])
            nuevos = [b for b in extra if not any(set(b["imp"].items()) <= set(m["imp"].items()) for m in med)]
            med = med + nuevos
            if len(med) >= 2:
                lec["medidas"] = med; lec["imp"] = union(med); lec["peso"] = max(m["peso"] for m in med)
            elif med:
                lec["imp"] = med[0]["imp"]; lec["peso"] = med[0]["peso"]
        fin.append(lec)
    os.makedirs(f"{SP}/final/salida/{L}", exist_ok=True)
    json.dump(fin, open(f"{SP}/final/salida/{L}/final.json", "w"), ensure_ascii=False, indent=1)
    print(L, [(x["id"], len(x.get("medidas", []))) for x in fin])
