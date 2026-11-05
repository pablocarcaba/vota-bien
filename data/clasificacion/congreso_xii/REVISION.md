# Clasificaciones pendientes de revisión (XII legislatura)

508 iniciativas; unas 220 reutilizan la clasificación de su equivalente en otras legislaturas. Duplicados con título idéntico igualados al integrar. Faltan 3 días de votaciones (10/10/2017, 19/10/2017, 13/11/2018): el Congreso sirve esos zips corruptos.

## 1. Decisiones de criterio

- [ ] Coste laboral para pymes: 122/000109 (registro de jornada) lo marca, 122/000107 y 122/000225 (negociación colectiva) no. Unificar.
- [ ] Tasas judiciales: 122/000066, 094 y 250 marcan `+empMicro`/`+empPeq`; la XI (122/000011) quedó vacía.
- [ ] Autopistas quebradas a una sociedad estatal (121/000034, 130/000045): regla de lo público (`+ciud`, `-secCons`).
- [ ] Liberalización del ferrocarril (121/000043, 130/000050): `-ciud`, `+secTrans`, `+cons`.
- [ ] Patrimonio Natural del PP (122/000103, 137): identificadas como rebaja de protección (`-ciud`, `+secPrim`), sin confirmar.
- [ ] Exhumación de Franco (121/000026, 130/000037): vacía.
- [ ] VTC (121/000032, 130/000030, 130/000040): vacías por efectos contrapuestos.
- [ ] Ley 52/2007: unas con peso 1 y otras con 2.
- [ ] Emprendedores de Baleares (125/000002, 125/000019): vacía como en la XI; la XIV marcó `-secCons`.
- [ ] IVA del 4 % en dependencia (124/000011): la XIV y la XV discrepan.

## 2. Pesos discutibles

- [ ] RDL 6/2019 de igualdad (130/000062) con 2; RDL 8/2019 (130/000063) con 3; leyes de autónomos (122/000028, 043) con 2 frente a 3 en la XV; reforma constitucional de la Jefatura del Estado (120/000020) con 1.

## 3. Contenido supuesto o desconocido

- [ ] 120/000013, 122/000027, 122/000111/113/118, 122/000166, 122/000308, 122/000317, 130/000003, 130/000017, 125/000023: vacías por no conocer el contenido.
- [ ] 122/000059 (matrimonio de personas con discapacidad), 122/000140 (¿crímenes del franquismo?), 122/000172 y 234 (emergencia habitacional, modelo catalán), 122/000194, 122/000256, 122/000270, 122/000285: contenido supuesto.

## 4. Partido no identificado

- [x] 40 proposiciones del Grupo Mixto: 35 identificadas por la firma del BOCG (`partidos_mixto.json`).
- [ ] Sin BOCG, deducidas: 122/000181 → PDeCAT (mismo título que 122/000182, firmada por el PDeCAT); 122/000324, 325 y 327 (deuda del Consorcio Valencia 2007) → Compromís.
- [ ] 122/000262 (transparencia de la Casa del Rey): sin BOCG; partido sin identificar.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 508 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 56 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 81–85 % idéntica, parecido medio 0.88, 3 con signo contrario; 385 de 508 idénticas en las tres lecturas.
- 223 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 201 antes, 228 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [ ] **Prestación de ingresos mínimos** (120/000002, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.
