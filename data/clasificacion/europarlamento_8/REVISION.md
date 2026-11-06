# Clasificaciones pendientes de revisión (Parlamento Europeo, 8.ª legislatura)

Clasificación inicial de 949 procedimientos legislativos (2014–2019) con la rúbrica vigente, por agentes. Los colectivos se aplican al efecto previsible en España. Solo hay votaciones nominales: los procedimientos aprobados a mano alzada no aparecen. Para cerrar un caso: corrige `clas_*.json` (o confirma que está bien) y marca la casilla.

## 1. Criterios por unificar entre legislaturas europeas

- [x] **Atún rojo y planes de pesca**: unos van vacíos (atún rojo 2009/0116, 2011/0144; en la 9.ª 2019/0272) y otros con `+ciud -secPrim` (2007/0058; en la 9.ª 2022/0111). Elegir un criterio. — Aplicada (06/11/2026): criterio común fijado: un plan con límites de capturas conocidos lleva `+ciud -secPrim`; una modificación sin contenido conocido, `{}`; solo obligaciones de registro, `-secPrim`. La 8.ª ya lo cumple: planes 2016/0074, 2018/0050, 0069, 0074 y 0109 con `+ciud -secPrim`; la adaptación del atún rojo 2015/0096, `{}`. Sin cambios en la 8.ª; lo de 6.ª 2004/0229 y 2008/0063 lo aplica el agente de la 6.ª.
- [x] **Asilo**: las normas que añaden garantías (Dublín III, procedimientos de asilo 2009/0165, acogida) llevan `+inmigrantes` y las restrictivas (sustituto de Dublín de la 9.ª, Dublín 2016/0133) `-inmigrantes`. Revisar el conjunto. — Resuelta (06/11/2026): v3 coherente con 3.7 y 3.1.1: las garantistas llevan `+inmigrantes` (Dublín III 2008/0243, acogida 2008/0244, procedimientos 2009/0165); los paquetes mixtos van vacíos (8.ª Dublín 2016/0133, 9.ª 2016/0222, 2016/0224A y 2020/0279); las restricciones puras llevan `-inmigrantes` (10.ª 2025/0101 y 2025/0132).
- [x] **Acuerdos comerciales con competencia agrícola** (Marruecos, Colombia y Perú, Centroamérica, Ecuador, SADC, Ucrania, Moldavia): casi todos vacíos, algunos con `-secPrim` (Marruecos 2010/0248, aceite tunecino 2015/0218) y Japón con `+secPrim`. Misma duda abierta en la 9.ª. — Aplicada (06/11/2026): criterio común fijado: `{}`, peso 1. La 8.ª ya lo cumple (todos `{}`, peso 1; las cláusulas de salvaguardia mantienen `+secPrim`). Sin cambios en la 8.ª; 7.ª 2010/0248 lo aplica el agente de la 7.ª.
- [x] **Liberalizaciones** (ferrocarril, correos, asistencia en tierra, autobuses, navegación aérea): `-ciud +secTrans` por la regla 3.2. — Aplicada (06/11/2026): criterio común fijado: sin `ciud` y con el efecto sectorial. La 8.ª ya lo cumple (2013/0157 y 2017/0288, `{}` por signos opuestos entre operadores). Sin cambios en la 8.ª; 7.ª 2013/0028, 0029 y 0186 los aplica el agente de la 7.ª.
- [x] **Presupuestos en dos procedimientos** (2011, 2013) con peso 3 cada uno: cuentan doble, como 2021 en la 9.ª. — Aplicada (06/11/2026): criterio común fijado: presupuestos anuales y MFF `{}`, peso 1, con los procedimientos del mismo presupuesto agrupados. La 8.ª ya lo cumple: un procedimiento por ejercicio, todos `{}`, peso 1, y MFF 2015/0010, 2016/0283 y 2018/0166R `{}`, peso 1. Sin cambios en la 8.ª; el 2011 de la 7.ª lo aplica el agente de la 7.ª.
- [x] **Arbitrio canario (AIEM)**: `+secInd` sin `-cons`. — Aplicada (06/11/2026): criterio común `+secInd`, sin `-cons`. 8.ª 2018/0417: `{}` → `{"secInd":1}`, peso 1. La 7.ª ya lo llevaba.
- [x] **Clasificación por la posición del Parlamento**: tiempo de trabajo (2004/0209) y propuestas no adoptadas o retiradas se clasifican por su contenido. — Resuelta (06/11/2026): coherente con 3.8 («las proposiciones se pesan por lo que proponen»): 6.ª 2004/0209 `+asal1-4 +proSan -empAut/Micro/Peq`, peso 2, y 8.ª 2017/0288 clasificada por su contenido (vacía por signos opuestos). La nota de 2004/0209 todavía dice «no se aprobó», contra la regla 4.

## 2. Casos señalados al clasificar


### lotes 00-01 (166/200 vacías)

- [x] 2010/0208 transgénicos vacía — Resuelta (06/11/2026): v3: `{}`. La restricción del cultivo depende de lo que decida cada Estado (P2); coherente con 2015/0093.
- [x] 2011/0023 PNR vacía peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1 (3.8: sin impactos → peso 1).
- [x] 2013/0157 puertos -ciud +secTrans — Obsoleta (06/11/2026): el `-ciud` venía de la regla «lo público frente a lo privado», retirada de 3.2. v3: `{}` (operadores con signos opuestos).
- [x] 2013/0402 secretos comerciales +emp peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1. Signo no determinable con el texto disponible (P4).
- [x] 2013/0390 gente de mar +asal1-4 -secTrans — Resuelta (06/11/2026): v3: `{}`. Solo afecta a una profesión, no a todos los asalariados (3.3.1), y es coherente con las normas laborales del transporte de la 8.ª (2017/0121, 2017/0122 y 2017/0123 vacías).
- [x] 2013/0436 descartes vacía — Resuelta (06/11/2026): v3: `{}`. Adapta el control y las medidas técnicas a la obligación de desembarque, con exigencias y flexibilidades a la vez (3.1.1).
- [x] 2013/0435 nuevos alimentos +secInd — Resuelta (06/11/2026): v3: `{}`. La autorización de nuevos alimentos tiene un signo no determinable para la industria (P4).
- [x] 2014/0100 ecológica +cons — Resuelta (06/11/2026): v3: `{}`. El etiquetado de alimentos no es un suministro (3.5.1) y para los productores el signo es mixto.
- [x] 2013/0314 índices +cons +hipot -secFin — Resuelta (06/11/2026): v3: `{}`. El efecto sobre `hipot` exige dos «porque» (P3) y el texto no fija el signo para el sector.
- [x] 2014/0121 accionistas -empGran — Resuelta (06/11/2026): v3: `{}`. Da derechos a los accionistas e impone obligaciones a las cotizadas: signo no determinable (P4).
- [x] 2013/0306, 2014/0017 fondos monetarios vacías — Resuelta (06/11/2026): v3 confirma `{}` en las dos: normas técnicas de los mercados financieros (3.1.1).
- [x] protocolos contaminación (2013/0448, 2014/0358, 0359) vacías vs techos 2013/0443 +ciud — Aplicada (06/11/2026): 2014/0358 y 2014/0359: `{}` → `{"ciud":1}`, peso 1, como 2013/0448 (enmiendas que endurecen el Protocolo de 1998, 3.2).
- [x] comercio Ecuador/Ucrania/Moldavia (2014/0287, 0279, 0250, 2013/0151A/B) vacías — Resuelta (06/11/2026): v3 confirma `{}` en las cinco, coherente con el resto de acuerdos comerciales de la 8.ª (la competencia depende del mercado, P2).
- [x] 2014/2062 FEAG CyL +desPres — Aplicada (06/11/2026): 2016/2298: `{"desPres":1}` → `{}` (despedidos de una empresa o región; no consta prestación). 2017/2079 conserva `+jovenes`, porque nombra a los jóvenes ninis. 2014/2062, 2014/2054, 2014/2064 y 2018/2014 siguen `{}`.
- [x] 2012/0288 ILUC +ciud -secInd — Resuelta (06/11/2026): v3 confirma `+ciud -secInd`, peso 2: endurece la protección climática y el sector de biocarburantes lo cumple (3.2).


### lotes 02-03 (148/200 vacías)

- [x] 2015/0009 FEIE +empMicro/Peq/Med peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1. Las ayudas llegan a través de intermediarios y convocatorias (P2).
- [x] 2015/0093 transgénicos vacía — Resuelta (06/11/2026): v3: `{}`, coherente con 2010/0208 (depende de cada Estado, P2).
- [x] 2015/0112 banano Colombia/Perú +secPrim — Resuelta (06/11/2026): v3 confirma `+secPrim`: cláusula de salvaguardia que protege directamente a los productores. Es coherente con 7.ª 2011/0262 y 2011/0263 y con 10.ª 2025/0322.
- [x] 2015/0218 aceite tunecino -secPrim — Resuelta (06/11/2026): v3: `{}`, coherente con el resto de medidas comerciales de la 8.ª (la competencia depende del mercado, P2).
- [x] SADC 2016/0005 y Ecuador 2016/0092 vacías — Resuelta (06/11/2026): v3 confirma `{}` en las dos (acuerdos comerciales, P2).
- [x] titulización/capital 2015/0225-0226 +secFin — Resuelta (06/11/2026): v3: `{}` en las dos. Requisitos técnicos de signo no determinable para el sector (P4).
- [x] folletos 2015/0268 +empPeq/Med — Resuelta (06/11/2026): v3: `{}`. Reglamento técnico de valores sin un signo claro por tamaño de empresa.
- [x] armas de fuego 2015/0269 vacía peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1 (3.8: sin impactos → peso 1).
- [x] RCDE fase IV 2015/0148 +ciud -secInd peso 2 (¿3? ¿-cons?) — Resuelta (06/11/2026): v3: `+ciud`, peso 2. `secInd` se retira por signos opuestos (más exigencia y asignación gratuita, 3.1.1); `cons` no (3.5.1); peso 3 no, porque no figura en el paso 1 de 3.8.
- [x] desplazados 2016/0070 +asal1/2 -secCons peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1. Los trabajadores desplazados no son el conjunto de los asalariados (3.3.1), y el efecto sobre la construcción depende de las empresas (P2).
- [x] Dublín 2016/0133 -inmigrantes — Resuelta (06/11/2026): v3: `{}`, coherente con los paquetes de asilo de signo mixto (9.ª 2020/0279 y 2016/0224A); ver «Asilo».
- [x] reubicaciones (2015/0125, 0209, 2016/0089) y presupuestos de refugiados (2015/2121, 2252, 2253, 2264) +inmigrantes — Resuelta (06/11/2026): v3: las reubicaciones mantienen `+inmigrantes` (amplían la acogida, 3.7) y los presupuestos de refugiados 2015/2121, 2252, 2253 y 2264 pasan a `{}` (mezclan gasto de fronteras y de acogida).
- [x] pesca técnica 2016/0074 y flota exterior 2015/0289 +ciud -secPrim — Resuelta (06/11/2026): v3: 2016/0074 `+ciud -secPrim`, coherente con los planes de la 8.ª (2018/0050, 0069, 0074, 0109); 2015/0289 `{}` (regula autorizaciones, no límites de capturas).
- [x] 700 MHz 2016/0027 vacía — Resuelta (06/11/2026): v3 confirma `{}`: televisión y telecomunicaciones (ambas `secDig`) tienen signos opuestos (3.1.1).
- [x] INL 2015/2010 -empGran, 2015/2085 +discapacidad +depend, 2015/2086 +infancia, 2015/2087 +victimas — Aplicada (06/11/2026): 2015/2085: `{"discapacidad":1,"mayores":1}` → `{"discapacidad":1}` (el texto se refiere a adultos vulnerables sin tramo de edad, 3.7).


### lotes 08-09 (114/149 vacías)

- [x] 2018/0161 CCP exención fabricación +secInd +pac (en 9.ª CCP vacíos) — Resuelta (06/11/2026): v3: `{}`, igual que los CCP de la 9.ª (2023/0127 y 2023/0130): los fabricantes de genéricos ganan y los de originales pierden (3.1.1), y `pac` depende del mercado (P2).
- [x] 2018/0166R informe provisional MFF como presupuesto peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1.
- [x] 2018/0169 reutilización agua +ciud +secPrim — Resuelta (06/11/2026): v3: `+ciud`, peso 1 (mejora ambiental del agua, 3.2); `secPrim` se retira.
- [x] taxonomía 2018/0178 +ciud -secFin peso 2 y divulgación 2018/0179 +cons -secFin — Resuelta (06/11/2026): v3: taxonomía 2018/0178 `{}`, peso 1 (es un marco de clasificación); divulgación 2018/0179 `-secFin`, peso 1, sin `cons` (3.5.1).
- [x] Europa Creativa 2018/0190 +secDig — Resuelta (06/11/2026): v3: `{}`. Programa de financiación por convocatorias (P2).
- [x] RDC 2018/0196 vacía peso 2 vs FEDER/FSE+ con impactos — Resuelta (06/11/2026): v3: RDC `{}`, peso 1 (disposiciones comunes de procedimiento), y FEDER 2018/0197 también `{}`. Solo llevan impactos los fondos con destinatario definido (FSE+ 2018/0206 `+pobreza`, FEMPA 2018/0210 `+secPrim`).
- [x] Marruecos-Sáhara 2018/0256/0256M vacías (¿-secPrim?) — Resuelta (06/11/2026): v3 confirma `{}` en las dos, coherente con los acuerdos comerciales de la 8.ª (sin `-secPrim`, P2).
- [x] Frontex 2018/0330 -inmigrantes peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1. Es una agencia de fronteras: norma institucional sin un cambio de derechos conocido (3.7).
- [x] contenidos terroristas 2018/0331 -secDig peso 2 — Resuelta (06/11/2026): v3 confirma `-secDig`, peso 2: obligación directa a los proveedores de alojamiento, coherente con 9.ª 2020/0361.
- [x] arbitrio canario 2018/0417 +secInd — Aplicada (06/11/2026): `{}` → `{"secInd":1}`, peso 1 (criterio común del AIEM; coherente con 7.ª 2010/0359).
- [x] FSUE incendios 2017 (2018/2029 + 2030) cuentan doble — Aplicada (06/11/2026): 2018/2029 y 2018/2030 agrupadas en temas.json (las dos `{"victimas":1}`, peso 1): cuentan una vez.
- [x] visados humanitarios 2018/2271 peso 1 — Resuelta (06/11/2026): peso 1, agrupada con 2017/2270 en temas.json (`+inmigrantes` en las dos).
- [x] mercado único 2018/0231 +empMicro/Peq (sucesor 10.ª vacío) — Resuelta (06/11/2026): v3: `+empMicro +empPeq +empMed`, peso 1 (nombra a las pymes, 3.4.2). La sucesora de la 10.ª (2025/0590) solo tiene título y por eso va vacía (3.9): no es incoherente.
- [x] Brexit: Erasmus 2019/0030 y FSE juvenil 2019/0027 con impacto, conexiones aéreas 2018/0433 vacía — Resuelta (06/11/2026): v3 coherente: Erasmus `+estud` y FSE juvenil `+jovenes` nombran a su colectivo; las conexiones aéreas 2018/0433 no nombran a ninguno y van `{}`.


### lotes 04-05 (140/200 vacías)

- [x] París 2016/0184 vacía peso 2 — Resuelta (06/11/2026): v3: `+ciud`, peso 1 (protección climática, 3.2).
- [x] CETA 2016/0205 +secInd +empGran — Resuelta (06/11/2026): v3: `{}`, coherente con los acuerdos comerciales de la 8.ª (P2).
- [x] derechos de autor 2016/0280 solo +estud +proDoc — Resuelta (06/11/2026): v3: `{}` (signos opuestos para plataformas, editores y creadores, 3.1.1).
- [x] BICCIS 2016/0336-0337 -empGran — Resuelta (06/11/2026): v3: `{}` en las dos. Con una base común, el signo de la carga para cada empresa no se conoce (P4).
- [x] 2016/0338 +empGran, 0339 -empGran — Resuelta (06/11/2026): v3: `{}` en las dos: 0338 es procedimental y 0339 regula una práctica fiscal sin distinguir tamaños (3.4.2).
- [x] MFF 2016/0283 +jovenes — Resuelta (06/11/2026): v3: `{}` (ajuste presupuestario institucional).
- [x] audiovisual 2016/0151 +infancia -secDig — Resuelta (06/11/2026): v3: `{}`. Para el sector audiovisual hay exigencias y flexibilidades publicitarias a la vez (3.1.1).
- [x] edificios 2016/0381 +ciud +secCons — Resuelta (06/11/2026): v3: `+ciud`, peso 2; `secCons` se retira (P2).
- [x] renovables 2016/0382 +ciud +cons — Resuelta (06/11/2026): v3: `+ciud`, peso 2; `cons` se retira.
- [x] IVA e-commerce 2016/0370 +secCom -cons — Resuelta (06/11/2026): v3: `+empMicro`, peso 2 (umbral que exime a las microempresas, 3.4.2). `secCom` y `cons` no: la competencia depende del mercado y no es un suministro (3.5.1).
- [x] aviación RCDE 2017/0017 como rebaja — Resuelta (06/11/2026): v3: `{}` por signos opuestos (prórroga de la exclusión de vuelos y factor de reducción lineal, 3.1.1). La 7.ª 2013/0344, que solo prorroga, lleva `-ciud +secTrans`: coherente.
- [x] conciliación 2017/0085 +infancia +mujeres +hombres +depend — Resuelta (06/11/2026): v3 confirma `+infancia +mujeres +hombres +depend`, peso 2. Encaja con 5.3; `depend` procede porque incluye el permiso de cuidadores.
- [x] conductores desplazados 2017/0121 +asal1/2 -secTrans — Resuelta (06/11/2026): v3: `{}`. Afecta a una profesión, no a los tramos `asal` (3.3.1), y tiene signo mixto para los operadores.
- [x] euroviñeta 2017/0115 +secTrans — Resuelta (06/11/2026): v3: `{}`. La rebaja depende de cada Estado (P2).
- [x] SIS retorno 2016/0407 -inmigrantes — Resuelta (06/11/2026): v3 confirma `-inmigrantes`, peso 1 (refuerza la ejecución del retorno de los irregulares, 3.7).
- [x] aceite 2017/0107 y Europass 2016/0304 vacías — Resuelta (06/11/2026): v3 confirma `{}` en las dos.


### lotes 06-07 (147/200 vacías)

- [x] movilidad 2017/0122-0123 solo -secTrans — Resuelta (06/11/2026): v3: `{}` en las dos (signo mixto para operadores y conductores).
- [x] autobuses larga distancia 2017/0288 -ciud +secTrans (no adoptada) — Obsoleta (06/11/2026): el `-ciud` venía de la regla «lo público frente a lo privado», retirada de 3.2. v3: `{}` (operadores establecidos y nuevos con signos opuestos).
- [x] DAC6 2017/0138 -empGran — Resuelta (06/11/2026): v3: `{}`. La obligación de comunicar no distingue tamaños (3.4.2).
- [x] PEPP 2017/0143 +secFin +cons — Resuelta (06/11/2026): v3: `{}`.
- [x] agua de consumo 2017/0332 +ciud +pobreza -secInd — Resuelta (06/11/2026): v3: `+cons`, peso 2. La calidad de un suministro va a `cons`, no a `ciud` (3.2); `pobreza` y `secInd` se retiran.
- [x] condiciones transparentes 2017/0355 +asal1-4 +jovenes -empAut/Micro/Peq — Resuelta (06/11/2026): v3: `+asal1-4`, peso 2 (derechos para todos los asalariados, 3.3.1). `jovenes` y los tamaños de empresa se retiran: no es un coste laboral general (3.4.2).
- [x] denunciantes 2018/0106 +asal1-4 -empMed/Gran — Resuelta (06/11/2026): v3: `{}`. Protege a quien denuncia, no a todos los asalariados, y el umbral es de plantilla, no de facturación (3.4.2).
- [x] interoperabilidad 2017/0351-0352 vacías — Resuelta (06/11/2026): v3 confirma `{}` en las dos.
- [x] código de visados 2018/0061 vacío — Resuelta (06/11/2026): v3 confirma `{}` (tasas más altas y visados de entradas múltiples más fáciles: signo mixto).
- [x] Japón 2018/0091 y 0091M +secPrim (cuenta doble) — Resuelta (06/11/2026): v3: `{}` en las dos, así que ya no cuentan doble; coherente con los acuerdos comerciales.
- [x] ELA 2018/0064 vacía — Resuelta (06/11/2026): v3 confirma `{}` (agencia institucional).
- [x] aguas occidentales 2018/0074 y pez espada 2018/0109 +ciud -secPrim — Resuelta (06/11/2026): v3 confirma `+ciud -secPrim` en las dos (3.2: endurecimiento de la protección y el sector que la cumple), igual que los demás planes de la 8.ª. Ver «Atún rojo» en la sección 1.
- [x] bonos garantizados 2018/0042-0043 y Euro 5 motos 2018/0065 vacíos — Aplicada (06/11/2026): Euro 5 2018/0065: `{"ciud":1,"secInd":-1}`, peso 2 → `{}`, peso 1 (3.9). No hay texto local de este expediente en data/cache/europarlamento_8/textos y sin red no se puede comprobar si endurece o suaviza. Los bonos 2018/0042 y 2018/0043 siguen `{}`.
- [x] flexibilidad migración 2017/2077 vacío — Resuelta (06/11/2026): v3 confirma `{}`.
- [x] impuestos digitales 2018/0072-0073 -secDig -empGran peso 2 — Resuelta (06/11/2026): v3 confirma `-secDig -empGran`, peso 2, en las dos (impuesto a un sector de grandes empresas, como el de la banca o las energéticas en 3.3).
- [x] IVA tipos 2018/0005 vacío peso 2 — Resuelta (06/11/2026): v3: `{}`, peso 1. Solo da margen a los Estados para fijar tipos (P2).


## 3. Datos

- [x] Cuatro procedimientos sin ficha en la API (2016/0062, 2016/0400, 2018/0152, 2018/0330): tipo tomado de una tabla manual. — Resuelta (06/11/2026): el tipo de procedimiento coincide con el sufijo del expediente (2016/0062 NLE; 2016/0400, 2018/0152 y 2018/0330 COD), y v3 les dio tipo y efectos por su título: `soc`, con 2016/0062 `+mujeres +victimas`.
- [x] CDC y PDeCAT se cuentan como PDeCAT (Tremosa); los eurodiputados «Independiente» no se cuentan. — Resuelta (06/11/2026): aplicado en `scripts/legislaturas.py` (CDC → PDeCAT; los «Independiente» no se cuentan).


## Reclasificación con la rúbrica v3 (05/11/2026)

Las 949 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título del procedimiento; las que quedaron sin efectos se releyeron con hasta 12.000 caracteres del texto aprobado oficial en español (API de datos abiertos del Parlamento Europeo). 114 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 93–94 % idéntica, parecido medio 0.94, 0 con signo contrario; 863 de 949 idénticas en las tres lecturas.
- 186 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 715 antes, 807 ahora.


## Aplicación del repaso (06/11/2026)

- 2018/0417(CNS): `{}` → `{"secInd":1}`, peso 1
- 2014/0358(NLE): `{}` → `{"ciud":1}`, peso 1
- 2014/0359(NLE): `{}` → `{"ciud":1}`, peso 1
- 2016/2298(BUD): `{"desPres":1}` → `{}`, peso 1
- 2015/2085(INL): `{"discapacidad":1,"mayores":1}` → `{"discapacidad":1}`, peso 1
- 2018/0065(COD): `{"ciud":1,"secInd":-1}`, peso 2 → `{}`, peso 1 (sin texto local; 3.9)
- temas.json: grupo nuevo 2018/2029(BUD) + 2018/2030(BUD) (Fondo de Solidaridad, incendios de 2017)
