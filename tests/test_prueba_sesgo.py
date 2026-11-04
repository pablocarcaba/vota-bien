"""La prueba de sesgo reproduce el cálculo de la web: si cambian las constantes de site/template.html sin
cambiar scripts/prueba_sesgo.py (o al revés), este test falla."""
import json, os, re, sys, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import prueba_sesgo as P

TPL = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()


def js_obj(nombre):
    m = re.search(r"const " + nombre + r" = (\{[^}]*\});", TPL)
    return json.loads(re.sub(r"'", '"', re.sub(r"([{,]\s*)(\w+)\s*:", r'\1"\2":', m.group(1))))


class TestParidadConLaWeb(unittest.TestCase):
    def test_prudencia(self):
        self.assertEqual(int(re.search(r"const K = (\d+);", TPL).group(1)), P.K)

    def test_peso(self):
        self.assertEqual({int(k): v for k, v in js_obj("PESO").items()}, P.PESO)

    def test_fuerza(self):
        self.assertEqual(js_obj("FUERZA"), P.FUERZA)

    def test_formula_de_la_nota(self):
        self.assertIn("r.s = Math.round(r.S/(r.W+K)*100)", TPL)

    def test_redondeo_como_js(self):
        self.assertEqual([P.js_round(x) for x in (0.5, 1.5, -0.5, -1.5, 2.4)], [1, 2, 0, -1, 2])


if __name__ == "__main__":
    unittest.main()
