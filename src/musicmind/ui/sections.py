"""Page sections for the MusicMind AI interface."""

from __future__ import annotations

import hashlib
import logging

import streamlit as st

from src.musicmind.audio.loader import SAMPLE_RATE, SUPPORTED_FORMATS, load_audio
from src.musicmind.audio.validation import (
    MAX_UPLOAD_MB,
    probe_duration_seconds,
    validate_upload,
)
from src.musicmind.models.inference import predict_genre
from src.musicmind.reports import load_split_counts, load_test_evaluation, load_training_setup
from src.musicmind.ui import charts, components as ui
from src.musicmind.ui.constants import display_name

logger = logging.getLogger(__name__)

MIME_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4",
}

CHART_CONFIG = {"displayModeBar": False}


# ------------------------------------------------------------------ cached

@st.cache_resource(show_spinner="Loading MusicMind AI model...")
def get_model():
    from src.musicmind.models.inference import load_model_and_config

    return load_model_and_config()


@st.cache_data(show_spinner=False)
def get_evaluation() -> dict | None:
    return load_test_evaluation()


@st.cache_data(show_spinner=False)
def get_training_setup() -> dict | None:
    return load_training_setup()


@st.cache_data(show_spinner=False)
def get_split_counts() -> dict | None:
    return load_split_counts()


@st.cache_data(show_spinner=False, max_entries=8)
def run_analysis(audio_bytes: bytes, filename: str) -> dict:
    """Decode and classify a track. Identical uploads are served from cache."""
    model, config = get_model()
    audio = load_audio(audio_bytes, filename)
    result = predict_genre(audio, model, config)
    result["duration_seconds"] = float(len(audio)) / SAMPLE_RATE
    return result


# ------------------------------------------------------------------ helpers

def _extension(filename: str) -> str:
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def _friendly_error(exc: Exception, extension: str) -> str:
    if isinstance(exc, ValueError):
        message = str(exc)
        if "decode" in message.lower() and extension in {".mp3", ".m4a"}:
            message += " MP3/M4A decoding depends on the server's audio codecs; converting the file to WAV usually fixes this."
        return message
    return "Something went wrong while analysing this file. Please try a different audio file."


def _per_genre(evaluation: dict | None, classes: list[str]) -> dict[str, dict] | None:
    if not evaluation:
        return None
    report = evaluation.get("classification_report", {})
    metrics = {genre: report[genre] for genre in classes if genre in report}
    return metrics or None


# ------------------------------------------------------------------ upload

def render_upload(config: dict) -> None:
    formats = sorted(f.lstrip(".") for f in SUPPORTED_FORMATS)
    ui.render(
        ui.section_header(
            "01 &mdash; Upload",
            "Analyze a track",
            "Drop an audio file below. MusicMind AI listens to the first 30 seconds and predicts its genre.",
        )
    )

    uploaded = st.file_uploader(
        "Upload an audio file",
        type=formats,
        label_visibility="collapsed",
        help="Drag and drop an audio file or browse from your device.",
    )

    chips = "".join(f'<span class="mm-chip">{f.upper()}</span>' for f in formats)
    ui.render(
        f'<div class="mm-formats">{chips}<span class="mm-hint">Up to {MAX_UPLOAD_MB} MB &middot; first 30 seconds analyzed</span></div>'
    )

    if uploaded is None:
        return

    data = uploaded.getvalue()
    extension = _extension(uploaded.name)

    try:
        validate_upload(uploaded.name, len(data))
    except ValueError as exc:
        st.error(str(exc))
        return

    file_id = hashlib.sha256(data).hexdigest()
    duration = probe_duration_seconds(data)

    analysis = st.session_state.get("analysis")
    if analysis and analysis["file_id"] == file_id:
        render_results(analysis, config)
        return

    left, right = st.columns([3, 2], gap="large")
    with left:
        st.audio(data, format=MIME_TYPES.get(extension, "audio/wav"))
        if duration is not None and duration < 30:
            ui.render(
                ui.note(
                    f"<b>Short track ({duration:.0f}s).</b> The model expects 30 seconds, "
                    "so the remainder is padded with silence, which can reduce reliability.",
                    "warn",
                )
            )
    with right:
        ui.render(
            ui.file_card(uploaded.name, ui.format_size(len(data)), ui.format_duration(duration), extension.lstrip("."))
        )

    if st.button("Analyze track", type="primary", width="stretch"):
        error_message = None
        with st.status("Analyzing audio: decoding, extracting Mel spectrograms, running the CNN...", expanded=False) as status:
            try:
                result = run_analysis(data, uploaded.name)
            except Exception as exc:  # noqa: BLE001 - surfaced to the user in friendly form
                logger.exception("Audio analysis failed")
                error_message = _friendly_error(exc, extension)
                status.update(label="Analysis failed", state="error")
            else:
                st.session_state["analysis"] = {
                    "file_id": file_id,
                    "name": uploaded.name,
                    "size": len(data),
                    "extension": extension,
                    "audio": data,
                    "result": result,
                }
        if error_message:
            st.error(error_message)
        else:
            st.rerun()


# ------------------------------------------------------------------ results

def render_results(analysis: dict, config: dict) -> None:
    result = analysis["result"]
    classes = config["classes"]
    total = result["total_segments"]
    genre = result["genre"]
    votes = result["class_votes"]
    mean_prob = result["mean_probabilities"]

    ui.render(
        ui.section_header(
            "02 &mdash; Results",
            "Your track's musical identity",
            "Predictions come from majority voting across ten 3-second segments.",
        )
    )

    left, right = st.columns([3, 2], gap="large")
    with left:
        ui.render(ui.result_card(genre, result["votes"], total, mean_prob[genre]))
    with right:
        ui.render(
            ui.file_card(
                analysis["name"],
                ui.format_size(analysis["size"]),
                ui.format_duration(result.get("duration_seconds")),
                analysis["extension"].lstrip("."),
            )
        )
        st.audio(analysis["audio"], format=MIME_TYPES.get(analysis["extension"], "audio/wav"))

    duration = result.get("duration_seconds")
    if duration is not None and duration < 30:
        ui.render("<br>" + ui.note(
            f"<b>Short track ({duration:.0f}s).</b> The model expects 30 seconds, so the remainder was padded "
            "with silence, which can reduce reliability.",
            "warn",
        ))

    top_votes = max(votes.values())
    tied = [g for g in classes if votes[g] == top_votes]
    if len(tied) > 1:
        names = " and ".join(display_name(g) for g in tied)
        ui.render("<br>" + ui.note(
            f"<b>Close call.</b> {names} received {top_votes} votes each. "
            "The model resolves ties in favour of the first genre in its class order.",
            "warn",
        ))
    elif result["votes"] / total < 0.6:
        ui.render("<br>" + ui.note(
            "<b>Low segment agreement.</b> The segments disagree noticeably, so treat this prediction as uncertain.",
            "warn",
        ))

    ui.render(
        "<br>" + ui.note(
            "<b>Confidence is not correctness.</b> Segment agreement is the share of segments voting for the genre, "
            "and average probability is the CNN's mean softmax output. Neither is a calibrated measure, "
            "so a high value does not guarantee the prediction is right."
        )
    )

    tab_prob, tab_time, tab_rank = st.tabs(["Probability distribution", "Segment timeline", "Ranked genres"])
    with tab_prob:
        st.caption("Average softmax probability per genre across all 10 segments.")
        st.plotly_chart(charts.probability_chart(mean_prob, genre), config=CHART_CONFIG)
    with tab_time:
        st.caption("How the CNN scored each 3-second segment. Brighter cells mean higher probability.")
        st.plotly_chart(charts.segment_heatmap(result["segment_probabilities"], classes), config=CHART_CONFIG)
    with tab_rank:
        rows = sorted(
            ((g, votes[g], mean_prob[g]) for g in classes),
            key=lambda r: (r[0] == genre, r[1], r[2]),
            reverse=True,
        )
        ui.render(ui.ranking_table(rows, total))


# ------------------------------------------------------------------ info sections

def render_how_it_works(config: dict) -> None:
    ui.render(
        ui.section_header(
            "How it works",
            "From waveform to genre in four steps",
            "The same preprocessing used during training runs on every upload.",
        )
    )
    n_mels = config["n_mels"]
    seconds = config["segment_duration_seconds"]
    segments = config["segments_per_track"]
    height, width = config["input_shape"][0], config["input_shape"][1]
    steps = [
        ("Decode and resample", f"The file is decoded, mixed down to mono and resampled to <code>{config['sample_rate']:,} Hz</code>."),
        ("Segment the audio", f"The first {seconds * segments} seconds are split into {segments} segments of {seconds} seconds. Shorter tracks are zero-padded."),
        ("Mel spectrogram", f"Each segment becomes a <code>{n_mels}</code>-bin Mel spectrogram (FFT {config['n_fft']}, hop {config['hop_length']}), converted to decibels and scaled. Input shape: <code>{height}&times;{width}</code>."),
        ("CNN and majority vote", f"A convolutional network scores every segment. The genre with the most segment votes is the final prediction."),
    ]
    ui.render(ui.step_cards(steps))


def render_genres(config: dict, evaluation: dict | None) -> None:
    ui.render(
        ui.section_header(
            "Supported genres",
            f"{config['num_classes']} genres, one prediction",
            "The model always answers with one of these genres. Bars show each genre's F1-score on the held-out test set.",
        )
    )
    ui.render(ui.genre_grid(config["classes"], _per_genre(evaluation, config["classes"])))


def render_performance(config: dict, evaluation: dict | None) -> None:
    ui.render(
        ui.section_header(
            "Model performance",
            "Measured on a held-out test set",
            "These figures come from the stored test evaluation. The test tracks were not used for training or model selection.",
        )
    )
    if not evaluation:
        st.info("The stored test evaluation report was not found, so performance metrics are unavailable.")
        return

    ui.render(
        ui.stat_cards(
            [
                (f"{evaluation['accuracy'] * 100:.2f}%", "Accuracy", f"{evaluation['correct_predictions']} of {evaluation['test_tracks']} test tracks correct"),
                (f"{evaluation['macro_f1'] * 100:.2f}%", "Macro F1", "Average F1 across the 10 genres"),
                (f"{evaluation['balanced_accuracy'] * 100:.2f}%", "Balanced accuracy", "Mean per-genre recall"),
                (f"{evaluation['test_tracks']}", "Test tracks", "Held out from training"),
            ]
        )
    )

    classes = config["classes"]
    tab_f1, tab_cm, tab_table = st.tabs(["Per-genre F1", "Confusion matrix", "Detailed report"])
    metrics = _per_genre(evaluation, classes)
    with tab_f1:
        if metrics:
            st.plotly_chart(charts.f1_chart(metrics), config=CHART_CONFIG)
    with tab_cm:
        labels = evaluation.get("class_labels", classes)
        st.caption("Rows are true genres and columns are predicted genres. Cell values are track counts; colour shows the share of each true genre.")
        st.plotly_chart(charts.confusion_heatmap(evaluation["confusion_matrix"], labels), config=CHART_CONFIG)
    with tab_table:
        if metrics:
            body = "".join(
                f"""<tr><td>{display_name(g)}</td><td class="num">{m['precision'] * 100:.1f}%</td>
                <td class="num">{m['recall'] * 100:.1f}%</td><td class="num">{m['f1-score'] * 100:.1f}%</td>
                <td class="num">{int(m['support'])}</td></tr>"""
                for g, m in metrics.items()
            )
            ui.render(
                f"""<div class="mm-table-wrap"><table class="mm-table"><thead><tr><th>Genre</th>
                <th class="num">Precision</th><th class="num">Recall</th><th class="num">F1</th>
                <th class="num">Tracks</th></tr></thead><tbody>{body}</tbody></table></div>"""
            )


def render_about(config: dict, model) -> None:
    ui.render(
        ui.section_header(
            "About the model",
            "Architecture and data",
            "A compact CNN trained on Mel spectrogram segments of the GTZAN dataset.",
        )
    )
    splits = get_split_counts()
    setup = get_training_setup() or {}
    evaluation = get_evaluation() or {}

    total_tracks = sum(splits.values()) if splits else None
    split_text = (
        f"{splits.get('train', 0)} train &middot; {splits.get('validation', 0)} validation &middot; {splits.get('test', 0)} test"
        if splits else "Train, validation and test splits"
    )
    dataset_body = (
        f"GTZAN music genre dataset, {total_tracks} cleaned tracks across {config['num_classes']} genres. {split_text}."
        if total_tracks else f"GTZAN music genre dataset across {config['num_classes']} genres."
    )

    arch = evaluation.get("architecture") or setup.get("architecture") or config.get("model_name", "CNN")
    params = f"{model.count_params():,} parameters." if model is not None else ""

    training_bits = []
    if setup.get("optimizer"):
        lr = setup.get("learning_rate_initial")
        training_bits.append(f"{setup['optimizer']} optimizer" + (f", initial learning rate {lr}" if lr else ""))
    if setup.get("dropout") is not None:
        training_bits.append(f"dropout {setup['dropout']}")
    if setup.get("augmentation"):
        training_bits.append(f"{setup['augmentation']} augmentation")
    joined = ", ".join(training_bits)
    training_body = joined[:1].upper() + joined[1:] + "." if training_bits else "See the project notebook for training details."

    cards = [
        ("Dataset", dataset_body),
        ("Architecture", f"{arch}. {params} Input: <code>{'&times;'.join(map(str, config['input_shape']))}</code> Mel spectrogram."),
        ("Training", training_body),
        ("Inference", f"{config['segments_per_track']} segments per track, aggregated by {config['aggregation_method'].replace('_', ' ')}."),
    ]
    html = "".join(f'<div class="mm-card"><div class="mm-card-title">{t}</div><p>{b}</p></div>' for t, b in cards)
    ui.render(f'<div class="mm-grid mm-grid-4">{html}</div>')

    if model is not None:
        with st.expander("Layer summary"):
            lines: list[str] = []
            model.summary(print_fn=lines.append)
            st.code("\n".join(lines), language="text")


def render_limitations(config: dict, evaluation: dict | None) -> None:
    ui.render(
        ui.section_header(
            "Limitations",
            "What to keep in mind",
            "MusicMind AI is a research and portfolio system, not a guaranteed classifier.",
        )
    )
    items = []
    if evaluation:
        wrong = evaluation["incorrect_predictions"]
        total = evaluation["test_tracks"]
        items.append(f"<b>Predictions can be wrong.</b> {wrong} of {total} held-out test tracks ({wrong / total * 100:.0f}%) were misclassified.")

        report = evaluation.get("classification_report", {})
        labels = evaluation.get("class_labels", config["classes"])
        scored = {g: report[g] for g in labels if g in report}
        if scored:
            weakest = min(scored, key=lambda g: scored[g]["f1-score"])
            row = labels.index(weakest)
            counts = evaluation["confusion_matrix"][row]
            confusions = sorted(
                ((c, labels[i]) for i, c in enumerate(counts) if i != row and c > 0), reverse=True
            )
            detail = ""
            if confusions:
                detail = f" Most often it was confused with {display_name(confusions[0][1])} ({confusions[0][0]} of {int(scored[weakest]['support'])} tracks)."
            items.append(
                f"<b>Weakest genre: {display_name(weakest)}.</b> It reached {scored[weakest]['recall'] * 100:.0f}% recall "
                f"and {scored[weakest]['f1-score'] * 100:.0f}% F1 on the test set.{detail}"
            )
        items.append(f"<b>Small test set.</b> Metrics come from {total} tracks, so they carry real statistical uncertainty.")

    items += [
        "<b>Confidence is not correctness.</b> Segment agreement and softmax probabilities are not calibrated and can be high for wrong predictions.",
        "<b>Only 30 seconds are analyzed.</b> Only the first 30 seconds of a track are used, and shorter tracks are padded with silence.",
        "<b>Closed set of genres.</b> The model always picks one of the 10 trained genres, even for music that fits none of them or for non-music audio. It has not been evaluated on data outside GTZAN.",
    ]
    ui.render(ui.limitations(items))
