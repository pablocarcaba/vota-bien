<h1 align="center">¿A quién te conviene votar?</h1>

<p align="center"><b>Lo que votó cada partido en las leyes que tocan tu sueldo, tu casa, tu negocio y tu familia.</b><br>
Leyes y votos reales, de fuentes oficiales · Cálculo trazable ley a ley · Tus respuestas se quedan en tu navegador</p>

<p align="center">
  <a href="https://www.votarbien.info/"><b>Abrir la web →</b></a>
  &nbsp;·&nbsp; <a href="#cómo-funciona">Cómo funciona</a>
  &nbsp;·&nbsp; <a href="#datos-reales-y-trazables">Trazabilidad</a>
  &nbsp;·&nbsp; <a href="#privacidad">Privacidad</a>
  &nbsp;·&nbsp; <a href="#cómo-se-calcula">Cómo se calcula</a>
  &nbsp;·&nbsp; <a href="#reconstruir-los-datos">Reconstruir los datos</a>
  &nbsp;·&nbsp; <a href="#quién-hace-esto">Quién hace esto</a>
  &nbsp;·&nbsp; <a href="#fuentes-y-licencia">Fuentes y licencia</a>
</p>

<p align="center">
  <img alt="11 legislaturas" src="https://img.shields.io/badge/legislaturas-11-C8102E?style=for-the-badge">
  <img alt="5.626 iniciativas" src="https://img.shields.io/badge/iniciativas-5.626-FFC400?style=for-the-badge&labelColor=1d1600">
  <img alt="4.226 votaciones clave" src="https://img.shields.io/badge/votaciones%20clave-4.226-0a0f1c?style=for-the-badge">
  <img alt="Sin dependencias" src="https://img.shields.io/badge/JS-sin%20dependencias-2f7d32?style=for-the-badge">
</p>

<table>
  <tr>
    <td width="72%"><img src=".github/captura-escritorio.jpg" alt="La web en escritorio: el perfil completado en los cuatro pasos y, al lado, el ranking de partidos filtrado por la provincia de Zaragoza"></td>
    <td width="28%"><img src=".github/captura-movil.jpg" alt="El ranking en el móvil, con el filtro por provincia y la nota de cada partido"></td>
  </tr>
</table>

---

## Qué es

Tú madrugas, trabajas y pagas tus impuestos. **Quienes te representan votan leyes.** Esta web te enseña qué votó cada partido cuando se decidía tu sueldo, tu casa, tu negocio y tu familia: no lo que prometió en campaña, sino lo que votó.

> **Tu voto es tuyo.** Aquí nadie te dice a quién votar: te enseñamos lo que votaron. Es un simulador informativo, no una recomendación de voto ni una encuesta.

## Cómo funciona

Un asistente de cuatro pasos. **Tu ranking sale al terminar el paso 3**, para que no veas un resultado con el perfil a medias; el 4 es opcional y solo afina.

| Paso | Qué te pregunta |
|:---:|---|
| **1 · Tú y tu familia** | Tu edad y si tienes hijos menores a cargo. Si quieres, también tu sexo, tu estado civil y si cuidas de una persona dependiente. |
| **2 · Trabajo e ingresos** | De qué vives. Según lo que marques, te pregunta tu tramo de IRPF (con «No lo sé»), tu subgrupo de funcionario, tu empresa y su sector, tu pensión o lo que cobras en paro. Si quieres, también si recibes alguna ayuda social (IMV, bono social…). |
| **3 · Vivienda y ahorros** | Dónde vives, cuántas viviendas tienes, si alquilas alguna, si tienes hipoteca y tus ahorros sin contar tu casa. Si quieres, también si vives en el medio rural. |
| **4 · Salud y situación personal** *(opcional)* | Datos sensibles: orientación, salud o enfermedad crónica, dependencia, discapacidad, origen o minoría y si eres víctima. Nada de este paso va en los enlaces que compartes. |

<p align="center"><img src=".github/captura-perfil.jpg" alt="El asistente del perfil, vacío: el paso 1 abierto con la edad, el sexo, los hijos, el estado civil y si cuidas de alguien, y al lado el aviso de que el resultado sale al completar los tres primeros pasos" width="88%"></p>

Con el perfil hecho:

- **El ranking.** Cada partido saca una nota de −100 a +100 según cómo votó las leyes que afectan a tu perfil, con un **veredicto en palabras** que habla de sus votos, no de sus efectos: «Mayoría clara de votos a tu favor», «Más votos a tu favor que en contra», «Votos repartidos», «Más votos en tu contra que a favor» o «Mayoría clara de votos en tu contra». Leyes económicas y sociales van en pestañas separadas.
- **¿En qué provincia votas?** Junto al ranking eliges tu provincia y ves solo los partidos a los que puedes votar ahí: los de ámbito estatal y los que se presentan en tu provincia o tu comunidad. El filtro solo oculta filas: **no cambia la nota de nadie**. Dónde se presenta cada partido es una asignación nuestra, pública en [`data/ambito_partidos.json`](data/ambito_partidos.json). En las europeas no se aplica, porque España es una circunscripción única.
- **El efecto Gobierno.** Los partidos del Gobierno suelen votar a favor de sus propios reales decretos-ley. En la ficha de cada partido esas leyes van marcadas como **«Iniciativa del Gobierno»**, y en «Ajustar el ranking» la casilla **«Excluir los reales decretos-ley»** (desactivada por defecto) los saca de todas las notas.
- **Ley a ley.** Pulsa un partido y ves cada ley que te afecta, cómo la votó y cuánto suma o resta, con enlace a su ficha oficial.

## Datos reales y trazables

Cada número de la web se puede seguir hasta la ley y la votación de las que sale. Sin cajas negras.

| Qué ves | De dónde sale | ¿Se puede comprobar? |
|---|---|---|
| **Leyes e iniciativas**: título, tipo, autor, fechas, resultado | Datos abiertos del [Congreso](https://www.congreso.es/es/opendata) y del [Parlamento Europeo](https://data.europarl.europa.eu) | Sí: cada ley enlaza a su ficha oficial |
| **Votos**: qué votó cada partido y en qué votación | Votaciones nominales del Pleno (Congreso, actas del PE y [HowTheyVote.eu](https://howtheyvote.eu)) | Sí: votación, fecha y voto de cada partido, ley a ley |
| **A quién afecta cada ley** y su alcance | Clasificación propia, hecha con ayuda de IA según una [rúbrica pública](data/clasificacion/RUBRICA.md) | Sí: está en [`data/clasificacion/`](data/clasificacion), y la web la muestra junto a cada ley |
| **La nota de cada partido** | Se calcula en tu navegador con una fórmula pública | Sí: la ficha del partido desglosa cuánto suma o resta cada ley |

**La cadena completa:** fuente oficial → `data/fuente/` (descarga tal cual) → `data/clasificacion/` (clasificación pública) → `site/data/<legislatura>.json` (lo que carga la web, descargable) → cálculo en tu navegador → desglose ley a ley en la ficha del partido.

**Ejemplo de cómo se rastrea una nota.** Si un partido votó a favor del proyecto de ley de reducción de la jornada laboral ([121/000058](https://www.congreso.es/es/busqueda-de-iniciativas?p_p_id=iniciativas&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_iniciativas_mode=mostrarDetalle&_iniciativas_legislatura=XV&_iniciativas_id=121/000058)) y tu perfil es un asalariado de 20.200–35.200 €:

- **Alcance:** es una gran reforma, así que pesa ×9.
- **Fuerza:** la votación clave fue una enmienda a la totalidad, que vale 0,5.
- **Aportación:** 9 × 0,5 = 4,5 puntos a favor en el cálculo de su nota.

Esa misma línea aparece en la ficha del partido, junto a todas las demás, y la suma de todas da su nota.

> **Lo que es oficial y lo que no.** Las leyes, las fechas y los votos son datos oficiales, sin tocar. Decidir a quién beneficia o perjudica una ley es una interpretación: por eso es pública, sigue una rúbrica fija igual para todos los partidos y se enseña al lado de cada ley para que la juzgues tú. Si ves una mal clasificada, abre un *issue*.

## Privacidad

**No sale de tu dispositivo: tus respuestas se guardan solo en este navegador.**

- Lo que marcas se calcula en tu navegador. No se envía a ningún servidor, no hay registro, ni cookies, ni analítica.
- La web es HTML estático en GitHub Pages; solo descarga los datos públicos de cada legislatura y las tipografías de Google Fonts.
- En tu propio navegador (`localStorage`) se recuerdan tus respuestas del perfil, para no perderlas al recargar, la provincia del filtro y dos preferencias de pantalla (ocultar partidos con pocos datos y pausar la animación). Nada de eso sale de tu dispositivo.
- El botón **«Borrar mis respuestas»** (en la barra de tu perfil y en el pie) borra del navegador el perfil y la provincia y reinicia el asistente.
- Compartir tu perfil es opcional: el enlace lleva en la URL (`?p=…`) los rasgos de los pasos 1 a 3 y tu provincia (`prov=`), y solo lo tiene quien tú se lo pases. Eso incluye sexo (Hombre, Mujer o «Prefiero no decirlo»), estado civil, cuidados, ayuda social y medio rural. **«Otro» en sexo y lo que marques en el paso 4 (orientación, salud, discapacidad, origen y víctimas) nunca van en el enlace**: se quedan en tu navegador. Al copiar el enlace, la web te dice siempre qué lleva.
- Hasta la versión 10, sexo, estado civil, cuidados, medio rural y ayuda social iban en el paso 4, que no viajaba en los enlaces. Si tenías esas respuestas guardadas de entonces, la web no las pone en ningún enlace hasta que confirmas su paso (o vuelves a tocar la pregunta), y te avisa una vez del cambio.

## Qué datos incluye

| Fuente | Legislatura | Iniciativas | Con votación clave |
|---|---|---:|---:|
| Congreso de los Diputados | XV · 2023–2026 | 540 | 213 |
| Congreso de los Diputados | XIV · 2019–2023 | 662 | 284 |
| Congreso de los Diputados | XIII · 2019 | 88 | 2 |
| Congreso de los Diputados | XII · 2016–2019 | 508 | 158 |
| Congreso de los Diputados | XI · 2016 | 51 | 7 |
| Congreso de los Diputados | X · 2011–2015 | 510 | 295 |
| Parlamento Europeo | 10.ª · 2024–2029 (en curso) | 260 | 260 |
| Parlamento Europeo | 9.ª · 2019–2024 | 545 | 545 |
| Parlamento Europeo | 8.ª · 2014–2019 | 949 | 949 |
| Parlamento Europeo | 7.ª · 2009–2014 | 931 | 931 |
| Parlamento Europeo | 6.ª · 2004–2009 | 582 | 582 |

Cada fuente y legislatura es un dataset independiente. Los partidos cambian entre legislaturas, así que **nunca se mezclan**: la web tiene un selector de fuente y otro de legislatura.

## Cómo se calcula

- **Autoría.** Los proyectos de ley y los reales decretos-ley son del Gobierno. Una proposición firmada por varios grupos cuenta para cada uno. Las del Grupo Mixto aparecen como «Grupo Mixto» porque el Congreso no indica el partido, salvo las que se han podido identificar (campo `partido` en `clas_*.json`).
- **Votación clave por iniciativa**, por este orden de prioridad: votación final (de conjunto o del dictamen) > convalidación del real decreto-ley > toma en consideración > enmienda a la totalidad. En la enmienda a la totalidad, votar sí equivale a oponerse a la ley, y se invierte.
- **Voto de un partido** = voto mayoritario de sus diputadas y diputados presentes. Los partidos que comparten grupo, como Podemos, BNG, CC, UPN o Compromís dentro del Mixto, se separan por voto nominal. Los no adscritos no se cuentan.
- **Impactos.** Cada iniciativa se clasifica como económica o social y se marca a qué colectivos beneficia (+1) o perjudica (−1), según [`RUBRICA.md`](data/clasificacion/RUBRICA.md). La clasificación es asistida por IA e **interpretativa**: conviene revisar las leyes de mayor relevancia.
- **Peso de cada voto.** Votar el texto final o la convalidación de un real decreto-ley cuenta 1; la toma en consideración o una enmienda a la totalidad, 0,5; lo que el partido solo presentó y no llegó a votar en el Pleno, 0,25. Las abstenciones no cuentan.
- **Alcance.** Una gran reforma pesa como 9 leyes menores, y una ley relevante como 3.
- **Nota del ranking.** (a favor − en contra) ÷ (total + 9) × 100, de −100 a +100. Los 9 puntos neutros de **prudencia** (el peso de una gran reforma) evitan que un partido con pocas leyes saque una nota extrema: con muchas leyes apenas cuentan; con pocas, acercan la nota a 0. Las leyes mixtas cuentan en el total sin sumar ni restar.
- **Veredicto.** «Votos repartidos» entre −25 y +25 (entre −35 y +35 si el partido tiene menos de 5 leyes que te afecten); «Mayoría clara» solo con ±60 o más y al menos 8 leyes. Con menos de 3 leyes, el partido lleva la etiqueta «pocos datos».
- **Reales decretos-ley.** Cuentan por defecto. La casilla «Excluir los reales decretos-ley» (o `rdl=0` en el enlace) los quita de todas las notas.
- **Provincia.** Filtra qué partidos se ven y recalcula los puestos entre los que quedan, pero no toca ninguna nota.
- **Colores.** Verde: beneficia algún rasgo de tu perfil y no perjudica ninguno. Rojo: al revés. Ámbar: ambas cosas. Gris: no te afecta.

### Estado de la rúbrica

La clasificación sigue la [rúbrica v3](data/clasificacion/RUBRICA.md) ([cambios respecto a la v2](data/clasificacion/RUBRICA_CAMBIOS_v3.md)) en **todas las legislaturas**. Cada ley se lee **tres veces de forma independiente** y un colectivo solo cuenta si lo marcan al menos dos de las tres lecturas (`scripts/consolidar_lecturas.py`). Los lectores son modelos de IA, no personas: no sustituyen a una revisión humana.

| Rúbrica | Legislaturas |
|---|---|
| **v3**, tres lecturas | Congreso XV, XIV, XIII, XII, XI y X · Parlamento Europeo 10.ª, 9.ª, 8.ª, 7.ª y 6.ª |

**Excepción en el Parlamento Europeo 6.ª y 7.ª.** La API oficial casi no publica el texto aprobado en español de esas legislaturas, así que se leyeron por el título del procedimiento. Las normas que la v3 dejaba sin efectos solo por no tener texto (80 en la 6.ª y 124 en la 7.ª) conservan la clasificación anterior. Están listadas en el `REVISION.md` de cada legislatura: [6.ª](data/clasificacion/europarlamento_6/REVISION.md) y [7.ª](data/clasificacion/europarlamento_7/REVISION.md).

Las tres lecturas y lo que cambió en cada ley están en `data/clasificacion/<clave>/lectura_v3/` (por ejemplo, [`congreso_xv/lectura_v3/CAMBIOS.md`](data/clasificacion/congreso_xv/lectura_v3/CAMBIOS.md)). En la XV, ninguna de las 540 iniciativas tiene signo contrario entre lecturas, 432 coinciden en las tres y el parecido medio es de 0,90; las 108 en las que no coinciden del todo pasan a revisión humana.

### Prueba de sesgo

Una herramienta neutral debería dar el primer puesto a partidos distintos según el perfil. `scripts/prueba_sesgo.py` genera 2.000 perfiles aleatorios y 20 arquetipos, calcula su ranking con el mismo cálculo que la web en cada legislatura y pestaña, con y sin «Ciudadanía general», y cuenta en qué porcentaje de perfiles sale primero cada partido. La prueba incluye también el camino «No lo sé» del tramo de IRPF: una cuarta parte de los asalariados y funcionarios aleatorios lo marca, y se calcula igual que en la web. El resultado completo se publica tal cual sale en [`data/analisis/SESGO.md`](data/analisis/SESGO.md). Algunas cifras:

- **Congreso, XV, leyes económicas con «Ciudadanía general»:** CC sale primero en el 42,4 % de los perfiles, PNV en el 30,6 % y PSOE en el 11,4 %.
- **Parlamento Europeo, leyes económicas:** en la 10.ª, BNG (46,7 %) con «Ciudadanía general» y PP (28,1 %) sin ella; en la 9.ª, PSOE (60,2 %) con ella y PP (24,6 %) sin ella.
- **Congreso, X, leyes económicas con «Ciudadanía general»:** PNV sale primero en el 55,9 % de los perfiles, UPN en el 27,0 % y CiU en el 5,5 %.
- **Parlamento Europeo 8.ª, 7.ª y 6.ª, leyes económicas con «Ciudadanía general»:** en la 8.ª, PNV (88,4 %); en la 7.ª, ICV (70,4 %); en la 6.ª, PSOE (65,2 %).
- **Legislaturas con pocas votaciones:** el resultado se concentra; en la XI, en leyes sociales, PSOE sale primero en el 100,0 % de los perfiles.
- **También hay concentraciones altas con muchas votaciones:** en la X, en leyes sociales con «Ciudadanía general», NC sale primero en el 97,8 % de los perfiles.

*Interpretación nuestra:* los partidos bisagra, con pocas votaciones en contra, tienden a salir arriba.

La metodología completa está en la propia web, en el apartado **Cómo se calcula**.

## Reconstruir los datos

```bash
python3 scripts/build_items.py congreso_xv       # fuente → items normalizados
python3 scripts/validar_clasificacion.py         # tiene que dar 0 errores
python3 scripts/build_data.py congreso_xv        # items + clasificación + votos → site/data
python3 scripts/build_page.py                    # template.html → index.html
```

`build_data.py` imprime las votaciones que reasigna, porque la web del Congreso no siempre indica el expediente de cada votación y se comprueba comparando títulos. La página carga los datos con `fetch`, así que en local tienes que servirla:

```bash
python3 -m http.server 8000 --directory site    # http://localhost:8000
```

<details>
<summary><b>Añadir una legislatura</b></summary>

1. **Descargar:** `python3 scripts/descargar_legislatura.py --leg XIV --desde 2019-12-03 --hasta 2023-05-30`. Tarda entre 1,5 y 2 h (una petición cada ~2,5 s) y se puede reanudar.
2. **Configurar** grupos, partidos y textos en `scripts/legislaturas.py`.
3. **Clasificar:** `build_items.py <clave>` y después el proceso de [`INSTRUCCIONES.md`](data/clasificacion/INSTRUCCIONES.md): `preparar_lotes.py` → clasificar los lotes → `integrar_clasificacion.py`.
4. **Grupo Mixto o Plural:** `.venv/bin/python scripts/identificar_mixto.py <clave>` y llevar el partido a `clas_*.json`.
5. **Publicar:** `build_data.py <clave>` y `build_page.py`. La legislatura aparece sola en el selector.

**Parlamento Europeo:** `python3 scripts/descargar_europarlamento.py [--actualizar]` para la 9.ª y la 10.ª, y `scripts/descargar_europarlamento_historico.py` para la 6.ª, 7.ª y 8.ª. Usan un formato propio, declarado con `"formato": "europarlamento"` en `legislaturas.py`; el resto del proceso es igual.

> **Aviso:** congreso.es tiene protección anti-bots. Nunca lances peticiones en paralelo, deja una cada 2-3 s y para ante un 403.

</details>

<details>
<summary><b>Estructura del repositorio</b></summary>

```
data/
  fuente/                       Datos de origen, uno por dataset (no se editan)
  clasificacion/
    RUBRICA.md                  Criterios de clasificación (v3), comunes a todas las legislaturas
    RUBRICA_CAMBIOS_v3.md       Qué cambió de la v2 a la v3
    INSTRUCCIONES.md            Proceso para clasificar lotes
    PROMPT_LECTOR.md            Texto literal con el que se lanza cada lector independiente de la reclasificación
    <clave>/clas_*.json         Tipo, impactos por colectivo (+1/−1) y nota de cada iniciativa
    <clave>/REVISION.md         Casos dudosos pendientes de revisión
    <clave>/lectura_v3/         Las tres lecturas independientes y CAMBIOS.md (legislaturas con la v3)
  analisis/SESGO.md             Prueba de sesgo (generada por prueba_sesgo.py)
  ambito_partidos.json          Dónde se presenta cada partido (filtro por provincia)
  generado/<clave>/items.json   Iniciativas normalizadas (generado; no editar)
  cache/                        Respuestas de congreso.es (ignorado por git)
scripts/
  legislaturas.py               Configuración por legislatura: grupos, partidos, textos
  descargar_legislatura.py      Iniciativas y votaciones del Pleno del Congreso (reanudable)
  descargar_historico.sh        Descarga en serie de las legislaturas X–XIII
  descargar_europarlamento.py   Parlamento Europeo 9.ª y 10.ª: procedimientos y voto de las eurodiputadas y los eurodiputados de España
  descargar_europarlamento_historico.py  Parlamento Europeo 6.ª a 8.ª (actas oficiales del PE y Parltrack)
  identificar_mixto.py          Partido de las proposiciones del Mixto y del Plural (por el BOCG)
  textos_bocg.py                Texto de iniciativas concretas para revisar su clasificación
  textos_boe.py                 Texto de los reales decretos-ley en el BOE (por ELI)
  agrupar_temas.py              Iniciativas con el mismo contenido (temas.json): cuentan una vez
  consolidar_medidas.py         Mayoría de 3 lecturas en la ronda de leyes ómnibus (medidas)
  build_items.py                fuente → items.json
  build_data.py                 items + clasificación + votaciones → site/data/<clave>.json
  build_page.py                 template.html + catálogo de datasets → index.html
  preparar_lotes.py             Lotes de iniciativas sin clasificar
  integrar_clasificacion.py     Integra lotes, armoniza RDL duplicados y valida
  validar_clasificacion.py      Comprueba clas_*.json contra la rúbrica y la web
  comparar_lecturas.py          Compara lecturas independientes de una legislatura
  consolidar_lecturas.py        Consolida tres lecturas por mayoría (2 de 3)
  lotes_reclasificacion.py      Reclasificación, paso 1: lotes con el texto oficial de cada iniciativa (y segunda ronda)
  aplicar_reclasificacion.py    Reclasificación, paso 5: combina las rondas, consolida por mayoría y lo lleva al repo
  cerrar_reclasificacion.py     Reclasificación, paso 6: cierra tras aplicar una o varias legislaturas
  prueba_sesgo.py               Prueba de sesgo: qué partido sale primero en miles de perfiles
tests/                          Tests de los scripts (los ejecuta la CI antes de publicar)
site/
  template.html                 La página: HTML/CSS/JS sin dependencias (solo Google Fonts)
  index.html                    Página final (generada)
  data/<clave>.json             Un dataset por fuente y legislatura
```

</details>

## Publicación

Cada push a `main` que toque `site/` publica la carpeta en GitHub Pages (`.github/workflows/pages.yml`).

Los enlaces se pueden compartir con un perfil ya marcado:

| Parámetro | Qué hace | Ejemplo |
|---|---|---|
| `p` | Rasgos del perfil, separados por comas (los de los pasos 1 a 3; la web nunca pone en el enlace los del paso 4: orientación, salud, discapacidad, origen y víctimas) | `?p=asal3,prop1` |
| `u` | Respuestas del asistente que no son rasgos (de qué vives, dónde vives…); la web lo añade junto a `p`, sin «Otro» en sexo | `?p=asal3&u=trAjena` |
| `prov` | Filtra el ranking por provincia (código INE de dos cifras) | `?p=asal3&prov=50` |
| `rdl=0` | Excluye los reales decretos-ley del cálculo (por defecto se cuentan) | `?p=asal3&rdl=0` |
| `c=0` | Desactiva «Ciudadanía general», que viene activa | `?p=asal3&c=0` |
| `co=0` | Desactiva las leyes de consumo, que vienen activas | `?p=asal3&co=0` |
| `t=soc` | Abre la pestaña de leyes sociales | `?p=asal3&t=soc` |
| `partido` | Abre la ficha de un partido | `?p=asal3&partido=PP` |
| `ds` | Abre otra legislatura (por defecto, la más reciente) | `?ds=congreso_xiv` |

## Pendiente

- [x] **Reclasificar con la rúbrica v3:** hecho en todas las legislaturas. En el Parlamento Europeo 6.ª y 7.ª, 80 y 124 normas sin texto oficial en español conservan la clasificación anterior ([ver arriba](#estado-de-la-rúbrica)).
- [ ] **Revisar 13 iniciativas con `desSub` que tratan del IMV o de ingresos mínimos** (apuntadas en el `REVISION.md` de cada legislatura del Congreso, de la X a la XV): la rúbrica reserva `desSub` para el subsidio por desempleo.
- [ ] **Revisar las clasificaciones** de las leyes más relevantes: fiscales, vivienda, pensiones, laboral, migración.
- [x] **Identificar el partido** de las proposiciones del Grupo Mixto y del Grupo Plural: hecho en 169 de 185 (122/000033 de la X ya está asignada al BNG). Las 16 restantes son, en su mayoría, iniciativas inadmitidas o retiradas sin texto publicado, y el BOCG no dice quién las firma (`data/clasificacion/<clave>/partidos_mixto.json`).
- [x] **Convertir la clasificación en un proceso repetible** entre legislaturas: [`scripts/lotes_reclasificacion.py`](scripts/lotes_reclasificacion.py), [`scripts/aplicar_reclasificacion.py`](scripts/aplicar_reclasificacion.py), [`scripts/cerrar_reclasificacion.py`](scripts/cerrar_reclasificacion.py) y [`data/clasificacion/PROMPT_LECTOR.md`](data/clasificacion/PROMPT_LECTOR.md).
- [x] **Leyes ómnibus:** clasificadas medida a medida (campo `medidas`, rúbrica 3.8) con el texto del BOCG o del BOE y tres lecturas independientes (`scripts/consolidar_medidas.py`).

## Quién hace esto

Lo hacemos **Pablo Carcaba** y **Nacho Rodríguez**, desarrolladores profesionales. No tenemos vínculos con ningún partido político y el proyecto no tiene financiación: ni pública, ni privada, ni de partidos. Todo es público: el código, los datos y la clasificación están en este repositorio.

¿Ves un error o una ley mal clasificada? [Abre un *issue*](https://github.com/pablocarcaba/vota-bien/issues). Cada ley tiene también en la web su propio enlace «¿Está mal clasificada?».

## Fuentes y licencia

- **Congreso de los Diputados**, datos abiertos: <https://www.congreso.es/es/opendata>. Su reutilización exige citar la fuente.
- **Textos oficiales para clasificar:** Boletín Oficial de las Cortes Generales (BOCG, en las fichas del Congreso) y, para los reales decretos-ley, [Boletín Oficial del Estado](https://www.boe.es) (BOE, por su identificador ELI; `scripts/textos_boe.py`). Los textos se guardan en la caché local y no se publican.
- **Parlamento Europeo:** votaciones nominales de [HowTheyVote.eu](https://howtheyvote.eu) (9.ª y 10.ª, datos abiertos con atribución) y de las actas oficiales del Parlamento Europeo (6.ª a 8.ª); títulos y fechas de la [API de datos abiertos del Parlamento Europeo](https://data.europarl.europa.eu). Para la 6.ª, también [Parltrack](https://parltrack.org) (ODbL 1.0).

La clasificación de impactos es propia e interpretativa. Si ves una ley mal clasificada, abre un *issue*.

El código es software libre con [licencia MIT](LICENSE). Los datos de origen pertenecen a sus editores y su reutilización exige citar la fuente.
