"""Descarga iniciativas y votaciones de una legislatura desde los datos abiertos del Congreso.

SIN PROBAR desde un ordenador normal: en la sesión original congreso.es estaba bloqueado
para el servidor y la descarga se hizo con JavaScript desde Chrome. Este script reproduce
la misma lógica en Python. Revísalo y pruébalo con un rango corto de fechas antes de lanzarlo entero.

IMPORTANTE: el Congreso usa protección anti-bots (Akamai). Peticiones en paralelo provocaron
un bloqueo temporal de la IP. Mantén SIEMPRE una petición cada 2-3 segundos y para ante un 403.

Uso:
  python3 scripts/scrape_congreso.py --leg XV --desde 2023-08-17 --hasta 2026-10-06 --out data/fuente/congreso_xv.json

Las iniciativas (proyectos, proposiciones, aprobadas) solo se publican como fichero para la
legislatura en curso; sus URLs cambian a diario y se leen de https://www.congreso.es/es/opendata/iniciativas
"""
import argparse, datetime as dt, json, re, sys, time
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote

BASE = "https://www.congreso.es"
UA = {"User-Agent": "Mozilla/5.0 (proyecto ciudadano; datos abiertos)"}
PAUSA = 2.5


def get(path):
    req = Request(BASE + path, headers=UA)
    try:
        with urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except HTTPError as e:
        if e.code == 403:
            sys.exit(f"403 en {path}: bloqueo anti-bots. Espera 30-60 min y reanuda.")
        raise


def iniciativas():
    html = get("/es/opendata/iniciativas")
    urls = sorted(set(re.findall(r'/webpublica/opendata/iniciativas/[^"\']+?\.json', html)))
    out = {}
    for key, pat in (("aprobadas", "IniciativasLegislativasAprobadas"), ("proyectos", "ProyectosDeLey"),
                     ("proposiciones", "ProposicionesDeLey")):
        u = next(x for x in urls if pat in x)
        j = json.loads(get(u))
        out[key] = j if isinstance(j, list) else list(j.values())[0]
        time.sleep(PAUSA)
    return out


class DayParser(HTMLParser):
    """Extrae, en orden, el número de expediente de cada tarjeta y los enlaces JSON de votación."""
    def __init__(self, leg_num):
        super().__init__()
        self.leg = f"Leg{leg_num}"
        self.votes, self.cur_exp, self.in_exp = [], "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "n_exp" in (a.get("class") or ""):
            self.in_exp = True
        href = a.get("href") or ""
        if tag == "a" and href.endswith(".json") and self.leg in href:
            self.votes.append({"href": href, "exp": self.cur_exp})

    def handle_data(self, data):
        if self.in_exp:
            m = re.search(r"\d{3}/\d{6}", data)
            if m:
                self.cur_exp = m.group(0)
            self.in_exp = False


def votaciones(leg, desde, hasta):
    leg_num = {"XIV": 14, "XV": 15}[leg]
    res, d = [], desde
    while d <= hasta:
        if d.weekday() in (1, 2, 3):  # martes a jueves; amplía si hace falta
            ds = d.strftime("%d/%m/%Y")
            html = get("/web/guest/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal"
                       f"&p_p_mode=view&targetLegislatura={leg}&targetDate={quote(ds, safe='')}")
            p = DayParser(leg_num); p.feed(html)
            for v in p.votes:
                time.sleep(PAUSA)
                j = json.loads(get(v["href"]))
                g = {}
                for x in j.get("votaciones", []):
                    c = g.setdefault(x["grupo"], {"s": 0, "n": 0, "a": 0, "nv": 0})
                    o = x["voto"]
                    c["s" if o in ("Sí", "Si") else "n" if o == "No" else "a" if o.startswith("Abst") else "nv"] += 1
                mx = {x["diputado"]: x["voto"] for x in j.get("votaciones", []) if x["grupo"] == "GMx"}
                info = j["informacion"]
                res.append({"exp": v["exp"], "d": ds, "ses": info["sesion"], "nv": info["numeroVotacion"],
                            "tit": info["titulo"], "txt": info["textoExpediente"], "sub": info.get("tituloSubGrupo", ""),
                            "tot": j["totales"], "g": g, "mx": mx})
            print(ds, len(p.votes), "votaciones", file=sys.stderr)
            time.sleep(PAUSA)
        d += dt.timedelta(days=1)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", default="XV")
    ap.add_argument("--desde", required=True)
    ap.add_argument("--hasta", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sin-iniciativas", action="store_true")
    a = ap.parse_args()
    data = {"generado": dt.datetime.utcnow().isoformat() + "Z", "fuente": "Congreso de los Diputados - datos abiertos",
            "legislatura": a.leg}
    if not a.sin_iniciativas:
        data.update(iniciativas())
    data["votaciones"] = votaciones(a.leg, dt.date.fromisoformat(a.desde), dt.date.fromisoformat(a.hasta))
    json.dump(data, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    print("Guardado", a.out)
