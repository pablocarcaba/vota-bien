# Rúbrica de clasificación de iniciativas legislativas (todas las legislaturas)

Versión 3 (fecha 04/11/2026). Cambios respecto a la v2:
- La regla de los «efectos indirectos claros» se sustituye por una **prueba de efecto** de cuatro preguntas (3.1.2) y una lista cerrada de efectos indirectos admitidos (3.1.3).
- **Tablas de decisión** para los tramos de IRPF y pensiones (3.3), los tamaños de empresa y los sectores (3.4), `cons` y `pobreza` (3.5) y `ciud` (3.2, sin cambiar su criterio de fondo, incluido el eje público/privado).
- Reglas nuevas para normas penales y sancionadoras, víctimas, medio rural y permisos y derechos ligados a una situación (3.7).
- **Peso** con umbrales cerrados y regla para leyes ómnibus y prórrogas (3.8).
- **Títulos genéricos** e iniciativas del mismo contenido (3.9): si no se conoce el contenido, `imp: {}`; nunca adivinar.
- Regla para la **nota**: solo efectos; nunca tramitación, resultado ni autor (4).
- **Ejemplos resueltos** con casos reales de la doble lectura de la XV (5).
- Los identificadores de colectivos y el formato de salida no cambian.

Cambio posterior (04/11/2026): nuevo colectivo **`casero`** (alquila una vivienda a otros). Las medidas sobre el arrendador pasan de `viv2` a `casero`; `viv2` queda para quien tiene más de una vivienda, la alquile o no (okupación, IBI, plusvalía). Tener una segunda vivienda no convierte a nadie en arrendador.

Objetivo: para cada iniciativa, decidir (1) si es de índole económica o social y (2) a qué colectivos beneficia (+1) o perjudica (−1) a partir de su título y del texto o contenido que se conozca con seguridad. La clasificación debe ser neutral, sobria y defendible: describe efectos, no opina sobre si la medida es buena o mala. **Cada regla se aplica igual sea cual sea el autor de la iniciativa y la orientación de la medida**: si una regla marca −1 al endurecer una exigencia, marca +1 al suavizarla, y viceversa.

## 1. Tipo
- `eco`: el núcleo son impuestos, salarios, pensiones, prestaciones, empleo, vivienda como mercado, empresa, energía y precios, financiación o regulación de sectores.
- `soc`: derechos, igualdad, familia, educación, sanidad, justicia, seguridad, migración, memoria, instituciones, medio ambiente, cultura, etc.
- Si tiene ambos componentes, elige el principal en `tipo` y anota igualmente los impactos de los dos tipos.

## 2. Colectivos (usa SOLO estos identificadores)

### General
- `ciud`: **ciudadanía general**. Toda la población; en la web está activo por defecto en todos los perfiles. Úsalo solo en los casos de 3.2.

### Económicos
- Asalariados por tramo de base liquidable IRPF: `asal1` (≤12.450 €), `asal2` (12.450–20.200), `asal3` (20.200–35.200), `asal4` (35.200–60.000), `asal5` (60.000–300.000), `asal6` (>300.000)
- Funcionarios por subgrupo: `funA1`, `funA2`, `funB`, `funC1`, `funC2E`
- Pensionistas por pensión anual: `pen1` (<12.000 €, mínimas y no contributivas), `pen2` (12.000–25.000), `pen3` (25.000–42.000, hasta la máxima)
- Desempleados: `desPres` (con prestación contributiva), `desSub` (solo subsidio por desempleo, el asistencial; el Ingreso Mínimo Vital y las rentas mínimas no son de desempleo y van a `pobreza`, ver 3.5.2)
- Vivienda en propiedad: `viv0` (ninguna), `viv1` (una, la habitual), `viv2` (dos o más)
- Hipoteca y alquiler: `hipot` (con hipoteca), `inq` (vive de alquiler), `casero` (alquila una vivienda a otros; el asistente lo pregunta a quien tiene una vivienda en la que no vive)
- Otro patrimonio neto **sin contar la vivienda habitual**: `prop1` (<200.000 €), `prop2` (200.000–700.000), `prop3` (700.000–3 M), `prop4` (>3 M)
- Empresarios por tamaño: `empAut` (autónomos), `empMicro` (<2 M€ de facturación), `empPeq` (2–10 M), `empMed` (10–50 M), `empGran` (>50 M)
- Empresarios por sector (complementa al tamaño): `secPrim` (agricultura, ganadería, pesca, forestal), `secInd` (industria, energía, minería, química), `secCons` (construcción, promoción e inmobiliario), `secTrans` (transporte y logística), `secCom` (comercio, hostelería y turismo), `secFin` (banca, seguros y finanzas), `secDig` (tecnología, telecomunicaciones y medios digitales), `secSoc` (sanidad, educación y cuidados privados: clínicas, aseguradoras de salud, centros concertados, residencias)
- Consumo: `cons` (consumidores y usuarios de suministros y servicios: luz, gas, agua, telecomunicaciones, banca, transporte)
- Profesiones públicas: `proSeg` (policía, guardia civil, funcionarios de prisiones y fuerzas armadas), `proSan` (personal sanitario), `proDoc` (docentes)

### Sociales
Sexo: `hombres`, `mujeres`, `lgtbi`. Edad: `jovenes` (hasta 35 años), `adultos` (36–64), `mayores` (65 o más). Estado civil: `civSol`, `civPar` (casado/a o pareja de hecho), `civSep` (separado/a o divorciado/a), `civViu` (viudo/a). Familia: `infancia` (cualquier familia con hijos menores a cargo), `hij1`/`hij2`/`hij3` (solo si la medida depende del número de hijos; `hij3` = familia numerosa), `monop` (familia monoparental). Otros: `inmigrantes`, `discapacidad`, `victimas` (víctimas de violencia, terrorismo, catástrofes o accidentes), `rural`, `minorias` (minorías étnicas o religiosas, como la etnia gitana), `estud` (estudiantes de cualquier nivel), `pac` (pacientes y enfermos crónicos), `depend` (personas dependientes y sus cuidadores), `pobreza` (personas en riesgo de pobreza o exclusión: IMV, bono social, vulnerabilidad energética o residencial, sinhogarismo)

## 3. Criterios de impacto

### 3.1 Regla general

#### 3.1.1 Qué se marca
- Se marca un colectivo cuando pasa la **prueba de efecto** (3.1.2). Todo lo demás se deja sin marcar.
- Se marcan **todos** los colectivos que pasan la prueba, también los económicos que se deriven de una medida social, siguiendo las tablas de 3.3–3.7.
- Leyes institucionales, procesales, electorales, de organización administrativa, tratados o normas técnicas sin efecto que pase la prueba → **sin impactos** (`imp: {}`). Es correcto y frecuente.
- **Signos opuestos dentro de la misma ley**: si una parte de la ley beneficia a un colectivo y otra le perjudica, o si el signo depende de datos que no constan, ese colectivo no se marca. Se marcan los demás.

#### 3.1.2 Prueba de efecto (las cuatro preguntas)
Para cada colectivo candidato, responde en orden. Solo se marca si las cuatro respuestas son «sí».

| # | Pregunta | Si la respuesta es «no» |
|---|----------|-------------------------|
| P1 | ¿La ley **nombra** al colectivo, o regula, grava, subvenciona, obliga o prohíbe **directamente** la actividad o la situación que lo define (su renta, su pensión, su vivienda, su empresa, su sector, su profesión, su enfermedad…)? | Solo se marca si el efecto está en la lista cerrada de 3.1.3. |
| P2 | ¿El beneficio o el coste le llega **como consecuencia necesaria** de aplicar la ley, sin depender de cómo reaccionen terceros (mercado, clientes, infractores, otras administraciones)? | No se marca. |
| P3 | ¿Puede explicarse en **una frase con un solo «porque»** que remite a una disposición de la ley? («Beneficia a los inquilinos porque limita la subida de la renta.») Si hacen falta dos o más «porque» encadenados, no. | No se marca. |
| P4 | ¿Se conoce el **signo** con el título y el texto disponible, y es el mismo en toda la ley? | No se marca (3.1.1, signos opuestos; 3.9, títulos genéricos). |

Ejemplos de cadenas que **no** pasan (dos «porque» o reacción de terceros):
- Endurecer penas por hurto → menos hurtos → beneficia al comercio. (P1 no, P2 no, P3 no.)
- Bajar la tasa de alcohol al volante → se bebe menos fuera → perjudica a la hostelería.
- Facilitar la inversión de ayuntamientos → más obra pública → beneficia a la construcción.
- Dar seguridad jurídica al planeamiento → más vivienda → beneficia a quien busca su primera vivienda o a los jóvenes.
- Ayudas a los usuarios del transporte → más viajeros → beneficia a las empresas de transporte.
- Embargo de armas → menos gasto en defensa → perjudica a las fuerzas armadas.

#### 3.1.3 Efectos indirectos admitidos (lista cerrada)
Solo estos efectos se marcan aunque la ley no nombre al colectivo (P1 «no»). Deben cumplir igualmente P2–P4.
1. `ciud`, en los supuestos de 3.2.
2. Coste laboral general a cargo de la empresa → −1 `empAut`, `empMicro`, `empPeq` (3.4.2).
3. Medidas generales de IRPF que alcanzan a las pensiones por tributar como rendimientos del trabajo → tramos `pen` según 3.3.1.

No son indirectos, porque la ley regula directamente su actividad o situación (P1 «sí»): el arrendador en las medidas de alquiler (`casero`) y el sector que cumple una exigencia ambiental, sanitaria o de seguridad.

### 3.2 Ciudadanía general (`ciud`)
El criterio de fondo no cambia respecto a la v2. Esta sección solo lo hace más predecible.

**Casos en que se marca `ciud`** (no hay otros):

| Supuesto | Signo |
|----------|-------|
| Mejora general de la salud pública, del medio ambiente (aire, agua, clima, residuos, biodiversidad), de la seguridad alimentaria o de productos | +1 |
| Rebaja de una protección ambiental, climática, de biodiversidad o de salud pública (aplazar, suavizar o suprimir exigencias) | −1 (y +1 al sector que se ahorra el coste) |
| Endurecimiento de esa protección | +1 (y −1 al sector que la cumple) |
| Mejora del acceso, la cobertura o la calidad de un **servicio público universal** en su conjunto (sanidad pública, atención en las administraciones, justicia, educación pública) | +1 (empeorarlo: −1) |
| Subida de un impuesto que paga toda la población (IVA general, IVA de los alimentos, impuestos especiales de consumo general) | −1 (bajada: +1) |
| **Lo público frente a lo privado**: traspaso a manos privadas de un servicio, empresa, infraestructura o concesión pública (privatización, liberalización que reparte un mercado público, externalización, conciertos, concesiones) | −1, y +1 al sector que lo recibe (y a `empGran` si son grandes empresas) |
| Lo inverso: nacionalización, reversión de concesiones, gestión directa, titularidad pública, devolución de ayudas públicas | +1, y −1 al sector afectado |

Ejemplos del eje público/privado (de la v2): liberalización del ferrocarril → −1 `ciud`, +1 `secTrans`; gestión pública de la sanidad → +1 `ciud`, −1 `secSoc`.

**Cuándo no se marca `ciud`** (aclaraciones de aplicación):
- Leyes institucionales, ideológicas o de derechos cuyo efecto general sea discutible: sistema electoral, CGPJ, símbolos, memoria, seguridad ciudadana, política exterior, transparencia o lucha contra la corrupción.
- **Normas penales o sancionadoras**, incluidas las de tráfico que solo tipifican delitos o cambian penas. En cambio, las normas administrativas que reducen un riesgo para la salud de todos (por ejemplo, bajar la tasa máxima de alcohol al volante para todos los conductores) son salud pública → +1 `ciud`.
- **Suministros** (luz, gas, agua, telecomunicaciones) y servicios contratados por usuarios: su precio, calidad o seguridad de suministro van a `cons`, no a `ciud`.
- **Rebajas de precio, ayudas o gratuidades** para los usuarios de un servicio (bonos de transporte, gafas gratuitas, comedor gratuito): se marcan sus usuarios (`cons`, `pac`, `estud`, `infancia`…), no `ciud`. `ciud` solo si la ley mejora el servicio público en su conjunto (cobertura, acceso o calidad para todos).
- **El eje público/privado exige un traspaso** de titularidad o de gestión entre lo público y lo privado (en uno u otro sentido). No se aplica a: traspasos entre administraciones (del Estado a una comunidad autónoma, cogestión autonómica), reglas de contratación pública que no cambian quién presta el servicio, regulación de empresas privadas ya privadas, ni a la financiación de la inversión pública.
- Prohibiciones de bienestar animal con efecto sobre una actividad económica → −1 al sector afectado (por ejemplo, `secPrim` en la acuicultura). `ciud` solo si hay un beneficio general sanitario o ambiental claro.

### 3.3 Impuestos, prestaciones, tramos de IRPF y pensiones

#### Reglas generales
- Una subida de un impuesto perjudica a quien lo paga; una bajada le beneficia. Patrimonio, sucesiones o grandes fortunas → tramos `prop*` afectados. Impuestos a la banca o a las energéticas → `empGran` y `secFin`/`secInd`.
- Prestaciones y subsidios: +1 a sus receptores. No marques perjuicio a los contribuyentes en general por el coste fiscal, salvo que la ley suba un impuesto concreto.
- Los tramos `asal*` y `pen*` miden **renta**. No son un sinónimo de «trabajadores», «rentas bajas» ni «familias». Se marcan solo según las tablas siguientes. Si la medida beneficia a una situación (tener hijos, cuidar, estar enfermo, vivir de alquiler), se marca la situación, no los tramos.

#### 3.3.1 Tabla de tramos de IRPF (`asal1`–`asal6`)

| Tipo de medida | Tramos que se marcan |
|----------------|----------------------|
| Subida o bajada del SMI | `asal1` (los salarios en el SMI tienen base liquidable de `asal1`) |
| Exención, mínimo exento, supresión de retenciones o deducción dirigida a salarios en el nivel del SMI | `asal1` |
| Cambio del tipo de un tramo concreto de la tarifa | El tramo `asal` que contiene ese tramo de la tarifa **y todos los superiores** (todos pagan ese tipo por esa parte de su base) |
| Deflactación o cambio de toda la tarifa, o del mínimo personal | Todos los tramos `asal1`–`asal6` con el mismo signo; si la ley concentra el efecto en ciertos tramos y lo dice, solo esos |
| Reducción por rendimientos del trabajo | Los tramos que cubre la reducción según su umbral (regla del umbral, abajo) |
| Deducción, reducción o ayuda **con umbral de renta** (becas, ayudas al alquiler, copago, deducciones condicionadas) | El colectivo de la situación (`estud`, `inq`, `pac`…) **y** los tramos por debajo del umbral, según la regla del umbral |
| Deducción o ayuda **sin umbral de renta** (por alquiler, por maternidad, por discapacidad…) | Solo el colectivo de la situación; ningún tramo |
| Reducción de jornada, derechos laborales que se aplican a todos los asalariados | `asal1`–`asal4` (criterio v2) |
| Permisos, protecciones o derechos ligados a una situación (nacimiento, cuidado, incapacidad, enfermedad de un hijo) | Ningún tramo: solo la situación (`infancia`, `depend`, `discapacidad`, `pac`, `mujeres`, `hombres`) |
| Prestaciones a quien no trabaja (IMV, subsidio, escudo social) | Ningún tramo `asal`: `desSub`, `desPres`, `pobreza` según proceda |
| Cotizaciones del trabajador por encima de la base máxima (destope) | `asal5`, `asal6` (la base máxima queda en la parte alta de `asal4`, menos de la mitad de su intervalo) |

**Regla del umbral.** Los tramos se miden en **base liquidable** de la escala general: `asal1` hasta 12.450 €, `asal2` 12.450–20.200 €, `asal3` 20.200–35.200 €, `asal4` 35.200–60.000 €, `asal5` 60.000–300.000 €, `asal6` más de 300.000 €. Un tramo se marca si el umbral de la ley cubre **más de la mitad** de su intervalo. Ejemplo: un umbral de 35.000 € de base cubre `asal1`, `asal2` y `asal3`; uno de 100.000 € no cubre `asal5` (40.000 de 240.000). Si la ley no fija umbral o no se conoce, no se marcan tramos.

Si la ley da el umbral en **salario bruto** o en otra magnitud (rendimientos, renta de la unidad familiar, múltiplos del IPREM), no se traduce con tablas aproximadas: se marcan solo los tramos que **con seguridad** quedan por debajo del umbral (la base liquidable siempre es menor que el salario bruto, así que un umbral de 30.000 € brutos cubre con seguridad `asal1` y `asal2`, pero no se puede afirmar lo mismo de `asal3`). Ante la duda entre dos tramos, se marca solo el inferior y se anota en `REVISION.md`.

**Pensiones en el IRPF.** Las pensiones tributan como rendimientos del trabajo. Una medida **general** de IRPF (tarifa, mínimo personal, reducción por rendimientos del trabajo) que alcanza a `asal1`, `asal2` o `asal3` alcanza también a `pen2`; una que alcanza a `asal3` o `asal4`, a `pen3`. `pen1` no se marca en medidas de IRPF (sus pensiones apenas tributan) salvo que la ley la nombre. Las medidas dirigidas expresamente a salarios (SMI, retenciones del salario) no se trasladan a las pensiones.

#### 3.3.2 Tabla de pensiones (`pen1`–`pen3`)

| Tipo de medida | Se marca |
|----------------|----------|
| Revalorización general (mismo porcentaje para todas) | `pen1`, `pen2`, `pen3` + `mayores` |
| Subida adicional solo de mínimas o no contributivas | `pen1` (+ `mayores` si se trata de jubilación) |
| Subida de la pensión máxima | `pen3` |
| Pensiones de viudedad u orfandad | `civViu` (orfandad: `infancia`) y el tramo `pen` solo si la ley lo fija (por ejemplo, mínimas → `pen1`) |
| Cambio en el cálculo, la edad o la jubilación anticipada para todos | `pen1`–`pen3` con el signo que corresponda + `adultos` si cambia el acceso a la jubilación de quienes aún trabajan |
| Medida de un colectivo profesional (coeficientes reductores, jubilación parcial de un cuerpo) | Solo la profesión (`proSeg`, `proSan`, `proDoc`, `fun*`…); ningún tramo `pen` |
| Copago u otra aportación con escalas por renta | Cada tramo `pen` cuyo signo conste en el texto; el que no conste, no se marca |
| Compatibilidad de la pensión con el trabajo | `mayores` y los tramos `pen` que la ley alcance |

- `mayores` acompaña a los tramos `pen` cuando la medida afecta a las pensiones de jubilación **con el mismo signo para todos**. Si el signo cambia según el tramo, `mayores` no se marca.
- Un colectivo agregado (`pac`, `mayores`, `cons`) no se marca si la ley redistribuye dentro de él (unos pagan menos y otros más); se marcan los tramos con signo conocido.

#### 3.3.3 Otros
- Bonificaciones del transporte público → +1 `cons` (y `jovenes`/`rural`/`estud` si la ley les da un descuento específico). Las empresas de transporte no se marcan: la ayuda va a los usuarios y al operador se le compensa.

### 3.4 Sectores y tamaño de empresa

#### 3.4.1 Sectores (`sec*`)
- Se marca **solo el sector cuya actividad la ley regula, grava, subvenciona, obliga o prohíbe directamente**. Nunca sus clientes, proveedores o competidores, ni los sectores que «podrían» notarlo.
- Mapa para actividades dudosas:

| Actividad | Sector |
|-----------|--------|
| Producción y venta de electricidad, gas, petróleo; industria electrointensiva; defensa y armamento; industria alimentaria; laboratorios farmacéuticos y fabricantes de productos sanitarios | `secInd` |
| Agricultura, ganadería (incluida la de lidia), pesca, acuicultura, regadío, forestal | `secPrim` |
| Comercio, hostelería, turismo, ocio y espectáculos privados, servicios personales (peluquería, estética), farmacias y ópticas como venta minorista | `secCom` |
| Construcción, promoción, inmobiliarias, alquiler de vivienda por empresas | `secCons` (el alquiler por particulares va a `casero`, 3.5) |
| Clínicas, hospitales privados, aseguradoras de salud, centros concertados, residencias, servicios de cuidados privados | `secSoc` |
| Banca, seguros, fondos, mercados financieros | `secFin` |
| Telecomunicaciones, plataformas digitales, tecnología, medios audiovisuales y prensa | `secDig` |
| Transporte de viajeros y mercancías, logística, puertos y aeropuertos como operadores | `secTrans` |

- Una ley que solo cambia quién nombra a los órganos de un ente público o qué administración lo gestiona no afecta al sector (3.2, traspasos entre administraciones).

#### 3.4.2 Tamaño de empresa (`empAut`, `empMicro`, `empPeq`, `empMed`, `empGran`)

| Caso | Tamaños que se marcan |
|------|------------------------|
| La ley regula o grava una actividad sin distinguir tamaños | **Ninguno**: solo el sector |
| La medida se aplica a **todas las empresas** de cualquier actividad por igual (tipo general de Sociedades, cotizaciones empresariales generales, una obligación general de facturación o contabilidad) | **Todos** los que la soportan (`empAut` solo si alcanza a los autónomos) |
| La ley nombra un tamaño o fija un umbral | **Solo los nombrados**: «autónomos» → `empAut`; «microempresas» → `empMicro`; «pequeñas empresas» → `empMicro` + `empPeq`; «pymes» → `empMicro` + `empPeq` + `empMed`; «grandes empresas» → `empGran`; umbral de facturación → regla del umbral de 3.3.1 con los intervalos de facturación |
| Coste laboral **general** a cargo de la empresa (SMI, reducción de jornada, cotizaciones empresariales generales que suben) | −1 `empAut`, `empMicro`, `empPeq` (criterio v2: es donde el coste es significativo para su tamaño) |
| Coste ligado a la situación de un trabajador concreto (adaptar un puesto, un permiso individual) o que paga la Seguridad Social o el Estado (prestación por nacimiento, subsidios) | **Ninguno** |
| Ayudas a negocios por catástrofes o crisis dirigidas a autónomos y pequeñas empresas | `empAut`, `empMicro`, `empPeq` (y el sector si la ley lo nombra) |
| Normas penales, procesales, de contratación pública o de organización administrativa | **Ninguno** |

### 3.5 Vivienda, patrimonio, consumo y pobreza

#### Vivienda y patrimonio (sin cambios de fondo respecto a la v2)
- Control de alquileres, limitación de desahucios, prórroga de contratos o restricciones al arrendador (incluido el alquiler turístico por particulares) → +1 `inq` (y `jovenes` si se dirige a ellos; `pobreza` si protege a vulnerables) y −1 `casero`. **No** uses `viv2` (no todo el que tiene dos viviendas alquila) ni los tramos `prop*` para esto.
- Incentivos fiscales al arrendador (por ejemplo, rebajas de IRPF por alquilar barato) → +1 `casero`. Si la misma ley también limita o grava al arrendador, o le compensa y además le da un incentivo, `casero` tiene signos opuestos y no se marca (3.1.1).
- Medidas contra grandes tenedores o la especulación inmobiliaria → −1 `prop3`/`prop4` (no `viv2` ni `casero`).
- Ayudas a la compra de la primera vivienda → +1 `viv0`. IBI de la vivienda habitual o comunidades de propietarios → `viv1` (y `viv2` si afectan a cualquier vivienda). Una modificación de la Ley de Propiedad Horizontal solo se marca si se conoce qué cambia (3.9).
- Okupación y desalojos exprés → +1 `viv2`. **No** marques `viv1`. Restricciones a las segundas residencias o a las viviendas vacías → `viv2`; si además limitan el alquiler, también `casero`.
- Hipotecas (Euríbor, ayudas, código de buenas prácticas) → +1 `hipot`; si cuestan a la banca, −1 `secFin`.

#### 3.5.1 Tabla de `cons`

| Se marca `cons` | No se marca `cons` |
|-----------------|--------------------|
| Precios, tarifas, calidad, derechos o seguridad de suministro de luz, gas, agua, telecomunicaciones, banca, seguros o transporte | Políticas de apoyo a productores (por ejemplo, declarar estratégico el sistema alimentario) |
| IVA o impuesto de un suministro o servicio concreto (luz, peluquería) | IVA general o de los alimentos: va a `ciud` (3.2) |
| Prohibición de prácticas abusivas, atención a la clientela, garantías de los consumidores | Medicamentos, gafas, tratamientos: van a `pac` |
| Bonificaciones del transporte público | Servicios públicos gratuitos (comedor, sanidad): sus usuarios (`estud`, `infancia`, `pac`) |

Si la protección del consumidor supone un coste para el sector regulado, −1 a ese sector.

#### 3.5.2 Tabla de `pobreza`

| Se marca `pobreza` | No se marca `pobreza` |
|--------------------|-----------------------|
| La ley se dirige por un criterio de vulnerabilidad o renta muy baja **que figura en ella**: IMV, bono social, vulnerabilidad energética o residencial, suspensión de desahucios de vulnerables, sinhogarismo, barrios vulnerables, ayudas con umbral igual o inferior a 2 veces el IPREM | Medidas universales (comedor gratuito para todos, gratuidad de un producto sanitario para todos) |
| | Medidas de IRPF, incluidas las del nivel del SMI: van a `asal1` |
| | Revalorización general de pensiones, subsidios por desempleo sin criterio de vulnerabilidad: van a `pen*`, `desSub` |
| | Ocupación ilegal de viviendas: el efecto se asigna a `viv2` (3.5), no a `pobreza` |

### 3.6 Educación, sanidad y cuidados
- Becas, tasas, acceso a la universidad o FP → `estud` (+ tramos de renta solo si la ley fija un umbral, según 3.3.1).
- Sanidad pública, listas de espera, enfermedades raras, ELA, salud mental o medicamentos → `pac` (+ `discapacidad`/`depend` si procede). Salud pública general → también `ciud`.
- Gestión sanitaria pública o privada → regla «lo público frente a lo privado» (3.2): +1 `ciud` y −1 `secSoc` si refuerza la gestión pública; al revés si amplía la privada.
- Dependencia, permisos y prestaciones por cuidado → `depend` (+ `mujeres` si el efecto sobre las cuidadoras es explícito en la ley, + `mayores` si procede).
- Condiciones laborales del personal sanitario, de los docentes o de las fuerzas de seguridad (salarios, equiparación, jubilación, condición de agente de la autoridad) → `proSan`/`proDoc`/`proSeg`. Se marcan solo si la ley regula esas condiciones; una reforma educativa o sanitaria que no las toca no marca `proDoc` ni `proSan`.

### 3.7 Otros
- Ayudas por catástrofes (DANA, La Palma, incendios) → +1 `victimas` y, si incluyen ayudas a negocios, `empAut`/`empMicro`/`empPeq` y el sector que la ley nombre (a menudo `secPrim` o `secCom`).
- **Normas penales y sancionadoras**: tipificar, endurecer, suavizar o despenalizar una conducta **no** se asigna a quienes podrían cometerla ni a sus víctimas potenciales en abstracto → `imp: {}`. Excepciones: (a) la ley da derechos, ayudas, indemnizaciones o garantías procesales a un colectivo concreto (víctimas, menores en un procedimiento, extranjeros en la determinación de su edad) → ese colectivo; (b) la ley prohíbe una práctica lícita propia de un colectivo (por ejemplo, prendas religiosas) → −1 a ese colectivo (`minorias`).
- `victimas`: se marca cuando la ley reconoce derechos, ayudas, indemnizaciones o protección procesal a las víctimas. No por endurecer o suavizar penas.
- Migración: regularizaciones o ampliación de derechos de extranjeros → +1 `inmigrantes`; restricciones → −1 `inmigrantes`. Un traspaso de competencias entre administraciones, sin cambio de derechos conocido, no se marca.
- Restricciones a prendas o prácticas religiosas (por ejemplo, prohibir el velo integral) → −1 `minorias`, no `inmigrantes`: afectan por religión, no por nacionalidad. No se añade `mujeres` ni `victimas` (P2: el beneficio alegado depende de supuestos, no del texto).
- Igualdad y violencia de género → `mujeres` (y `victimas` si la ley da derechos o ayudas a víctimas de violencia). LGTBI → `lgtbi`.
- `hombres`: solo cuando la medida se dirige a ellos o se aplica expresamente a ambos sexos o progenitores (permiso de nacimiento igual para los dos → +`mujeres` y +`hombres`). **No** marques −`hombres` en medidas de igualdad a favor de las mujeres, salvo que retiren un derecho concreto a los hombres.
- Familia: `infancia` para cualquier familia con hijos; `hij3` para familias numerosas; `monop` solo si la ley contiene una disposición específica para familias monoparentales; `civViu` para viudedad u orfandad; `civSep` para divorcio, custodia o pensiones compensatorias solo si el signo es claro. Los menores extranjeros no acompañados no son `infancia` (que es «familia con hijos a cargo»).
- Edad: `jovenes`/`adultos`/`mayores` cuando la medida fija un tramo de edad (bono alquiler joven, subsidio para mayores de 52 → `adultos`, pensiones de jubilación → `mayores` según 3.3.2).
- `rural`: solo medidas **territoriales** (municipios rurales, despoblación, servicios o transporte en el medio rural). Las medidas para el sector agrario, ganadero o pesquero van a `secPrim`, no a `rural`.
- Funcionarios (`fun*`): se marcan cuando la ley cambia las condiciones de los empleados públicos con signo conocido; todos los subgrupos si se aplica a todos, solo los nombrados si los distingue. Un permiso o derecho general que también alcanza a los empleados públicos se marca por la situación (3.3.1), no por `fun*`.
- Si dudas entre +1 y −1 para un colectivo, no lo marques. Si dudas solo de la intensidad, márcalo.

### 3.8 Peso de la iniciativa (`peso`)
Mide el alcance de la norma, no si es buena o mala ni si se aprobó. La web lo usa para que una gran reforma cuente más que una ley menor (peso 3 = 9 leyes menores, peso 2 = 3). **Se pesa por lo que la iniciativa cambia, no por el nombre de la ley que modifica**: una proposición que reforma la ley de educación solo para regular los comedores no es una ley de educación integral.

Aplica las preguntas en este orden y quédate con la primera que se cumpla:

| Paso | Pregunta | Peso |
|------|----------|------|
| 1 | ¿Es una de estas? Presupuestos Generales; reforma laboral (cambia al menos dos de: contratación, despido, negociación colectiva, jornada general); reforma de pensiones (cálculo, edad, revalorización estructural o financiación del sistema); reforma fiscal integral (cambia la tarifa del IRPF completa o al menos dos de IRPF, IVA y Sociedades); SMI; revalorización general de las pensiones; creación o reforma integral del IMV; ley integral de vivienda, educación o sanidad (nueva ley orgánica o de bases completa); ómnibus con **tres o más bloques que por sí solos pesarían 2** | **3** |
| 2 | ¿Se limita a un colectivo pequeño (una profesión o cuerpo concreto, los afectados por una enfermedad concreta, una comunidad autónoma, isla o ciudad), es una prórroga sin cambios sustantivos, una transposición técnica, uno o pocos artículos sin cambiar los elementos principales, o una norma institucional o procesal? | **1** |
| 3 | ¿Crea, suprime o cambia los elementos principales (cuantía, tipo, duración, requisitos) de un impuesto, una prestación, un derecho laboral o social, o regula de forma sustantiva la actividad de un sector entero? | **2** |
| 4 | Resto | **1** |

- **Ómnibus** (reales decretos-ley o leyes con varios bloques): los impactos son la unión de los de cada bloque identificable en el título o el texto disponible, aplicando 3.1.1 a los signos opuestos. Las disposiciones finales técnicas no se clasifican si no se conoce su contenido. El peso es 3 si hay tres o más bloques de peso 2; si no, el del bloque más pesado.
- **Prórrogas**: la prórroga de un paquete se pesa con la regla de ómnibus, valorando cada bloque prorrogado como si fuera nuevo; la prórroga de una medida suelta pesa 1.
- Una iniciativa con `imp: {}` lleva peso 1, salvo las grandes reformas institucionales (Constitución, estatutos de autonomía, ley electoral, Ley Orgánica del Poder Judicial completa), que llevan 2 como máximo.
- Las proposiciones se pesan por lo que proponen, aunque no prosperasen.
- El real decreto-ley y su tramitación como proyecto de ley llevan el mismo peso **y los mismos impactos** (3.9).

### 3.9 Títulos genéricos e iniciativas del mismo contenido
- Un **título genérico** solo cita la ley o el artículo que modifica («modificación de la Ley 35/2006 del IRPF…», «modifica el apartado Uno.2 del artículo 91 de la Ley del IVA», «reforma parcial del Estatuto Básico del Empleado Público», «modificación del Código Penal»).
- Si con el título y el texto disponible (exposición de motivos, texto publicado, contenido conocido con seguridad) **no se puede determinar a quién afecta y con qué signo** → `imp: {}`, `peso: 1`, nota «El título no permite determinar el contenido». **Nunca adivinar** el contenido por el nombre de la ley, por el autor ni por su orientación.
- Si el contenido se conoce con seguridad, se clasifica por ese contenido, y la nota lo resume para que otro lector pueda comprobarlo.
- Iniciativas con el mismo contenido (registros duplicados, el real decreto-ley y el proyecto de ley que procede de él, proposiciones idénticas de distintos grupos) llevan **la misma clasificación**. La duplicidad se anota en `REVISION.md`, no en la nota.

## 4. Formato de salida
Un array JSON, un objeto por iniciativa, en el mismo orden de entrada:
```
{"id":"122/000086","tipo":"soc","imp":{"estud":1,"asal1":1},"peso":2,"nota":"Amplía las becas; beneficia a estudiantes de rentas bajas.","partido":""}
```
- `imp`: objeto colectivo → 1 o -1 (omite los neutros). Puede ser `{}`.
- `peso`: 1, 2 o 3 según 3.8.
- `nota`: máximo 25 palabras, en español y neutral; explica el porqué de los impactos (o de su ausencia). **Describe solo a quién afecta la ley y cómo.** No menciones nunca su tramitación ni su resultado (aprobada, rechazada, retirada, convalidada, no convalidada, decaída, caducada, en vigor, tomada en consideración, duplicada), ni su autor o grupo, ni valoraciones. La web muestra qué votó cada partido: si la ley salió adelante o no es irrelevante para la clasificación.
- `partido`: solo cuando el autor es un grupo que agrupa varios partidos (Grupo Mixto; en la XIV también el Grupo Plural): indica el partido proponente si lo sabes con seguridad, con el nombre exacto que usa `nominal` en `scripts/legislaturas.py` para esa legislatura (XV: `Podemos`, `BNG`, `CC`, `UPN`, `Compromís`); si no, deja "". En el resto, "". **Conserva el valor existente** al reclasificar.

## 5. Ejemplos resueltos (casos reales de la doble lectura de la XV)
Las lecturas A y B son dos lectores independientes que aplicaron la v2. «Vigente» es la clasificación publicada. La columna «v3» es la clasificación correcta con esta rúbrica.

### 5.1 Título genérico: 122/000155 y 125/000011
Ambas se titulan «Proposición de Ley de modificación de la Ley 35/2006 … del IRPF y de modificación parcial de las leyes de los Impuestos sobre Sociedades, sobre la Renta de no Residentes y sobre el Patrimonio».
- A y B, que solo vieron el título, supusieron una reforma fiscal amplia (+`asal1`…, −`asal5`, −`prop4`, −`empGran`, peso 3) en las dos.
- El texto dice cosas muy distintas: la 122/000155 prohíbe practicar retenciones a quien cobra el SMI; la 125/000011 declara exentas las indemnizaciones a ganaderos por sacrificio obligatorio o daños de fauna salvaje.
- **v3**: con el texto, 122/000155 → `{"asal1":1}`, peso 1 (tabla 3.3.1: medida dirigida a salarios del SMI; uno o pocos artículos). 125/000011 → `{"secPrim":1}`, peso 1 (`rural` no: es una medida sectorial, no territorial, 3.7). **Sin el texto**, las dos → `{}`, peso 1 (3.9). Lo que nunca procede es deducir el contenido del título.

### 5.2 Copago con escalas por renta: 130/000042 (y su proyecto de ley 121/000097)
Rehace la aportación farmacéutica: topes reducidos para activos con base inferior a 35.000 €, exención para quien cobra complemento a mínimos y un «tope intermedio» para pensionistas.
- Vigente: `asal1–3 +`, `pen1–3 +`, `pac +`. A: `pen2 −`, `pen3 −`, `pac −`, `mayores −`, `secSoc +`. B: `pen3 −`, `pac +`, `mayores +`, `secSoc −`. En el proyecto de ley, A y B no marcaron nada.
- **v3**: `{"asal1":1,"asal2":1,"asal3":1,"pen1":1}`, peso 2, igual en las dos iniciativas (3.9). El umbral de 35.000 € de base cubre `asal1`–`asal3` (regla del umbral). `pen2` y `pen3` solo se marcan si el texto deja claro si su tope sube o baja: A y B les dieron signos opuestos, prueba de que se estaba adivinando (P4). `pac` y `mayores` no se marcan mientras el signo de algún tramo no conste (3.3.2). `secSoc` no: las farmacias y laboratorios no son el sector regulado por el copago (P1).

### 5.3 Permiso ligado a una situación: 130/000023
Amplía el permiso de nacimiento y cuidado para ambos progenitores (Estatuto de los Trabajadores, EBEP y Seguridad Social).
- Vigente: `infancia`, `mujeres`, `hombres`, `depend` +. A añade −`empAut`, −`empMicro`, −`empPeq` y `monop`. B añade `asal1–4`, los cinco `fun*` y −`empAut`, −`empMicro`; peso 3.
- **v3**: `{"infancia":1,"mujeres":1,"hombres":1}`, peso 2. Es un permiso ligado a una situación: no se marcan tramos `asal` ni `fun*` (3.3.1, 3.7). La prestación la paga la Seguridad Social: ningún tamaño de empresa (3.4.2). `depend` no: el permiso es por nacimiento, no por cuidado de una persona dependiente. `monop` solo si el texto incluye una ampliación específica para familias monoparentales. Peso 2: cambia la duración de una prestación (3.8, paso 3).

### 5.4 Norma penal: 124/000037 (multirreincidencia en hurto y estafa) y 122/000192 (coacciones al derecho al trabajo)
- 124/000037. Vigente: `secCom +`. A: sin impactos. B: `secCom`, `empAut`, `empMicro` +.
- 122/000192. Vigente: sin impactos. A: `asal1–3 +`. B: `empAut`, `empMicro`, `empPeq` +.
- **v3**: las dos → `{}`, peso 1. Endurecer penas no beneficia a las víctimas potenciales en abstracto ni perjudica a quien podría cometer el delito (3.7). El supuesto beneficio necesita dos «porque» y depende de cómo reaccionen los infractores (P2, P3). La regla es la misma para cualquier norma que endurezca o suavice penas.

### 5.5 Rebaja y endurecimiento ambiental: 122/000140 (residuos) y 122/000275 (alimentación saludable)
- 122/000140 suprime el impuesto a los envases de plástico no reutilizables y rebaja objetivos de reutilización. Vigente: `secInd +`. A: `ciud −`, `secInd +`, `secCom +`. B: `ciud −` («sentido incierto»).
- 122/000275 promueve alimentos saludables y limita los no saludables. Vigente: `ciud +`, `infancia +`, `secInd −`. A: `ciud +`, `cons +`, `pac +`, `secInd −`. B: `ciud +`, `secInd −`.
- **v3**: 122/000140 → `{"ciud":-1,"secInd":1}`, peso 2. Es una rebaja de protección ambiental (3.2) y el impuesto lo pagan fabricantes e importadores de envases (`secInd`); el comercio no es el sector gravado (3.4.1). Si solo se dispone del título («modificación de la Ley 7/2022 de residuos»), `{}` (3.9): no se puede saber si endurece o suaviza.
  122/000275 → `{"ciud":1,"secInd":-1}`, peso 2. Es la regla inversa: salud pública +1 `ciud` y −1 a la industria alimentaria que cumple. `cons` no (3.5.1), `pac` no (no regula ningún tratamiento), `infancia` solo si el texto contiene medidas dirigidas a menores.

### 5.6 Signos opuestos en el mismo sector y suministro: 130/000021 (refuerzo del sistema eléctrico)
Impulsa el almacenamiento, impone exigencias técnicas a los operadores y recupera apoyos a la industria electrointensiva.
- Vigente: `secInd +` (con la nota «No fue convalidado»). A y B: `ciud +`, `cons +`, `secInd −`; B, peso 3.
- **v3**: `{"cons":1}`, peso 2. La seguridad de suministro eléctrico va a `cons`, no a `ciud` (3.2). `secInd` recibe exigencias (−) y apoyos (+) en la misma ley: no se marca (3.1.1). Peso 2: regulación sustantiva de un sector. La nota debe describir solo el efecto, sin mencionar la convalidación (4).

### 5.7 Medida mixta sobre el arrendador: 122/000196 (alquiler asequible)
Rebajas de IRPF a quien alquila barato o a jóvenes, IVA del 21 % al alquiler turístico, impuesto a compradores extracomunitarios y vivienda pública.
- Vigente: `inq`, `jovenes`, `viv2` +, `secCom −`. A: `inq`, `jovenes`, `viv2`, `secCons` +. B: `inq`, `jovenes` +, `viv2 −`.
- **v3**: `{"inq":1,"jovenes":1}`, peso 2. El arrendador (hoy `casero`) gana con la rebaja de IRPF y pierde con el IVA turístico: signos opuestos, no se marca (3.1.1, 3.5). `secCom` solo si la ley grava expresamente a empresas turísticas; el alquiler turístico de particulares va a `casero` (3.4.1). `secCons` no: «más oferta beneficia a la construcción» necesita dos «porque» (P3).

### 5.8 Peso por contenido, no por la ley modificada: 122/000117 (comedores escolares en la LOE)
Mandata comedores escolares universales, gratuitos y abiertos todo el año en centros públicos.
- Vigente: `estud`, `infancia`, `pobreza` +, peso 2. A: `estud`, `infancia`, `proDoc` +, peso 3. B: `estud`, `proDoc` +, peso 3.
- **v3**: `{"estud":1,"infancia":1}`, peso 2. Reforma un servicio concreto, no toda la ley de educación (3.8). `proDoc` no: no regula las condiciones de los docentes (3.6). `pobreza` no: la medida es universal (3.5.2). `ciud` no: es una gratuidad para los usuarios (3.2).

### 5.9 Ómnibus: 130/000012 (Real Decreto-ley 9/2024)
Revaloriza las pensiones, prorroga ayudas al transporte y la suspensión de desahucios de personas vulnerables.
- Vigente: `pen1–3`, `inq`, `pobreza`, `cons` +, `viv2 −`. A: añade `mayores`, `secTrans`, `empAut` y quita `inq` y `viv2`. B: `pen1`, `pen2`, `mayores`, `cons`, `pobreza`, `inq`, `asal1`, `asal2` +.
- **v3**: `{"pen1":1,"pen2":1,"pen3":1,"mayores":1,"cons":1,"inq":1,"pobreza":1,"casero":-1}`, peso 3. Unión de los bloques identificables (3.8): revalorización general → los tres tramos + `mayores` (3.3.2); transporte → `cons`, sin `secTrans` (3.3.3); desahucios de vulnerables → `inq`, `pobreza`, −`casero` (3.5). `asal1`/`asal2` no: no hay medida sobre salarios (3.3.1). `empAut` no: no consta el bloque en el título ni en el texto disponible. Peso 3 porque incluye la revalorización general de las pensiones (3.8, paso 1, y regla de ómnibus).

### 5.10 Tipo reducido de IVA de un servicio: 124/000001
Título: «modifica el apartado Uno, punto 2, del artículo 91 de la Ley del IVA». El texto aplica el 10 % a peluquería, barbería y estética.
- Vigente: `cons`, `secCom`, `empAut`, `empMicro` +. A y B, solo con el título: sin impactos.
- **v3**: con el texto → `{"cons":1,"secCom":1}`, peso 1. El IVA de un servicio concreto va a `cons` (3.5.1) y al sector que lo presta (servicios personales → `secCom`, 3.4.1). Ningún tamaño: el tipo no distingue tamaños (3.4.2). Sin el texto, A y B acertaron con `{}` (3.9).

### 5.11 Estatuto del Empleado Público sin contenido conocido: 125/000008 y 125/000010
Títulos: «reforma parcial» y «modificación» del Estatuto Básico del Empleado Público.
- Vigente: sin impactos. A y B: los cinco subgrupos `fun*` +, peso 1 o 2.
- **v3**: `{}`, peso 1, mientras no se conozca qué cambian (3.9). Que una ley trate de los funcionarios no dice si les beneficia o les perjudica (P4).

### 5.12 Cadena de efectos en seguridad vial: 122/000139 (tasa de alcohol) y 122/000257 (delito de velocidad)
- 122/000139. Vigente: `ciud +`. A: `ciud +`, `victimas +`, `secCom −`. B: `ciud +`, `secTrans −`.
- 122/000257. Vigente y A: sin impactos. B: `ciud +`.
- **v3**: 122/000139 → `{"ciud":1}`, peso 1. Bajar la tasa para todos los conductores es una medida administrativa de salud pública (3.2). La hostelería no está regulada (P1) y el efecto depende de cómo reaccionen los clientes (P2). `secTrans` solo si el texto cambia la tasa de los conductores profesionales. `victimas` no: la ley no da derechos a las víctimas (3.7).
  122/000257 → `{}`, peso 1: es solo penal (3.2, 3.7).
