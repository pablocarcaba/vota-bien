"""Proceso repetible de reclasificación: lotes con texto (+ hueco de la segunda ronda), aplicar y cerrar.
Todo corre sobre árboles temporales (tests/helpers.py), nunca sobre los datos reales del repo."""
import json
import os
import sys
import unittest

from helpers import CLAVE, REPO, TempTree

sys.path.insert(0, os.path.join(REPO, "scripts"))
import cerrar_reclasificacion as CR

PE = "fixture_pe"
PE_CONFIG = '''
LEGISLATURAS["fixture_pe"] = dict(LEGISLATURAS["fixture_min"], fuente="europarlamento", formato="europarlamento", leg="10.ª")
'''


def volcar(path, datos):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False)


def escribir(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(texto)


def leer(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def lectura(i, imp, peso=1, tipo="eco"):
    return {"id": i, "tipo": tipo, "imp": imp, "peso": peso, "nota": "Nota de prueba.", "partido": ""}


class ArbolConPE(TempTree):
    def __init__(self):
        super().__init__()
        with open(self.path("scripts", "legislaturas.py"), "a", encoding="utf-8") as f:
            f.write(PE_CONFIG)

    def put_lotes(self, clave, items):
        volcar(self.path("data", "clasificacion", clave, "lotes", "lote_00.json"), items)


class LotesTest(unittest.TestCase):
    def setUp(self):
        self.tree = ArbolConPE()
        self.addCleanup(self.tree.cleanup)
        self.out = self.tree.path("salida")

    def lotes(self, clave, *args):
        p = self.tree.run("lotes_reclasificacion.py", clave, self.out, *args)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p

    def salida(self):
        return {it["id"]: it for f in sorted(os.listdir(self.out)) if "_l" in f for it in self.tree.read_json(self.out, f)}

    def test_congreso_incluye_texto_desde_la_exposicion_de_motivos(self):
        self.tree.put_lotes(CLAVE, [{"id": "121/000001", "tipo": "Proyecto de ley", "titulo": "Ley uno.", "autor": "Gobierno"}])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000001.txt"),
                 "Portada del boletín\nEXPOSICIÓN DE MOTIVOS\nLa ley regula   los alquile-\nres de vivienda.\n\n\nArtículo 1.")
        self.lotes(CLAVE)
        t = self.salida()["121/000001"]["texto"]
        self.assertTrue(t.startswith("EXPOSICIÓN DE MOTIVOS"), t)
        self.assertIn("La ley regula los alquileres de vivienda.", t)
        self.assertNotIn("Portada", t)

    def test_chars_recorta_y_sin_texto_va_vacio(self):
        self.tree.put_lotes(CLAVE, [{"id": "121/000001", "titulo": "Ley uno."}, {"id": "121/000002", "titulo": "Ley dos."}])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000001.txt"), "x" * 300)
        self.lotes(CLAVE, "--chars", "40")
        s = self.salida()
        self.assertEqual(len(s["121/000001"]["texto"]), 40)
        self.assertEqual(s["121/000002"]["texto"], "")

    def test_rdl_toma_el_texto_de_su_proyecto_de_ley(self):
        self.tree.put_lotes(CLAVE, [
            {"id": "121/000005", "titulo": "Proyecto de Ley por la que se tramita como proyecto de ley el Real Decreto-ley 3/2024, de 5 de marzo."},
            {"id": "130/000003", "titulo": "Real Decreto-ley 3/2024, de 5 de marzo, de medidas urgentes."},
            {"id": "130/000004", "titulo": "Real Decreto-ley 9/2024, de 1 de abril, sin proyecto de ley."},
        ])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000005.txt"), "PREÁMBULO\nTexto del proyecto.")
        escribir(self.tree.path("data", "cache", "fx", "textos", "130_000004.txt"), "Texto propio del decreto.")
        p = self.lotes(CLAVE)
        s = self.salida()
        self.assertIn("Texto del proyecto.", s["130/000003"]["texto"])
        self.assertIn("121/000005", s["130/000003"]["nota_fuente"])
        self.assertEqual(s["130/000004"]["texto"], "Texto propio del decreto.")
        self.assertNotIn("nota_fuente", s["130/000004"])
        self.assertEqual(json.loads(p.stdout)["fuentes"], {"propio": 2, "proyecto": 1, "vacio": 0})

    def test_ids_filtra_pero_el_rdl_sigue_viendo_su_proyecto(self):
        self.tree.put_lotes(CLAVE, [
            {"id": "121/000005", "titulo": "Real Decreto-ley 3/2024, de 5 de marzo."},
            {"id": "130/000003", "titulo": "Real Decreto-ley 3/2024, de 5 de marzo."},
            {"id": "122/000002", "titulo": "Otra."},
        ])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000005.txt"), "Texto del proyecto.")
        volcar(self.tree.path("ids.json"), ["130/000003"])
        self.lotes(CLAVE, "--ids", self.tree.path("ids.json"))
        s = self.salida()
        self.assertEqual(list(s), ["130/000003"])
        self.assertEqual(s["130/000003"]["texto"], "Texto del proyecto.")

    def test_tam_reparte_en_lotes(self):
        self.tree.put_lotes(CLAVE, [{"id": f"122/{n:06d}", "titulo": "t"} for n in range(5)])
        p = self.lotes(CLAVE, "--tam", "2")
        self.assertEqual(json.loads(p.stdout)["lotes"], [f"{CLAVE}_l00.json", f"{CLAVE}_l01.json", f"{CLAVE}_l02.json"])

    def test_europarlamento_lee_el_texto_por_referencia(self):
        self.tree.put_lotes(PE, [{"id": "2020/0310(COD)", "titulo": "Reglamento."}, {"id": "2021/0001(NLE)", "titulo": "Acuerdo."}])
        escribir(self.tree.path("data", "cache", PE, "textos", "2020_0310_COD_.txt"), "Resolución legislativa\nPREÁMBULO\nTexto aprobado.")
        self.lotes(PE)
        s = self.salida()
        # en el PE el texto va desde el principio (no se busca la exposición de motivos)
        self.assertTrue(s["2020/0310(COD)"]["texto"].startswith("Resolución legislativa"))
        self.assertEqual(s["2021/0001(NLE)"]["texto"], "")

    def ronda1(self, lecturas):
        """lecturas: {id: (imp_C, imp_D, imp_E)} -> <tree>/r1/{C,D,E}/lote_00.json"""
        for n, x in enumerate("CDE"):
            volcar(self.tree.path("r1", x, "lote_00.json"), [lectura(i, v[n]) for i, v in lecturas.items()])

    def test_hueco_exige_dos_de_tres_vacios_y_efectos_en_la_vigente(self):
        a = {"jovenes": 1}
        self.tree.put_lotes(CLAVE, [{"id": i, "titulo": "t"} for i in ("A", "B", "C", "D", "E")])
        volcar(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json"), [
            lectura("A", a), lectura("B", a), lectura("C", {}), lectura("D", a), lectura("E", a)])
        self.ronda1({"A": ({}, {}, a), "B": ({}, a, a), "C": ({}, {}, {}), "D": (a, a, a), "E": ({}, {}, {})})
        escribir(self.tree.path("data", "cache", "fx", "textos", "A.txt"), "z" * 9000)
        self.lotes(CLAVE, "--hueco", self.tree.path("r1"))
        # A: 2 de 3 vacíos y con efectos antes -> entra; B: solo 1 vacío; C: vigente sin efectos; D: ninguno; E: 3 vacíos y con efectos
        self.assertEqual(self.tree.read_json("salida", "ids_hueco.json"), ["A", "E"])
        s = self.salida()
        self.assertEqual(sorted(s), ["A", "E"])
        self.assertEqual(len(s["A"]["texto"]), 9000)  # con --hueco el extracto por defecto es de 12.000

    def test_hueco_cuenta_como_vacio_al_lector_que_no_leyo_la_iniciativa(self):
        a = {"jovenes": 1}
        self.tree.put_lotes(CLAVE, [{"id": "A", "titulo": "t"}])
        volcar(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json"), [lectura("A", a)])
        volcar(self.tree.path("r1", "C", "lote_00.json"), [lectura("A", {})])
        volcar(self.tree.path("r1", "D", "lote_00.json"), [lectura("A", a)])
        volcar(self.tree.path("r1", "E", "lote_00.json"), [])
        self.lotes(CLAVE, "--hueco", self.tree.path("r1"))
        self.assertEqual(self.tree.read_json("salida", "ids_hueco.json"), ["A"])

    def test_hueco_e_ids_son_excluyentes(self):
        volcar(self.tree.path("ids.json"), [])
        p = self.tree.run("lotes_reclasificacion.py", CLAVE, self.out, "--ids", self.tree.path("ids.json"), "--hueco", self.tree.path("r1"))
        self.assertNotEqual(p.returncode, 0)


class AplicarTest(unittest.TestCase):
    IDS = ["121/000001", "122/000002", "122/000004", "130/000003", "130/000009"]

    def setUp(self):
        self.tree = TempTree()
        self.addCleanup(self.tree.cleanup)
        self.tree.put_fuente()
        self.tree.put_clas(["clas_ok.json"])
        self.assertEqual(self.tree.run("build_items.py", CLAVE).returncode, 0)
        escribir(self.tree.path("data", "clasificacion", "RUBRICA.md"), "# Rúbrica\n\nVersión 3 (fecha 04/11/2026). Cambios.\n")
        ec, pr, ci = {"ciud": 1, "asal3": -1}, {"prop1": -1}, {"jovenes": 1}
        # ronda 1: 122/000004 sin efectos en los tres; 130/000003: dos lectores -1 y uno +1 (gana -1)
        r1 = {
            "121/000001": [(ec, 3)] * 3,
            "122/000002": [(ci, 1), (ci, 1), ({}, 1)],
            "122/000004": [({}, 2)] * 3,
            "130/000003": [(pr, 2), (pr, 2), ({"prop1": 1}, 2)],
            "130/000009": [({"pen1": 1}, 1)] * 3,
        }
        for n, x in enumerate("CDE"):
            volcar(self.tree.path("r1", x, "lote_00.json"), [lectura(i, v[n][0], v[n][1]) for i, v in r1.items()])
            volcar(self.tree.path("r2", x, "lote_00.json"), [lectura("122/000004", {"mayores": 1}, 2)])

    def aplicar(self, *args, ok=True):
        p = self.tree.run("aplicar_reclasificacion.py", CLAVE, self.tree.path("r1"), *args)
        if ok:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return p

    def final(self):
        return {x["id"]: x for x in self.tree.read_json("data", "clasificacion", CLAVE, "clas_0.json")}

    def test_sin_ronda2_consolida_por_mayoria_y_escribe_lectura_v3(self):
        p = self.aplicar("--fuente", "BOCG de prueba", "--fecha", "15/11/2026")
        f = self.final()
        self.assertEqual(f["122/000002"]["imp"], {"jovenes": 1})
        self.assertEqual(f["130/000003"]["imp"], {"prop1": -1})
        self.assertEqual(f["122/000004"]["imp"], {})
        base = self.tree.path("data", "clasificacion", CLAVE, "lectura_v3")
        self.assertEqual(sorted(os.listdir(base)), ["C", "CAMBIOS.md", "D", "E", "lecturas.json"])
        r = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual((r["n"], r["ronda2"], r["contra"], r["cambian"], r["unanimes"]), (5, 0, 1, 0, 3))
        self.assertTrue(os.path.exists(self.tree.path("site", "data", CLAVE + ".json")))

    def test_ronda2_sustituye_por_id_en_el_consolidado_y_en_lectura_v3(self):
        p = self.aplicar(self.tree.path("r2"), "--fuente", "BOCG de prueba", "--fecha", "15/11/2026")
        self.assertEqual(self.final()["122/000004"]["imp"], {"mayores": 1})
        # el resto de iniciativas siguen siendo las de la ronda 1
        self.assertEqual(self.final()["122/000002"]["imp"], {"jovenes": 1})
        for x in "CDE":
            lote = {it["id"]: it for it in self.tree.read_json("data", "clasificacion", CLAVE, "lectura_v3", x, "lote_00.json")}
            self.assertEqual(lote["122/000004"]["imp"], {"mayores": 1})
            self.assertEqual(len(lote), 5)
        r = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual((r["ronda2"], r["cambian"], r["vacias_antes"], r["vacias_ahora"]), (1, 1, 1, 0))

    def test_revision_con_fecha_dada_version_de_la_rubrica_y_ronda2(self):
        self.aplicar(self.tree.path("r2"), "--fuente", "BOCG de prueba", "--fecha", "15/11/2026")
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn("## Reclasificación con la rúbrica v3 (15/11/2026)", rev)
        self.assertIn("Texto usado: BOCG de prueba.", rev)
        self.assertIn("1 iniciativas que la primera pasada dejó sin efectos", rev)
        self.assertIn("lectura_v3/CAMBIOS.md", rev)

    def test_la_version_se_lee_de_la_cabecera_de_la_rubrica(self):
        escribir(self.tree.path("data", "clasificacion", "RUBRICA.md"), "# Rúbrica\n\nVersión 4 (fecha 01/01/2027).\n")
        self.aplicar("--fuente", "x", "--fecha", "01/01/2027")
        self.assertTrue(os.path.isdir(self.tree.path("data", "clasificacion", CLAVE, "lectura_v4")))
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn("## Reclasificación con la rúbrica v4 (01/01/2027)", rev)

    def test_sin_version_legible_falla_salvo_con_rubrica(self):
        escribir(self.tree.path("data", "clasificacion", "RUBRICA.md"), "# Rúbrica sin versión\n")
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--rubrica", p.stderr)
        self.aplicar("--fuente", "x", "--rubrica", "v9", "--fecha", "01/01/2027")
        self.assertTrue(os.path.isdir(self.tree.path("data", "clasificacion", CLAVE, "lectura_v9")))

    def test_fecha_por_defecto_es_hoy(self):
        import datetime
        self.aplicar("--fuente", "x")
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn(f"({datetime.date.today().strftime('%d/%m/%Y')})", rev)

    def test_repetir_reemplaza_la_seccion_de_esa_version_y_respeta_el_resto(self):
        rev = self.tree.path("data", "clasificacion", CLAVE, "REVISION.md")
        escribir(rev, "# Revisión\n\nprevio\n\n## Reclasificación con la rúbrica v3 (01/01/2026)\n\nviejo\n\n## Otra\n\ncontenido\n")
        self.aplicar("--fuente", "x", "--fecha", "15/11/2026")
        txt = leer(rev)
        self.assertEqual(txt.count("## Reclasificación con la rúbrica v3"), 1)
        self.assertNotIn("viejo", txt)
        self.assertIn("(15/11/2026)", txt)
        self.assertIn("previo", txt)
        self.assertIn("## Otra\n\ncontenido", txt)

    def test_lotes_incompletos_fallan_sin_tocar_la_clasificacion(self):
        volcar(self.tree.path("r1", "E", "lote_00.json"), [lectura("121/000001", {})])
        antes = leer(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json"))
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("lotes incompletos", p.stderr)
        self.assertEqual(leer(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json")), antes)
        self.assertFalse(os.path.exists(self.tree.path("data", "clasificacion", CLAVE, "lectura_v3")))


class CerrarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TempTree()
        self.addCleanup(self.tmp.cleanup)

    def lectura_v3(self, clave, ver="v3"):
        os.makedirs(self.tmp.path("data", "clasificacion", clave, "lectura_" + ver))

    def test_frase_con_legislaturas_v3_y_las_que_siguen_con_v2(self):
        self.lectura_v3("congreso_xv")
        self.lectura_v3("europarlamento_10")
        escribir(self.tmp.path("site", "data", "congreso_x.json"), "{}")
        escribir(self.tmp.path("site", "data", "congreso_xv.json"), "{}")
        f = CR.frase_alcance(self.tmp.root, "v3", ["congreso_xv", "congreso_x", "europarlamento_10"])
        self.assertEqual(f, "Están clasificadas con la v3, por tres lecturas independientes: Congreso de los Diputados XV legislatura "
                            "y Parlamento Europeo 10.ª legislatura. Siguen con la v2, a la espera de reclasificarse igual: "
                            "Congreso de los Diputados X legislatura.")

    def test_frase_cuando_todas_estan_en_v3_y_version_previa_de_v4(self):
        self.lectura_v3("congreso_xv", "v4")
        f = CR.frase_alcance(self.tmp.root, "v4", ["congreso_xv"])
        self.assertTrue(f.endswith("Todas las legislaturas están ya clasificadas con la v4."), f)
        escribir(self.tmp.path("site", "data", "congreso_x.json"), "{}")
        self.assertIn("Siguen con la v3,", CR.frase_alcance(self.tmp.root, "v4", ["congreso_xv", "congreso_x"]))

    def test_frase_sin_ninguna_lectura_falla(self):
        with self.assertRaises(SystemExit):
            CR.frase_alcance(self.tmp.root, "v3", ["congreso_xv"])

    def test_reescribir_alcance_cambia_solo_el_span(self):
        html = 'a <span id="alcance-v3">vieja</span> b <span id="otro">x</span>'
        self.assertEqual(CR.reescribir_alcance(html, "nueva"), 'a <span id="alcance-v3">nueva</span> b <span id="otro">x</span>')
        with self.assertRaises(SystemExit):
            CR.reescribir_alcance("<html></html>", "nueva")

    def test_solo_alcance_reescribe_el_span_segun_las_carpetas(self):
        escribir(self.tmp.path("site", "template.html"), 'x <span id="alcance-v3">vieja</span> y')
        escribir(self.tmp.path("data", "clasificacion", "RUBRICA.md"), "Versión 3 (fecha 04/11/2026).\n")
        self.lectura_v3("fixture_min")
        p = self.tmp.run("cerrar_reclasificacion.py", "--solo-alcance")
        self.assertEqual(p.returncode, 0, p.stderr)
        html = leer(self.tmp.path("site", "template.html"))
        self.assertEqual(html, 'x <span id="alcance-v3">Están clasificadas con la v3, por tres lecturas independientes: '
                               'Congreso de los Diputados Fixture. Todas las legislaturas están ya clasificadas con la v3.</span> y')

    SESGO = {
        "europarlamento_10": {"eco_con_ciud": {"partidos": [{"partido": "Bildu", "primero_pct": 41.26}]},
                              "eco_sin_ciud": {"partidos": [{"partido": "PP", "primero_pct": 30.0}]}},
        "europarlamento_9": {"eco_con_ciud": {"partidos": [{"partido": "PSOE", "primero_pct": 60.04}]},
                             "eco_sin_ciud": {"partidos": [{"partido": "VOX", "primero_pct": 12.34}]}},
        "congreso_xv": {"eco_con_ciud": {"partidos": [{"partido": "CC", "primero_pct": 50.0}, {"partido": "PNV", "primero_pct": 20.5},
                                                      {"partido": "ERC", "primero_pct": 10.1}]}},
        "congreso_xi": {"soc_con_ciud": {"partidos": [{"partido": "PSOE", "primero_pct": 99.0}]}},
    }
    PLANTILLA = (
        '<tr><th scope="row">10.ª · 2024–2029</th><td>BNG · 1,0 %</td><td>PP · 2,0 %</td></tr>\n'
        '<tr><th scope="row">9.ª · 2019–2024</th><td>X · 3,0 %</td><td>Y · 4,0 %</td></tr>\n'
        '<p>salen primeros A en el 1,0 % de los perfiles, B en el 2,0 % y C en el 3,0 %. Más. '
        'en la XI, en leyes sociales, VOX sale primero en el 5,0 % de los perfiles</p>'
    )

    def test_cifras_cada_frase_se_actualiza_desde_sesgo(self):
        h = CR.actualizar_cifras(self.PLANTILLA, self.SESGO)
        self.assertIn('<tr><th scope="row">10.ª · 2024–2029</th><td>EH Bildu · 41,3 %</td><td>PP · 30,0 %</td></tr>', h)
        self.assertIn('<tr><th scope="row">9.ª · 2019–2024</th><td>PSOE · 60,0 %</td><td>VOX · 12,3 %</td></tr>', h)
        self.assertIn("salen primeros CC en el 50,0 % de los perfiles, PNV en el 20,5 % y ERC en el 10,1 %.", h)
        self.assertIn("en la XI, en leyes sociales, PSOE sale primero en el 99,0 % de los perfiles", h)

    def test_cifras_falla_y_nombra_la_frase_que_ya_no_casa(self):
        for quitar in ('en la XI, en leyes sociales, VOX sale primero en el 5,0 % de los perfiles', '9.ª · 2019–2024'):
            with self.subTest(quitar=quitar), self.assertRaises(SystemExit) as cm:
                CR.actualizar_cifras(self.PLANTILLA.replace(quitar, "XX"), self.SESGO)
            self.assertIn("ya no casan", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
