"""Proceso repetible de reclasificación: lotes con texto (+ hueco de la segunda ronda), aplicar y cerrar.
Todo corre sobre árboles temporales (tests/helpers.py), nunca sobre los datos reales del repo."""
import datetime
import json
import os
import sys
import types
import unittest
from unittest import mock

from helpers import CLAVE, REPO, TempTree

sys.path.insert(0, os.path.join(REPO, "scripts"))
import aplicar_reclasificacion as AR
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
        self.assertIn("not allowed with", p.stderr)

    def hueco_fallido(self, quitar):
        a = {"jovenes": 1}
        self.tree.put_lotes(CLAVE, [{"id": "A", "titulo": "t"}])
        volcar(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json"), [lectura("A", a)])
        for x in "CDE":
            if x != quitar:
                volcar(self.tree.path("r1", x, "lote_00.json"), [lectura("A", {})])
        p = self.tree.run("lotes_reclasificacion.py", CLAVE, self.out, "--hueco", self.tree.path("r1"))
        self.assertNotEqual(p.returncode, 0)
        return p

    def test_hueco_falla_si_falta_un_lector(self):
        for x in "CDE":
            with self.subTest(falta=x):
                self.tree.cleanup()
                self.setUp()
                p = self.hueco_fallido(x)
                self.assertIn(f"{x} no tiene lecturas", p.stderr)
                self.assertFalse(os.path.exists(self.tree.path("salida", "ids_hueco.json")))

    def test_hueco_recorre_la_union_de_los_lectores_y_avisa_de_lo_no_leido(self):
        a = {"jovenes": 1}
        self.tree.put_lotes(CLAVE, [{"id": i, "titulo": "t"} for i in ("A", "B")])
        volcar(self.tree.path("data", "clasificacion", CLAVE, "clas_0.json"), [lectura("A", a), lectura("B", a)])
        # C no leyó B; D y E sí, y sin efectos: B solo entra si se recorre la unión, no solo los ids de C
        volcar(self.tree.path("r1", "C", "lote_00.json"), [lectura("A", a)])
        volcar(self.tree.path("r1", "D", "lote_00.json"), [lectura("A", a), lectura("B", {})])
        volcar(self.tree.path("r1", "E", "lote_00.json"), [lectura("A", a), lectura("B", {})])
        p = self.lotes(CLAVE, "--hueco", self.tree.path("r1"))
        self.assertEqual(self.tree.read_json("salida", "ids_hueco.json"), ["B"])
        self.assertIn("el lector C no leyó 1 iniciativas", p.stderr)

    def test_titulo_completo_de_items_para_encontrar_el_proyecto_de_ley(self):
        largo = "Proyecto de Ley " + "x" * 600 + " (procedente del Real Decreto-ley 3/2024, de 5 de marzo)."
        lotes = [{"id": "121/000005", "titulo": largo[:500]},  # el lote lo trae truncado, sin el real decreto-ley
                 {"id": "130/000003", "titulo": "Real Decreto-ley 3/2024, de 5 de marzo."}]
        self.tree.put_lotes(CLAVE, lotes)
        volcar(self.tree.path("data", "generado", CLAVE, "items.json"), [{"id": "121/000005", "titulo": largo}])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000005.txt"), "Texto del proyecto.")
        self.lotes(CLAVE)
        self.assertEqual(self.salida()["130/000003"]["texto"], "Texto del proyecto.")

    def test_sin_items_json_avisa_y_con_items_json_no(self):
        self.tree.put_lotes(CLAVE, [{"id": "121/000001", "titulo": "Ley uno."}])
        self.assertIn("no existe", self.lotes(CLAVE).stderr)
        volcar(self.tree.path("data", "generado", CLAVE, "items.json"), [{"id": "121/000001", "titulo": "Ley uno."}])
        self.assertNotIn("Aviso", self.lotes(CLAVE).stderr)

    def test_chars_cero_deja_el_texto_vacio(self):
        self.tree.put_lotes(CLAVE, [{"id": "121/000001", "titulo": "Ley uno."}])
        escribir(self.tree.path("data", "cache", "fx", "textos", "121_000001.txt"), "x" * 300)
        self.lotes(CLAVE, "--chars", "0")
        self.assertEqual(self.salida()["121/000001"]["texto"], "")


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
        self.assertEqual(AR.fecha_por_defecto(datetime.date(2027, 1, 2)), "02/01/2027")
        antes = datetime.date.today()
        self.aplicar("--fuente", "x")
        despues = datetime.date.today()  # tolera que el test cruce la medianoche
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertTrue(any(f"({AR.fecha_por_defecto(d)})" in rev for d in (antes, despues)), rev)

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

    # --- estado del repo para comprobar que un fallo no escribe nada
    def estado(self):
        base = self.tree.path("data", "clasificacion", CLAVE)
        return {f: leer(os.path.join(base, f)) for f in sorted(os.listdir(base)) if f.endswith((".json", ".md"))}, \
            os.path.isdir(os.path.join(base, "lectura_v3")), os.path.exists(self.tree.path("site", "data", CLAVE + ".json"))

    def editar_vigente(self, i, imp=None, **campos):
        f = self.tree.path("data", "clasificacion", CLAVE, "clas_0.json")
        datos = self.tree.read_json("data", "clasificacion", CLAVE, "clas_0.json")
        for it in datos:
            if it["id"] == i:
                if imp is not None:
                    it["imp"] = imp
                it.update(campos)
        volcar(f, datos)

    def cambiar_lecturas(self, i, imp):
        """Las tres lecturas de la ronda 1 pasan a dar `imp` en la iniciativa i."""
        for x in "CDE":
            f = self.tree.path("r1", x, "lote_00.json")
            volcar(f, [dict(it, imp=imp) if it["id"] == i else it for it in self.tree.read_json("r1", x, "lote_00.json")])

    def test_lector_sin_lotes_falla_sin_escribir(self):
        os.remove(self.tree.path("r1", "D", "lote_00.json"))
        antes = self.estado()
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("r1/D no tiene lotes", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_si_build_data_falla_se_restaura_todo(self):
        escribir(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"), "# Revisión\n\nprevio\n")
        escribir(self.tree.path("scripts", "build_data.py"), "import sys\nsys.exit('boom')\n")
        antes = self.estado()
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("restaurado", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_reaplicar_exige_rehacer_con_motivo(self):
        self.aplicar("--fuente", "x", "--fecha", "15/11/2026")
        antes = self.estado()
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertIn("ya existe", p.stderr)
        p = self.aplicar("--fuente", "x", "--rehacer", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--motivo", p.stderr)
        p = self.aplicar("--fuente", "x", "--rehacer", "--motivo", "  ", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.estado(), antes)
        self.aplicar("--fuente", "x", "--fecha", "16/11/2026", "--rehacer", "--motivo", "lecturas corregidas")
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertEqual(rev.count("## Reclasificación con la rúbrica v3"), 1)
        self.assertIn("Motivo: lecturas corregidas", rev)

    def test_vigente_editada_a_mano_tras_aplicar_obliga_a_decidir_cada_iniciativa(self):
        self.aplicar("--fuente", "x")
        self.editar_vigente("122/000002", {"casero": 1})
        antes = self.estado()
        # --rehacer + motivo solo autoriza repetir: no autoriza a perder la corrección
        p = self.aplicar("--fuente", "x", "--rehacer", "--motivo", "prueba", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("corregidas a mano después de las lecturas y se perderían: 122/000002", p.stderr)
        self.assertIn("Sin decidir", p.stderr)
        self.assertEqual(self.estado(), antes)
        # sobrescribir explícito
        self.aplicar("--fuente", "x", "--rehacer", "--motivo", "prueba", "--sobrescribir", "122/000002")
        self.assertEqual(self.final()["122/000002"]["imp"], {"jovenes": 1})
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn("Se han sobrescrito 1 iniciativas", rev)
        self.assertIn("122/000002", rev)
        # conservar explícito
        self.editar_vigente("122/000002", {"casero": 1})
        self.aplicar("--fuente", "x", "--rehacer", "--motivo", "prueba", "--conservar", "122/000002")
        self.assertEqual(self.final()["122/000002"]["imp"], {"casero": 1})
        self.assertEqual(self.final()["130/000003"]["imp"], {"prop1": -1})
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn("Se han conservado 1 iniciativas", rev)
        self.assertNotIn("Se han sobrescrito", rev)

    def test_conservar_y_sobrescribir_no_pueden_compartir_ids(self):
        p = self.aplicar("--fuente", "x", "--conservar", "122/000002", "--sobrescribir", "122/000002,130/000003", ok=False)
        self.assertIn("comparten ids", p.stderr)

    def test_rehacer_sin_lectura_previa_falla(self):
        antes = self.estado()
        p = self.aplicar("--fuente", "x", "--rehacer", "--motivo", "m", ok=False)
        self.assertIn("no existe", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_rehacer_con_lecturas_nuevas_y_vigente_sin_editar_no_bloquea(self):
        self.aplicar("--fuente", "x")
        self.cambiar_lecturas("122/000002", {"mayores": 1})
        p = self.aplicar("--fuente", "x", "--rehacer", "--motivo", "lecturas corregidas")
        self.assertNotIn("a mano", p.stderr)
        self.assertEqual(self.final()["122/000002"]["imp"], {"mayores": 1})

    def test_correccion_manual_solo_de_peso_o_de_tipo_tambien_cuenta(self):
        self.aplicar("--fuente", "x")
        for campo, valor, original in (("peso", 3, 1), ("tipo", "soc", "eco")):
            with self.subTest(campo=campo):
                self.editar_vigente("122/000002", **{campo: valor})
                p = self.aplicar("--fuente", "x", "--rehacer", "--motivo", "m", ok=False)
                self.assertNotEqual(p.returncode, 0)
                self.assertIn("se perderían: 122/000002", p.stderr)
                self.editar_vigente("122/000002", **{campo: original})

    def test_consolidacion_que_no_valida_falla_sin_escribir(self):
        for n, x in enumerate("CDE"):
            volcar(self.tree.path("r1", x, "lote_00.json"),
                   [lectura(it["id"], {"zzz": 1} if it["id"] == "121/000001" else it["imp"], it["peso"])
                    for it in self.tree.read_json("r1", x, "lote_00.json")])
        antes = self.estado()
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("colectivo desconocido", p.stdout + p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_colectivo_obsoleto_fuera_de_la_rubrica_no_bloquea_pero_se_avisa(self):
        self.editar_vigente("122/000002", {"viv2": 1})  # ninguna lectura lo usa, pero la rúbrica no lo menciona
        p = self.aplicar("--fuente", "x")
        self.assertIn("no coincide con ninguna lectura", p.stderr)
        self.assertIn("122/000002", p.stderr)
        self.assertNotIn("a mano", p.stderr)
        self.assertEqual(self.final()["122/000002"]["imp"], {"jovenes": 1})

    def test_colectivo_que_usan_las_lecturas_de_otra_legislatura_no_bloquea(self):
        self.con_casero_en_la_rubrica()
        volcar(self.tree.path("data", "clasificacion", "otra_leg", "lectura_v3", "C", "lote_00.json"), [lectura("X", {"casero": 1})])
        p = self.aplicar("--fuente", "x")
        self.assertNotIn("a mano", p.stderr)

    def test_edicion_posterior_a_la_version_anterior_se_avisa_sin_bloquear(self):
        # lecturas v2 idénticas a la vigente (mismo tipo y peso): solo la iniciativa editada difiere
        vig = self.tree.read_json("data", "clasificacion", CLAVE, "clas_0.json")
        for x in "CDE":
            volcar(self.tree.path("data", "clasificacion", CLAVE, "lectura_v2", x, "lote_00.json"), vig)
        self.editar_vigente("122/000002", {"inq": 1})  # la vigente ya no es la consolidación de la v2
        p = self.aplicar("--fuente", "x")
        aviso = [l for l in p.stderr.splitlines() if l.startswith("AVISO")]
        self.assertEqual(len(aviso), 1, p.stderr)
        self.assertIn("lectura_v2", aviso[0])
        self.assertIn("122/000002", aviso[0])
        self.assertNotIn("130/000009", aviso[0])
        self.assertIn("1 iniciativas", aviso[0])

    def test_sobrescribir_un_id_desconocido_falla(self):
        antes = self.estado()
        p = self.aplicar("--fuente", "x", "--sobrescribir", "999/000001", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("no están en la clasificación vigente", p.stderr)
        self.assertIn("999/000001", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_sobrescribir_un_id_no_editado_falla(self):
        antes = self.estado()
        p = self.aplicar("--fuente", "x", "--sobrescribir", "130/000003", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("nada que sobrescribir", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_conservar_un_id_no_editado_se_acepta_con_otra_redaccion_en_revision(self):
        self.con_casero_en_la_rubrica()  # 122/000002 sí detectada; 130/000003 se conserva sin que lo parezca
        self.aplicar("--fuente", "x", "--conservar", "122/000002,130/000003")
        rev = leer(self.tree.path("data", "clasificacion", CLAVE, "REVISION.md"))
        self.assertIn("conservado 1 iniciativas con la clasificación que ya tenían (correcciones manuales detectadas "
                      "posteriores a las lecturas): 122/000002.", rev)
        self.assertIn("conservado 1 iniciativas por decisión manual (no se detectó ninguna corrección posterior a las "
                      "lecturas): 130/000003.", rev)
        self.assertEqual(self.final()["130/000003"]["imp"], {"prop1": -1})

    def con_casero_en_la_rubrica(self):
        escribir(self.tree.path("data", "clasificacion", "RUBRICA.md"),
                 "# Rúbrica\n\nVersión 3 (fecha 04/11/2026).\n\nNuevo colectivo `casero`.\n")
        self.editar_vigente("122/000002", {"casero": 1})  # corrección manual posterior a las lecturas

    def test_colectivo_de_la_rubrica_que_ninguna_lectura_conoce_bloquea_la_primera_aplicacion(self):
        self.con_casero_en_la_rubrica()
        antes = self.estado()
        p = self.aplicar("--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("122/000002", p.stderr)
        self.assertIn("--conservar", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_conservar_por_ids_o_por_fichero_mantiene_el_valor(self):
        self.con_casero_en_la_rubrica()
        self.aplicar("--fuente", "x", "--conservar", "122/000002")
        self.assertEqual(self.final()["122/000002"]["imp"], {"casero": 1})
        self.assertEqual(self.final()["130/000003"]["imp"], {"prop1": -1})
        volcar(self.tree.path("conservar.json"), ["122/000002"])
        self.aplicar("--fuente", "x", "--rehacer", "--motivo", "m", "--conservar", self.tree.path("conservar.json"))
        self.assertEqual(self.final()["122/000002"]["imp"], {"casero": 1})

    def test_sobrescribir_decide_la_primera_aplicacion(self):
        self.con_casero_en_la_rubrica()
        self.aplicar("--fuente", "x", "--sobrescribir", "122/000002")
        self.assertEqual(self.final()["122/000002"]["imp"], {"jovenes": 1})

    def test_conservar_un_id_que_no_existe_falla(self):
        antes = self.estado()
        p = self.aplicar("--fuente", "x", "--conservar", "999/000001", ok=False)
        self.assertIn("999/000001", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_las_secciones_posteriores_de_revision_se_conservan(self):
        rev = self.tree.path("data", "clasificacion", CLAVE, "REVISION.md")
        escribir(rev, "# Revisión\n\n## Antes\n\nA\n\n## Reclasificación con la rúbrica v3 (01/01/2026)\n\nviejo\n\n"
                      "## Revisiones posteriores\n\n- 04/11/2026 · 121/000021: casero.\n")
        self.aplicar("--fuente", "x", "--fecha", "15/11/2026")
        self.aplicar("--fuente", "x", "--fecha", "16/11/2026", "--rehacer", "--motivo", "m")
        txt = leer(rev)
        self.assertIn("## Revisiones posteriores\n\n- 04/11/2026 · 121/000021: casero.\n", txt)
        self.assertIn("## Antes\n\nA", txt)
        self.assertEqual(txt.count("## Reclasificación con la rúbrica v3"), 1)
        self.assertIn("(16/11/2026)", txt)
        self.assertNotIn("viejo", txt)

    # --- ronda 2
    def r2_en(self, lector, items):
        volcar(self.tree.path("r2", lector, "lote_00.json"), items)

    def test_ronda2_incompleta_en_un_lector_falla_antes_de_escribir(self):
        self.r2_en("E", [])
        antes = self.estado()
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("Ronda 2 parcial", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_ronda2_con_ids_que_no_estan_en_la_ronda1_falla(self):
        for x in "CDE":
            self.r2_en(x, [lectura("122/000004", {"mayores": 1}, 2), lectura("999/000001", {"mayores": 1}, 2)])
        antes = self.estado()
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x", ok=False)
        self.assertIn("no están en la ronda 1", p.stderr)
        self.assertEqual(self.estado(), antes)

    def test_ronda2_debe_coincidir_con_ids_hueco(self):
        volcar(self.tree.path("r2", "ids_hueco.json"), ["122/000004", "121/000001"])
        antes = self.estado()
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x", ok=False)
        self.assertIn("ids_hueco.json", p.stderr)
        self.assertEqual(self.estado(), antes)
        volcar(self.tree.path("r2", "ids_hueco.json"), ["122/000004"])
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x")
        self.assertEqual(json.loads(p.stdout.strip().splitlines()[-1])["ronda2"], 1)

    def test_ronda2_ids_hueco_por_opcion(self):
        volcar(self.tree.path("hueco.json"), ["121/000001"])
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x", "--ids-hueco", self.tree.path("hueco.json"), ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("hueco.json", p.stderr)

    def test_n2_cuenta_solo_los_ids_aplicados(self):
        p = self.aplicar(self.tree.path("r2"), "--fuente", "x")
        self.assertEqual(json.loads(p.stdout.strip().splitlines()[-1])["ronda2"], 1)


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

    def cerrar_simulado(self, validacion):
        """Ejecuta main() con los pasos externos simulados; devuelve (órdenes lanzadas, excepción o None)."""
        escribir(self.tmp.path("site", "template.html"), self.PLANTILLA + '<span id="alcance-v3">v</span>')
        escribir(self.tmp.path("data", "clasificacion", "RUBRICA.md"), "Versión 3 (fecha 04/11/2026).\n")
        volcar(self.tmp.path("data", "analisis", "sesgo.json"), {"legislaturas": self.SESGO})
        os.makedirs(self.tmp.path("data", "clasificacion", "congreso_xv", "lectura_v3"), exist_ok=True)
        ordenes = []

        def run(*cmd):
            ordenes.append(os.path.basename(cmd[1]))
            if cmd[1].endswith("build_page.py"):  # build_page lee la plantilla: ya debe estar escrita
                self.plantilla_en_build_page = leer(self.tmp.path("site", "template.html"))
            return validacion if cmd[1].endswith("validar_clasificacion.py") else ""
        tests = types.SimpleNamespace(returncode=0, stderr="a\nb\nc\nOK")
        err = None
        with mock.patch.object(CR, "ROOT", self.tmp.root), mock.patch.object(CR, "run", run), \
                mock.patch.object(CR.subprocess, "run", return_value=tests):
            try:
                CR.main([])
            except SystemExit as e:
                err = e
        return ordenes, err

    def test_cerrar_valida_las_clasificaciones_antes_de_regenerar_la_pagina(self):
        n = len(CR.LEGISLATURAS)
        ordenes, err = self.cerrar_simulado(" 0 errores" * (n - 1) + " 2 errores")
        self.assertIsNotNone(err)
        self.assertIn("Validación con errores", str(err))
        self.assertNotIn("build_page.py", ordenes)
        # la plantilla no se toca hasta que valida
        self.assertEqual(leer(self.tmp.path("site", "template.html")), self.PLANTILLA + '<span id="alcance-v3">v</span>')
        ordenes, err = self.cerrar_simulado(" 0 errores" * n)
        self.assertIsNone(err)
        self.assertEqual(ordenes, ["prueba_sesgo.py", "validar_clasificacion.py", "build_page.py"])
        self.assertIn("Están clasificadas con la v3", self.plantilla_en_build_page)
        self.assertIn("EH Bildu · 41,3 %", self.plantilla_en_build_page)

    def test_cifras_falla_y_nombra_la_frase_que_ya_no_casa(self):
        for quitar in ('en la XI, en leyes sociales, VOX sale primero en el 5,0 % de los perfiles', '9.ª · 2019–2024'):
            with self.subTest(quitar=quitar), self.assertRaises(SystemExit) as cm:
                CR.actualizar_cifras(self.PLANTILLA.replace(quitar, "XX"), self.SESGO)
            self.assertIn("ya no casan", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
