"""MusicMind AI — Music Genre Classification Application."""

import streamlit as st

from src.musicmind.models.inference import load_model_and_config


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="MusicMind AI | Music Genre Recognition",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# Global Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #0B1020;
            color: #F1F5F9;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .brand {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            color: #F8FAFC;
        }

        .brand span {
            color: #8B7CFF;
        }

        .subtitle {
            color: #94A3B8;
            font-size: 0.95rem;
            margin-top: -8px;
        }

        .hero {
            padding: 3rem 0 2rem 0;
        }

        .hero-title {
            font-size: clamp(2.2rem, 5vw, 3.6rem);
            font-weight: 800;
            letter-spacing: -2px;
            line-height: 1.15;
            color: #F8FAFC;
        }

        .hero-title span {
            color: #9B8CFF;
        }

        .hero-description {
            color: #94A3B8;
            font-size: 1.05rem;
            line-height: 1.8;
            max-width: 680px;
        }

        .section-label {
            color: #A5B4FC;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        div[data-testid="stFileUploader"] {
            background: #131B30;
            border: 1px dashed #495477;
            border-radius: 16px;
            padding: 1rem;
        }

        .stButton > button {
            background: #8B7CFF;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            min-height: 3rem;
        }

        .stButton > button:hover {
            background: #7563F5;
            color: white;
            border: none;
        }

        .stAlert {
            border-radius: 12px;
        }

        div[data-testid="stAudio"] {
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Model Loading
# --------------------------------------------------

@st.cache_resource(show_spinner="Loading MusicMind AI model...")
def get_model():
    return load_model_and_config()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="brand">MusicMind<span> AI</span></div>
    <div class="subtitle">Intelligent Music Genre Recognition</div>
    <div class="hero">
        <div class="section-label">AI-POWERED AUDIO INTELLIGENCE</div>
        <div class="hero-title">
            Discover the <span>sound</span><br>
            behind every song.
        </div>
        <p class="hero-description">
            Upload an audio track and let our deep learning model
            analyze its sound patterns to identify its musical genre.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Model Initialization
# --------------------------------------------------

try:
    model, config = get_model()
    st.session_state["model"] = model
    st.session_state["config"] = config

except Exception as exc:
    st.error(f"Unable to initialize MusicMind AI: {exc}")
    st.stop()


st.success("MusicMind AI is ready to analyze your music.")

# --------------------------------------------------
# Audio Upload Section
# --------------------------------------------------

st.markdown(
    '<div class="section-label">01 — UPLOAD YOUR TRACK</div>',
    unsafe_allow_html=True,
)

st.markdown("### Let's analyze your music")

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "ogg", "flac", "m4a"],
    help="Upload an audio track to identify its musical genre.",
)

if uploaded_file is not None:

    st.audio(uploaded_file)

    st.caption(
        f"File: {uploaded_file.name} · "
        f"Size: {uploaded_file.size / (1024 * 1024):.2f} MB"
    )

    analyze_button = st.button(
        "Analyze Track",
        use_container_width=True,
    )

    if analyze_button:

        from src.musicmind.audio.loader import load_audio
        from src.musicmind.models.inference import predict_genre

        try:
            with st.spinner("Analyzing audio patterns..."):

                audio = load_audio(
                    uploaded_file.getvalue(),
                    uploaded_file.name,
                )

                result = predict_genre(
                    audio,
                    st.session_state["model"],
                    st.session_state["config"],
                )

                st.session_state["prediction"] = result
                st.session_state["analyzed_filename"] = uploaded_file.name

        except Exception as exc:
            st.error(f"Audio analysis failed: {exc}")


# --------------------------------------------------
# Prediction Results
# --------------------------------------------------

if "prediction" in st.session_state:

    result = st.session_state["prediction"]

    st.markdown("---")

    st.markdown(
        '<div class="section-label">02 — ANALYSIS RESULTS</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Your track's musical identity")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #191F3A, #25234A);
            border: 1px solid #6256A8;
            border-radius: 18px;
            padding: 2rem;
            margin: 1rem 0;
        ">
            <div style="color:#A5B4FC; font-size:0.85rem;">
                PREDICTED GENRE
            </div>
            <div style="
                font-size:2.8rem;
                font-weight:800;
                color:#FFFFFF;
                text-transform:capitalize;
                margin:0.5rem 0;
            ">
                {result["genre"]}
            </div>
            <div style="color:#94A3B8;">
                Segment Agreement:
                {result["votes"]}/{result["total_segments"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Segment agreement measures how consistently the model "
        "classified the audio segments. It is not a calibrated confidence score."
    )

    import plotly.express as px

    chart_data = {
        "Genre": list(result["class_votes"].keys()),
        "Votes": list(result["class_votes"].values()),
    }

    fig = px.bar(
        chart_data,
        x="Votes",
        y="Genre",
        orientation="h",
        text="Votes",
        color="Votes",
        color_continuous_scale=["#343B60", "#9B8CFF"],
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0",
        xaxis_title="Number of Segment Votes",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=20, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)