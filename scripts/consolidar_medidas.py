"""Consolida por mayoría las tres lecturas independientes (C, D, E) de la ronda de leyes ómnibus y las aplica.

Uso: python3 scripts/consolidar_medidas.py <dir_lotes> <dir_salida_ronda> [--aplicar]

<dir_lotes> tiene los lotes (entradas con `clave` e `id`); <dir_salida_ronda> tiene C/, D/ y E/ con un fichero por
lote. Regla (determinista y auditable, extensión de scripts/consolidar_lecturas.py):
  - la ley es ómnibus si al menos 2 de las 3 lecturas le ponen `medidas`;
  - un colectivo con un signo cuenta si lo marcan al menos 2 lecturas (en cualquiera de sus medidas, o en el `imp`
    de la ley si esa lectura no la divide);
  - ómnibus: se toman las medidas de la lectura (de las que la dividen) que más se parece al resultado y en cada
    medida se dejan solo los colectivos con mayoría; una medida que queda vacía se quita. Si quedan menos de 2, la ley
    no se divide. `imp` de la ley = unión de las medidas sin signos opuestos; `peso` = el de la medida más pesada;
  - no ómnibus: `imp` = los colectivos con mayoría; `peso` = la mediana;
  - `tipo`, el de la mayoría; `nota`, la de la lectura más parecida al resultado.
Escribe <dir_salida_ronda>/consolidada.json y CAMBIOS.md (diferencias con la vigente). Con --aplicar lo lleva a
data/clasificacion/<clave>/clas_*.json y copia la clasificación a las iniciativas del mismo grupo de temas.json
(rúbrica 3.9: el proyecto de ley que procede de un real decreto-ley lleva sus mismas medidas). No hace peticiones de red.
"""
import glob, json, os, statistics, sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LECTORES = ("C", "D", "E")


def pares(lec):
    if lec.get("medidas"):
        return {(k, v) for m in lec["medidas"] for k, v in m["imp"].items()}
    return set(lec.get("imp", {}).items())


def union(medidas):
    u = {}
    for m in medidas:
        for k, v in m["imp"].items():
            u.setdefault(k, set()).add(v)
    return {k: next(iter(s)) for k, s in sorted(u.items()) if len(s) == 1}


def parecido(lec, obj):
    p = pares(lec)
    return len(p & obj) / len(p | obj) if p | obj else 1.0


def consolidar(lecturas):
    votos = Counter(p for l in lecturas for p in pares(l))
    may = {p for p, n in votos.items() if n >= 2}
    tipo = Counter(l.get("tipo") for l in lecturas).most_common(1)[0][0]
    divididas = [l for l in lecturas if l.get("medidas")]
    if len(divididas) >= 2:
        base = max(divididas, key=lambda l: parecido(l, may))
        med = []
        for m in base["medidas"]:
            imp = {k: v for k, v in m["imp"].items() if (k, v) in may}
            if imp:
                med.append({"d": m["d"], "imp": imp, "peso": m["peso"]})
        if len(med) >= 2:
            return {"tipo": tipo, "imp": union(med), "peso": max(m["peso"] for m in med), "nota": base.get("nota", ""),
                    "medidas": med}
    imp = {}
    for k, v in sorted(may):
        if (k, -v) not in may:
            imp[k] = v
    mejor = max(lecturas, key=lambda l: parecido(l, may))
    return {"tipo": tipo, "imp": imp, "peso": int(statistics.median([l.get("peso") or 1 for l in lecturas])),
            "nota": mejor.get("nota", "")}


def fmt(c):
    s = ", ".join(f"{k} {'+' if v > 0 else '−'}" for k, v in sorted((c.get("imp") or {}).items())) or "sin impactos"
    return s + f" · peso {c.get('peso')}" + (f" · {len(c['medidas'])} medidas" if c.get("medidas") else "")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    dl, ds, aplicar = sys.argv[1], sys.argv[2], "--aplicar" in sys.argv
    res = []
    for lf in sorted(glob.glob(os.path.join(dl, "*.json"))):
        lote = json.load(open(lf, encoding="utf-8"))
        lecs = [json.load(open(os.path.join(ds, L, os.path.basename(lf)), encoding="utf-8")) for L in LECTORES]
        for j, e in enumerate(lote):
            ls = [l[j] for l in lecs]
            assert all(x["id"] == e["id"] for x in ls), (lf, e["id"])
            res.append({"clave": e["clave"], "id": e["id"], **consolidar(ls),
                        "omnibus_votos": sum(1 for x in ls if x.get("medidas"))})
    json.dump(res, open(os.path.join(ds, "consolidada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lineas = ["# Ronda de leyes ómnibus: consolidación por mayoría (2 de 3)\n"]
    cambios = 0
    for clave in sorted({r["clave"] for r in res}):
        d = os.path.join(ROOT, "data", "clasificacion", clave)
        files = {p: json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(d, "clas_*.json")))}
        idx = {x["id"]: x for arr in files.values() for x in arr}
        grupos = json.load(open(os.path.join(d, "temas.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "temas.json")) else []
        gde = {i: g["ids"] for g in grupos for i in g["ids"]}
        nuevos = {r["id"]: r for r in res if r["clave"] == clave}
        for i, r in list(nuevos.items()):  # mismo contenido: la que se dividió manda; si no, el real decreto-ley
            for j in gde.get(i, []):
                o = nuevos.get(j)
                if j != i and (o is None or (r.get("medidas") and not o.get("medidas"))
                               or (bool(r.get("medidas")) == bool(o.get("medidas")) and i.startswith("130/") and not j.startswith("130/") and not o.get("_de"))):
                    nuevos[j] = {**r, "id": j, "_de": i}
        lineas.append(f"\n## {clave}\n")
        for i, r in sorted(nuevos.items()):
            x = idx[i]
            antes = fmt(x)
            if aplicar:
                x["tipo"], x["imp"], x["peso"], x["nota"] = r["tipo"], r["imp"], r["peso"], r["nota"]
                if r.get("medidas"):
                    x["medidas"] = r["medidas"]
                else:
                    x.pop("medidas", None)
            despues = fmt(r)
            if antes != despues:
                cambios += 1
                de = f" (copiada de {r['_de']})" if r.get("_de") else f" (ómnibus para {r.get('omnibus_votos', 0)} de 3)"
                lineas.append(f"- {i}{de}: {antes} → {despues}")
        if aplicar:
            for p, arr in files.items():
                orig = open(p, encoding="utf-8").read()
                ind = len(orig.split("\n")[1]) - len(orig.split("\n")[1].lstrip())
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(arr, ensure_ascii=False, indent=ind) + ("\n" if orig.endswith("\n") else ""))
    open(os.path.join(ds, "CAMBIOS.md"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"{len(res)} leyes consolidadas; {sum(1 for r in res if r.get('medidas'))} ómnibus; "
          f"{cambios} diferencias con la vigente{' (aplicadas)' if aplicar else ''}")


if __name__ == "__main__":
    main()
