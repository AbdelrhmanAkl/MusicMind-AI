"""Reusable HTML building blocks for the MusicMind AI interface.

Every function returns an HTML string; ``render`` sends it to Streamlit.
User-controlled text (e.g. file names) is always escaped.
"""

from __future__ import annotations

from html import escape

import streamlit as st

from src.musicmind.ui.constants import GITHUB_URL, display_name


def render(html: str) -> None:
    """Render an HTML fragment (blank lines are stripped to keep Markdown from splitting it)."""
    cleaned = "\n".join(line.strip() for line in html.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "Unknown"
    minutes, secs = divmod(int(round(seconds)), 60)
    return f"{minutes}:{secs:02d}"


def format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    return f"{size_bytes / 1024:.1f} KB"


# ---------------------------------------------------------------- layout

def brand_bar() -> str:
    return """
    <div class="mm-nav">
      <div class="mm-brand">
        <div class="mm-logo"><i></i><i></i><i></i><i></i></div>
        <div class="mm-brand-name">MusicMind<span> AI</span></div>
      </div>
      <div class="mm-pill"><span class="mm-dot"></span>CNN genre recognition</div>
    </div>
    """


def hero(num_genres: int, accuracy_text: str | None) -> str:
    stat = f" Held-out test accuracy: {accuracy_text}." if accuracy_text else ""
    return f"""
    <div class="mm-hero">
      <div class="mm-eyebrow">AI-powered audio intelligence</div>
      <div class="mm-h1">Hear the <span class="mm-grad">genre</span><br>behind every track.</div>
      <p>Upload a song and MusicMind AI converts it into Mel spectrograms, runs them
      through a convolutional neural network, and predicts one of {num_genres} music
      genres.{stat}</p>
    </div>
    """


def section_header(eyebrow: str, title: str, subtitle: str = "") -> str:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    return f"""
    <div class="mm-section">
      <div class="mm-eyebrow">{eyebrow}</div>
      <div class="mm-h2">{title}</div>
      {sub}
    </div>
    """


def note(text: str, kind: str = "info") -> str:
    return f'<div class="mm-note {kind}">{text}</div>'


def footer() -> str:
    return f"""
    <div class="mm-footer">
      <div>MusicMind AI &middot; TensorFlow, Keras, librosa and Streamlit</div>
      <div>Built by Abdelrahman Akl &middot; <a href="{GITHUB_URL}" target="_blank" rel="noopener">View on GitHub</a></div>
    </div>
    """


# ---------------------------------------------------------------- sections

def stat_cards(items: list[tuple[str, str, str]]) -> str:
    cards = "".join(
        f"""<div class="mm-card"><div class="mm-stat-value">{value}</div>
        <div class="mm-stat-label">{label}</div><div class="mm-stat-sub">{sub}</div></div>"""
        for value, label, sub in items
    )
    return f'<div class="mm-grid mm-grid-4">{cards}</div>'


def step_cards(steps: list[tuple[str, str]]) -> str:
    cards = "".join(
        f"""<div class="mm-card"><div class="mm-step-num">{index}</div>
        <div class="mm-card-title">{title}</div><p>{body}</p></div>"""
        for index, (title, body) in enumerate(steps, start=1)
    )
    return f'<div class="mm-grid mm-grid-4">{cards}</div>'


def genre_grid(genres: list[str], metrics: dict[str, dict] | None) -> str:
    cards = []
    for index, genre in enumerate(genres, start=1):
        meta, width = "", 0
        if metrics and genre in metrics:
            f1 = metrics[genre]["f1-score"]
            recall = metrics[genre]["recall"]
            width = round(f1 * 100)
            meta = f"F1 {f1 * 100:.0f}% &middot; Recall {recall * 100:.0f}%"
        cards.append(
            f"""<div class="mm-card mm-genre">
            <div class="mm-genre-top"><span class="mm-genre-name">{escape(display_name(genre))}</span>
            <span class="mm-genre-idx">{index:02d}</span></div>
            <div class="mm-bar"><div style="width:{width}%"></div></div>
            <div class="mm-genre-meta">{meta}</div></div>"""
        )
    return f'<div class="mm-grid mm-grid-5">{"".join(cards)}</div>'


def limitations(items: list[str]) -> str:
    rows = "".join(
        f'<div class="mm-limit"><div class="mm-limit-mark"></div><p>{text}</p></div>'
        for text in items
    )
    return f'<div class="mm-card"><div class="mm-limits">{rows}</div></div>'


# ---------------------------------------------------------------- results

def result_card(
    genre: str,
    votes: int,
    total: int,
    mean_probability: float,
) -> str:
    agreement = round(votes / total * 100)
    return f"""
    <div class="mm-result">
      <div class="mm-result-row">
        <div>
          <div class="mm-result-label">Predicted genre</div>
          <div class="mm-result-genre">{escape(display_name(genre))}</div>
          <div class="mm-result-sub">{votes} of {total} audio segments voted for this genre.</div>
        </div>
        <div class="mm-ring" style="--p:{agreement}">
          <div class="mm-ring-inner"><b>{agreement}%</b><span>agreement</span></div>
        </div>
      </div>
      <div class="mm-metrics">
        <div class="mm-metric"><b>{votes}/{total}</b><span>Segment votes</span></div>
        <div class="mm-metric"><b>{mean_probability * 100:.1f}%</b><span>Avg. softmax probability</span></div>
      </div>
    </div>
    """


def file_card(name: str, size_text: str, duration_text: str, extension: str) -> str:
    return f"""
    <div class="mm-card mm-file">
      <div class="mm-eyebrow" style="margin:0">Uploaded audio</div>
      <div class="mm-file-name">{escape(name)}</div>
      <div class="mm-kv"><span>Size</span><b>{escape(size_text)}</b></div>
      <div class="mm-kv"><span>Duration</span><b>{escape(duration_text)}</b></div>
      <div class="mm-kv"><span>Format</span><b>{escape(extension.upper())}</b></div>
    </div>
    """


def ranking_table(rows: list[tuple[str, int, float]], total: int) -> str:
    body = "".join(
        f"""<tr class="{'top' if rank == 1 else ''}"><td>{rank}</td>
        <td>{escape(display_name(genre))}</td>
        <td class="num">{votes}/{total}</td>
        <td class="num">{prob * 100:.1f}%</td></tr>"""
        for rank, (genre, votes, prob) in enumerate(rows, start=1)
    )
    return f"""
    <div class="mm-table-wrap"><table class="mm-table">
      <thead><tr><th>#</th><th>Genre</th><th class="num">Segment votes</th><th class="num">Avg. probability</th></tr></thead>
      <tbody>{body}</tbody>
    </table></div>
    """
