# Clasificaciones pendientes de revisión (Parlamento Europeo, 10.ª legislatura)

Clasificación inicial de 260 procedimientos legislativos (agentes, rúbrica vigente). Los colectivos se aplican al efecto previsible en España. Contenido de 2025-2026 a menudo deducido del título: conviene comprobarlo con el texto (EUR-Lex / OEIL).

## 1. Criterios aplicados

- [x] Rebajas de exigencias ambientales o sanitarias (Ómnibus de sostenibilidad 2025/0044 y 0045, CO2 de coches 2025/0070, lobo 2025/0058, condicionalidad de la PAC 2025/0236, deforestación 2024/0249 y 2025/0329, camiones 2025/0423, químicos 2025/0531, metano 2026/0325) → `-ciud` y `+sector` (nueva regla en la rúbrica 3.2). — Corregida (06/11/2026): con la v3 solo llevan `-ciud` y `+sector` 2025/0070, 2025/0058, 2024/0249 y 2026/0325. 2025/0044 lleva `+empGran` y 2025/0045 `+empGran`, `+empMed` (obligaciones de información y diligencia debida, sin `ciud`); 2025/0236 y 2025/0329, solo `+secPrim`; 2025/0423 y 2025/0531, `{}`.

## 2. Dudas

- [x] Euro digital (2023/0212): `+cons`, `-secFin`; ¿regla de lo público frente a lo privado (`+ciud`)? — Obsoleta (06/11/2026): depende de la regla público/privado, que 3.2 ya no aplica a `ciud`; v3: `{}`.
- [x] Derechos de los pasajeros aéreos (2013/0072) y coordinación de la seguridad social (2016/0397): vacías por signo incierto. — Aplicada (06/11/2026): 2013/0072 se queda en `{}` p1 (sin red no se puede comprobar en OEIL qué texto se votó); nota reescrita para describir el efecto. 2016/0397 sin cambios.
- [x] Aranceles con EE. UU. (2025/0012, 0260, 0261) y productos ucranianos (2025/0056): vacías; ¿`-secPrim`? — Resuelta (06/11/2026): v3: 2025/0012, 0260, 0261 y 2025/0056 `{}`; sin `-secPrim` porque 3.4.1 no marca a los competidores (igual que Ucrania en la 9.ª).
- [x] Presupuestos de la UE 2025-2027: unos vacíos y otros con `+secPrim`/`rural`/`estud`; unificar criterio. — Resuelta (06/11/2026): v3: todos los presupuestos anuales (BUD) `{}`; solo llevan colectivos los fondos de catástrofes (`+victimas`, 3.7) y el FEAG de Galicia 2026/0195 (`+desPres`).
- [x] Marco financiero 2028-2034 (2025/0571R) y RESTORE/Feader por la DANA (2024/0274, 0275), Fondo de Solidaridad DANA (2025/0318): pesos y efecto en España por comprobar. — Resuelta (06/11/2026): v3: 2025/0571R `{}` peso 1; 2024/0274 `+secPrim`, `+victimas`; 2024/0275 y 2025/0318 `+victimas`; todas peso 1 (3.7).
- [x] Reglamento de retorno (2025/0059): peso 2 o 3. — Resuelta (06/11/2026): v3: `-inmigrantes`, peso 2 (no está en la lista de peso 3 de 3.8).
- [x] ITV (2025/0097): contenido de la propuesta, no del texto final. — Resuelta (06/11/2026): v3: `{}`, peso 1 (3.9); ya no se clasifica por el contenido de la propuesta.
- [x] Nuevas técnicas genómicas (2023/0226), IVA digital (2022/0407), perros y gatos (2023/0447): signos discutibles. — Resuelta (06/11/2026): v3: 2023/0226 y 2022/0407 `{}` (P4); 2023/0447 `-secCom`, peso 2 (exigencias a criadores y vendedores, 3.2 bienestar animal).
- [x] Informes de iniciativa legislativa laborales (INL): `+asal1-4` aunque solo piden una directiva. — Resuelta (06/11/2026): v3: 2025/2080 y 2026/2023 `asal1-4`, peso 2: derechos laborales generales (3.3.1), clasificados por lo que proponen (3.8), igual que la 9.ª (2019/2181).


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 260 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título y contenido conocido de cada norma; para las que quedaron sin efectos, segunda lectura con el texto aprobado oficial del Parlamento Europeo (hasta 12.000 caracteres). 83 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 93–95 % idéntica, parecido medio 0.94, 0 con signo contrario; 235 de 260 idénticas en las tres lecturas.
- 67 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 174 antes, 202 ahora.

## Aplicación del repaso (06/11/2026)

- 2013/0072(COD): `{}` p1 → `{}` p1 (solo nota)
- 2025/0726(COD): `{"secInd": 1}` p2 → `{}` p1 (3.4.1: medida comercial, no se marca al sector protegido; criterio común con Ucrania y EE. UU.)

## `famDisc`: familias con una hija o un hijo con discapacidad (06/11/2026)

Colectivo nuevo (rúbrica 3.6.1). Las 186 leyes candidatas (todas las que llevaban `discapacidad` y las que nombran la discapacidad, la dependencia o la accesibilidad) se leyeron dos veces por separado y una tercera para resolver los desacuerdos (6 de 186). Lecturas en `data/clasificacion/lecturas_famDisc_06-11-2026/`.

- [x] 2023/0437(COD) (derechos de los pasajeros): +`famDisc`. Comprobado con el resumen del texto aprobado (T10-0347/2026): si la aerolínea exige acompañante, este viaja gratis y sentado al lado; además, información de accesibilidad en formato accesible y protección de sillas de ruedas y perros de asistencia.
