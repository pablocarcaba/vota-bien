# Relectura ómnibus del repaso de REVISION.md (06/11/2026)

Cuatro reales decretos-ley que el repaso de las dudas de `REVISION.md` señaló como ómnibus sin `medidas` o con bloques perdidos: RDL 8/2014 (congreso_x 130/000055, y su proyecto 121/000104), RDL 12/2012 (130/000013), RDL 16/2013 (130/000046) y RDL 8/2019 (congreso_xii 130/000063).

Tres lectores independientes (C, D, E) con el prompt de `../PROMPT_LECTOR.md` («Ronda de leyes ómnibus») y el texto del BOE (`scripts/textos_boe.py`):
1. `ronda1/`: primeros 60.000 caracteres de cada texto.
2. `ronda2/`: segunda parte (desde el carácter 55.000) de los dos textos más largos (RDL 8/2014 y 8/2019); cada lector solo añade bloques nuevos.

`combinar.py` une las dos rondas lector a lector con la regla de `../lectura_omnibus/combinar.py` (un bloque ya cubierto por una medida no se suma); `final/` son las lecturas combinadas; `consolidada.json` y `CAMBIOS.md`, la mayoría 2 de 3 de `scripts/consolidar_medidas.py`, aplicada con `--aplicar`.
