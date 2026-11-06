# Clasificaciones pendientes de revisión (Parlamento Europeo, 6.ª legislatura)

Clasificación inicial de 582 procedimientos legislativos (2004–2009) con la rúbrica vigente, por agentes. Los colectivos se aplican al efecto previsible en España. Solo hay votaciones nominales: los procedimientos aprobados a mano alzada no aparecen. Para cerrar un caso: corrige `clas_*.json` (o confirma que está bien) y marca la casilla.

## 1. Criterios por unificar entre legislaturas europeas

- [x] **Atún rojo y planes de pesca**: unos van vacíos (atún rojo 2009/0116, 2011/0144; en la 9.ª 2019/0272) y otros con `+ciud -secPrim` (2007/0058; en la 9.ª 2022/0111). Elegir un criterio. — Aplicada (06/11/2026): criterio común (plan con límites de capturas → `+ciud -secPrim`; modificación sin contenido → `{}`; solo registro → `-secPrim`). En la 6.ª, 2008/0063 `-secPrim` → `+ciud -secPrim`; 2009/0029 peso 1 → 2, igual que 2007/0058 en su grupo de `temas.json`. 2009/0041: las de la 7.ª las aplica el agente de esa legislatura.
- [x] **Asilo**: las normas que añaden garantías (Dublín III, procedimientos de asilo 2009/0165, acogida) llevan `+inmigrantes` y las restrictivas (sustituto de Dublín de la 9.ª, Dublín 2016/0133) `-inmigrantes`. Revisar el conjunto. — Resuelta (06/11/2026): las restrictivas ya no llevan `-inmigrantes`: Dublín 2016/0133 `{}` y el sustituto de la 9.ª 2020/0279 `{}` (signo mixto); las de garantías llevan `+inmigrantes` (2008/0243, acogida 2008/0244, 2009/0165). Eurodac 2008/0242 se trata en su propia casilla.
- [x] **Acuerdos comerciales con competencia agrícola** (Marruecos, Colombia y Perú, Centroamérica, Ecuador, SADC, Ucrania, Moldavia): casi todos vacíos, algunos con `-secPrim` (Marruecos 2010/0248, aceite tunecino 2015/0218) y Japón con `+secPrim`. Misma duda abierta en la 9.ª. — Aplicada (06/11/2026): criterio común: `{}` peso 1 (3.4.1). La 6.ª no tiene casos con `secPrim`; Marruecos 2010/0248: las de la 7.ª las aplica el agente de esa legislatura.
- [x] **Liberalizaciones** (ferrocarril, correos, asistencia en tierra, autobuses, navegación aérea): `-ciud +secTrans` por la regla 3.2. — Aplicada (06/11/2026): criterio común: sin `ciud`, con el efecto sectorial. La 6.ª ya lo cumplía (2004/0047, 2006/0196 `+secTrans`); 2013/0028, 2013/0029 y 2013/0186: las de la 7.ª las aplica el agente de esa legislatura.
- [x] **Presupuestos en dos procedimientos** (2011, 2013) con peso 3 cada uno: cuentan doble, como 2021 en la 9.ª. — Aplicada (06/11/2026): criterio común: presupuestos anuales `{}` peso 1 y procedimientos del mismo presupuesto agrupados en `temas.json`. Sin casos en la 6.ª; 2011 y 2013: las de la 7.ª las aplica el agente de esa legislatura.
- [x] **Arbitrio canario (AIEM)**: `+secInd` sin `-cons`. — Aplicada (06/11/2026): criterio común: `+secInd` sin `-cons`. Sin casos en la 6.ª; la 7.ª ya lo cumple y 2018/0417 lo aplica el agente de la 8.ª.
- [x] **Clasificación por la posición del Parlamento**: tiempo de trabajo (2004/0209) y propuestas no adoptadas o retiradas se clasifican por su contenido. — Resuelta (06/11/2026): la rúbrica 3.8 pesa las propuestas por lo que proponen aunque no prosperen; 2004/0209, 2006/0165 y 2007/0023 se clasifican por su contenido. La nota de 2004/0209 se trata en su casilla.

## 2. Casos señalados al clasificar


### lotes 02-03 (145/200 vacías)

- [x] 2007/0037B APPCC microempresas como rebaja sanitaria (contenido no seguro) — Resuelta (06/11/2026): conservada por decisión manual: `-ciud +empMicro +secCom`, coherente con 3.2 (rebaja sanitaria: `-ciud` y `+` al sector que se ahorra el coste) y 3.4.2 (microempresas nombradas).
- [x] atún rojo 2007/0058 +ciud -secPrim (9.ª vacío: unificar) — Resuelta (06/11/2026): v3 por mayoría confirma `+ciud -secPrim` peso 2 (3.2, endurecimiento); 2019/0272 de la 9.ª es `{}` por signo mixto, otro contenido. El criterio general sigue en la sección 1.
- [x] bacalao 2008/0063 +ciud (¿vacío?) — Aplicada (06/11/2026): `-secPrim` → `+ciud -secPrim` (3.2, endurecimiento).
- [x] sanciones a empleadores de irregulares 2007/0094 -secPrim -secCons -secCom sin inmigrantes — Aplicada (06/11/2026): 2007/0094 `-secPrim -secCons -secCom` peso 2 → `{}` peso 1 (3.7, 3.4.1).
- [x] OCM vino 2007/0138 vacía peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1 (reforma de signo mixto para el sector, 3.1.1).
- [x] tercer paquete energético 2007/0195-0196 +cons +pobreza -secInd — Resuelta (06/11/2026): v3: 2007/0195 y 2007/0196 `+cons` peso 2, sin `pobreza` ni `-secInd` (separación de actividades con efectos de signo opuesto para el sector, 3.1.1).
- [x] telecom 2007/0247-0248 +cons -secDig peso 2 c/u — Resuelta (06/11/2026): contenidos distintos (marco regulador y derechos de los usuarios), no son el mismo tema (3.9): peso 2 cada uno por 3.8 paso 3. 2007/0247 conserva `+cons -secDig`; 2007/0248, v3 `+cons`.
- [x] renovables 2008/0016 +ciud +secInd peso 2 (¿3?) — Resuelta (06/11/2026): v3: `+ciud` peso 2 (sin `secInd`); no está en el paso 1 de 3.8, así que no es 3.
- [x] CAC 2008/0015 +ciud peso 1 — Resuelta (06/11/2026): conservada: `+ciud` peso 1 (instrumento climático, 3.2).
- [x] transportista 2007/0098 -secTrans -empAut, cabotaje/autocar vacías — Aplicada (06/11/2026): 2007/0098 `-secTrans -empAut` → `-secTrans` (3.4.2).
- [x] defensa 2007/0280 vacía vs 2007/0279 +secInd — Resuelta (06/11/2026): v3: 2007/0279 `+secInd` peso 2 (simplifica transferencias de la industria de defensa) y 2007/0280 `{}` (reglas de contratación pública, 3.4.2). Coherentes.
- [x] ARTEMIS/Hidrógeno 2007/0088, 0211 +secDig/+secInd — Resuelta (06/11/2026): conservadas: 2007/0088 `+secDig` y 2007/0211 `+secInd`, peso 1; subvencionan directamente la investigación de su sector (P1).
- [x] contingentes Canarias 2008/0054 +secInd +cons — Aplicada (06/11/2026): `+secInd +cons` → `+secInd` (3.5.1).
- [x] IVA 2007/0136, 0267 vacías — Resuelta (06/11/2026): v3: ambas `{}` peso 1 (título genérico, 3.9). Coherente con 2008/0143, que se clasifica porque su contenido se conoce.
- [x] nuevos alimentos 2008/0002 vacía — Resuelta (06/11/2026): v3: `{}` peso 1 (procedimiento de autorización, sin signo determinable).
- [x] INL fondos especulativos 2007/2238 -secFin, 2007/2239 vacía — Aplicada (06/11/2026): 2007/2239 `{}` → `-secFin`, igual que 2007/2238.


### lotes 04-05 (118/182 vacías)

- [x] Dublín III 2008/0243 +inmigrantes (9.ª sustituto -inmigrantes) — Resuelta (06/11/2026): conservada `+inmigrantes` peso 2 (más garantías, 3.7); el sustituto de la 9.ª (2020/0279) ya no lleva `-inmigrantes` sino `{}`.
- [x] Eurodac 2008/0242 -inmigrantes peso 1 — Aplicada (06/11/2026): `-inmigrantes` → `{}` peso 1.
- [x] edificios 2008/0223 +ciud +cons peso 2 — Resuelta (06/11/2026): v3: `+ciud -secCons` peso 2 (endurecimiento ambiental, 3.2), sin `cons`.
- [x] chequeo PAC 2008/0103 +secPrim +rural peso 2 (¿3?) — Resuelta (06/11/2026): conservada `+secPrim +rural` peso 2: la PAC no está en el paso 1 de 3.8, así que es 2 (paso 3).
- [x] adaptación PAC 2008/0104 vacía — Resuelta (06/11/2026): v3: `{}` peso 1 (título genérico de modificación, 3.9).
- [x] 2008/0088 +secPrim por título — Aplicada (06/11/2026): `+secPrim` → `{}` peso 1, nota «El título no permite determinar el contenido» (3.9).
- [x] FSUE fuera de España (2008/2017, 2252, 2316, 2009/2008) vacíos (9.ª/10.ª mezclan) — Resuelta (06/11/2026): en la 6.ª los cuatro son `{}`; en la 7.ª a la 10.ª solo llevan `+victimas` las movilizaciones que incluyen a España (2011/2300, 2018/2029, 2022/0337, 2025/0318, 2026/0120, 2026/0284). Criterio coherente.
- [x] derechos de autor 70 años 2008/0157 +secDig (¿-cons?) — Resuelta (06/11/2026): conservada `+secDig` peso 1; `-cons` no procede (3.5.1: no es un suministro; el efecto en precios depende del mercado, P2).
- [x] IVA reducido 2008/0143 +cons +secCom — Aplicada (06/11/2026): `+cons +secCom` peso 2 → `{}` peso 1 (P2: facultativa para los Estados).
- [x] depósitos 2008/0199 +cons -secFin — Resuelta (06/11/2026): v3: `+cons -secFin` peso 2 (3.5.1, protección con coste para el sector).
- [x] SPE 2008/0130 +empMicro/Peq — Aplicada (06/11/2026): `+empMicro +empPeq` → `+empMicro +empPeq +empMed` (pymes, 3.4.2).
- [x] sociedades 2008/0083, 0084, 0182 con impactos pequeños — Aplicada (06/11/2026): 2008/0083 `+empMicro +empPeq` y 2008/0182 `+empMed +empGran` → `+empMicro +empPeq +empMed +empGran` (3.4.2); 2008/0084 sin cambios.
- [x] Lamfalussy INL 2008/2148 -secFin — Resuelta (06/11/2026): conservada `-secFin` peso 1 (pide reforzar la supervisión del sector), coherente con 2007/2238.
- [x] matanza 2008/0180 -secPrim — Resuelta (06/11/2026): v3: `-secInd` peso 2 (mataderos = industria alimentaria, 3.4.1), ya no `secPrim`.
- [x] experimentación 2008/0211 -secInd — Resuelta (06/11/2026): conservada `-secInd` peso 1 (bienestar animal con coste para laboratorios, 3.2 y 3.4.1).


### lotes 00-01 (119/200 vacías)

- [x] tiempo de trabajo 2004/0209 por la posición del PE (+asal1-4 +proSan -empAut/Micro/Peq), no aprobada — Aplicada (06/11/2026): `imp` sin cambios; nota reescrita sin «Posición del Parlamento» ni «no se aprobó» (regla 4).
- [x] Bolkestein 2004/0001 +cons +secCom +empAut peso 3, sin efecto en asalariados — Aplicada (06/11/2026): `+cons +secCom +empAut` peso 3 → `+cons +secCom` peso 2.
- [x] asilo 2000/0238 vacía peso 2 — Resuelta (06/11/2026): v3: `{}` peso 1 (signo mixto; 3.8: sin impactos, peso 1).
- [x] ETT 2002/0072 +asal1/2 +jovenes — Resuelta (06/11/2026): v3: `+asal1`-`asal4` peso 2 (3.3.1, derechos laborales), sin `jovenes` (no fija edad).
- [x] conservación de datos 2005/0182 -cons -secDig — Resuelta (06/11/2026): v3: `-secDig` peso 2, ya sin `-cons`.
- [x] ferrocarril 2004/0047 y postal 2006/0196 -ciud +secTrans (3.2) — Obsoleta (06/11/2026): regla «lo público frente a lo privado» retirada; ahora 2004/0047 y 2006/0196 llevan solo `+secTrans` peso 2.
- [x] fondos de cohesión 2004/0163 +secCons +rural peso 3 — Aplicada (06/11/2026): `+secCons +rural` peso 3 → `{}` peso 1.
- [x] adhesión Bulgaria/Rumanía 2005/0901-0902 +inmigrantes peso 2 — Resuelta (06/11/2026): conservadas `+inmigrantes` peso 2: cambian directamente el estatuto de búlgaros y rumanos residentes (3.7, más derechos para extranjeros); países distintos, no se agrupan (3.9).
- [x] alcohol 2006/0165 y gasóleo 2007/0023 -cons -sector (no adoptadas) — Resuelta (06/11/2026): se clasifican por su contenido aunque no se adoptasen (3.8): conservadas `-cons -secInd` y `-cons -secTrans`, peso 1.
- [x] CO2 turismos 2005/0130 vacía — Resuelta (06/11/2026): v3: `{}` peso 1 (título genérico, 3.9).
- [x] sanciones PI 2005/0127 vacía — Resuelta (06/11/2026): v3: `{}` peso 1 (norma penal, 3.7).
- [x] frutas y hortalizas 2007/0012 +secPrim peso 2 — Resuelta (06/11/2026): conservada `+secPrim` peso 2 (ayudas y regulación sustantiva del sector, 3.8 paso 3).
- [x] pesca Marruecos 2005/0280 peso 2 — Resuelta (06/11/2026): v3: `+secPrim` peso 1, como los demás acuerdos de pesca.
- [x] modulación 2006/0083 vacía — Resuelta (06/11/2026): v3: `{}` peso 1 (facultativa para los Estados, P2).
- [x] Instituto Igualdad 2005/0017 +mujeres — Aplicada (06/11/2026): `+mujeres` → `{}` (3.1.1).


## 3. Datos

- [x] De 10/2005 a 12/2008 las votaciones vienen de Parltrack (no hay anexos oficiales en el servidor de distribución); coinciden con los oficiales donde se solapan. — Resuelta (06/11/2026): documentado en `scripts/descargar_europarlamento_historico.py`: Parltrack solo cubre los días sin anexo oficial y coincide en las 372 votaciones comparables.
- [x] Bernat Joan (Europa de los Pueblos) se cuenta como ERC y Mikel Irujo como EA. — Resuelta (06/11/2026): aplicado en `POR_PERSONA` de `scripts/descargar_europarlamento_historico.py` (Europa de los Pueblos: JOAN i MARÍ → ERC, IRUJO AMEZAGA → EA).


## Reclasificación con la rúbrica v3 (05/11/2026)

Las 582 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título del procedimiento (la API del Parlamento Europeo no publica el texto aprobado en español de esta legislatura); las normas que la v3 deja sin efectos solo por falta de texto conservan la clasificación anterior. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 92–95 % idéntica, parecido medio 0.95, 0 con signo contrario; 530 de 582 idénticas en las tres lecturas.
- 66 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 382 antes, 373 ahora.
- Se han conservado 80 iniciativas por decisión manual (no se detectó ninguna corrección posterior a las lecturas): 2003/0318(CNS), 2004/0001(COD), 2004/0154(COD), 2004/0162(CNS), 2004/0163(AVC), 2004/0166(AVC), 2004/0167(COD), 2004/0209(COD), 2004/2001(BUD), 2005/0017(COD), 2005/0037B(COD), 2005/0052(CNS), 2005/0237A(COD), 2005/0237B(COD), 2005/0238(COD), 2005/0239(COD), 2005/0259(CNS), 2005/0263(COD), 2005/0264(CNS), 2005/0270(CNS), 2005/0278(CNS), 2005/0807(CNS), 2005/0901(AVC), 2005/0902(AVC), 2005/2001(BUD), 2006/0009(CNS), 2006/0056(CNS), 2006/0140(COD), 2006/0165(CNS), 2006/0182(COD), 2006/0190(CNS), 2007/0012(CNS), 2007/0023(CNS), 2007/0037B(COD), 2007/0088(CNS), 2007/0094(COD), 2007/0098(COD), 2007/0143(COD), 2007/0206(CNS), 2007/0211(CNS), 2007/0232(CNS), 2007/0234(COD), 2007/0242(CNS), 2007/0247(COD), 2007/0281(CNS), 2007/2019(BUD), 2007/2238(INL), 2008/0015(COD), 2008/0054(CNS), 2008/0055(COD), 2008/0062(COD), 2008/0083(COD), 2008/0088(CNS), 2008/0103(CNS), 2008/0105(CNS), 2008/0112(CNS), 2008/0130(NLE), 2008/0138(CNS), 2008/0141(COD), 2008/0143(CNS), 2008/0150(CNS), 2008/0152(COD), 2008/0153(COD), 2008/0157(COD), 2008/0172(COD), 2008/0182(COD), 2008/0188(COD), 2008/0191(COD), 2008/0198(COD), 2008/0211(COD), 2008/0214(COD), 2008/0242(COD), 2008/0243(COD), 2008/0245(COD), 2008/0247(COD), 2008/0267(COD), 2008/2026(BUD), 2008/2148(INL), 2009/0042(COD), 2009/2039(BUD).

- [x] **Sin la regla «lo público frente a lo privado» en `ciud`** (decisión del 06/11/2026, rúbrica 3.2): se quita `ciud` de 2004/0047(COD), 2006/0196(COD). Se mantiene el efecto sobre el sector afectado.

## Aplicación del repaso (06/11/2026)

- 2004/0001(COD): `cons +, secCom +, empAut +` peso 3 → `cons +, secCom +` peso 2
- 2004/0163(AVC): `secCons +, rural +` peso 3 → sin impactos, peso 1
- 2004/0209(COD): sin cambios en `imp`; nota sin mención al resultado
- 2005/0017(COD): `mujeres +` → sin impactos
- 2007/0094(COD): `secPrim −, secCons −, secCom −` peso 2 → sin impactos, peso 1
- 2007/0098(COD): `secTrans −, empAut −` → `secTrans −`
- 2007/2239(INL): sin impactos → `secFin −`
- 2008/0054(CNS): `secInd +, cons +` → `secInd +`
- 2008/0063(CNS): `secPrim −` → `ciud +, secPrim −`
- 2008/0083(COD): `empMicro +, empPeq +` → `empMicro +, empPeq +, empMed +, empGran +`
- 2008/0088(CNS): `secPrim +` → sin impactos
- 2008/0130(NLE): `empMicro +, empPeq +` → `empMicro +, empPeq +, empMed +`
- 2008/0143(CNS): `cons +, secCom +` peso 2 → sin impactos, peso 1
- 2008/0182(COD): `empMed +, empGran +` → `empMicro +, empPeq +, empMed +, empGran +`
- 2008/0242(COD): `inmigrantes −` → sin impactos
- 2009/0029(CNS): peso 1 → 2 (igual que 2007/0058 en su grupo de `temas.json`)
- 2004/0229(CNS) (fletán negro): `-secPrim` → `+ciud -secPrim` (criterio común de planes de pesca con límites de captura, 3.2).
