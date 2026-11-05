"""Paso 5 del proceso de reclasificación: combina las rondas, consolida por mayoría y lleva el resultado al repo.

Uso: python3 scripts/aplicar_reclasificacion.py <clave> <dir_ronda1> [<dir_ronda2>] --fuente "<texto usado>"
         [--fecha dd/mm/aaaa] [--rubrica v3]

Cada dir de ronda contiene C/, D/ y E/ con los lotes JSON de cada lector. La ronda 2 sustituye por id a las mismas
iniciativas de la ronda 1. Después:
  1. consolida con scripts/consolidar_lecturas.py (un colectivo cuenta si lo marcan 2 de 3) y valida el resultado;
  2. sustituye data/clasificacion/<clave>/clas_*.json por la consolidada;
  3. guarda las lecturas en data/clasificacion/<clave>/lectura_<versión>/ (C, D, E, CAMBIOS.md y lecturas.json);
  4. añade (o reemplaza, si ya existía la de esa versión) la sección de REVISION.md con las métricas de
     scripts/comparar_lecturas.py; la fecha es --fecha o la de hoy;
  5. regenera site/data/<clave>.json con scripts/build_data.py.
La versión de la rúbrica se lee de la cabecera de data/clasificacion/RUBRICA.md («Versión 3 …» -> v3); --rubrica la fuerza.
No hace peticiones de red.

Flujo completo del proceso (detalle en scripts/lotes_reclasificacion.py):
  descargar los textos -> lotes -> tres lecturas independientes con RUBRICA.md y el prompt de
  data/clasificacion/PROMPT_LECTOR.md -> segunda ronda con más texto (--hueco) -> ESTE script -> cerrar_reclasificacion.py.
Descargas: congreso.es no admite peticiones en paralelo; una cada 2-3 s y parar ante un 403.
"""
import argparse, datetime, glob, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comparar_lecturas as C

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def version_rubrica(root=ROOT, forzada=None):
    """«v3» desde la cabecera de RUBRICA.md («Versión 3 (fecha …)»), o la forzada."""
    if forzada:
        return forzada
    with open(os.path.join(root, "data", "clasificacion", "RUBRICA.md"), encoding="utf-8") as f:
        m = re.search(r"^Versi[óo]n\s+(\d+)\b", f.read(), re.M)
    if not m:
        sys.exit("No se pudo leer la versión de RUBRICA.md: pásala con --rubrica vN")
    return "v" + m.group(1)


def run(*cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"Falló {' '.join(cmd)}\n{p.stdout}{p.stderr}")
    return p.stdout


def combinar(r1, r2, tmp):
    """Escribe en tmp/final/<L>/ los lotes de la ronda 1 con las iniciativas de la ronda 2 sustituidas por id."""
    n2 = 0
    for L in "CDE":
        ficheros = sorted(glob.glob(f"{r1}/{L}/*.json"))
        if not ficheros:
            sys.exit(f"{r1}/{L} no tiene lotes")
        nuevo = {it["id"]: it for f in glob.glob(f"{r2}/{L}/*.json") for it in json.load(open(f, encoding="utf-8"))} if r2 else {}
        n2 = max(n2, len(nuevo))
        os.makedirs(f"{tmp}/final/{L}")
        for f in ficheros:
            lote = [nuevo.get(it["id"], it) for it in json.load(open(f, encoding="utf-8"))]
            json.dump(lote, open(f"{tmp}/final/{L}/{os.path.basename(f)}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return n2


def escribir_seccion(path, prefijo, seccion):
    """Añade la sección al final del fichero o reemplaza la que empiece por `prefijo` (hasta el siguiente «## »)."""
    lineas = open(path, encoding="utf-8").read().splitlines(keepends=True) if os.path.exists(path) else []
    ini = next((n for n, l in enumerate(lineas) if l.startswith(prefijo)), None)
    if ini is None:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n\n" + seccion)
        return
    fin = next((n for n in range(ini + 1, len(lineas)) if lineas[n].startswith("## ")), len(lineas))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(lineas[:ini]) + seccion + ("\n" if fin < len(lineas) else "") + "".join(lineas[fin:]))


def main():
    ap = argparse.ArgumentParser(description="Aplica una reclasificación (rondas -> consolidación -> repo).")
    ap.add_argument("clave")
    ap.add_argument("ronda1")
    ap.add_argument("ronda2", nargs="?")
    ap.add_argument("--fuente", required=True, help="descripción del texto usado, para REVISION.md")
    ap.add_argument("--fecha", default=datetime.date.today().strftime("%d/%m/%Y"))
    ap.add_argument("--rubrica", help="versión de la rúbrica (vN); por defecto, la de RUBRICA.md")
    a = ap.parse_args()
    clave = a.clave
    ver = version_rubrica(ROOT, a.rubrica)
    base = os.path.join(ROOT, "data", "clasificacion", clave)
    with tempfile.TemporaryDirectory(prefix="aplicar_" + clave + "_") as tmp:
        n2 = combinar(a.ronda1, a.ronda2, tmp)
        print(run("python3", "scripts/consolidar_lecturas.py", clave, *[f"{tmp}/final/{L}" for L in "CDE"], f"{tmp}/consol").strip())
        for f in sorted(glob.glob(f"{tmp}/consol/clas_*.json")):
            out = run("python3", "scripts/validar_clasificacion.py", clave, f)
            if " 0 errores" not in out:
                sys.exit(f"La consolidación no valida:\n{out}")
        Lr = {x: C.cargar(f"{tmp}/final/{x}/*.json") for x in "CDE"}
        Lr["N"] = C.cargar(f"{tmp}/consol/clas_*.json")
        Lr["v"] = C.cargar(os.path.join(base, "clas_*.json"))
        ids = sorted(Lr["v"])
        for x in "CDEN":
            falta = [i for i in ids if i not in Lr[x]]
            if falta:
                sys.exit(f"Al lector {x} le faltan {len(falta)} iniciativas de la vigente (p. ej. {falta[:3]}): lotes incompletos")
        pares = [C.resumen_par(Lr, p, q, ids) for p, q in (("C", "D"), ("C", "E"), ("D", "E"))]
        un = sum(1 for i in ids if C.pares(Lr["C"][i]) == C.pares(Lr["D"][i]) == C.pares(Lr["E"][i]))
        contra = max(p["con_contradiccion"] for p in pares)
        jac = round(sum(p["jaccard_medio"] for p in pares) / 3, 2)
        exac = (min(p["impactos_exactos_pct"] for p in pares), max(p["impactos_exactos_pct"] for p in pares))
        cambian = sum(1 for i in ids if C.pares(Lr["N"][i]) != C.pares(Lr["v"][i]) or Lr["N"][i].get("peso") != Lr["v"][i].get("peso"))
        vac_v = sum(1 for i in ids if not Lr["v"][i].get("imp"))
        vac_n = sum(1 for i in ids if not Lr["N"][i].get("imp"))
        # al repo
        for f in glob.glob(f"{tmp}/consol/clas_*.json"):
            shutil.copy(f, base)
        dst = os.path.join(base, "lectura_" + ver)
        shutil.rmtree(dst, ignore_errors=True)
        for L in "CDE":
            shutil.copytree(f"{tmp}/final/{L}", f"{dst}/{L}")
        for f in ("CAMBIOS.md", "lecturas.json"):
            shutil.copy(f"{tmp}/consol/{f}", dst)
    ronda2 = f" {n2} iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial." if a.ronda2 else ""
    escribir_seccion(os.path.join(base, "REVISION.md"), f"## Reclasificación con la rúbrica {ver} (", f"""## Reclasificación con la rúbrica {ver} ({a.fecha})

Las {len(ids)} iniciativas se han reclasificado con la rúbrica {ver} por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: {a.fuente}.{ronda2} Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: {exac[0]:.0f}–{exac[1]:.0f} % idéntica, parecido medio {jac}, {contra} con signo contrario; {un} de {len(ids)} idénticas en las tres lecturas.
- {cambian} iniciativas cambian respecto a la clasificación anterior: `lectura_{ver}/CAMBIOS.md`. Las tres lecturas: `lectura_{ver}/lecturas.json` y `lectura_{ver}/<lector>/`.
- Sin efectos: {vac_v} antes, {vac_n} ahora.
""")
    print(run("python3", "scripts/build_data.py", clave).strip().splitlines()[-1][:120])
    print(json.dumps({"clave": clave, "n": len(ids), "unanimes": un, "contra": contra, "jaccard": jac, "exactas": exac,
                      "cambian": cambian, "vacias_antes": vac_v, "vacias_ahora": vac_n, "ronda2": n2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
