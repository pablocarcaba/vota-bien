# Rúbrica de clasificación de iniciativas legislativas (XV legislatura)

Objetivo: para cada iniciativa, decidir (1) si es de índole económica o social y (2) a qué colectivos beneficia (+1) o perjudica (-1) **de forma directa y previsible** según su título y lo que sepas de ella. La clasificación debe ser neutral, sobria y defendible: describe efectos, no opines sobre si la medida es buena o mala.

## 1. Tipo
- `eco`: el núcleo son impuestos, salarios, pensiones, prestaciones, empleo, vivienda como mercado, empresa, energía/precios, financiación, regulación de sectores.
- `soc`: derechos, igualdad, familia, educación, sanidad, justicia, seguridad, migración, memoria, instituciones, medio ambiente, cultura, etc.
- Si tiene ambos componentes, elige el principal en `tipo` y anota igualmente los impactos de ambos tipos.

## 2. Colectivos (usa SOLO estos identificadores)

Económicos:
- Asalariados por tramo de base liquidable IRPF: `asal1` (≤12.450 €), `asal2` (12.450–20.200), `asal3` (20.200–35.200), `asal4` (35.200–60.000), `asal5` (60.000–300.000), `asal6` (>300.000)
- Funcionarios por subgrupo: `funA1`, `funA2`, `funB`, `funC1`, `funC2E`
- Pensionistas por pensión anual: `pen1` (<12.000 €, mínimas y no contributivas), `pen2` (12.000–25.000), `pen3` (25.000–42.000, hasta la máxima)
- Desempleados: `desPres` (con prestación contributiva), `desSub` (subsidio o Ingreso Mínimo Vital)
- Propietarios por patrimonio neto: `prop1` (<200.000 €), `prop2` (200.000–700.000), `prop3` (700.000–3 M), `prop4` (>3 M)
- Empresarios: `empAut` (autónomos), `empMicro` (<2 M€ de facturación), `empPeq` (2–10 M), `empMed` (10–50 M), `empGran` (>50 M)

Sociales:
`mujeres`, `lgtbi`, `jovenes`, `infancia` (infancia y familias), `mayores`, `inmigrantes`, `discapacidad`, `victimas` (víctimas de violencia, terrorismo, catástrofes, accidentes), `rural`, `minorias` (minorías étnicas, gitanos)

## 3. Criterios de impacto
- Marca un colectivo solo si el efecto es **directo** y razonablemente claro (p. ej. subida del SMI → +1 para `asal1`; coste laboral para `empAut`, `empMicro` → -1 si es significativo).
- Impuestos: una subida de un impuesto perjudica a quien lo paga; una bajada le beneficia. Impuesto de patrimonio o a grandes fortunas → `prop3`/`prop4`. Impuestos a la banca o a energéticas → `empGran`.
- Prestaciones/subsidios: +1 a los receptores. No marques "perjuicio" a los contribuyentes en general por el coste fiscal salvo que la ley suba un impuesto concreto.
- Vivienda: control de alquileres o limitación de desahucios → +1 inquilinos vulnerables (usa `jovenes` si se dirige a jóvenes; si no, no marques social) y -1 `prop2`/`prop3`/`prop4` (propietarios arrendadores). Okupación/desalojos exprés → +1 propietarios.
- Ayudas por catástrofes (DANA, La Palma, incendios) → +1 `victimas` y, si incluyen ayudas a negocios, `empAut`/`empMicro`/`empPeq`. Si incluyen bonificaciones de transporte o medidas generales, márcalas por su colectivo.
- Leyes institucionales, procesales, de organización administrativa, tratados o técnicas sin efecto distributivo claro → `tipo` soc (o eco si es técnica económica) y **sin impactos** (lista vacía). Es correcto y frecuente que una iniciativa no afecte a ningún colectivo.
- Migración: regularizaciones o ampliación de derechos de extranjeros → +1 `inmigrantes`; restricciones → -1 `inmigrantes`.
- Igualdad, violencia de género → `mujeres` (y `victimas` si es violencia). LGTBI → `lgtbi`.
- No marques más de los colectivos claramente afectados. Si una medida beneficia a todos los asalariados por igual, marca `asal1`…`asal6` solo si la medida es realmente general (p. ej. reducción de jornada → +1 asal1–asal4, -1 empAut, empMicro, empPeq).
- Ante duda razonable, no marques.

## 4. Formato de salida
Un array JSON, un objeto por iniciativa, en el mismo orden de entrada:
```
{"id":"122/000086","tipo":"soc","imp":{"mujeres":1},"nota":"Crea oficina anticorrupción; sin efecto distributivo directo.","partido":""}
```
- `imp`: objeto colectivo → 1 o -1 (omite los neutros). Puede ser `{}`.
- `nota`: máximo 25 palabras, en español, neutral, explica el porqué del impacto (o de su ausencia).
- `partido`: solo cuando el autor es "Grupo Parlamentario Mixto": indica el partido proponente si lo sabes con seguridad (`Podemos`, `BNG`, `CC`, `UPN`, `Compromís`), si no, deja "". En el resto, "".
