#!/bin/bash
# Terminologiya yangilanishidan keyin barcha mavzularni qayta qurish.
# Tartib: ma'lumot skriptlari -> rasm chizish -> kontent JSON -> DOCX -> QA
set -u
cd "$(dirname "$0")"
PY=/home/user/.venv-book/bin/python
LOG=/tmp/rebuild_all.log
: > "$LOG"

run () {   # run <nomi> <skript>
  local name="$1"; shift
  if timeout 900 "$PY" "$@" >>"$LOG" 2>&1; then
    echo "OK   $name"
  else
    echo "FAIL $name (kod $?)"
  fi
}

echo "=== 1. MA'LUMOT SKRIPTLARI ==="
for s in equilibria_03_01 effects_03_02 ph_03_03 titration_03_04 buffer_03_05 \
         kinetics_03_06 redox_04_02 neutral_04_01 passive_04_03 complex_04_04 \
         decomp_04_05 prep_05_01 prep_05_02 prep_05_03 prep_05_04 \
         prep_06_01 prep_06_02 prep_06_03 prep_06_04 prep_06_05 prep_06_06; do
  [ -f "$s.py" ] && run "$s" "$s.py"
done

echo "=== 2. RASMLAR ==="
for s in draw_*.py; do
  [ "$s" = "draw_mundarija.py" ] && continue
  run "${s%.py}" "$s"
done

echo "=== 3. KONTENT JSON ==="
for s in content_*.py; do run "${s%.py}" "$s"; done

echo "=== 4. DOCX ==="
for s in build_01_01.py build_01_01_sidebar.py build_*_sidebar.py build_mundarija_docx.py; do
  [ -f "$s" ] && run "${s%.py}" "$s"
done

echo "=== 5. QA ==="
for s in check_*.py; do run "${s%.py}" "$s"; done

echo "=== TAYYOR (log: $LOG) ==="
