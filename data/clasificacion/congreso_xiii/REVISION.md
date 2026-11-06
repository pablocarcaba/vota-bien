# Clasificaciones pendientes de revisión (XIII legislatura)

88 iniciativas; 60 reutilizan la clasificación de su equivalente en la XIV. Solo 15 votaciones en el Pleno (legislatura de cuatro meses sin investidura).

## Dudas

- [x] 130/000007 (RDL 17/2019, retribución eléctrica y cierre de térmicas): vacía, signo mixto. — Resuelta (06/11/2026): v3: `{}`, peso 1 (tres lectores: ajustes de retribución y cierre de térmicas sin signo único, 3.1.1).
- [x] 122/000013 (ITP-AJD, art. 31.2): se supone el AJD de las hipotecas (`+hipot`, `+secFin`). — Aplicada (06/11/2026): `{"hipot": 1, "viv0": 1}` → `{"secFin": 1}` (el sujeto pasivo del AJD es la entidad prestamista; el ahorro de `hipot` y `viv0` depende de que lo traslade, P2), nota actualizada.
- [x] 122/000053 (UP, suficiencia de ingresos): solo `+pobreza`. — Resuelta (06/11/2026): v3: `{}`, peso 1; caducó sin publicarse (la caché solo trae el anuncio de caducidad), así que el contenido no se conoce (3.9).
- [x] 125/000005 y 125/000010 (Navarra, Seguridad Social y SNS): vacías por no conocer el contenido. — Resuelta (06/11/2026): v3 con el texto: 125/000005 `{}` (desempleo de parlamentarios autonómicos, sin colectivo); 125/000010 `+ciud`, `+inmigrantes`, `+pac`.
- [x] 122/000031 y 122/000038 (igualdad en el empleo): solo `+mujeres`, sin coste para empresas. — Resuelta (06/11/2026): v3: `+mujeres`, peso 2, sin tamaños de empresa (no consta un coste laboral general, 3.4.2); agrupadas en `temas.json`.
- [x] 122/000025 (cierre de nucleares): `-secInd`, `-empGran`, sin `ciud`. — Aplicada (06/11/2026): `{"ciud": 1, "secInd": -1}` → `{"secInd": -1}`, como la XII (122/000073, 122/000224), nota actualizada.
- [x] 122/000022 (nulidad de la Ley de Amnistía de 1977): `+victimas`. — Resuelta (06/11/2026): v3: `+victimas` (anula sentencias franquistas: reparación, 3.7), igual que la XII (122/000139, 122/000141).
- [x] 130/000001 (RDL 11/2019, DANA): peso 1. — Aplicada (06/11/2026): peso 2 → 1 (3.8, paso 2: ámbito territorial), como las medidas de la DANA de la XV.
- [x] Partido del Grupo Mixto: solo identificado 123/000002 (Compromís); el resto de proposiciones son de grupos con un único partido. — Resuelta (06/11/2026): la única iniciativa del Mixto en la caché de la XIII es 123/000002 (autor «Baldoví Roda, Joan (GMx)»), con partido `Compromís`; el resto son de grupos de un solo partido, de parlamentos autonómicos o ILP.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 88 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 10 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 83–84 % idéntica, parecido medio 0.9, 1 con signo contrario; 69 de 88 idénticas en las tres lecturas.
- 38 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 37 antes, 42 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [x] **Prestación de ingresos mínimos** (120/000002, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`. — Resuelta (06/11/2026): relectura del IMV: `+pobreza`, sin `desSub`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.

### Relectura de las ILP con el texto bien recortado (05/11/2026)

El texto del BOCG en caché de las iniciativas legislativas populares (120/) empezaba en el sumario del boletín y arrastraba iniciativas vecinas (corregido en 33661ff). Las ILP afectadas de esta legislatura se releyeron con el texto correcto por tres lectores independientes y se consolidaron por mayoría. Lecturas en `data/clasificacion/lecturas_ilp_05-11-2026/`.

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 122/000020. Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 122/000013: `{"hipot": 1, "viv0": 1}` → `{"secFin": 1}`.
- 122/000025: `{"ciud": 1, "secInd": -1}` → `{"secInd": -1}`.
- 130/000001: peso 2 → 1.
