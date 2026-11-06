"""Prueba de sesgo: ¿algún partido sale arriba para casi todo el mundo?

Uso: python3 scripts/prueba_sesgo.py [--perfiles 2000] [--semilla 2026] [--guardar]

Calcula el ranking de la web para muchos perfiles —unos arquetipos con nombre (asalariado medio,
pensionista, autónomo…) y una muestra aleatoria reproducible— en cada legislatura y pestaña, con
«Ciudadanía general» activada (como viene en la web) y desactivada. Reproduce exactamente el cálculo
de site/template.html (impactOf, voteColor, evidence, computeRank con la prudencia K); los tests
comprueban que no se separan.

Mide, por partido: en qué porcentaje de perfiles queda primero (los empates se reparten), su puesto
medio y su nota media. Y, por pestaña, cuánto se separa el primero: el margen mediano entre el 1.º y el 2.º y en qué
porcentaje de perfiles hay empate técnico en cabeza (el 2.º, o 2 o más partidos además del primero, a EMPATE puntos
o menos), como marca la web. Una herramienta neutral debería dar primeros puestos repartidos según el
perfil; si un partido gana para casi cualquier perfil, la clasificación o el método empujan hacia él.
El resultado se publica tal cual salga.

Con --guardar escribe data/analisis/sesgo.json y data/analisis/SESGO.md.
"""
import json, math, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# --- cálculo de la web (site/template.html) ---
PESO = {1: 1, 2: 3, 3: 9}
K = 9
# empate técnico: a esta distancia o menos del primero (en puntos de nota) la diferencia es demasiado pequeña para ordenarlos (EMPATE en la web)
EMPATE = 3
FUERZA = {"Votación final": 1, "Convalidación": 1, "Toma en consideración": 0.5, "Enmienda a la totalidad": 0.5}
IMPLICA = {"hij1": ["infancia"], "hij2": ["infancia"], "hij3": ["infancia"], "cuid": ["depend"]}
SIN_PAREJA, CON_HIJOS = {"civSol", "civSep", "civViu"}, {"hij1", "hij2", "hij3"}
# «No lo sé» en el tramo de IRPF (asalNs): asalariado sin tramo concreto. Le aplican las leyes que afectan a NS_MIN tramos
# o más, con el signo de su suma; no las que afectan solo a 1 o 2 (impNs en la web)
TRAMOS, NS_MIN = ["asal1", "asal2", "asal3", "asal4", "asal5", "asal6"], 3
# fracción de asalariados (y funcionarios) de la muestra aleatoria que responden «No lo sé» en el tramo
P_NS = 0.25


def js_round(x):
    return math.floor(x + 0.5)


def rasgos(sel):
    r = set(sel)
    for k in sel:
        r.update(IMPLICA.get(k, []))
    if sel & SIN_PAREJA and sel & CON_HIJOS:
        r.add("monop")
    return r


def imp_ns(it):
    v = [it["imp"][t] for t in TRAMOS if it["imp"].get(t)]
    if len(v) < NS_MIN:
        return 0
    s = sum(1 if x > 0 else -1 for x in v)
    return (s > 0) - (s < 0)


def imp_de(it, k):
    return imp_ns(it) if k == "asalNs" else it["imp"].get(k)


def signo_imp(imp, R):
    it = {"imp": imp}
    p = n = False
    for k in R:
        v = imp_de(it, k)
        if v and v > 0:
            p = True
        elif v and v < 0:
            n = True
    return 0 if p and n else 1 if p else -1 if n else None


def efecto(it, R):
    """(c, q, peso) como efecto() en la web: en una ley ómnibus (m), saldo de las medidas que afectan, ponderado."""
    if not it.get("m"):
        s = signo_imp(it["imp"], R)
        return ("neu" if s is None else "mix" if s == 0 else "pos" if s > 0 else "neg"), (1 if s else 0), it.get("w")
    num = den = 0
    w = 0
    for m in it["m"]:
        s = signo_imp(m["imp"], R)
        if s is not None:
            num += s * PESO[m["w"]]
            den += PESO[m["w"]]
            w = max(w, m["w"])
    if not den:
        return "neu", 0, it.get("w")
    net = num / den
    return ("mix" if abs(net) < 1e-9 else "pos" if net > 0 else "neg"), abs(net), w


def impact_of(it, R):
    return efecto(it, R)[0]


def vote_color(imp, v):
    if not v:
        return None
    if imp == "mix":
        return "mix"
    if imp == "neu" or v == "a":
        return "neu"
    if imp == "pos":
        return "pos" if v == "s" else "neg"
    return "pos" if v == "n" else "neg"


COMUN = {"ciud", "cons"}
F_COMUN = 0.5


def solo_comun(it, R):
    imps = [m["imp"] for m in it["m"]] if it.get("m") else [it["imp"]]
    af = [k for imp in imps for k in R if imp_de({"imp": imp}, k)]
    return bool(af) and all(k in COMUN for k in af)


def fkey(it):
    d = (it.get("vd") or it.get("f") or "").split("/")
    return int(d[2] + d[1].zfill(2) + d[0].zfill(2)) if len(d) == 3 else 0


VIA_RANGO = {"voto": 2, "aus": 1, "pres": 0}


def compute_rank(items, parties, R, tab):
    U = [it for it in items if it["tp"] == tab]
    efs = {id(it): efecto(it, R) for it in U}
    imps = [(it, efs[id(it)][0]) for it in U]
    # leyes que solo afectan por los rasgos comunes (ciud, cons): cuentan la mitad (F_COMUN en la web)
    comun = {id(it): F_COMUN if solo_comun(it, R) else 1 for it in U}
    out = []
    for p in parties:
        ev = []  # (it, c, w, via)
        for it, imp in imps:
            if imp == "neu":
                continue
            v = (it.get("v") or {}).get(p)
            if v:
                c = vote_color(imp, v)
                if c == "neu":
                    continue
                f, via = FUERZA.get(it.get("vk"), 0.5), "voto"
            elif it.get("v") and p in (it.get("nv") or []):
                # ausencia con escaño: cuenta en el total, no suma ni resta (como en la web)
                c, f, via = "aus", FUERZA.get(it.get("vk"), 0.5), "aus"
            elif p in it["a"]:
                c, f, via = imp, 0.25, "pres"
            else:
                continue
            _, q, wl = efs[id(it)]
            ev.append((it, c, PESO.get(wl, 1) * f * comun[id(it)], via, q if c in ("pos", "neg") else 1))
        # mismo contenido (campo g): una sola vez por partido, con la mejor prueba (como evidencias() en la web)
        best = {}
        for e in ev:
            g = e[0].get("g")
            if g:
                k = (VIA_RANGO[e[3]], e[2], fkey(e[0]))
                if g not in best or k > best[g][0]:
                    best[g] = (k, e)
        S = W = 0.0
        rel = 0
        for e in ev:
            it, c, w, _, q = e
            if it.get("g") and best[it["g"]][1] is not e:
                continue
            rel += 1
            W += w
            S += w * q if c == "pos" else -w * q if c == "neg" else 0
        if rel:
            out.append({"k": p, "s": js_round(S / (W + K) * 100), "rel": rel})
    out.sort(key=lambda r: (-r["s"], -r["rel"]))
    return out


def cabeza(rank):
    """(margen entre el 1.º y el 2.º, cuántos partidos además del primero quedan a EMPATE puntos o menos) de un
    ranking ya ordenado; (None, 0) si hay menos de dos partidos."""
    if len(rank) < 2:
        return None, 0
    return rank[0]["s"] - rank[1]["s"], sum(1 for r in rank[1:] if rank[0]["s"] - r["s"] <= EMPATE)


def resumen_cabeza(cabezas, validos):
    """Margen mediano y porcentajes de empate técnico sobre los perfiles con resultado (`validos`)."""
    margenes = [m for m, _ in cabezas if m is not None]
    pct = lambda n: round(100 * n / validos, 1) if validos else 0
    m = statistics.median(margenes) if margenes else None
    return {"margen_mediano": int(m) if m is not None and m == int(m) else m,
            "empate_tecnico_pct": pct(sum(1 for _, n in cabezas if n >= 1)),
            "empate_varios_pct": pct(sum(1 for _, n in cabezas if n >= 2))}


# --- perfiles ---
UNO = {  # categorías de una sola opción (como en la web)
    "edad": ["jovenes", "adultos", "mayores"],
    "civ": ["civSol", "civPar", "civSep", "civViu"],
    "hij": ["hij0", "hij1", "hij2", "hij3"],
    "vivn": ["viv0", "viv1", "viv2"],
    "prop": ["prop1", "prop2", "prop3", "prop4"],
    "sexo": ["hombres", "mujeres"],
}
TRABAJO = {  # situación laboral principal (una)
    "asal": ["asal1", "asal2", "asal3", "asal4", "asal5", "asal6"],
    "fun": ["funA1", "funA2", "funB", "funC1", "funC2E"],
    "pen": ["pen1", "pen2", "pen3"],
    "des": ["desPres", "desSub"],
    "emp": ["empAut", "empMicro", "empPeq", "empMed", "empGran"],
}
VARIOS = {
    "vivs": ["hipot", "inq", "casero"],
    "pro": ["proSeg", "proSan", "proDoc"],
    "sec": ["secPrim", "secInd", "secCons", "secTrans", "secCom", "secFin", "secDig", "secSoc"],
    "soc": ["estud", "pac", "depend", "discapacidad", "famDisc", "inmigrantes", "minorias", "rural", "victimas", "pobreza"],
    "otros": ["cuid", "lgtbi"],
}

ARQUETIPOS = {
    "Asalariado medio con hipoteca e hijos": ["asal3", "viv1", "hipot", "civPar", "hij2", "adultos"],
    "Joven de alquiler": ["asal2", "inq", "jovenes", "civSol", "hij0", "viv0"],
    "Pensionista con casa propia": ["pen2", "mayores", "viv1", "civPar"],
    "Pensionista con pensión baja": ["pen1", "mayores", "viv1", "civViu"],
    "Autónomo del comercio": ["empAut", "secCom", "viv1", "hipot", "adultos"],
    "Empresario de pyme industrial": ["empPeq", "secInd", "viv2", "prop2", "adultos"],
    "Funcionario docente": ["funA2", "asal3", "proDoc", "viv1", "hipot", "adultos"],
    "Policía o guardia civil": ["funC1", "asal2", "proSeg", "viv1", "hipot", "adultos"],
    "Sanitario asalariado": ["asal3", "proSan", "viv1", "adultos"],
    "Familia numerosa": ["asal3", "hij3", "civPar", "viv1", "hipot", "adultos"],
    "Rentas altas con patrimonio": ["asal5", "prop3", "viv2", "adultos"],
    "Gran patrimonio y gran empresa": ["empGran", "prop4", "viv2", "adultos"],
    "Parado con subsidio": ["desSub", "inq", "pobreza", "adultos"],
    "Agricultor en el medio rural": ["empAut", "secPrim", "rural", "viv1", "adultos"],
    "Madre sola con hijo": ["mujeres", "civSep", "hij1", "asal2", "inq", "adultos"],
    "Estudiante": ["estud", "jovenes", "viv0", "civSol"],
    "Mayor dependiente": ["pen1", "mayores", "depend", "viv1"],
    "Familia con un hijo con discapacidad": ["asal3", "hij1", "famDisc", "civPar", "viv1", "hipot", "adultos"],
    "Casero con varias viviendas": ["asal4", "viv2", "casero", "prop2", "adultos"],
    "Transportista autónomo": ["empAut", "secTrans", "viv1", "adultos"],
    "Asalariado de salario mínimo": ["asal1", "inq", "adultos"],
}


def aleatorio(rng):
    """Un perfil como los que permite el formulario de la web: edad e hijos siempre; una o dos
    situaciones laborales con sus subpreguntas (el funcionario también marca tramo; el sector solo
    con negocio); vivienda y ahorros siempre; el resto opcional. Asalariados y funcionarios responden
    «No lo sé» (asalNs) en el tramo de IRPF con probabilidad P_NS."""
    sel = {rng.choice(UNO["edad"]), rng.choice(UNO["hij"]), rng.choice(UNO["prop"])}
    for k in ("civ", "sexo"):
        if rng.random() < 0.6:
            sel.add(rng.choice(UNO[k]))
    sel.add(rng.choice(UNO["vivn"]))
    if "viv0" not in sel and rng.random() < 0.4:
        sel.add("hipot")
    if rng.random() < 0.3:
        sel.add("inq")
    # un solo tramo por perfil, como en la web (pregunta de una opción, con «No lo sé» como alternativa)
    elegido = []

    def tramo():
        if not elegido:
            elegido.append("asalNs" if rng.random() < P_NS else rng.choice(TRABAJO["asal"]))
        return elegido[0]

    for t in rng.sample(list(TRABAJO), 2 if rng.random() < 0.15 else 1):
        sel.add(tramo() if t == "asal" else rng.choice(TRABAJO[t]))
        if t == "fun":
            sel.add(tramo())
        if t in ("asal", "fun") and rng.random() < 0.15:
            sel.add(rng.choice(VARIOS["pro"]))
        if t == "emp":
            sel.add(rng.choice(VARIOS["sec"]))
    for o in VARIOS["soc"] + ["cuid", "lgtbi"]:
        if rng.random() < 0.08:
            sel.add(o)
    return sel


def main():
    args = sys.argv[1:]
    n = int(args[args.index("--perfiles") + 1]) if "--perfiles" in args else 2000
    semilla = int(args[args.index("--semilla") + 1]) if "--semilla" in args else 2026
    guardar = "--guardar" in args
    rng = random.Random(semilla)
    muestra = [aleatorio(rng) for _ in range(n)]
    res = {"semilla": semilla, "perfiles_aleatorios": n, "K": K, "legislaturas": {}}
    for clave in LEGISLATURAS:
        f = os.path.join(ROOT, "site", "data", clave + ".json")
        if not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        items, parties = d["items"], d["meta"]["parties"]
        res["legislaturas"][clave] = {"titulo": LEGISLATURAS[clave]["titulo"], "fuente": d["meta"]["fuente_txt"]}
        for tab in ("eco", "soc"):
            for ciud in (True, False):
                primeros = {p: 0.0 for p in parties}
                puesto = {p: [] for p in parties}
                nota = {p: [] for p in parties}
                validos = 0
                cabezas = []
                for sel in muestra:
                    s = set(sel) | {"cons"} | ({"ciud"} if ciud else set())
                    rank = compute_rank(items, parties, rasgos(s), tab)
                    rank = [r for r in rank if r["rel"] >= 3]  # como «ocultar pocos datos»: evita primeros con 1-2 leyes
                    if not rank:
                        continue
                    validos += 1
                    cabezas.append(cabeza(rank))
                    top = [r for r in rank if r["s"] == rank[0]["s"]]
                    for r in top:
                        primeros[r["k"]] += 1 / len(top)
                    for i, r in enumerate(rank):
                        puesto[r["k"]].append(i + 1)
                        nota[r["k"]].append(r["s"])
                tabla = sorted(
                    ({"partido": p, "primero_pct": round(100 * primeros[p] / validos, 1) if validos else 0,
                      "puesto_medio": round(sum(puesto[p]) / len(puesto[p]), 1) if puesto[p] else None,
                      "nota_media": round(sum(nota[p]) / len(nota[p])) if nota[p] else None,
                      "perfiles": len(puesto[p])} for p in parties if puesto[p]),
                    key=lambda x: -x["primero_pct"])
                arq = {}
                for nombre, rasg in ARQUETIPOS.items():
                    s = set(rasg) | {"cons"} | ({"ciud"} if ciud else set())
                    rank = [r for r in compute_rank(items, parties, rasgos(s), tab) if r["rel"] >= 3]
                    arq[nombre] = [f"{r['k']} {r['s']:+d}" for r in rank[:3]]
                res["legislaturas"][clave][f"{tab}_{'con' if ciud else 'sin'}_ciud"] = {
                    "perfiles_con_resultado": validos, **resumen_cabeza(cabezas, validos), "partidos": tabla,
                    "arquetipos_top3": arq}
    print(json.dumps({k: {t: {"primeros": v[t]["partidos"][:3], "margen_mediano": v[t]["margen_mediano"],
                              "empate_tecnico_pct": v[t]["empate_tecnico_pct"], "empate_varios_pct": v[t]["empate_varios_pct"]}
                          for t in v if t.endswith("_ciud")} for k, v in res["legislaturas"].items()},
                     ensure_ascii=False, indent=1))
    if guardar:
        out = os.path.join(ROOT, "data", "analisis")
        os.makedirs(out, exist_ok=True)
        json.dump(res, open(os.path.join(out, "sesgo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        with open(os.path.join(out, "SESGO.md"), "w", encoding="utf-8") as fh:
            fh.write("# Prueba de sesgo\n\n")
            fh.write(f"Generado por `scripts/prueba_sesgo.py` (semilla {semilla}, {n} perfiles aleatorios y "
                     f"{len(ARQUETIPOS)} arquetipos, prudencia K = {K}). Mismo cálculo que la web; solo se cuentan partidos "
                     "con 3 o más iniciativas que afecten al perfil. «Primero» reparte los empates. "
                     f"En la muestra aleatoria, el {P_NS * 100:.0f} % de las personas asalariadas y del sector público responde «No lo sé» "
                     "en el tramo de IRPF.\n\n"
                     "Una herramienta neutral debería dar el primer puesto a partidos distintos según el perfil. Si uno gana "
                     "para casi cualquier perfil, la clasificación o el método empujan hacia él. Se publica tal cual sale.\n\n"
                     f"Salir primero puede ser un empate técnico: si el 2.º queda a {EMPATE} puntos o menos del 1.º, la diferencia "
                     "es demasiado pequeña para ordenarlos y la web los agrupa como «Empatado en cabeza». Bajo cada tabla, el margen mediano entre el 1.º y el 2.º "
                     f"(en puntos de nota, de −100 a +100) y el porcentaje de perfiles con empate técnico en cabeza: con el 2.º a "
                     f"{EMPATE} puntos o menos, y con 2 o más partidos, además del primero, a esa distancia.\n")
            for clave, v in res["legislaturas"].items():
                fh.write(f"\n## {v['fuente']} · {v['titulo']}\n")
                for t, nombre in (("eco", "Leyes económicas"), ("soc", "Leyes sociales")):
                    for c in ("con", "sin"):
                        r = v[f"{t}_{c}_ciud"]
                        fh.write(f"\n### {nombre} · {c} «Ciudadanía general»\n\n| Partido | Primero en | Puesto medio | Nota media |\n|---|---:|---:|---:|\n")
                        for x in r["partidos"]:
                            fh.write(f"| {x['partido']} | {x['primero_pct']} % | {x['puesto_medio']} | {x['nota_media']:+d} |\n")
                        if r["margen_mediano"] is not None:
                            fh.write(f"\nMargen mediano entre el 1.º y el 2.º: {r['margen_mediano']:g} puntos. Empate técnico en "
                                     f"cabeza (2.º a {EMPATE} puntos o menos): {r['empate_tecnico_pct']} % de los perfiles; con 2 o "
                                     f"más partidos además del primero: {r['empate_varios_pct']} %.\n")
                        fh.write("\n<details><summary>Arquetipos (tres primeros)</summary>\n\n")
                        for a, top in r["arquetipos_top3"].items():
                            fh.write(f"- {a}: {', '.join(top) or 'sin resultado'}\n")
                        fh.write("\n</details>\n")
        print("Guardado en", out)


if __name__ == "__main__":
    main()
