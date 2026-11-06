"""Upload validation helpers for MusicMind AI."""

from __future__ import annotations

from io import BytesIO

import soundfile as sf

from src.musicmind.audio.loader import SUPPORTED_FORMATS

MAX_UPLOAD_MB = 50
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024


def validate_upload(filename: str, size_bytes: int) -> None:
    """Raise ValueError with a user-friendly message if the upload is unusable."""

    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in SUPPORTED_FORMATS:
        supported = ", ".join(sorted(f.lstrip(".").upper() for f in SUPPORTED_FORMATS))
        raise ValueError(
            f"Unsupported file type ({extension or 'no extension'}). "
            f"Please upload one of: {supported}."
        )

    if size_bytes <= 0:
        raise ValueError("The uploaded file is empty.")

    if size_bytes > MAX_UPLOAD_BYTES:
        raise ValueError(
            f"This file is {size_bytes / (1024 * 1024):.2f} MB. "
            f"The maximum supported size is {MAX_UPLOAD_MB} MB."
        )


def probe_duration_seconds(audio_bytes: bytes) -> float | None:
    """Return the audio duration without full decoding, or None if unavailable."""

    try:
        info = sf.info(BytesIO(audio_bytes))
        if info.samplerate > 0 and info.frames > 0:
            return float(info.frames) / float(info.samplerate)
    except Exception:
        return None
    return None
