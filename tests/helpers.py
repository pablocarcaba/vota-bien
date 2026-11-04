"""Utilidades de test: ejecutan los scripts sobre una copia temporal del arbol, nunca sobre el repo."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
CLAVE = "fixture_min"

FIXTURE_CONFIG = '''
LEGISLATURAS["fixture_min"] = {
    "fuente": "congreso", "leg": "FX", "titulo": "Fixture", "periodo": "p", "gobierno": "g",
    "grupos": {"GS": "PSOE", "GP": "PP"},
    "nominal": {"Belarra": "Podemos", "Otra": "Podemos", "Tercera": "BNG"},
    "nominal_txt": "t",
    "autores": {"Grupo Parlamentario Socialista": "PSOE", "Grupo Parlamentario Popular en el Congreso": "PP"},
    "etiquetas": {"GS": "PSOE", "GP": "PP"},
    "partidos": ["PSOE", "PP", "Podemos", "BNG"],
    "autores_web": ["Gobierno", "PSOE", "PP"],
}
LEGISLATURAS["fixture_xss"] = dict(LEGISLATURAS["fixture_min"], titulo="Titulo </script><b>x</b>")
'''


def fixture(name):
    return os.path.join(FIXTURES, name)


def load_fixture(name):
    with open(fixture(name), encoding="utf-8") as f:
        return json.load(f)


class TempTree:
    """Arbol temporal con scripts/ (legislaturas.py ampliado con las claves fixture_*) y datos minimos."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="vota-bien-test-")
        scripts = os.path.join(self.root, "scripts")
        os.makedirs(scripts)
        for f in os.listdir(os.path.join(REPO, "scripts")):
            if f.endswith(".py"):
                shutil.copy(os.path.join(REPO, "scripts", f), scripts)
        with open(os.path.join(scripts, "legislaturas.py"), "a", encoding="utf-8") as f:
            f.write(FIXTURE_CONFIG)
        os.makedirs(os.path.join(self.root, "site", "data"))
        # build_page.py incrusta el ámbito territorial de los partidos
        os.makedirs(os.path.join(self.root, "data"))
        shutil.copy(os.path.join(REPO, "data", "ambito_partidos.json"), os.path.join(self.root, "data"))

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def put_fuente(self, name="fuente_min.json", clave=CLAVE):
        dst = self.path("data", "fuente", clave + ".json")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(fixture(name), dst)

    def put_clas(self, files, clave=CLAVE):
        d = self.path("data", "clasificacion", clave)
        os.makedirs(d, exist_ok=True)
        for i, name in enumerate(files):
            shutil.copy(fixture(name), os.path.join(d, "clas_%d.json" % i))

    def put_template(self, real=False):
        dst = self.path("site", "template.html")
        if real:
            shutil.copy(os.path.join(REPO, "site", "template.html"), dst)
        else:
            with open(dst, "w", encoding="utf-8") as f:
                f.write('<html><script id="catalogo" type="application/json">__CATALOGO__</script></html>')

    def run(self, script, *args):
        return subprocess.run([sys.executable, self.path("scripts", script)] + list(args),
                              capture_output=True, text=True, cwd=self.root)

    def read_json(self, *parts):
        with open(self.path(*parts), encoding="utf-8") as f:
            return json.load(f)

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)
