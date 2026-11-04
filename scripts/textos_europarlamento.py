"""Descarga el texto aprobado (en español) de procedimientos concretos del Parlamento Europeo para clasificarlos.

Uso: .venv/bin/python scripts/textos_europarlamento.py <clave> <ref> [<ref> …]
     (ref como en site/data: 2020/0310(COD))

Para cada procedimiento: API de datos abiertos del PE (procedures/<aaaa-nnnn>) -> último texto aprobado
(TA-…) -> adopted-texts/<TA> -> PDF oficial en español (distribution/…_es.pdf). Escribe el texto en
data/cache/<clave>/textos/<ref>.txt (hasta 40.000 caracteres) e imprime la ruta, o «sin texto».
Peticiones secuenciales con pausa de 1,5 s; para ante un 403 o 429. Necesita pypdf (.venv).
Fuente: datos abiertos del Parlamento Europeo (https://data.europarl.europa.eu), reutilización con atribución.
"""
import io, json, os, re, sys, time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from pypdf import PdfReader

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
API = "https://data.europarl.europa.eu/api/v2/"
DIST = "https://data.europarl.europa.eu/"
UA = {"User-Agent": "Mozilla/5.0 (proyecto ciudadano vota-bien; datos abiertos)", "Accept": "application/ld+json"}
PAUSA = 1.5
_ultima = [0.0]


def get(url, binario=False):
    espera = PAUSA - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    _ultima[0] = time.time()
    try:
        with urlopen(Request(url, headers=UA), timeout=60) as r:
            raw = r.read()
    except HTTPError as e:
        if e.code in (403, 429):
            sys.exit(f"\n{e.code} en {url}: el servidor limita las peticiones. Espera y relanza el mismo comando.")
        if e.code == 404:
            return None
        raise
    return raw if binario else json.loads(raw)


def texto(ref):
    pid = re.match(r"(\d{4})/(\d{4})", ref)
    if not pid:
        return ""
    d = get(f"{API}procedures/{pid.group(1)}-{pid.group(2)}?format=application%2Fld%2Bjson")
    x = ((d or {}).get("data") or [{}])[0]
    tas = sorted(i.rsplit("/", 1)[-1] for i in x.get("created_a_realization_of") or [] if "/TA-" in i)
    if not tas:
        return ""
    a = get(f"{API}adopted-texts/{tas[-1]}?format=application%2Fld%2Bjson&language=es")
    y = ((a or {}).get("data") or [{}])[0]
    for e in y.get("is_realized_by") or []:
        if not e.get("id", "").endswith("/es"):
            continue
        for m in e.get("is_embodied_by") or []:
            if str(m.get("is_exemplified_by", "")).endswith(".pdf"):
                pdf = get(DIST + m["is_exemplified_by"], binario=True)
                if pdf:
                    return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(pdf)).pages)
    return ""


def main():
    clave, refs = sys.argv[1], sys.argv[2:]
    out = os.path.join(ROOT, "data", "cache", clave, "textos")
    os.makedirs(out, exist_ok=True)
    for ref in refs:
        dest = os.path.join(out, re.sub(r"[^\w]", "_", ref) + ".txt")
        if os.path.exists(dest):
            print(ref, dest, "(caché)")
            continue
        t = texto(ref)
        if not t:
            print(ref, "sin texto")
            continue
        open(dest, "w", encoding="utf-8").write(t[:40000])
        print(ref, dest, len(t))


if __name__ == "__main__":
    main()
