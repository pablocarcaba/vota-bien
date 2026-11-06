# Clasificaciones pendientes de revisión (XIV legislatura)

Casos dudosos señalados al clasificar la XIV con la rúbrica vigente (con peso y la regla de lo público frente a lo privado). Para cerrar uno: corrige `clas_*.json` (o confirma que está bien), marca la casilla y, si cambia el criterio, actualiza `RUBRICA.md`.

Ya igualados al integrar: voto a los 16 (`+jovenes`, como en la XV), deslocalizaciones, cajeros en zonas rurales, copago de MUFACE/ISFAS, Ley de Minas e integración de centros privados en la red pública.

## 1. Decisiones de criterio

- [x] **Sareb** (130/000073, 121/000090, RDL 1/2022): regla de lo público (`+ciud`, `-secFin`), aunque para la banca supone más un alivio que una pérdida. — Obsoleta (06/11/2026): regla de lo público retirada (3.2); v3: 130/000073 y 121/000090 solo `+secCom` (horarios comerciales), sin `ciud` ni `secFin`.
- [x] **Permiso retribuido recuperable** (130/000011, 121/000012): `+ciud` por salud pública y `-empAut/empMicro/empPeq`; sin efecto marcado para asalariados. — Aplicada (06/11/2026): 121/000012 `{}` → `{"ciud":1}` peso 2, igual que 130/000011 (salud pública, 3.2); las dos agrupadas en `temas.json`.
- [x] **Excepción ibérica** (130/000082, 130/000095): `-secInd` por los menores ingresos de las eléctricas. — Resuelta (06/11/2026): v3: 130/000082 y 130/000095 solo `+cons`, sin `-secInd`.
- [x] **IVA cero de alimentos** (130/000092, 121/000140, RDL 20/2022): `+ciud` aplicando al revés la regla de cargas generales (bajada de un impuesto que paga todo el mundo). — Resuelta (06/11/2026): la rúbrica 3.2 recoge ya la bajada del IVA de los alimentos como `+ciud`; v3: medida «IVA del 0 % y 5 % en alimentos básicos» `{"ciud":1}` en 130/000092 y 121/000140 (agrupadas en `temas.json`).
- [x] **Complemento de brecha de género** (130/000043, 121/000049): solo `+mujeres`; también lo cobran algunos hombres y baja la cuantía para algunas madres de 3 o más hijos. — Resuelta (06/11/2026): v3: medida del complemento `{"mujeres":1,"hombres":1}` en 130/000043 y 121/000049; `hij3` sin marcar (signo no único).
- [x] **Aborto** (121/000122): `+ciud` y `-secSoc` por garantizar la prestación en la sanidad pública; choca con no usar `ciud` en leyes de derechos discutidas. — Resuelta (06/11/2026): v3: 121/000122 solo `+mujeres`, sin `ciud` ni `secSoc`.
- [x] **LOMLOE** (121/000007): solo `+ciud` y `-secSoc` por la regla de lo público. — Obsoleta (06/11/2026): regla de lo público retirada (3.2); v3: 121/000007 solo `+estud`, peso 3, sin `ciud` ni `secSoc`.
- [x] **Soberanía energética de VOX** (122/000251, 122/000279, 122/000312): `+secInd` y `-ciud` por revertir protección ambiental. — Resuelta (06/11/2026): v3: las tres `{"ciud":-1,"secInd":1}`, peso 2, conforme a 3.2 (rebaja de protección climática: −`ciud`, +sector); agrupadas en `temas.json`.
- [x] **Memoria histórica**: 122/000012 (VOX, derogación) `-victimas` frente a 121/000064 `+victimas`. — Resuelta (06/11/2026): v3: 122/000012 `-victimas` y 121/000064 `+victimas`, simétricas (3.7: reconoce o retira derechos de reparación).
- [x] **Reforma laboral y despidos covid** (130/000072, 121/000011, 130/000010, 121/000008, 130/000005): `-empAut/empMicro/empPeq` por coste laboral; no se marcan medianas y grandes. — Resuelta (06/11/2026): v3: las cinco `+asal1..asal4`, sin ningún `emp*` (no es coste laboral general de la tabla 3.4.2); desaparece la duda sobre medianas y grandes.
- [x] **Gravamen a banca, energéticas y grandes fortunas** (122/000247): incluye `-asal6` por el IRPF del ahorro. — Resuelta (06/11/2026): v3: 122/000247 `{"empGran":-1,"secFin":-1,"secInd":-1}` con dos medidas (gravamen energético y bancario), sin `asal6`.
- [x] **Pesos discutibles**: cotización de autónomos por ingresos reales (130/000085, 121/000119) con 2; Ley de cambio climático (121/000019) con 2; amnistía (122/000132) con 2; Fondo COVID de 16.000 M€ a las comunidades (130/000023) con 1. — Resuelta (06/11/2026): v3: 130/000085 y 121/000119 `{}` peso 1 (signos opuestos); 121/000019 `+ciud` peso 2 (paso 3 de 3.8); 122/000132 `{}` peso 1; 130/000023 `{}` peso 1 (con `imp: {}` el peso es 1).

## 2. Huecos de la rúbrica (no hay colectivo)

- [x] **Emigrantes retornados** (122/000205, doble imposición): vacía. — Resuelta (06/11/2026): v3: 122/000205 `{"mayores":1}` peso 1; ya no está vacía.
- [x] **Profesionales de la justicia** (122/000046, conciliación): vacía. — Resuelta (06/11/2026): v3: 122/000046 `{"hombres":1,"mujeres":1}` peso 1 (permiso ligado a una situación, 3.3.1 y 3.7); ya no está vacía.
- [x] **Mecenazgo y donantes** (122/000032, 122/000117, 122/000136, 122/000137): vacías. — Resuelta (06/11/2026): la rúbrica v3 no crea colectivo; las cuatro siguen `{}` peso 1, coherente con 3.1.1 (ningún colectivo pasa la prueba de efecto).
- [x] **Beneficios fiscales territoriales** (Canarias, ZEC, Baleares: 125/000018, 130/000071): vacías. — Resuelta (06/11/2026): v3: 125/000018 `{"secCom":1}` (comercio mayorista en la ZEC) y 130/000071 `{}` peso 1; sin colectivo territorial en la rúbrica, coherente con 3.7 (`rural` solo para medio rural).

## 3. Contenido supuesto o desconocido

Revisado con el texto del BOCG/BOE (49 iniciativas, 21 cambios; gemelas 122/000303 y 122/000093 igualadas a 304 y 094). Siguen sin texto comprobable: 122/000023, 122/000135, 120/000005, 006, 008, 011, 014, 016, 025, 122/000329, 122/000332 y 124/000006.

- [x] 121/000060: paquete covid sin RDL identificado con seguridad; clasificado como genérico con peso 3. — Resuelta (06/11/2026): v3: `{}` peso 1 (3.9: contenido no determinado; ya no se clasifica como genérico de peso 3).
- [x] 121/000077 (ley ferroviaria): ¿amplía la liberalización? Si es así, `-ciud` y `+secTrans`. — Resuelta (06/11/2026): v3: `{"secTrans":1}` peso 2, la nota confirma que profundiza la liberalización; sin `ciud` por la decisión del 06/11/2026 (3.2).
- [x] 130/000065 (RDL 25/2021) y 130/000081 (RDL 9/2022): contenido no claro; vacías. — Aplicada (06/11/2026): leído el texto del BOE local. 130/000065 `{}` → `{"victimas":1}` peso 1 (no tributación de las ayudas por la erupción de La Palma; el resto son créditos presupuestarios y un ajuste técnico bancario). 130/000081 sigue `{}` peso 1, ahora con contenido conocido (anotación registral de bienes de testaferros de sancionados y pagos de los servicios en el exterior: sin colectivo).
- [x] 122/000206 y 122/000216 (Ley de Minas, UP): se supone endurecimiento ambiental. — Resuelta (06/11/2026): v3 leyó el texto: las dos `{"ciud":1,"secInd":-1}` peso 2 (endurecen exigencias ambientales a la minería, 3.2).
- [x] 122/000292 (cierre de los CIE, autor VOX según los datos): autor y contenido parecen incoherentes; comprobar. — Aplicada (06/11/2026): comprobado en el BOCG local (B-316-1): el autor es VOX y el texto endurece el internamiento y limita el uso de la solicitud de asilo; la «clausura definitiva» del título no cambia el sentido. Se mantiene `{"inmigrantes":-1}` peso 1, sin cambios.
- [x] 122/000300 (régimen de los CIE, VOX), 122/000303 y 122/000304 (ley de emprendedores), 122/000172 (crédito inmobiliario), 122/000135 (presupuestos 2021, PP): vacías por no conocer el sentido. — Resuelta (06/11/2026): v3 con texto: 122/000300 `{"inmigrantes":-1}`; 122/000303 y 122/000304 `{"inmigrantes":-1}` (suprimen la residencia por compra de inmuebles, agrupadas en `temas.json`); 122/000172 `{}` con contenido conocido (secciones de crédito de cooperativas); 122/000135 `{}` (sin texto, 3.9).
- [x] 125/000006 (AP-9 a Galicia): tratada como traspaso; si suprime peajes o revierte la concesión, aplicar la regla de lo público. — Obsoleta (06/11/2026): regla de lo público retirada (3.2) y es un traspaso entre administraciones; v3: `{}` peso 1.
- [x] 125/000019 (arrendamientos urbanos de Baleares): podría restringir el alquiler turístico (`+inq`, `-viv2`). — Resuelta (06/11/2026): v3: `{"inq":1,"casero":-1}` peso 2 (habilita a las comunidades a contener rentas; `casero` en lugar de `viv2`, 3.5).
- [x] Varias proposiciones con títulos genéricos (Código Penal, Ley 40/2015, Universidades, Haciendas Locales, EBEP: 122/000023, 025, 041, 063, 089, 096, 038, 055, 040, 056, 093, 094; iniciativas populares 120/000006, 011, 014, 025): vacías por no conocer el contenido. — Resuelta (06/11/2026): v3: todas `{}` peso 1; las que tienen texto se clasifican por contenido (penales u organizativas, 3.7 y 3.1.1: 122/000025, 041, 063, 089, 038, 055, 040, 056, 094) y las que siguen sin texto (122/000023, 093, ILP 120/000006, 011, 014, 025) quedan `{}` conforme a 3.9.
- [ ] 13 iniciativas sin autor en la ficha del Congreso (entre ellas 122/000166 y 122/000221) aparecen como «Otros». — Sigue abierta (06/11/2026): el autor sale en el texto del BOCG local de 10 de ellas (122/000039 Plural, Bildu, PSOE, ERC y UP; 090, 109, 122, 247 y 271 PSOE y UP; 133 ERC y Plural; 166 UP, ERC, Plural, Bildu y Mixto; 189 PP, Cs y Mixto; 221 ERC y Bildu), pero el autor se lee de `data/fuente/congreso_xiv.json`, que no es un fichero de clasificación: hay que completarlo allí o en el script de descarga. 122/000132, 123/000002 y 123/000004: requiere BOCG, sin red.

## 4. Partido no identificado (grupos Plural y Mixto)

- [ ] 122/000057, 084, 099, 100, 112, 170, 185, 187, 188, 229: el texto del BOCG no indica el partido. Varias son iniciativas conjuntas de varios partidos del Plural (actos del Rey, registro patrimonial…). — Sigue abierta (06/11/2026): requiere BOCG, sin red: las diez se inadmitieron o se retiraron sin publicarse en el BOCG, y la caché local no tiene su texto ni la ficha da los firmantes.
- [x] 122/000096 y 122/000204: atribuidas a todos los partidos firmantes. — Resuelta (06/11/2026): `partido` «Junts, Compromís, BNG, CUP» y «Junts, Más País, Compromís, BNG, CC»; el validador y `build_data.py` admiten varios partidos separados por coma.

## 5. Dudas nuevas tras leer el texto

- [x] **Prisión permanente revisable** (122/000005, suprimirla): vacía; por simetría con la XV (ampliarla → `+victimas`) tocaría `-victimas`. — Resuelta (06/11/2026): v3: 122/000005 `{}` y en la XV 122/000226 (ampliarla) también `{}`: simétricas como normas penales (3.7).
- [x] **Atentado contra la autoridad** (122/000089, derogarlo): sin `-proSeg`, aunque endurecerlo (122/000163) lleva `+proSeg`. — Resuelta (06/11/2026): v3: 122/000089 y 122/000163 las dos `{}` peso 1 (normas penales, 3.7); ya no hay `+proSeg`.
- [x] **Lo público sin sector claro**: 125/000014 (prórroga de concesiones de costas) solo `-ciud`; 122/000263 (rescate de concesiones) usa `-empGran`. — Obsoleta (06/11/2026): regla de lo público retirada (3.2); v3: 125/000014 `{"ciud":-1}` por rebaja de protección ambiental (exime de la ley de cambio climático), no por la regla de lo público; 122/000263 `{}` sin `empGran`.
- [x] **Rebajas** (125/000008): restringe al comercio, la defiende el pequeño comercio; vacía. — Resuelta (06/11/2026): v3: 125/000008 `{}` peso 1 por signo no conocido (P4).
- [x] **122/000315** (VOX, repartidores y planes de igualdad): `-asal1` en espejo de la ley rider. — Aplicada (06/11/2026): `{"mujeres":-1}` → `{"mujeres":-1,"secDig":1}` peso 2, espejo de la ley rider (121/000059 y 130/000049, `-secDig`); nota actualizada.
- [x] **Pesos**: 122/000292 y 122/000300 (CIE) y 122/000089 suben a 2. — Resuelta (06/11/2026): v3: 122/000292 y 122/000300 peso 1 (uno o pocos artículos, 3.8 paso 2) y 122/000089 peso 1 (`imp: {}`).


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 662 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley. 95 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 81–82 % idéntica, parecido medio 0.88, 0 con signo contrario; 488 de 662 idénticas en las tres lecturas.
- 340 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 256 antes, 297 ahora.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [x] **Creación del IMV** (121/000025, 130/000021): `desSub` y `pobreza`. — Resuelta (06/11/2026): v3: 121/000025 y 130/000021 `{"pobreza":1}`, sin `desSub`.
- [x] **Mejora del IMV junto a complemento de brecha y moratorias** (121/000049, 130/000043): `desSub` y `pobreza`. — Resuelta (06/11/2026): v3: 121/000049 y 130/000043 sin `desSub`; medida del IMV `{"pobreza":1,"victimas":1}`.
- [x] **IMV y rentas mínimas exentas de IRPF** (121/000042, 130/000039): `desSub` y `pobreza`. — Resuelta (06/11/2026): v3: 121/000042 y 130/000039 `{"pobreza":1,"secFin":1}`, sin `desSub`.
- [x] **Prestación de ingresos mínimos** (120/000002, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`. — Resuelta (06/11/2026): v3: 120/000002 `{"pobreza":1}`, sin `desSub`.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.

### Relectura de las ILP con el texto bien recortado (05/11/2026)

El texto del BOCG en caché de las iniciativas legislativas populares (120/) empezaba en el sumario del boletín y arrastraba iniciativas vecinas (corregido en 33661ff). Las ILP afectadas de esta legislatura se releyeron con el texto correcto por tres lectores independientes y se consolidaron por mayoría. Lecturas en `data/clasificacion/lecturas_ilp_05-11-2026/`.


## Leyes ómnibus: medida a medida, tres lecturas

Clasificadas con la regla «Medidas» de 3.8 por tres lectores independientes (C, D, E) y mayoría 2 de 3 (`scripts/consolidar_medidas.py`; lecturas en `data/clasificacion/lectura_omnibus/`). Textos del BOCG o del BOE. El proyecto de ley que procede de un real decreto-ley lleva sus mismas medidas.

- [x] Criterios discutibles que se repiten entre lectores: congelación salarial pública como −`fun*` (Presupuestos 2012-2015); prórrogas pesadas como bloques nuevos (3.8); peso 1 de los decretos de la DANA por su ámbito territorial; `ciud` o `cons` para la rebaja del impuesto de hidrocarburos; −`casero` en las prórrogas de la suspensión de desahucios pese a la compensación al arrendador. — Aplicada (06/11/2026): en la XIV no quedaba nada que cambiar; en la XV, 121/000091, 130/000038 y 130/000049 pasan la medida de hidrocarburos de `ciud` a `cons` (criterio común, 3.5.1).
- [x] **RDL 6/2022 (130/000079)** y otros con preámbulo de más de 150.000 caracteres (RDL 20/2011, 16/2012, 8/2023, 9/2024 de la XV): la caché del BOE se corta en 150.000; puede faltar algún bloque del final. — Aplicada (06/11/2026): el texto del BOE local de 130/000079 sí está cortado a 150.000 caracteres (acaba en la exposición de motivos, en la disposición final 37.ª). El BOCG local del proyecto de ley 121/000100 (A-100-1) trae el texto completo: lo que falta es la DF 38.ª (sequía, ya expuesta antes) y las DF 39.ª a 43.ª (rango, títulos competenciales, habilitación, transposición y entrada en vigor), sin bloques nuevos. Las demás normas citadas (RDL 20/2011, 16/2012, 8/2023, 9/2024) son de otras legislaturas.
- [x] **122/000321** (donación de órganos): un lector propone `{"pac":1}`, peso 1, en vez de los cinco `emp*`: la reducción del 75 % de cuotas para mayores de 62 ya existía (art. 144.4 LGSS) y la proposición solo añade la donación de órganos. Pendiente de tres lecturas. — Aplicada (06/11/2026): comprobado en la caché local: la reducción del 75 % para mayores de 62 ya la introdujo la reforma de pensiones (proyecto 121/000066); la proposición solo reescribe el art. 144.4 para incluir la nueva incapacidad temporal de donantes. `{"empMicro":1,"empPeq":1,"empMed":1,"empGran":1}` peso 2 → `{}` peso 1, igual que 122/000308 (mismo contenido).

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 121/000077, 121/000110, 122/000155, 122/000173, 122/000218, 122/000264. Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 121/000012: `{}` peso 2 → `{"ciud":1}` peso 2 (igual que su RDL 130/000011; grupo nuevo en `temas.json`).
- 130/000073: `{"secCom":1}` peso 2 → peso 1 (igual que 121/000090, mismo grupo de `temas.json`; la medida de horarios es una prórroga).
- 130/000065: `{}` → `{"victimas":1}` peso 1 (texto del BOE).
- 130/000081: `{}` peso 1 sin cambios; nota con el contenido del BOE.
- 122/000315: `{"mujeres":-1}` → `{"mujeres":-1,"secDig":1}` peso 2.
- 122/000321: `{"empMicro":1,"empPeq":1,"empMed":1,"empGran":1}` peso 2 → `{}` peso 1.
- [x] 130/000079 y 121/000100 (RDL 6/2022): entre sus 17 medidas falta la bonificación extraordinaria del precio de los carburantes, que el texto recoge (`cons`, como en su prórroga 130/000083 y 121/000115). No cambia el `imp` total (ya lleva `+cons`); falta añadir la medida. — Aplicada (06/11/2026): añadida la medida «Bonificación del precio de los carburantes» `{"cons":1}` peso 2 en las dos (18 medidas). El `imp` de la ley sigue siendo la unión sin signos opuestos y no cambia; peso de la ley 2, el de su medida más pesada.
