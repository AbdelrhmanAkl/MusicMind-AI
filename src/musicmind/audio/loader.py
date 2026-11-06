"""Audio loading and validation utilities for MusicMind AI."""

from __future__ import annotations

from io import BytesIO

import librosa
import numpy as np
import soundfile as sf


SAMPLE_RATE = 22050
SUPPORTED_FORMATS = {".wav", ".mp3", ".ogg", ".flac", ".m4a"}


def load_audio(
    audio_bytes: bytes,
    filename: str
) -> np.ndarray:
    """Load audio bytes, convert to mono, and resample."""

    if not audio_bytes:
        raise ValueError("The uploaded audio file is empty.")

    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {extension or 'unknown'}"
        )

    try:
        audio, sample_rate = sf.read(
            BytesIO(audio_bytes),
            dtype="float32",
            always_2d=True
        )

    except (sf.SoundFileRuntimeError, ValueError, OSError):
        try:
            audio, sample_rate = librosa.load(
                BytesIO(audio_bytes),
                sr=None,
                mono=False
            )
        except Exception as exc:
            raise ValueError(
                "Unable to decode this audio file. Please upload a valid audio file."
            ) from exc

    if audio.ndim == 2:
        audio = np.mean(audio, axis=1) if audio.shape[1] <= 8 else np.mean(audio, axis=0)

    if audio.size == 0 or not np.all(np.isfinite(audio)):
        raise ValueError("The audio file contains invalid or empty audio data.")

    if sample_rate != SAMPLE_RATE:
        audio = librosa.resample(
            audio,
            orig_sr=sample_rate,
            target_sr=SAMPLE_RATE
        )

    return np.asarray(audio, dtype=np.float32)
