"""textos_bocg.fragmento recorta el texto de la iniciativa y no el sumario ni las vecinas del boletín."""
import os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import textos_bocg as T

OBJETO_ILP = "Proposición de Ley sobre establecimiento de una prestación de ingresos mínimos en el ámbito de protección de la Seguridad Social."

# Estructura real de un BOCG de la serie D: sumario con puntos de relleno, luego los cuerpos.
BOCG = """BOLETÍN OFICIAL DE LAS CORTES GENERALES
SUMARIO
120/000035  Acuerdo de la Mesa de la Cámara admitiendo el escrito presentado por don 
José Campos Trujillo y otros, por el que se ejercita el trámite inicial de la iniciativa 
legislativa popular sobre establecimiento de una prestación de ingresos mínimos 
en el ámbito de protección de la Seguridad Social  ............................................. 12
162/000100  Proposición no de Ley sobre la dependencia  ............ 3
Control de la acción del Gobierno
PROPOSICIONES NO DE LEY
La Mesa de la Cámara ha acordado admitir a trámite las siguientes Proposiciones no de Ley.
162/000100
Autor: Grupo Parlamentario Socialista
Texto: la dependencia debe financiarse.
162/000101
Autor: Grupo Parlamentario Popular
Texto: alta velocidad.
Iniciativa legislativa popular
69120/000035
La Mesa de la Cámara admite a trámite la iniciativa legislativa popular sobre establecimiento de una
prestación de ingresos mínimos en el ámbito de protección de la Seguridad Social.
Autor: Don José Campos Trujillo y otros.
162/000102
Autor: Grupo Parlamentario Mixto
Texto: horas extraordinarias.
"""


class TestFragmento(unittest.TestCase):
    def test_salta_el_sumario_y_corta_en_la_siguiente_iniciativa(self):
        f = T.fragmento(BOCG, "120/000035")
        self.assertTrue(f.startswith("120/000035\nLa Mesa de la Cámara admite"), f[:80])
        self.assertIn("Campos Trujillo", f)
        self.assertNotIn("dependencia", f)
        self.assertNotIn("horas extraordinarias", f)
        self.assertNotIn("69", f.split("\n")[0])  # sin el número de página pegado

    def test_no_confunde_expedientes_que_comparten_prefijo(self):
        self.assertIsNone(T.fragmento("120/0000350\notro texto\n", "120/000035"))
        self.assertIsNone(T.fragmento("x 120/000035/0000\n", "120/000036"))

    def test_expediente_solo_en_el_sumario_es_none(self):
        self.assertIsNone(T.fragmento("120/000035  Titulo largo ........ 12\ncuerpo\n", "120/000035"))

    def test_tolera_espacios_alrededor_de_la_barra(self):
        self.assertIsNotNone(T.fragmento("cve\n120 / 000035\nLa Mesa admite.\n", "120/000035"))


class TestCorresponde(unittest.TestCase):
    def test_texto_correcto(self):
        self.assertTrue(T.texto_corresponde(T.fragmento(BOCG, "120/000035"), "120/000035", OBJETO_ILP)[0])

    def test_sumario_y_vecinas_se_detectan(self):
        # el fallo original: el texto arranca en la línea del sumario y arrastra otras iniciativas
        malo = BOCG[BOCG.index("120/000035"):]
        self.assertEqual(T.texto_corresponde(malo, "120/000035", OBJETO_ILP), (False, "empieza en un sumario"))

    def test_texto_de_otra_iniciativa(self):
        ok, motivo = T.texto_corresponde("162/000100\nAutor: PSOE\nla dependencia debe financiarse\n", "120/000035", OBJETO_ILP)
        self.assertFalse(ok)

    def test_senado_sin_numero_124_pero_con_titulo(self):
        t = "I. INICIATIVAS LEGISLATIVAS\n" + OBJETO_ILP + "\n"
        self.assertTrue(T.texto_corresponde(t, "124/000001", OBJETO_ILP)[0])


if __name__ == "__main__":
    unittest.main()
