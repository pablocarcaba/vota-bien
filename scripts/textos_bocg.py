"""Descarga el texto de iniciativas concretas (primer BOCG de su ficha) para revisar su clasificación.

Uso: .venv/bin/python scripts/textos_bocg.py congreso_xv 121/000097 124/000001 …

Respeta el anti-bots de congreso.es (secuencial, pausa de 2,5 s, para ante un 403) y cachea en
data/cache/<leg>/. Escribe cada texto en data/cache/<leg>/textos/<id>.txt (solo el fragmento de esa
iniciativa, hasta 40.000 caracteres) e imprime la ruta, o «sin BOCG» si la ficha no tiene boletín.
Los reales decretos-ley (130/) no se publican en el BOCG: usa su proyecto de ley (121/) si se tramitó
como tal, o el BOE.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS
import descargar_legislatura as D
from identificar_mixto import texto_pdf, ROOT


def main():
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
        t = texto_pdf(leg, bols[0]["pdf"])
        k = t.find(i)
        frag = t[k:k + 40000] if k >= 0 else t[:40000]
        dest = os.path.join(out, i.replace("/", "_") + ".txt")
        open(dest, "w", encoding="utf-8").write(frag)
        print(i, dest, len(frag))


if __name__ == "__main__":
    main()
