"""items + clasificación + votaciones -> site/data/<clave>.json (dataset que consume la web).

Uso: python3 scripts/build_data.py congreso_xv
"""
import json, re, collections, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legislaturas import FUENTES, LEGISLATURAS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CLAVE = sys.argv[1] if len(sys.argv) > 1 else "congreso_xv"
CFG = LEGISLATURAS[CLAVE]
D = os.path.join(ROOT, "data")
raw = json.load(open(os.path.join(D, "fuente", CLAVE + ".json"), encoding="utf-8"))
items = json.load(open(os.path.join(D, "generado", CLAVE, "items.json"), encoding="utf-8"))
CLAS_DIR = os.path.join(D, "clasificacion", CLAVE)
clas = {x["id"]: x for f in sorted(os.listdir(CLAS_DIR)) if re.match(r"clas_\d+\.json$", f)
        for x in json.load(open(os.path.join(CLAS_DIR, f), encoding="utf-8"))}
extra = json.load(open(os.path.join(D, "fuente", CFG["votos_extra"]), encoding="utf-8")) if CFG.get("votos_extra") else []

GROUP2P = CFG["grupos"]
MX2P = CFG["nominal"]
AUTH2P = CFG["autores"]
GRP_TAG = CFG["etiquetas"]


def mx_party(name):
    for k, p in MX2P.items():
        if name.startswith(k):
            return p
    return None


def letter(v):
    v = (v or "").strip()
    if v in ("Sí", "Si", "S"):
        return "s"
    if v in ("No", "N"):
        return "n"
    if v.startswith("Abst") or v == "A":
        return "a"
    return None


def stance_from_counts(c):
    tot = {k: c.get(k, 0) for k in "sna"}
    if sum(tot.values()) == 0:
        return None
    return max(tot, key=lambda k: tot[k])


def party_stances(g, mx):
    out = {}
    for grp, p in GROUP2P.items():
        if grp in g:
            c = g[grp]
            if isinstance(c, str):
                l = letter(c)
                if l:
                    out[p] = l
            else:
                l = stance_from_counts(c)
                if l:
                    out[p] = l
    per = collections.defaultdict(collections.Counter)
    for name, v in (mx or {}).items():
        p = mx_party(name)
        l = letter(v)
        if p and l:
            per[p][l] += 1
    for p, c in per.items():
        out[p] = c.most_common(1)[0][0]
    return out


def party_seated(g, mx):
    """Partidos con registro en la votación (votaran o no): grupo con algún recuento, incluido «nv», o diputado
    con cualquier valor en el nominal, incluido «No vota». Sin registro (aún no era diputado, o ya no) no cuenta."""
    out = set()
    for grp, p in GROUP2P.items():
        c = g.get(grp)
        if isinstance(c, str) or (isinstance(c, dict) and sum(x or 0 for x in c.values())):
            out.add(p)
    for name in mx or {}:
        p = mx_party(name)
        if p:
            out.add(p)
    return out


def vote_kind(v):
    tit, txt = v["tit"], v["txt"].strip()
    if tit.startswith(("Avocación", "Acuerdo de tramitación", "Enmiendas del Senado", "Veto")):
        return None
    if txt.lower().startswith("tramitación como proyecto"):
        return None
    if txt.startswith("Votación de conjunto") or txt.lower().startswith("votación del dictamen") or tit.startswith("Dictámenes"):
        return "final"
    if "enmienda a la totalidad" in txt.lower() or tit.startswith("Debates de totalidad"):
        return "totalidad"
    if tit.startswith("Convalidación"):
        return "convalidacion"
    if tit.startswith("Toma en consideración"):
        return "toma"
    if tit.startswith("Tramitación directa"):
        return "final"
    return None


PRIO = {"final": 4, "convalidacion": 3, "toma": 2, "totalidad": 1}
LABEL = {"final": "Votación final", "convalidacion": "Convalidación", "toma": "Toma en consideración",
         "totalidad": "Enmienda a la totalidad"}

best = {}


def consider(exp, kind, date, st, tot, seated=()):
    if not exp or not kind or not st:
        return
    if kind == "totalidad":
        st = {p: {"s": "n", "n": "s", "a": "a"}[l] for p, l in st.items()}
    cur = best.get(exp)
    if cur is None or PRIO[kind] > PRIO[cur["k"]] or (PRIO[kind] == PRIO[cur["k"]] and kind == "final"):
        # nv: partidos con escaño en esa votación que no votaron (ni sí, ni no, ni abstención)
        best[exp] = {"k": kind, "d": date, "st": st, "tot": tot, "nv": sorted(set(seated) - set(st))}


STOP = set("proposicion proyecto orgánica organica para sobre desde entre grupo parlamentario votacion conjunto dictamen enmienda totalidad texto alternativo devolucion presentada popular congreso socialista plurinacional sumar republicano mixto junts catalunya vasco bildu".split())
toks = lambda s: {w for w in re.findall(r"[a-záéíóúñ0-9]+", s.lower()) if len(w) > 3 and w not in STOP}
ITEM_TOKS = {it["id"]: toks(it["titulo"]) for it in items}


def sim(a, b):
    return len(a & b) / max(1, min(len(a), len(b)))


def resolve_exp(v):
    exp = v["exp"][:10]
    t = toks(v["txt"])
    if len(t) < 4 or exp not in ITEM_TOKS:
        return exp
    if sim(t, ITEM_TOKS[exp]) >= 0.5:
        return exp
    score = lambda i: sim(t, ITEM_TOKS[i]) + 0.02 * len(t & ITEM_TOKS[i])
    ranked = sorted(ITEM_TOKS, key=score, reverse=True)
    top, second = ranked[0], ranked[1]
    if sim(t, ITEM_TOKS[top]) < 0.7 or score(top) - score(second) < 0.05:
        return None
    return top


remapped = 0
EP = CFG.get("formato") == "europarlamento"
if EP:  # Parlamento Europeo: una votación clave por procedimiento, ya marcada en la descarga
    ids = {it["id"] for it in items}
    for v in raw["votaciones"]:
        if v.get("clave") and v["exp"] in ids:
            tot = v.get("tot") or {}
            desde = CFG.get("escano_desde", {})
            iso = "-".join(reversed(v["d"].split("/"))) if "/" in v["d"] else v["d"]
            seated = {p for p in party_seated(v["g"], {}) if iso >= desde.get(p, "")}
            consider(v["exp"], "final", v["d"], party_stances(v["g"], {}),
                     {"s": tot.get("afavor"), "n": tot.get("enContra"), "a": tot.get("abstenciones")}, seated)
for v in ([] if EP else raw["votaciones"]):
    k = vote_kind(v)
    if not k:
        continue
    exp = resolve_exp(v)
    if exp != v["exp"][:10]:
        remapped += 1
        print("reasignada:", v["exp"][:10], "->", exp, "|", v["txt"][:70], file=sys.stderr)
    if not exp:
        continue
    tot = v.get("tot") or {}
    consider(exp, k, v["d"], party_stances(v["g"], v["mx"]),
             {"s": tot.get("afavor"), "n": tot.get("enContra"), "a": tot.get("abstenciones")},
             party_seated(v["g"], v["mx"]))

# extra final votes matched by title
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
for e in extra:
    key = norm(e["txt"])[:90]
    match = [it["id"] for it in items if norm(it["titulo"]).startswith(key[:60])]
    if len(match) >= 1:
        exp = match[-1]
        consider(exp, "final" if e["kind"] == "conjunto" else "totalidad", e["d"], party_stances(e["g"], e["mx"]), {},
                 party_seated(e["g"], e["mx"]))
    else:
        print("sin match:", e["txt"][:70], file=sys.stderr)

PARTIES = CFG["partidos"]


def authors(it, c):
    a = it["autor"]
    if a in ("Gobierno", "Comisión Europea", "Parlamento Europeo"):
        return [a]
    found = []
    for name, p in AUTH2P.items():
        if name in a:
            found.append(p)
    for tag, p in GRP_TAG.items():
        if f"({tag})" in a and p not in found:
            found.append(p)
    # grupos que agrupan varios partidos (Mixto, Plural): se sustituyen por el partido de la clasificación
    if c.get("partido"):
        # puede ser varios, separados por comas (p. ej. "Podemos, BNG" cuando firman diputados de ambos)
        found = [q for x in found for q in (c["partido"].split(", ") if x in ("Mixto", "Plural") else [x])]
    return found or ["Otros"]


def otros_label(it):
    a = it["autor"]
    if a.startswith("Senado"):
        return "Senado"
    if a.startswith("Comunidad"):
        return "Parlamento autonómico"
    if it["tipo_ini"].startswith("Proposición de ley de iniciativa popular") or it["id"].startswith("120"):
        return "Iniciativa popular"
    return "Otros"


EP_KIND = {"COD": "Legislación ordinaria (reglamento o directiva)", "CNS": "Consulta legislativa",
           "NLE": "Acuerdo o aprobación", "BUD": "Presupuesto", "BUI": "Presupuesto", "APP": "Aprobación legislativa",
           "INL": "Iniciativa legislativa del Parlamento"}


def short_kind(it):
    m = re.search(r"\((\w+)\)$", it["id"])
    if m and m.group(1) in EP_KIND:
        return EP_KIND[m.group(1)]
    t = it["tipo_ini"]
    if t.startswith("Proyecto"):
        return "Proyecto de ley"
    if t.startswith("Real Decreto"):
        return "Real decreto-ley"
    return "Proposición de ley"


# iniciativas con el mismo contenido (data/clasificacion/<clave>/temas.json, scripts/agrupar_temas.py): campo «g»
# con el id del primero del grupo; en la nota, cada partido cuenta el grupo una sola vez
TEMA = {}
_tf = os.path.join(ROOT, "data", "clasificacion", CLAVE, "temas.json")
if os.path.exists(_tf):
    for g in json.load(open(_tf, encoding="utf-8")):
        for i in g["ids"]:
            TEMA[i] = g["ids"][0]

out = []
for it in items:
    c = clas.get(it["id"])
    if c is None:  # iniciativa aún sin clasificar: se omite
        continue
    b = best.get(it["id"])
    res = it["resultado"]
    if it["tipo_ini"] == "Real Decreto-ley" and b:
        s, n = b["tot"].get("s") or 0, b["tot"].get("n") or 0
        res = "Convalidado" if s > n else "Derogado"
    a = authors(it, c)
    rec = {
        "id": it["id"], "t": it["titulo"], "k": short_kind(it), "a": a,
        "ao": otros_label(it) if a == ["Otros"] else "",
        "f": it["fecha"], "r": res or it["situacion"], "tp": c["tipo"], "imp": c["imp"], "w": c["peso"], "n": c["nota"],
    }
    if b:
        rec["v"] = b["st"]
        rec["vk"] = LABEL[b["k"]]
        rec["vd"] = b["d"]
        nv = [p for p in b["nv"] if p in PARTIES]
        if nv:
            rec["nv"] = nv
    if it["id"] in TEMA:
        rec["g"] = TEMA[it["id"]]
    # ley ómnibus (rúbrica 3.8): sus medidas, cada una con su imp y su peso
    if c.get("medidas"):
        rec["m"] = [{"d": m["d"], "imp": m["imp"], "w": m["peso"]} for m in c["medidas"]]
    out.append(rec)

meta = {"clave": CLAVE, "fuente": CFG["fuente"], "fuente_txt": FUENTES[CFG["fuente"]], "leg": CFG["leg"],
        "titulo": CFG["titulo"], "periodo": CFG["periodo"], "gobierno": CFG["gobierno"],
        "nominal_txt": CFG["nominal_txt"], "formato": CFG.get("formato", "congreso"), "generado": raw["generado"][:10], "parties": PARTIES,
        "authors": CFG["autores_web"],
        # los items llevan «nv» (partidos con escaño que no votaron): la ficha calcula con ello la participación
        "participacion": True}
dest = os.path.join(ROOT, "site", "data", CLAVE + ".json")
os.makedirs(os.path.dirname(dest), exist_ok=True)
json.dump({"meta": meta, "items": out}, open(dest, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("sin clasificar:", len(items) - len(out))

with_votes = sum(1 for r in out if "v" in r)
print("items", len(out), "con voto", with_votes)
print(collections.Counter(r["vk"] for r in out if "v" in r))
print(collections.Counter(x for r in out for x in r["a"]))
pv = collections.Counter(p for r in out if "v" in r for p in r["v"])
print(pv)
