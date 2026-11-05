"""Paso 1 del proceso de reclasificación: lotes con el texto oficial de cada iniciativa (y cálculo de la segunda ronda).

Uso:
  python3 scripts/lotes_reclasificacion.py <clave> <dir_salida> [--chars N] [--tam N] [--ids f.json]
  python3 scripts/lotes_reclasificacion.py <clave> <dir_salida> --hueco <dir_ronda1> [--chars N] [--tam N]

Sirve para las claves del Congreso (`congreso_*`) y del Parlamento Europeo (`europarlamento_*`); la fuente se
detecta por `scripts/legislaturas.py`. Toma los lotes de data/clasificacion/<clave>/lotes/ (id, tipo, título,
autor) y añade a cada iniciativa `texto`, leído de la caché local:
  - Congreso: data/cache/<leg>/textos/<id>.txt, desde la exposición de motivos o el preámbulo si se encuentra.
    En un real decreto-ley (130/) usa el texto de su proyecto de ley (121/) y lo anota en `nota_fuente`.
  - Parlamento Europeo: data/cache/<clave>/textos/<ref>.txt (texto aprobado), desde el principio.
Sin texto, `texto` va vacío y el lector se ciñe al título. Este script no hace peticiones de red.
--chars: caracteres de texto por iniciativa (5.000; 12.000 con --hueco). --tam: iniciativas por lote (55).

Segunda ronda: con --ids solo entran los ids del fichero JSON (lista de ids). Con --hueco <dir_ronda1> los calcula:
entran las iniciativas que al menos 2 de los 3 lectores de la primera ronda (<dir_ronda1>/C, /D y /E) dejan sin
`imp` y que en la clasificación vigente sí tenían efectos. Los ids se guardan en <dir_salida>/ids_hueco.json.

Flujo completo, repetible por cualquiera (cada paso es un script o una instrucción de este repositorio):
  1. Descargar los textos que falten, en secuencia (congreso.es tiene anti-bots: nunca en paralelo, una petición
     cada 2-3 s, parar ante un 403; los scripts de descarga ya lo respetan):
       .venv/bin/python scripts/textos_bocg.py <clave> <id> …                 (Congreso)
       .venv/bin/python scripts/textos_europarlamento.py <clave> <ref> …      (Parlamento Europeo)
  2. Generar los lotes de la primera ronda (este script).
  3. Tres lecturas independientes (C, D y E) de cada lote con data/clasificacion/RUBRICA.md, cada una por un agente
     de IA distinto que no vea la clasificación vigente ni a los otros lectores. El prompt literal está en
     data/clasificacion/PROMPT_LECTOR.md. Salida: <dir_ronda1>/<lector>/<lote>.json.
  4. Segunda ronda con más texto: bajar los textos de los ids con --hueco, generar sus lotes con
     `--hueco <dir_ronda1> --chars 12000` y repetir el paso 3 (prompt de segunda ronda) hacia <dir_ronda2>.
  5. Aplicar: python3 scripts/aplicar_reclasificacion.py <clave> <dir_ronda1> [<dir_ronda2>] --fuente "…"
  6. Cerrar (tras aplicar una o varias legislaturas): python3 scripts/cerrar_reclasificacion.py
"""
import argparse, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INICIO = re.compile(r"EXPOSICI[ÓO]N\s+DE\s+MOTIVOS|PRE[ÁA]MBULO|Exposici[óo]n\s+de\s+motivos|Pre[áa]mbulo")
RDL = re.compile(r"Real Decreto-ley (\d+/\d{4})")
CHARS_RONDA1, CHARS_HUECO, TAM = 5000, 12000, 55


def limpiar(t):
    return re.sub(r"\n{2,}", "\n", re.sub(r"[ \t]+", " ", re.sub(r"-\n(?=\w)", "", t))).strip()


def leer_lotes(clave, root=ROOT):
    return [x for f in sorted(glob.glob(os.path.join(root, "data", "clasificacion", clave, "lotes", "*.json")))
            for x in json.load(open(f, encoding="utf-8"))]


def leer_texto(clave, ident, root=ROOT):
    cfg = LEGISLATURAS[clave]
    if cfg["fuente"] == "congreso":
        p = os.path.join(root, "data", "cache", cfg["leg"].lower(), "textos", ident.replace("/", "_") + ".txt")
    elif cfg["fuente"] == "europarlamento":
        p = os.path.join(root, "data", "cache", clave, "textos", re.sub(r"[^\w]", "_", ident) + ".txt")
    else:
        raise SystemExit(f"fuente no soportada: {cfg['fuente']!r}")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def cargar_lectores(dir_ronda):
    """{lector: {id: lectura}} de <dir_ronda>/C, /D y /E."""
    return {x: {it["id"]: it for f in glob.glob(os.path.join(dir_ronda, x, "*.json"))
                for it in json.load(open(f, encoding="utf-8"))} for x in "CDE"}


def hueco(clave, dir_ronda1, root=ROOT):
    """Ids de la segunda ronda: sin `imp` en al menos 2 de 3 lectores y con efectos en la clasificación vigente."""
    L = cargar_lectores(dir_ronda1)
    if not L["C"]:
        raise SystemExit(f"{dir_ronda1}/C no tiene lecturas")
    vigente = {it["id"]: it for f in glob.glob(os.path.join(root, "data", "clasificacion", clave, "clas_*.json"))
               for it in json.load(open(f, encoding="utf-8"))}
    return sorted(i for i in L["C"]
                  if sum(1 for x in "CDE" if not (L[x].get(i) or {}).get("imp")) >= 2 and vigente.get(i, {}).get("imp"))


def construir(clave, chars, solo=None, root=ROOT):
    """Iniciativas de los lotes con su `texto`; devuelve (lista, recuento de fuentes de texto)."""
    congreso = LEGISLATURAS[clave]["fuente"] == "congreso"
    todos = leer_lotes(clave, root)
    rdl2pl = {}
    for it in todos:
        m = RDL.search(it["titulo"])
        if it["id"].startswith("121/") and m:
            rdl2pl.setdefault(m.group(1), it["id"])
    res, cuenta = [], {"propio": 0, "proyecto": 0, "vacio": 0}
    for it in todos:
        if solo is not None and it["id"] not in solo:
            continue
        it, t = dict(it), ""
        if congreso and it["id"].startswith("130/"):
            m = RDL.search(it["titulo"])
            pl = rdl2pl.get(m.group(1)) if m else None
            if pl and leer_texto(clave, pl, root):
                t = leer_texto(clave, pl, root)
                cuenta["proyecto"] += 1
                it["nota_fuente"] = f"texto del proyecto de ley {pl}, que procede de este real decreto-ley"
        if not t:
            t = leer_texto(clave, it["id"], root)
            cuenta["propio" if t else "vacio"] += 1
        m = INICIO.search(t) if congreso else None
        it["texto"] = limpiar(t[m.start():] if m else t)[:chars]
        res.append(it)
    return res, cuenta


def main():
    ap = argparse.ArgumentParser(description="Lotes de reclasificación con texto oficial.")
    ap.add_argument("clave")
    ap.add_argument("dir_salida")
    ap.add_argument("--chars", type=int)
    ap.add_argument("--tam", type=int, default=TAM)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ids", help="JSON con la lista de ids que entran (segunda ronda manual)")
    g.add_argument("--hueco", metavar="DIR_RONDA1", help="calcula los ids de la segunda ronda desde la primera")
    a = ap.parse_args()
    if a.clave not in LEGISLATURAS:
        sys.exit(f"clave desconocida: {a.clave}")
    chars = a.chars or (CHARS_HUECO if a.hueco else CHARS_RONDA1)
    solo = None
    os.makedirs(a.dir_salida, exist_ok=True)
    if a.ids:
        solo = set(json.load(open(a.ids, encoding="utf-8")))
    elif a.hueco:
        ids = hueco(a.clave, a.hueco)
        json.dump(ids, open(os.path.join(a.dir_salida, "ids_hueco.json"), "w", encoding="utf-8"), ensure_ascii=False)
        solo = set(ids)
    res, cuenta = construir(a.clave, chars, solo)
    nombres = []
    for n in range(0, len(res), a.tam):
        fn = f"{a.clave}_l{n // a.tam:02d}.json"
        json.dump(res[n:n + a.tam], open(os.path.join(a.dir_salida, fn), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        nombres.append(fn)
    print(json.dumps({"clave": a.clave, "fuentes": cuenta, "total": len(res), "lotes": nombres}, ensure_ascii=False))


if __name__ == "__main__":
    main()
