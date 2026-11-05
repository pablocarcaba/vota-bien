import json
import re
import unittest

from helpers import TempTree

CAT_RE = re.compile(r'<script id="catalogo" type="application/json">(.*?)</script>', re.S)


class BuildPageTest(unittest.TestCase):
    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        self.tree.put_template()

    def touch_dataset(self, clave):
        with open(self.tree.path("site", "data", clave + ".json"), "w", encoding="utf-8") as f:
            f.write("{}")

    def catalogo_raw(self):
        with open(self.tree.path("site", "index.html"), encoding="utf-8") as f:
            return CAT_RE.search(f.read()).group(1)

    def test_catalogo_es_json_valido_y_solo_incluye_datasets_existentes(self):
        self.touch_dataset("fixture_min")
        p = self.tree.run("build_page.py")
        self.assertEqual(p.returncode, 0, p.stderr)
        cat = json.loads(self.catalogo_raw())
        self.assertEqual([c["clave"] for c in cat], ["fixture_min"])
        self.assertEqual(set(cat[0]), {"clave", "fuente", "fuente_txt", "leg", "titulo", "rubrica"})
        # sin lectura_v3 en el árbol de prueba, la legislatura sigue con la v2
        self.assertEqual(cat[0]["rubrica"]["version"], "v2")

    def test_no_incluye_datasets_que_no_existen(self):
        self.touch_dataset("fixture_min")
        self.tree.run("build_page.py")
        claves = [c["clave"] for c in json.loads(self.catalogo_raw())]
        self.assertNotIn("fixture_xss", claves)
        self.assertNotIn("congreso_xv", claves)

    def test_escapa_cierre_de_etiqueta(self):
        self.touch_dataset("fixture_xss")
        p = self.tree.run("build_page.py")
        self.assertEqual(p.returncode, 0, p.stderr)
        raw = self.catalogo_raw()
        self.assertNotIn("</", raw)
        self.assertIn("<\\/script>", raw)
        # JSON valido y el titulo original se recupera
        self.assertEqual(json.loads(raw)[0]["titulo"], "Titulo </script><b>x</b>")

    def test_sin_datasets_falla(self):
        p = self.tree.run("build_page.py")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("No hay datasets", p.stderr)

    def test_rubrica_v3_con_lectura_v3(self):
        import os
        self.touch_dataset("fixture_min")
        os.makedirs(self.tree.path("data", "clasificacion", "fixture_min", "lectura_v3"))
        with open(self.tree.path("data", "clasificacion", "RUBRICA.md"), "w", encoding="utf-8") as f:
            f.write("# Rúbrica\n\nVersión 3 (fecha 04/11/2026). Cambios\n")
        self.tree.run("build_page.py")
        self.assertEqual(json.loads(self.catalogo_raw())[0]["rubrica"], {"version": "v3", "fecha": "04/11/2026"})

    def test_respeta_el_orden_de_la_configuracion(self):
        self.touch_dataset("fixture_xss")
        self.touch_dataset("fixture_min")
        self.tree.run("build_page.py")
        self.assertEqual([c["clave"] for c in json.loads(self.catalogo_raw())], ["fixture_min", "fixture_xss"])


if __name__ == "__main__":
    unittest.main()
