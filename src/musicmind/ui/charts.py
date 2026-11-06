"""Plotly charts styled for the MusicMind AI dark theme."""

from __future__ import annotations

import plotly.graph_objects as go

from src.musicmind.ui.constants import display_name
from src.musicmind.ui.theme import MUTED, TEXT, VIOLET, VIOLET_DEEP, VIOLET_LIGHT

_MUTED_BAR = "#3B3560"
_SCALE = [[0.0, "#14141F"], [0.35, VIOLET_DEEP], [1.0, VIOLET_LIGHT]]


def _base_layout(height: int, **extra) -> dict:
    layout = dict(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT, size=13),
        margin=dict(l=10, r=20, t=10, b=10),
        hoverlabel=dict(bgcolor="#1A1A28", font_color=TEXT, bordercolor=VIOLET),
    )
    layout.update(extra)
    return layout


def probability_chart(mean_probabilities: dict[str, float], predicted: str) -> go.Figure:
    """Horizontal bars: mean softmax probability per genre, highest first."""
    ordered = sorted(mean_probabilities.items(), key=lambda kv: kv[1], reverse=True)
    names = [display_name(g) for g, _ in ordered]
    values = [v * 100 for _, v in ordered]
    colors = [VIOLET_LIGHT if g == predicted else _MUTED_BAR for g, _ in ordered]

    fig = go.Figure(
        go.Bar(
            x=values, y=names, orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in values], textposition="outside",
            textfont=dict(color=TEXT), cliponaxis=False,
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(
            380,
            xaxis=dict(range=[0, max(values) * 1.18 or 1], showgrid=False, visible=False),
            yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(color=TEXT)),
            bargap=0.35,
        )
    )
    return fig


def segment_heatmap(segment_probabilities: list[list[float]], classes: list[str]) -> go.Figure:
    """Heatmap: softmax probability of each genre in each 3-second segment."""
    z = [[row[i] * 100 for row in segment_probabilities] for i in range(len(classes))]
    x = [f"{i * 3}-{i * 3 + 3}s" for i in range(len(segment_probabilities))]
    fig = go.Figure(
        go.Heatmap(
            z=z, x=x, y=[display_name(c) for c in classes],
            colorscale=_SCALE, zmin=0, zmax=100,
            colorbar=dict(title=dict(text="%", font=dict(color=MUTED)), tickfont=dict(color=MUTED), outlinewidth=0, thickness=12),
            hovertemplate="Segment %{x}<br>%{y}: %{z:.1f}%<extra></extra>",
            xgap=2, ygap=2,
        )
    )
    fig.update_layout(
        **_base_layout(
            380,
            xaxis=dict(tickfont=dict(color=MUTED, size=11), side="bottom"),
            yaxis=dict(autorange="reversed", tickfont=dict(color=TEXT)),
        )
    )
    return fig


def f1_chart(per_genre: dict[str, dict]) -> go.Figure:
    """Per-genre F1-score on the held-out test set."""
    ordered = sorted(per_genre.items(), key=lambda kv: kv[1]["f1-score"])
    names = [display_name(g) for g, _ in ordered]
    values = [m["f1-score"] * 100 for _, m in ordered]
    fig = go.Figure(
        go.Bar(
            x=values, y=names, orientation="h",
            marker=dict(color=values, colorscale=_SCALE, cmin=30, cmax=100, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in values], textposition="outside",
            textfont=dict(color=TEXT), cliponaxis=False,
            hovertemplate="%{y}: F1 %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(
            400,
            xaxis=dict(range=[0, 112], showgrid=False, visible=False),
            yaxis=dict(showgrid=False, tickfont=dict(color=TEXT)),
            bargap=0.35,
        )
    )
    return fig


def confusion_heatmap(matrix: list[list[int]], labels: list[str]) -> go.Figure:
    """Test-set confusion matrix; colour = row-normalised share, label = count."""
    names = [display_name(label) for label in labels]
    normalised = [
        [(value / sum(row) if sum(row) else 0.0) for value in row] for row in matrix
    ]
    fig = go.Figure(
        go.Heatmap(
            z=normalised, x=names, y=names, colorscale=_SCALE, zmin=0, zmax=1,
            text=matrix, texttemplate="%{text}", textfont=dict(color=TEXT, size=12),
            showscale=False, xgap=2, ygap=2,
            hovertemplate="True: %{y}<br>Predicted: %{x}<br>Tracks: %{text}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(
            470,
            xaxis=dict(title=dict(text="Predicted", font=dict(color=MUTED)), tickfont=dict(color=MUTED), tickangle=-35),
            yaxis=dict(title=dict(text="True genre", font=dict(color=MUTED)), autorange="reversed", tickfont=dict(color=TEXT)),
        )
    )
    return fig
