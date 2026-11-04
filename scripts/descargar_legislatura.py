"""Descarga iniciativas legislativas y votaciones del Pleno de una legislatura desde congreso.es.

Sirve para legislaturas cerradas (el Congreso solo publica el fichero de iniciativas de la legislatura
en curso): recorre las fichas de iniciativa por número de expediente y los zips diarios de votaciones.

Uso:
  python3 scripts/descargar_legislatura.py --leg XIV --desde 2019-12-03 --hasta 2023-05-30
  python3 scripts/descargar_legislatura.py --leg XIV --solo iniciativas      # por partes
  python3 scripts/descargar_legislatura.py --leg XIV --desde ... --hasta ... --solo votaciones

Es REANUDABLE: cada respuesta se guarda en data/cache/<leg>/ (ignorado por git). Si se corta o el
Congreso devuelve 403, vuelve a lanzar el mismo comando más tarde y seguirá donde lo dejó.

Protección anti-bots (Akamai): una sola petición cada ~2,5 s, nunca en paralelo, y parada ante un 403.

Salida: data/fuente/congreso_<leg>.json con
  proyectos / proposiciones / rdl: fichas (NUMEXPEDIENTE, TIPO, OBJETO, AUTOR, FECHAPRESENTACION,
      RESULTADOTRAMITACION, SITUACIONACTUAL, BOLETINES)
  votaciones: una entrada por votación del Pleno (mismo formato que congreso_xv.json)
"""
import argparse, datetime as dt, html, http.client, http.cookiejar, io, json, os, random, re, ssl, sys, time, zipfile
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, HTTPSHandler, Request, build_opener

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "https://www.congreso.es"
UA = {"User-Agent": "Mozilla/5.0 (proyecto ciudadano vota-bien; datos abiertos)"}
PAUSA = 2.5
LEG_NUM = {"X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15}
# tipos de expediente legislativo: 120 iniciativa popular, 121 proyectos, 122 proposiciones de grupos,
# 123 del Senado, 124 de comunidades autónomas, 125 iniciativa legislativa popular, 130 reales decretos-ley
TIPOS = ["121", "122", "123", "124", "125", "120", "130"]
FALLOS_SEGUIDOS = 8  # expedientes inexistentes consecutivos para dar por terminada una serie

try:  # algunos Python (p. ej. el de PlatformIO o el de python.org en macOS) no traen certificados raíz
    import certifi
    _ssl = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl = ssl.create_default_context()
opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()), HTTPSHandler(context=_ssl))
_ultima = [0.0]


def get(path, binary=False):
    espera = PAUSA + random.uniform(0, 0.8) - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    for intento in range(6):
        try:
            _ultima[0] = time.time()
            with opener.open(Request(BASE + path, headers=UA), timeout=60) as r:
                data = r.read()
                return data if binary else data.decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code == 403:
                sys.exit(f"\n403 en {path}: bloqueo anti-bots. Espera 30-60 min y relanza el mismo comando.")
            if e.code == 404:
                return None
            if intento == 5:
                raise
            err = e
        except (URLError, TimeoutError, ConnectionError, http.client.HTTPException) as e:
            # cortes de conexión sueltos: esperar cada vez más (1, 2, 4, 8, 16 min)
            if intento == 5:
                raise
            err = e
        espera = 60 * 2 ** intento
        print(f"\n{type(err).__name__} en {path[:80]}; reintento en {espera // 60} min", file=sys.stderr)
        time.sleep(espera)


def cached(path, fn):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    val = fn()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(val, f, ensure_ascii=False)
    os.replace(path + ".tmp", path)
    return val


# ---------------------------------------------------------------- iniciativas
def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def ficha(leg, exp):
    h = get("/es/busqueda-de-iniciativas?p_p_id=iniciativas&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view"
            f"&_iniciativas_mode=mostrarDetalle&_iniciativas_legislatura={leg}&_iniciativas_id={quote(exp, safe='')}")
    if not h or "entradilla-iniciativa" not in h:
        return None
    body = h[h.find("cuerpo-iniciativa-det"):]
    m = lambda pat: (re.search(pat, body, re.S) or [None, ""])[1]
    entr = txt(m(r'class="entradilla-iniciativa">(.*?)</div>'))
    objeto = re.sub(r"\s*\(\d{3}/\d{6}\)\s*$", "", entr)
    autor_blk = m(r"<h3>\s*Autor\s*</h3>(.*?)<h3")
    autores = [txt(a) for a in re.findall(r"<li>(.*?)</li>", autor_blk, re.S)] or [txt(autor_blk)]
    tram = [txt(x) for x in re.split(r"<br\s*/?>", m(r'class="iniciativaTramitacion">(.*?)</div>')) if txt(x)]
    boletines = []
    for li in re.findall(r"<li>(.*?)</li>", m(r'<ul class="boletines">(.*?)</ul>'), re.S):
        pdf = re.search(r'href="([^"]+\.PDF[^"]*)"', li, re.I)
        boletines.append({"desc": txt(li.split("</div>")[0]), "pdf": pdf.group(1) if pdf else ""})
    return {
        "NUMEXPEDIENTE": exp,
        "TIPO": txt(m(r'<h2 class="titular-seccion"[^>]*>(.*?)</h2>')).rstrip("."),
        "OBJETO": objeto,
        "AUTOR": "; ".join(a for a in autores if a),
        "FECHAPRESENTACION": (re.search(r"Presentado el (\d{2}/\d{2}/\d{4})", txt(m(r'class="f-present">(.*?)</div>'))) or [None, ""])[1],
        "RESULTADOTRAMITACION": txt(m(r'class="resultadoTramitacion">(.*?)</div>')),
        "SITUACIONACTUAL": tram[-1] if tram else "",
        "BOLETINES": boletines,
    }


def iniciativas(leg, cache):
    out = {"proyectos": [], "proposiciones": [], "rdl": []}
    for tipo in TIPOS:
        n, fallos = 0, 0
        while fallos < FALLOS_SEGUIDOS:
            n += 1
            exp = f"{tipo}/{n:06d}"
            f = cached(os.path.join(cache, "iniciativas", exp.replace("/", "_") + ".json"), lambda: ficha(leg, exp))
            if f is None:
                fallos += 1
                continue
            fallos = 0
            key = "proyectos" if tipo == "121" else "rdl" if tipo == "130" else "proposiciones"
            out[key].append(f)
            print(f"\r{exp} {f['OBJETO'][:60]:60}", end="", file=sys.stderr)
        print(f"\n{tipo}: {n - fallos} expedientes revisados", file=sys.stderr)
    return out


# ---------------------------------------------------------------- votaciones
class DayParser(HTMLParser):
    """Asocia cada votación del día (VotacionNNN) al último número de expediente visto en la página."""

    def __init__(self, leg_num):
        super().__init__()
        self.leg = f"Leg{leg_num}"
        self.votes, self.zip, self.cur_exp, self.in_exp = {}, "", "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        href = a.get("href") or ""
        if tag == "a" and "n_exp" in (a.get("class") or ""):
            self.in_exp = True
        if tag == "a" and self.leg in href:
            if href.endswith(".zip"):
                self.zip = href
            m = re.search(r"Votacion(\d+)/[^/]+\.json$", href)
            if m:
                self.votes[int(m.group(1))] = self.cur_exp

    def handle_data(self, data):
        if self.in_exp:
            m = re.search(r"\d{3}/\d{6}", data)
            if m:
                self.cur_exp = m.group(0)
            self.in_exp = False


def dia(leg, d):
    h = get("/es/web/guest/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view"
            f"&targetLegislatura={leg}&targetDate={quote(d.strftime('%d/%m/%Y'), safe='')}")
    p = DayParser(LEG_NUM[leg])
    p.feed(h or "")
    return {"zip": p.zip, "exp": {str(k): v for k, v in p.votes.items()}}


def resumen_zip(raw, exps, ds):
    out = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in sorted(z.namelist()):
            if not name.lower().endswith(".json"):
                continue
            j = json.loads(z.read(name).decode("utf-8-sig"))
            info = j["informacion"]
            g = {}
            for x in j.get("votaciones", []):
                c = g.setdefault(x["grupo"], {"s": 0, "n": 0, "a": 0, "nv": 0})
                o = x["voto"]
                c["s" if o in ("Sí", "Si") else "n" if o == "No" else "a" if o.startswith("Abst") else "nv"] += 1
            out.append({
                "exp": exps.get(str(info["numeroVotacion"]), ""), "d": ds, "ses": info["sesion"],
                "nv": info["numeroVotacion"], "tit": info.get("titulo", ""), "txt": info.get("textoExpediente", ""),
                "sub": info.get("tituloSubGrupo", ""), "tot": j.get("totales", {}), "g": g,
                # voto nominal de los grupos donde conviven varios partidos (Mixto y, en la XIV, Plural)
                "mx": {x["diputado"]: x["voto"] for x in j.get("votaciones", []) if x["grupo"] in ("GMx", "GPlu")},
            })
    return sorted(out, key=lambda v: v["nv"])


def votaciones(leg, desde, hasta, cache):
    res, d, dias = [], desde, 0
    while d <= hasta:
        if d.weekday() < 5:  # lunes a viernes: hay plenos extraordinarios fuera de martes-jueves
            key = d.strftime("%Y%m%d")
            info = cached(os.path.join(cache, "dias", key + ".json"), lambda: dia(leg, d))
            if info["zip"]:
                ds = d.strftime("%d/%m/%Y")
                try:
                    vs = cached(os.path.join(cache, "votos", key + ".json"),
                                lambda: resumen_zip(get(info["zip"], binary=True), info["exp"], ds))
                except zipfile.BadZipFile:
                    # el Congreso sirve a veces un zip corrupto o una página de error: se salta ese día
                    # (no se cachea, así que se reintenta al relanzar) y se apunta en el log
                    print(f"\nAVISO {ds}: zip de votaciones corrupto ({info['zip']}); día omitido", file=sys.stderr)
                    vs = []
                res.extend(vs)
                dias += 1 if vs else 0
            print(f"\r{d} · {dias} días con pleno · {len(res)} votaciones", end="", file=sys.stderr)
        d += dt.timedelta(days=1)
    print(file=sys.stderr)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", required=True, choices=sorted(LEG_NUM))
    ap.add_argument("--desde", help="AAAA-MM-DD (necesario para votaciones)")
    ap.add_argument("--hasta", help="AAAA-MM-DD (necesario para votaciones)")
    ap.add_argument("--solo", choices=["iniciativas", "votaciones"])
    ap.add_argument("--out")
    a = ap.parse_args()
    cache = os.path.join(ROOT, "data", "cache", a.leg.lower())
    out = a.out or os.path.join(ROOT, "data", "fuente", f"congreso_{a.leg.lower()}.json")
    data = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(), "fuente": "Congreso de los Diputados - datos abiertos",
            "legislatura": a.leg}
    if os.path.exists(out):  # conserva la parte no descargada en esta ejecución
        data = {**json.load(open(out, encoding="utf-8")), "generado": data["generado"]}
    if a.solo != "votaciones":
        data.update(iniciativas(a.leg, cache))
    if a.solo != "iniciativas":
        if not (a.desde and a.hasta):
            sys.exit("--desde y --hasta son necesarios para descargar votaciones")
        data["votaciones"] = votaciones(a.leg, dt.date.fromisoformat(a.desde), dt.date.fromisoformat(a.hasta), cache)
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("Guardado", out, {k: len(v) for k, v in data.items() if isinstance(v, list)}, file=sys.stderr)
