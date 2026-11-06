"""Audio preprocessing utilities for MusicMind AI."""

from __future__ import annotations

import numpy as np
import librosa


SAMPLE_RATE = 22050
SEGMENT_DURATION = 3
SEGMENTS_PER_TRACK = 10

N_FFT = 2048
HOP_LENGTH = 512
N_MELS = 128

SAMPLES_PER_SEGMENT = SAMPLE_RATE * SEGMENT_DURATION
EXPECTED_AUDIO_LENGTH = SAMPLE_RATE * 30


def extract_track_segments(audio: np.ndarray) -> list[np.ndarray]:
    """Convert a mono audio waveform into normalized Mel spectrograms."""

    if audio.ndim != 1:
        raise ValueError("Audio input must be mono (one-dimensional).")

    if audio.size == 0:
        raise ValueError("Audio input is empty.")

    if not np.all(np.isfinite(audio)):
        raise ValueError("Audio contains invalid numerical values.")

    if len(audio) < EXPECTED_AUDIO_LENGTH:
        audio = np.pad(
            audio,
            (0, EXPECTED_AUDIO_LENGTH - len(audio))
        )

    audio = audio[:EXPECTED_AUDIO_LENGTH]

    segments = []

    for index in range(SEGMENTS_PER_TRACK):
        start = index * SAMPLES_PER_SEGMENT
        end = start + SAMPLES_PER_SEGMENT

        segment = audio[start:end]

        mel_spec = librosa.feature.melspectrogram(
            y=segment,
            sr=SAMPLE_RATE,
            n_fft=N_FFT,
            hop_length=HOP_LENGTH,
            n_mels=N_MELS,
            power=2.0
        )

        mel_db = librosa.power_to_db(
            mel_spec,
            ref=np.max
        )

        mel_db = np.clip(mel_db, -80, 0) / 80.0

        segments.append(mel_db.astype(np.float32))

    return segments
