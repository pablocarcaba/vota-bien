"""Privacidad retroactiva del perfil guardado (site/template.html).

Hasta la v10, sexo, estado civil, cuidados, medio rural y ayuda social iban en el paso 4, que prometía no salir del
dispositivo. Ahora van en los pasos 1 a 3 y sí viajan en los enlaces. Un perfil guardado sin versión (pasosPerfil sin `v`)
no puede sacarlas en el enlace hasta que se confirma su paso o se vuelve a tocar la pregunta.

Ejecuta con node las funciones reales de la plantilla (cargarGuardado, shareUrl, continuar, elegir…) con stubs del DOM.
"""
import json
import os
import re
import shutil
import subprocess
import unittest

from helpers import REPO

TPL = open(os.path.join(REPO, "site", "template.html"), encoding="utf-8").read()
FUNCIONES = ["qName", "qOpts", "qSolo", "visible", "respondida", "faltan", "completo", "terminado", "minimoActual",
             "avisaMinimo", "deriva", "guardarPasos", "cargarGuardado", "confirma", "shareUrl", "continuar", "elegir",
             "yLista", "nombresRet", "marcada", "retPaso", "liberarTodo", "qDe", "cierra", "pasoRev", "textoBoton"]
MOVIDAS = ["mujeres", "civViu", "cuid", "rural", "pobreza"]
# perfil de la v10: pasos 1 a 4 hechos, con las respuestas que entonces estaban en el paso 4
V10 = {"sel": ["adultos", "hij0", "asal3", "prop1"] + MOVIDAS, "ui": ["trAjena", "vdAlq", "nv0"], "done": [0, 1, 2, 3], "cur": -1}


def funcion(nombre):
    m = re.search(r"\nfunction %s\(" % nombre, TPL)
    assert m, nombre
    i, nivel = TPL.index("{", m.end()), 0
    for j in range(i, len(TPL)):
        nivel += {"{": 1, "}": -1}.get(TPL[j], 0)
        if nivel == 0:
            return TPL[m.start() + 1:j + 1]
    raise AssertionError("llaves sin cerrar en " + nombre)


PRELUDIO = """
const ALMACEN = {}, localStorage = {getItem:k=>k in ALMACEN ? ALMACEN[k] : null, setItem:(k,v)=>{ ALMACEN[k]=String(v); }, removeItem:k=>{ delete ALMACEN[k]; }};
const location = {origin:'https://x.test', pathname:'/', search:''};
const CATALOGO = [{clave:'congreso_xv'}], PARTIES = [];
let PEND = '', DESHACER = null, isExample = false;
const FOCO = [], IRPASO = [];
const render = ()=>{}, irPaso = i=>IRPASO.push(i), verResultado = ()=>IRPASO.push('resultado'), $ = id=>({focus:()=>FOCO.push(id)});
const state = {tab:'eco', ds:'congreso_xv', sel:new Set(['ciud','cons']), prov:'', pasos:{ui:new Set(), done:new Set(), cur:0, ret:new Set(), aviso:false}};
"""


def ejecutar(cuerpo):
    i, j = TPL.index("const CATS = ["), TPL.index("const CHECK")
    esperfil = re.search(r"const esPerfil = .*\n", TPL).group(0)
    js = PRELUDIO + TPL[i:j] + esperfil + "\n".join(funcion(f) for f in FUNCIONES) + "\n" + cuerpo
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if out.returncode:
        raise AssertionError(out.stderr)
    return json.loads(out.stdout)


def claves(url):
    q = dict(x.split("=", 1) for x in url.split("?", 1)[1].split("#")[0].split("&"))
    return set(q.get("p", "").split(",")) | set(q.get("u", "").split(",")), q


@unittest.skipUnless(shutil.which("node"), "hace falta node")
class PrivacidadRetroactivaTest(unittest.TestCase):
    def test_perfil_heredado_no_saca_las_respuestas_movidas(self):
        d = ejecutar("cargarGuardado(%s); deriva();"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true), ret:[...state.pasos.ret], aviso:state.pasos.aviso}));"
                     % json.dumps(V10))
        k, _ = claves(d["url"])
        for m in MOVIDAS:
            self.assertNotIn(m, k, m)
        self.assertIn("asal3", k)
        self.assertEqual(set(d["ret"]), set(MOVIDAS))
        self.assertTrue(d["aviso"])

    def test_confirmar_cada_paso_las_vuelve_a_sacar(self):
        d = ejecutar("cargarGuardado(%s); deriva(); const r=[];"
                     "continuar(0); r.push(shareUrl(null,null,true));"
                     "continuar(1); r.push(shareUrl(null,null,true));"
                     "continuar(2); r.push(shareUrl(null,null,true));"
                     "process.stdout.write(JSON.stringify({r, aviso:state.pasos.aviso, guardado:JSON.parse(ALMACEN.pasosPerfil)}));"
                     % json.dumps(V10))
        k1, k2, k3 = (claves(u)[0] for u in d["r"])
        self.assertTrue({"mujeres", "civViu", "cuid"} <= k1)
        self.assertFalse({"pobreza", "rural"} & k1)
        self.assertIn("pobreza", k2)
        self.assertNotIn("rural", k2)
        self.assertIn("rural", k3)
        self.assertFalse(d["aviso"])
        self.assertEqual(d["guardado"]["v"], 2)
        self.assertEqual(d["guardado"]["ret"], [])

    def test_tocar_la_pregunta_tambien_confirma(self):
        d = ejecutar("cargarGuardado(%s); deriva(); state.pasos.cur=0;"
                     "elegir(PASOS[0].q.find(q=>q.id==='civ'), 'civSep');"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true)}));" % json.dumps(V10))
        k, _ = claves(d["url"])
        self.assertIn("civSep", k)
        self.assertNotIn("mujeres", k)

    def test_la_retencion_sobrevive_a_recargar(self):
        # se guarda con versión y la retención no se pierde al volver a cargar
        d = ejecutar("cargarGuardado(%s); deriva(); guardarPasos();"
                     "const g=JSON.parse(ALMACEN.pasosPerfil); state.sel=new Set(['ciud','cons']); state.pasos={ui:new Set(),done:new Set(),cur:0,ret:new Set(),aviso:false};"
                     "cargarGuardado(g); deriva();"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true), v:g.v}));" % json.dumps(V10))
        self.assertEqual(d["v"], 2)
        self.assertFalse(set(MOVIDAS) & claves(d["url"])[0])

    def test_perfil_con_version_no_retiene_nada(self):
        g = dict(V10, v=2, ret=[], aviso=False)
        d = ejecutar("cargarGuardado(%s); deriva();"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true), aviso:state.pasos.aviso}));" % json.dumps(g))
        self.assertTrue(set(MOVIDAS) <= claves(d["url"])[0])
        self.assertFalse(d["aviso"])

    def test_boton_incluir_libera_todo_y_lo_anuncia(self):
        # «Incluir también estas respuestas en mis enlaces»: decisión explícita, libera todo lo retenido de una vez
        d = ejecutar("cargarGuardado(%s); deriva(); const antes=shareUrl(null,null,true); liberarTodo(true);"
                     "process.stdout.write(JSON.stringify({antes, url:shareUrl(null,null,true), ret:[...state.pasos.ret], aviso:state.pasos.aviso,"
                     "pend:PEND, foco:FOCO, guardado:JSON.parse(ALMACEN.pasosPerfil)}));" % json.dumps(V10))
        self.assertFalse(set(MOVIDAS) & claves(d["antes"])[0])
        self.assertTrue(set(MOVIDAS) <= claves(d["url"])[0])
        self.assertEqual(d["ret"], [])
        self.assertFalse(d["aviso"])
        self.assertEqual(d["guardado"]["ret"], [])
        self.assertFalse(d["guardado"]["aviso"])
        self.assertIn("Ya se incluyen en los enlaces: sexo, estado civil, cuidados, ayuda social y medio rural.", d["pend"])
        self.assertIn("Se ha cerrado el aviso", d["pend"])
        self.assertIn("Compartir mi perfil", d["pend"])
        self.assertEqual(d["foco"], ["copy-btn"])

    def test_los_datos_sensibles_siguen_fuera_tras_liberar(self):
        g = dict(V10, sel=V10["sel"] + ["lgtbi"], ui=V10["ui"] + ["sexOtro"])
        d = ejecutar("cargarGuardado(%s); deriva(); liberarTodo(false);"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true), foco:FOCO}));" % json.dumps(g))
        k = claves(d["url"])[0]
        self.assertFalse({"lgtbi", "sexOtro"} & k)
        self.assertEqual(d["foco"], ["filters-h"])

    def test_continuar_lleva_al_siguiente_paso_con_retenidas(self):
        # con todos los pasos hechos, «Continuar» en el paso 1 no salta al resultado si quedan retenidas en otro paso
        d = ejecutar("cargarGuardado(%s); deriva(); state.pasos.cur=0; continuar(0); const a=[...IRPASO];"
                     "continuar(1); const b=[...IRPASO]; continuar(2);"
                     "process.stdout.write(JSON.stringify({a, b, c:IRPASO, pend:PEND}));" % json.dumps(V10))
        self.assertEqual(d["a"], [1])
        self.assertEqual(d["b"], [1, 2])
        self.assertEqual(d["c"], [1, 2, "resultado"])
        self.assertIn("Ya se incluyen en los enlaces: sexo, estado civil y cuidados.", d["pend"])

    def test_quitar_una_respuesta_no_anuncia_que_se_incluye(self):
        d = ejecutar("cargarGuardado(%s); deriva(); state.sel.delete('cuid'); confirma(['cuid']);"
                     "process.stdout.write(JSON.stringify({pend:PEND, ret:[...state.pasos.ret]}));" % json.dumps(V10))
        self.assertEqual(d["pend"], "")
        self.assertNotIn("cuid", d["ret"])

    def test_boton_del_paso_con_retenidas_en_otro_paso(self):
        # el texto del botón es el de adónde lleva continuar(): con retenidas en otro paso, «Continuar», no «Ver mi resultado»
        d = ejecutar("cargarGuardado(%s); deriva(); const t=[0,1,2,3].map(textoBoton), r=[0,1,2].map(pasoRev);"
                     "continuar(0); continuar(1); const u=[textoBoton(2), pasoRev(2)];"
                     "process.stdout.write(JSON.stringify({t, r, u}));" % json.dumps(V10))
        self.assertEqual(d["t"], ["Continuar", "Continuar", "Continuar", "Continuar"])
        self.assertEqual(d["r"], [1, 0, 0])
        # solo queda retenido el paso 3: su botón ya lleva al resultado
        self.assertEqual(d["u"], ["Ver mi resultado", -1])

    def test_desmarcar_y_volver_a_marcar_se_anuncia(self):
        # desmarcar una retenida no la libera; volver a marcarla sí, y se anuncia como las otras vías
        d = ejecutar("cargarGuardado(%s); deriva(); state.pasos.cur=0; const q=PASOS[0].q.find(q=>q.id==='civ');"
                     "elegir(q,'civViu'); const a={pend:PEND, ret:state.pasos.ret.has('civViu')}; PEND='';"
                     "elegir(q,'civViu'); const b={pend:PEND, url:shareUrl(null,null,true)};"
                     "process.stdout.write(JSON.stringify({a, b}));" % json.dumps(V10))
        self.assertEqual(d["a"]["pend"], "")
        self.assertTrue(d["a"]["ret"])
        self.assertIn("Ya se incluyen en los enlaces: estado civil.", d["b"]["pend"])
        self.assertIn("civViu", claves(d["b"]["url"])[0])

    def test_cambiar_de_opcion_en_una_retenida_se_anuncia(self):
        d = ejecutar("cargarGuardado(%s); deriva(); state.pasos.cur=0;"
                     "elegir(PASOS[0].q.find(q=>q.id==='civ'),'civSep'); process.stdout.write(JSON.stringify({pend:PEND}));" % json.dumps(V10))
        self.assertIn("Ya se incluyen en los enlaces: estado civil.", d["pend"])

    def test_la_provincia_va_en_el_enlace(self):
        d = ejecutar("state.prov='50'; cargarGuardado(%s); deriva();"
                     "process.stdout.write(JSON.stringify({url:shareUrl(null,null,true)}));" % json.dumps(V10))
        self.assertEqual(claves(d["url"])[1].get("prov"), "50")


if __name__ == "__main__":
    unittest.main()
