# Clasificaciones pendientes de revisión (X legislatura)

Casos dudosos señalados al clasificar la X (2011–2015) con la rúbrica vigente. Para cerrar uno: corrige `clas_*.json` (o confirma que está bien), marca la casilla y, si cambia el criterio, actualiza `RUBRICA.md`.

Ya igualados al integrar: 8 pares de real decreto-ley y su tramitación como proyecto de ley (RDL 8/2012, 24/2012, 25/2012, 4/2013, 11/2013, 4/2014, 11/2014 y 4/2015), con la unión de impactos y el peso mayor.

## 1. Decisiones de criterio

- [x] **Cajas de ahorros convertidas en bancos** (121/000049): regla de lo público (`-ciud`, `+secFin`), aunque las cajas no eran propiedad pública en sentido estricto. — Obsoleta (06/11/2026): la regla de lo público ya no da `ciud` (3.2); v3: `-secFin` (limita tamaño y ámbito de las cajas), sin `ciud`.
- [x] **Seguridad privada** (121/000050): `-ciud`, `+empGran` por privatizar funciones; no hay colectivo de sector exacto. — Obsoleta (06/11/2026): la regla de lo público ya no da `ciud` (3.2); v3: `{}` (los tres lectores no ven signo con el texto), sin `ciud` ni `empGran`.
- [x] **Privatización parcial de AENA** (RDL 8/2014: 130/000055, 121/000104): `-ciud`, `+secTrans`, `+empGran`, peso 3. — Aplicada (06/11/2026): relectura ómnibus con el texto del BOE (tres lecturas, dos rondas): 11 medidas; `+empMicro +empPeq +empMed` → `+ciud +cons +discapacidad +empAut −empGran +hipot +jovenes +proSeg +secCom +secDig −secFin −secInd +secTrans`, peso 2; recupera la Garantía Juvenil. Lecturas en `data/clasificacion/lectura_omnibus_repaso_06-11-2026/`.
- [x] **Aznalcóllar** (130/000053): regla de concesión pública a un privado (`-ciud`, `+secInd`). — Resuelta (06/11/2026): v3: `+secInd`, peso 1, sin `ciud` (3.2 vigente: solo el sector que recibe la concesión).
- [x] **Rescate de peajes** (125/000009): reversión de concesiones (`+ciud`, `-secTrans`) además de `+cons`. — Resuelta (06/11/2026): v3: solo `+cons` (fondo que subvenciona peajes; 2 de 3 lectores no ven reversión de concesiones); sin `ciud`, que 3.2 ya no da.
- [x] **Liberalización del tráfico aéreo de Canarias** (122/000128, CC y NC): solo `+cons`; no se aplica la regla de 3.2. — Obsoleta (06/11/2026): la regla 3.2 ya no da `ciud`; v3: `{}` (gana la aerolínea extranjera y pierde la nacional: signos opuestos), sin `cons`.
- [x] **Registro Civil público** (120/000034): `+ciud` sin sector contrario. — Obsoleta (06/11/2026): `ciud` quitado el 06/11/2026 (3.2); v3: `{}`; los registradores no tienen colectivo de sector.
- [x] **Rescate bancario** (RDL 24/2012: 130/000025, 121/000023): `+secFin`, `-cons`, `-prop1` por las quitas a preferentistas; no se usa `ciud`. — Resuelta (06/11/2026): v3: `{}` en 130/000025 y 121/000023 (tres lectores: exigencias y apoyos de signo mixto, 3.1.1); sin `secFin`, `cons` ni `prop1`; misma clasificación en el RDL y su proyecto.
- [x] **Sanidad: RDL 16/2012** (130/000017): peso 3 y `-ciud` (en la XII su reversión tiene peso 2); `-asal4/5/6` por el copago según renta. — Resuelta (06/11/2026): v3 con `medidas`: peso 2 (la medida más pesada), igual que sus reversiones (XII 122/000002, 125/000011, 125/000023 y XIII 125/000010: `+ciud`, peso 2); `-ciud` e `-inmigrantes` por la condición de asegurado (servicio público universal, 3.2); copago: `-asal3`–`-asal6`, `-pen1`–`-pen3`, `-mayores`, `-pac`. Ojo: la medida del copago aparece dos veces en `medidas`.
- [x] **Consentimiento paterno en el aborto de menores** (122/000195, PP): `-mujeres`, `-jovenes` como restricción de un derecho. — Resuelta (06/11/2026): v3: `-jovenes`, `-discapacidad` (menores y personas con la capacidad modificada), sin `-mujeres`: la restricción solo alcanza a esos grupos.
- [x] **Seguridad ciudadana** (121/000105): `-inmigrantes` por el rechazo en frontera; en otras legislaturas las reformas o derogaciones van vacías. — Aplicada (06/11/2026): 121/000105 `{}` → `{"inmigrantes": -1}` (rechazo en frontera en Ceuta y Melilla, que entró por enmienda en el texto votado; coherente con la XV 122/000298), nota actualizada.
- [x] **Factor de sostenibilidad de las pensiones** (121/000068): además de pensionistas, `-adultos` por las pensiones futuras. — Resuelta (06/11/2026): v3 con `medidas`: factor de sostenibilidad → `-adultos`; índice de revalorización → `-pen1`–`-pen3`, `-mayores` (3.3.2).
- [x] **IVA de la cadena alimentaria al 4 %** (122/000019, BNG): `+ciud`, regla de cargas generales al revés. — Resuelta (06/11/2026): v3: `+ciud`, conforme a 3.2 (IVA de los alimentos: bajada +1).
- [x] **Voto secreto de personas ciegas** (122/000211): `+discapacidad`, aunque las reformas electorales van vacías. — Resuelta (06/11/2026): v3: `+discapacidad`; la ley nombra al colectivo (P1), no es una reforma electoral general.
- [x] **Emigrantes retornados** (122/000120, 122/000127): `+pen1`, `+pen2`, `+mayores`; en la XIV (122/000205) está vacía y en la XII con pensiones. Igualar. — Resuelta (06/11/2026): igualadas: X 122/000120 y 122/000127, XII 122/000206 y 122/000216, XIV 122/000205, todas `+mayores`, peso 1, sin tramos `pen`.

## 2. Pesos discutibles

- [x] Ley de Estabilidad Presupuestaria (121/000003) peso 3 sin impactos; RDL 14/2012 educativo (130/000015) peso 2; Programa de Activación para el Empleo (130/000063) peso 1 aunque es el de creación; fondos de financiación autonómica (130/000022, 130/000064) peso 2 sin impactos; LRSAL (121/000058, `-rural` discutible). — Resuelta (06/11/2026): v3: 121/000003 `{}` peso 1; 130/000015 `-estud`, `-proDoc` peso 2; 130/000063 `+desSub` peso 2; 130/000022 y 130/000064 `{}` peso 1; 121/000058 `{}` peso 1, sin `-rural`.

## 3. Contenido supuesto o desconocido

- [x] Clasificadas por el título, sin comprobar el texto: 122/000018 y 122/000107 (progresividad fiscal: `-asal5/6`, `-prop3/4`, `-empGran`), 122/000040 (FROB, IU: entidades públicas), 122/000077 (vacaciones y baja), 122/000161 (antitabaco, se supone endurecimiento), 122/000187 (carburantes), 122/000193 (abuso de derecho), 122/000203 (publicidad de la amnistía fiscal). — Resuelta (06/11/2026): v3 con el texto del BOCG: 122/000018 `-asal5`, `-asal6` (tramo del 50 % sobre 100.000 €); 122/000107 `-empGran`, `-prop3`, `-prop4`; 122/000040 `+hipot`, `-secFin` (dación en pago); 122/000077 `+asal1`–`+asal4`, `-empAut`, `-empMicro`, `-empPeq`; 122/000161 `+ciud`, `-secInd`; 122/000187 `+cons`; 122/000193 `-empGran`; 122/000203 `{}`.
- [x] Sin impactos por no conocer el sentido: 122/000003 (Inspección de Trabajo), 122/000021 (IVA, CiU), 122/000102 y 122/000117 (aborto, UPN), 122/000116 (sector eléctrico, UPN), 122/000196, 181, 202, 125/000001, 125/000006 (agua de Castilla-La Mancha), 121/000011 y 130/000018 (RDL 17/2012 de medio ambiente), 121/000059 (evaluación ambiental), 121/000074 (desindexación). — Resuelta (06/11/2026): v3 con el texto: 122/000021 `+empAut`, `+empMicro`, `+empPeq` (IVA de caja); 122/000116 `+cons`; 122/000181 `+desSub`; el resto `{}` con el contenido leído (122/000102 y 122/000117: ecografía previa al aborto, signo no determinable; 121/000011 y 130/000018: medidas ambientales de signo mixto; los demás, institucionales).
- [x] Signo mixto, revisar: 130/000001 (RDL 20/2011, subidas de IRPF e IBI frente a la deducción por vivienda y pensiones), 130/000013 (RDL 12/2012, amnistía fiscal `+prop3/4`), 121/000064 (Ley del Sector Eléctrico solo `-secInd`), 130/000060 (Castor), 130/000046 (RDL 16/2013), 121/000106 (mutuas), 121/000069 (Presupuestos 2014). — Aplicada (06/11/2026): relectura ómnibus con el texto del BOE: 130/000013 `{}` → 2 medidas de Sociedades (los cinco tamaños de empresa −), peso 2; 130/000046 `{}` → 3 medidas (`+infancia −empAut +empMicro +empPeq`), peso 1. El resto de la casilla ya estaba resuelto.
- [x] 121/000084 (justicia gratuita de Gallardón, no aprobada): clasificada por su contenido. — Resuelta (06/11/2026): v3: `+victimas`, peso 2, por su contenido (3.8: las proposiciones se pesan por lo que proponen).

## 4. Partido no identificado (Grupo Mixto)

30 de 33 identificadas por la firma del BOCG (`partidos_mixto.json`); 122/000128 se atribuye a CC y NC.

- [x] 122/000033 (Ley de Amnistía de 1977): el PDF extraído no incluye la firma. — Resuelta (06/11/2026): partido `BNG` por la firma del BOCG B_044-01 (ver la nota de más abajo); v3: `{}`.
- [x] 122/000091 y 122/000092 (derecho de autodeterminación): sin BOCG. — Cerrada sin cambios (06/11/2026): partido vacío; sin BOCG ni votaciones, así que no afecta a la nota.

## 5. Datos

- [x] Seis días de votaciones con el zip corrupto en congreso.es (19/12/2013, 29/05/2014, 25/09/2014, 07/07/2015, 29/09/2015, 20/10/2015): omitidos. — Aplicada (06/11/2026): zips con 404; recuperadas 209 votaciones sueltas de las seis fechas (89, 55, 8, 8, 4 y 45).
- [x] Viera Chacón (exPSOE, en el Mixto desde 2015) no se cuenta en ningún partido. — Cerrada sin cambios (06/11/2026): sigue excluido a propósito (`scripts/legislaturas.py`): diputado exPSOE en el Mixto sin partido al que asignarlo.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 510 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: extracto de hasta 5.000 caracteres del texto oficial (BOCG) de cada iniciativa; en los reales decretos-ley, el de su proyecto de ley; las pocas sin texto publicado, solo con el título. 94 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 85–86 % idéntica, parecido medio 0.89, 0 con signo contrario; 403 de 510 idénticas en las tres lecturas.
- 247 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 229 antes, 307 ahora.

- 121/000021: `viv2` → `casero`, como en 93a7102 (colectivo «casero», 04/11/2026). Las lecturas v3 de la X se hicieron con la rúbrica anterior a ese cambio y la aplicación lo había revertido. El resto de `viv2` de la X (130/000001, IBI) sigue siendo `viv2`.

## `desSub` en iniciativas del IMV (rúbrica, 05/11/2026)

La rúbrica (línea de Desempleados) deja `desSub` solo para el subsidio por desempleo: el IMV y las rentas mínimas van a `pobreza` (3.5.2). Estas iniciativas llevan `desSub` y su nota habla del IMV o de una renta mínima; todas tienen ya `pobreza`. Revisar si `desSub` sobra o si la iniciativa toca además el subsidio por desempleo.

- [x] **Prestación de ingresos mínimos** (120/000035, ILP): renta mínima de la Seguridad Social, no subsidio por desempleo; `desSub` y `pobreza`. — Resuelta (06/11/2026): relectura del IMV: `+pobreza`, sin `desSub`.

- 122/000033: partido `BNG` (Grupo Mixto). Evidencia: BOCG B_044-01, «a instancia de don Francisco Jorquera Caselas, Diputado por A Coruña (BNG) y doña M.ª Olaia Fernández Davila […] presentan la siguiente Proposición de Ley del BNG». `identificar_mixto.py` no la encontró porque el PDF extraído trae el expediente con otro número en el acuerdo de la Mesa.

### Reclasificación del IMV y de ingresos mínimos (05/11/2026)

Tras corregir en la rúbrica la definición de `desSub` (solo subsidio por desempleo; el IMV y las rentas mínimas van a `pobreza`, 3.5.2), las iniciativas de esta legislatura que tenían `desSub` y trataban del IMV o de ingresos mínimos se releyeron con el texto oficial del BOCG por tres lectores independientes (C, D y E) y se consolidaron por mayoría. Lecturas y consolidación en `data/clasificacion/lecturas_imv_05-11-2026/`; resultado: `desSub` se retira salvo donde el texto trata del subsidio por desempleo.

### Revisión de «Ciudadanía general» tras la v3 (05/11/2026)

El análisis de la prueba de sesgo vio que la v3 había quitado casi todos los `ciud` en contra de la X (de 16 a favor y 10 en contra a 18 y 1), lo que empujaba a NC a salir primero. Se releyeron con el texto oficial del BOCG, por tres lectores independientes y consolidación por mayoría, las 16 iniciativas que perdieron `ciud` −1, 121/000145 (signo invertido respecto a la v2) y 130/000033 (RDL 3/2013, tasas judiciales). Resultado: 122/000034, 122/000050 y 125/000005 (Costas) recuperan `ciud` −1; 121/000145 se confirma en +1 (la v2 estaba mal); 130/000033 se queda en +1 (2 de 3); el resto sigue sin `ciud`. Cambian 8 iniciativas. Lecturas en `revision_ciud_05-11-2026/`.

### Relectura de las ILP con el texto bien recortado (05/11/2026)

El texto del BOCG en caché de las iniciativas legislativas populares (120/) empezaba en el sumario del boletín y arrastraba iniciativas vecinas (corregido en 33661ff). Las ILP afectadas de esta legislatura se releyeron con el texto correcto por tres lectores independientes y se consolidaron por mayoría. Lecturas en `data/clasificacion/lecturas_ilp_05-11-2026/`.


## Leyes ómnibus: medida a medida, tres lecturas

Clasificadas con la regla «Medidas» de 3.8 por tres lectores independientes (C, D, E) y mayoría 2 de 3 (`scripts/consolidar_medidas.py`; lecturas en `data/clasificacion/lectura_omnibus/`). Textos del BOCG o del BOE. El proyecto de ley que procede de un real decreto-ley lleva sus mismas medidas.

- [x] Criterios discutibles que se repiten entre lectores: congelación salarial pública como −`fun*` (Presupuestos 2012-2015); prórrogas pesadas como bloques nuevos (3.8); peso 1 de los decretos de la DANA por su ámbito territorial; `ciud` o `cons` para la rebaja del impuesto de hidrocarburos; −`casero` en las prórrogas de la suspensión de desahucios pese a la compensación al arrendador. — Aplicada (06/11/2026): congelación salarial → `-fun*` se mantiene; prórroga del Patrimonio en 121/000118: medida peso 1 → 2, como 121/000069 y 121/000163 (bloque prorrogado valorado como nuevo, 3.8). El peso de la ley sigue en 3.

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 120/000034, 122/000037, 122/000047. Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 121/000105: `{}` → `{"inmigrantes": -1}` (rechazo en frontera), peso 1.
- 121/000118: medida «Prórroga del Impuesto sobre el Patrimonio en 2015» peso 1 → 2 (peso de la ley, 3, sin cambio).
- 130/000017: se funden las dos medidas «Copago farmacéutico por renta y para pensionistas» en una (`-asal3`…`-asal6`, `-pen1`…`-pen3`, `-mayores`, `-pac`, `+pobreza`); el `imp` de la ley no cambia.

- Unificación entre legislaturas (06/11/2026): 122/000033, 122/000053 y 122/000142 (excluir los crímenes del franquismo de la amnistía de 1977): `{}` → `{"victimas":1}`, peso 1, como 122/000139 (XII) y 122/000022 (XIII); el texto del BOCG repone el derecho de las víctimas a obtener justicia (3.7).

## `famDisc`: familias con una hija o un hijo con discapacidad (06/11/2026)

Colectivo nuevo (rúbrica 3.6.1). Las 186 leyes candidatas (todas las que llevaban `discapacidad` y las que nombran la discapacidad, la dependencia o la accesibilidad) se leyeron dos veces por separado y una tercera para resolver los desacuerdos (6 de 186). Lecturas en `data/clasificacion/lecturas_famDisc_06-11-2026/`.

- [x] 121/000008, 121/000027, 121/000069, 121/000118, 121/000163 (PGE 2012-2016) y 130/000001 (RDL 20/2011): nueva medida «Subida de la asignación por hijo a cargo con discapacidad» (+`famDisc`, peso 1); cuantías comprobadas en el BOE. 121/000027 no tenía medidas: ahora lleva dos (revalorización de las pensiones, con su clasificación y peso, y la asignación).
- [x] 130/000030 (RDL 29/2012): `famDisc` en la medida de orfandad de huérfanos con discapacidad y en una medida nueva de la asignación; no en la revalorización de las pensiones (peso 3).
- [x] 122/000101 (deudores hipotecarios): +`famDisc`. Comprobado con el texto aprobado (Ley 1/2013, BOE): protege a la «unidad familiar en la que alguno de sus miembros tenga declarada discapacidad superior al 33 por ciento» y eleva para ella el límite de ingresos.
- [x] 122/000195 (consentimiento para el aborto de menores y personas con la capacidad modificada): sin `famDisc`; cambia el papel de la familia sin un signo claro para ella (P4).
