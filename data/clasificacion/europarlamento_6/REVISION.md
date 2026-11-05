# Clasificaciones pendientes de revisión (Parlamento Europeo, 6.ª legislatura)

Clasificación inicial de 582 procedimientos legislativos (2004–2009) con la rúbrica vigente, por agentes. Los colectivos se aplican al efecto previsible en España. Solo hay votaciones nominales: los procedimientos aprobados a mano alzada no aparecen. Para cerrar un caso: corrige `clas_*.json` (o confirma que está bien) y marca la casilla.

## 1. Criterios por unificar entre legislaturas europeas

- [ ] **Atún rojo y planes de pesca**: unos van vacíos (atún rojo 2009/0116, 2011/0144; en la 9.ª 2019/0272) y otros con `+ciud -secPrim` (2007/0058; en la 9.ª 2022/0111). Elegir un criterio.
- [ ] **Asilo**: las normas que añaden garantías (Dublín III, procedimientos de asilo 2009/0165, acogida) llevan `+inmigrantes` y las restrictivas (sustituto de Dublín de la 9.ª, Dublín 2016/0133) `-inmigrantes`. Revisar el conjunto.
- [ ] **Acuerdos comerciales con competencia agrícola** (Marruecos, Colombia y Perú, Centroamérica, Ecuador, SADC, Ucrania, Moldavia): casi todos vacíos, algunos con `-secPrim` (Marruecos 2010/0248, aceite tunecino 2015/0218) y Japón con `+secPrim`. Misma duda abierta en la 9.ª.
- [ ] **Liberalizaciones** (ferrocarril, correos, asistencia en tierra, autobuses, navegación aérea): `-ciud +secTrans` por la regla 3.2.
- [ ] **Presupuestos en dos procedimientos** (2011, 2013) con peso 3 cada uno: cuentan doble, como 2021 en la 9.ª.
- [ ] **Arbitrio canario (AIEM)**: `+secInd` sin `-cons`.
- [ ] **Clasificación por la posición del Parlamento**: tiempo de trabajo (2004/0209) y propuestas no adoptadas o retiradas se clasifican por su contenido.

## 2. Casos señalados al clasificar


### lotes 02-03 (145/200 vacías)

- [ ] 2007/0037B APPCC microempresas como rebaja sanitaria (contenido no seguro)
- [ ] atún rojo 2007/0058 +ciud -secPrim (9.ª vacío: unificar)
- [ ] bacalao 2008/0063 +ciud (¿vacío?)
- [ ] sanciones a empleadores de irregulares 2007/0094 -secPrim -secCons -secCom sin inmigrantes
- [ ] OCM vino 2007/0138 vacía peso 2
- [ ] tercer paquete energético 2007/0195-0196 +cons +pobreza -secInd
- [ ] telecom 2007/0247-0248 +cons -secDig peso 2 c/u
- [ ] renovables 2008/0016 +ciud +secInd peso 2 (¿3?)
- [ ] CAC 2008/0015 +ciud peso 1
- [ ] transportista 2007/0098 -secTrans -empAut, cabotaje/autocar vacías
- [ ] defensa 2007/0280 vacía vs 2007/0279 +secInd
- [ ] ARTEMIS/Hidrógeno 2007/0088, 0211 +secDig/+secInd
- [ ] contingentes Canarias 2008/0054 +secInd +cons
- [ ] IVA 2007/0136, 0267 vacías
- [ ] nuevos alimentos 2008/0002 vacía
- [ ] INL fondos especulativos 2007/2238 -secFin, 2007/2239 vacía


### lotes 04-05 (118/182 vacías)

- [ ] Dublín III 2008/0243 +inmigrantes (9.ª sustituto -inmigrantes)
- [ ] Eurodac 2008/0242 -inmigrantes peso 1
- [ ] edificios 2008/0223 +ciud +cons peso 2
- [ ] chequeo PAC 2008/0103 +secPrim +rural peso 2 (¿3?)
- [ ] adaptación PAC 2008/0104 vacía
- [ ] 2008/0088 +secPrim por título
- [ ] FSUE fuera de España (2008/2017, 2252, 2316, 2009/2008) vacíos (9.ª/10.ª mezclan)
- [ ] derechos de autor 70 años 2008/0157 +secDig (¿-cons?)
- [ ] IVA reducido 2008/0143 +cons +secCom
- [ ] depósitos 2008/0199 +cons -secFin
- [ ] SPE 2008/0130 +empMicro/Peq
- [ ] sociedades 2008/0083, 0084, 0182 con impactos pequeños
- [ ] Lamfalussy INL 2008/2148 -secFin
- [ ] matanza 2008/0180 -secPrim
- [ ] experimentación 2008/0211 -secInd


### lotes 00-01 (119/200 vacías)

- [ ] tiempo de trabajo 2004/0209 por la posición del PE (+asal1-4 +proSan -empAut/Micro/Peq), no aprobada
- [ ] Bolkestein 2004/0001 +cons +secCom +empAut peso 3, sin efecto en asalariados
- [ ] asilo 2000/0238 vacía peso 2
- [ ] ETT 2002/0072 +asal1/2 +jovenes
- [ ] conservación de datos 2005/0182 -cons -secDig
- [ ] ferrocarril 2004/0047 y postal 2006/0196 -ciud +secTrans (3.2)
- [ ] fondos de cohesión 2004/0163 +secCons +rural peso 3
- [ ] adhesión Bulgaria/Rumanía 2005/0901-0902 +inmigrantes peso 2
- [ ] alcohol 2006/0165 y gasóleo 2007/0023 -cons -sector (no adoptadas)
- [ ] CO2 turismos 2005/0130 vacía
- [ ] sanciones PI 2005/0127 vacía
- [ ] frutas y hortalizas 2007/0012 +secPrim peso 2
- [ ] pesca Marruecos 2005/0280 peso 2
- [ ] modulación 2006/0083 vacía
- [ ] Instituto Igualdad 2005/0017 +mujeres


## 3. Datos

- [ ] De 10/2005 a 12/2008 las votaciones vienen de Parltrack (no hay anexos oficiales en el servidor de distribución); coinciden con los oficiales donde se solapan.
- [ ] Bernat Joan (Europa de los Pueblos) se cuenta como ERC y Mikel Irujo como EA.


## Reclasificación con la rúbrica v3 (05/11/2026)

Las 582 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título del procedimiento (la API del Parlamento Europeo no publica el texto aprobado en español de esta legislatura); las normas que la v3 deja sin efectos solo por falta de texto conservan la clasificación anterior. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 92–95 % idéntica, parecido medio 0.95, 0 con signo contrario; 530 de 582 idénticas en las tres lecturas.
- 66 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 382 antes, 373 ahora.
- Se han conservado 80 iniciativas por decisión manual (no se detectó ninguna corrección posterior a las lecturas): 2003/0318(CNS), 2004/0001(COD), 2004/0154(COD), 2004/0162(CNS), 2004/0163(AVC), 2004/0166(AVC), 2004/0167(COD), 2004/0209(COD), 2004/2001(BUD), 2005/0017(COD), 2005/0037B(COD), 2005/0052(CNS), 2005/0237A(COD), 2005/0237B(COD), 2005/0238(COD), 2005/0239(COD), 2005/0259(CNS), 2005/0263(COD), 2005/0264(CNS), 2005/0270(CNS), 2005/0278(CNS), 2005/0807(CNS), 2005/0901(AVC), 2005/0902(AVC), 2005/2001(BUD), 2006/0009(CNS), 2006/0056(CNS), 2006/0140(COD), 2006/0165(CNS), 2006/0182(COD), 2006/0190(CNS), 2007/0012(CNS), 2007/0023(CNS), 2007/0037B(COD), 2007/0088(CNS), 2007/0094(COD), 2007/0098(COD), 2007/0143(COD), 2007/0206(CNS), 2007/0211(CNS), 2007/0232(CNS), 2007/0234(COD), 2007/0242(CNS), 2007/0247(COD), 2007/0281(CNS), 2007/2019(BUD), 2007/2238(INL), 2008/0015(COD), 2008/0054(CNS), 2008/0055(COD), 2008/0062(COD), 2008/0083(COD), 2008/0088(CNS), 2008/0103(CNS), 2008/0105(CNS), 2008/0112(CNS), 2008/0130(NLE), 2008/0138(CNS), 2008/0141(COD), 2008/0143(CNS), 2008/0150(CNS), 2008/0152(COD), 2008/0153(COD), 2008/0157(COD), 2008/0172(COD), 2008/0182(COD), 2008/0188(COD), 2008/0191(COD), 2008/0198(COD), 2008/0211(COD), 2008/0214(COD), 2008/0242(COD), 2008/0243(COD), 2008/0245(COD), 2008/0247(COD), 2008/0267(COD), 2008/2026(BUD), 2008/2148(INL), 2009/0042(COD), 2009/2039(BUD).
