# MusicMind AI
### Deep Learning-Based Music Genre Classification

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-orange?logo=tensorflow)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**MusicMind AI** is an end-to-end deep learning application designed to classify music into 10 distinct genres using Convolutional Neural Networks (CNNs) and Mel Spectrogram representations.

The system processes audio recordings, extracts time-frequency features, and generates genre predictions using segment-level inference and majority voting.

It also features an interactive **Streamlit web application**, allowing users to upload audio files and explore classification results through an intuitive interface.

**Live Demo:** [MusicMind AI](https://musicmind-ai.streamlit.app/)

**GitHub Repository:** [MusicMind-AI](https://github.com/AbdelrhmanAkl/MusicMind-AI)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Supported Genres](#supported-genres)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Model Architecture](#model-architecture)
- [Evaluation Results](#evaluation-results)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Run the Application](#run-the-application)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [Technologies](#technologies)
- [Author](#author)

---

## Overview

Music genre classification is a Music Information Retrieval (MIR) task that involves identifying the musical characteristics and genre of an audio recording.

MusicMind AI approaches this task using a Convolutional Neural Network trained on Mel Spectrograms, which represent audio signals in the time-frequency domain.

Rather than relying on a single prediction for an entire recording, the system:

1. Divides each audio recording into 10 non-overlapping segments.
2. Converts each segment into a Mel Spectrogram.
3. Uses the trained CNN to classify individual segments.
4. Aggregates predictions through majority voting.
5. Returns the final track-level genre prediction.

This segment-based approach provides a track-level classification based on multiple independent audio segments.

## Key Features

- **10-Class Classification:** Recognizes 10 distinct music genres.
- **CNN-Based Deep Learning:** Uses a custom Convolutional Neural Network architecture.
- **Mel Spectrogram Feature Extraction:** Converts raw audio into time-frequency representations.
- **Segment-Level Inference:** Analyzes 10 segments per recording.
- **Majority Voting:** Aggregates segment predictions into a final classification.
- **Interactive Streamlit Dashboard:** Provides an accessible interface for audio classification.
- **Multiple Audio Formats:** Supports WAV, MP3, OGG, FLAC, and M4A, subject to decoder compatibility.
- **Prediction Visualization:** Displays the predicted genre, segment agreement, average softmax probability per genre, a per-segment probability timeline and ranked genres.
- **Product-style Interface:** Dark violet UI with upload validation, audio playback, and sections for how it works, supported genres, held-out test metrics, model details and limitations.

## Supported Genres

MusicMind AI classifies audio recordings into the following 10 genres:

| # | Genre |
|---|---|
| 1 | Blues |
| 2 | Classical |
| 3 | Country |
| 4 | Disco |
| 5 | Hip-Hop |
| 6 | Jazz |
| 7 | Metal |
| 8 | Pop |
| 9 | Reggae |
| 10 | Rock |

## Dataset

The project uses the **GTZAN Music Genre Dataset**, a widely used benchmark dataset for music genre classification.

**Dataset Source:** [GTZAN Music Genre Classification – Kaggle](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification)

### Dataset Summary

| Property | Value |
|---|---:|
| Original Audio Tracks | 1,000 |
| Number of Genres | 10 |
| Cleaned Audio Tracks | 984 |
| Sample Rate | 22,050 Hz |
| Audio Duration | 30 seconds |
| Training Samples | 688 |
| Validation Samples | 148 |
| Test Samples | 148 |

### Data Cleaning and Splitting

Before training, the dataset was inspected and cleaned.

- Corrupted audio files were excluded.
- Identified duplicate tracks were removed.
- Audio recordings were standardized to a consistent format.
- Data splitting was performed at the original track level using stratified sampling.

**Important:** Splitting was performed before segment generation to prevent segments originating from the same track from appearing across different dataset splits.

This helps reduce data leakage and ensures a more reliable evaluation.

## Methodology

### 1. Audio Preprocessing

Each audio recording undergoes the following preprocessing steps:

- Audio loading and decoding.
- Conversion to mono.
- Resampling to 22,050 Hz.
- Standardization to 30 seconds.
- Division into 10 non-overlapping segments.

Each segment represents 3 seconds of audio.

### 2. Mel Spectrogram Extraction

Each audio segment is transformed into a Mel Spectrogram to capture relevant time-frequency characteristics.

| Parameter | Value |
|---|---:|
| Sample Rate | 22,050 Hz |
| FFT Size | 2,048 |
| Hop Length | 512 |
| Mel Bins | 128 |
| Segment Duration | 3 seconds |
| Spectrogram Shape | 128 × 130 |

The extracted spectrograms are converted into decibel representations, clipped to a fixed range, and normalized before being passed to the CNN.

### 3. Model Training

A Convolutional Neural Network was trained using the extracted Mel Spectrogram representations.

The training pipeline incorporated:

- Data augmentation to improve generalization.
- Batch normalization for more stable training.
- Dropout for regularization.
- Validation-based model selection.

The best-performing model was selected based on validation performance.

### 4. Track-Level Prediction

For an uploaded audio recording, the inference pipeline performs the following operations:

1. Preprocesses the audio recording.
2. Extracts 10 audio segments.
3. Generates a Mel Spectrogram for each segment.
4. Runs each spectrogram through the trained CNN.
5. Collects the predicted genre for every segment.
6. Applies majority voting to determine the final genre.

The final output represents the genre receiving the highest number of segment-level votes.

## Model Architecture

MusicMind AI uses an augmented Convolutional Neural Network (CNN) designed for spectrogram-based classification.

### Architecture Components

| Layer | Configuration |
|---|---|
| Input | 128 × 130 × 1 |
| Convolutional Block 1 | 32 Filters |
| Convolutional Block 2 | 64 Filters |
| Convolutional Block 3 | 128 Filters |
| Normalization | Batch Normalization |
| Activation | ReLU |
| Pooling | Max Pooling |
| Feature Aggregation | Global Average Pooling |
| Dense Layer | 128 Units |
| Regularization | Dropout (0.5) |
| Output | 10 Classes |
| Output Activation | Softmax |

**Model Input:** `(128, 130, 1)`

**Model Output:** `(10,)`

### Saved Model

The selected trained model is stored in Keras format:

```text
artifacts/models/musicmind_cnn_augmented_best.keras
```

## Evaluation Results

The final model was evaluated using an untouched held-out test set containing **148 audio tracks**.

### Overall Performance

| Metric | Score |
|---|---:|
| Test Accuracy | **82.43%** |
| Balanced Accuracy | **82.43%** |
| Macro F1-Score | **81.49%** |
| Weighted F1-Score | **81.48%** |

### Per-Class Performance

| Genre | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Blues | 0.94 | 1.00 | 0.97 |
| Classical | 0.88 | 1.00 | 0.94 |
| Country | 0.81 | 0.87 | 0.84 |
| Disco | 0.65 | 0.87 | 0.74 |
| Hip-Hop | 0.78 | 0.93 | 0.85 |
| Jazz | 0.87 | 0.87 | 0.87 |
| Metal | 0.92 | 0.79 | 0.85 |
| Pop | 0.75 | 0.86 | 0.80 |
| Reggae | 1.00 | 0.73 | 0.85 |
| Rock | 0.71 | 0.33 | 0.45 |

*Evaluation metrics are based on the held-out GTZAN test set. Results may differ when processing recordings from other datasets or real-world music sources.*

## Project Structure

```text
MusicMind-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .streamlit/config.toml
├── tests/test_pipeline.py
│
├── artifacts/
│   ├── metadata/
│   │   └── model_config.json
│   │
│   ├── models/
│   │   └── musicmind_cnn_augmented_best.keras
│   │
│   └── reports/
│       ├── data_split_manifest.csv
│       ├── final_model_experiment.json
│       ├── final_test_confusion_matrix.csv
│       ├── final_test_evaluation.json
│       └── final_test_predictions.csv
│
├── notebooks/
│   └── music_genre_classification.ipynb
│
└── src/
    └── musicmind/
        ├── audio/
        │   ├── loader.py
        │   ├── preprocessing.py
        │   └── validation.py
        │
        ├── models/
        │   └── inference.py
        │
        ├── reports.py
        │
        └── ui/
            ├── charts.py
            ├── components.py
            ├── constants.py
            ├── sections.py
            └── theme.py
```

## Installation

### Prerequisites

- Python 3.11
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/AbdelrhmanAkl/MusicMind-AI.git

cd MusicMind-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

## Run the Application

Launch the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the local URL provided by Streamlit, typically:

```text
http://localhost:8501
```

Upload an audio file to start the classification process and explore the predicted music genre.

## How It Works

The complete system follows this inference pipeline:

```text
          Audio Upload
               |
               v
          Audio Loading
               |
               v
       Mono Conversion
        & Resampling
               |
               v
       Audio Segmentation
          (10 Segments)
               |
               v
        Mel Spectrograms
               |
               v
           CNN Model
               |
               v
      Segment Predictions
               |
               v
        Majority Voting
               |
               v
        Predicted Genre
               |
               v
       Streamlit Dashboard
```

## Limitations

- The model was trained and evaluated using the GTZAN dataset.
- Generalization to music outside the training distribution is not guaranteed.
- Music genres can overlap in their acoustic characteristics.
- Rock achieved the lowest recall (0.33) in the held-out test evaluation.
- Audio quality, recording conditions, and genre combinations may influence predictions.
- Majority voting provides a final track-level prediction but does not guarantee that every segment belongs to the predicted genre.

## Technologies

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Deep Learning | TensorFlow, Keras |
| Audio Processing | Librosa, SoundFile |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Visualization | Plotly |
| Web Application | Streamlit |
| Development | Jupyter Notebook, Git, GitHub |

---

## Author

**Abdelrahman Akl**

AI & Machine Learning Engineer

- **GitHub:** [@AbdelrhmanAkl](https://github.com/AbdelrhmanAkl)
- **LinkedIn:** [Abdelrahman Akl](https://www.linkedin.com/in/abdelrahmanakl/)

---

*MusicMind AI is an end-to-end deep learning portfolio project demonstrating audio preprocessing, feature extraction, CNN development, model evaluation, track-level inference, and interactive deployment.*