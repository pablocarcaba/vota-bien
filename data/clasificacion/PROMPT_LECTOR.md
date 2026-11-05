# Prompt de los lectores independientes

Prompt de referencia normalizado para repetir el proceso (un agente de IA por lector y por lote). No es el texto
literal de la reclasificación con la rúbrica v3: los lectores reales se lanzaron con variantes cuya redacción y
restricciones difirieron entre lectores y rondas; aquí se unifican. Forma parte del proceso repetible descrito en `scripts/lotes_reclasificacion.py`,
`scripts/aplicar_reclasificacion.py` y `scripts/cerrar_reclasificacion.py`.

Marcadores que hay que sustituir antes de lanzar cada lector:

| Marcador | Valor |
|---|---|
| `{{REPO}}` | ruta absoluta del repositorio |
| `{{CLAVE}}` | clave de la legislatura (`congreso_xv`, `europarlamento_10`…) |
| `{{LECTOR}}` | `C`, `D` o `E` (tres lectores por lote, cada uno sin ver a los otros) |
| `{{LOTE}}` | nombre del fichero de lote (`<clave>_l00.json`…) |
| `{{DIR_LOTES}}` | carpeta con los lotes generados por `lotes_reclasificacion.py` |
| `{{DIR_SALIDA}}` | carpeta de la ronda: cada lector escribe en `{{DIR_SALIDA}}/{{LECTOR}}/{{LOTE}}`; esa carpeta es la que recibe `aplicar_reclasificacion.py` |
| `{{MAX_CHARS}}` | caracteres de texto de cada lote (`--chars`; 12.000 en la segunda ronda) |

Reglas del proceso (no del prompt): lanzar los lectores con modelos y sesiones independientes, sin compartir contexto
entre ellos; ningún lector escribe en el repositorio; los lotes se leen enteros.

## Primera ronda (Congreso; en el Parlamento Europeo, cambiar «BOCG» por «texto aprobado oficial»)

```
Eres un LECTOR INDEPENDIENTE (lector {{LECTOR}}) de una reclasificación con la rúbrica v3. Directorio: {{REPO}}.

1. Lee ENTERA `data/clasificacion/RUBRICA.md` (v3), la única fuente de criterios (prueba de efecto, tablas, peso, títulos genéricos, nota sin tramitación).
2. Clasifica el lote `{{DIR_LOTES}}/{{LOTE}}` (Congreso, legislatura {{CLAVE}}). Cada iniciativa trae `texto`: un extracto del texto oficial del BOCG (en reales decretos-ley, el de su proyecto de ley, ver `nota_fuente`). **Basa la clasificación en el `texto`.** Si está vacío o no permite saber quién gana o pierde y con qué signo, usa solo lo que sepas con seguridad; si aun así no se puede, aplica 3.9 (`imp: {}`, peso 1). Normas penales: regla 3.7.
3. Por iniciativa, en el mismo orden e id: `{"id","tipo","imp","peso","nota","partido"}`; la nota solo efectos (sin tramitación, resultado ni autor); `partido` vacío salvo que el texto lo diga.
4. Escribe el array JSON en `{{DIR_SALIDA}}/{{LECTOR}}/{{LOTE}}` (crea la carpeta) y valida con `python3 scripts/validar_clasificacion.py {{CLAVE}} <salida>`: puede avisar de iniciativas que faltan (lote parcial), pero no debe dar otros errores.

Independencia: NO leas `data/clasificacion/{{CLAVE}}/clas_*.json`, `REVISION.md`, `data/generado/`, `site/data/`, el historial de git ni otras carpetas de trabajo aparte de tu lote y tu salida. No modifiques el repositorio. Devuelve ruta, validado, nº sin impactos y total.
```

Respuesta esperada de cada lector: `{salida, validado, sin_impactos, total}`.

## Segunda ronda, Congreso (`lotes_reclasificacion.py --hueco`, `--chars 12000`)

```
Eres un LECTOR INDEPENDIENTE (lector {{LECTOR}}) de una reclasificación con la rúbrica v3. Directorio: {{REPO}}.

1. Lee ENTERA `data/clasificacion/RUBRICA.md` (v3), la única fuente de criterios.
2. Clasifica el lote `{{DIR_LOTES}}/{{LOTE}}`: iniciativas del Congreso que en una ronda anterior quedaron sin efectos por falta de contexto. Ahora `texto` trae hasta {{MAX_CHARS}} caracteres del texto oficial del BOCG (exposición de motivos y articulado; en reales decretos-ley, el de su proyecto de ley). **Lee el texto entero de cada una y basa la clasificación en lo que dice.** Si `texto` está vacío, usa solo el título. Solo si aun así no se puede determinar quién gana o pierde y con qué signo, aplica 3.9 (`imp: {}`, peso 1). Normas penales: regla 3.7.
3. Por iniciativa, en el mismo orden e id: `{"id","tipo","imp","peso","nota","partido"}`; la nota solo efectos (sin tramitación, resultado ni autor); `partido` vacío salvo que el texto lo diga.
4. Escribe el array JSON en `{{DIR_SALIDA}}/{{LECTOR}}/{{LOTE}}` (crea la carpeta) y valida con `python3 scripts/validar_clasificacion.py {{CLAVE}} <salida>`: puede avisar de iniciativas que faltan (lote parcial), pero no debe dar otros errores.

Independencia: NO leas `data/clasificacion/{{CLAVE}}/clas_*.json`, `REVISION.md`, `data/generado/`, `site/data/`, el historial de git ni otras carpetas de trabajo aparte de tu lote y tu salida. No modifiques el repositorio. Devuelve ruta, validado, nº sin impactos y total.
```

## Segunda ronda, Parlamento Europeo

```
Eres un LECTOR INDEPENDIENTE (lector {{LECTOR}}) de una reclasificación con la rúbrica v3. Directorio: {{REPO}}.

1. Lee ENTERA `data/clasificacion/RUBRICA.md` (v3), la única fuente de criterios.
2. Clasifica el lote `{{DIR_LOTES}}/{{LOTE}}`: procedimientos del Parlamento Europeo que en una ronda anterior, solo con el título, no se pudieron clasificar. Ahora `texto` trae hasta {{MAX_CHARS}} caracteres del **texto aprobado oficial** (resolución legislativa y, a menudo, la posición del Parlamento con el articulado). **Lee el texto y basa la clasificación en lo que la norma hace a ciudadanos, colectivos y sectores en España.** Si aun así no se puede determinar quién gana o pierde y con qué signo, aplica 3.9 (`imp: {}`, peso 1).
3. Por iniciativa, en el mismo orden e id: `{"id","tipo","imp","peso","nota","partido"}`; `tipo` eco o soc; la nota solo efectos (sin tramitación, resultado ni autor); `partido` vacío.
4. Escribe el array JSON en `{{DIR_SALIDA}}/{{LECTOR}}/{{LOTE}}` (crea la carpeta) y valida con `python3 scripts/validar_clasificacion.py {{CLAVE}} <salida>`: puede avisar de iniciativas que faltan (lote parcial), pero no debe dar otros errores.

Independencia: NO leas `data/clasificacion/{{CLAVE}}/clas_*.json`, `REVISION.md`, `data/generado/`, `site/data/`, el historial de git ni otras carpetas de trabajo aparte de tu lote y tu salida. No modifiques el repositorio. Devuelve ruta, validado, nº sin impactos y total.
```

## Ronda de leyes ómnibus (medidas, rúbrica 3.8)

Lotes con varias legislaturas: cada entrada lleva `clave`, `id`, `titulo` y `texto` (BOCG o, en los reales
decretos-ley, el BOE descargado con `scripts/textos_boe.py`; 20.000 caracteres). Tres lectores (C, D y E) por lote,
independientes. Se consolida con `scripts/consolidar_medidas.py` (es ómnibus si lo dicen 2 de 3; cada colectivo y
signo de las medidas cuenta si lo marcan 2 de 3).

```
Eres un LECTOR INDEPENDIENTE (lector {{LECTOR}}) de la clasificación de leyes ómnibus. Directorio: {{REPO}}.

1. Lee ENTERA `data/clasificacion/RUBRICA.md`, sobre todo 3.8 («Medidas (`medidas`) de una ley ómnibus»), 3.1.1, 3.1.2 y las tablas 3.3-3.7.
2. Clasifica cada ley del lote `{{DIR_LOTES}}/{{LOTE}}` basándote en su `texto` (oficial: BOCG o BOE). Si el texto no basta para un bloque, no lo inventes: omítelo. No hagas peticiones a congreso.es.
3. Decide si cada ley es ómnibus (dos o más bloques de medidas distintos, cada uno con su efecto) o no (una sola medida, aunque tenga ganadores y perdedores; o una ley con un único objeto).
   - Ómnibus: `medidas` = [{"d": 1-12 palabras, "imp": {...}, "peso": 1-3}], solo bloques con efecto claro; `imp` de la ley = unión de las medidas sin los colectivos con signos opuestos entre medidas; `peso` = el de la medida más pesada.
   - No ómnibus: sin `medidas`, con `imp` y `peso` según la rúbrica.
   - `tipo` (eco/soc) y `nota` (máx. 25 palabras, solo efectos, sin tramitación, resultado ni autor).
4. Salida: array JSON en el mismo orden e ids del lote, `{"id","tipo","imp","peso","nota","medidas"?}`, en `{{DIR_SALIDA}}/{{LECTOR}}/{{LOTE}}`. Compruébalo con `python3 -I {{COMPROBADOR}} {{DIR_LOTES}}/{{LOTE}} <salida>` hasta que dé OK.

Independencia: NO leas `data/clasificacion/*/clas_*.json`, `temas.json`, `REVISION.md`, `data/generado/`, `site/data/`, el historial de git ni otras carpetas de trabajo (rondas anteriores, otros lectores) aparte de tu lote y tu salida. No modifiques el repositorio. Devuelve: ruta, resultado del comprobador, nº de leyes con medidas y dudas.
```
