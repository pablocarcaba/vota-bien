import json
import os
import re
import sys
import unittest

from helpers import REPO

sys.path.insert(0, os.path.join(REPO, "scripts"))
from legislaturas import LEGISLATURAS  # noqa: E402

DATA = os.path.join(REPO, "site", "data")


def load(clave):
    with open(os.path.join(DATA, clave + ".json"), encoding="utf-8") as f:
        return json.load(f)


class SiteDataTest(unittest.TestCase):
    def test_cada_dataset_de_la_configuracion_existe(self):
        for clave in LEGISLATURAS:
            with self.subTest(clave=clave):
                self.assertTrue(os.path.exists(os.path.join(DATA, clave + ".json")))

    def test_no_hay_datasets_huerfanos(self):
        en_disco = {f[:-5] for f in os.listdir(DATA) if f.endswith(".json")}
        self.assertEqual(en_disco - set(LEGISLATURAS), set())

    def test_catalogo_incrustado_en_index_apunta_a_datasets_existentes(self):
        index = os.path.join(REPO, "site", "index.html")
        with open(index, encoding="utf-8") as f:
            m = re.search(r'<script id="catalogo" type="application/json">(.*?)</script>', f.read(), re.S)
        self.assertIsNotNone(m, "index.html sin catalogo incrustado (falta ejecutar build_page.py)")
        cat = json.loads(m.group(1))
        self.assertTrue(cat)
        for c in cat:
            with self.subTest(clave=c["clave"]):
                self.assertTrue(os.path.exists(os.path.join(DATA, c["clave"] + ".json")))

    def test_estructura_y_votos_de_cada_dataset(self):
        for clave in LEGISLATURAS:
            with self.subTest(clave=clave):
                d = load(clave)
                self.assertEqual(set(d), {"meta", "items"})
                meta = d["meta"]
                self.assertEqual(meta["clave"], clave)
                self.assertTrue(meta["parties"], "meta.parties vacio")
                self.assertTrue(d["items"], "sin iniciativas")
                ids = [i["id"] for i in d["items"]]
                self.assertEqual(len(ids), len(set(ids)), "ids duplicados")
                for it in d["items"]:
                    self.assertIn(it["tp"], ("eco", "soc"), it["id"])
                    self.assertIn(it["w"], (1, 2, 3), it["id"])
                    self.assertIsInstance(it["imp"], dict, it["id"])
                    self.assertEqual("v" in it, "vk" in it, it["id"])
                    for partido, voto in it.get("v", {}).items():
                        self.assertIn(voto, ("s", "n", "a"), "%s %s" % (it["id"], partido))
                        self.assertIn(partido, meta["parties"], "%s: partido fuera de meta.parties" % it["id"])


if __name__ == "__main__":
    unittest.main()
