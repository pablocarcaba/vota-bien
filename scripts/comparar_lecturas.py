"""Compara lecturas independientes de la clasificación de una legislatura (doble lectura).

Uso: python3 scripts/comparar_lecturas.py <clave> <dir_lector_A> <dir_lector_B> [--guardar]

Cada directorio contiene los lotes clasificados por un lector (mismos nombres que los lotes, mismo
formato que clas_*.json). Se comparan tres lecturas por iniciativa: la clasificación vigente
(data/clasificacion/<clave>/clas_*.json) y los lectores A y B, que la hicieron sin ver la vigente.

Para cada par de lecturas mide:
  - coincidencia exacta de impactos (mismos colectivos con el mismo signo),
  - parecido de impactos (Jaccard sobre los pares colectivo+signo; dos lecturas vacías = 1),
  - contradicciones (un colectivo marcado con signo contrario),
  - coincidencia de tipo (eco/soc) y de alcance (peso).

Con --guardar copia las lecturas A y B a data/clasificacion/<clave>/doble_lectura/ y escribe allí
resumen.json (métricas) y DISCREPANCIAS.md (casos para revisión humana). No modifica clas_*.json:
la clasificación vigente solo cambia por decisión humana, siguiendo INSTRUCCIONES.md.
"""
import glob, json, os, shutil, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def cargar(patron):
    out = {}
    for f in sorted(glob.glob(patron)):
        for it in json.load(open(f, encoding="utf-8")):
            out[it["id"]] = it
    return out


def pares(it):
    return {(k, 1 if v > 0 else -1) for k, v in (it.get("imp") or {}).items() if v}


def comparar(x, y):
    px, py = pares(x), pares(y)
    union = px | py
    cx = {k: s for k, s in px}
    cy = {k: s for k, s in py}
    return {
        "exacta": px == py,
        "jaccard": 1.0 if not union else len(px & py) / len(union),
        "contradicciones": sorted(k for k in cx.keys() & cy.keys() if cx[k] != cy[k]),
        "tipo": x.get("tipo") == y.get("tipo"),
        "peso": x.get("peso") == y.get("peso"),
    }


def resumen_par(lect, a, b, ids):
    cs = [comparar(lect[a][i], lect[b][i]) for i in ids]
    n = len(cs)
    return {
        "par": f"{a}-{b}",
        "n": n,
        "impactos_exactos_pct": round(100 * sum(c["exacta"] for c in cs) / n, 1),
        "jaccard_medio": round(sum(c["jaccard"] for c in cs) / n, 3),
        "con_contradiccion": sum(bool(c["contradicciones"]) for c in cs),
        "tipo_pct": round(100 * sum(c["tipo"] for c in cs) / n, 1),
        "peso_pct": round(100 * sum(c["peso"] for c in cs) / n, 1),
    }


def fmt(it):
    imp = it.get("imp") or {}
    s = ", ".join(f"{k} {'+' if v > 0 else '−'}" for k, v in sorted(imp.items())) or "sin impactos"
    return f"{s} · peso {it.get('peso')}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    clave, dir_a, dir_b = args
    guardar = "--guardar" in sys.argv
    base = os.path.join(ROOT, "data", "clasificacion", clave)
    lect = {
        "vigente": cargar(os.path.join(base, "clas_*.json")),
        "A": cargar(os.path.join(dir_a, "*.json")),
        "B": cargar(os.path.join(dir_b, "*.json")),
    }
    ids = sorted(set(lect["A"]) & set(lect["B"]) & set(lect["vigente"]))
    faltan = {k: sorted(set(lect["vigente"]) - set(v)) for k, v in lect.items() if k != "vigente"}
    if not ids:
        sys.exit("No hay iniciativas comunes a las tres lecturas")

    pares_res = [resumen_par(lect, a, b, ids) for a, b in (("A", "B"), ("vigente", "A"), ("vigente", "B"))]
    # una iniciativa es «consolidada» si las tres lecturas coinciden en impactos; «a revisar» si hay
    # alguna contradicción de signo o el parecido medio entre pares es bajo
    consolidadas, revisar = [], []
    for i in ids:
        cs = [comparar(lect[a][i], lect[b][i]) for a, b in (("A", "B"), ("vigente", "A"), ("vigente", "B"))]
        if all(c["exacta"] for c in cs):
            consolidadas.append(i)
        elif any(c["contradicciones"] for c in cs) or sum(c["jaccard"] for c in cs) / 3 < 0.5:
            revisar.append((i, sorted({k for c in cs for k in c["contradicciones"]}), sum(c["jaccard"] for c in cs) / 3))

    res = {
        "clave": clave,
        "iniciativas": len(ids),
        "faltan_por_lector": {k: len(v) for k, v in faltan.items()},
        "pares": pares_res,
        "consolidadas": len(consolidadas),
        "a_revisar": len(revisar),
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))

    if guardar:
        out = os.path.join(base, "doble_lectura")
        for k, d in (("A", dir_a), ("B", dir_b)):
            os.makedirs(os.path.join(out, k), exist_ok=True)
            for f in sorted(glob.glob(os.path.join(d, "*.json"))):
                shutil.copy(f, os.path.join(out, k, os.path.basename(f)))
        json.dump(res, open(os.path.join(out, "resumen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        tit = {i: lect["vigente"][i].get("nota", "") for i in ids}
        with open(os.path.join(out, "DISCREPANCIAS.md"), "w", encoding="utf-8") as f:
            f.write(f"# Doble lectura de {clave}: casos para revisión humana\n\n")
            f.write("Generado por `scripts/comparar_lecturas.py`. Tres lecturas por iniciativa: la vigente y dos lectores "
                    "independientes (A y B) que clasificaron sin verla, con la misma rúbrica. Aquí solo aparecen las "
                    "iniciativas con una contradicción de signo o con poco parecido entre lecturas. La clasificación "
                    "vigente no se ha tocado: cualquier cambio se decide caso a caso.\n\n")
            for p in pares_res:
                f.write(f"- **{p['par']}**: impactos idénticos en el {p['impactos_exactos_pct']} %, parecido medio "
                        f"{p['jaccard_medio']}, {p['con_contradiccion']} con signo contrario, tipo {p['tipo_pct']} %, "
                        f"alcance {p['peso_pct']} %\n")
            f.write(f"\n{len(consolidadas)} de {len(ids)} iniciativas coinciden en las tres lecturas; {len(revisar)} a revisar.\n")
            for i, contra, j in sorted(revisar, key=lambda r: (-len(r[1]), r[2])):
                f.write(f"\n## {i}\n\n{tit[i]}\n\n")
                if contra:
                    f.write(f"Signo contrario en: {', '.join(contra)}. Parecido medio {j:.2f}.\n\n")
                else:
                    f.write(f"Parecido medio {j:.2f}.\n\n")
                for k in ("vigente", "A", "B"):
                    f.write(f"- {k}: {fmt(lect[k][i])}\n")
        print("Guardado en", out)


if __name__ == "__main__":
    main()
