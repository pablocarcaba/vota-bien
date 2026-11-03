"""Valida los ficheros de clasificación contra RUBRICA.md y la web.

Uso:
  python3 scripts/validar_clasificacion.py                 # valida data/clasificacion/clas_*.json
  python3 scripts/validar_clasificacion.py fichero.json …  # valida ficheros concretos (sin comprobar cobertura)

Comprueba: identificadores de colectivo válidos, valores ±1, tipo eco/soc, nota de 1 a 25 palabras,
partido permitido, ids existentes en items.json, sin duplicados, cobertura de todas las iniciativas
y que los colectivos coinciden con los que ofrece site/template.html.
"""
import glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

COLECTIVOS = {
    "ciud",
    "asal1", "asal2", "asal3", "asal4", "asal5", "asal6",
    "funA1", "funA2", "funB", "funC1", "funC2E",
    "pen1", "pen2", "pen3",
    "desPres", "desSub",
    "prop1", "prop2", "prop3", "prop4",
    "empAut", "empMicro", "empPeq", "empMed", "empGran",
    "secPrim", "secInd", "secCons", "secTrans", "secCom", "secFin", "secDig",
    "viv0", "viv1", "viv2", "inq", "hipot", "cons",
    "proSeg", "proSan", "proDoc",
    "hombres", "mujeres", "lgtbi", "jovenes", "adultos", "infancia", "mayores", "inmigrantes", "discapacidad",
    "victimas", "rural", "minorias", "estud", "pac", "depend", "pobreza",
}
PARTIDOS = {"", "Podemos", "BNG", "CC", "UPN", "Compromís"}


def main(paths):
    full = not paths
    paths = paths or sorted(glob.glob(os.path.join(ROOT, "data", "clasificacion", "clas_*.json")))
    items = {x["id"] for x in json.load(open(os.path.join(ROOT, "data", "generado", "items.json"), encoding="utf-8"))}
    errs, seen = [], set()
    for p in paths:
        for i, x in enumerate(json.load(open(p, encoding="utf-8"))):
            w = f"{os.path.basename(p)}[{i}] {x.get('id')}"
            if x.get("id") not in items:
                errs.append(f"{w}: id desconocido")
            if x.get("id") in seen:
                errs.append(f"{w}: id duplicado")
            seen.add(x.get("id"))
            if x.get("tipo") not in ("eco", "soc"):
                errs.append(f"{w}: tipo {x.get('tipo')!r}")
            imp = x.get("imp")
            if not isinstance(imp, dict):
                errs.append(f"{w}: imp no es objeto")
            else:
                for k, v in imp.items():
                    if k not in COLECTIVOS:
                        errs.append(f"{w}: colectivo desconocido {k!r}")
                    if v not in (1, -1):
                        errs.append(f"{w}: valor {v!r} en {k}")
            n = len((x.get("nota") or "").split())
            if not 1 <= n <= 25:
                errs.append(f"{w}: nota de {n} palabras")
            if x.get("partido", "") not in PARTIDOS:
                errs.append(f"{w}: partido {x.get('partido')!r}")
    if full:
        falta = items - seen
        if falta:
            errs.append(f"{len(falta)} iniciativas sin clasificar: {sorted(falta)[:5]}…")
        tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
        bloque = tpl[tpl.index("const CATS"):tpl.index("const LABEL")]
        web = set(re.findall(r"\['(\w+)','", bloque))
        if web != COLECTIVOS:
            errs.append(f"la web y el validador no coinciden: solo web {sorted(web - COLECTIVOS)}, "
                        f"solo validador {sorted(COLECTIVOS - web)}")
    for e in errs:
        print(e)
    print(f"{len(seen)} clasificaciones, {len(errs)} errores")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
