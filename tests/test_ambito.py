"""Cada partido del Congreso tiene ámbito territorial en data/ambito_partidos.json, y el mapa es coherente."""
import json, os, sys, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from legislaturas import LEGISLATURAS

A = json.load(open(os.path.join(ROOT, "data", "ambito_partidos.json"), encoding="utf-8"))


class TestAmbito(unittest.TestCase):
    def test_todos_los_partidos_del_congreso_tienen_ambito(self):
        for clave, c in LEGISLATURAS.items():
            f = os.path.join(ROOT, "site", "data", clave + ".json")
            if c.get("formato") == "europarlamento" or not os.path.exists(f):
                continue
            for p in json.load(open(f, encoding="utf-8"))["meta"]["parties"]:
                self.assertIn(p, A["partidos"], f"{clave}: falta el ámbito de {p}")

    def test_ambitos_validos(self):
        provs = set(A["provincias"])
        self.assertEqual(len(provs), 52)
        self.assertEqual({p for c in A["comunidades"].values() for p in c["provincias"]}, provs)
        for p, amb in A["partidos"].items():
            if amb != "espana":
                for x in amb:
                    self.assertTrue(x in A["comunidades"] or x in provs, f"{p}: ámbito desconocido {x}")


if __name__ == "__main__":
    unittest.main()
