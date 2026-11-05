"""Empate en cabeza en site/template.html: el bloque empatado comparte el 1.º y se explica en una sola frase.

Ejecuta con node las funciones reales de la plantilla (tecFrase, yLista, puestoDe) sobre un ranking de prueba con
cinco partidos a 3 puntos o menos del primero (dos con la misma nota) y uno empatado más abajo.
"""
import json
import re
import shutil
import subprocess
import unittest

from test_gobierno_plantilla import TEMPLATE, funcion


def constante(src, nombre):
    m = re.search(r"^const %s = .*$" % nombre, src, re.M)
    if not m:
        raise AssertionError("no está la constante %s en la plantilla" % nombre)
    return m.group(0)


class EmpatePlantillaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEMPLATE, encoding="utf-8") as f:
            cls.src = f.read()

    def test_vocabulario(self):
        # «no es significativo» se leía como jerga estadística; ahora, «demasiado pequeña para ordenarlos»
        self.assertNotRegex(self.src, r"significativ")
        self.assertNotIn("Empate técnico", self.src)
        self.assertIn("demasiado pequeña para ordenarlos", self.src)
        self.assertIn("Las votaciones en las que no vota no suman ni restan a su nota.", self.src)
        self.assertNotIn("no asiste", self.src)

    @unittest.skipUnless(shutil.which("node"), "hace falta node para ejecutar la plantilla")
    def test_bloque_empatado(self):
        js = "\n".join([constante(self.src, "EMPATE"), constante(self.src, "puestoDe"), funcion(self.src, "yLista"),
                        funcion(self.src, "tecFrase")])
        rows = [{"k": "PNV", "s": 86, "puesto": 1, "tec": True}, {"k": "PDeCAT", "s": 85, "puesto": 2, "tec": True},
                {"k": "PSOE", "s": 83, "puesto": 3, "tec": True}, {"k": "Cs", "s": 83, "puesto": 3, "tec": True},
                {"k": "ERC", "s": 77, "puesto": 5, "tec": False}, {"k": "PP", "s": 71, "puesto": 6, "tec": False}]
        code = ("const esc=s=>s, pn=k=>k;\n%s\nconst rows=%s;\nconsole.log(JSON.stringify({rank:tecFrase(rows), "
                "ficha:tecFrase(rows,'PSOE'), sin:tecFrase(rows.map(x=>({...x,tec:false}))), puestos:rows.map(puestoDe)}));"
                % (js, json.dumps(rows)))
        p = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertEqual(r["rank"], "PNV, PDeCAT, PSOE y Cs están prácticamente empatados (a 3 puntos o menos).")
        self.assertEqual(r["ficha"], "Empatado en cabeza con PNV, PDeCAT y Cs, a 3 puntos o menos")
        self.assertEqual(r["sin"], "")
        # el bloque comparte el 1.º; fuera de él, el puesto de siempre
        self.assertEqual(r["puestos"], [1, 1, 1, 1, 5, 6])


if __name__ == "__main__":
    unittest.main()
