"""Paso 5 del proceso de reclasificación: combina las rondas, consolida por mayoría y lleva el resultado al repo.

Uso: python3 scripts/aplicar_reclasificacion.py <clave> <dir_ronda1> [<dir_ronda2>] --fuente "<texto usado>"
         [--fecha dd/mm/aaaa] [--rubrica v3] [--rehacer --motivo "…"] [--conservar <ids|fichero.json>] [--ids-hueco f.json]

Cada dir de ronda contiene C/, D/ y E/ con los lotes JSON de cada lector. La ronda 2 sustituye por id a las mismas
iniciativas de la ronda 1; en C, D y E debe ser el mismo conjunto de ids, incluido en la ronda 1 (y, si hay
ids_hueco.json en <dir_ronda2> o se pasa --ids-hueco, idéntico a él): si no, falla antes de escribir. Después:
  1. consolida con scripts/consolidar_lecturas.py (un colectivo cuenta si lo marcan 2 de 3) y valida el resultado;
  2. sustituye data/clasificacion/<clave>/clas_*.json por la consolidada;
  3. guarda las lecturas en data/clasificacion/<clave>/lectura_<versión>/ (C, D, E, CAMBIOS.md y lecturas.json);
  4. añade (o reemplaza, si ya existía la de esa versión) la sección de REVISION.md con las métricas de
     scripts/comparar_lecturas.py; la fecha es --fecha o la de hoy. El resto de secciones (p. ej. «## Revisiones
     posteriores») se conserva;
  5. regenera site/data/<clave>.json con scripts/build_data.py. Si falla, restaura clas_*.json, REVISION.md y
     lectura_<versión>/ como estaban.
Protección de las correcciones manuales (heurística, no exacta):
  - si ya existe lectura_<versión>/ falla salvo con --rehacer --motivo "…" (solo autoriza repetir sobre esa carpeta);
  - antes de escribir, detecta las iniciativas de la vigente que parecen corregidas a mano después de las lecturas: la
    vigente difiere de la consolidación de la lectura_<versión> ya aplicada, o lleva un colectivo que aparece entre
    backticks en RUBRICA.md y que ninguna lectura (C, D, E de ninguna legislatura, data/clasificacion/*/lectura_<versión>/)
    usa. Cada una debe decidirse: --conservar <ids|fichero.json> (se mantiene la vigente) o --sobrescribir <ids|fichero.json>
    (se escribe la lectura). Si queda alguna sin decidir, falla antes de escribir. Los ids de ambas listas van a REVISION.md;
  - aviso, sin bloquear: iniciativas cuya vigente no coincide con ninguna lectura, y las que difieren de la última
    lectura_vN anterior (ediciones posteriores a esa versión).
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


def leer_ids(dir_ronda, L):
    """Ids que el lector L tiene en <dir_ronda>/L/*.json."""
    return {it["id"] for f in glob.glob(f"{dir_ronda}/{L}/*.json") for it in json.load(open(f, encoding="utf-8"))}


def comprobar_ronda2(r1, r2, ids_hueco=None):
    """La ronda 2 debe ser idéntica en C, D y E, estar incluida en la ronda 1 y, si hay ids_hueco.json, coincidir con él."""
    ids = {L: leer_ids(r2, L) for L in "CDE"}
    if not ids["C"]:
        sys.exit(f"{r2}/C no tiene lecturas: la ronda 2 está vacía")
    if not ids["C"] == ids["D"] == ids["E"]:
        dif = {L: len(ids[L]) for L in "CDE"}
        union = ids["C"] | ids["D"] | ids["E"]
        falta = {L: sorted(union - ids[L])[:3] for L in "CDE" if union - ids[L]}
        sys.exit(f"Ronda 2 parcial: los lectores C, D y E no leyeron las mismas iniciativas ({dif}); les faltan {falta}")
    fuera = sorted(ids["C"] - leer_ids(r1, "C"))
    if fuera:
        sys.exit(f"La ronda 2 trae {len(fuera)} ids que no están en la ronda 1 (p. ej. {fuera[:3]})")
    ids_hueco = ids_hueco or (os.path.join(r2, "ids_hueco.json") if os.path.exists(os.path.join(r2, "ids_hueco.json")) else None)
    if ids_hueco:
        esperados = set(json.load(open(ids_hueco, encoding="utf-8")))
        if esperados != ids["C"]:
            sys.exit(f"La ronda 2 no coincide con {ids_hueco}: faltan {sorted(esperados - ids['C'])[:3]}, sobran {sorted(ids['C'] - esperados)[:3]}")
    return ids["C"]


def combinar(r1, r2, tmp, ids_hueco=None):
    """Escribe en tmp/final/<L>/ los lotes de la ronda 1 con las iniciativas de la ronda 2 sustituidas por id.
    Devuelve cuántas iniciativas se sustituyen (solo las aplicadas)."""
    ids2 = comprobar_ronda2(r1, r2, ids_hueco) if r2 else set()
    for L in "CDE":
        ficheros = sorted(glob.glob(f"{r1}/{L}/*.json"))
        if not ficheros:
            sys.exit(f"{r1}/{L} no tiene lotes")
        nuevo = {it["id"]: it for f in glob.glob(f"{r2}/{L}/*.json") for it in json.load(open(f, encoding="utf-8"))} if r2 else {}
        os.makedirs(f"{tmp}/final/{L}")
        for f in ficheros:
            lote = [nuevo.get(it["id"], it) for it in json.load(open(f, encoding="utf-8"))]
            json.dump(lote, open(f"{tmp}/final/{L}/{os.path.basename(f)}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(ids2)


def igual(a, b):
    return C.pares(a) == C.pares(b) and a.get("peso") == b.get("peso") and a.get("tipo") == b.get("tipo")


def colectivos_usados(root, ver, lecturas):
    """Colectivos que usa alguna lectura: las de esta legislatura y las lectura_<ver>/[CDE] de todas las legislaturas."""
    usados = {k for x in "CDE" for it in lecturas[x].values() for k, _ in C.pares(it)}
    for f in glob.glob(os.path.join(root, "data", "clasificacion", "*", "lectura_" + ver, "[CDE]", "*.json")):
        usados |= {k for it in json.load(open(f, encoding="utf-8")) for k, _ in C.pares(it)}
    return usados


def lectura_anterior(base, ver):
    """Ruta de la lectura_vN más reciente anterior a `ver` con sus tres lectores, o None."""
    m = re.fullmatch(r"v(\d+)", ver)
    if not m:
        return None
    previas = sorted((int(re.fullmatch(r"lectura_v(\d+)", os.path.basename(d)).group(1)), d)
                     for d in glob.glob(os.path.join(base, "lectura_v*")) if re.fullmatch(r"lectura_v\d+", os.path.basename(d)))
    for n, d in reversed(previas):
        if n < int(m.group(1)) and all(glob.glob(f"{d}/{x}/*.json") for x in "CDE"):
            return d
    return None


def riesgos(vig, nueva, lecturas, previa, rubrica, usados):
    """(editadas, sin_respaldo): iniciativas cuyo valor vigente se perdería al escribir la consolidación `nueva`.
    editadas (heurística): la vigente difiere de la consolidación de la lectura ya aplicada (`previa`)
      o lleva un colectivo de la rúbrica actual que ninguna lectura (`usados`) usa.
    sin_respaldo (aviso): la vigente tiene algo que ninguno de los tres lectores marcó en esa iniciativa."""
    en_rubrica = set(re.findall(r"`(\w+)`", rubrica))
    ignorados = ({k for it in vig.values() for k, _ in C.pares(it)} & en_rubrica) - usados
    editadas, sin_respaldo = [], []
    for i in sorted(vig):
        if igual(vig[i], nueva[i]):
            continue
        desconocido = any(k in ignorados for k, _ in C.pares(vig[i]))
        tocada = previa is not None and i in previa and not igual(vig[i], previa[i])
        if desconocido or tocada:
            editadas.append(i)
            continue
        lect = [lecturas[x][i] for x in "CDE"]
        if not (C.pares(vig[i]) <= set().union(*(C.pares(l) for l in lect))
                and vig[i].get("peso") in {l.get("peso") for l in lect} and vig[i].get("tipo") in {l.get("tipo") for l in lect}):
            sin_respaldo.append(i)
    return editadas, sin_respaldo


def leer_conservar(valor):
    """--conservar: lista de ids separados por comas o ruta de un JSON con la lista."""
    if not valor:
        return set()
    if os.path.isfile(valor):
        return set(json.load(open(valor, encoding="utf-8")))
    return {x.strip() for x in valor.split(",") if x.strip()}


def conservar_en(consol_dir, vig, ids):
    """Sustituye en los clas_*.json consolidados las iniciativas `ids` por su valor vigente."""
    for f in glob.glob(f"{consol_dir}/clas_*.json"):
        datos = json.load(open(f, encoding="utf-8"))
        if any(it["id"] in ids for it in datos):
            datos = [vig[it["id"]] if it["id"] in ids else it for it in datos]
            json.dump(datos, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def respaldar(rutas, tmp):
    """Copia a tmp/respaldo lo que se va a tocar; devuelve lo necesario para restaurarlo."""
    r = []
    for n, p in enumerate(rutas):
        dst = f"{tmp}/respaldo/{n}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isdir(p):
            shutil.copytree(p, dst)
        elif os.path.exists(p):
            shutil.copy2(p, dst)
        r.append((p, dst))
    return r


def restaurar(respaldo):
    for p, dst in respaldo:
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)
        if os.path.isdir(dst):
            shutil.copytree(dst, p)
        elif os.path.exists(dst):
            shutil.copy2(dst, p)


def fecha_por_defecto(hoy=None):
    return (hoy or datetime.date.today()).strftime("%d/%m/%Y")


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
    ap.add_argument("--fecha", default=None, help="dd/mm/aaaa; por defecto, hoy")
    ap.add_argument("--rubrica", help="versión de la rúbrica (vN); por defecto, la de RUBRICA.md")
    ap.add_argument("--rehacer", action="store_true", help="repetir sobre una lectura_<versión>/ que ya existe (no autoriza a perder correcciones manuales)")
    ap.add_argument("--motivo", help="razón de --rehacer (obligatoria con él); queda en REVISION.md")
    ap.add_argument("--conservar", help="ids (separados por comas) o fichero JSON con ids cuya clasificación vigente se mantiene")
    ap.add_argument("--sobrescribir", help="ids (separados por comas) o fichero JSON con ids corregidos a mano que se sobrescriben con las lecturas")
    ap.add_argument("--ids-hueco", help="ids_hueco.json de la segunda ronda (por defecto, el de <ronda2>/ si existe)")
    a = ap.parse_args()
    clave = a.clave
    if a.rehacer and not (a.motivo or "").strip():
        sys.exit('--rehacer exige --motivo "…" (por qué se rehace; queda en REVISION.md)')
    if a.motivo and not a.rehacer:
        sys.exit("--motivo solo se usa con --rehacer")
    ver = version_rubrica(ROOT, a.rubrica)
    base = os.path.join(ROOT, "data", "clasificacion", clave)
    dst = os.path.join(base, "lectura_" + ver)
    if os.path.isdir(dst) and not a.rehacer:
        sys.exit(f"{dst} ya existe: esta reclasificación ya se aplicó. Para repetirla, pasa --rehacer --motivo \"…\" "
                 "(y --conservar / --sobrescribir <ids> para decidir qué pasa con las correcciones manuales posteriores).")
    if a.rehacer and not os.path.isdir(dst):
        sys.exit(f"--rehacer solo repite una reclasificación ya aplicada, y {dst} no existe: quita --rehacer "
                 "(para decidir sobre correcciones manuales usa --conservar / --sobrescribir).")
    conservar, sobrescribir = leer_conservar(a.conservar), leer_conservar(a.sobrescribir)
    if conservar & sobrescribir:
        sys.exit(f"--conservar y --sobrescribir comparten ids: {sorted(conservar & sobrescribir)[:5]}")
    with tempfile.TemporaryDirectory(prefix="aplicar_" + clave + "_") as tmp:
        n2 = combinar(a.ronda1, a.ronda2, tmp, a.ids_hueco)
        print(run("python3", "scripts/consolidar_lecturas.py", clave, *[f"{tmp}/final/{L}" for L in "CDE"], f"{tmp}/consol").strip())
        Lr = {x: C.cargar(f"{tmp}/final/{x}/*.json") for x in "CDE"}
        Lr["N"] = C.cargar(f"{tmp}/consol/clas_*.json")
        Lr["v"] = C.cargar(os.path.join(base, "clas_*.json"))
        ids = sorted(Lr["v"])
        for x in "CDEN":
            falta = [i for i in ids if i not in Lr[x]]
            if falta:
                sys.exit(f"Al lector {x} le faltan {len(falta)} iniciativas de la vigente (p. ej. {falta[:3]}): lotes incompletos")
        desconocidas = sorted((conservar | sobrescribir) - set(ids))
        if desconocidas:
            sys.exit(f"--conservar/--sobrescribir: ids que no están en la clasificación vigente: {desconocidas[:5]}")
        # qué se perdería de la vigente
        previa = None
        if os.path.isdir(dst) and all(glob.glob(f"{dst}/{x}/*.json") for x in "CDE"):
            run("python3", "scripts/consolidar_lecturas.py", clave, *[f"{dst}/{x}" for x in "CDE"], f"{tmp}/previa")
            previa = C.cargar(f"{tmp}/previa/clas_*.json")
        ruta_rubrica = os.path.join(base, "..", "RUBRICA.md")
        rubrica = open(ruta_rubrica, encoding="utf-8").read() if os.path.exists(ruta_rubrica) else ""
        editadas, sin_respaldo = riesgos(Lr["v"], Lr["N"], Lr, previa, rubrica, colectivos_usados(ROOT, ver, Lr))
        anterior = None if previa is not None else lectura_anterior(base, ver)
        if anterior:
            run("python3", "scripts/consolidar_lecturas.py", clave, *[f"{anterior}/{x}" for x in "CDE"], f"{tmp}/anterior")
            ant = C.cargar(f"{tmp}/anterior/clas_*.json")
            tras = [i for i in ids if i in ant and not igual(Lr["v"][i], ant[i])]
            if tras:
                print(f"AVISO: {len(tras)} iniciativas de la vigente difieren de la consolidación de {os.path.basename(anterior)} "
                      f"(correcciones posteriores a la {os.path.basename(anterior)[8:]} anterior; no bloquea): {', '.join(tras[:15])}"
                      f"{' …' if len(tras) > 15 else ''}", file=sys.stderr)
        if sin_respaldo:
            print(f"Aviso: {len(sin_respaldo)} iniciativas cambian y su valor vigente no coincide con ninguna lectura "
                  f"(normal si la rúbrica cambió; revisa lectura_{ver}/CAMBIOS.md): {', '.join(sin_respaldo[:10])}"
                  f"{' …' if len(sin_respaldo) > 10 else ''}", file=sys.stderr)
        inutiles = sorted(sobrescribir - set(editadas))
        if inutiles:
            sys.exit(f"--sobrescribir: no hay nada que sobrescribir en {inutiles[:5]}: no parecen corregidas a mano "
                     "(la lectura se aplica igualmente; quítalas de --sobrescribir).")
        perdidas = [i for i in editadas if i not in conservar and i not in sobrescribir]
        if editadas:
            print(f"{len(editadas)} iniciativas de la vigente parecen corregidas a mano después de las lecturas y se perderían: "
                  f"{', '.join(editadas)}", file=sys.stderr)
        if perdidas:
            sys.exit(f"Sin decidir {len(perdidas)} iniciativas que parecen corregidas a mano: {', '.join(perdidas)}.\n"
                     "Mantenlas con --conservar <ids|fichero> o sobrescríbelas con --sobrescribir <ids|fichero>.")
        conservar_en(f"{tmp}/consol", Lr["v"], conservar)
        for f in sorted(glob.glob(f"{tmp}/consol/clas_*.json")):
            run("python3", "scripts/validar_clasificacion.py", clave, f)  # sale con 1 si no valida
        Lr["N"] = C.cargar(f"{tmp}/consol/clas_*.json")
        pares = [C.resumen_par(Lr, p, q, ids) for p, q in (("C", "D"), ("C", "E"), ("D", "E"))]
        un = sum(1 for i in ids if C.pares(Lr["C"][i]) == C.pares(Lr["D"][i]) == C.pares(Lr["E"][i]))
        contra = max(p["con_contradiccion"] for p in pares)
        jac = round(sum(p["jaccard_medio"] for p in pares) / 3, 2)
        exac = (min(p["impactos_exactos_pct"] for p in pares), max(p["impactos_exactos_pct"] for p in pares))
        cambian = sum(1 for i in ids if C.pares(Lr["N"][i]) != C.pares(Lr["v"][i]) or Lr["N"][i].get("peso") != Lr["v"][i].get("peso"))
        vac_v = sum(1 for i in ids if not Lr["v"][i].get("imp"))
        vac_n = sum(1 for i in ids if not Lr["N"][i].get("imp"))
        ronda2 = f" {n2} iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial." if a.ronda2 else ""
        extra = ""
        detectadas = sorted(conservar & set(editadas))
        manuales = sorted(conservar - set(editadas))
        if detectadas:
            extra += (f"- Se han conservado {len(detectadas)} iniciativas con la clasificación que ya tenían (correcciones manuales "
                      f"detectadas posteriores a las lecturas): {', '.join(detectadas)}.\n")
        if manuales:
            extra += (f"- Se han conservado {len(manuales)} iniciativas por decisión manual (no se detectó ninguna corrección "
                      f"posterior a las lecturas): {', '.join(manuales)}.\n")
        if sobrescribir:
            extra += (f"- Se han sobrescrito {len(sobrescribir)} iniciativas con la lectura, por decisión explícita "
                      f"(`--sobrescribir`): {', '.join(sorted(sobrescribir))}.\n")
        if a.rehacer:
            extra += f"- Reaplicada con --rehacer. Motivo: {a.motivo.strip()}\n"
        seccion = f"""## Reclasificación con la rúbrica {ver} ({a.fecha or fecha_por_defecto()})

Las {len(ids)} iniciativas se han reclasificado con la rúbrica {ver} por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: {a.fuente}.{ronda2} Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: {exac[0]:.0f}–{exac[1]:.0f} % idéntica, parecido medio {jac}, {contra} con signo contrario; {un} de {len(ids)} idénticas en las tres lecturas.
- {cambian} iniciativas cambian respecto a la clasificación anterior: `lectura_{ver}/CAMBIOS.md`. Las tres lecturas: `lectura_{ver}/lecturas.json` y `lectura_{ver}/<lector>/`.
- Sin efectos: {vac_v} antes, {vac_n} ahora.
{extra}"""
        # al repo; si algo falla (p. ej. build_data) se restaura todo lo tocado
        revision = os.path.join(base, "REVISION.md")
        tocado = sorted(glob.glob(os.path.join(base, "clas_*.json"))) + [revision, dst, os.path.join(ROOT, "site", "data", clave + ".json")]
        respaldo = respaldar(tocado, tmp)
        try:
            for f in glob.glob(f"{tmp}/consol/clas_*.json"):
                shutil.copy(f, base)
            shutil.rmtree(dst, ignore_errors=True)
            for L in "CDE":
                shutil.copytree(f"{tmp}/final/{L}", f"{dst}/{L}")
            for f in ("CAMBIOS.md", "lecturas.json"):
                shutil.copy(f"{tmp}/consol/{f}", dst)
            escribir_seccion(revision, f"## Reclasificación con la rúbrica {ver} (", seccion)
            salida = run("python3", "scripts/build_data.py", clave)
        except BaseException as e:
            restaurar(respaldo)
            sys.exit(f"{e}\nSe ha restaurado el estado anterior: no se ha cambiado ninguna clasificación.")
    print(salida.strip().splitlines()[-1][:120])
    print(json.dumps({"clave": clave, "n": len(ids), "unanimes": un, "contra": contra, "jaccard": jac, "exactas": exac,
                      "cambian": cambian, "vacias_antes": vac_v, "vacias_ahora": vac_n, "ronda2": n2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
