"""Combina, lector a lector, las rondas de leyes ómnibus en una lectura final por ley:
base = r4 (relectura) > r3 (preámbulo completo hasta 70.000) > r2 (20.000); más los bloques de r5 (segunda parte
del preámbulo). Escribe final/lotes/final.json y final/salida/{C,D,E}/final.json para consolidar_medidas.py."""
import glob, json, os
SP = os.path.dirname(os.path.abspath(__file__))
def leer(r):
    out = {}
    for lf in glob.glob(f"{SP}/{r}/lotes/*.json"):
        lote = json.load(open(lf))
        for L in "CDE":
            p = f"{SP}/{r}/salida/{L}/{os.path.basename(lf)}"
            if not os.path.exists(p): continue
            for e, s in zip(lote, json.load(open(p))):
                out[(L, e["clave"], e["id"])] = s
    return out
R2, R3, R4, R5 = leer("r2"), leer("r3"), leer("r4"), leer("r5")
leyes = [(x["clave"], x["id"]) for f in sorted(glob.glob(f"{SP}/r2/lotes/*.json")) for x in json.load(open(f))]
def union(med):
    u = {}
    for m in med:
        for k, v in m["imp"].items(): u.setdefault(k, set()).add(v)
    return {k: next(iter(s)) for k, s in sorted(u.items()) if len(s) == 1}
fin = {L: [] for L in "CDE"}; fuente = {}
for clave, i in leyes:
    for L in "CDE":
        key = (L, clave, i)
        base = R4.get(key) or R3.get(key) or R2[key]
        fuente[(clave, i)] = "r4" if key in R4 else "r3" if key in R3 else "r2"
        lec = json.loads(json.dumps(base))
        extra = (R5.get(key) or {}).get("bloques", [])
        if extra:
            med = lec.get("medidas") or ([{"d": "Medida principal", "imp": lec["imp"], "peso": lec["peso"]}] if lec.get("imp") else [])
            # sin duplicar: un bloque cuyos colectivos y signos ya cubre una medida de la primera parte no se suma
            nuevos = [b for b in extra if not any(set(b["imp"].items()) <= set(m["imp"].items()) for m in med)]
            med = med + nuevos
            if len(med) >= 2:
                lec["medidas"] = med; lec["imp"] = union(med); lec["peso"] = max(m["peso"] for m in med)
            elif med:
                lec["imp"] = med[0]["imp"]; lec["peso"] = med[0]["peso"]
        fin[L].append(lec)
os.makedirs(f"{SP}/final/lotes", exist_ok=True)
json.dump([{"clave": c, "id": i} for c, i in leyes], open(f"{SP}/final/lotes/final.json", "w"), ensure_ascii=False)
for L in "CDE":
    os.makedirs(f"{SP}/final/salida/{L}", exist_ok=True)
    json.dump(fin[L], open(f"{SP}/final/salida/{L}/final.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(leyes), "leyes;", Counter(fuente.values()), "; con segunda parte:", len({(c, i) for (_, c, i) in R5}))
