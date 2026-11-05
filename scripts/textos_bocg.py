"""Descarga el texto de iniciativas concretas (primer BOCG de su ficha) para revisar su clasificación.

Uso: .venv/bin/python scripts/textos_bocg.py congreso_xv 121/000097 124/000001 …
     .venv/bin/python scripts/textos_bocg.py --auditar   (revisa sin red todos los textos en caché)

Respeta el anti-bots de congreso.es (secuencial, pausa de 2,5 s, para ante un 403) y cachea en
data/cache/<leg>/. Escribe cada texto en data/cache/<leg>/textos/<id>.txt (solo el fragmento de esa
iniciativa, hasta 40.000 caracteres) e imprime la ruta, o «sin BOCG» si la ficha no tiene boletín.
Los reales decretos-ley (130/) no se publican en el BOCG: usa su proyecto de ley (121/) si se tramitó
como tal, o el BOE.
"""
import glob, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS
import descargar_legislatura as D

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
norm = lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

MAX = 40000
# en el sumario de un boletín cada entrada acaba en puntos de relleno y el número de página
SUMARIO = re.compile(r"\.{6,}\s*\d+")
OTRO_EXPEDIENTE = re.compile(r"^\d{3}/\d{6}\s*$", re.M)


def _patron_id(i):
    a, b = i.split("/")
    # el número de página a veces se pega al expediente al extraer el PDF («69130/000022»)
    return re.compile(r"(?:(?<![\d/])|^\d{1,4})(?P<id>" + a + r"\s*/\s*" + b + r"(?!\d))", re.M)


def fragmento(t, i):
    """Fragmento de `t` (texto de un BOCG) que corresponde a la iniciativa `i`, o None si no está.

    La primera aparición del expediente suele ser su línea del sumario (que lleva puntos de relleno y
    número de página): tomar desde ahí devuelve el sumario y las iniciativas vecinas. Se salta el
    sumario y se prefiere la cabecera del expediente (solo en su línea); el texto acaba donde
    empieza el expediente siguiente.
    """
    cand = [m for m in _patron_id(i).finditer(t) if not SUMARIO.search(t[m.end():m.end() + 500])]
    # (m.start("id") es el inicio del expediente, sin el número de página pegado)
    if not cand:
        return None
    cab = [m for m in cand if re.match(r"[ \t]*(\n|$)", t[m.end():]) and (m.start() == 0 or t[m.start() - 1] == "\n")]
    k = (cab or cand)[0].start("id")
    frag = t[k:k + MAX]
    sig = next((m for m in OTRO_EXPEDIENTE.finditer(frag, len(i) + 1) if m.group().strip() != i), None)
    return frag[:sig.start()] if sig else frag


def palabras(s):
    return {w for w in re.findall(r"[a-z]{5,}", norm(s))}


def texto_corresponde(frag, i, objeto, umbral=0.4):
    """(ok, motivo): el texto no empieza en un sumario y es el de su iniciativa.

    Es suya si el título (OBJETO de la ficha) está presente en las primeras líneas (umbral del 40 %
    de sus palabras de 5+ letras, para tolerar erratas y paráfrasis) y, además, aparece su expediente
    o el título casa casi entero (60 %: los textos del Senado no llevan el número 124/ del Congreso).
    """
    if not frag.strip():
        return False, "vacío"
    if SUMARIO.search(frag[:700]):
        return False, "empieza en un sumario"
    con_id = bool(_patron_id(i).search(frag))
    pw = palabras(objeto or "")
    if not pw:
        return (True, "") if con_id else (False, "no contiene su expediente")
    r = len(pw & palabras(frag[:6000])) / len(pw)
    if r < umbral:
        return False, f"título poco presente ({r:.0%})"
    if not con_id and r < 0.6:
        return False, f"no contiene su expediente (título {r:.0%})"
    return True, ""


def _dirs_textos():
    """Cachés de textos del Congreso (x, xi, …); los de europarlamento_* no son BOCG."""
    return sorted(d for d in glob.glob(os.path.join(ROOT, "data", "cache", "*", "textos"))
                  if re.fullmatch(r"[xiv]+", os.path.basename(os.path.dirname(d))))


def auditar():
    """Revisa todos los textos en caché (sin red). Devuelve la lista de sospechosos."""
    sosp = []
    for d in _dirs_textos():
        leg = os.path.basename(os.path.dirname(d))
        for f in sorted(glob.glob(os.path.join(d, "*.txt"))):
            i = os.path.basename(f)[:-4].replace("_", "/")
            ficha = os.path.join(ROOT, "data", "cache", leg, "iniciativas", i.replace("/", "_") + ".json")
            obj = json.load(open(ficha, encoding="utf-8")).get("OBJETO", "") if os.path.exists(ficha) else ""
            frag = open(f, encoding="utf-8").read()
            ok, motivo = texto_corresponde(frag, i, obj)
            if not ok:
                sosp.append((i, leg, motivo, re.sub(r"\s+", " ", frag[:160])))
    return sosp


def main():
    if sys.argv[1:2] == ["--auditar"]:
        n = sum(len(glob.glob(os.path.join(d, "*.txt"))) for d in _dirs_textos())
        sosp = auditar()
        print(f"{n} textos revisados, {len(sosp)} sospechosos")
        for i, leg, motivo, ext in sosp:
            print(f"{i}\t{leg}\t{motivo}\t{ext}")
        return
    from identificar_mixto import texto_pdf  # aparte: necesita pypdf, y las funciones de arriba no
    clave, ids = sys.argv[1], sys.argv[2:]
    leg = LEGISLATURAS[clave]["leg"]
    out = os.path.join(ROOT, "data", "cache", leg.lower(), "textos")
    os.makedirs(out, exist_ok=True)
    for i in ids:
        f = D.cached(os.path.join(ROOT, "data", "cache", leg.lower(), "iniciativas", i.replace("/", "_") + ".json"),
                     lambda: D.ficha(leg, i))
        bols = [b for b in (f or {}).get("BOLETINES", []) if b.get("pdf")]
        if not bols:
            print(i, "sin BOCG")
            continue
        frag = None
        textos = [texto_pdf(leg, b["pdf"]) for b in bols[:1]]
        for n, b in enumerate(bols):  # el primer boletín no siempre es el que publica la iniciativa
            if n >= len(textos):
                textos.append(texto_pdf(leg, b["pdf"]))
            frag = fragmento(textos[n], i)
            if frag and texto_corresponde(frag, i, f.get("OBJETO", ""))[0]:
                break
            frag = None
        if not frag:  # p. ej. proposiciones del Senado: el boletín no lleva el número 124/ del Congreso
            frag = next((t[:MAX] for t in textos if texto_corresponde(t[:MAX], i, f.get("OBJETO", ""))[0]), None)
        if not frag:
            print(i, "expediente no localizado en sus boletines; no se escribe texto")
            continue
        dest = os.path.join(out, i.replace("/", "_") + ".txt")
        open(dest, "w", encoding="utf-8").write(frag)
        print(i, dest, len(frag))


if __name__ == "__main__":
    main()
