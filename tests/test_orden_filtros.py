"""Los controles que filtran van antes de lo que filtran, también en el orden del DOM (lectores de pantalla y teclado).

- Ranking: «Ajustar el ranking» se pinta en #raj, dentro de la barra #rtools (pestañas y provincia), que va antes de #rank.
  Nunca se añade dentro de #rank, donde quedaría debajo de las filas.
- Ley a ley: el filtro de efecto se añade a la vista antes que la lista (.items); en la ficha, tipo de leyes y partido
  van en la cabecera (cambian la nota y los plegables), antes que todo lo demás.
"""
import os
import re
import unittest

from helpers import REPO

TPL = open(os.path.join(REPO, "site", "template.html"), encoding="utf-8").read()


def funcion(nombre):
    m = re.search(r"function %s\(" % nombre, TPL)
    assert m, nombre
    i, nivel = TPL.index("{", m.end()), 0
    for j in range(i, len(TPL)):
        nivel += {"{": 1, "}": -1}.get(TPL[j], 0)
        if nivel == 0:
            return TPL[m.start():j + 1]
    raise AssertionError("llaves sin cerrar en " + nombre)


class OrdenFiltrosTest(unittest.TestCase):
    def test_ajustar_en_la_barra_antes_del_ranking(self):
        barra = re.search(r'<div class="rtools" id="rtools">.*?</div></div>', TPL).group(0)
        self.assertIn('id="raj"', barra)
        self.assertLess(TPL.index('id="rtools"'), TPL.index('id="rank"'))
        rank = funcion("renderRank")
        self.assertIn("$('raj').appendChild(ajustarEl())", rank)
        self.assertNotIn("r.appendChild(ajustarEl())", rank)

    def test_filtros_de_la_lista_antes_de_la_lista(self):
        lista = funcion("renderList")
        self.assertLess(lista.index("v.appendChild(filtros('lfilters'"), lista.index("const list=el('div',{class:'items'})"))
        # en la ficha, tipo de leyes y partido van en la cabecera, antes de la nota
        self.assertLess(lista.index("head.appendChild(filtros('lfilters ltop'"), lista.index("class:'lscore'"))


if __name__ == "__main__":
    unittest.main()
