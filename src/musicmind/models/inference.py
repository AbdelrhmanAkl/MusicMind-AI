"""Model inference utilities for MusicMind AI."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from tensorflow import keras

from src.musicmind.audio.preprocessing import extract_track_segments


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "models"
    / "musicmind_cnn_augmented_best.keras"
)

CONFIG_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "metadata"
    / "model_config.json"
)


def load_model_and_config():
    """Load the trained CNN and its metadata."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Model configuration not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8-sig") as file:
        config = json.load(file)

    model = keras.models.load_model(MODEL_PATH)

    return model, config


def predict_genre(
    audio: np.ndarray,
    model,
    config: dict
) -> dict:
    """Predict a song genre using majority voting across 10 segments."""

    segments = extract_track_segments(audio)

    expected_segments = config["segments_per_track"]

    if len(segments) != expected_segments:
        raise ValueError("Unexpected number of audio segments.")

    model_input = np.asarray(segments, dtype=np.float32)[..., np.newaxis]

    probabilities = model.predict(model_input, verbose=0)

    if probabilities.shape != (
        expected_segments,
        config["num_classes"]
    ):
        raise ValueError("Model output shape does not match configuration.")

    segment_predictions = np.argmax(probabilities, axis=1)

    votes = np.bincount(
        segment_predictions,
        minlength=config["num_classes"]
    )

    predicted_index = int(np.argmax(votes))
    predicted_genre = config["classes"][predicted_index]

    # Additive reporting fields: the decision rule above (majority voting) is
    # unchanged; these expose the CNN's per-segment softmax outputs for display.
    mean_probabilities = probabilities.mean(axis=0)

    return {
        "genre": predicted_genre,
        "mean_probabilities": {
            config["classes"][index]: float(value)
            for index, value in enumerate(mean_probabilities)
        },
        "segment_probabilities": probabilities.astype(float).tolist(),
        "votes": int(votes[predicted_index]),
        "total_segments": expected_segments,
        "vote_ratio": float(votes[predicted_index] / expected_segments),
        "segment_predictions": [
            config["classes"][int(index)]
            for index in segment_predictions
        ],
        "class_votes": {
            config["classes"][index]: int(count)
            for index, count in enumerate(votes)
        }
    }

