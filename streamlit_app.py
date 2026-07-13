import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from whisper_model import model
from audio_preprocess import audio_preprocess
from text_to_speech import text_speech

from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

load_dotenv()

st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️")
st.title("🎙️ AI Voice Assistant")
st.caption("Tap record, speak, and the assistant will reply back to you in voice.")

SYSTEM_PROMPT = """You are a helpful, friendly voice assistant. The user is speaking to you, and your responses will be converted to speech, so follow these rules:

1. Keep responses short and conversational — 1 to 3 sentences unless the user asks for detail.
2. Never use markdown, bullet points, numbered lists, headers, or special formatting — speak in plain, natural sentences since this will be read aloud, not displayed as text.
3. Avoid abbreviations, symbols, or anything hard to pronounce (e.g. say "for example" instead of "e.g.", say "twenty twenty six" instead of "2026" when it reads more naturally).
4. Be warm, direct, and clear — like a knowledgeable friend, not a formal assistant.
5. If you don't know something or the request is ambiguous, ask a short clarifying question instead of guessing.
6. Don't repeat the user's question back to them before answering — just answer.
7. If the user's message seems like a transcription with minor errors (from speech-to-text), interpret their intended meaning rather than pointing out the errors."""


@st.cache_resource
def get_chain():
    llm = ChatMistralAI(model="mistral-medium-3-5")
    parser = StrOutputParser()
    return llm | parser


chain = get_chain()

if "history" not in st.session_state:
    st.session_state.history = []

audio_value = st.audio_input("Record your message")

if audio_value is not None:
    raw_path = None
    wav_path = None
    reply_audio_path = None

    try:
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_value.read())
                raw_path = tmp.name

            wav_path = audio_preprocess(raw_path)
            result = model.transcribe(wav_path)
            user_text = result["text"].strip()

        if not user_text:
            st.warning("Couldn't hear anything clear in that recording. Try again.")
        else:
            st.chat_message("user").write(user_text)

            with st.spinner("Thinking..."):
                response = chain.invoke(
                    [
                        ("system", SYSTEM_PROMPT),
                        ("user", user_text),
                    ]
                )

            st.chat_message("assistant").write(response)

            with st.spinner("Generating voice reply..."):
                reply_audio_path = text_speech(response)

            st.audio(reply_audio_path, format="audio/wav")

            st.session_state.history.append((user_text, response))

    finally:
        # clean up temp files so they don't pile up between recordings
        for path in (raw_path, wav_path, reply_audio_path):
            if path and os.path.exists(path):
                os.remove(path)

if st.session_state.history:
    st.divider()
    st.subheader("Conversation history")
    for user_msg, bot_msg in st.session_state.history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Assistant:** {bot_msg}")
