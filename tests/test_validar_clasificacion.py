import glob
import os
import unittest

from helpers import CLAVE, REPO, TempTree, fixture


class ValidarDatosRealesTest(unittest.TestCase):
    """El validador debe pasar sobre los datos reales del repo (solo lectura)."""

    @classmethod
    def setUpClass(cls):
        import subprocess
        import sys
        cls.proc = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "validar_clasificacion.py")],
                                  capture_output=True, text=True, cwd=REPO)

    def test_exit_code_cero(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_cero_errores_en_todas_las_claves(self):
        claves = sorted(os.path.basename(os.path.dirname(p)) for p in
                        glob.glob(os.path.join(REPO, "data", "clasificacion", "*", "clas_0.json")))
        self.assertGreaterEqual(len(claves), 11)
        lines = self.proc.stdout.splitlines()
        for clave in claves:
            with self.subTest(clave=clave):
                resumen = [l for l in lines if l.startswith(clave + ":")]
                self.assertEqual(len(resumen), 1, "no hay resumen para " + clave)
                self.assertTrue(resumen[0].endswith(", 0 errores"), resumen[0])


class ValidarFixturesTest(unittest.TestCase):
    """Fixtures minimos: el validador detecta cada tipo de error."""

    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        self.tree.put_fuente()
        self.tree.put_template(real=True)
        built = self.tree.run("build_items.py", CLAVE)
        self.assertEqual(built.returncode, 0, built.stderr)

    def validar(self, *fixtures):
        return self.tree.run("validar_clasificacion.py", CLAVE, *[fixture(f) for f in fixtures])

    def test_fixture_valido_pasa(self):
        p = self.validar("clas_ok.json")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("0 errores", p.stdout)

    def test_colectivo_desconocido(self):
        p = self.validar("clas_colectivo_desconocido.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("colectivo desconocido 'colectivo_inventado'", p.stdout)

    def test_peso_fuera_de_rango(self):
        p = self.validar("clas_peso_fuera_rango.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("peso 4", p.stdout)

    def test_valor_de_impacto_invalido(self):
        p = self.validar("clas_valor_invalido.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("valor 2 en ciud", p.stdout)

    def test_id_duplicado(self):
        p = self.validar("clas_id_duplicado.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("id duplicado", p.stdout)

    def test_id_desconocido(self):
        p = self.validar("clas_id_desconocido.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("id desconocido", p.stdout)

    def test_tipo_y_nota_invalidos(self):
        p = self.validar("clas_tipo_y_nota.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("tipo 'otro'", p.stdout)
        self.assertIn("nota de 0 palabras", p.stdout)

    def test_iniciativas_sin_clasificar_en_modo_completo(self):
        self.tree.put_clas(["clas_parcial.json"])
        p = self.tree.run("validar_clasificacion.py", CLAVE)
        self.assertEqual(p.returncode, 1)
        self.assertIn("iniciativas sin clasificar", p.stdout)

    def test_cobertura_completa_en_modo_completo(self):
        # 6 iniciativas en items.json; clas_ok cubre 5 y el id 122/000005 queda sin clasificar
        self.tree.put_clas(["clas_ok.json"])
        p = self.tree.run("validar_clasificacion.py", CLAVE)
        self.assertEqual(p.returncode, 1)
        self.assertIn("1 iniciativas sin clasificar", p.stdout)
        self.assertIn("122/000005", p.stdout)


if __name__ == "__main__":
    unittest.main()
