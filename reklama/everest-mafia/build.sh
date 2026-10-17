#!/usr/bin/env bash
# Everest Mafia — reklama videosini yigʻish.
# Ishlatish:  bash build.sh [9x16|4x5]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FMT="${1:-9x16}"
exec /home/user/venv/bin/python "$HERE/build_video.py" --format "$FMT"
