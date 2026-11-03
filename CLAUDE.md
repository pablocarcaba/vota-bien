# Notas para Claude Code

Proyecto: web estática "¿Quién legisla para ti?" (lee README.md primero).

- Idioma del proyecto y de la web: español. Tono neutral; no tomar partido.
- Fuente de verdad del dataset: `data/fuente/` (congreso_xv.json, votos_extra.json) + `data/clasificacion/clas_*.json`. No edites nada de `data/generado/` ni `site/index.html` a mano: regenera con los scripts (ver README).
- Cualquier cambio de clasificación sigue `data/clasificacion/RUBRICA.md` y se hace en `data/clasificacion/clas_*.json`.
- congreso.es tiene protección anti-bots: nunca peticiones en paralelo; una cada 2-3 s; parar ante un 403.
- La página es un único HTML sin build ni dependencias JS. Colores por tokens CSS con modo claro y oscuro; debe funcionar a 400 px de ancho.
- Despliegue previsto: GitHub Pages.
