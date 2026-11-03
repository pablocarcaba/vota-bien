# ¿Quién legisla para ti?

Herramienta web que permite a cualquier persona marcar su perfil (tramo de IRPF, funcionario, pensionista, propietario, empresario, colectivos sociales…) y ver qué partidos presentaron y votaron leyes que le benefician o perjudican.

Piloto: XV legislatura del Congreso de los Diputados (17/08/2023 – disolución 06/10/2026). Datos descargados el 02/11/2026.

## Estructura

```
data/
  fuente/                 Datos de origen (no se regeneran)
    congreso_xv.json        Datos brutos del Congreso (iniciativas + 315 votaciones clave + índice de 2.175 votaciones)
    votos_extra.json        38 votaciones finales que faltaban en la primera pasada (resumidas por grupo)
  clasificacion/          Clasificación de impactos (editable, siguiendo la rúbrica)
    RUBRICA.md              Criterios de clasificación. Cualquier reclasificación debe seguirla
    clas_0..4.json          Clasificación de cada iniciativa: tipo (eco/soc), impactos por colectivo (+1/-1), nota
    lotes/chunk_0..4.json   Lotes de iniciativas enviados a clasificar (histórico, no los usa ningún script)
  generado/               Salida de los scripts; no editar a mano
    items.json              Las 540 iniciativas normalizadas (build_items.py)
    dataset.json            Dataset final que consume la web (build_data.py)
scripts/
  scrape_congreso.py    Descarga desde congreso.es (SIN PROBAR fuera de Chrome; ver avisos dentro)
  build_items.py        congreso_xv.json -> items.json
  build_data.py         items + clasificación + votaciones -> dataset.json
  build_page.py         template.html + dataset.json -> site/index.html
site/
  template.html         Página (HTML/CSS/JS sin dependencias, salvo Google Fonts)
  index.html            Página final con los datos incrustados (lista para GitHub Pages)
```

## Reconstruir

```
python3 scripts/build_items.py data/fuente/congreso_xv.json data/generado/items.json
python3 scripts/build_data.py
python3 scripts/build_page.py
```

`build_data.py` imprime las votaciones que reasigna (la web del Congreso no siempre indica el expediente de cada votación; se comprueba comparando títulos).

## Metodología resumida

- **Autoría:** proyectos de ley y reales decretos-ley = Gobierno (PSOE–Sumar). Proposiciones con varios grupos cuentan para cada uno. Las del Grupo Mixto aparecen como "Grupo Mixto" porque el Congreso no indica el partido (solo 8 identificadas: campo `partido` en data/clasificacion/clas_*.json).
- **Votación clave por iniciativa**, por prioridad: votación final (conjunto/dictamen) > convalidación de RDL > toma en consideración > enmienda a la totalidad (en esta, votar sí = oponerse; se invierte).
- **Voto de un partido** = voto mayoritario de sus diputados presentes. Podemos (Belarra, Sánchez Serna, Velarde, Santana), BNG (Rego), CC (Valido), UPN (Catalán) y Compromís (Micó) se separan del Grupo Mixto por voto nominal. Ábalos, Ortega Smith y Verstrynge no se cuentan.
- **Impactos:** clasificación asistida por IA a partir del título, según data/clasificacion/RUBRICA.md. Interpretativa; conviene revisar las de mayor relevancia.
- **Colores:** verde = beneficia algún rasgo del perfil y no perjudica ninguno; rojo = al revés; ámbar = ambas; gris = no afecta. En votos: sí a lo que beneficia o no a lo que perjudica = verde.

## Pendiente (siguientes pasos)

1. **Publicar en GitHub Pages**: crear repositorio, subir `site/index.html` (renombrar o configurar Pages para servir `site/`). El enlace por perfil usa `?p=asal3,prop2`, que funciona en GitHub Pages.
2. **Imagen de previsualización** (Open Graph) y metaetiquetas para compartir en redes y WhatsApp.
3. **Revisar clasificaciones** de las leyes más relevantes (fiscales, vivienda, pensiones, laboral, migración).
4. **Identificar el partido** de las 54 proposiciones del Grupo Mixto (ficha de cada iniciativa en congreso.es, campo de autores/firmantes).
5. **Separar `dataset.json`** de la página si crece (cargarlo con `fetch` desde Pages).
6. **Ampliar a otras legislaturas**: para legislaturas cerradas, el Congreso no publica el fichero de iniciativas; habría que reconstruirlas a partir de las votaciones o del buscador de iniciativas.

## Fuente y licencia de los datos

Congreso de los Diputados, datos abiertos: https://www.congreso.es/es/opendata — su reutilización exige citar la fuente.
