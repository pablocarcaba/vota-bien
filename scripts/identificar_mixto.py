"""Propone el partido de las proposiciones de grupos que agrupan varios partidos (Mixto, Plural).

Uso: .venv/bin/python scripts/identificar_mixto.py congreso_xv

El Congreso publica como autor solo el grupo. El partido se deduce del texto de la proposición en el
BOCG (quién la firma o «a instancia de» qué diputados se presenta), cruzando los nombres con el mapeo
`nominal` de scripts/legislaturas.py. Necesita pypdf (pip install pypdf en .venv).

Con `--salida DIR` escribe partidos_mixto.json en DIR en vez de en data/clasificacion/<clave>/ (prueba sin tocar el repo).

Respeta el anti-bots de congreso.es (peticiones secuenciales, pausa de 2,5 s, para ante un 403) y guarda
todo en data/cache/<leg>/. Escribe data/clasificacion/<clave>/partidos_mixto.json con la propuesta y la
evidencia de cada iniciativa; integrarla en clas_*.json es un paso aparte y revisado.
"""
import glob, io, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS
import descargar_legislatura as D
from pypdf import PdfReader
from textos_bocg import fragmento

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GRUPOS_VARIOS = ("Grupo Parlamentario Mixto", "Grupo Parlamentario Plural")
norm = lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def texto_pdf(leg, pdf):
    dest = os.path.join(ROOT, "data", "cache", leg.lower(), "bocg", os.path.basename(pdf.split("?")[0]) + ".txt")
    if os.path.exists(dest):
        return open(dest, encoding="utf-8").read()
    raw = D.get(pdf if pdf.startswith("/") else "/" + pdf.split("congreso.es", 1)[-1].lstrip("/"), binary=True)
    t = "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(raw)).pages) if raw else ""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(t)
    return t


def texto_de(t, i):
    """Texto de la iniciativa `i` dentro del BOCG `t` (hasta 6000 caracteres).

    Usa textos_bocg.fragmento, que salta el sumario y corta en el expediente siguiente; `t.find(i)` caía
    en la línea del sumario. Si el expediente no figura (p. ej. textos del Senado), cae al inicio del boletín.
    """
    frag = fragmento(t, i)
    return (frag if frag is not None else t)[:6000]


def proponer(t, i, nombres, partidos):
    """(texto, votos): partidos que casan en la cabecera y la firma del texto de la iniciativa `i`."""
    frag = texto_de(t, i)
    cabeza = norm(frag[:2500])
    firma = norm(frag[-2500:] if len(frag) < 6000 else frag)
    votos = {}
    for k, p in nombres.items():
        pat = r"\b" + re.escape(k) + r"\b"  # palabra completa: «Micó» no debe casar con «económico»
        c = len(re.findall(pat, cabeza)) + len(re.findall(pat, firma))
        if c:
            votos[p] = votos.get(p, 0) + c
    for k, p in partidos.items():
        c = len(re.findall(r"\b" + re.escape(k) + r"\b", cabeza))
        if c:
            votos[p] = votos.get(p, 0) + 2 * c
    return frag, votos


def main():
    args = sys.argv[1:]
    salida = args.pop(args.index("--salida") + 1) if "--salida" in args else None
    if salida is not None:
        args.remove("--salida")
    clave = args[0]
    cfg = LEGISLATURAS[clave]
    leg = cfg["leg"]
    items = json.load(open(os.path.join(ROOT, "data", "generado", clave, "items.json"), encoding="utf-8"))
    cdir = os.path.join(ROOT, "data", "clasificacion", clave)
    clas = {x["id"]: x for p in glob.glob(os.path.join(cdir, "clas_*.json")) for x in json.load(open(p, encoding="utf-8"))}
    pend = [it for it in items if any(g in it["autor"] for g in GRUPOS_VARIOS) and not clas.get(it["id"], {}).get("partido")]
    # nombres a buscar: apellidos del mapeo nominal y nombres de partido
    nombres = {norm(k.split(",")[0]): p for k, p in cfg["nominal"].items()}
    partidos = {norm(p): p for p in set(cfg["nominal"].values())}
    out = {}
    for n, it in enumerate(pend, 1):
        f = D.cached(os.path.join(ROOT, "data", "cache", leg.lower(), "iniciativas", it["id"].replace("/", "_") + ".json"),
                     lambda: D.ficha(leg, it["id"]))
        bols = [b for b in (f or {}).get("BOLETINES", []) if b.get("pdf")]
        t = texto_pdf(leg, bols[0]["pdf"]) if bols else ""
        frag, votos = proponer(t, it["id"], nombres, partidos)
        m = re.search(r"(a (instancia|iniciativa|propuesta) de[^.]{0,200})", frag, re.I)
        out[it["id"]] = {"titulo": it["titulo"][:120], "propuesta": max(votos, key=votos.get) if votos else "",
                         "votos": votos, "evidencia": re.sub(r"\s+", " ", m.group(1))[:200] if m else ""}
        print(f"[{n}/{len(pend)}] {it['id']} -> {out[it['id']]['propuesta'] or '?'} {votos}", file=sys.stderr)
    dest = os.path.join(salida or cdir, "partidos_mixto.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Escrito", dest, len(out))


if __name__ == "__main__":
    main()
