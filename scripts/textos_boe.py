"""Descarga del BOE el texto de los reales decretos-ley (130/) de una legislatura del Congreso.

Uso: python3 scripts/textos_boe.py <clave> [<id> …]     (sin ids: todos los 130/ de la legislatura)

Los reales decretos-ley no se publican en el BOCG: su texto oficial es el del BOE. El enlace se construye con el
identificador europeo de legislación (ELI) a partir del título («Real Decreto-ley N/AAAA, de D de mes…»):
  https://www.boe.es/eli/es/rdl/AAAA/MM/DD/N/dof/spa/html   (texto original publicado)
Escribe el texto plano en data/cache/<leg>/textos_boe/<id>.txt (hasta 150.000 caracteres) y no vuelve a descargar
lo que ya está en caché. Peticiones en secuencia con una pausa de 1,5 s; no hace ninguna petición a congreso.es.
scripts/lotes_reclasificacion.py usa este texto para los 130/ antes que el de su proyecto de ley.
"""
import html, json, os, re, ssl, sys, time
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MESES = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre "
                                         "noviembre diciembre".split())}
TITULO = re.compile(r"Real Decreto-ley (\d+)/(\d{4}), de (\d{1,2}) de (\w+)", re.I)
MAX, PAUSA = 150000, 1.5
try:  # algunos Python (p. ej. el de python.org en macOS) no traen certificados raíz
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = ssl.create_default_context()


def eli(titulo):
    m = TITULO.search(titulo)
    if not m or m.group(4).lower() not in MESES:
        return None
    n, a, d, mes = m.group(1), m.group(2), int(m.group(3)), MESES[m.group(4).lower()]
    return f"https://www.boe.es/eli/es/rdl/{a}/{mes:02d}/{d:02d}/{n}/dof/spa/html"


def texto(url):
    req = Request(url, headers={"User-Agent": "vota-bien (clasificación de leyes; https://www.votarbien.info)"})
    with urlopen(req, timeout=60, context=_SSL) as r:
        h = r.read().decode("utf-8", errors="replace")
    m = re.search(r'<div id="textoxslt">(.*)', h, re.S)
    s = re.sub(r"<(p|br|h\d|li|div)[^>]*>", "\n", m.group(1) if m else h)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()[:MAX]


def main():
    clave, ids = sys.argv[1], sys.argv[2:]
    leg = LEGISLATURAS[clave]["leg"].lower()
    items = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "data", "generado", clave, "items.json"), encoding="utf-8"))}
    ids = ids or sorted(i for i in items if i.startswith("130/"))
    out = os.path.join(ROOT, "data", "cache", leg, "textos_boe")
    os.makedirs(out, exist_ok=True)
    for i in ids:
        dest = os.path.join(out, i.replace("/", "_") + ".txt")
        if os.path.exists(dest):
            print(i, "en caché")
            continue
        url = eli(items[i]["titulo"]) if i in items else None
        if not url:
            print(i, "sin ELI (título no reconocido)")
            continue
        try:
            t = texto(url)
        except Exception as e:
            print(i, "error", e)
            continue
        finally:
            time.sleep(PAUSA)
        if len(t) < 500:
            print(i, "texto vacío o demasiado corto", url)
            continue
        open(dest, "w", encoding="utf-8").write(t)
        print(i, dest, len(t))


if __name__ == "__main__":
    main()
