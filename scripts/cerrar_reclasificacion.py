"""Paso 6 del proceso de reclasificación: cierra tras aplicar una o varias legislaturas.

Uso: python3 scripts/cerrar_reclasificacion.py [--rubrica v3] [--solo-alcance]

  1. Reescribe el span `alcance-v3` de site/template.html (metodología) según las carpetas
     data/clasificacion/<clave>/lectura_<versión>/ que existen: qué legislaturas están ya con la versión actual y
     cuáles siguen con la anterior. La versión sale de la cabecera de RUBRICA.md (--rubrica la fuerza).
     Con --solo-alcance se detiene aquí.
  2. Ejecuta scripts/prueba_sesgo.py --perfiles 2000 --guardar (escribe data/analisis/sesgo.json).
  3. Actualiza en site/template.html las cifras de la metodología (tabla del Parlamento Europeo y frases del Congreso)
     desde sesgo.json. Si una de esas frases ya no existe en la plantilla, falla y dice cuál: hay que
     sincronizar este script con el texto.
  4. Valida todas las clasificaciones (0 errores en todas), regenera la página (build_page.py) y pasa los tests.
No hace peticiones de red.

Flujo completo del proceso (detalle en scripts/lotes_reclasificacion.py):
  descargar los textos -> lotes -> tres lecturas independientes con RUBRICA.md y el prompt de
  data/clasificacion/PROMPT_LECTOR.md -> segunda ronda con más texto (--hueco) -> aplicar_reclasificacion.py -> ESTE script.
Descargas: congreso.es no admite peticiones en paralelo; una cada 2-3 s y parar ante un 403.
"""
import argparse, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import FUENTES, LEGISLATURAS
from aplicar_reclasificacion import version_rubrica

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SPAN = re.compile(r'<span id="alcance-v3">.*?</span>', re.S)


def run(*cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"Falló {' '.join(cmd)}\n{p.stdout}{p.stderr}")
    return p.stdout


def frase_alcance(root, ver, claves=None):
    claves = list(LEGISLATURAS if claves is None else claves)
    actuales = [k for k in claves if os.path.isdir(os.path.join(root, "data", "clasificacion", k, "lectura_" + ver))]
    antiguas = [k for k in claves if k not in actuales and os.path.exists(os.path.join(root, "site", "data", k + ".json"))]
    if not actuales:
        sys.exit(f"Ninguna legislatura tiene lectura_{ver}: aplica antes alguna reclasificación")
    nombre = lambda k: f"{FUENTES[LEGISLATURAS[k]['fuente']]} {LEGISLATURAS[k]['titulo'].split(' · ')[0]}"
    lista = lambda ks: ", ".join(nombre(k) for k in ks[:-1]) + (" y " if len(ks) > 1 else "") + nombre(ks[-1])
    previa = f"v{int(ver[1:]) - 1}" if re.fullmatch(r"v\d+", ver) else "la anterior"
    frase = f"Están clasificadas con la {ver}, por tres lecturas independientes: {lista(actuales)}."
    if antiguas:
        return frase + f" Siguen con la {previa}, a la espera de reclasificarse igual: {lista(antiguas)}."
    return frase + f" Todas las legislaturas están ya clasificadas con la {ver}."


def reescribir_alcance(html, frase):
    nuevo, n = SPAN.subn(lambda m: f'<span id="alcance-v3">{frase}</span>', html, count=1)
    if n != 1:
        sys.exit('No se encontró <span id="alcance-v3"> en site/template.html')
    return nuevo


def actualizar_cifras(html, sesgo):
    """Pone en la metodología las cifras de data/analisis/sesgo.json (`sesgo` = su clave «legislaturas»)."""
    f = lambda x: f"{x:.1f}".replace(".", ",")
    top = lambda k, t, n=1: sesgo[k][t]["partidos"][:n]
    nombre = {"Bildu": "EH Bildu"}
    pct = lambda x: f"{nombre.get(x['partido'], x['partido'])} · {f(x['primero_pct'])} %"
    sin_aplicar = []

    def sub(patron, repl):
        nonlocal html
        html, n = re.subn(patron, lambda m: repl, html, count=1)
        if n != 1:
            sin_aplicar.append(patron)

    for clave, leg in (("europarlamento_10", "10.ª · 2024–2029"), ("europarlamento_9", "9.ª · 2019–2024")):
        sub(rf'<tr><th scope="row">{re.escape(leg)}</th><td>[^<]*</td><td>[^<]*</td></tr>',
            f'<tr><th scope="row">{leg}</th><td>{pct(top(clave, "eco_con_ciud")[0])}</td>'
            f'<td>{pct(top(clave, "eco_sin_ciud")[0])}</td></tr>')
    a, b, c = top("congreso_xv", "eco_con_ciud", 3)
    sub(r"salen primeros [^.]*? en el [\d,]+ % de los perfiles, [^.]*? en el [\d,]+ % y [^.]*? en el [\d,]+ %\.",
        f"salen primeros {a['partido']} en el {f(a['primero_pct'])} % de los perfiles, {b['partido']} en el "
        f"{f(b['primero_pct'])} % y {c['partido']} en el {f(c['primero_pct'])} %.")
    xi = top("congreso_xi", "soc_con_ciud")[0]
    sub(r"en la XI, en leyes sociales, [^ ]+ sale primero en el [\d,]+ % de los perfiles",
        f"en la XI, en leyes sociales, {xi['partido']} sale primero en el {f(xi['primero_pct'])} % de los perfiles")
    if sin_aplicar:
        sys.exit("Frases de la metodología que ya no casan (sincroniza actualizar_cifras con la plantilla):\n  "
                 + "\n  ".join(sin_aplicar))
    return html


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cierra una reclasificación: metodología, sesgo, página y tests.")
    ap.add_argument("--rubrica", help="versión de la rúbrica (vN); por defecto, la de RUBRICA.md")
    ap.add_argument("--solo-alcance", action="store_true", help="solo reescribe la frase de alcance")
    a = ap.parse_args(argv)
    ver = version_rubrica(ROOT, a.rubrica)
    tpl = os.path.join(ROOT, "site", "template.html")
    frase = frase_alcance(ROOT, ver)
    html = reescribir_alcance(open(tpl, encoding="utf-8").read(), frase)
    print(frase)
    if a.solo_alcance:
        open(tpl, "w", encoding="utf-8").write(html)
        return
    run("python3", "scripts/prueba_sesgo.py", "--perfiles", "2000", "--guardar")
    sesgo = json.load(open(os.path.join(ROOT, "data", "analisis", "sesgo.json"), encoding="utf-8"))["legislaturas"]
    html = actualizar_cifras(html, sesgo)
    # la plantilla no se escribe hasta que las clasificaciones validan
    val = run("python3", "scripts/validar_clasificacion.py")
    if val.count(" 0 errores") != len(LEGISLATURAS):
        sys.exit("Validación con errores:\n" + val)
    open(tpl, "w", encoding="utf-8").write(html)
    run("python3", "scripts/build_page.py")
    t = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT, capture_output=True, text=True)
    if t.returncode:
        sys.exit("Tests en rojo:\n" + t.stderr[-2000:])
    print("tests OK,", t.stderr.strip().splitlines()[-3])


if __name__ == "__main__":
    main()
