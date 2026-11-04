# Clasificaciones pendientes de revisión (Parlamento Europeo, 10.ª legislatura)

Clasificación inicial de 260 procedimientos legislativos (agentes, rúbrica vigente). Los colectivos se aplican al efecto previsible en España. Contenido de 2025-2026 a menudo deducido del título: conviene comprobarlo con el texto (EUR-Lex / OEIL).

## 1. Criterios aplicados

- [x] Rebajas de exigencias ambientales o sanitarias (Ómnibus de sostenibilidad 2025/0044 y 0045, CO2 de coches 2025/0070, lobo 2025/0058, condicionalidad de la PAC 2025/0236, deforestación 2024/0249 y 2025/0329, camiones 2025/0423, químicos 2025/0531, metano 2026/0325) → `-ciud` y `+sector` (nueva regla en la rúbrica 3.2).

## 2. Dudas

- [ ] Euro digital (2023/0212): `+cons`, `-secFin`; ¿regla de lo público frente a lo privado (`+ciud`)?
- [ ] Derechos de los pasajeros aéreos (2013/0072) y coordinación de la seguridad social (2016/0397): vacías por signo incierto.
- [ ] Aranceles con EE. UU. (2025/0012, 0260, 0261) y productos ucranianos (2025/0056): vacías; ¿`-secPrim`?
- [ ] Presupuestos de la UE 2025-2027: unos vacíos y otros con `+secPrim`/`rural`/`estud`; unificar criterio.
- [ ] Marco financiero 2028-2034 (2025/0571R) y RESTORE/Feader por la DANA (2024/0274, 0275), Fondo de Solidaridad DANA (2025/0318): pesos y efecto en España por comprobar.
- [ ] Reglamento de retorno (2025/0059): peso 2 o 3.
- [ ] ITV (2025/0097): contenido de la propuesta, no del texto final.
- [ ] Nuevas técnicas genómicas (2023/0226), IVA digital (2022/0407), perros y gatos (2023/0447): signos discutibles.
- [ ] Informes de iniciativa legislativa laborales (INL): `+asal1-4` aunque solo piden una directiva.


## Reclasificación con la rúbrica v3 (04/11/2026)

Las 260 iniciativas se han reclasificado con la rúbrica v3 por tres lectores independientes (C, D y E), que no vieron la clasificación anterior ni el trabajo de los otros. Texto usado: título y contenido conocido de cada norma; para las que quedaron sin efectos, segunda lectura con el texto aprobado oficial del Parlamento Europeo (hasta 12.000 caracteres). 83 iniciativas que la primera pasada dejó sin efectos se volvieron a leer con más texto oficial. Clasificación final: consolidación por mayoría (`scripts/consolidar_lecturas.py`; un colectivo cuenta si lo marcan 2 de 3; tipo por mayoría; peso, la mediana).

- Coincidencia entre lectores: 93–95 % idéntica, parecido medio 0.94, 0 con signo contrario; 235 de 260 idénticas en las tres lecturas.
- 67 iniciativas cambian respecto a la clasificación anterior: `lectura_v3/CAMBIOS.md`. Las tres lecturas: `lectura_v3/lecturas.json` y `lectura_v3/<lector>/`.
- Sin efectos: 174 antes, 202 ahora.
