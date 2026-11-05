# Clasificaciones pendientes de revisión (XI legislatura)

51 iniciativas; unas 25 reutilizan la clasificación de su equivalente en la XIII, XIV o XV. Legislatura de cuatro meses sin investidura.

## Dudas

- [ ] 122/000015 y 122/000018 (tasas judiciales): `+empMicro`/`+empPeq` porque solo pagan personas jurídicas.
- [ ] 122/000016 (PP, segunda oportunidad) y 125/000002 (Baleares, emprendedores): vacías por no conocer el contenido.
- [ ] 122/000020 (art. 42.1 ET, subcontratas): solo `+asal1`/`+asal2`.
- [ ] 122/000021 (tasa AEDE): vacía por efectos contrapuestos en `secDig`.
- [ ] 122/000024 (CP, PNV): se supone prisión permanente revisable.
- [ ] 122/000025-27 (autoconsumo del ciclo del agua) y 125/000003 (autoconsumo, Murcia): criterio de `secInd` distinto del de la XIV.
- [ ] 123/000001 (Ley 25 de emergencia social): contenido de memoria; peso 3.
- [ ] 122/000001 (suspensión de la LOMCE): vacía, peso 2.
- [x] 122/000034 (Grupo Mixto): UPN, según la firma del BOCG.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 51 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 8 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 80–88 % idéntica, parecido medio 0.88, 0 con signo contrario; 40 de 51 idénticas en las tres lecturas.
- 20 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 29 antes, 29 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [ ] **Prestación de ingresos mínimos** (120/000003, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.
