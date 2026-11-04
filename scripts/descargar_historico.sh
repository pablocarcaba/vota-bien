#!/bin/sh
# Descarga en serie las legislaturas X a XIII del Congreso (nunca en paralelo: anti-bots).
# Reanudable: si se corta o hay un 403, vuelve a lanzarlo y seguirá desde la caché.
# Uso: sh scripts/descargar_historico.sh   (log en data/cache/historico.log)
cd "$(dirname "$0")/.." || exit 1
LOG=data/cache/historico.log
mkdir -p data/cache
# espera a que termine cualquier otra descarga contra congreso.es
while pgrep -f "textos_bocg.py|identificar_mixto.py|descargar_legislatura.py" >/dev/null; do sleep 20; done
for spec in "XIII 2019-05-21 2019-09-24" "XI 2016-01-13 2016-05-03" "XII 2016-07-19 2019-03-05" "X 2011-12-13 2015-10-27"; do
  set -- $spec
  echo "=== $1 ($2 a $3) $(date)" >> "$LOG"
  python3 scripts/descargar_legislatura.py --leg "$1" --desde "$2" --hasta "$3" 2>> "$LOG" || { echo "FALLO en $1 (código $?)" >> "$LOG"; exit 1; }
done
echo "=== FIN $(date)" >> "$LOG"
