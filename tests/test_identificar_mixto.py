"""identificar_mixto recorta el texto de cada iniciativa con textos_bocg.fragmento, no con t.find (que cae en el sumario)."""
import ast, inspect, os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import textos_bocg as T
try:
    import identificar_mixto as M
except ImportError:  # pypdf solo está en .venv
    M = None

NOMBRES = {"rego": "BNG", "baldovi": "Compromís", "oramas": "CC"}
PARTIDOS = {"bng": "BNG", "compromis": "Compromís", "cc": "CC"}

# El sumario enumera varias iniciativas; la del BNG (122/000033) va primero y la de Compromís justo detrás.
BOCG = """BOLETÍN OFICIAL DE LAS CORTES GENERALES
SUMARIO
122/000033  Proposición de Ley de modificación de la Ley de Amnistía  ............ 2
122/000034  Proposición de Ley sobre el valenciano, presentada a instancia de don Joan Baldoví Roda, de Compromís  .... 5
Proposiciones de Ley
122/000033
Presentada por el Grupo Parlamentario Mixto, a instancia de don Néstor Rego Candamil, del BNG.
Texto: se excluyen los crímenes de lesa humanidad.
122/000034
Presentada por el Grupo Parlamentario Mixto, a instancia de don Joan Baldoví Roda, de Compromís.
Texto: valenciano.
"""


def viejo(t, i):
    """El recorte anterior, solo como contraste de la prueba."""
    k = t.find(i)
    return t[k:k + 6000] if k >= 0 else t[:6000]


@unittest.skipIf(M is None, "falta pypdf")
class TestIdentificarMixto(unittest.TestCase):
    def test_propuesta_de_su_texto_y_no_del_sumario_ni_de_las_vecinas(self):
        frag, votos = M.proponer(BOCG, "122/000033", NOMBRES, PARTIDOS)
        self.assertEqual(set(votos), {"BNG"}, votos)
        self.assertNotIn("Baldoví", frag)
        self.assertNotIn("122/000034", frag)

    def test_la_vecina_tambien_se_atribuye_a_su_partido(self):
        _, votos = M.proponer(BOCG, "122/000034", NOMBRES, PARTIDOS)
        self.assertEqual(set(votos), {"Compromís"}, votos)

    def test_el_recorte_anterior_si_se_equivocaba(self):
        # contraste: con t.find el texto empieza en el sumario y arrastra a la vecina
        self.assertIn("Baldoví", viejo(BOCG, "122/000033"))

    def test_si_no_figura_el_expediente_cae_al_inicio_del_boletin(self):
        self.assertEqual(M.texto_de("texto sin expedientes", "122/000999"), "texto sin expedientes")

    def test_reutiliza_fragmento_de_textos_bocg(self):
        self.assertIs(M.fragmento, T.fragmento)

    def test_no_vuelve_a_usar_t_find_para_recortar(self):
        arbol = ast.parse(inspect.getsource(M))
        finds = [n.lineno for n in ast.walk(arbol)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "find"]
        self.assertEqual(finds, [], f"str.find en identificar_mixto.py (líneas {finds}): usa textos_bocg.fragmento")


if __name__ == "__main__":
    unittest.main()
