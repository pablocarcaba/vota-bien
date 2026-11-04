"""Consolida por mayoría varias lecturas independientes de la clasificación de una legislatura.

Uso: python3 scripts/consolidar_lecturas.py <clave> <dir_lector_1> <dir_lector_2> <dir_lector_3> <dir_salida>

Regla (determinista y auditable):
  - un colectivo se marca con un signo si al menos 2 de las 3 lecturas lo marcan con ese signo;
  - el tipo (eco/soc) es el de la mayoría; el peso, la mediana;
  - la nota es la de la lectura cuyos impactos más se parecen al resultado consolidado;
  - `partido` se conserva de la clasificación vigente; si está vacía y 2 lecturas coinciden, se usa ese.
Escribe en <dir_salida> los mismos ficheros clas_N.json que la vigente (mismo reparto de ids), un
informe CAMBIOS.md con lo que cambia respecto a la vigente y lecturas.json con las tres lecturas
por iniciativa, para que cada cambio se pueda rastrear. No toca data/clasificacion/<clave>/clas_*.json.
"""
import glob, json, os, statistics, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comparar_lecturas import cargar, pares

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def consolidar(lecturas, vigente):
    votos = Counter(p for l in lecturas for p in pares(l))
    imp = {k: s for (k, s), n in sorted(votos.items()) if n >= 2}
    # un colectivo no puede quedar con los dos signos (2+2 es imposible con 3 lecturas, pero por si acaso)
    tipo = Counter(l.get("tipo") for l in lecturas).most_common(1)[0][0]
    peso = int(statistics.median([l.get("peso") or 1 for l in lecturas]))
    obj = set(imp.items())
    mejor = max(lecturas, key=lambda l: (len(pares(l) & obj) / len(pares(l) | obj)) if (pares(l) | obj) else 1.0)
    partido = vigente.get("partido", "") or next((p for p, n in Counter(l.get("partido", "") for l in lecturas if l.get("partido")).items() if n >= 2), "")
    return {"id": vigente["id"], "tipo": tipo, "imp": imp, "peso": peso, "nota": mejor.get("nota", ""), "partido": partido}


def fmt(imp):
    return ", ".join(f"{k} {'+' if v > 0 else '−'}" for k, v in sorted(imp.items())) or "sin impactos"


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    clave, d1, d2, d3, out = sys.argv[1:]
    base = os.path.join(ROOT, "data", "clasificacion", clave)
    L = [cargar(os.path.join(d, "*.json")) for d in (d1, d2, d3)]
    os.makedirs(out, exist_ok=True)
    cambios, todas, falta = [], {}, []
    for f in sorted(glob.glob(os.path.join(base, "clas_*.json"))):
        vig = json.load(open(f, encoding="utf-8"))
        nuevo = []
        for v in vig:
            i = v["id"]
            if not all(i in l for l in L):
                falta.append(i)
                nuevo.append(v)
                continue
            c = consolidar([l[i] for l in L], v)
            nuevo.append(c)
            todas[i] = {"vigente": v, "lecturas": [l[i] for l in L], "consolidada": c}
            dif = [x for x in ("tipo", "peso") if c[x] != v.get(x)]
            if pares(c) != pares(v) or dif:
                cambios.append((i, v, c, dif))
        json.dump(nuevo, open(os.path.join(out, os.path.basename(f)), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(todas, open(os.path.join(out, "lecturas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(out, "CAMBIOS.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Consolidación por mayoría de {clave}\n\nGenerado por `scripts/consolidar_lecturas.py`: un colectivo se "
                 "marca si lo marcan al menos 2 de 3 lecturas independientes; tipo por mayoría; peso, la mediana.\n\n"
                 f"{len(todas)} iniciativas consolidadas; {len(cambios)} cambian respecto a la clasificación anterior"
                 f"{f'; {len(falta)} sin las tres lecturas (se mantienen)' if falta else ''}.\n")
        for i, v, c, dif in cambios:
            fh.write(f"\n- **{i}** · antes: {fmt(v.get('imp') or {})} · peso {v.get('peso')} → ahora: {fmt(c['imp'])} · peso {c['peso']}"
                     f"{' · cambia ' + ', '.join(dif) if dif else ''}\n")
    print(f"{len(todas)} consolidadas, {len(cambios)} cambian, {len(falta)} sin las tres lecturas ->", out)


if __name__ == "__main__":
    main()
