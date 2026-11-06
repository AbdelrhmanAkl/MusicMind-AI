"""Visual system for MusicMind AI: palette tokens and global CSS."""

from __future__ import annotations

import streamlit as st

# Palette (kept in sync with the CSS variables below and with charts.py)
BG = "#0A0A0F"
SURFACE = "#12121A"
SURFACE_2 = "#181823"
VIOLET = "#8B5CF6"
VIOLET_LIGHT = "#A78BFA"
VIOLET_DEEP = "#6D28D9"
TEXT = "#F4F4F8"
MUTED = "#9A9AB0"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0A0A0F;
    --surface: #12121A;
    --surface-2: #181823;
    --border: rgba(255, 255, 255, 0.08);
    --border-strong: rgba(167, 139, 250, 0.35);
    --text: #F4F4F8;
    --muted: #9A9AB0;
    --violet: #8B5CF6;
    --violet-light: #A78BFA;
    --violet-deep: #6D28D9;
    --radius: 18px;
}

html, body, [class*="css"], .stApp, .stMarkdown, button, input {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.stApp {
    background:
        radial-gradient(900px 480px at 12% -8%, rgba(109, 40, 217, 0.22), transparent 60%),
        radial-gradient(700px 420px at 92% 4%, rgba(139, 92, 246, 0.12), transparent 60%),
        var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

.mm-nav, .mm-nav *, .mm-hero, .mm-hero *, .mm-section, .mm-section *, .mm-card, .mm-card *,
.mm-result, .mm-result *, .mm-note, .mm-note *, .mm-table, .mm-table *, .mm-footer, .mm-footer *,
.mm-formats, .mm-formats *, .stTabs button, [data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] button, .stButton button {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ---------- Brand bar ---------- */
.mm-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 0 1.4rem 0;
}
.mm-brand { display: flex; align-items: center; gap: 0.7rem; }
.mm-logo {
    width: 38px; height: 38px; border-radius: 11px;
    background: linear-gradient(135deg, var(--violet-deep), var(--violet));
    display: flex; align-items: flex-end; justify-content: center;
    gap: 3px; padding: 9px 8px;
    box-shadow: 0 6px 22px rgba(109, 40, 217, 0.45);
}
.mm-logo i { display: block; width: 4px; border-radius: 2px; background: #fff; }
.mm-logo i:nth-child(1) { height: 9px; opacity: .85; }
.mm-logo i:nth-child(2) { height: 18px; }
.mm-logo i:nth-child(3) { height: 13px; opacity: .9; }
.mm-logo i:nth-child(4) { height: 7px; opacity: .8; }
.mm-brand-name { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.03em; }
.mm-brand-name span { color: var(--violet-light); }
.mm-pill {
    display: inline-flex; align-items: center; gap: 0.45rem;
    padding: 0.35rem 0.8rem; border-radius: 999px;
    background: rgba(139, 92, 246, 0.10); border: 1px solid var(--border-strong);
    color: var(--violet-light); font-size: 0.78rem; font-weight: 600;
}
.mm-dot { width: 7px; height: 7px; border-radius: 50%; background: #34D399; }

/* ---------- Hero ---------- */
.mm-hero { padding: 1.6rem 0 1.4rem 0; max-width: 860px; }
.mm-eyebrow {
    color: var(--violet-light); font-size: 0.76rem; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 0.9rem;
}
.mm-h1 {
    font-size: clamp(2.2rem, 5.4vw, 3.7rem); font-weight: 800; color: var(--text);
    line-height: 1.08; letter-spacing: -0.04em; margin: 0 0 1.1rem 0; padding: 0;
}
.mm-h1 .mm-grad {
    background: linear-gradient(90deg, var(--violet-light), var(--violet));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.mm-hero p { color: var(--muted); font-size: 1.08rem; line-height: 1.75; max-width: 680px; margin: 0; }

/* ---------- Section headers ---------- */
.mm-section { margin: 3.4rem 0 1.3rem 0; }
.mm-section .mm-eyebrow { margin-bottom: 0.5rem; }
.mm-h2 { color: var(--text); font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 700; margin: 0 0 0.5rem 0; padding: 0; }
.mm-section p { color: var(--muted); margin: 0; max-width: 700px; line-height: 1.65; }

/* ---------- Cards ---------- */
.mm-card {
    background: linear-gradient(180deg, var(--surface-2), var(--surface));
    border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1.4rem 1.5rem; height: 100%;
    transition: border-color .2s ease, transform .2s ease;
}
.mm-card:hover { border-color: var(--border-strong); }
.mm-grid { display: grid; gap: 1rem; margin-bottom: 1.2rem; }
.mm-grid-4 { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.mm-grid-5 { grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }
.mm-grid-3 { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }

.mm-step-num {
    width: 30px; height: 30px; border-radius: 9px; display: inline-flex;
    align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;
    color: var(--violet-light); background: rgba(139, 92, 246, 0.14);
    border: 1px solid var(--border-strong); margin-bottom: 0.9rem;
}
.mm-card-title { color: var(--text); font-size: 1.02rem; font-weight: 650; margin: 0 0 0.45rem 0; padding: 0; }
.mm-card p, .mm-card li { color: var(--muted); font-size: 0.92rem; line-height: 1.6; margin: 0; }
.mm-card code {
    background: rgba(139, 92, 246, 0.12); color: var(--violet-light);
    padding: 0.08rem 0.4rem; border-radius: 6px; font-size: 0.82rem;
}

.mm-stat-value { font-size: 2.1rem; font-weight: 800; letter-spacing: -0.03em; color: var(--text); line-height: 1.1; }
.mm-stat-label { color: var(--violet-light); font-size: 0.74rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.55rem; }
.mm-stat-sub { color: var(--muted); font-size: 0.82rem; margin-top: 0.3rem; }

.mm-genre { display: flex; flex-direction: column; gap: 0.5rem; }
.mm-genre-top { display: flex; justify-content: space-between; align-items: baseline; }
.mm-genre-name { font-size: 1.05rem; font-weight: 650; }
.mm-genre-idx { color: var(--muted); font-size: 0.75rem; font-weight: 600; }
.mm-bar { height: 5px; border-radius: 3px; background: rgba(255,255,255,0.07); overflow: hidden; }
.mm-bar > div { height: 100%; border-radius: 3px; background: linear-gradient(90deg, var(--violet-deep), var(--violet-light)); }
.mm-genre-meta { color: var(--muted); font-size: 0.78rem; }

/* ---------- Upload zone ---------- */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.07), rgba(18, 18, 26, 0.9));
    border: 1.5px dashed rgba(167, 139, 250, 0.5);
    border-radius: 22px;
    padding: 2.6rem 1.5rem;
    transition: border-color .2s ease, box-shadow .2s ease;
}
[data-testid="stFileUploaderDropzone"] {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 0.9rem; min-height: 230px; text-align: center;
}
[data-testid="stFileUploaderDropzone"]::before {
    content: "Drop your audio track here"; order: -1;
    font-size: 1.55rem; font-weight: 700; letter-spacing: -0.02em; color: var(--text);
}
[data-testid="stFileUploaderDropzone"] small { color: var(--muted); }
[data-testid="stFileUploader"]:has([data-testid="stFileChips"]) [data-testid="stFileUploaderDropzone"] {
    min-height: auto; padding: 1.1rem 1.3rem; flex-direction: row; justify-content: flex-start;
}
[data-testid="stFileUploader"]:has([data-testid="stFileChips"]) [data-testid="stFileUploaderDropzone"]::before { display: none; }
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--violet-light);
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.12), 0 12px 40px rgba(109, 40, 217, 0.18);
}
[data-testid="stFileUploaderDropzone"] button {
    background: rgba(139, 92, 246, 0.14); color: var(--violet-light);
    border: 1px solid var(--border-strong); border-radius: 10px; font-weight: 600;
}
[data-testid="stFileUploaderDropzone"] button:hover { background: rgba(139, 92, 246, 0.24); color: #fff; border-color: var(--violet-light); }
[data-testid="stFileChips"] { background: var(--surface-2); border-radius: 12px; }

.mm-formats { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.9rem 0 1.4rem 0; align-items: center; }
.mm-chip {
    padding: 0.22rem 0.65rem; border-radius: 8px; font-size: 0.74rem; font-weight: 600;
    color: var(--violet-light); background: rgba(139, 92, 246, 0.10); border: 1px solid var(--border);
}
.mm-hint { color: var(--muted); font-size: 0.82rem; }

/* ---------- Buttons ---------- */
.stButton > button, button[data-testid="stBaseButton-primary"] {
    border-radius: 12px; font-weight: 700; min-height: 3.1rem; font-size: 1rem;
    transition: transform .15s ease, box-shadow .2s ease, filter .2s ease;
}
.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, var(--violet-deep), var(--violet));
    border: none; color: #fff; box-shadow: 0 10px 30px rgba(109, 40, 217, 0.35);
}
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
    filter: brightness(1.1); transform: translateY(-1px); box-shadow: 0 14px 36px rgba(109, 40, 217, 0.45); color: #fff;
}
.stButton > button:disabled { opacity: 0.45; }
.stButton { margin-top: 1.1rem; }

/* ---------- Results ---------- */
.mm-result {
    position: relative; overflow: hidden; border-radius: 22px; padding: 1.8rem 1.9rem;
    background:
        radial-gradient(420px 220px at 100% 0%, rgba(139, 92, 246, 0.25), transparent 70%),
        linear-gradient(180deg, #1A1A28, #12121A);
    border: 1px solid var(--border-strong);
    box-shadow: 0 20px 60px rgba(76, 29, 149, 0.25);
}
.mm-result-row { display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap; }
.mm-result-label { color: var(--violet-light); font-size: 0.74rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; }
.mm-result-genre { font-size: clamp(2.4rem, 6vw, 3.6rem); font-weight: 800; letter-spacing: -0.04em; line-height: 1.05; margin: 0.35rem 0 0.6rem 0; }
.mm-result-sub { color: var(--muted); font-size: 0.95rem; line-height: 1.6; }
.mm-ring {
    --p: 0; width: 118px; height: 118px; border-radius: 50%; flex: none;
    background: conic-gradient(var(--violet-light) calc(var(--p) * 1%), rgba(255,255,255,0.08) 0);
    display: grid; place-items: center;
}
.mm-ring-inner {
    width: 94px; height: 94px; border-radius: 50%; background: #14141F;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.mm-ring-inner b { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.03em; }
.mm-ring-inner span { font-size: 0.64rem; color: var(--muted); font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
.mm-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.8rem; margin-top: 1.4rem; }
.mm-metric { background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: 12px; padding: 0.75rem 0.95rem; }
.mm-metric b { display: block; font-size: 1.15rem; font-weight: 700; }
.mm-metric span { color: var(--muted); font-size: 0.74rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }

.mm-file { display: flex; flex-direction: column; gap: 0.55rem; }
.mm-file-name { font-weight: 650; font-size: 1.02rem; word-break: break-all; }
.mm-kv { display: flex; justify-content: space-between; gap: 1rem; font-size: 0.88rem; color: var(--muted); border-top: 1px solid var(--border); padding-top: 0.5rem; }
.mm-kv b { color: var(--text); font-weight: 600; text-align: right; }

.mm-note {
    border-radius: 14px; padding: 0.9rem 1.1rem; font-size: 0.9rem; line-height: 1.6;
    border: 1px solid var(--border); background: rgba(255,255,255,0.03); color: var(--muted);
}
.mm-note b { color: var(--text); }
.mm-note.warn { border-color: rgba(251, 191, 36, 0.35); background: rgba(251, 191, 36, 0.06); }
.mm-note.info { border-color: var(--border-strong); background: rgba(139, 92, 246, 0.07); }

.mm-table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
.mm-table th { text-align: left; color: var(--muted); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.5rem 0.6rem; border-bottom: 1px solid var(--border); }
.mm-table td { padding: 0.62rem 0.6rem; border-bottom: 1px solid var(--border); color: var(--text); }
.mm-table tr.top td { color: var(--violet-light); font-weight: 700; }
.mm-table td.num, .mm-table th.num { text-align: right; font-variant-numeric: tabular-nums; }
.mm-table-wrap { overflow-x: auto; }

.mm-limits { display: grid; gap: 0.8rem; }
.mm-limit { display: flex; gap: 0.9rem; align-items: flex-start; }
.mm-limit-mark { flex: none; width: 8px; height: 8px; border-radius: 50%; background: var(--violet); margin-top: 0.5rem; }
.mm-limit p { color: var(--muted); font-size: 0.93rem; line-height: 1.65; margin: 0; }
.mm-limit b { color: var(--text); }

.mm-footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.84rem; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem; }
.mm-footer a { color: var(--violet-light); text-decoration: none; }
.mm-footer a:hover { text-decoration: underline; }

/* ---------- Streamlit widgets ---------- */
div[data-testid="stAudio"] { margin-top: 0.9rem; }
div[data-testid="stAudio"] audio { width: 100%; border-radius: 12px; color-scheme: dark; }
[data-testid="stStatus"], div[data-testid="stExpander"] details {
    background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
}
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { color: var(--muted); font-weight: 600; }
.stTabs [aria-selected="true"] { color: var(--violet-light); }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--violet); }
.stAlert { border-radius: 14px; }
hr { border-color: var(--border); }

@media (max-width: 640px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .mm-result { padding: 1.3rem 1.2rem; }
    .mm-nav .mm-pill { display: none; }
}
</style>
"""


def inject_theme() -> None:
    """Inject the global stylesheet once per run."""
    st.markdown(_CSS, unsafe_allow_html=True)
