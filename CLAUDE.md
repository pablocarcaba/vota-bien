# Notas para Claude Code

Proyecto: web estática "¿A quién puedo votar?" (antes «¿Quién legisla para ti?») (lee README.md primero).

- Idioma del proyecto y de la web: español. Tono neutral; no tomar partido.
- Cada fuente y legislatura es un dataset aparte con clave `<fuente>_<leg>` (p. ej. `congreso_xv`); nunca se mezclan partidos de legislaturas distintas. Su configuración está en `scripts/legislaturas.py`.
- Fuente de verdad: `data/fuente/<clave>*.json` + `data/clasificacion/<clave>/clas_*.json`. No edites `data/generado/`, `site/data/` ni `site/index.html` a mano: regenera con los scripts (ver README).
- Tras tocar la clasificación o los colectivos de la web, ejecuta `python3 scripts/validar_clasificacion.py` (0 errores) antes de regenerar.
- Cualquier cambio de clasificación sigue `data/clasificacion/RUBRICA.md` y se hace en `data/clasificacion/<clave>/clas_*.json`; los dudosos se apuntan en su `REVISION.md`.
- congreso.es tiene protección anti-bots: nunca peticiones en paralelo; una cada 2-3 s; parar ante un 403.
- La página es HTML sin build ni dependencias JS; carga `site/data/<clave>.json` con fetch (en local, sírvela con `python3 -m http.server`). Colores por tokens CSS con modo claro y oscuro; debe funcionar a 400 px de ancho.
- Despliegue: GitHub Pages (repo pablocarcaba/vota-bien), automático al hacer push de `site/` a `main`.
