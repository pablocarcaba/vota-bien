import json
import unittest

from helpers import CLAVE, TempTree, load_fixture


class BuildItemsTest(unittest.TestCase):
    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        self.tree.put_fuente()
        self.proc = self.tree.run("build_items.py", CLAVE)
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)
        self.items = self.tree.read_json("data", "generado", CLAVE, "items.json")
        self.by_id = {i["id"]: i for i in self.items}

    def test_estructura_de_cada_item(self):
        for it in self.items:
            with self.subTest(id=it["id"]):
                self.assertEqual(set(it), {"id", "tipo_ini", "titulo", "autor", "fecha", "resultado", "situacion"})

    def test_id_truncado_a_10_caracteres(self):
        self.assertIn("121/000001", self.by_id)
        self.assertNotIn("121/000001/0000", self.by_id)

    def test_espacios_normalizados(self):
        self.assertEqual(self.by_id["121/000001"]["titulo"], "Proyecto de Ley de prueba uno.")
        self.assertEqual(self.by_id["121/000001"]["resultado"], "Aprobado 10/09/2024")

    def test_rdl_marcado_como_real_decreto_ley(self):
        self.assertEqual(self.by_id["130/000003"]["tipo_ini"], "Real Decreto-ley")

    def test_rdl_tomado_de_votaciones_si_no_estaba(self):
        rdl = self.by_id["130/000009"]
        self.assertEqual(rdl["autor"], "Gobierno")
        self.assertEqual(rdl["tipo_ini"], "Real Decreto-ley")

    def test_votacion_de_tramitacion_no_genera_item(self):
        self.assertNotIn("130/000010", self.by_id)

    def test_total_de_iniciativas(self):
        self.assertEqual(len(self.items), 6)


class BuildDataTest(unittest.TestCase):
    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        self.tree.put_fuente()
        self.tree.put_clas(["clas_ok.json"])
        self.assertEqual(self.tree.run("build_items.py", CLAVE).returncode, 0)
        self.proc = self.tree.run("build_data.py", CLAVE)
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)
        self.data = self.tree.read_json("site", "data", CLAVE + ".json")
        self.by_id = {i["id"]: i for i in self.data["items"]}

    def test_estructura_de_salida(self):
        self.assertEqual(set(self.data), {"meta", "items"})
        for it in self.data["items"]:
            with self.subTest(id=it["id"]):
                self.assertLessEqual({"id", "t", "k", "a", "tp", "imp", "w", "n", "f", "r"}, set(it))
                self.assertIn(it["tp"], ("eco", "soc"))
                self.assertIn(it["w"], (1, 2, 3))
                self.assertIsInstance(it["a"], list)

    def test_meta(self):
        meta = self.data["meta"]
        self.assertEqual(meta["clave"], CLAVE)
        self.assertEqual(meta["parties"], ["PSOE", "PP", "Podemos", "BNG"])
        self.assertEqual(meta["generado"], "2026-01-01")
        self.assertIs(meta["participacion"], True)

    def test_iniciativa_sin_clasificar_se_omite(self):
        self.assertNotIn("122/000005", self.by_id)
        self.assertEqual(len(self.data["items"]), 5)
        self.assertIn("sin clasificar: 1", self.proc.stdout)

    def test_autoria(self):
        self.assertEqual(self.by_id["121/000001"]["a"], ["Gobierno"])
        self.assertEqual(self.by_id["122/000002"]["a"], ["PP"])
        self.assertEqual(self.by_id["122/000004"]["a"], ["PSOE"])

    def test_tipos_de_iniciativa(self):
        self.assertEqual(self.by_id["121/000001"]["k"], "Proyecto de ley")
        self.assertEqual(self.by_id["122/000002"]["k"], "Proposición de ley")
        self.assertEqual(self.by_id["130/000003"]["k"], "Real decreto-ley")

    def test_votacion_final_gana_a_toma_y_totalidad(self):
        it = self.by_id["121/000001"]
        self.assertEqual(it["vk"], "Votación final")
        self.assertEqual(it["vd"], "10/01/2024")
        self.assertEqual(it["v"], {"PSOE": "s", "PP": "n"})

    def test_toma_gana_a_totalidad(self):
        it = self.by_id["122/000002"]
        self.assertEqual(it["vk"], "Toma en consideración")
        self.assertEqual(it["vd"], "04/01/2024")
        self.assertEqual(it["v"]["PSOE"], "n")
        self.assertEqual(it["v"]["PP"], "s")

    def test_convalidacion_gana_a_toma(self):
        it = self.by_id["130/000003"]
        self.assertEqual(it["vk"], "Convalidación")
        self.assertEqual(it["vd"], "08/01/2024")
        self.assertEqual(it["v"], {"PSOE": "s", "PP": "n"})

    def test_enmienda_a_la_totalidad_invierte_el_voto(self):
        # fuente: GS "Sí" y GP abstención -> oponerse a la ley: PSOE n, abstencion se mantiene
        it = self.by_id["122/000004"]
        self.assertEqual(it["vk"], "Enmienda a la totalidad")
        self.assertEqual(it["v"], {"PSOE": "n", "PP": "a"})

    def test_voto_mayoritario_de_partidos_del_mixto_por_nominal(self):
        v = self.by_id["122/000002"]["v"]
        self.assertEqual(v["Podemos"], "s")  # dos diputados Si
        self.assertEqual(v["BNG"], "n")

    def test_rdl_convalidado_segun_totales(self):
        self.assertEqual(self.by_id["130/000003"]["r"], "Convalidado")
        self.assertEqual(self.by_id["130/000009"]["r"], "Convalidado")

    def test_votos_son_s_n_a(self):
        for it in self.data["items"]:
            for p, l in it.get("v", {}).items():
                with self.subTest(id=it["id"], partido=p):
                    self.assertIn(l, ("s", "n", "a"))
                    self.assertIn(p, self.data["meta"]["parties"])

    def test_voto_con_clave_solo_si_hay_votacion(self):
        for it in self.data["items"]:
            self.assertEqual("v" in it, "vk" in it)
            self.assertEqual("v" in it, "vd" in it)


class ParticipacionTest(unittest.TestCase):
    """«nv» de cada iniciativa: partidos con escaño en su votación clave que no votaron (la ficha calcula con ello la
    participación). Un partido sin registro en esa votación (aún no era diputado) no cuenta como ausente."""

    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        fuente = load_fixture("fuente_min.json")
        toma = next(v for v in fuente["votaciones"] if v["exp"] == "122/000002" and v["tit"].startswith("Toma"))
        toma["g"]["GP"] = {"s": 0, "n": 0, "a": 0, "nv": 130}  # todo el grupo ausente
        toma["mx"]["Tercera, Eva"] = "No vota"  # única diputada de BNG
        self.tree.put_fuente()
        with open(self.tree.path("data", "fuente", CLAVE + ".json"), "w", encoding="utf-8") as f:
            json.dump(fuente, f, ensure_ascii=False)
        self.tree.put_clas(["clas_ok.json"])
        self.assertEqual(self.tree.run("build_items.py", CLAVE).returncode, 0)
        proc = self.tree.run("build_data.py", CLAVE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.by_id = {i["id"]: i for i in self.tree.read_json("site", "data", CLAVE + ".json")["items"]}

    def test_ausentes_de_la_votacion_clave(self):
        it = self.by_id["122/000002"]
        self.assertEqual(it["vk"], "Toma en consideración")
        self.assertEqual(it["v"], {"PSOE": "n", "Podemos": "s"})
        self.assertEqual(it["nv"], ["BNG", "PP"])

    def test_sin_registro_no_es_ausencia(self):
        # 121/000001: BNG y Podemos no figuran en la votación (sin nominal); todos los que figuran votaron
        self.assertNotIn("nv", self.by_id["121/000001"])
        self.assertTrue(all("nv" not in it for it in self.by_id.values() if it["id"] != "122/000002"))


if __name__ == "__main__":
    unittest.main()
