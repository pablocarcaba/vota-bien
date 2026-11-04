# ¿Quién legisla para ti?

Herramienta web que permite a cualquier persona marcar su perfil (tramo de IRPF, funcionario, pensionista, propietario, empresario, colectivos sociales…) y ver qué partidos presentaron y votaron leyes que le benefician o perjudican.

Web: https://pablocarcaba.github.io/vota-bien/

Disponible: XV legislatura del Congreso de los Diputados (17/08/2023 – disolución 06/10/2026), datos descargados el 02/11/2026. En preparación: XIV legislatura.

## Estructura

Cada fuente y legislatura es un dataset independiente con clave `<fuente>_<legislatura>` (p. ej. `congreso_xv`). Los partidos cambian entre legislaturas, así que nunca se mezclan: la web tiene un selector de fuente y otro de legislatura.

```
data/
  fuente/                     Datos de origen (no se editan)
    congreso_xv.json            Iniciativas y votaciones de la XV
    congreso_xv_votos_extra.json  38 votaciones finales que faltaban en la primera pasada
    congreso_xiv.json           (en descarga) XIV legislatura
  clasificacion/
    RUBRICA.md                  Criterios de clasificación, comunes a todas las legislaturas
    INSTRUCCIONES.md            Proceso y encargo fijo para clasificar lotes
    congreso_xv/
      clas_0..4.json            Clasificación de cada iniciativa: tipo, impactos por colectivo (+1/-1), nota
      REVISION.md               Casos dudosos pendientes de revisión
      lotes/chunk_0..4.json     Lotes enviados a clasificar (histórico)
  generado/<clave>/items.json   Iniciativas normalizadas (build_items.py); no editar
  cache/                      Respuestas de congreso.es guardadas por la descarga (ignorado por git)
scripts/
  legislaturas.py             Configuración por legislatura: grupos, partidos, textos
  descargar_legislatura.py    Descarga fichas de iniciativas y votaciones del Pleno (reanudable)
  descargar_historico.sh      Descarga en serie las legislaturas X–XIII del Congreso
  descargar_europarlamento.py Parlamento Europeo (10.ª): procedimientos y voto de eurodiputados españoles
  identificar_mixto.py        Partido de las proposiciones de los grupos Mixto y Plural (por el BOCG)
  textos_bocg.py              Texto de iniciativas concretas (BOCG) para revisar su clasificación
  build_items.py              data/fuente/<clave>.json -> data/generado/<clave>/items.json
  build_data.py               items + clasificación + votaciones -> site/data/<clave>.json
  build_page.py               template.html + catálogo de datasets -> site/index.html
  preparar_lotes.py           Lotes de iniciativas sin clasificar
  integrar_clasificacion.py   Integra lotes clasificados, armoniza RDL duplicados y valida
  validar_clasificacion.py    Comprueba clas_*.json contra la rúbrica y los colectivos de la web
site/
  template.html               Página (HTML/CSS/JS sin dependencias, salvo Google Fonts)
  index.html                  Página final (generada)
  data/<clave>.json           Un dataset por fuente y legislatura; la página los carga con fetch
```

## Reconstruir

```
python3 scripts/build_items.py congreso_xv
python3 scripts/validar_clasificacion.py
python3 scripts/build_data.py congreso_xv
python3 scripts/build_page.py
```

`build_data.py` imprime las votaciones que reasigna (la web del Congreso no siempre indica el expediente de cada votación; se comprueba comparando títulos). La página carga los datos con `fetch`: para verla en local, sírvela con `python3 -m http.server 8000 --directory site`.

## Añadir una legislatura

1. Descargar: `python3 scripts/descargar_legislatura.py --leg XIV --desde 2019-12-03 --hasta 2023-05-30` (1,5–2 h; una petición cada ~2,5 s; reanudable).
2. Configurar grupos, partidos y textos en `scripts/legislaturas.py`.
3. `build_items.py <clave>` y clasificar con el proceso de `data/clasificacion/INSTRUCCIONES.md` (`preparar_lotes.py` → clasificar lotes → `integrar_clasificacion.py`).
4. Si hay Grupo Mixto o Plural: `.venv/bin/python scripts/identificar_mixto.py <clave>` y llevar el partido a `clas_*.json`.
5. `build_data.py <clave>` y `build_page.py`: la legislatura aparece sola en el selector.

Parlamento Europeo: `python3 scripts/descargar_europarlamento.py [--actualizar]` (clave `europarlamento_10`, formato propio declarado con `"formato": "europarlamento"` en `legislaturas.py`); el resto del proceso es igual.

## Metodología resumida

- **Autoría:** proyectos de ley y reales decretos-ley = Gobierno (PSOE–Sumar). Proposiciones con varios grupos cuentan para cada uno. Las del Grupo Mixto aparecen como "Grupo Mixto" porque el Congreso no indica el partido (solo 8 identificadas: campo `partido` en data/clasificacion/congreso_xv/clas_*.json).
- **Votación clave por iniciativa**, por prioridad: votación final (conjunto/dictamen) > convalidación de RDL > toma en consideración > enmienda a la totalidad (en esta, votar sí = oponerse; se invierte).
- **Voto de un partido** = voto mayoritario de sus diputados presentes. Podemos (Belarra, Sánchez Serna, Velarde, Santana), BNG (Rego), CC (Valido), UPN (Catalán) y Compromís (Micó) se separan del Grupo Mixto por voto nominal. Ábalos, Ortega Smith y Verstrynge no se cuentan.
- **Impactos:** clasificación asistida por IA a partir del título, según data/clasificacion/RUBRICA.md. Interpretativa; conviene revisar las de mayor relevancia.
- **Colores:** verde = beneficia algún rasgo del perfil y no perjudica ninguno; rojo = al revés; ámbar = ambas; gris = no afecta. En votos: sí a lo que beneficia o no a lo que perjudica = verde.

## Pendiente (siguientes pasos)

1. **Imagen de previsualización** (Open Graph) y metaetiquetas para compartir en redes y WhatsApp.
2. **Revisar clasificaciones** de las leyes más relevantes (fiscales, vivienda, pensiones, laboral, migración).
3. **Identificar el partido** de las 54 proposiciones del Grupo Mixto (ficha de cada iniciativa en congreso.es, campo de autores/firmantes).
4. **Otras legislaturas**: XIV en descarga; falta configurarla, clasificarla y convertir la clasificación en un proceso repetible.
5. **Leyes ómnibus**: leer el texto (BOE / BOCG) y clasificar medida a medida.

## Publicación

Cada push a `main` que toque `site/` publica la carpeta en GitHub Pages (`.github/workflows/pages.yml`). Los enlaces por perfil usan `?p=asal3,prop1`; `&c=0` desactiva «Ciudadanía general», que está activa por defecto, y `&ds=congreso_xiv` abre otra legislatura (por defecto, la más reciente).

## Fuente y licencia de los datos

Congreso de los Diputados, datos abiertos: https://www.congreso.es/es/opendata — su reutilización exige citar la fuente.

Parlamento Europeo: votaciones nominales de HowTheyVote.eu (https://howtheyvote.eu, datos abiertos con atribución) y títulos y fechas de la API de datos abiertos del Parlamento Europeo (https://data.europarl.europa.eu).
