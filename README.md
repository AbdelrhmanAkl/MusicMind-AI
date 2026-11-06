\# MusicMind AI

\### Deep Learning-Based Music Genre Classification



\[!\[Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)

\[!\[TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-orange?logo=tensorflow)](https://www.tensorflow.org/)

\[!\[Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit)](https://streamlit.io/)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



\*\*MusicMind AI\*\* is a deep learning-powered music genre classification system that analyzes audio signals using Convolutional Neural Networks (CNNs) and Mel Spectrograms to classify music into 10 distinct genres.



The project includes an interactive Streamlit web application where users can upload audio files and receive genre predictions based on segment-level analysis and majority voting.



\*\*Live Demo:\*\* https://musicmind-ai.streamlit.app/



\*\*GitHub Repository:\*\* https://github.com/AbdelrhmanAkl/MusicMind-AI



\---



\## Table of Contents



\- \[Overview](#overview)

\- \[Key Features](#key-features)

\- \[Supported Genres](#supported-genres)

\- \[Dataset](#dataset)

\- \[Methodology](#methodology)

\- \[Model Architecture](#model-architecture)

\- \[Evaluation Results](#evaluation-results)

\- \[Project Structure](#project-structure)

\- \[Installation](#installation)

\- \[Run the Application](#run-the-application)

\- \[How It Works](#how-it-works)

\- \[Limitations](#limitations)

\- \[Technologies](#technologies)



\---



\## Overview



Music genre classification is a music information retrieval task that aims to identify the musical style of an audio recording.



MusicMind AI approaches this problem using a CNN trained on Mel Spectrogram representations of audio signals.



Instead of classifying an entire track in a single prediction, the system divides the audio into multiple segments, predicts the genre of each segment, and combines the predictions using majority voting.



This approach provides a track-level prediction based on multiple audio segments.



\## Key Features



\- \*\*10-Class Classification:\*\* Identifies 10 different music genres.

\- \*\*CNN-Based Architecture:\*\* Uses a Convolutional Neural Network for spectrogram-based classification.

\- \*\*Mel Spectrogram Processing:\*\* Converts audio signals into time-frequency representations.

\- \*\*Segment-Based Prediction:\*\* Analyzes 10 audio segments per track.

\- \*\*Majority Voting:\*\* Aggregates segment predictions into a final genre.

\- \*\*Interactive Web Application:\*\* Built with Streamlit.

\- \*\*Audio Upload:\*\* Supports WAV, MP3, OGG, FLAC, and M4A extensions, subject to decoder compatibility.

\- \*\*Prediction Visualization:\*\* Displays genre predictions and segment vote distribution.



\## Supported Genres



The model classifies music into the following 10 genres:



1\. Blues

2\. Classical

3\. Country

4\. Disco

5\. Hip-Hop

6\. Jazz

7\. Metal

8\. Pop

9\. Reggae

10\. Rock



\## Dataset



The project uses the \*\*GTZAN Music Genre Dataset\*\*.



Dataset source:



\[GTZAN Music Genre Classification - Kaggle](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification)



\### Dataset Summary



| Property | Value |

|---|---:|

| Original audio tracks | 1,000 |

| Genres | 10 |

| Clean tracks used | 984 |

| Audio sample rate | 22,050 Hz |

| Audio duration | 30 seconds |

| Training samples | 688 |

| Validation samples | 148 |

| Test samples | 148 |



The dataset was inspected and cleaned before model training. Corrupted audio and identified duplicate tracks were excluded.



The data was split at the original track level using stratified sampling to prevent segments from the same track from appearing across different splits.



\## Methodology



\### 1. Audio Preprocessing



\- Load audio files and convert them to mono.

\- Resample audio to 22,050 Hz.

\- Standardize audio length to 30 seconds.

\- Divide each track into 10 non-overlapping segments.

\- Each segment represents 3 seconds of audio.



\### 2. Mel Spectrogram Extraction



Each audio segment is transformed into a Mel Spectrogram using:



| Parameter | Value |

|---|---:|

| Sample Rate | 22,050 Hz |

| FFT Size | 2,048 |

| Hop Length | 512 |

| Mel Bins | 128 |

| Segment Duration | 3 seconds |

| Spectrogram Shape | 128 × 130 |



The spectrogram values are converted to decibels, clipped to a fixed range, and normalized before being passed to the CNN.



\### 3. Model Training



A CNN architecture was trained using Mel Spectrogram inputs.



The training pipeline included data augmentation and validation-based model selection.



\### 4. Track-Level Prediction



For each uploaded track:



1\. Extract 10 Mel Spectrogram segments.

2\. Generate a prediction for each segment.

3\. Count the predicted genres.

4\. Select the genre with the highest number of votes.



The final prediction is determined by majority voting.



\## Model Architecture



The selected model is an augmented CNN consisting of:



\- Convolutional Block 1: 32 filters

\- Convolutional Block 2: 64 filters

\- Convolutional Block 3: 128 filters

\- Batch Normalization

\- ReLU Activation

\- Max Pooling

\- Global Average Pooling

\- Dense Layer: 128 units

\- Dropout: 0.5

\- Output Layer: 10 classes with Softmax activation



\*\*Model Input:\*\* `(128, 130, 1)`



\*\*Model Output:\*\* `(10,)`



The trained model is saved in Keras format:



`artifacts/models/musicmind\_cnn\_augmented\_best.keras`



\## Evaluation Results



The final model was evaluated on an untouched held-out test set containing 148 tracks.



\### Overall Performance



| Metric | Score |

|---|---:|

| Test Accuracy | \*\*82.43%\*\* |

| Balanced Accuracy | \*\*82.43%\*\* |

| Macro F1-Score | \*\*81.49%\*\* |

| Weighted F1-Score | \*\*81.48%\*\* |



\### Per-Class Performance



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



\*Evaluation metrics are based on the held-out test set and reflect performance on this dataset, not a guarantee of accuracy on arbitrary real-world recordings.\*



\## Project Structure



```text

MusicMind-AI/

│

├── app.py

├── requirements.txt

├── .gitignore

│

├── artifacts/

│   ├── metadata/

│   │   └── model\_config.json

│   │

│   ├── models/

│   │   └── musicmind\_cnn\_augmented\_best.keras

│   │

│   └── reports/

│       ├── data\_split\_manifest.csv

│       ├── final\_model\_experiment.json

│       ├── final\_test\_confusion\_matrix.csv

│       ├── final\_test\_evaluation.json

│       └── final\_test\_predictions.csv

│

├── notebooks/

│   └── music\_genre\_classification.ipynb

│

└── src/

&#x20;   └── musicmind/

&#x20;       ├── audio/

&#x20;       │   ├── loader.py

&#x20;       │   └── preprocessing.py

&#x20;       │

&#x20;       └── models/

&#x20;           └── inference.py

```



\## Installation



\### Prerequisites



\- Python 3.11

\- Git



\### 1. Clone the Repository



```bash

git clone https://github.com/AbdelrhmanAkl/MusicMind-AI.git

cd MusicMind-AI

```



\### 2. Create a Virtual Environment



```bash

python -m venv .venv

```



Activate it on Windows:



```powershell

.venv\\Scripts\\Activate.ps1

```



\### 3. Install Dependencies



```bash

python -m pip install --upgrade pip

pip install -r requirements.txt

```



\## Run the Application



Start the Streamlit application:



```bash

python -m streamlit run app.py

```



Open the local URL provided by Streamlit, usually:



`http://localhost:8501`



Upload an audio file and let MusicMind AI analyze its musical characteristics.



\## How It Works



```text

&#x20;         Audio Upload

&#x20;               |

&#x20;               v

&#x20;       Audio Loading

&#x20;               |

&#x20;               v

&#x20;      Mono Conversion

&#x20;      \& Resampling

&#x20;               |

&#x20;               v

&#x20;      Audio Segmentation

&#x20;         (10 Segments)

&#x20;               |

&#x20;               v

&#x20;     Mel Spectrograms

&#x20;               |

&#x20;               v

&#x20;         CNN Model

&#x20;               |

&#x20;               v

&#x20;     Segment Predictions

&#x20;               |

&#x20;               v

&#x20;       Majority Voting

&#x20;               |

&#x20;               v

&#x20;      Predicted Genre

&#x20;               |

&#x20;               v

&#x20;      Streamlit Dashboard

```



\## Limitations



\- The model is trained and evaluated using the GTZAN dataset.

\- Performance may vary with music outside the training dataset.

\- Genre boundaries can overlap, making some recordings difficult to classify.

\- Rock showed the weakest recall in the held-out evaluation.

\- Audio quality, recording conditions, and genre mixing may affect predictions.



\## Technologies



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



\---



\## Author



\*\*Abdelrahman Akl\*\*



AI \& Machine Learning Engineer



\- GitHub: \[@AbdelrhmanAkl](https://github.com/AbdelrhmanAkl)

\- LinkedIn: \[Abdelrahman Akl](https://www.linkedin.com/in/abdelrahmanakl/)



\---



\*Built as an end-to-end deep learning portfolio project, covering audio preprocessing, CNN model development, evaluation, inference, and interactive deployment.\*

