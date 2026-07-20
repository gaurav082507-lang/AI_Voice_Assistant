# AI Voice Assistant

An interactive, end-to-end AI Voice Assistant application built with Python and Streamlit. This application allows users to speak into their microphone, transcribes the audio locally using Whisper, processes the query through a custom AI agent, and vocalizes the response using a high-performance local Text-to-Speech (TTS) pipeline.

## 🚀 Features

*   **Voice-In, Voice-Out:** Seamlessly speak to the assistant and hear its responses back.
*   **Local Audio Preprocessing:** Efficient audio handling via `audio_preprocess.py`.
*   **Whisper Transcription:** Local or API-driven speech-to-text capabilities using `whisper_model.py`.
*   **Fast Text-to-Speech:** Uses a high-quality ONNX runtime TTS engine (`en_US-lessac-medium.onnx`) for near-instant speech synthesis.
*   **Streamlit Web Interface:** A clean, user-friendly UI configured with a modern dark theme out of the box.
*   **Customizable AI Persona:** Easily adjust the assistant's behavior and system guidelines within `streamlit_app.py`.

## 📁 Repository Structure

*   `streamlit_app.py`: The main application entry point and user interface.
*   `audio_preprocess.py`: Handles audio buffering, formats, and preprocessing tasks.
*   `whisper_model.py`: Manages the speech-to-text inference logic using Whisper.
*   `text_to_speech.py`: Handles the local ONNX TTS synthesis framework.
*   `en_US-lessac-medium.onnx` & `.json`: Pre-trained local voice model weights and configuration.
*   `.streamlit/`: Configuration folder containing the UI dark theme setup.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gaurav082507-lang/AI_Voice_Assistant.git](https://github.com/gaurav082507-lang/AI_Voice_Assistant.git)
   cd AI_Voice_Assistant
