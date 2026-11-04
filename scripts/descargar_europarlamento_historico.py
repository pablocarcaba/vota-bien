"""Descarga los procedimientos y las votaciones nominales del Pleno del Parlamento Europeo de las legislaturas
6.ª (20/07/2004-13/07/2009), 7.ª (14/07/2009-30/06/2014) y 8.ª (01/07/2014-01/07/2019), con el voto de los
eurodiputados españoles agrupado por partido nacional. Produce data/fuente/europarlamento_<leg>.json con el
mismo formato que scripts/descargar_europarlamento.py (9.ª y 10.ª, desde HowTheyVote.eu, que no cubre antes de
julio de 2019).

Fuentes (todas abiertas, sin claves ni scraping de páginas web):
  1. Anexos oficiales del acta "Resultados de las votaciones nominales" (PV-<leg>-<aaaa-mm-dd>-RCV, XML en
     francés) en el servidor de distribución de datos abiertos del PE:
     https://data.europarl.europa.eu/distribution/reds_iPlPv_Rcv/<id>/<id>-FNL_fr.xml. Cada votación trae su
     descripción ("A7-0003/2012 - Antonio Masip Hidalgo - Vote unique"), los totales y la lista de quién votó
     sí/no/abstención por grupo político, con un MepId interno del acta (no es el PersId de la API) y el
     apellido con que vota. Reutilización autorizada citando la fuente (aviso legal del PE). Las direcciones
     www.europarl.europa.eu/doceo y /RegData responden 403 a clientes no navegadores, así que no se usan.
  2. Anexos "Resultados de las votaciones" (PV-...-VOT, mismo servidor): solo para reconocer los acuerdos que
     se votan como una enmienda o un bloque de enmiendas, tras lo cual el resto decae: "Accord provisoire -
     Am 271" (8.ª), "Ensemble du texte - Am 190" o "bloc n° 1 - compromis" (7.ª), "Option 1 - Paquet de
     compromis" (6.ª, segundas lecturas). El anexo RCV solo dice "Am 271"; se empareja con la fila del VOT por
     documento, día y totales, y solo cuenta si es la última votación de conjunto de ese texto ese día.
  3. API de datos abiertos del PE v2 (https://data.europarl.europa.eu/api/v2/): eurodiputados de España en la
     legislatura (meps?parliamentary-term=N&country-of-representation=ES) con sus mandatos, partido nacional
     (NATIONAL_POLITICAL_GROUP) y grupo político con fechas (meps/<id>, corporate-bodies/<id>); documento ->
     procedimiento (meetings/MTG-PL-<fecha>/vote-results y, si falta, plenary-documents/<doc>); referencia,
     tipo, título en español, firma, DOUE y textos aprobados del procedimiento (procedures/<aaaa-nnnn>).
  4. Solo para la 6.ª: Parltrack (https://parltrack.org/dumps/ep_votes.json.zst, licencia ODbL 1.0, atribución
     "Parltrack"). La distribución oficial no tiene los anexos RCV entre octubre de 2005 y diciembre de 2008
     (sí 09/2004-09/2005 y 01-05/2009). Parltrack los extrajo en su día de los mismos XML oficiales (RegData) y
     ya resolvió cada eurodiputado a su PersId y cada votación a su procedimiento; se usa solo para los días que
     faltan. Requiere la orden `zstd` (brew install zstd). En los días con ambas fuentes coinciden totales y
     voto de cada español en las 372 votaciones comparables. (En la 7.ª y la 8.ª, Parltrack tiene errores que
     el acta oficial no: no resuelve a Javi López y asigna a Gabriel Mato el PersId de Ana Mato.)
  Descartados: la API v2 no tiene voto nominal antes de 2019 (meetings/.../decisions da 404) y su lista de
  sesiones empieza en 2014; VoteWatch Europe ya no publica descargas; los datos de Hix-Noury-Roland solo llegan
  a 2014 y no traen el partido nacional con fechas ni el procedimiento.

Uso:
  python3 scripts/descargar_europarlamento_historico.py --leg 8   # (6, 7 u 8)
  python3 scripts/descargar_europarlamento_historico.py --leg 7 --solo-descarga   # solo los anexos RCV

Caché: data/cache/europarlamento_<leg>/ (ignorado por git): rcv/*.xml.gz y vot/*.xml.gz (con _sin_*.txt de
los días probados sin anexo), api/ (respuestas JSON de la API, también las vacías) y, en la 6.ª, parltrack/.
Peticiones de una en una: 1,2 s de pausa con la API y 2,5 s con el servidor de distribución (responde 429 con
menos); ante un 429 espera lo que pida (o 5 min) dos veces y luego para; ante un 403, para. Días de sesión: en
la 8.ª, la lista de la API; en la 6.ª y la 7.ª se prueban miércoles y jueves de cada semana (fuera de agosto) y,
si alguno tiene anexo, el lunes y el martes. Desde cero tarda ~2-3 h por legislatura; con caché, 1-2 min.

Salida: igual que europarlamento_10.json (ver el docstring de descargar_europarlamento.py), con estas
diferencias:
  - nv / nvot: id de la votación en el acta (Identifier) hasta 2017; en los anexos de 2018-2019, que no lo
    traen, aaaammddNNN (fecha + número de orden en el anexo). En los días de Parltrack, su voteid (= Identifier).
  - sub: tramo final de la descripción oficial en francés ("Vote unique", "Résolution législative",
    "Proposition de la Commission"...); "Accord provisoire - Am 271" para los acuerdos votados como enmienda.
    tit: la descripción completa; ref: documentos citados (A-7-2012-0003...); etapa: siempre "".
  - res: "Aprobado" si hay más síes que noes (los anexos no dicen el resultado; no se tienen en cuenta las
    mayorías cualificadas, que casi nunca afectan a la votación clave).
  - tot.noVotan: escaños del Pleno en esa fecha (732/785 en la 6.ª; 736/754/766 en la 7.ª; 751 en la 8.ª)
    menos presentes: incluye ausentes y no descuenta vacantes. En g/mx, "nv"/"No vota" son los españoles con
    mandato ese día que no figuran en la lista (ausentes o presentes sin votar: el acta no lo distingue).
  - Se ignoran las votaciones secretas y las correcciones de voto posteriores (no cambian el resultado).
  - hora: algunos anexos de la 7.ª usan reloj de 12 h sin a. m./p. m. ("01:14"): las horas < 08 se suman 12.
  - Procedimientos que la API no devuelve (404; ver TIPO_SIN_API): tipo según el OEIL y título del informe.
  - hasta: fin de la legislatura en los eurodiputados.
Votaciones incluidas: solo las de conjunto ligadas a un procedimiento (descripción que empieza por "Vote
unique", "Résolution (législative)", "Proposition de la Commission", "Approbation", "Décision", "Accord
provisoire", "Proposition de rejet"... y no es una enmienda, un apartado ni una votación por partes). Votación
clave: la última de esas del procedimiento en la legislatura que no sea un rechazo, una urgencia ni la decisión
de abrir negociaciones; si no hay otra, la última. LIMITACIÓN IMPORTANTE: solo hay voto nominal cuando un grupo
lo pide (o es obligatorio, como en las resoluciones legislativas desde 2009 aprox.): muchos procedimientos se
aprobaron a mano alzada y no aparecen, sobre todo en la 6.ª, y de algunos solo hay la votación de la propuesta
de la Commission y no la de la resolución.

Identificación de los españoles (6.ª días oficiales, 7.ª y 8.ª): el acta da apellido y grupo, no el país. Entre
los españoles con mandato en esa fecha se busca coincidencia exacta del nombre normalizado (sin tildes ni
signos) con apellidos o nombre + apellidos; si no hay, que una forma prolongue a la otra por palabras completas
("Aguilera García" ~ "Aguilera", "Pagazaurtundúa Ruiz" ~ "Pagazaurtundúa") y que coincida el grupo. Solo
valen las coincidencias únicas; después cada MepId del acta se asocia por mayoría (>= 90 %) a un PersId y se
usa en todas las votaciones. Se comprobó contra Parltrack, que hace la resolución por su cuenta.

Normalización de partidos (etiqueta oficial de la API -> g): ver PARTIDOS. PSC -> PSOE; Izquierda Xunida
(federación asturiana de IU) -> IU; IU-ICV-EUiA e ICV-EUiA (Romeva, 6.ª) -> ICV; Delegación Ciudadanos
Europeos -> Cs; Alternativa galega de esquerda en Europa (Lidia Senra, Anova) -> AGE; Coalición por Europa
(primeros días de Tremosa y Sedó) -> CDC / UDC y Europa de los Pueblos (Bernat Joan, 2004-2007; Irujo, unos
días de 2007) -> ERC / EA, porque la API da la coalición y no el partido (ver POR_PERSONA); Nova Esquerra
Catalana -> NECat; "-" (sin partido) -> Independiente; las demás, por su sigla (PP, PSOE, IU, ICV, CDC, UDC,
PDeCAT, PNV, EA, Aralar, ERC, BNG, UPN, UPyD, Cs, Podemos, Bildu, Compromís, Equo, VOX, Los Verdes). Cada
eurodiputado cuenta con el partido que la API le asigna en la fecha de la votación (p. ej. Tremosa: CEU -> CDC
-> PDeCAT; Vidal-Quadras pasa de PP a VOX en 03/2014; Couso, Becerra o Punset pasan a Independiente).
"""
import argparse, datetime as dt, gzip, json, os, re, sys, time, unicodedata
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import ssl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TERMS = {"6": ("2004-07-20", "2009-07-13"), "7": ("2009-07-14", "2014-06-30"), "8": ("2014-07-01", "2019-07-01")}
API = "https://data.europarl.europa.eu/api/v2/"
RCV = "https://data.europarl.europa.eu/distribution/reds_iPlPv_Rcv/{id}/{id}-FNL_fr.xml"
VOT = "https://data.europarl.europa.eu/distribution/reds_iPlPv_Vot/{id}/{id}-FNL_fr.xml"
UA = {"User-Agent": "quien-legisla (proyecto ciudadano; datos abiertos)"}
PAUSA = 1.2        # API v2
PAUSA_RCV = 2.5    # el servidor de distribución de documentos responde 429 con pausas de ~1 s

VOTO = {"s": "Sí", "n": "No", "a": "Abstención", "nv": "No vota"}
TIPOS = {"COD": "Procedimiento legislativo ordinario", "SYN": "Procedimiento de cooperación", "AVC": "Dictamen conforme",
         "CNS": "Consulta legislativa", "APP": "Aprobación legislativa",
         "NLE": "Procedimiento no legislativo (aprobación/consentimiento)", "BUD": "Presupuesto",
         "BUI": "Procedimiento presupuestario interinstitucional", "INL": "Informe de iniciativa legislativa",
         "INI": "Informe de propia iniciativa", "RSP": "Resolución sobre un tema de actualidad",
         "DEC": "Aprobación de la gestión", "DEA": "Objeción a acto delegado", "RPS": "Objeción a medida de ejecución",
         "RSO": "Organización interna", "REG": "Reglamento interno", "INS": "Investigación",
         "ACI": "Acuerdo interinstitucional", "IMM": "Inmunidad parlamentaria", "COS": "Comunicación de la Comisión"}
LEGISLATIVOS = {"COD", "SYN", "AVC", "CNS", "APP", "NLE", "BUD", "BUI", "INL"}
# partido nacional oficial (API v2, NATIONAL_POLITICAL_GROUP) -> nombre corto estable
PARTIDOS = {
    "Partido Popular": "PP", "Partido Socialista Obrero Español": "PSOE", "Partit dels Socialistes de Catalunya": "PSOE",
    "PODEMOS": "Podemos", "Podemos": "Podemos", "Unión, Progreso y Democracia": "UPyD",
    "Ciudadanos – Partido de la Ciudadanía": "Cs", "Delegación Ciudadanos Europeos": "Cs",
    "Izquierda Unida": "IU", "Izquierda Xunida": "IU", "Iniciativa per Catalunya Verds": "ICV",
    "Alternativa galega de esquerda en Europa": "AGE", "Esquerra Republicana de Catalunya": "ERC",
    "Nova Esquerra Catalana": "NECat", "Convergència Democràtica de Catalunya": "CDC",
    "Unió Democràtica de Catalunya": "UDC", "Partit Demòcrata Europeu i Català": "PDeCAT",
    "Coalición por Europa": "CEU", "EH BILDU": "Bildu", "COMPROMIS": "Compromís", "Bloque Nacionalista Galego": "BNG",
    "EQUO": "Equo", "Partido Nacionalista Vasco": "PNV", "Independiente": "Independiente", "-": "Independiente",
    # 6.ª y 7.ª
    "Convergència Democràtica Catalunya": "CDC", "Unión del Pueblo Navarro": "UPN", "Los Verdes": "Los Verdes",
    "Izquierda Unida - Iniciativa Per Catalunya Verds - Esquerra Unida í Alternativa": "ICV",
    "Iniciativa Per Catalunya Verds - Esquerra Unida í Alternativa": "ICV", "Eusko Alkartasuna": "EA",
    "Europa de los Pueblos": "Europa de los Pueblos", "Europa de los Pueblos-Verdes": "Europa de los Pueblos",
    "Aralar": "Aralar", "Vox": "VOX",
}
# procedimientos con voto nominal que la API v2 no devuelve (404); tipo según el OEIL
TIPO_SIN_API = {"2016-0062": "NLE", "2016-0400": "COD", "2018-0152": "COD", "2018-0330": "COD"}
PARLTRACK_LEGS = {"6"}  # legislaturas con huecos en la distribución oficial
GRUPOS = {}  # sigla de grupo de la API -> la del acta, si algún día difieren (hoy coinciden)
# coaliciones que la API da en lugar del partido del eurodiputado: (apellido del acta, etiqueta) -> partido
POR_PERSONA = {("JOAN i MARÍ", "Europa de los Pueblos"): "ERC", ("IRUJO AMEZAGA", "Europa de los Pueblos"): "EA",
               ("TREMOSA i BALCELLS", "Coalición por Europa"): "CDC", ("SEDÓ i ALABART", "Coalición por Europa"): "UDC"}
ALIAS = {}   # PersId -> nombres alternativos con que vota en el acta (hoy no hace falta ninguno)

try:  # algunos Python de macOS no traen certificados raíz
    import certifi
    _ssl = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl = ssl.create_default_context()
_ultima = [0.0]


def get(url, accept=None, pausa=PAUSA):
    """GET secuencial con pausa; None si 404/204; ante 429 espera y reintenta dos veces; para ante 403."""
    espera = pausa - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    h = dict(UA, **({"Accept": accept} if accept else {}))
    esperas_429 = 0
    for intento in range(5):
        try:
            _ultima[0] = time.time()
            with urlopen(Request(url, headers=h), timeout=300, context=_ssl) as r:
                return r.read() if r.status != 204 else None
        except HTTPError as e:
            if e.code in (404, 204, 410):
                return None
            if e.code == 429 and esperas_429 < 2:  # retroceder: esperar lo que pida el servidor (o 5 min)
                esperas_429 += 1
                t = int(e.headers.get("Retry-After") or 0) if (e.headers.get("Retry-After") or "").isdigit() else 300
                print(f"\n429 en {url[:90]}; espero {max(t, 60)} s", file=sys.stderr)
                time.sleep(max(t, 60))
                continue
            if e.code in (403, 429):
                sys.exit(f"\n{e.code} en {url}: el servidor pide parar. Relanza más tarde (la caché se conserva).")
            err = e
        except (URLError, TimeoutError, ConnectionError) as e:
            err = e
        if intento == 4:
            raise err
        print(f"\n{type(err).__name__} en {url[:90]}; reintento en {15 * 2 ** intento} s", file=sys.stderr)
        time.sleep(15 * 2 ** intento)


def cache_json(ruta, url, accept="application/ld+json"):
    """JSON de la API v2 con caché en disco (también se cachea la respuesta vacía como null)."""
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    raw = get(url, accept)
    try:
        val = json.loads(raw) if raw else None
    except ValueError:
        val = None
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta + ".tmp", "w", encoding="utf-8") as f:
        json.dump(val, f, ensure_ascii=False)
    os.replace(ruta + ".tmp", ruta)
    return val


def api(cache, ruta, path):
    sep = "&" if "?" in path else "?"
    return cache_json(os.path.join(cache, "api", ruta), f"{API}{path}{sep}format=application%2Fld%2Bjson")


def dias_candidatos(leg, cache):
    """Días con posible sesión plenaria. La API de reuniones solo cubre desde 2014: para la 8.ª se usa su
    lista; para la 6.ª y la 7.ª se prueban todos los lunes-jueves fuera de agosto (nunca hubo votaciones
    nominales en viernes en esos años)."""
    ini, fin = TERMS[leg]
    if leg == "8":
        d = api(cache, "meetings.json", "meetings?offset=0&limit=5000")
        dias = sorted({m["activity_id"][7:17] for m in (d or {}).get("data", []) if ini <= m["activity_id"][7:17] <= fin})
        if dias:
            return dias
    a, b = dt.date.fromisoformat(ini), dt.date.fromisoformat(fin)
    return [str(a + dt.timedelta(i)) for i in range((b - a).days + 1)
            if (a + dt.timedelta(i)).weekday() < 4 and (a + dt.timedelta(i)).month != 8]


def descargar_rcv(leg, cache):
    """Baja (con caché gzip) el anexo de votaciones nominales en francés de cada sesión; devuelve las rutas."""
    d = os.path.join(cache, "rcv")
    os.makedirs(d, exist_ok=True)
    faltan_p = os.path.join(d, "_sin_rcv.txt")
    faltan = set(open(faltan_p).read().split()) if os.path.exists(faltan_p) else set()
    dias = dias_candidatos(leg, cache)
    rutas = []

    def bajar(dia):
        pid = f"PV-{leg}-{dia}-RCV"
        p = os.path.join(d, pid + ".xml.gz")
        if os.path.exists(p):
            return p
        if dia in faltan:
            return None
        print(f"\r{dia} {pid}   ", end="", file=sys.stderr)
        raw = get(RCV.format(id=pid), pausa=PAUSA_RCV)
        if raw and b"RollCallVoteResults" in raw[:3000]:
            with gzip.open(p + ".tmp", "wb") as f:
                f.write(raw)
            os.replace(p + ".tmp", p)
            return p
        faltan.add(dia)
        with open(faltan_p, "a") as f:
            f.write(dia + "\n")
        return None

    # por semanas: se prueban miércoles y jueves (siempre hay votaciones en ellos si hay sesión, también en
    # las minisesiones de Bruselas); solo si alguno existe se prueban el lunes y el martes de esa semana
    semanas = {}
    for dia in dias:
        x = dt.date.fromisoformat(dia)
        semanas.setdefault(x - dt.timedelta(x.weekday()), []).append(dia)
    for lunes, ds in sorted(semanas.items()):
        orden = sorted(ds, key=lambda z: dt.date.fromisoformat(z).weekday() < 2)
        hay = False
        for dia in orden:
            if dt.date.fromisoformat(dia).weekday() < 2 and not hay and leg != "8":
                continue
            p = bajar(dia)
            if p:
                hay = True
                rutas.append(p)
    rutas.sort()
    print(f"\n{len(rutas)} sesiones con votaciones nominales", file=sys.stderr)
    return rutas


def norm(t):
    t = unicodedata.normalize("NFKD", (t or "").replace("ß", "ss")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", t)


def periodo(m):
    md = m.get("memberDuring") or {}
    return md.get("startDate", ""), md.get("endDate", "") or "9999-12-31"


def org_label(cache, org):
    oid = org.rsplit("/", 1)[-1]
    d = api(cache, f"org/{oid}.json", f"corporate-bodies/{oid}")
    x = ((d or {}).get("data") or [{}])[0]
    pref = x.get("prefLabel") or {}
    alt = x.get("altLabel") or {}
    lab = (pref.get("es") or pref.get("en") or pref.get("fr") or x.get("label") or oid) if isinstance(pref, dict) else (pref or oid)
    corto = x.get("label") or (alt.get("en") or alt.get("fr") or "" if isinstance(alt, dict) else alt) or lab
    return {"label": lab, "corto": corto}


def eurodiputados_es(leg, cache):
    """Eurodiputados de España en la legislatura (API v2): mandatos, partidos nacionales y grupos con fechas."""
    lista = api(cache, f"meps_es.json", f"meps?parliamentary-term={leg}&country-of-representation=ES&offset=0&limit=500")
    out = []
    ini, fin = TERMS[leg]
    for x in (lista or {}).get("data", []):
        pid = x["identifier"]
        d = api(cache, f"meps/{pid}.json", f"meps/{pid}")
        m = ((d or {}).get("data") or [{}])[0]
        mand, partidos, grupos = [], [], []
        for h in m.get("hasMembership") or []:
            a, b = periodo(h)
            if b < ini or a > fin:
                continue
            cls = (h.get("membershipClassification") or "").rsplit("/", 1)[-1]
            rol = (h.get("role") or "").rsplit("/", 1)[-1]
            if h.get("organization") == f"org/ep-{leg}" and rol == "MEMBER_PARLIAMENT" \
                    and any(r.endswith("/ESP") for r in h.get("represents") or []):
                mand.append((max(a, ini), min(b, fin)))
            elif cls == "NATIONAL_POLITICAL_GROUP":
                partidos.append((max(a, ini), min(b, fin), org_label(cache, h["organization"])["label"]))
            elif cls == "EU_POLITICAL_GROUP":
                grupos.append((max(a, ini), min(b, fin), org_label(cache, h["organization"])))
        fam, nom = m.get("familyName") or x.get("familyName", ""), m.get("givenName") or x.get("givenName", "")
        out.append({"id": int(pid), "fam": fam, "nom": nom, "nombre": f"{(m.get('upperFamilyName') or fam.upper())}, {nom}",
                    "mandatos": sorted(mand), "partidos": sorted(partidos), "grupos": sorted(grupos, key=lambda g: g[:2])})
    return out


def en(periodos, dia):
    return any(p[0] <= dia <= p[1] for p in periodos)


def a_la_fecha(periodos, dia):
    """Elemento vigente en la fecha (el último que empezó, si se solapan)."""
    vig = [p for p in periodos if p[0] <= dia <= p[1]]
    return vig[-1] if vig else None


def toks(t):
    # sin las conjunciones de los apellidos compuestos ("Junqueras i Vies" ~ "Junqueras Vies")
    return [norm(x) for x in re.split(r"[\s\-]+", t or "") if norm(x) and norm(x) not in ("i", "y")]


def grupo_en(e, dia):
    g = a_la_fecha([(x, y, z["corto"]) for x, y, z in e.get("grupos", [])], dia)
    return GRUPOS.get(g[2], g[2]) if g else ""


def identificar(votos, meps):
    """Asocia el MepId interno del anexo (no es el PersId de la API) con cada eurodiputado español.
    El acta da solo el apellido con que vota cada uno (a veces los dos apellidos, a veces nombre y apellido para
    desambiguar) y su grupo. Entre los españoles con mandato en esa fecha se busca: 1) coincidencia exacta con
    apellidos, nombre + apellidos o un alias; 2) si no hay, que una forma sea prolongación de la otra por palabras
    completas ("Aguilera García" ~ "Aguilera") y que coincida el grupo político. Solo cuentan las coincidencias
    únicas; luego se fija por mayoría el PersId de cada MepId y se usa en todas las votaciones."""
    formas = []
    for e in meps:
        fs = [toks(e["fam"]), toks(e["nom"]) + toks(e["fam"])] + [toks(a) for a in ALIAS.get(e["id"], ())]
        formas.append((e, fs))
    exactas = {}
    for e, fs in formas:
        for f in fs:
            exactas.setdefault(" ".join(f), []).append(e)
    cuenta, memo = {}, {}
    for v in votos:
        for mid, nom, grp, pos in v["miembros"]:
            clave = (nom, grp, v["d"])
            if clave not in memo:
                tl = toks(nom)
                cand = [e for e in exactas.get(" ".join(tl), []) if en(e["mandatos"], v["d"])]
                if not cand and tl:
                    cand = [e for e, fs in formas if en(e["mandatos"], v["d"]) and grupo_en(e, v["d"]) == grp
                            and (any(len(f) and tl[:len(f)] == f for f in fs)
                                 or (len("".join(tl)) >= 4 and toks(e["fam"])[:len(tl)] == tl))]
                memo[clave] = cand[0]["id"] if len(cand) == 1 else None
            if memo[clave]:
                c = cuenta.setdefault(mid, {})
                c[memo[clave]] = c.get(memo[clave], 0) + 1
    mapa = {}
    for mid, c in cuenta.items():
        pid, n = max(c.items(), key=lambda x: x[1])
        if n >= 0.9 * sum(c.values()):
            mapa[mid] = pid
        else:
            print(f"AVISO: MepId {mid} ambiguo {c}", file=sys.stderr)
    # un mismo eurodiputado no puede figurar con dos MepId en la misma votación (sería un homónimo extranjero)
    dobles = set()
    for v in votos:
        vistos = {}
        for mid, nom, grp, pos in v["miembros"]:
            if mid in mapa:
                if mapa[mid] in vistos and vistos[mapa[mid]] != mid:
                    dobles.add((mapa[mid], vistos[mapa[mid]], mid))
                vistos[mapa[mid]] = mid
    for pid, m1, m2 in sorted(dobles):
        print(f"AVISO: el eurodiputado {pid} aparece con dos MepId ({m1}, {m2}) en una misma votación", file=sys.stderr)
    return mapa


def descargar_vot(leg, cache, dias):
    """Anexo de resultados de votación (PV-VOT, francés) de cada día con votaciones nominales."""
    d = os.path.join(cache, "vot")
    os.makedirs(d, exist_ok=True)
    faltan_p = os.path.join(d, "_sin_vot.txt")
    faltan = set(open(faltan_p).read().split()) if os.path.exists(faltan_p) else set()
    rutas = []
    for dia in sorted(dias):
        pid = f"PV-{leg}-{dia}-VOT"
        p = os.path.join(d, pid + ".xml.gz")
        if not os.path.exists(p) and dia not in faltan:
            print(f"\r{pid}   ", end="", file=sys.stderr)
            raw = get(VOT.format(id=pid), pausa=PAUSA_RCV)
            if raw and b"Vote.Result" in raw[:5000]:
                with gzip.open(p + ".tmp", "wb") as f:
                    f.write(raw)
                os.replace(p + ".tmp", p)
            else:
                faltan.add(dia)
                with open(faltan_p, "a") as f:
                    f.write(dia + "\n")
        if os.path.exists(p):
            rutas.append(p)
    return rutas


def acuerdos_provisionales(ruta):
    """{(día, doc, s, n, a): objeto}: filas del anexo VOT votadas por llamamiento nominal cuyo objeto es un
    acuerdo provisional ("Accord provisoire", 8.ª) o el texto en su conjunto votado como bloque de compromiso
    ("Ensemble du texte bloc n° 1 - compromis", 6.ª-7.ª). El acuerdo de trílogo se vota como una enmienda o un
    bloque de enmiendas («Am 271») y el anexo RCV no dice que es la votación del texto completo."""
    import xml.etree.ElementTree as ET
    dia = re.search(r"(\d{4}-\d\d-\d\d)", os.path.basename(ruta))[1]
    with gzip.open(ruta) as f:
        raiz = ET.parse(f).getroot()
    out = {}
    for r in raiz.iter("Vote.Result"):
        cab = " ".join("".join(e.itertext()) for e in r if e.tag in ("Vote.Result.Text.Title", "Vote.Result.Description.Text"))
        docs = analizar_desc(cab)[0]
        seccion = ""
        for tr in r.iter("TR"):
            celdas = [" ".join("".join(td.itertext()).split()) for td in tr.findall("TD")]
            tot = {k: tr.find(f".//Vote.Result.Table.TotalVote.{k}") for k in ("For", "Against", "Abstention")}
            if len(celdas) == 1 or (celdas and not any(celdas[1:])):
                seccion = celdas[0]
                continue
            if not celdas:
                continue
            if tot["For"] is not None:
                try:
                    clave = tuple(int((tot[k].text or "0").strip()) for k in ("For", "Against", "Abstention"))
                except (ValueError, AttributeError):
                    continue
            else:  # en la 6.ª los totales van como texto: "529,98,24"
                m = re.search(r"(?<![\d,])(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?![\d,])", celdas[-1])
                if not m:
                    continue
                clave = tuple(int(x) for x in m.groups())
            objet = celdas[0] or seccion
            po = plano(objet)
            if po.startswith("accord provisoire") or plano(seccion).startswith("accord provisoire") \
                    or "paquet de compromis" in po \
                    or (po.startswith("ensemble du texte") and ("bloc" in po or "compromis" in po
                                                                 or (len(celdas) > 1 and celdas[1]))):
                for doc in docs:
                    out[(dia, doc) + clave] = "Accord provisoire" if "accord" in po or not po else " ".join(objet.split())
    return out


POSICIONES = {"Result.For": "s", "Result.Against": "n", "Result.Abstention": "a"}
RE_HORA = re.compile(r"\s*(\d\d)/(\d\d)/(\d{4}) (\d\d:\d\d)(:\d\d)?(\.\d+)?\s*$")


def leer_rcv(ruta):
    """Votaciones de un anexo RCV: [{id, d, hora, desc, refs, cuenta{s,n,a}, miembros[(MepId, nombre, grupo, pos)]}].
    Hay dos formatos: hasta 2017 cada votación trae Identifier y Date con hora; después solo Number y la hora
    va al final de la descripción. Se ignoran las votaciones secretas y las correcciones de voto (son
    intenciones posteriores que no cambian el resultado oficial)."""
    import xml.etree.ElementTree as ET
    dia = re.search(r"(\d{4}-\d\d-\d\d)", os.path.basename(ruta))[1]
    with gzip.open(ruta) as f:
        raiz = ET.parse(f).getroot()
    out = []
    for r in raiz.iter("RollCallVote.Result"):
        desc_el = r.find("RollCallVote.Description.Text")
        desc = " ".join("".join(desc_el.itertext()).split()) if desc_el is not None else ""
        hora = ""
        m = RE_HORA.search(desc)
        if m:
            hora, desc = m[4] + (m[5] or ":00"), desc[:m.start()].strip()
        elif " " in (r.get("Date") or ""):
            hora = r.get("Date").split(" ")[1][:8]
        if hora and int(hora[:2]) < 8:  # algunos anexos usan reloj de 12 h sin a. m./p. m. ("01:14" = 13:14)
            hora = "%02d%s" % (int(hora[:2]) + 12, hora[2:])
        if r.get("Identifier"):
            vid = int(r.get("Identifier"))
        else:
            vid = int(dia.replace("-", "") + "%03d" % int(re.sub(r"\D", "", r.get("Number") or "0") or 0))
        cuenta, miembros = {"s": 0, "n": 0, "a": 0}, []
        for tag, pos in POSICIONES.items():
            el = r.find(tag)
            if el is None:
                continue
            cuenta[pos] = int(el.get("Number") or 0)
            for g in el.findall("Result.PoliticalGroup.List"):
                for mm in g:
                    if mm.tag.endswith("Member.Name"):
                        miembros.append((mm.get("MepId") or "", " ".join("".join(mm.itertext()).split()),
                                         g.get("Identifier") or "", pos))
        if r.find("Result.Secret") is not None and not miembros:
            continue
        out.append({"id": vid, "d": dia, "hora": hora[:5], "seg": hora, "desc": desc, "cuenta": cuenta, "miembros": miembros})
    return out


RE_DOC = re.compile(r"\b(RC-)?([ABC])(\d)-(\d{4})/(\d{4})")
# descripciones (en francés, como en el acta) de las votaciones de conjunto de un texto: se comparan sin tildes,
# en minúsculas y por el comienzo del último tramo de la descripción
PRINCIPALES = ("vote unique", "resolution legislative", "resolution", "proposition de resolution", "ensemble du texte",
               "proposition de la commission", "proposition commission", "proposition modifiee", "vote: proposition",
               "vote : proposition", "decision", "proposition de decision", "projet de decision", "approbation",
               "procedure d'approbation", "accord provisoire", "projet du conseil", "projet commun", "texte commun",
               "position du conseil", "recommandation", "proposition de recommandation", "proposition de rejet",
               "rejet", "demande de decision d'urgence", "demandes de decision d'urgence",
               "decision d'engager des negociations", "projet de budget", "proposition de reglement",
               "proposition de directive", "projet de reglement", "projet de directive", "projet d'accord")
NO_CLAVE = ("proposition de rejet", "rejet", "demande de decision d'urgence", "demandes de decision d'urgence",
            "decision d'engager des negociations")
RE_ENMIENDA = re.compile(r"(^|\W)(am|ams|amendement|amendements|par|cons|considerant|visa|bloc|annexe|article|"
                         r"point|tiret|alinea)(\W|\d|$)|§|/\d{1,2}\s*$|\d+\s*(ere|eme|e) partie")


def plano(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().strip()


def analizar_desc(desc):
    """(documentos citados en formato de la API, tramo final de la descripción)."""
    docs = []
    for rc, l, t, num, anio in RE_DOC.findall(desc):
        docs.append(f"{'RC-' if rc else ''}{l}-{t}-{anio}-{num}")
    sub = desc.split(" - ")[-1].strip() if " - " in desc else desc
    return docs, sub


def es_principal(sub):
    p = plano(sub)
    return p.startswith(PRINCIPALES) and not RE_ENMIENDA.search(p)


def procs_de_sesion(cache, dia):
    """doc -> procedimiento ('2011-0135') según los resultados de votación de la sesión (API v2)."""
    d = api(cache, f"vote-results/{dia}.json", f"meetings/MTG-PL-{dia}/vote-results?offset=0&limit=1000")
    out = {}
    for x in (d or {}).get("data", []):
        procs = [i["id"].rsplit("/", 1)[-1] for i in x.get("inverse_consists_of") or [] if "/proc/" in i["id"]]
        for doc in x.get("based_on_a_realization_of") or []:
            if procs:
                out.setdefault(doc.rsplit("/", 1)[-1], (procs[0], (x.get("activity_label") or {}).get("fr", "")))
    return out


def proc_de_doc(cache, doc):
    if doc.startswith("RC-"):
        return ""
    d = api(cache, f"docs/{doc}.json", f"plenary-documents/{doc}")
    x = ((d or {}).get("data") or [{}])[0]
    procs = [p.rsplit("/", 1)[-1] for p in x.get("inverse_created_a_realization_of") or [] if "/proc/" in p]
    return procs[0] if procs else ""


def procedimiento(cache, pid, pista="", docs=()):
    """Referencia (2011/0135(COD)), tipo, títulos e hitos del procedimiento desde la API v2."""
    d = api(cache, f"procedimientos/{pid}.json", f"procedures/{pid}")
    x = ((d or {}).get("data") or [{}])[0]
    t = x.get("process_title") or {}
    tipo, ref = x.get("process_type") or "", x.get("label") or ""
    if isinstance(ref, list) or isinstance(tipo, list):
        # número compartido por dos procedimientos (p. ej. 2018/0900): se toma el primero de la API
        # número compartido por dos procedimientos (p. ej. 2018/0900): se elige por el título del punto votado
        refs = ref if isinstance(ref, list) else [ref]
        tits = t.get("fr") if isinstance(t.get("fr"), list) else [t.get("fr", "")]
        pal = set(plano(pista or "").split())
        i = max(range(len(tits)), key=lambda j: len(pal & set(plano(tits[j] or "").split()))) if tits else 0
        t = {k: (v[i] if isinstance(v, list) and i < len(v) else v[0] if isinstance(v, list) else v) for k, v in t.items()}
        # la etiqueta que acompaña a ese título: la API da etiquetas y títulos en órdenes distintos, así que se
        # empareja por tipo (el título de un proyecto de decisión del Consejo Europeo es NLE; si no, COD)
        ref = next((r for r in refs if ("(NLE)" in r) == plano(t.get("fr", "")).startswith("projet de decision du conseil europeen")), refs[0])
        tipo = ref.split("(")[-1].rstrip(")")
    tipo = tipo.rsplit("/", 1)[-1]
    if not re.match(r"\d{4}/\d{4}\([A-Z]+\)", ref):
        ref = f"{pid[:4]}/{pid[5:]}({tipo})"
    if not x:  # procedimientos que la API no tiene (404): tipo comprobado a mano en el OEIL
        tipo = TIPO_SIN_API.get(pid, "")
        ref = f"{pid[:4]}/{pid[5:]}({tipo})"
        for doc in docs:  # título del informe votado ("INFORME sobre la propuesta de ...")
            dd = api(cache, f"docs/{doc}.json", f"plenary-documents/{doc}")
            td = (((dd or {}).get("data") or [{}])[0].get("title_dcterms") or {})
            if td:
                t = {k: re.sub(r"^(INFORME|REPORT|RAPPORT|RECOMENDACIÓN|RECOMMENDATION)(\s+(PROVISIONAL|INTERIM|INTÉRIMAIRE))?\s+(sobre|on|sur)\s+(el|la|los|las|the|le|les|l')?\s*",
                               "", v, flags=re.I) for k, v in td.items()}
                t = {k: v[:1].upper() + v[1:] for k, v in t.items()}
                break
    tipo = tipo or ref.split("(")[-1].rstrip(")")
    val = {"ref": ref, "tipo": tipo, "es": t.get("es", ""), "en": t.get("en", ""), "fr": t.get("fr", ""),
           "firma": "", "doue": "",
           "ta": sorted(d.rsplit("/", 1)[-1] for d in x.get("created_a_realization_of") or [] if "/TA-" in d)}
    for ev in x.get("consists_of") or []:
        tp = (ev.get("had_activity_type") or "").rsplit("/", 1)[-1]
        if tp == "SIGNATURE":
            val["firma"] = max(val["firma"], ev.get("activity_date", ""))
        elif tp == "PUBLICATION_OFFICIAL_JOURNAL":
            val["doue"] = max(val["doue"], ev.get("activity_date", ""))
    return val


PARLTRACK = "https://parltrack.org/dumps/ep_votes.json.zst"
POS_PT = {"+": "s", "-": "n", "0": "a"}


def votos_parltrack(leg, cache, dias_oficiales):
    """Votaciones de las sesiones que faltan en la distribución oficial, desde el volcado de Parltrack
    (ODbL), que las extrajo en su día de los mismos XML oficiales (RegData) y ya resolvió cada eurodiputado
    a su PersId. Se descomprime con la orden `zstd` y se guarda un extracto de la legislatura en la caché."""
    import subprocess
    ini, fin = TERMS[leg]
    ext = os.path.join(cache, "parltrack", f"votos_{leg}.json.gz")
    if not os.path.exists(ext):
        zst = os.path.join(cache, "parltrack", "ep_votes.json.zst")
        os.makedirs(os.path.dirname(zst), exist_ok=True)
        if not os.path.exists(zst):
            print("Descargando el volcado de votaciones de Parltrack (~11 MB)...", file=sys.stderr)
            raw = get(PARLTRACK)
            with open(zst + ".tmp", "wb") as f:
                f.write(raw)
            os.replace(zst + ".tmp", zst)
        todo = json.loads(subprocess.run(["zstd", "-dc", zst], check=True, capture_output=True).stdout)
        sel = [v for v in todo if ini <= v["ts"][:10] <= fin]
        del todo
        with gzip.open(ext + ".tmp", "wt", encoding="utf-8") as f:
            json.dump(sel, f, ensure_ascii=False)
        os.replace(ext + ".tmp", ext)
    with gzip.open(ext, "rt", encoding="utf-8") as f:
        sel = json.load(f)
    out = []
    for v in sel:
        dia = v["ts"][:10]
        if dia in dias_oficiales or not v.get("votes"):
            continue
        cuenta, miembros = {"s": 0, "n": 0, "a": 0}, []
        for k, pos in POS_PT.items():
            x = v["votes"].get(k) or {}
            cuenta[pos] = int(x.get("total") or 0)
            for grp, lista in (x.get("groups") or {}).items():
                miembros.extend((f"P{m['mepid']}", m.get("name", ""), grp, pos) for m in lista if "mepid" in m)
        out.append({"id": int(v["voteid"]), "d": dia, "hora": v["ts"][11:16], "seg": v["ts"][11:19], "desc": " ".join(v["title"].split()),
                    "cuenta": cuenta, "miembros": miembros, "epref": v.get("epref") or [], "pt": True})
    return out


def texto_aprobado(tas, dia):
    """'TA-8-2016-0177' -> 'P8_TA(2016)0177'; si hay varios, el último del año de la votación clave."""
    del_anio = [t for t in tas if t.split("-")[2] == dia[:4]] or tas
    if not del_anio:
        return ""
    _, leg, anio, num = del_anio[-1].split("-")
    return f"P{leg}_TA({anio}){num}"


def escanos(leg, dia):
    """Escaños del Pleno en la fecha (para 'noVotan'; no descuenta vacantes)."""
    if leg == "6":
        return 732 if dia < "2007-01-01" else 785
    if leg == "7":
        return 736 if dia < "2011-12-01" else 754 if dia < "2013-07-01" else 766
    return 751


def fecha(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}" if iso and iso < "9999" else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--leg", required=True, choices=sorted(TERMS), help="legislatura (6, 7 u 8)")
    ap.add_argument("--solo-descarga", action="store_true", help="solo bajar los anexos de votación nominal")
    a = ap.parse_args()
    leg = a.leg
    ini, fin = TERMS[leg]
    cache = os.path.join(ROOT, "data", "cache", f"europarlamento_{leg}")
    salida = os.path.join(ROOT, "data", "fuente", f"europarlamento_{leg}.json")
    rutas = descargar_rcv(leg, cache)
    if a.solo_descarga:
        return

    # 1. todas las votaciones nominales de la legislatura
    votos = []
    for r in rutas:
        votos.extend(leer_rcv(r))
    dias_of = {v["d"] for v in votos}
    print(f"{len(votos)} votaciones nominales en {len(rutas)} sesiones (distribución oficial)", file=sys.stderr)
    if leg in PARLTRACK_LEGS:
        extra = votos_parltrack(leg, cache, dias_of)
        print(f"+ {len(extra)} votaciones de {len({v['d'] for v in extra})} sesiones desde Parltrack", file=sys.stderr)
        votos.extend(extra)
    votos.sort(key=lambda v: (v["d"], v.get("seg", v["hora"]), v["id"]))

    # acuerdos provisionales votados como enmienda (anexo VOT)
    acuerdos = {}
    for r in descargar_vot(leg, cache, {v["d"] for v in votos}):
        acuerdos.update(acuerdos_provisionales(r))
    for v in votos:
        docs, sub = analizar_desc(v["desc"])
        c = v["cuenta"]
        ac = next((acuerdos[k] for k in ((v["d"], d, c["s"], c["n"], c["a"]) for d in docs) if k in acuerdos), "")
        if ac and not es_principal(sub):
            v["acuerdo"] = f"{ac} - {sub}"
    # solo cuenta como votación de conjunto si es la última del texto ese día y no la sigue ninguna votación
    # de conjunto (en primera lectura, los bloques del "paquet de compromis" van seguidos de la resolución)
    ultimo = {}
    for v in votos:
        for doc in analizar_desc(v["desc"])[0]:
            if v.get("acuerdo") or es_principal(analizar_desc(v["desc"])[1]):
                ultimo[(v["d"], doc)] = v["id"]
    for v in votos:
        if v.get("acuerdo") and all(ultimo.get((v["d"], doc)) != v["id"] for doc in analizar_desc(v["desc"])[0]):
            del v["acuerdo"]
    print(f"{sum('acuerdo' in v for v in votos)} acuerdos provisionales votados como enmienda", file=sys.stderr)

    # 2. eurodiputados españoles (API) y su MepId en las actas
    meps = eurodiputados_es(leg, cache)
    por_id = {e["id"]: e for e in meps}
    mapa = identificar([v for v in votos if not v.get("pt")], meps)
    mapa.update({f"P{e['id']}": e["id"] for e in meps})
    sin = [e["nombre"] for e in meps if e["id"] not in mapa.values()]
    print(f"{len(meps)} eurodiputados españoles; {len(set(mapa.values()))} identificados en las actas"
          + (f"; sin identificar: {sin}" if sin else ""), file=sys.stderr)

    # 3. votaciones de conjunto ligadas a un procedimiento
    principales, doc_proc, dias_vistos, pistas = [], {}, set(), {}
    for i, v in enumerate(votos):
        docs, sub = analizar_desc(v["desc"])
        sub = v.get("acuerdo", sub)
        if not docs or not (v.get("acuerdo") or es_principal(sub)):
            continue
        if v["d"] not in dias_vistos:
            print(f"\rprocedimientos: {v['d']}", end="", file=sys.stderr)
            dias_vistos.add(v["d"])
            for k, pr in procs_de_sesion(cache, v["d"]).items():
                doc_proc.setdefault(k, pr[0])
                pistas.setdefault(pr[0], pr[1])
        pid = next((doc_proc[d] for d in docs if d in doc_proc), "")
        if not pid and v.get("epref"):
            pid = v["epref"][0].split("(")[0].replace("/", "-")
        if not pid:
            for d in docs:
                pid = doc_proc.setdefault(d, proc_de_doc(cache, d))
                if pid:
                    break
        if pid:
            v["proc"], v["sub"], v["docs"] = pid, sub, docs
            principales.append(v)
    print(file=sys.stderr)
    por_proc = {}
    for v in principales:
        por_proc.setdefault(v["proc"], []).append(v)
    info = {}
    for i, pid in enumerate(sorted(por_proc)):
        print(f"\r{i + 1}/{len(por_proc)} procedimiento {pid}   ", end="", file=sys.stderr)
        info[pid] = procedimiento(cache, pid, pistas.get(pid, ""), sorted({d for v in por_proc[pid] for d in v["docs"]}))
    print(file=sys.stderr)
    clave = {}
    for pid, vs in por_proc.items():
        buenas = [v for v in vs if not plano(v["sub"]).startswith(NO_CLAVE)]
        clave[pid] = (buenas or vs)[-1]["id"]

    # 4. salida
    def corto(nombre, lab):
        for (ape, et), p in POR_PERSONA.items():
            if et == lab and nombre.startswith(ape):
                return p
        return PARTIDOS.get(lab, lab)

    def partido(e, dia):
        p = a_la_fecha(e["partidos"], dia)
        return corto(e["nombre"], p[2]) if p else "Sin partido"

    procedimientos, votaciones, cuenta_mep = [], [], {}
    for pid, vs in sorted(por_proc.items(), key=lambda x: info[x[0]]["ref"]):
        k = next(v for v in vs if v["id"] == clave[pid])
        pi = info[pid]
        res = lambda v: "Aprobado" if v["cuenta"]["s"] > v["cuenta"]["n"] else "Rechazado"
        procedimientos.append({
            "exp": pi["ref"], "tipo": pi["tipo"], "tipo_txt": TIPOS.get(pi["tipo"], pi["tipo"]),
            "legislativo": pi["tipo"] in LEGISLATIVOS, "tit": pi["es"] or pi["en"] or pi["fr"],
            "tit_en": pi["en"] or pi["fr"], "d": fecha(k["d"]), "res": res(k), "firma": fecha(pi["firma"]),
            "doue": fecha(pi["doue"]), "ta": texto_aprobado(pi["ta"], k["d"]), "nvot": k["id"], "nvotaciones": len(vs)})
    for v in principales:
        pi = info[v["proc"]]
        voto_es = {}
        for mid, nom, grp, pos in v["miembros"]:
            pid = mapa.get(mid)
            if pid and en(por_id[pid]["mandatos"], v["d"]):
                voto_es[pid] = pos
        g, mx = {}, {}
        activos = [e for e in meps if en(e["mandatos"], v["d"])]
        for e in sorted(activos, key=lambda e: e["nombre"]):
            pos = voto_es.get(e["id"], "nv")
            c = g.setdefault(partido(e, v["d"]), {"s": 0, "n": 0, "a": 0, "nv": 0})
            c[pos] += 1
            mx[e["nombre"]] = VOTO[pos]
            cuenta_mep.setdefault(e["id"], []).append(v["d"])
        s_, n_, a_ = v["cuenta"]["s"], v["cuenta"]["n"], v["cuenta"]["a"]
        votaciones.append({
            "exp": pi["ref"], "d": fecha(v["d"]), "hora": v["hora"], "nv": v["id"],
            "tit": v["desc"], "txt": pi["es"] or pi["en"] or pi["fr"], "sub": v["sub"],
            "ref": " ".join(v["docs"]), "etapa": "",
            "res": "Aprobado" if s_ > n_ else "Rechazado", "clave": v["id"] == clave[v["proc"]],
            "tot": {"presentes": s_ + n_ + a_, "afavor": s_, "enContra": n_, "abstenciones": a_,
                    "noVotan": max(escanos(leg, v["d"]) - s_ - n_ - a_, 0)},
            "g": dict(sorted(g.items(), key=lambda x: -sum(x[1].values()))), "mx": mx})

    eurodiputados = []
    for e in sorted(meps, key=lambda e: e["nombre"]):
        tramos = e["partidos"] or [(e["mandatos"][0][0] if e["mandatos"] else ini, fin, "Sin partido")]
        for a_, b_, lab in tramos:
            gr = a_la_fecha([(x, y, z["corto"]) for x, y, z in e["grupos"]], max(a_, ini))
            eurodiputados.append({
                "id": e["id"], "nombre": e["nombre"], "partido": corto(e["nombre"], lab), "partido_oficial": lab,
                "grupo": GRUPOS.get(gr[2], gr[2]) if gr else "", "desde": fecha(a_), "hasta": fecha(b_),
                "votos": sum(a_ <= f <= b_ for f in cuenta_mep.get(e["id"], []))})

    out = {"generado": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
           "fuente": "Parlamento Europeo, datos abiertos (data.europarl.europa.eu): anexos de votación nominal "
                     "del acta (PV-RCV, XML) y API v2 (eurodiputados, partidos nacionales, resultados de votación, "
                     "documentos y procedimientos)",
           "legislatura": leg, "desde": fecha(ini), "hasta": fecha(fin), "procedimientos": procedimientos,
           "votaciones": votaciones, "eurodiputados": eurodiputados}
    with open(salida + ".tmp", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(salida + ".tmp", salida)
    nleg = sum(p["legislativo"] for p in procedimientos)
    print(f"{salida}: {len(procedimientos)} procedimientos ({nleg} legislativos), {len(votaciones)} votaciones, "
          f"{len({e['id'] for e in eurodiputados})} eurodiputados españoles", file=sys.stderr)


if __name__ == "__main__":
    main()
