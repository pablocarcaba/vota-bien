"""Lotes de clasificación con un extracto del texto oficial de cada iniciativa.

Uso: python3 scripts/preparar_lotes_texto.py <clave> <dir_salida> [--chars 2500] [--tam 108]

Toma los lotes de data/clasificacion/<clave>/lotes/ (id, tipo, título, autor) y añade a cada iniciativa
`texto`: un extracto del primer BOCG descargado con textos_bocg.py (data/cache/<leg>/textos/<id>.txt),
empezando por la exposición de motivos o el preámbulo si se encuentran, que es donde la ley explica qué
hace. Si no hay texto (reales decretos-ley, iniciativas sin boletín), `texto` va vacío y el clasificador
se ciñe al título, como hasta ahora. No hace peticiones de red.
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INICIO = re.compile(r"EXPOSICI[ÓO]N\s+DE\s+MOTIVOS|PRE[ÁA]MBULO|Exposici[óo]n\s+de\s+motivos|Pre[áa]mbulo")


def extracto(txt, n):
    m = INICIO.search(txt)
    t = txt[m.start():] if m else txt
    t = re.sub(r"[ \t]+", " ", re.sub(r"-\n(?=\w)", "", t))
    t = re.sub(r"\n{2,}", "\n", t).strip()
    return t[:n]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    clave, out = args[0], args[1]
    n = int(sys.argv[sys.argv.index("--chars") + 1]) if "--chars" in sys.argv else 2500
    leg = LEGISLATURAS[clave]["leg"].lower()
    textos = os.path.join(ROOT, "data", "cache", leg, "textos")
    os.makedirs(out, exist_ok=True)
    con = sin = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "clasificacion", clave, "lotes", "*.json"))):
        lote = json.load(open(f, encoding="utf-8"))
        for it in lote:
            p = os.path.join(textos, it["id"].replace("/", "_") + ".txt")
            it["texto"] = extracto(open(p, encoding="utf-8").read(), n) if os.path.exists(p) else ""
            con += bool(it["texto"])
            sin += not it["texto"]
        json.dump(lote, open(os.path.join(out, os.path.basename(f)), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{con} con texto, {sin} sin texto ->", out)


if __name__ == "__main__":
    main()
