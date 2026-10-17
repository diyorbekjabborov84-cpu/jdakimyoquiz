#!/usr/bin/env python3
"""
Everest Mafia — reklama videosini ffmpeg bilan yigʻadi.

Bosqichlar:
  1) Ovoz kliplarini tozalash (jimlik kesiladi) va tezlashtirish
  2) Sahna davomiyaliklarini ovozdan olish -> durations.json
  3) render_video.py orqali fon + matn qatlamlarini tayyorlash
  4) Har sahna: kadr kesilishlari (Ken Burns) + matn qatlamlarining ochilishi
  5) Barcha sahnalarni birlashtirish, grain, yorqinlik va ovozni mux qilish

Ishlatish:  python build_video.py --format 9x16
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import wave

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
FF = subprocess.run(
    [PY, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
    capture_output=True, text=True, check=True,
).stdout.strip()

AUDIO_SRC = os.path.join(HERE, "audio")
BUILD = os.path.join(HERE, "build")
OUTPUT = os.path.join(HERE, "output")
GAP = 0.14          # sahnalar orasidagi jimlik
SPEED = "1.12"      # ovoz tezligi
def scene_keys() -> list[str]:
    """audio/vo_01.mp3, vo_02.mp3 ... — raqamlangan kliplar soniga qarab."""
    files = [f for f in os.listdir(AUDIO_SRC) if re.fullmatch(r"vo_\d+\.mp3", f)]
    n = len(files)
    return [f"s{i}" for i in range(1, n + 1)]


def run(args: list[str]) -> None:
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-4000:], file=sys.stderr)
        raise SystemExit(f"ffmpeg xatosi: {' '.join(args[:6])} ...")


def ff(args: list[str]) -> None:
    run([FF, "-y", "-loglevel", "error"] + args)


def wav_duration(path: str) -> float:
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def make_sweep(w: int, h: int, path: str) -> None:
    """Yumshoq yorqinlik chizigʻi (koʻrinishga yugurib oʻtadi)."""
    band = int(w * 0.95)
    img = Image.new("RGBA", (band, h), (0, 0, 0, 0))
    px = img.load()
    for x in range(band):
        t = x / (band - 1)
        a = int(12 * (1 - abs(t * 2 - 1)) ** 3)
        for y in range(h):
            px[x, y] = (255, 250, 240, a)
    img.save(path)


def build_part(bg: str, dur: float, out: str, w: int, h: int, motion: str, flash: str) -> None:
    """Bitta kadr: Ken Burns / burst / shake + kirish effekti."""
    drift_x = "42*(zoom-1)*sin(on/48)"
    drift_y = "30*(zoom-1)*cos(on/66)"
    if motion == "in":
        z = "min(1+on*0.00030,1.14)"
        x = f"iw/2-(iw/zoom/2)+{drift_x}"
        y = f"ih/2-(ih/zoom/2)+{drift_y}"
    elif motion == "out":
        z = "max(1.14-on*0.00030,1.0)"
        x = f"iw/2-(iw/zoom/2)+{drift_x}"
        y = f"ih/2-(ih/zoom/2)+{drift_y}"
    elif motion == "burst":
        # tez zoom "snap": 1.34 -> 1.0 (0.4 s), keyin sekin drift
        z = "if(lt(on,13),1.34-on*0.026,1.005+on*0.00022)"
        x = f"iw/2-(iw/zoom/2)+{drift_x}"
        y = f"ih/2-(ih/zoom/2)+{drift_y}"
    else:  # shake — kamera tebranishi
        z = "min(1+on*0.00028,1.12)"
        x = "iw/2-(iw/zoom/2)+90*sin(on*1.35)*min(1,on/12)"
        y = "ih/2-(ih/zoom/2)+60*cos(on*1.15)*min(1,on/12)"

    # kesishdagi chaqnash: iliq "light leak" (noir uslubga mos)
    fade_in = 0.06 if flash == "white" else 0.45
    color = "0xFFF2E0" if flash == "white" else "black"
    # burst kadrlarda qisqa kontrast/rang "punch"
    punch = ""
    if motion == "burst":
        punch = "eq=eval=frame:contrast='1+0.35*max(0,1-t/0.16)':saturation='1+0.5*max(0,1-t/0.16)',"

    ff([
        "-framerate", "30", "-loop", "1", "-t", f"{dur:.3f}", "-i", bg,
        "-vf",
        f"scale={w*2}:{h*2}:flags=lanczos,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={w}x{h}:fps=30,"
        f"{punch}"
        f"fade=t=in:st=0:d={fade_in}:color={color},format=yuv420p",
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-an", out,
    ])


def concat(parts: list[str], list_file: str, out: str) -> None:
    with open(list_file, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    ff(["-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", out])


def build_scene(scene: dict, stills: str, seg_dir: str, w: int, h: int, sweep: str) -> str:
    key = scene["key"]
    dur = scene["duration"]
    parts = scene["parts"]

    part_files = []
    for i, p in enumerate(parts):
        out = os.path.join(seg_dir, f"{key}_p{i}.mp4")
        motion = p.get("motion", "in")
        if i == 0 and key == "s1":
            flash = "black"
        else:
            flash = "white"
        build_part(os.path.join(stills, p["bg"]), p["duration"], out, w, h, motion, flash)
        part_files.append(out)

    base = os.path.join(seg_dir, f"{key}_base.mp4")
    if len(part_files) == 1:
        ff(["-i", part_files[0], "-c", "copy", base])
    else:
        concat(part_files, os.path.join(seg_dir, f"{key}_parts.txt"), base)

    # Yorqinlik (yorugʻlik chizigʻi) va matn qatlamlari
    inputs: list[str] = ["-i", base, "-i", sweep]
    filters = [f"[0][1]overlay=x='-w+(W+w)*min(1,t/{max(dur,0.1):.3f})':y=0:format=auto[base0]"]
    cur = "base0"

    idx = 2          # kirish (input) indekslari
    tag = 0          # filtr nomlari uchun
    for layer in scene["layers"]:
        if layer["kind"] == "text":
            png = os.path.join(stills, layer["file"])
            inputs += ["-loop", "1", "-i", png]
            d = layer["delay"]
            filters.append(
                f"[{idx}]format=rgba,"
                f"scale=w='iw*(0.94+0.06*min(1,max(0,(t-{d:.3f})/0.3)))':h=-1:eval=frame,"
                f"fade=t=in:st={d:.3f}:d=0.3:alpha=1,setpts=PTS-STARTPTS[ov{tag}]"
            )
            filters.append(
                f"[{cur}][ov{tag}]overlay=x={layer['x']}:"
                f"y='{layer['y']}+30*(1-min(1,max(0,(t-{d:.3f})/0.38)))':format=auto[o{tag}]"
            )
            cur = f"o{tag}"
            idx += 1
            tag += 1
        elif layer["kind"] == "glow":
            png = os.path.join(stills, layer["file"])
            inputs += ["-loop", "1", "-i", png]
            d = layer["delay"]
            filters.append(
                f"[{idx}]format=rgba,eq=eval=frame:brightness='0.10+0.10*sin(2*PI*t/1.5)',"
                f"fade=t=in:st={d:.3f}:d=0.6:alpha=1,setpts=PTS-STARTPTS[gl{tag}]"
            )
            filters.append(f"[{cur}][gl{tag}]overlay=x={layer['x']}:y={layer['y']}:format=auto[g{tag}]")
            cur = f"g{tag}"
            idx += 1
            tag += 1
        elif layer["kind"] == "bar":
            d = layer["delay"]
            filters.append(
                f"[{cur}]drawbox=x={layer['x']}:y={layer['y']}:"
                f"w='min(1,max(0,(t-{d:.3f})/0.5))*{layer['w']}':h={layer['h']}:"
                f"color=0xE2202A@0.95:t=fill[bb{tag}]"
            )
            cur = f"bb{tag}"
            tag += 1

    filters.append(
        f"[{cur}]fade=t=out:st={max(0.0, dur - 0.30):.3f}:d=0.30:color=black,format=yuv420p[out]"
    )

    out = os.path.join(seg_dir, f"{key}.mp4")
    ff(inputs + [
        "-filter_complex", ";".join(filters),
        "-map", "[out]", "-t", f"{dur:.3f}",
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-an", out,
    ])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["9x16", "4x5"], default="9x16")
    args = ap.parse_args()

    fmt = args.format
    w, h = (1080, 1920) if fmt == "9x16" else (1080, 1350)
    aud_dir = os.path.join(BUILD, "audio")
    seg_dir = os.path.join(BUILD, "segments", fmt)
    stills = os.path.join(BUILD, "stills", fmt)
    os.makedirs(aud_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)

    keys = scene_keys()
    n = len(keys)

    # 1) Ovoz kliplari
    print(f"▸ Ovoz kliplari tayyorlanmoqda ({n} ta)...")
    for i in range(1, n + 1):
        ff([
            "-i", os.path.join(AUDIO_SRC, f"vo_{i:02d}.mp3"),
            "-af", f"silenceremove=start_periods=1:start_duration=0.05:start_threshold=-45dB:"
                   f"stop_periods=-1:stop_duration=0.25:stop_threshold=-45dB,atempo={SPEED}",
            "-ar", "44100", "-ac", "1", os.path.join(aud_dir, f"vo_{i:02d}.wav"),
        ])

    # 2) Davomiyliklar
    durations = {}
    for i, key in enumerate(keys, start=1):
        durations[key] = round(wav_duration(os.path.join(aud_dir, f"vo_{i:02d}.wav")) + GAP, 3)
    dur_path = os.path.join(BUILD, "durations.json")
    with open(dur_path, "w") as f:
        json.dump(durations, f, indent=2)
    print("  Sahna davomiyaliklari:", " ".join(f"{k}={v}" for k, v in durations.items()))

    # 3) Kadrlar va matn qatlamlari
    print("▸ Kadrlar va matn qatlamlari render qilinmoqda...")
    run([PY, os.path.join(HERE, "render_video.py"), "--format", fmt, "--durations", dur_path])
    with open(os.path.join(stills, "manifest.json")) as f:
        manifest = json.load(f)

    # 4) Sahnalar
    sweep = os.path.join(stills, "sweep.png")
    make_sweep(w, h, sweep)
    print("▸ Sahnalar yig'ilmoqda...")
    scene_files = []
    for scene in manifest["scenes"]:
        scene_files.append(build_scene(scene, stills, seg_dir, w, h, sweep))

    # 5) Birlashtirish + grain + ovoz
    print("▸ Birlashtirilmoqda va ovoz qo'shilmoqda...")
    merged = os.path.join(seg_dir, "merged.mp4")
    concat(scene_files, os.path.join(seg_dir, "scenes.txt"), merged)

    # Ovoz trekini jimliklar bilan yigʻish
    inputs = []
    for i in range(1, n + 1):
        inputs += ["-i", os.path.join(aud_dir, f"vo_{i:02d}.wav")]
    pads = "".join(f"[{i}]apad=pad_dur={GAP}[a{i}];" for i in range(n))
    ac = pads + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    voice = os.path.join(aud_dir, "vo_full.wav")
    ff(inputs + ["-filter_complex", ac, "-map", "[a]", "-c:a", "pcm_s16le", voice])

    out_video = os.path.join(OUTPUT, f"everest_mafia_{fmt}.mp4")
    ff([
        "-i", merged, "-i", voice,
        "-filter_complex", "[0:v]noise=alls=5:allf=t+u,format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "1", "-shortest",
        "-r", "30", out_video,
    ])

    # Ovozsiz variant
    ff(["-i", out_video, "-c:v", "copy", "-an", os.path.join(OUTPUT, f"everest_mafia_{fmt}_muted.mp4")])

    # Cover
    cover_src = os.path.join(stills, "cover.jpg")
    if os.path.exists(cover_src):
        ff(["-i", cover_src, "-vf", f"scale={w}:{h}", "-q:v", "3", os.path.join(OUTPUT, f"cover_{fmt}.jpg")])

    print("✓ Tayyor:", out_video)


if __name__ == "__main__":
    main()
