"""Prepara lotes de iniciativas sin clasificar para una legislatura.

Uso: python3 scripts/preparar_lotes.py congreso_xiv [--tam 100]

Escribe data/clasificacion/<clave>/lotes/lote_NN.json con las iniciativas que aún no están en ningún
clas_*.json. Cada lote se clasifica siguiendo data/clasificacion/INSTRUCCIONES.md y RUBRICA.md, y el
resultado se integra con integrar_clasificacion.py.

Los reales decretos-ley que luego se tramitan como proyecto de ley son la misma norma: se ponen en el
mismo lote para que se clasifiquen igual (y integrar_clasificacion.py los armoniza igualmente).
"""
import argparse, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clave")
    ap.add_argument("--tam", type=int, default=100)
    a = ap.parse_args()
    items = json.load(open(os.path.join(ROOT, "data", "generado", a.clave, "items.json"), encoding="utf-8"))
    cdir = os.path.join(ROOT, "data", "clasificacion", a.clave)
    hechas = {x["id"] for p in glob.glob(os.path.join(cdir, "clas_*.json")) for x in json.load(open(p, encoding="utf-8"))}
    pend = [it for it in items if it["id"] not in hechas]
    # agrupa RDL y su proyecto de ley (mismo número de RDL en el título) para que vayan juntos
    rdl = lambda t: (re.search(r"Real Decreto-ley (\d+/\d{4})", t) or [None, None])[1]
    pend.sort(key=lambda it: (rdl(it["titulo"]) or "~", it["id"]))
    os.makedirs(os.path.join(cdir, "lotes"), exist_ok=True)
    n0 = len(glob.glob(os.path.join(cdir, "lotes", "lote_*.json")))
    lotes = [pend[i:i + a.tam] for i in range(0, len(pend), a.tam)]
    for i, lote in enumerate(lotes):
        p = os.path.join(cdir, "lotes", f"lote_{n0 + i:02d}.json")
        json.dump([{"id": it["id"], "tipo": it["tipo_ini"], "titulo": it["titulo"], "autor": it["autor"]} for it in lote],
                  open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(p, len(lote))
    print(f"{len(pend)} iniciativas pendientes en {len(lotes)} lotes ({len(hechas)} ya clasificadas)")


if __name__ == "__main__":
    main()
