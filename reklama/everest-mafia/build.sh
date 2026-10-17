#!/usr/bin/env bash
# Everest Mafia — Instagram reklama videosini yig'ish (ffmpeg).
# Sahna davomiyaliklari audio kliplaridan avtomatik olinadi.
# Ishlatish:  bash build.sh [9x16|4x5]
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FMT="${1:-9x16}"
PY="/home/user/venv/bin/python"
FF="$($PY -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')"
STILLS="$HERE/build/stills/$FMT"
SEG="$HERE/build/segments/$FMT"
AUD="$HERE/build/audio"
OUT="$HERE/output"
GAP=0.14  # sahnalar orasidagi jimlik (soniya)
mkdir -p "$SEG" "$AUD" "$OUT"

if [[ "$FMT" == "9x16" ]]; then W=1080; H=1920; else W=1080; H=1350; fi

echo "▸ Still'lar render qilinmoqda ($FMT)..."
$PY "$HERE/render_video.py" --format "$FMT" >/dev/null

echo "▸ Audio kliplari tayyorlanmoqda (jimlik kesiladi, biroz tezlashtiriladi)..."
for i in 01 02 03 04 05 06 07; do
  $FF -y -loglevel error -i "$HERE/audio/vo_$i.mp3" \
    -af "silenceremove=start_periods=1:start_duration=0.05:start_threshold=-45dB:stop_periods=-1:stop_duration=0.25:stop_threshold=-45dB,atempo=1.12" \
    -ar 44100 -ac 1 "$AUD/vo_$i.wav"
done

# Kliplar uzunligidan sahna davomiyaliklari
DURATIONS=($($PY - "$AUD" "$GAP" <<'PY'
import sys, wave, os
aud, gap = sys.argv[1], float(sys.argv[2])
for i in range(1, 8):
    with wave.open(os.path.join(aud, f"vo_{i:02d}.wav")) as w:
        d = w.getnframes() / w.getframerate()
    print(f"{d + gap:.3f}")
PY
))
echo "  Sahna davomiyaliklari (s): ${DURATIONS[*]}"

echo "▸ Ovoz trekini yig'ish (jimliklar bilan)..."
$FF -y -loglevel error \
  -i "$AUD/vo_01.wav" -i "$AUD/vo_02.wav" -i "$AUD/vo_03.wav" -i "$AUD/vo_04.wav" \
  -i "$AUD/vo_05.wav" -i "$AUD/vo_06.wav" -i "$AUD/vo_07.wav" \
  -filter_complex "[0]apad=pad_dur=$GAP[a0];[1]apad=pad_dur=$GAP[a1];[2]apad=pad_dur=$GAP[a2];[3]apad=pad_dur=$GAP[a3];[4]apad=pad_dur=$GAP[a4];[5]apad=pad_dur=$GAP[a5];[6]apad=pad_dur=$GAP[a6];[a0][a1][a2][a3][a4][a5][a6]concat=n=7:v=0:a=1[a]" \
  -map "[a]" -c:a pcm_s16le "$AUD/vo_full.wav"

echo "▸ Segmentlar yig'ilmoqda..."
FILES=()
i=0
for d in "${DURATIONS[@]}"; do
  n=$(printf "%02d" $((i+1)))
  IN="$STILLS/scene$n.png"
  OUTF="$SEG/scene$n.mp4"
  # 0 = ichkariga (push-in), 1 = tashqariga (pull-out)
  if (( i % 2 == 0 )); then Z="min(zoom+0.0009,1.13)"; else Z="if(eq(on,0),1.13,max(zoom-0.0009,1.0))"; fi
  FADE_OUT=$($PY -c "print(f'{$d - 0.3:.3f}')")
  $FF -y -loglevel error -framerate 30 -loop 1 -t "$d" -i "$IN" \
    -vf "scale=$((W*2)):$((H*2)):flags=lanczos,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=${W}x${H}:fps=30,fade=t=in:st=0:d=0.3,fade=t=out:st=${FADE_OUT}:d=0.3,format=yuv420p" \
    -r 30 -c:v libx264 -preset medium -crf 20 -an "$OUTF"
  FILES+=("$OUTF")
  i=$((i+1))
done

echo "▸ Segmentlar birlashtirilmoqda..."
LIST="$SEG/list.txt"; : > "$LIST"
for f in "${FILES[@]}"; do printf "file '%s'\n" "$f" >> "$LIST"; done
$FF -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$SEG/merged.mp4"

echo "▸ Mux qilinmoqda..."
$FF -y -loglevel error -i "$SEG/merged.mp4" -i "$AUD/vo_full.wav" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -ar 44100 -ac 1 -shortest \
  "$OUT/everest_mafia_${FMT}.mp4"
$FF -y -loglevel error -i "$OUT/everest_mafia_${FMT}.mp4" -c:v copy -an "$OUT/everest_mafia_${FMT}_muted.mp4"
$FF -y -loglevel error -i "$OUT/everest_mafia_${FMT}_muted.mp4" -vf "select=eq(n\,0)" -frames:v 1 "$OUT/cover_${FMT}.jpg"
# Cover — CTA kadr (eng ta'sirli variant)
$FF -y -loglevel error -i "$STILLS/scene07.png" -vf "scale=${W}:${H}" -q:v 3 "$OUT/cover_${FMT}.jpg"

echo "✓ Tayyor: $OUT"
$FF -i "$OUT/everest_mafia_${FMT}.mp4" 2>&1 | grep -E "Duration|Stream" || true
ls -lh "$OUT" | grep "$FMT"
