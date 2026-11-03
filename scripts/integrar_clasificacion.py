"""Integra lotes clasificados en data/clasificacion/<clave>/ y armoniza duplicados.

Uso: python3 scripts/integrar_clasificacion.py congreso_xiv salida/lote_00.json [salida/lote_01.json …]

- Cada fichero de entrada (salida de clasificar un lote) se guarda como clas_N.json (N siguiente libre).
- Los reales decretos-ley tramitados después como proyecto de ley son la misma norma: se les da la unión
  de impactos y la nota más completa (si los signos se contradicen, se avisa y no se toca).
- Termina ejecutando el validador.
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def armonizar(clave):
    cdir = os.path.join(ROOT, "data", "clasificacion", clave)
    files = {p: json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(cdir, "clas_*.json")))}
    c = {x["id"]: x for f in files.values() for x in f}
    items = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "data", "generado", clave, "items.json"), encoding="utf-8"))}
    grupos = {}
    for i, it in items.items():
        m = re.search(r"Real Decreto-ley (\d+/\d{4})", it["titulo"])
        if m and i in c:
            grupos.setdefault(m.group(1), []).append(i)
    n = 0
    for rdl, ids in grupos.items():
        if len(ids) < 2 or all(c[i]["imp"] == c[ids[0]]["imp"] for i in ids):
            continue
        u, choque = {}, False
        for i in ids:
            for k, v in c[i]["imp"].items():
                choque |= u.get(k, v) != v
                u[k] = v
        if choque:
            print(f"AVISO RDL {rdl}: signos contradictorios entre {ids}; revísalo a mano")
            continue
        mejor = max(ids, key=lambda i: len(c[i]["imp"]))
        for i in ids:
            c[i]["imp"], c[i]["nota"] = dict(u), c[mejor]["nota"]
        n += 1
    for p, f in files.items():
        json.dump(f, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"{n} RDL armonizados")


def main():
    clave, entradas = sys.argv[1], sys.argv[2:]
    cdir = os.path.join(ROOT, "data", "clasificacion", clave)
    os.makedirs(cdir, exist_ok=True)
    hechas = {x["id"] for p in glob.glob(os.path.join(cdir, "clas_*.json")) for x in json.load(open(p, encoding="utf-8"))}
    n = len(glob.glob(os.path.join(cdir, "clas_*.json")))
    for e in entradas:
        datos = json.load(open(e, encoding="utf-8"))
        rep = [x["id"] for x in datos if x["id"] in hechas]
        if rep:
            sys.exit(f"{e}: {len(rep)} iniciativas ya estaban clasificadas ({rep[:3]}…); no se integra")
        dest = os.path.join(cdir, f"clas_{n}.json")
        json.dump(datos, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        hechas |= {x["id"] for x in datos}
        print(e, "->", dest, len(datos))
        n += 1
    armonizar(clave)
    sys.exit(subprocess.call([sys.executable, os.path.join(ROOT, "scripts", "validar_clasificacion.py"), clave]))


if __name__ == "__main__":
    main()
