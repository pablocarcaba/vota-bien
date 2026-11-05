# Lecturas de la ronda de leyes ómnibus (medidas, rúbrica 3.8)

Tres lectores independientes (C, D, E; modelos de IA sin ver la clasificación vigente ni a los otros) por ley, con el
prompt de `../PROMPT_LECTOR.md` («Ronda de leyes ómnibus»). Textos: BOCG o, en los reales decretos-ley, BOE
(`scripts/textos_boe.py`). Las 57 leyes son las que una primera lectura exploratoria dividió en medidas, más 4 dudosas.

Rondas, por lector (`combinar.py` las une):
1. 20.000 caracteres de texto (todas).
2. Preámbulo completo hasta 70.000 caracteres (43 leyes a las que la ronda 1 les perdía bloques por el corte).
3. RDL 7/2024 de nuevo, con el texto bien recortado (su lote empezaba a mitad del preámbulo).
4. Segunda parte del preámbulo (desde el carácter 65.000) de 16 reales decretos-ley; sus bloques se suman a la
   lectura del mismo lector salvo los que repiten colectivos y signos de una medida ya leída.

`lecturas.json` de cada lector es la lectura combinada; `consolidada.json`, la mayoría 2 de 3
(`scripts/consolidar_medidas.py`); `CAMBIOS.md`, las diferencias con la clasificación anterior. Decisión manual
posterior: RDL 2/2026 (congreso_xv 130/000033) sin −`casero`, porque excluye de la suspensión a quien tiene dos
viviendas o menos (anotado en `congreso_xv/REVISION.md`).
