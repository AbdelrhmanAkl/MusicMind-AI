"""Read-only access to the stored evaluation reports."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "artifacts" / "reports"


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)
    except (OSError, ValueError):
        return None


def load_test_evaluation() -> dict | None:
    """Held-out TEST-set evaluation (final_test_evaluation.json)."""
    return _read_json(REPORTS_DIR / "final_test_evaluation.json")


def load_training_setup() -> dict | None:
    """Training hyper-parameters (final_model_experiment.json).

    Only configuration values are used from this file; its metrics are
    validation metrics and are never displayed as test results.
    """
    return _read_json(REPORTS_DIR / "final_model_experiment.json")


def load_split_counts() -> dict[str, int] | None:
    """Number of tracks per split, counted from data_split_manifest.csv."""
    path = REPORTS_DIR / "data_split_manifest.csv"
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            return dict(Counter(row["split"] for row in csv.DictReader(file)))
    except (OSError, KeyError, ValueError):
        return None
