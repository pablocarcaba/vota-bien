"""Descarga los procedimientos y las votaciones nominales del Pleno del Parlamento Europeo (10.ª legislatura,
desde el 16/07/2024) con el voto de los eurodiputados españoles agrupado por partido nacional.

Fuentes (datos abiertos, sin claves ni scraping):
  1. HowTheyVote.eu (https://github.com/HowTheyVote/data, licencia abierta con atribución: ver
     https://howtheyvote.eu/about#license). Publica cada semana un export en CSV con todas las votaciones
     nominales del Pleno (votes), el voto de cada eurodiputado (member_votes) CON SU PARTIDO NACIONAL en la
     fecha de la votación, los eurodiputados y las afiliaciones a partidos nacionales con fechas. Los datos
     salen de las actas oficiales del PE (listas de votación nominal) y ya vienen ligados al procedimiento
     (p. ej. 2024/0234(COD)), su tipo y etapa, y marcan qué votación es la principal ("is_main") de cada
     informe. Es la opción más sencilla y robusta: ~9 ficheros estáticos, descarga en bloque, sin paginar
     ni reconstruir el partido nacional de cada eurodiputado.
  2. API de datos abiertos del PE (https://data.europarl.europa.eu/api/v2/procedures/<aaaa-nnnn>): solo
     para el título oficial en español del procedimiento y los hitos de firma y publicación en el DOUE
     (HowTheyVote solo da el título en inglés). Una petición por procedimiento.
  Se descartó usar solo la API v2: el voto nominal y el partido nacional exigen cruzar varios endpoints
  paginados (meetings/vote-results, meps, memberships) por cada sesión, más frágil y lento.

Uso:
  python3 scripts/descargar_europarlamento.py               # usa la versión de HowTheyVote en caché
  python3 scripts/descargar_europarlamento.py --actualizar  # baja la última versión semanal

Caché: data/cache/europarlamento_10/ (ignorado por git): htv/<versión>/*.csv.gz (~107 MB, sobre todo
member_votes) y procedimientos/<id>.json. Una sola petición cada vez, con pausa >= 1 s. Relanzar con caché
completa tarda ~1 min (lectura de member_votes); desde cero, ~10-15 min.

Salida: data/fuente/europarlamento_10.json, con formato parecido a congreso_xiv.json:
  procedimientos: uno por procedimiento con alguna votación principal en la legislatura:
      exp (referencia, p. ej. "2024/0234(COD)"), tipo (código: COD, CNS, NLE, RSP, INI...), tipo_txt,
      legislativo (bool: COD, CNS, APP, NLE, BUD, INL...), tit (español si existe), tit_en, d (fecha de la
      votación clave, dd/mm/aaaa), res ("Aprobado"/"Rechazado" en la votación clave), firma y doue (fechas
      de firma y de publicación en el DOUE, si las hay), ta (referencia del texto aprobado), nvot (id de la
      votación clave).
  votaciones: las votaciones principales (is_main) de esos procedimientos, con:
      exp, d, nv (id de la votación en HowTheyVote), hora, tit (título), txt (título del procedimiento,
      español si existe), sub (descripción oficial de la votación, en francés como en el acta: "Proposition
      de la Commission", "Accord provisoire - Am 12", "Proposition de résolution (ensemble du texte)"...),
      etapa (OLP_FIRST_READING...), res, clave (bool: votación que resume el procedimiento),
      tot {presentes, afavor, enContra, abstenciones, noVotan} (los 720 eurodiputados),
      g {partido español: {s, n, a, nv}} (solo eurodiputados españoles; partido en la fecha de la votación),
      mx {"APELLIDOS, Nombre": "Sí"/"No"/"Abstención"/"No vota"} (cada eurodiputado español).
  eurodiputados: una entrada por eurodiputado español y periodo de afiliación: id, nombre, partido
      (normalizado), partido_oficial, grupo (grupo político del PE), desde, hasta, votos (nº de votaciones
      principales en que figura).

Diferencias con congreso_*.json: no hay proyectos/proposiciones/rdl sino "procedimientos"; "g" va por partido
nacional (no por grupo parlamentario); no hay "ses" ni "asentimiento"; "nv" es el id de HowTheyVote y no el
número de votación del día; "noVotan" incluye ausentes. Votación clave: la última votación principal del
procedimiento que no sea una propuesta de rechazo, una decisión de urgencia ni la de abrir negociaciones
(normalmente el acuerdo provisional o la resolución legislativa de primera lectura); si no hay otra, la última.
Normalización de partidos: PSC-PSOE -> PSOE, Movimiento Sumar -> Sumar, Catalunya en Comú -> Comuns,
EH Bildu -> Bildu, PODEMOS -> Podemos, Se Acabó La Fiesta -> SALF. Junts no tiene eurodiputado con escaño
efectivo (Toni Comín no llegó a acreditarse). Solier y Junco figuran como "Independiente" desde 12/2024
(salieron de SALF).
"""
import argparse, csv, datetime as dt, gzip, io, json, os, sys, time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import ssl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CACHE = os.path.join(ROOT, "data", "cache", "europarlamento_10")
# legislaturas cubiertas por HowTheyVote (desde julio de 2019): sesión constitutiva y último día
TERMS = {"9": ("2019-07-02", "2024-07-15"), "10": ("2024-07-16", "9999-12-31")}
INICIO, FIN = TERMS["10"]
SALIDA = os.path.join(ROOT, "data", "fuente", "europarlamento_10.json")
HTV = "https://github.com/HowTheyVote/data/releases"
EPAPI = "https://data.europarl.europa.eu/api/v2/procedures/"
UA = {"User-Agent": "quien-legisla (proyecto ciudadano; datos abiertos)"}
PAUSA = 2.0
TABLAS = ["votes", "members", "national_parties", "national_party_memberships", "groups", "group_memberships",
          "member_votes"]
PARTIDOS = {"PSOE": "PSOE", "PSC-PSOE": "PSOE", "PP": "PP", "VOX": "VOX", "SALF": "SALF", "SMR": "Sumar",
            "Catalunya en Comú": "Comuns", "Compromís": "Compromís", "PODEMOS": "Podemos", "ERC": "ERC",
            "EH BILDU": "Bildu", "PNV": "PNV", "BNG": "BNG", "JxCat-Junts": "Junts", "Junts": "Junts",
            "IU": "IU", "Independiente": "Independiente",
            # 9.ª legislatura
            "CS": "Cs", "DCE": "Cs", "ANTICAPITALISTAS": "Anticapitalistas"}
VOTO = {"FOR": "Sí", "AGAINST": "No", "ABSTENTION": "Abstención", "DID_NOT_VOTE": "No vota"}
CLAVE_VOTO = {"FOR": "s", "AGAINST": "n", "ABSTENTION": "a", "DID_NOT_VOTE": "nv"}
TIPOS = {"COD": "Procedimiento legislativo ordinario", "CNS": "Consulta legislativa", "APP": "Aprobación legislativa",
         "NLE": "Procedimiento no legislativo (aprobación/consentimiento)", "BUD": "Presupuesto",
         "BUI": "Procedimiento presupuestario interinstitucional", "INL": "Informe de iniciativa legislativa",
         "INI": "Informe de propia iniciativa", "RSP": "Resolución sobre un tema de actualidad",
         "DEC": "Aprobación de la gestión", "DEA": "Objeción a acto delegado", "RPS": "Objeción a medida de ejecución",
         "RSO": "Organización interna", "REG": "Reglamento interno", "INS": "Investigación", "ACI": "Acuerdo interinstitucional"}
LEGISLATIVOS = {"COD", "CNS", "APP", "NLE", "BUD", "BUI", "INL"}
NO_CLAVE = ("Proposition de rejet", "Rejet", "Demande de décision d'urgence", "Demandes de décision d'urgence",
            "Décision d'engager des négociations")

try:  # algunos Python de macOS no traen certificados raíz
    import certifi
    _ssl = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl = ssl.create_default_context()
_ultima = [0.0]


def get(url, accept=None):
    espera = PAUSA - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    h = dict(UA, **({"Accept": accept} if accept else {}))
    for intento in range(5):
        try:
            _ultima[0] = time.time()
            with urlopen(Request(url, headers=h), timeout=300, context=_ssl) as r:
                return r.read()
        except HTTPError as e:
            if e.code in (404, 204):
                return None
            if e.code in (403, 429):
                sys.exit(f"\n{e.code} en {url}: el servidor pide parar. Relanza más tarde (la caché se conserva).")
            err = e
        except (URLError, TimeoutError, ConnectionError) as e:
            err = e
        if intento == 4:
            raise err
        print(f"\n{type(err).__name__} en {url[:90]}; reintento en {15 * 2 ** intento} s", file=sys.stderr)
        time.sleep(15 * 2 ** intento)


def version_htv(actualizar):
    base = os.path.join(CACHE, "htv")
    locales = sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))) if os.path.isdir(base) else []
    completas = [d for d in locales if all(os.path.exists(os.path.join(base, d, t + ".csv.gz")) for t in TABLAS)]
    if completas and not actualizar:
        return completas[-1]
    raw = get("https://api.github.com/repos/HowTheyVote/data/releases/latest", "application/vnd.github+json")
    return json.loads(raw)["tag_name"]


def descargar_htv(ver):
    d = os.path.join(CACHE, "htv", ver)
    os.makedirs(d, exist_ok=True)
    for t in TABLAS:
        p = os.path.join(d, t + ".csv.gz")
        if not os.path.exists(p):
            print(f"Descargando {t}.csv.gz ({ver})...", file=sys.stderr)
            data = get(f"{HTV}/download/{ver}/{t}.csv.gz")
            with open(p + ".tmp", "wb") as f:
                f.write(data)
            os.replace(p + ".tmp", p)
    return d


def leer(d, t):
    with gzip.open(os.path.join(d, t + ".csv.gz"), "rt", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def fecha(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}" if iso else ""


def procedimiento(ref):
    """Título en español e hitos (firma, DOUE) desde la API del PE, con caché. ref = '2024/0234(COD)'."""
    pid = ref.split("(")[0].replace("/", "-")
    p = os.path.join(CACHE, "procedimientos", pid + ".json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    raw = get(f"{EPAPI}{pid}?format=application%2Fld%2Bjson", "application/ld+json")
    val = {"es": "", "en": "", "firma": "", "doue": "", "fase": ""}
    if raw:
        try:
            x = (json.loads(raw).get("data") or [{}])[0]
        except ValueError:
            x = {}
        t = x.get("process_title") or {}
        val.update(es=t.get("es", ""), en=t.get("en", ""), fase=str((x.get("current_stage") or [""])[0] if isinstance(x.get("current_stage"), list) else (x.get("current_stage") or "")).rsplit("/", 1)[-1])
        uno = lambda v: (v[0] if v else "") if isinstance(v, list) else (v or "")  # a veces llegan listas
        for ev in x.get("consists_of") or []:
            tipo = str(uno(ev.get("had_activity_type"))).rsplit("/", 1)[-1]
            fecha_ev = str(uno(ev.get("activity_date")))
            if tipo == "SIGNATURE":
                val["firma"] = max(val["firma"], fecha_ev)
            elif tipo == "PUBLICATION_OFFICIAL_JOURNAL":
                val["doue"] = max(val["doue"], fecha_ev)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + ".tmp", "w", encoding="utf-8") as f:
        json.dump(val, f, ensure_ascii=False)
    os.replace(p + ".tmp", p)
    return val


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--actualizar", action="store_true", help="descargar la última versión semanal de HowTheyVote")
    ap.add_argument("--leg", default="10", choices=sorted(TERMS), help="legislatura (9 o 10)")
    a = ap.parse_args()
    global INICIO, FIN, SALIDA
    INICIO, FIN = TERMS[a.leg]
    SALIDA = os.path.join(ROOT, "data", "fuente", f"europarlamento_{a.leg}.json")
    ver = version_htv(a.actualizar)
    d = descargar_htv(ver)

    # votaciones principales de la legislatura ligadas a un procedimiento
    votos = [v for v in leer(d, "votes") if INICIO <= v["timestamp"][:10] <= FIN and v["is_main"] == "True"
             and v["procedure_reference"]]
    votos.sort(key=lambda v: v["timestamp"])
    por_proc = {}
    for v in votos:
        por_proc.setdefault(v["procedure_reference"], []).append(v)
    clave = {}
    for ref, vs in por_proc.items():
        buenas = [v for v in vs if not v["description"].startswith(NO_CLAVE)]
        clave[ref] = (buenas or vs)[-1]["id"]
    print(f"HowTheyVote {ver}: {len(votos)} votaciones principales, {len(por_proc)} procedimientos", file=sys.stderr)

    # eurodiputados españoles y su partido nacional
    np_ = {p["id"]: p for p in leer(d, "national_parties")}
    miembros = {m["id"]: m for m in leer(d, "members")}
    grupos = {g["code"]: g["short_label"] for g in leer(d, "groups")}
    gm = {}
    for g in leer(d, "group_memberships"):
        if g["term"] == a.leg:
            gm.setdefault(g["member_id"], []).append(g)
    afil = [m for m in leer(d, "national_party_memberships") if np_[m["national_party_id"]]["country_code"] == "ESP"
            and (not m["end_date"] or m["end_date"] >= INICIO) and m["start_date"] <= FIN]

    # voto de cada eurodiputado español (member_votes es grande: se lee en streaming)
    ids = {v["id"]: v["timestamp"][:10] for v in votos}
    nominal, fechas_voto = {}, {}
    for mv in leer(d, "member_votes"):
        if mv["country_code"] != "ESP" or mv["vote_id"] not in ids:
            continue
        nominal.setdefault(mv["vote_id"], []).append(mv)
        fechas_voto.setdefault(mv["member_id"], []).append(ids[mv["vote_id"]])

    def nombre(mid):
        m = miembros[mid]
        return f"{m['last_name']}, {m['first_name']}"

    def grupo(mid, desde):
        gs = [g for g in gm.get(mid, []) if g["start_date"] <= max(desde, INICIO) <= (g["end_date"] or "9999")]
        return grupos.get(gs[0]["group_code"], gs[0]["group_code"]) if gs else ""

    eurodiputados = []
    for m in sorted(afil, key=lambda m: (nombre(m["member_id"]), m["start_date"])):
        if m["start_date"] == m["end_date"]:
            continue  # afiliaciones de un solo día (corrección de la sesión constitutiva)
        p = np_[m["national_party_id"]]
        eurodiputados.append({"id": int(m["member_id"]), "nombre": nombre(m["member_id"]),
                              "partido": PARTIDOS.get(p["short_label"], p["short_label"]),
                              "partido_oficial": p["label"], "grupo": grupo(m["member_id"], m["start_date"]),
                              "desde": fecha(max(m["start_date"], INICIO)), "hasta": fecha(min(m["end_date"] or FIN, FIN) if FIN < "9999" else m["end_date"]),
                              "votos": sum(m["start_date"] <= f <= (m["end_date"] or "9999")
                                           for f in fechas_voto.get(m["member_id"], []))})

    # procedimientos (título en español desde la API del PE)
    procedimientos, titulos = [], {}
    for i, (ref, vs) in enumerate(sorted(por_proc.items())):
        print(f"\r{i + 1}/{len(por_proc)} {ref:20}", end="", file=sys.stderr)
        k = next(v for v in vs if v["id"] == clave[ref])
        tipo = k["procedure_type"] or (ref.split("(")[-1].rstrip(")") if "(" in ref else "")
        # la API solo se consulta para los legislativos (los únicos que usa la web): menos peticiones
        info = procedimiento(ref) if tipo in LEGISLATIVOS else {"es": "", "en": "", "firma": "", "doue": ""}
        titulos[ref] = info["es"] or k["procedure_title"] or k["display_title"]
        procedimientos.append({
            "exp": ref, "tipo": tipo, "tipo_txt": TIPOS.get(tipo, tipo), "legislativo": tipo in LEGISLATIVOS,
            "tit": titulos[ref], "tit_en": k["procedure_title"] or info["en"] or k["display_title"],
            "d": fecha(k["timestamp"][:10]), "res": "Aprobado" if k["result"] == "ADOPTED" else "Rechazado",
            "firma": fecha(info["firma"]), "doue": fecha(info["doue"]), "ta": k["texts_adopted_reference"],
            "nvot": int(k["id"]), "nvotaciones": len(vs)})
    print(file=sys.stderr)

    votaciones = []
    for v in votos:
        g, mx = {}, {}
        for mv in sorted(nominal.get(v["id"], []), key=lambda x: nombre(x["member_id"])):
            part = PARTIDOS.get(mv["national_party_short_label"], mv["national_party_short_label"] or "Sin partido")
            c = g.setdefault(part, {"s": 0, "n": 0, "a": 0, "nv": 0})
            c[CLAVE_VOTO.get(mv["position"], "nv")] += 1
            mx[nombre(mv["member_id"])] = VOTO.get(mv["position"], mv["position"])
        s, n, ab, nv = (int(v[c] or 0) for c in ("count_for", "count_against", "count_abstention", "count_did_not_vote"))
        votaciones.append({
            "exp": v["procedure_reference"], "d": fecha(v["timestamp"][:10]), "hora": v["timestamp"][11:16],
            "nv": int(v["id"]), "tit": v["display_title"], "txt": titulos[v["procedure_reference"]],
            "sub": v["description"], "ref": v["reference"], "etapa": v["procedure_stage"],
            "res": "Aprobado" if v["result"] == "ADOPTED" else "Rechazado" if v["result"] == "REJECTED" else v["result"],
            "clave": v["id"] == clave[v["procedure_reference"]],
            "tot": {"presentes": s + n + ab, "afavor": s, "enContra": n, "abstenciones": ab, "noVotan": nv},
            "g": dict(sorted(g.items(), key=lambda x: -sum(x[1].values()))), "mx": mx})

    out = {"generado": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
           "fuente": f"HowTheyVote.eu (versión {ver}, github.com/HowTheyVote/data) + API de datos abiertos del "
                     "Parlamento Europeo (data.europarl.europa.eu)",
           "legislatura": a.leg, "desde": fecha(INICIO), "procedimientos": procedimientos,
           "votaciones": votaciones, "eurodiputados": eurodiputados}
    with open(SALIDA + ".tmp", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(SALIDA + ".tmp", SALIDA)
    leg = sum(p["legislativo"] for p in procedimientos)
    print(f"{SALIDA}: {len(procedimientos)} procedimientos ({leg} legislativos), {len(votaciones)} votaciones, "
          f"{len({e['id'] for e in eurodiputados})} eurodiputados españoles", file=sys.stderr)


if __name__ == "__main__":
    main()
