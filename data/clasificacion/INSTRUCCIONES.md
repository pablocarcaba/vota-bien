# Instrucciones para clasificar un lote

Estas instrucciones son las mismas para cualquier legislatura y para quien clasifique (una persona o un agente de IA). Así todas las legislaturas se clasifican con el mismo criterio.

## Proceso

1. `python3 scripts/preparar_lotes.py <clave>` crea `data/clasificacion/<clave>/lotes/lote_NN.json` con las iniciativas pendientes (id, tipo, título, autor).
2. Se clasifica cada lote siguiendo estas instrucciones y `RUBRICA.md`. La salida va **fuera del repositorio** (por ejemplo, una carpeta temporal), con el mismo nombre del lote.
3. Se comprueba cada salida: `python3 scripts/validar_clasificacion.py <clave> <salida.json>` (0 errores).
4. `python3 scripts/integrar_clasificacion.py <clave> <salidas…>` guarda los `clas_N.json`, armoniza los RDL duplicados y valida todo.
5. Los casos dudosos se anotan en `data/clasificacion/<clave>/REVISION.md`.
6. Se regenera: `build_data.py <clave>` y `build_page.py`.

## Encargo para cada lote (texto para el agente)

> Clasifica las iniciativas legislativas del fichero `<lote>` para la web ciudadana y neutral «¿Quién legisla para ti?», que muestra a cada persona qué leyes le benefician o perjudican según su perfil.
>
> Lee entero `data/clasificacion/RUBRICA.md`: es la única fuente de criterios. No modifiques ningún fichero del proyecto.
>
> Para cada iniciativa, en el mismo orden y con el mismo id, produce `{"id", "tipo", "imp", "peso", "nota", "partido"}` según la sección 4 de la rúbrica.
> - Marca efectos directos y también los indirectos claros (rúbrica 3.1). Las leyes institucionales, procesales o electorales sin efecto distributivo claro llevan `imp: {}`: no fuerces impactos. No uses `ciud` para leyes ideológicas o institucionales (3.2).
> - Usa lo que sepas de cada ley concreta (su contenido real, no solo el título) cuando lo conozcas con seguridad; si no, cíñete al título.
> - Neutralidad estricta: describe efectos, sin valorarlos. El mismo criterio sea cual sea el partido autor.
> - `peso` (1, 2 o 3): alcance de la norma según la rúbrica 3.8; reserva el 3 para las grandes reformas.
> - `partido`: solo para el Grupo Mixto (o grupos que agrupen varios partidos) y solo si lo sabes con seguridad.
> - `nota`: 25 palabras como máximo, en español, explicando los impactos.
>
> Escribe el array JSON (UTF-8) en `<salida>` y valida con `python3 scripts/validar_clasificacion.py <clave> <salida>` hasta tener 0 errores.
>
> Al terminar, informa de: cuántas iniciativas quedan sin impactos, los 10 colectivos más usados y una lista de casos dudosos (id + una línea) para revisión humana.

## Criterios de calidad

- Lotes de unos 100: cabe el lote entero en una sola lectura y se mantiene la coherencia interna.
- Si dos lotes tratan leyes parecidas (por ejemplo, varias proposiciones sobre okupación), conviene revisar después que tengan los mismos colectivos.
- Cualquier cambio de criterio va primero a `RUBRICA.md` y después se reclasifica lo afectado, nunca al revés.
