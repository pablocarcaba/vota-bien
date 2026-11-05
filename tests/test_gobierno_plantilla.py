"""La etiqueta «Iniciativa del Gobierno de …» se decide por la fecha de PRESENTACIÓN (it.f), no por la de votación.

Ejecuta las funciones reales de site/template.html (gobDe, fkey, dkey) con node sobre los datos de la XII.
121/000012 se presentó el 06/11/2017 (Rajoy) y se votó el 20/12/2018 (ya con Sánchez): si gobDe vuelve a usar
la fecha de votación (vd), sale «Sánchez» y el test falla.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest

from helpers import REPO

sys.path.insert(0, os.path.join(REPO, "scripts"))
from legislaturas import LEGISLATURAS  # noqa: E402

TEMPLATE = os.path.join(REPO, "site", "template.html")
DATA = os.path.join(REPO, "site", "data", "congreso_xii.json")


def funcion(src, nombre):
    """Código de `function nombre(...){...}` de la plantilla (llaves equilibradas)."""
    m = re.search(r"function %s\(" % nombre, src)
    if not m:
        raise AssertionError("no está la función %s en la plantilla" % nombre)
    i = src.index("{", m.end())
    nivel = 0
    for j in range(i, len(src)):
        if src[j] == "{":
            nivel += 1
        elif src[j] == "}":
            nivel -= 1
            if nivel == 0:
                return src[m.start():j + 1]
    raise AssertionError("llaves sin cerrar en %s" % nombre)


def items(*ids):
    with open(DATA, encoding="utf-8") as f:
        todos = {it["id"]: it for it in json.load(f)["items"]}
    return [todos[i] for i in ids]


class GobiernoPlantillaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEMPLATE, encoding="utf-8") as f:
            cls.src = f.read()

    def test_los_datos_distinguen_presentacion_y_votacion(self):
        # sin esto el test de abajo no probaría nada: la votación cae ya con Sánchez
        for it in items("121/000012", "121/000013"):
            with self.subTest(id=it["id"]):
                self.assertTrue(it["f"].endswith("/2017"))
                self.assertTrue(it["vd"].endswith("/2018"))

    def test_gobde_no_usa_la_fecha_de_votacion(self):
        cuerpo = funcion(self.src, "gobDe")
        self.assertNotIn("dkey(", cuerpo)
        self.assertNotIn(".vd", cuerpo)

    @unittest.skipUnless(shutil.which("node"), "hace falta node para ejecutar la plantilla")
    def test_gobde_por_fecha_de_presentacion(self):
        js = "\n".join(funcion(self.src, n) for n in ("fkey", "dkey", "gobDe"))
        gob = LEGISLATURAS["congreso_xii"]["gobiernos"]
        prueba = items("121/000012", "121/000013")
        code = "const gobiernos=()=>%s;\n%s\nconsole.log(JSON.stringify(%s.map(gobDe)));" % (
            json.dumps(gob), js, json.dumps(prueba))
        p = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout), ["Rajoy", "Rajoy"])


if __name__ == "__main__":
    unittest.main()
