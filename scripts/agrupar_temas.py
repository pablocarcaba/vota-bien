"""Agrupa las iniciativas con el mismo contenido de cada legislatura (rúbrica 3.9) para que cuenten una sola vez.

Uso: python3 scripts/agrupar_temas.py [clave ...]     (sin claves: todas las legislaturas clasificadas)

Escribe data/clasificacion/<clave>/temas.json: una lista de grupos {"ids": [...], "t": título del primero}. Es una
propuesta automática y revisable: se puede editar a mano (quitar o juntar grupos) y build_data.py la respeta. Si se
vuelve a ejecutar, se regenera desde cero.

Criterio (estricto, para no juntar decisiones distintas): mismo tipo (eco/soc) y misma clasificación (imp, no vacía), y
  - un real decreto-ley y el proyecto de ley «procedente del Real Decreto-ley N/AAAA», o
  - títulos casi iguales (≥ 75 % de palabras en común) con los mismos números (años, leyes que modifican).
No junta presupuestos de años distintos, prórrogas sucesivas de un decreto ni acuerdos con países distintos.

En la nota, cada partido cuenta un solo grupo con su mejor prueba (votó > tenía escaño y no votó > solo la presentó;
después, la de más peso y la más reciente).
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STOP = set("proposicion proposición proyecto ley orgánica organica para sobre desde entre por la el los las del de en y "
           "a que con se al una un su sus no o le real decreto-ley decreto".split())


def toks(s):
    return {w for w in re.findall(r"[a-záéíóúñü]+", s.lower()) if len(w) > 3 and w not in STOP}


def nums(s):
    return set(re.findall(r"\d+(?:/\d+)?", s))


def rdl(s):
    m = re.search(r"real decreto-ley (\d+/\d{4})", s.lower())
    return m and m.group(1)


def mismo(a, b):
    if a["tipo"] != b["tipo"] or a["imp"] != b["imp"]:
        return False
    ra, rb = rdl(a["titulo"]), rdl(b["titulo"])
    if ra and ra == rb and ("procedente" in a["titulo"].lower()) != ("procedente" in b["titulo"].lower()):
        return True
    ta, tb = toks(a["titulo"]), toks(b["titulo"])
    if not ta or not tb or nums(a["titulo"]) != nums(b["titulo"]):
        return False
    return len(ta & tb) / len(ta | tb) >= 0.75


def agrupar(clave):
    d = os.path.join(ROOT, "data", "clasificacion", clave)
    clas = {}
    for p in sorted(glob.glob(os.path.join(d, "clas_*.json"))):
        for x in json.load(open(p, encoding="utf-8")):
            clas[x["id"]] = x
    items = json.load(open(os.path.join(ROOT, "data", "generado", clave, "items.json"), encoding="utf-8"))
    its = [{"id": i["id"], "titulo": i["titulo"], **clas[i["id"]]} for i in items if i["id"] in clas and clas[i["id"]]["imp"]]
    par = {i["id"]: i["id"] for i in its}

    def raiz(x):
        while par[x] != x:
            x = par[x]
        return x

    for i, a in enumerate(its):
        for b in its[i + 1:]:
            if mismo(a, b):
                par[raiz(a["id"])] = raiz(b["id"])
    G = {}
    for i in its:
        G.setdefault(raiz(i["id"]), []).append(i)
    grupos = [{"ids": [i["id"] for i in g], "t": g[0]["titulo"][:120]} for g in G.values() if len(g) > 1]
    grupos.sort(key=lambda g: g["ids"][0])
    with open(os.path.join(d, "temas.json"), "w", encoding="utf-8") as fh:
        json.dump(grupos, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"{clave}: {len(grupos)} grupos, {sum(len(g['ids']) for g in grupos)} iniciativas")


if __name__ == "__main__":
    claves = sys.argv[1:] or [k for k in LEGISLATURAS
                              if os.path.exists(os.path.join(ROOT, "data", "clasificacion", k, "clas_0.json"))]
    for k in claves:
        agrupar(k)
