"""Smoke tests for the MusicMind AI pipeline (run with: python -m pytest tests -q).

Audio is synthetic, so these tests check plumbing and invariants, not genre accuracy.
"""

from io import BytesIO

import numpy as np
import pytest
import soundfile as sf

from src.musicmind.audio.loader import SAMPLE_RATE, load_audio
from src.musicmind.audio.validation import MAX_UPLOAD_BYTES, validate_upload
from src.musicmind.models.inference import load_model_and_config, predict_genre


def _wav_bytes(seconds: float) -> bytes:
    t = np.arange(int(SAMPLE_RATE * seconds)) / SAMPLE_RATE
    buffer = BytesIO()
    sf.write(buffer, (0.3 * np.sin(2 * np.pi * 220 * t)).astype("float32"), SAMPLE_RATE, format="WAV")
    return buffer.getvalue()


@pytest.fixture(scope="module")
def model_and_config():
    return load_model_and_config()


@pytest.mark.parametrize("name,size", [("a.txt", 10), ("a.wav", 0), ("a.wav", MAX_UPLOAD_BYTES + 1)])
def test_validation_rejects(name, size):
    with pytest.raises(ValueError):
        validate_upload(name, size)


def test_validation_accepts():
    validate_upload("song.mp3", 1024)


@pytest.mark.parametrize("seconds", [5, 30])
def test_inference_invariants(model_and_config, seconds):
    model, config = model_and_config
    result = predict_genre(load_audio(_wav_bytes(seconds), "x.wav"), model, config)
    assert result["genre"] in config["classes"]
    assert sum(result["class_votes"].values()) == config["segments_per_track"]
    assert abs(sum(result["mean_probabilities"].values()) - 1.0) < 1e-3
    assert np.asarray(result["segment_probabilities"]).shape == (10, config["num_classes"])


def test_corrupt_audio_raises_friendly_error():
    with pytest.raises(ValueError):
        load_audio(b"not audio" * 50, "bad.mp3")
