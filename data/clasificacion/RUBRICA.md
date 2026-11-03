# Rúbrica de clasificación de iniciativas legislativas (XV legislatura)

Versión 2 (03/11/2026). Cambios respecto a la v1: se añaden la ciudadanía general, los sectores de empresa, la vivienda y el consumo, las profesiones públicas, los estudiantes, los pacientes, la dependencia y el riesgo de pobreza. Se pasa de "ante la duda, no marques" a "marca los efectos directos y los indirectos claros".

Objetivo: para cada iniciativa, decidir (1) si es de índole económica o social y (2) a qué colectivos beneficia (+1) o perjudica (-1) de forma **directa, o indirecta pero claramente previsible**, a partir de su título y de lo que se sepa de ella. La clasificación debe ser neutral, sobria y defendible: describe efectos, no opina sobre si la medida es buena o mala.

## 1. Tipo
- `eco`: el núcleo son impuestos, salarios, pensiones, prestaciones, empleo, vivienda como mercado, empresa, energía y precios, financiación o regulación de sectores.
- `soc`: derechos, igualdad, familia, educación, sanidad, justicia, seguridad, migración, memoria, instituciones, medio ambiente, cultura, etc.
- Si tiene ambos componentes, elige el principal en `tipo` y anota igualmente los impactos de los dos tipos.

## 2. Colectivos (usa SOLO estos identificadores)

### General
- `ciud`: **ciudadanía general**. Toda la población; en la web está activo por defecto en todos los perfiles. Úsalo solo cuando el efecto alcance a la población en su conjunto (ver criterios 3.2).

### Económicos
- Asalariados por tramo de base liquidable IRPF: `asal1` (≤12.450 €), `asal2` (12.450–20.200), `asal3` (20.200–35.200), `asal4` (35.200–60.000), `asal5` (60.000–300.000), `asal6` (>300.000)
- Funcionarios por subgrupo: `funA1`, `funA2`, `funB`, `funC1`, `funC2E`
- Pensionistas por pensión anual: `pen1` (<12.000 €, mínimas y no contributivas), `pen2` (12.000–25.000), `pen3` (25.000–42.000, hasta la máxima)
- Desempleados: `desPres` (con prestación contributiva), `desSub` (subsidio o Ingreso Mínimo Vital)
- Vivienda en propiedad: `viv0` (ninguna), `viv1` (una, la habitual), `viv2` (dos o más)
- Hipoteca y alquiler: `hipot` (con hipoteca), `inq` (vive de alquiler)
- Otro patrimonio neto **sin contar la vivienda habitual**: `prop1` (<200.000 €), `prop2` (200.000–700.000), `prop3` (700.000–3 M), `prop4` (>3 M)
- Empresarios por tamaño: `empAut` (autónomos), `empMicro` (<2 M€ de facturación), `empPeq` (2–10 M), `empMed` (10–50 M), `empGran` (>50 M)
- Empresarios por sector (complementa al tamaño): `secPrim` (agricultura, ganadería, pesca, forestal), `secInd` (industria, energía, minería, química), `secCons` (construcción, promoción e inmobiliario), `secTrans` (transporte y logística), `secCom` (comercio, hostelería y turismo), `secFin` (banca, seguros y finanzas), `secDig` (tecnología, telecomunicaciones y medios digitales)
- Consumo: `cons` (consumidores y usuarios de suministros y servicios: luz, gas, agua, telecomunicaciones, banca, transporte)
- Profesiones públicas: `proSeg` (policía, guardia civil, funcionarios de prisiones y fuerzas armadas), `proSan` (personal sanitario), `proDoc` (docentes)

### Sociales
`mujeres`, `lgtbi`, `jovenes`, `infancia` (infancia y familias), `mayores`, `inmigrantes`, `discapacidad`, `victimas` (víctimas de violencia, terrorismo, catástrofes o accidentes), `rural`, `minorias` (minorías étnicas, gitanos), `estud` (estudiantes de cualquier nivel), `pac` (pacientes y enfermos crónicos), `depend` (personas dependientes y sus cuidadores), `pobreza` (personas en riesgo de pobreza o exclusión: IMV, bono social, vulnerabilidad energética o residencial, sinhogarismo)

## 3. Criterios de impacto

### 3.1 Regla general
- Marca un colectivo si el efecto es **directo**, o **indirecto pero claro y previsible** por el objeto de la ley. No basta con que el colectivo "pudiera" verse afectado; tiene que poder explicarse en una frase.
- Marca **todos** los colectivos claramente afectados, también los económicos que se deriven de una medida social. Por ejemplo, las becas benefician a `estud` y a los tramos de renta que cumplen los umbrales (`asal1`, `asal2`, `desSub`, `pobreza`).
- Leyes institucionales, procesales, electorales, de organización administrativa, tratados o normas técnicas sin efecto distributivo claro → **sin impactos** (lista vacía). Sigue siendo correcto y frecuente.

### 3.2 Ciudadanía general (`ciud`)
- +1 cuando la ley mejora de forma general la salud pública, el medio ambiente (aire, agua, clima, residuos, biodiversidad), la seguridad alimentaria o de productos, o un servicio público universal.
- -1 cuando impone una carga general a toda la población (por ejemplo, una subida del IVA o de un impuesto que paga todo el mundo).
- **No** uses `ciud` para leyes institucionales, ideológicas o de derechos cuyo efecto general sea discutible (sistema electoral, CGPJ, símbolos, memoria, seguridad ciudadana). En esos casos marca solo los colectivos concretos o déjala vacía.
- Si el beneficio general recae en alguien con un coste concreto, marca también el perjuicio: una ley ambiental o de salud pública perjudica (-1) a los **sectores** que la cumplen (`secInd`, `secTrans`, `secPrim`…) y, si el coste es significativo para su tamaño, a `empAut`/`empMicro`/`empPeq`.
- Prohibiciones de bienestar animal con efecto sobre una actividad económica → -1 al sector afectado (por ejemplo, `secPrim` en la acuicultura). `ciud` solo si hay un beneficio general claro (sanitario o ambiental).

### 3.3 Impuestos y prestaciones
- Una subida de un impuesto perjudica a quien lo paga; una bajada le beneficia. Impuesto de patrimonio, sucesiones o grandes fortunas → tramos `prop*` afectados. Impuestos a la banca o a las energéticas → `empGran` y `secFin`/`secInd`.
- Prestaciones y subsidios: +1 a sus receptores. No marques perjuicio a los contribuyentes en general por el coste fiscal, salvo que la ley suba un impuesto concreto.
- Bonificaciones del transporte público → +1 `cons` (y `jovenes`/`rural` si van dirigidas a ellos).

### 3.4 Sectores y tamaño de empresa
- Usa el sector cuando la ley regula o grava una actividad concreta. Añade el tamaño solo si el efecto depende del tamaño (por ejemplo, un impuesto solo para grandes empresas → `empGran`).
- Coste laboral general (SMI, reducción de jornada) → -1 `empAut`, `empMicro`, `empPeq` (los sectores solo si les afecta especialmente, como `secCom` en hostelería).

### 3.5 Vivienda, patrimonio y consumo
- Control de alquileres, limitación de desahucios o restricciones al arrendador (incluido el alquiler turístico) → +1 `inq` (y `jovenes` si se dirige a ellos; `pobreza` si protege a vulnerables) y -1 `viv2` (quien tiene viviendas además de la habitual, que es quien alquila). **No** uses los tramos `prop*` para esto.
- Medidas contra grandes tenedores o la especulación inmobiliaria → -1 `prop3`/`prop4` (no `viv2`: tener una segunda vivienda no te hace gran tenedor).
- Ayudas a la compra de la primera vivienda → +1 `viv0`. Medidas sobre la vivienda habitual en propiedad (IBI de la vivienda habitual, comunidades de propietarios) → `viv1` (y `viv2` si afectan a cualquier vivienda).
- Okupación y desalojos exprés → +1 `viv2`. **No** marques `viv1`: quien solo tiene su vivienda habitual no gana nada, porque ocuparla ya es allanamiento de morada y tiene desalojo inmediato.
- Medidas sobre hipotecas (Euríbor, ayudas, código de buenas prácticas) → +1 `hipot`; si cuestan a la banca, -1 `secFin`.
- Protección del consumidor, rebajas de tarifas o prohibición de prácticas abusivas → +1 `cons` y -1 al sector regulado si le supone coste.

### 3.6 Educación, sanidad y cuidados
- Becas, tasas, acceso a la universidad o FP → `estud` (+ los tramos de renta si dependen de umbrales económicos).
- Sanidad pública, listas de espera, enfermedades raras, ELA, salud mental o medicamentos → `pac` (+ `discapacidad`/`depend` si procede). Salud pública general → también `ciud`.
- Dependencia, permisos y prestaciones por cuidado → `depend` (+ `mujeres` si el efecto sobre las cuidadoras es explícito, + `mayores` si procede).
- Condiciones laborales del personal sanitario, de los docentes o de las fuerzas de seguridad (salarios, equiparación, jubilación, condición de agente de la autoridad) → `proSan`/`proDoc`/`proSeg`.

### 3.7 Otros
- Ayudas por catástrofes (DANA, La Palma, incendios) → +1 `victimas` y, si incluyen ayudas a negocios, `empAut`/`empMicro`/`empPeq` y el sector afectado (a menudo `secPrim` o `secCom`).
- Migración: regularizaciones o ampliación de derechos de extranjeros → +1 `inmigrantes`; restricciones → -1 `inmigrantes`.
- Igualdad y violencia de género → `mujeres` (y `victimas` si se trata de violencia). LGTBI → `lgtbi`.
- Medidas generales para todos los asalariados (por ejemplo, la reducción de jornada) → +1 `asal1`–`asal4`.
- Si dudas entre +1 y -1 para un colectivo, no lo marques. Si dudas solo de la intensidad, márcalo.

## 4. Formato de salida
Un array JSON, un objeto por iniciativa, en el mismo orden de entrada:
```
{"id":"122/000086","tipo":"soc","imp":{"estud":1,"asal1":1},"nota":"Amplía las becas; beneficia a estudiantes de rentas bajas.","partido":""}
```
- `imp`: objeto colectivo → 1 o -1 (omite los neutros). Puede ser `{}`.
- `nota`: máximo 25 palabras, en español y neutral; explica el porqué de los impactos (o de su ausencia).
- `partido`: solo cuando el autor es el "Grupo Parlamentario Mixto": indica el partido proponente si lo sabes con seguridad (`Podemos`, `BNG`, `CC`, `UPN`, `Compromís`); si no, deja "". En el resto, "". **Conserva el valor existente** al reclasificar.
