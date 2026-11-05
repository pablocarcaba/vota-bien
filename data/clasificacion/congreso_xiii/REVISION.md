# Clasificaciones pendientes de revisión (XIII legislatura)

88 iniciativas; 60 reutilizan la clasificación de su equivalente en la XIV. Solo 15 votaciones en el Pleno (legislatura de cuatro meses sin investidura).

## Dudas

- [ ] 130/000007 (RDL 17/2019, retribución eléctrica y cierre de térmicas): vacía, signo mixto.
- [ ] 122/000013 (ITP-AJD, art. 31.2): se supone el AJD de las hipotecas (`+hipot`, `+secFin`).
- [ ] 122/000053 (UP, suficiencia de ingresos): solo `+pobreza`.
- [ ] 125/000005 y 125/000010 (Navarra, Seguridad Social y SNS): vacías por no conocer el contenido.
- [ ] 122/000031 y 122/000038 (igualdad en el empleo): solo `+mujeres`, sin coste para empresas.
- [ ] 122/000025 (cierre de nucleares): `-secInd`, `-empGran`, sin `ciud`.
- [ ] 122/000022 (nulidad de la Ley de Amnistía de 1977): `+victimas`.
- [ ] 130/000001 (RDL 11/2019, DANA): peso 1.
- [ ] Partido del Grupo Mixto: solo identificado 123/000002 (Compromís); el resto de proposiciones son de grupos con un único partido.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 88 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 10 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 83–84 % idéntica, parecido medio 0.9, 1 con signo contrario; 69 de 88 idénticas en las tres lecturas.
- 38 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 37 antes, 42 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [ ] **Prestación de ingresos mínimos** (120/000002, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.
