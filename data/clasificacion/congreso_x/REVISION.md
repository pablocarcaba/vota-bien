# Clasificaciones pendientes de revisión (X legislatura)

Casos dudosos señalados al clasificar la X (2011–2015) con la rúbrica vigente. Para cerrar uno: corrige `clas_*.json` (o confirma que está bien), marca la casilla y, si cambia el criterio, actualiza `RUBRICA.md`.

Ya igualados al integrar: 8 pares de real decreto-ley y su tramitación como proyecto de ley (RDL 8/2012, 24/2012, 25/2012, 4/2013, 11/2013, 4/2014, 11/2014 y 4/2015), con la unión de impactos y el peso mayor.

## 1. Decisiones de criterio

- [ ] **Cajas de ahorros convertidas en bancos** (121/000049): regla de lo público (`-ciud`, `+secFin`), aunque las cajas no eran propiedad pública en sentido estricto.
- [ ] **Seguridad privada** (121/000050): `-ciud`, `+empGran` por privatizar funciones; no hay colectivo de sector exacto.
- [ ] **Privatización parcial de AENA** (RDL 8/2014: 130/000055, 121/000104): `-ciud`, `+secTrans`, `+empGran`, peso 3.
- [ ] **Aznalcóllar** (130/000053): regla de concesión pública a un privado (`-ciud`, `+secInd`).
- [ ] **Rescate de peajes** (125/000009): reversión de concesiones (`+ciud`, `-secTrans`) además de `+cons`.
- [ ] **Liberalización del tráfico aéreo de Canarias** (122/000128, CC y NC): solo `+cons`; no se aplica la regla de 3.2.
- [ ] **Registro Civil público** (120/000034): `+ciud` sin sector contrario.
- [ ] **Rescate bancario** (RDL 24/2012: 130/000025, 121/000023): `+secFin`, `-cons`, `-prop1` por las quitas a preferentistas; no se usa `ciud`.
- [ ] **Sanidad: RDL 16/2012** (130/000017): peso 3 y `-ciud` (en la XII su reversión tiene peso 2); `-asal4/5/6` por el copago según renta.
- [ ] **Consentimiento paterno en el aborto de menores** (122/000195, PP): `-mujeres`, `-jovenes` como restricción de un derecho.
- [ ] **Seguridad ciudadana** (121/000105): `-inmigrantes` por el rechazo en frontera; en otras legislaturas las reformas o derogaciones van vacías.
- [ ] **Factor de sostenibilidad de las pensiones** (121/000068): además de pensionistas, `-adultos` por las pensiones futuras.
- [ ] **IVA de la cadena alimentaria al 4 %** (122/000019, BNG): `+ciud`, regla de cargas generales al revés.
- [ ] **Voto secreto de personas ciegas** (122/000211): `+discapacidad`, aunque las reformas electorales van vacías.
- [ ] **Emigrantes retornados** (122/000120, 122/000127): `+pen1`, `+pen2`, `+mayores`; en la XIV (122/000205) está vacía y en la XII con pensiones. Igualar.

## 2. Pesos discutibles

- [ ] Ley de Estabilidad Presupuestaria (121/000003) peso 3 sin impactos; RDL 14/2012 educativo (130/000015) peso 2; Programa de Activación para el Empleo (130/000063) peso 1 aunque es el de creación; fondos de financiación autonómica (130/000022, 130/000064) peso 2 sin impactos; LRSAL (121/000058, `-rural` discutible).

## 3. Contenido supuesto o desconocido

- [ ] Clasificadas por el título, sin comprobar el texto: 122/000018 y 122/000107 (progresividad fiscal: `-asal5/6`, `-prop3/4`, `-empGran`), 122/000040 (FROB, IU: entidades públicas), 122/000077 (vacaciones y baja), 122/000161 (antitabaco, se supone endurecimiento), 122/000187 (carburantes), 122/000193 (abuso de derecho), 122/000203 (publicidad de la amnistía fiscal).
- [ ] Sin impactos por no conocer el sentido: 122/000003 (Inspección de Trabajo), 122/000021 (IVA, CiU), 122/000102 y 122/000117 (aborto, UPN), 122/000116 (sector eléctrico, UPN), 122/000196, 181, 202, 125/000001, 125/000006 (agua de Castilla-La Mancha), 121/000011 y 130/000018 (RDL 17/2012 de medio ambiente), 121/000059 (evaluación ambiental), 121/000074 (desindexación).
- [ ] Signo mixto, revisar: 130/000001 (RDL 20/2011, subidas de IRPF e IBI frente a la deducción por vivienda y pensiones), 130/000013 (RDL 12/2012, amnistía fiscal `+prop3/4`), 121/000064 (Ley del Sector Eléctrico solo `-secInd`), 130/000060 (Castor), 130/000046 (RDL 16/2013), 121/000106 (mutuas), 121/000069 (Presupuestos 2014).
- [ ] 121/000084 (justicia gratuita de Gallardón, no aprobada): clasificada por su contenido.

## 4. Partido no identificado (Grupo Mixto)

30 de 33 identificadas por la firma del BOCG (`partidos_mixto.json`); 122/000128 se atribuye a CC y NC.

- [ ] 122/000033 (Ley de Amnistía de 1977): el PDF extraído no incluye la firma.
- [ ] 122/000091 y 122/000092 (derecho de autodeterminación): sin BOCG.

## 5. Datos

- [ ] Seis días de votaciones con el zip corrupto en congreso.es (19/12/2013, 29/05/2014, 25/09/2014, 07/07/2015, 29/09/2015, 20/10/2015): omitidos.
- [ ] Viera Chacón (exPSOE, en el Mixto desde 2015) no se cuenta en ningún partido.
