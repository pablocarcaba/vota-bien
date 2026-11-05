"""Estructura del asistente del perfil (site/template.html): qué pregunta va en cada paso y qué no viaja en los enlaces.

Evalúa con node las constantes reales de la plantilla (CATS, PASOS, PRIVADO). Si una pregunta cambia de paso o un dato
sensible pasa a viajar en el enlace (o al revés), este test falla: el cambio tiene que ser deliberado.
"""
import json
import os
import shutil
import subprocess
import unittest

from helpers import REPO

TEMPLATE = os.path.join(REPO, "site", "template.html")

PASOS = [
    ("Tú y tu familia", False, ["edad", "hij", "sexo", "civ", "car"]),
    ("Trabajo e ingresos", False, ["sit", "asal", "fun", "pro", "emp", "sec", "pen", "des", "ayu"]),
    ("Vivienda y ahorros", False, ["donde", "nviv", "alq", "hip", "prop", "rur"]),
    ("Salud y situación personal", True, ["ori", "soc"]),
]
PASO4_PRIVADO = {"lgtbi", "pac", "depend", "discapacidad", "inmigrantes", "minorias", "victimas", "socNo"}
# fuera del paso 4, solo «Otro» en sexo (paso 1) no viaja: puede revelar la identidad de género
PRIVADO_FUERA_DEL_PASO4 = {"sexOtro"}
PRIVADO = PASO4_PRIVADO | PRIVADO_FUERA_DEL_PASO4


def bloque(src):
    """De `const CATS` a `const CHECK`, más qOpts (declarada más abajo) y un `state` mínimo."""
    i, j = src.index("const CATS = ["), src.index("const CHECK")
    k = src.index("function qOpts(")
    return ("const state={sel:new Set(),pasos:{ui:new Set(),done:new Set(),cur:0,ret:new Set(),aviso:false}};\n" + src[i:j]
            + src[k:src.index("\n", k)] + "\n")


@unittest.skipUnless(shutil.which("node"), "hace falta node")
class PasosPerfilTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEMPLATE, encoding="utf-8") as f:
            js = bloque(f.read()) + """
process.stdout.write(JSON.stringify({
  pasos: PASOS.map(P=>({t:P.t, opt:!!P.opt, q:P.q.map(q=>q.id), opts:P.q.map(qOpts)})),
  cat: Object.fromEntries(PASOS.flatMap(P=>P.q).map(q=>[q.id, q.cat||null])),
  privado: [...PRIVADO], implica: IMPLICA}));"""
        out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
        cls.d = json.loads(out)

    def test_preguntas_de_cada_paso(self):
        self.assertEqual([(p["t"], p["opt"], p["q"]) for p in self.d["pasos"]], [(t, o, q) for t, o, q in PASOS])

    def test_privado_es_explicito(self):
        self.assertEqual(set(self.d["privado"]), PRIVADO)

    def test_privado_es_el_paso_opcional_mas_sex_otro(self):
        opt = {k for p in self.d["pasos"] if p["opt"] for q in p["opts"] for k in q}
        self.assertEqual(opt, PASO4_PRIVADO)
        self.assertEqual(set(self.d["privado"]) - opt, PRIVADO_FUERA_DEL_PASO4)

    def test_sex_otro_es_una_respuesta_de_sexo_del_paso_1(self):
        paso1 = self.d["pasos"][0]
        self.assertIn("sexOtro", paso1["opts"][paso1["q"].index("sexo")])

    def test_viajan_en_el_enlace(self):
        # como antes de la v8: lo personal que no es una categoría especial de datos sí va en el enlace
        for k in ("hombres", "mujeres", "sexNs", "civSol", "civPar", "civSep", "civViu", "cuid",
                  "pobreza", "rural"):
            self.assertNotIn(k, self.d["privado"], k)

    def test_cada_respuesta_se_pregunta_una_sola_vez(self):
        todas = [k for p in self.d["pasos"] for q in p["opts"] for k in q]
        self.assertEqual(len(todas), len(set(todas)))

    def test_la_ayuda_social_es_pobreza_y_no_depende_del_paro(self):
        paso2 = self.d["pasos"][1]
        self.assertEqual(paso2["opts"][paso2["q"].index("ayu")], ["pobreza"])
        self.assertNotIn("pobreza", self.d["implica"].get("desSub", []))

    def test_alquiler_justo_despues_de_cuantas_viviendas(self):
        q = self.d["pasos"][2]["q"]
        self.assertEqual(q.index("alq"), q.index("nviv") + 1)


if __name__ == "__main__":
    unittest.main()
