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

    def test_metodologia_declara_la_fraccion_de_no_lo_se(self):
        self.assertIn(f"el {P.P_NS * 100:.0f} % de las personas asalariadas y del sector público responde «No lo sé»", TPL)

    def test_redondeo_como_js(self):
        self.assertEqual([P.js_round(x) for x in (0.5, 1.5, -0.5, -1.5, 2.4)], [1, 2, 0, -1, 2])


def ley(tramos, signo=1, **extra):
    imp = {t: signo for t in tramos}
    imp.update(extra)
    return {"id": "x", "tp": "eco", "imp": imp, "w": 1, "a": [], "v": {"A": "s"}, "vk": "Votación final"}


class TestNoLoSe(unittest.TestCase):
    """«No lo sé» en el tramo de IRPF: el mismo camino en la web (impNs) y en la prueba de sesgo (imp_ns)."""

    def test_constantes_como_la_web(self):
        m = re.search(r"const TRAMOS = \[([^\]]*)\], NS_MIN = (\d+);", TPL)
        self.assertIsNotNone(m, "la web ya no define TRAMOS y NS_MIN")
        self.assertEqual(re.findall(r"'(\w+)'", m.group(1)), P.TRAMOS)
        self.assertEqual(int(m.group(2)), P.NS_MIN)

    def test_la_web_usa_la_regla(self):
        self.assertIn("return n>=NS_MIN ? Math.sign(s) : 0;", TPL)
        self.assertIn("k==='asalNs' ? impNs(it) : it.imp[k]", TPL)
        self.assertIn("if(state.pasos.ui.has('asalNs')) r.add('asalNs');", TPL)
        self.assertIn("const v=impDe(it,k);", TPL)

    def test_leyes_de_3_o_mas_tramos_cuentan_con_su_signo(self):
        R = P.rasgos({"asalNs"})
        self.assertEqual(P.impact_of(ley(["asal1", "asal2", "asal3"]), R), "pos")
        self.assertEqual(P.impact_of(ley(P.TRAMOS, -1), R), "neg")

    def test_leyes_de_1_o_2_tramos_no_cuentan(self):
        R = P.rasgos({"asalNs"})
        self.assertEqual(P.impact_of(ley(["asal1"]), R), "neu")
        self.assertEqual(P.impact_of(ley(["asal5", "asal6"], -1), R), "neu")

    def test_signos_mezclados_suma(self):
        it = ley(["asal1", "asal2", "asal3"])
        it["imp"]["asal6"] = -1
        self.assertEqual(P.imp_ns(it), 1)
        it["imp"].update(asal4=-1, asal5=-1)
        self.assertEqual(P.imp_ns(it), 0)

    def test_entra_en_el_ranking(self):
        items = [ley(["asal1", "asal2", "asal3", "asal4"]), ley(["asal1"], -1)]
        r = P.compute_rank(items, ["A"], P.rasgos({"asalNs"}), "eco")
        self.assertEqual(r, [{"k": "A", "s": P.js_round(1 / (1 + P.K) * 100), "rel": 1}])

    def test_la_muestra_aleatoria_recorre_el_camino(self):
        rng = P.random.Random(2026)
        muestra = [P.aleatorio(rng) for _ in range(2000)]
        asal = [s for s in muestra if s & (set(P.TRABAJO["asal"]) | {"asalNs"})]
        ns = [s for s in asal if "asalNs" in s]
        self.assertTrue(ns, "ningún perfil aleatorio usa «No lo sé»")
        self.assertTrue(0.18 <= len(ns) / len(asal) <= 0.32, len(ns) / len(asal))
        # como en la web: «No lo sé» y un tramo concreto se excluyen
        self.assertFalse([s for s in ns if s & set(P.TRABAJO["asal"])])
        # y llega al cálculo: con «No lo sé» cambia el resultado frente a no contar ningún tramo
        items = [ley(P.TRAMOS)]
        self.assertNotEqual(P.compute_rank(items, ["A"], P.rasgos(ns[0]), "eco"),
                            P.compute_rank(items, ["A"], P.rasgos(ns[0] - {"asalNs"}), "eco"))


class TestMargen(unittest.TestCase):
    """Margen entre el 1.º y el 2.º y empate técnico en cabeza: el mismo umbral que marca la web."""

    def test_umbral_como_la_web(self):
        m = re.search(r"const EMPATE = (\d+);", TPL)
        self.assertIsNotNone(m, "la web ya no define EMPATE")
        self.assertEqual(int(m.group(1)), P.EMPATE)
        self.assertIn("rows[0].s-rows[1].s<=EMPATE", TPL)

    def test_margen_y_partidos_cerca(self):
        r = lambda *ss: [{"k": str(i), "s": s, "rel": 3} for i, s in enumerate(ss)]
        self.assertEqual(P.cabeza(r(50, 48, 47, 40)), (2, 2))
        self.assertEqual(P.cabeza(r(50, 46, 46)), (4, 0))
        self.assertEqual(P.cabeza(r(-10, -13)), (3, 1))
        self.assertEqual(P.cabeza(r(50)), (None, 0))

    def test_resumen(self):
        c = [(0, 3), (1, 1), (2, 2), (5, 0), (None, 0)]
        self.assertEqual(P.resumen_cabeza(c, 5), {"margen_mediano": 1.5, "empate_tecnico_pct": 60.0, "empate_varios_pct": 40.0})
        self.assertEqual(P.resumen_cabeza([], 0), {"margen_mediano": None, "empate_tecnico_pct": 0, "empate_varios_pct": 0})

    def test_se_calcula_sobre_el_ranking_real(self):
        # A vota a favor de dos leyes que te benefician, B de una: A +17, B +10 -> margen 7
        it = lambda i, votos: {"id": i, "tp": "eco", "imp": {"asal1": 1}, "w": 1, "a": [], "v": votos, "vk": "Votación final"}
        items = [it("1", {"A": "s", "B": "s"}), it("2", {"A": "s"})]
        rank = P.compute_rank(items, ["A", "B"], P.rasgos({"asal1"}), "eco")
        self.assertEqual([x["s"] for x in rank], [P.js_round(200 / 11), P.js_round(100 / 10)])
        self.assertEqual(P.cabeza(rank), (rank[0]["s"] - rank[1]["s"], 0))


if __name__ == "__main__":
    unittest.main()
