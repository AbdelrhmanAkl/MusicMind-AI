"""MusicMind AI: music genre classification application."""

import streamlit as st

st.set_page_config(
    page_title="MusicMind AI | Music Genre Recognition",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.musicmind.ui import components as ui  # noqa: E402
from src.musicmind.ui import sections  # noqa: E402
from src.musicmind.ui.theme import inject_theme  # noqa: E402


def main() -> None:
    inject_theme()
    ui.render(ui.brand_bar())

    try:
        model, config = sections.get_model()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Unable to initialize MusicMind AI: {exc}")
        st.stop()

    evaluation = sections.get_evaluation()
    accuracy_text = f"{evaluation['accuracy'] * 100:.2f}%" if evaluation else None

    ui.render(ui.hero(config["num_classes"], accuracy_text))
    sections.render_upload(config)
    sections.render_how_it_works(config)
    sections.render_genres(config, evaluation)
    sections.render_performance(config, evaluation)
    sections.render_about(config, model)
    sections.render_limitations(config, evaluation)
    ui.render(ui.footer())


main()
