import os
from datetime import datetime

import lameenc
import numpy as np
import soundfile as sf
from transformers import pipeline

CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)

PROMPT = "lofi hip hop radio - beats to relax/study to"

musicgen = pipeline("text-to-audio", model="facebook/musicgen-small")


def generate_wav(prompt: str, duration_sec: int = 15) -> str:
    print("[1] MusicGen 生成中...")
    result = musicgen(
        prompt, forward_params={"do_sample": True, "max_new_tokens": duration_sec * 50}
    )

    audio: np.ndarray = result["audio"]
    audio = np.squeeze(audio)
    wav_path = os.path.join(CACHE_DIR, "temp.wav")

    sf.write(wav_path, audio, samplerate=16000)
    return wav_path


def wav_to_numpy(wav_path: str) -> tuple[np.ndarray, int]:
    print("[2] WAV 読み込み → NumPy 変換中...")
    data, sr = sf.read(wav_path, dtype="float32")
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    return data, sr


def build_looped_audio(audio: np.ndarray, sr: int) -> np.ndarray:
    print("[3] 4連結 + フェードアウト中...")
    looped = np.tile(audio, 4)

    fade_samples = int(sr * 2)
    fade_curve = np.linspace(1.0, 0.0, fade_samples)
    looped[-fade_samples:] *= fade_curve
    return looped


def save_mp3(audio: np.ndarray, sr: int) -> str:
    print("[4] MP3 書き出し中...")
    pcm16 = (audio * 32767).astype(np.int16).tobytes()

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sr)
    encoder.set_channels(1)
    encoder.set_quality(2)

    mp3_data = encoder.encode(pcm16)
    mp3_data += encoder.flush()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mp3_path = os.path.join(CACHE_DIR, f"bgm_{timestamp}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(mp3_data)
    return mp3_path


if __name__ == "__main__":
    wav = generate_wav(PROMPT)
    audio, sr = wav_to_numpy(wav)
    looped_audio = build_looped_audio(audio, sr)
    final = save_mp3(looped_audio, sr)
    print(f"[完了] 生成MP3: {final}")
