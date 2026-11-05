# -*- coding: utf-8 -*-
"""
Builds webapp/audio/*.mp3 and webapp/audio/manifest.json from listening_scripts.py.

Voices: Kokoro (Apache-2.0), runs locally, no API key.
Setup:  pip install -r scripts/requirements-audio.txt, ffmpeg on PATH, and kokoro-v1.0.onnx + voices-v1.0.bin
        from https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
Usage:  python scripts/generate_listening_audio.py <model-folder> [test:section ...]
        With no test:section list, every section is rebuilt.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from kokoro_onnx import Kokoro

from listening_scripts import NARRATOR_VOICE, SECTIONS, spoken

AUDIO_DIR = Path(__file__).resolve().parent.parent / "webapp" / "audio"
MANIFEST = AUDIO_DIR / "manifest.json"

SPEED = 0.95
SAMPLE_RATE = 24000
SENTENCE_GAP = 0.22
TURN_GAP = 0.45
PARAGRAPH_GAP = 0.8
INTRO_GAP = 2.0


def silence(seconds):
    return np.zeros(int(seconds * SAMPLE_RATE), dtype=np.float32)


def speak(kokoro, text, voice):
    lang = "en-gb" if voice.startswith("b") else "en-us"
    clips = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        audio, rate = kokoro.create(sentence, voice=voice, speed=SPEED, lang=lang)
        assert rate == SAMPLE_RATE, rate
        clips += [audio.astype(np.float32), silence(SENTENCE_GAP)]
    return np.concatenate(clips[:-1])


def build_section(kokoro, data):
    gap = PARAGRAPH_GAP if len(data["voices"]) == 1 else TURN_GAP
    clips = [speak(kokoro, data["intro"], NARRATOR_VOICE), silence(INTRO_GAP)]
    for speaker, text in data["turns"]:
        clips += [speak(kokoro, spoken(text), data["voices"][speaker]), silence(gap)]
    return np.concatenate(clips)


def write_mp3(samples, target):
    with tempfile.TemporaryDirectory() as folder:
        wav_path = Path(folder) / "section.wav"
        with wave.open(str(wav_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes((np.clip(samples, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
             "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "64k", str(target)],
            check=True,
        )


def main():
    model = Path(sys.argv[1])
    wanted = {tuple(int(n) for n in item.split(":")) for item in sys.argv[2:]} or set(SECTIONS)
    kokoro = Kokoro(str(model / "kokoro-v1.0.onnx"), str(model / "voices-v1.0.bin"))

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    for test, section in sorted(wanted):
        samples = build_section(kokoro, SECTIONS[(test, section)])
        stem = f"t{test}_s{section}"
        temp = AUDIO_DIR / f"{stem}.tmp.mp3"
        write_mp3(samples, temp)
        digest = hashlib.sha256(temp.read_bytes()).hexdigest()[:10]
        for old in AUDIO_DIR.glob(f"{stem}-*.mp3"):
            old.unlink()
        final = AUDIO_DIR / f"{stem}-{digest}.mp3"
        temp.rename(final)
        seconds = round(len(samples) / SAMPLE_RATE)
        manifest.setdefault(str(test), {})[str(section)] = {"url": f"/audio/{final.name}", "seconds": seconds}
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        print(f"{final.name}: {seconds // 60}:{seconds % 60:02d}, {final.stat().st_size / 1048576:.1f} MB", flush=True)


if __name__ == "__main__":
    main()
