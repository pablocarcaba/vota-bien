# Clasificaciones pendientes de revisión (XII legislatura)

508 iniciativas; unas 220 reutilizan la clasificación de su equivalente en otras legislaturas. Duplicados con título idéntico igualados al integrar. Faltan 3 días de votaciones (10/10/2017, 19/10/2017, 13/11/2018): el Congreso sirve esos zips corruptos.

## 1. Decisiones de criterio

- [x] Coste laboral para pymes: 122/000109 (registro de jornada) lo marca, 122/000107 y 122/000225 (negociación colectiva) no. Unificar. — Resuelta (06/11/2026): la diferencia ya la explica la rúbrica: 122/000109 (registro de jornada, obligación general de todas las empresas, 3.4.2) `+asal1`–`+asal4`, `-empMicro`, `-empPeq`, `-empMed`, `-empGran`, igual que 130/000063; 122/000107 y 122/000225 (negociación colectiva) solo `+asal1`–`+asal4`: no imponen un coste directo (P2); agrupadas en `temas.json`.
- [x] Tasas judiciales: 122/000066, 094 y 250 marcan `+empMicro`/`+empPeq`; la XI (122/000011) quedó vacía. — Resuelta (06/11/2026): la XI ya no está vacía: 122/000011 lleva `+empMicro`, `+empPeq`, igual que 122/000066, 122/000094 y 122/000250 (umbral de «reducida dimensión», 3.4.2).
- [x] Autopistas quebradas a una sociedad estatal (121/000034, 130/000045): regla de lo público (`+ciud`, `-secCons`). — Obsoleta (06/11/2026): la regla de lo público ya no da `ciud` (3.2); v3: 121/000034 y 130/000045 `-secTrans` (obliga a los vehículos pesados a ir por autopistas de peaje), sin `ciud` ni `-secCons`; agrupadas en `temas.json`.
- [x] Liberalización del ferrocarril (121/000043, 130/000050): `-ciud`, `+secTrans`, `+cons`. — Resuelta (06/11/2026): `ciud` quitado el 06/11/2026; `medidas`: apertura a la competencia → `+secTrans` (el ejemplo de 3.2); viajes combinados → `+cons`, `-secCom`.
- [x] Patrimonio Natural del PP (122/000103, 137): identificadas como rebaja de protección (`-ciud`, `+secPrim`), sin confirmar. — Aplicada (06/11/2026): 122/000103 y 122/000137 `{"secPrim": 1}` → `{"ciud": -1, "secPrim": 1}` (rebaja de protección de la biodiversidad, 3.2), nota actualizada.
- [x] Exhumación de Franco (121/000026, 130/000037): vacía. — Resuelta (06/11/2026): v3: 121/000026 y 130/000037 `{}` (memoria sin `ciud`, 3.2; no reconoce derechos a víctimas, 2 de 3 lectores).
- [x] VTC (121/000032, 130/000030, 130/000040): vacías por efectos contrapuestos. — Resuelta (06/11/2026): v3: `{}` en las tres por signos opuestos dentro de `secTrans` (3.1.1).
- [x] Ley 52/2007: unas con peso 1 y otras con 2. — Aplicada (06/11/2026): grupo [122/000157, 122/000159, 125/000010] igualado a peso 2 (122/000159 y 125/000010: 1 → 2).
- [x] Emprendedores de Baleares (125/000002, 125/000019): vacía como en la XI; la XIV marcó `-secCons`. — Resuelta (06/11/2026): v3 con el texto: 125/000002 y 125/000019 `{}` (deporte base y voluntariado deportivo), igual que la XI 125/000002; en la caché de la XIV no hay ninguna iniciativa balear sobre la Ley 14/2013 con la que comparar.
- [x] IVA del 4 % en dependencia (124/000011): la XIV y la XV discrepan. — Resuelta (06/11/2026): igualadas: XII 124/000011, XIV 124/000005 y XV 124/000015, todas `+depend`, `+secSoc`, peso 1.

## 2. Pesos discutibles

- [x] RDL 6/2019 de igualdad (130/000062) con 2; RDL 8/2019 (130/000063) con 3; leyes de autónomos (122/000028, 043) con 2 frente a 3 en la XV; reforma constitucional de la Jefatura del Estado (120/000020) con 1. — Aplicada (06/11/2026): 130/000063 releído como ómnibus con el texto del BOE (tres lecturas, dos rondas): 11 medidas, peso 3 → 2. El resto de la casilla ya estaba resuelto.

## 3. Contenido supuesto o desconocido

- [x] 120/000013, 122/000027, 122/000111/113/118, 122/000166, 122/000308, 122/000317, 130/000003, 130/000017, 125/000023: vacías por no conocer el contenido. — Resuelta (06/11/2026): v3 con el texto: 122/000027 `+ciud`; 122/000118, 122/000166, 122/000308, 122/000317 y 130/000017 `{}` con el contenido leído; 125/000023 `+ciud`, `+inmigrantes`. Siguen `{}` sin contenido (3.9) 120/000013, 122/000111 y 122/000113, porque no tienen texto publicado (inadmitida y retiradas), y 130/000003, porque son ajustes técnicos financieros (FROB, SAREB, Fondo Único de Resolución).
- [x] 122/000059 (matrimonio de personas con discapacidad), 122/000140 (¿crímenes del franquismo?), 122/000172 y 234 (emergencia habitacional, modelo catalán), 122/000194, 122/000256, 122/000270, 122/000285: contenido supuesto. — Aplicada (06/11/2026): 122/000234 `{"inq": 1, "pobreza": 1}` → igual que 122/000172 (`+hipot`, `+inq`, `+pobreza`, `-secFin`, `-casero`), misma nota; agrupadas en `temas.json`.

## 4. Partido no identificado

- [x] 40 proposiciones del Grupo Mixto: 35 identificadas por la firma del BOCG (`partidos_mixto.json`).
- [x] Sin BOCG, deducidas: 122/000181 → PDeCAT (mismo título que 122/000182, firmada por el PDeCAT); 122/000324, 325 y 327 (deuda del Consorcio Valencia 2007) → Compromís. — Cerrada sin cambios (06/11/2026): ninguna tiene votaciones, así que el partido deducido no afecta a la nota.
- [x] 122/000262 (transparencia de la Casa del Rey): sin BOCG; partido sin identificar. — Cerrada sin cambios (06/11/2026): inadmitida, sin BOCG y sin votaciones: no afecta a la nota.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 508 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 56 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 81–85 % idéntica, parecido medio 0.88, 3 con signo contrario; 385 de 508 idénticas en las tres lecturas.
- 223 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 201 antes, 228 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [x] **Prestación de ingresos mínimos** (120/000002, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`. — Resuelta (06/11/2026): relectura del IMV: `+pobreza`, sin `desSub`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.

### Relectura de las ILP con el texto bien recortado (05/11/2026)

El texto del BOCG en caché de las iniciativas legislativas populares (120/) empezaba en el sumario del boletín y arrastraba iniciativas vecinas (corregido en 33661ff). Las ILP afectadas de esta legislatura se releyeron con el texto correcto por tres lectores independientes y se consolidaron por mayoría. Lecturas en `data/clasificacion/lecturas_ilp_05-11-2026/`.


## Leyes ómnibus: medida a medida, tres lecturas

Clasificadas con la regla «Medidas» de 3.8 por tres lectores independientes (C, D, E) y mayoría 2 de 3 (`scripts/consolidar_medidas.py`; lecturas en `data/clasificacion/lectura_omnibus/`). Textos del BOCG o del BOE. El proyecto de ley que procede de un real decreto-ley lleva sus mismas medidas.

- [x] Criterios discutibles que se repiten entre lectores: congelación salarial pública como −`fun*` (Presupuestos 2012-2015); prórrogas pesadas como bloques nuevos (3.8); peso 1 de los decretos de la DANA por su ámbito territorial; `ciud` o `cons` para la rebaja del impuesto de hidrocarburos; −`casero` en las prórrogas de la suspensión de desahucios pese a la compensación al arrendador. — Aplicada (06/11/2026): 121/000020: medida «Prórroga del Impuesto sobre el Patrimonio en 2018» peso 1 → 2, como la X y la XV (3.8); `-casero` en 130/000048 se mantiene.

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 121/000043, 122/000083, 122/000177, 122/000176, 122/000236, 130/000050. Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 122/000103: `{"secPrim": 1}` → `{"ciud": -1, "secPrim": 1}`.
- 122/000137: `{"secPrim": 1}` → `{"ciud": -1, "secPrim": 1}`.
- 122/000159: peso 1 → 2 (grupo de la Ley 52/2007).
- 125/000010: peso 1 → 2 (grupo de la Ley 52/2007).
- 122/000234: `{"inq": 1, "pobreza": 1}` → `{"hipot": 1, "inq": 1, "pobreza": 1, "secFin": -1, "casero": -1}`; nuevo grupo [122/000172, 122/000234] en `temas.json`.
- 121/000020: medida «Prórroga del Impuesto sobre el Patrimonio en 2018» peso 1 → 2 (peso de la ley, 3, sin cambio).
