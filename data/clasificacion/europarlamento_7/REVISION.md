# Clasificaciones pendientes de revisión (Parlamento Europeo, 7.ª legislatura)

Clasificación inicial de 931 procedimientos legislativos (2009–2014) con la rúbrica vigente, por agentes. Los colectivos se aplican al efecto previsible en España. Solo hay votaciones nominales: los procedimientos aprobados a mano alzada no aparecen. Para cerrar un caso: corrige `clas_*.json` (o confirma que está bien) y marca la casilla.

## 1. Criterios por unificar entre legislaturas europeas

- [x] **Atún rojo y planes de pesca**: unos van vacíos (atún rojo 2009/0116, 2011/0144; en la 9.ª 2019/0272) y otros con `+ciud -secPrim` (2007/0058; en la 9.ª 2022/0111). Elegir un criterio. — Aplicada (06/11/2026): criterio común (límites de captura conocidos → `+ciud -secPrim`; modificación sin contenido → `{}`; solo registro → `-secPrim`): 2009/0041 `-secPrim` → `+ciud -secPrim`; el resto ya lo cumplía.
- [x] **Asilo**: las normas que añaden garantías (Dublín III, procedimientos de asilo 2009/0165, acogida) llevan `+inmigrantes` y las restrictivas (sustituto de Dublín de la 9.ª, Dublín 2016/0133) `-inmigrantes`. Revisar el conjunto. — Resuelta (06/11/2026): ya no hay asimetría: el lado restrictivo está hoy vacío (8.ª 2016/0133 `{}`, 9.ª 2020/0279 `{}` por signo mixto) y las refundiciones que añaden garantías llevan `+inmigrantes` (2009/0164, 2009/0165; 6.ª 2008/0243, 2008/0244), conforme a 3.7.
- [x] **Acuerdos comerciales con competencia agrícola** (Marruecos, Colombia y Perú, Centroamérica, Ecuador, SADC, Ucrania, Moldavia): casi todos vacíos, algunos con `-secPrim` (Marruecos 2010/0248, aceite tunecino 2015/0218) y Japón con `+secPrim`. Misma duda abierta en la 9.ª. — Aplicada (06/11/2026): 2010/0248 `-secPrim` peso 2 → `{}` peso 1 (3.4.1, signo mixto).
- [x] **Liberalizaciones** (ferrocarril, correos, asistencia en tierra, autobuses, navegación aérea): `-ciud +secTrans` por la regla 3.2. — Aplicada (06/11/2026): 2013/0028, 2013/0029 y 2013/0186 `-ciud +secTrans` → `+secTrans`.
- [x] **Presupuestos en dos procedimientos** (2011, 2013) con peso 3 cada uno: cuentan doble, como 2021 en la 9.ª. — Aplicada (06/11/2026): 2010/2001 y 2010/2290 agrupados en temas.json; además, `+secPrim +rural +estud` peso 3 → `{}` peso 1.
- [x] **Arbitrio canario (AIEM)**: `+secInd` sin `-cons`. — Resuelta (06/11/2026): 2010/0359, 2011/0192, 2013/0387 y 2014/0093 llevan solo `+secInd`; `-cons` no procede (3.5.1: el AIEM no es impuesto de un suministro o servicio, y la repercusión en precio depende del mercado, P2); coherente con 8.ª 2018/0417 `+secInd`.
- [x] **Clasificación por la posición del Parlamento**: tiempo de trabajo (2004/0209) y propuestas no adoptadas o retiradas se clasifican por su contenido. — Resuelta (06/11/2026): la rúbrica 3.8 lo fija: las propuestas se pesan por lo que proponen aunque no prosperasen; quedan notas que citan el resultado, contra la regla 4 (2008/0255-0256, 2011/0092, 2011/0167, 2012/0035), anotadas en sus casillas.

## 2. Casos señalados al clasificar


### lotes 08-09 (100/131 vacías)

- [x] 2013/0253 MUR solo -secFin peso 3 (en 9.ª crisis bancarias vacía) — Resuelta (06/11/2026): v3: `-secFin` peso 2 (fondo de resolución financiado por las entidades); las de la 9.ª (2023/0111-0113) son modificaciones de título genérico, vacías por 3.9.
- [x] 2013/0344 aviación RCDE «stop the clock» como rebaja -ciud +secTrans — Resuelta (06/11/2026): `-ciud +secTrans` es el supuesto de rebaja de protección climática de 3.2.
- [x] AIEM canario (2013/0387, 2014/0093) +secInd sin -cons — Resuelta (06/11/2026): `+secInd` sin `-cons`, ver criterio del AIEM arriba.
- [x] 2013/0266 contingentes pescado Canarias +secInd (¿-secPrim?) — Resuelta (06/11/2026): v3: solo `+secInd`; `-secPrim` no procede (los pescadores son competidores, 3.4.1).
- [x] 2013/0415 visados Colombia/Perú +inmigrantes — Resuelta (06/11/2026): `+inmigrantes`: amplía derechos de nacionales de terceros países (exención de visado), 3.7.
- [x] FSE refuerzo (2013/0271, 2013/2159, 2160) +jovenes +desSub +pobreza — Aplicada (06/11/2026): 2013/0271 `+jovenes +desSub +pobreza` → `+jovenes`.
- [x] Eurostars 2013/0232 y FEI 2014/0034 +empMicro +empPeq — Aplicada (06/11/2026): 2014/0034 `+empMicro +empPeq` → `{}` (P2: el crédito depende de los bancos; coherente con el FEIE 2015/0009); Eurostars sin cambios.
- [x] 2013/0343 IVA normalizada +empAut/Micro/Peq — Aplicada (06/11/2026): 2013/0343 `+empAut +empMicro +empPeq` → `+empAut +empMicro +empPeq +empMed +empGran` (obligación general, 3.4.2).
- [x] 2013/0400 matrices-filiales -empGran — Aplicada (06/11/2026): 2013/0400 `-empGran` → `{}` (3.4.2).
- [x] 2013/0222 tasas farmacovigilancia -secInd — Resuelta (06/11/2026): v3 confirma `-secInd` peso 1: tasa a los titulares de autorizaciones de medicamentos.
- [x] 2013/0307 invasoras +ciud -secPrim peso 2 — Resuelta (06/11/2026): v3: `+ciud` peso 2, sin `-secPrim` (no se identifica un sector que cumpla la exigencia).
- [x] 2013/0371 bolsas +ciud -secInd -secCom — Resuelta (06/11/2026): v3: `+ciud` peso 2, sin `-secInd -secCom` (la directiva obliga a los Estados, no a un sector concreto).
- [x] 2013/0340 seguridad nuclear +ciud -secInd — Resuelta (06/11/2026): `+ciud -secInd` peso 2: endurecimiento de protección (3.2, 5.5).
- [x] 2013/0255 Fiscalía Europea vacía peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1, norma institucional (3.8).
- [x] 2013/0438-0439 retribuciones UE vacías — Resuelta (06/11/2026): `{}` peso 1: afectan a funcionarios de la UE, no a un colectivo español.


### lotes 00-01 (152/200 vacías; tipo eco/soc de las vacías asignado por palabras clave)

- [x] Atenas 2003/0132A +cons -secTrans — Resuelta (06/11/2026): `+cons -secTrans`: amplía la responsabilidad del transportista frente a los pasajeros (3.5.1).
- [x] origen 2005/0254 +cons +secInd — Resuelta (06/11/2026): v3: solo `+cons`; `secInd` no (la industria nacional es competidora, 3.4.1).
- [x] maternidad 2008/0193 +mujeres +infancia — Resuelta (06/11/2026): v3: `+mujeres +infancia` peso 2, permiso ligado a una situación (3.3.1, 5.3).
- [x] info medicamentos 2008/0255-0256 +secInd — Aplicada (06/11/2026): etiquetas sin cambios (`+secInd`); nota reescrita sin el resultado.
- [x] planes pesca (2009/0041, 0057, 0112) +ciud -secPrim vs atún rojo 2009/0116 vacío (unificar) — Aplicada (06/11/2026): 2009/0041 `-secPrim` → `+ciud -secPrim`; 2009/0057, 2009/0112 (`+ciud -secPrim`) y 2009/0116 (`-secPrim`, solo registro) sin cambios.
- [x] NEAFC 2009/0051 +ciud -secPrim — Resuelta (06/11/2026): v3: solo `-secPrim` (régimen de control con obligaciones para la flota; no endurece la protección del recurso).
- [x] acuicultura exóticas 2009/0153 y motores flexibles 2010/0195 como rebajas — Resuelta (06/11/2026): `-ciud +secPrim` y `-ciud +secInd`: rebajas de protección ambiental (3.2).
- [x] transgénicos 2010/0208 vacía peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1.
- [x] plátano 2010/0056-0057 -secPrim — Aplicada (06/11/2026): se mantienen `-secPrim`, simétricas con las salvaguardias 2011/0262-0263 `+secPrim` (un solo producto, signo conocido).
- [x] pagos directos PAC 2009/0084 vacía — Resuelta (06/11/2026): `{}` peso 1: modificación técnica sin contenido determinable (3.9).
- [x] Frontex 2010/0039 vacía — Resuelta (06/11/2026): `{}` peso 1: norma institucional.
- [x] supervisión financiera (2009/0140, 0142 peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1, normas institucionales.
- [x] 0143, 0144 peso 1) vacías — Resuelta (06/11/2026): v3: `{}` peso 1.
- [x] ICT 2010/0209 +inmigrantes +empGran — Resuelta (06/11/2026): v3: solo `+inmigrantes`, sin `empGran`.
- [x] asilo 2009/0165 +inmigrantes vs reglamento 9.ª -inmigrantes — Resuelta (06/11/2026): la 9.ª 2020/0279 ya no lleva `-inmigrantes` (`{}`, signo mixto); 2009/0165 `+inmigrantes` por las garantías añadidas.


### lotes 02-03 (144/200 vacías)

- [x] six-pack 2010/0276, 0278, 0280, 0281 vacíos peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1, normas institucionales.
- [x] minas de carbón 2010/0220 +secInd — Resuelta (06/11/2026): `+secInd` peso 2: autoriza ayudas al carbón que de otro modo expiraban en 2010.
- [x] Marruecos agrícola 2010/0248 -secPrim — Aplicada (06/11/2026): 2010/0248 `-secPrim` peso 2 → `{}` peso 1.
- [x] ferroviario refundido 2010/0253 vacío — Resuelta (06/11/2026): `{}` peso 1: refundición técnica.
- [x] tractores 2010/0301, 2011/0002 como rebajas — Resuelta (06/11/2026): `-ciud +secInd`: rebajas de protección ambiental (3.2).
- [x] presupuesto 2011 doble (2010/2001, 2010/2290) peso 3 — Aplicada (06/11/2026): 2010/2001 y 2010/2290 `+secPrim +rural +estud` peso 3 → `{}` peso 1, agrupados en temas.json.
- [x] MFF 2014-2020 2011/0177 peso 3 (en 9.ª revisiones vacías) — Aplicada (06/11/2026): presupuestos anuales y MFF (2009/2002, 2010/2001, 2010/2290, 2011/2020, 2011/0177, 2012/2092, 2012/2307, 2013/2145) `+secPrim +rural +estud` peso 3 → `{}` peso 1.
- [x] fiscalidad energética 2011/0092 +ciud -cons -secTrans — Aplicada (06/11/2026): etiquetas sin cambios (`+ciud -cons -secTrans`; el impuesto de hidrocarburos va a `cons`); nota reescrita sin «Retirada».
- [x] ACTA 2011/0167 +secInd -cons peso 2 — Aplicada (06/11/2026): 2011/0167 `+secInd -cons` → `+secInd` (3.7); nota reescrita sin el resultado.
- [x] patente unitaria (2010/0384, 2011/0093, 0094) vacías — Resuelta (06/11/2026): `{}` peso 1: normas institucionales de propiedad industrial.
- [x] interpretación 2010/0801 +inmigrantes — Resuelta (06/11/2026): `+inmigrantes`: garantía procesal a extranjeros, excepción (a) de 3.7.
- [x] pesca Marruecos 2011/0139 +secPrim — Resuelta (06/11/2026): `+secPrim`, como los demás protocolos de pesca.
- [x] atún rojo 2011/0144 vacío — Resuelta (06/11/2026): `{}` peso 1: modificación sin contenido determinable (3.9); el criterio general de planes sigue abierto arriba.
- [x] arbitrio canario 2010/0359, 2011/0192 +secInd — Resuelta (06/11/2026): `+secInd`, ver criterio del AIEM; 2011/0192 y 2013/0387 agrupados en temas.json con la misma clasificación.
- [x] PPC 2011/0195 +ciud -secPrim peso 2 (¿3?) — Resuelta (06/11/2026): v3: `+ciud -secPrim` peso 2 (regula de forma sustantiva un sector, 3.8 paso 3).


### lotes 04-05 (148/200 vacías)

- [x] controles fronteras interiores 2011/0242 -inmigrantes — Aplicada (06/11/2026): 2011/0242 `-inmigrantes` → `{}`.
- [x] Colombia-Perú 2011/0249 y Centroamérica 2011/0303 vacíos (¿-secPrim?) — Resuelta (06/11/2026): `{}` peso 1, coherente con 8.ª 2014/0234 y 9.ª (acuerdos comerciales vacíos).
- [x] salvaguardias plátano 2011/0262-0263 +secPrim — Aplicada (06/11/2026): se mantienen `+secPrim`, simétricas con los plátanos 2010/0056-0057 `-secPrim`.
- [x] ITF 2011/0261 -secFin -empGran — Resuelta (06/11/2026): v3: solo `-secFin` peso 2; grava una actividad sin distinguir tamaños (3.4.2).
- [x] Fondo de Cohesión 2011/0274 vacío — Resuelta (06/11/2026): `{}` peso 1.
- [x] asistencia en tierra 2011/0397 -ciud +secTrans — Resuelta (06/11/2026): ya sin `ciud`: `+secTrans` (decisión del 06/11/2026, 3.2).
- [x] ruido aeropuertos 2011/0398 vacío — Resuelta (06/11/2026): `{}` peso 1: signo no determinable.
- [x] aleteo 2011/0364 +ciud -secPrim — Resuelta (06/11/2026): `+ciud -secPrim`: endurecimiento de protección de biodiversidad (3.2).
- [x] FSI fronteras 2011/0365 y EUROSUR 2011/0427 vacíos — Resuelta (06/11/2026): `{}` peso 1: normas de financiación y organización.
- [x] FAMI 2011/0366 +inmigrantes — Aplicada (06/11/2026): 2011/0366 `+inmigrantes` → `{}` (signos opuestos, 3.1.1).
- [x] concesiones 2011/0437 vacía — Resuelta (06/11/2026): `{}` peso 1: contratación pública (3.2, 3.4.2).
- [x] contratación pública 2011/0438 +empMicro/Peq peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1; contratación pública no marca tamaños (3.4.2).
- [x] RGPD 2012/0011 +cons -secDig peso 3 — Aplicada (06/11/2026): 2012/0011 `{}` peso 1 → `+cons -secDig` peso 2 (contenido conocido, 3.9; peso 3 no está en el paso 1 de 3.8).
- [x] Horizonte 2020 2011/0401 +secInd +secDig peso 2 — Aplicada (06/11/2026): 2011/0401 `+secInd +secDig` peso 2 → `{}` peso 1.
- [x] precios medicamentos 2012/0035 +pac +secInd — Aplicada (06/11/2026): etiquetas sin cambios (`+pac +secInd`); nota reescrita sin «después retirada».


### lotes 06-07 (136/200 vacías)

- [x] BRRD 2012/0150 +ciud -secFin peso 3 — Aplicada (06/11/2026): 2012/0150 `+ciud -secFin` peso 3 → `-secFin` peso 2.
- [x] MUS 2012/0242 -secFin peso 2 — Aplicada (06/11/2026): 2012/0242 `-secFin` peso 2 → `{}` peso 1 (cambio de supervisor, 3.4.1).
- [x] cumplimiento desplazados 2012/0061 +asal1/2 -secCons — Aplicada (06/11/2026): 2012/0061 `+asal1 +asal2 -secCons` → `-secCons`.
- [x] ITF reforzada 2012/0298, 2013/0045 -secFin (+ -empGran -prop3/4) — Aplicada (06/11/2026): 2012/0298 sale del grupo de temas.json (autorizar la cooperación reforzada no es el mismo contenido que el impuesto ni grava a nadie): `-secFin` peso 1 → `{}` peso 1; 2013/0045 sigue `-secFin` peso 2.
- [x] cuarto paquete ferroviario 2013/0028-0029 -ciud +secTrans — Aplicada (06/11/2026): 2013/0028 y 2013/0029 `-ciud +secTrans` → `+secTrans`.
- [x] SES2+ 2013/0186 -ciud +secTrans — Aplicada (06/11/2026): 2013/0186 `-ciud +secTrans` → `+secTrans`.
- [x] presupuesto 2013 doble (2012/2092, 2307) peso 3 — Resuelta (06/11/2026): 2012/2092 y 2012/2307 agrupados en temas.json: cuentan una vez (el criterio de fondo de presupuestos sigue abierto arriba).
- [x] RCDE aviación 2012/0328 como rebaja — Resuelta (06/11/2026): `-ciud +secTrans`: rebaja de protección climática (3.2).
- [x] ILUC 2012/0288 -secInd — Aplicada (06/11/2026): 2012/0288 `{}` peso 1 → `+ciud -secInd` peso 2 (se restaura la anterior; límite a biocombustibles de cultivos, 3.2).
- [x] reproducción vegetal 2013/0137 vacía — Resuelta (06/11/2026): `{}` peso 1: signo no determinable.
- [x] Convenio OIT 189 2013/0085 vacío — Resuelta (06/11/2026): `{}` peso 1: autoriza ratificar un tratado (3.1.1).
- [x] tabaco 2012/0366 +ciud +jovenes -secInd peso 2 (¿3?) — Resuelta (06/11/2026): v3: `+ciud -secInd` peso 2, sin `jovenes` (5.5).
- [x] cuentas de pago 2013/0139 +cons +pobreza +inmigrantes -secFin — Resuelta (06/11/2026): v3: `+cons -secFin` peso 2, sin `pobreza` ni `inmigrantes`.
- [x] INL reestructuraciones 2012/2061 +asal1-4 — Resuelta (06/11/2026): `+asal1-4` peso 2: derechos laborales para todos los asalariados (3.3.1).
- [x] FSUE 2012/2237 supuesto Italia sin confirmar — Resuelta (06/11/2026): `{}` peso 1: no afecta a España.


## Reclasificación con la rúbrica v3 (05/11/2026)

Las 931 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título del procedimiento (la API del Parlamento Europeo solo publica el texto aprobado en español de 4 normas de esta legislatura, que se releyeron con él); las normas que la v3 deja sin efectos solo por falta de texto conservan la clasificación anterior. 4 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 95–96 % idéntica, parecido medio 0.96, 0 con signo contrario; 872 de 931 idénticas en las tres lecturas.
- 89 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 680 antes, 680 ahora.
- Se han conservado 124 iniciativas por decisión manual (no se detectó ninguna corrección posterior a las lecturas): 2003/0132A(NLE), 2007/0206(CNS), 2008/0255(COD), 2008/0256(COD), 2009/0054(COD), 2009/0057(COD), 2009/0112(COD), 2009/0127(COD), 2009/0152(CNS), 2009/0153(COD), 2009/0165(COD), 2009/0170(COD), 2009/2002(BUD), 2009/2066(BUD), 2010/0032(COD), 2010/0056(COD), 2010/0057(NLE), 2010/0195(COD), 2010/0199(COD), 2010/0220(NLE), 2010/0248(NLE), 2010/0254(COD), 2010/0261(COD), 2010/0271(COD), 2010/0301(COD), 2010/0326(COD), 2010/0353(COD), 2010/0359(CNS), 2010/0362(COD), 2010/0373(COD), 2010/0801(COD), 2010/2001(BUD), 2010/2066(BUD), 2010/2068(BUD), 2010/2136(BUD), 2010/2165(BUD), 2010/2250(BUD), 2010/2251(BUD), 2010/2252(BUD), 2010/2265(BUD), 2010/2290(BUD), 2010/2293(BUD), 2011/0001(COD), 2011/0002(COD), 2011/0092(CNS), 2011/0147(COD), 2011/0152(COD), 2011/0156(COD), 2011/0167(NLE), 2011/0177(APP), 2011/0192(CNS), 2011/0194(COD), 2011/0195(COD), 2011/0197(COD), 2011/0231(COD), 2011/0242(COD), 2011/0268(COD), 2011/0269(COD), 2011/0270(COD), 2011/0275(COD), 2011/0281(COD), 2011/0286(COD), 2011/0294(COD), 2011/0295(COD), 2011/0296(COD), 2011/0298(COD), 2011/0299(COD), 2011/0300(COD), 2011/0302(COD), 2011/0308(COD), 2011/0339(COD), 2011/0340(COD), 2011/0344(COD), 2011/0366(COD), 2011/0370(COD), 2011/0397(COD), 2011/0401(COD), 2011/0428(COD), 2011/0461(COD), 2011/2020(BUD), 2012/0035(COD), 2012/0055(COD), 2012/0061(COD), 2012/0130(NLE), 2012/0150(COD), 2012/0168(COD), 2012/0184(COD), 2012/0186(COD), 2012/0190(COD), 2012/0192(COD), 2012/0202(COD), 2012/0242(CNS), 2012/0297(COD), 2012/0298(APP), 2012/0337(COD), 2012/2023(BUD), 2012/2089(BUD), 2012/2092(BUD), 2012/2160(BUD), 2012/2280(BUD), 2012/2307(BUD), 2013/0012(COD), 2013/0103(COD), 2013/0105(COD), 2013/0117(COD), 2013/0124(COD), 2013/0136(COD), 2013/0141(COD), 2013/0186(COD), 2013/0188(CNS), 2013/0239(COD), 2013/0271(COD), 2013/0305(COD), 2013/0343(CNS), 2013/0344(COD), 2013/0387(CNS), 2013/0400(CNS), 2013/0415(COD), 2013/2145(BUD), 2013/2192(BUD), 2014/0034(COD), 2014/0093(CNS), 2014/2013(BUD), 2014/2027(BUD).

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 2011/0397(COD). Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 2008/0255(COD): `+secInd` → igual; nota sin el resultado
- 2008/0256(COD): `+secInd` → igual; nota sin el resultado
- 2009/0041(CNS): `-secPrim` → `+ciud -secPrim`
- 2009/2002(BUD): `+secPrim +rural +estud` p3 → `{}` p1
- 2010/0248(NLE): `-secPrim` p2 → `{}` p1
- 2010/2001(BUD): `+secPrim +rural +estud` p3 → `{}` p1 (agrupado con 2010/2290)
- 2010/2290(BUD): `+secPrim +rural +estud` p3 → `{}` p1 (agrupado con 2010/2001)
- 2011/0092(CNS): `+ciud -cons -secTrans` → igual; nota sin el resultado
- 2011/0167(NLE): `+secInd -cons` → `+secInd`; nota sin el resultado
- 2011/0177(APP): `+secPrim +rural +estud` p3 → `{}` p1
- 2011/0242(COD): `-inmigrantes` → `{}`
- 2011/0366(COD): `+inmigrantes` → `{}`
- 2011/0401(COD): `+secInd +secDig` p2 → `{}` p1
- 2011/2020(BUD): `+secPrim +rural +estud` p3 → `{}` p1
- 2012/0011(COD): `{}` p1 → `+cons -secDig` p2
- 2012/0035(COD): `+pac +secInd` → igual; nota sin el resultado
- 2012/0061(COD): `+asal1 +asal2 -secCons` → `-secCons`
- 2012/0150(COD): `+ciud -secFin` p3 → `-secFin` p2
- 2012/0242(CNS): `-secFin` p2 → `{}` p1
- 2012/0288(COD): `{}` p1 → `+ciud -secInd` p2
- 2012/0298(APP): `-secFin` p1 → `{}` p1 (sale del grupo de temas.json con 2013/0045)
- 2012/2092(BUD): `+secPrim +rural +estud` p3 → `{}` p1
- 2012/2307(BUD): `+secPrim +rural +estud` p3 → `{}` p1
- 2013/0028(COD): `-ciud +secTrans` → `+secTrans`
- 2013/0029(COD): `-ciud +secTrans` → `+secTrans`
- 2013/0186(COD): `-ciud +secTrans` → `+secTrans`
- 2013/0271(COD): `+jovenes +desSub +pobreza` → `+jovenes`
- 2013/0343(CNS): `+empAut +empMicro +empPeq` → `+empAut +empMicro +empPeq +empMed +empGran`
- 2013/0400(CNS): `-empGran` → `{}`
- 2013/2145(BUD): `+secPrim +rural +estud` p3 → `{}` p1
- 2014/0034(COD): `+empMicro +empPeq` → `{}`
