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

<<<<<<< HEAD
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
)
=======
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️")
st.title("🎙️ AI Voice Assistant")
st.caption("Tap record, speak, and the assistant will reply back to you in voice.")
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c

SYSTEM_PROMPT = """You are a helpful, friendly voice assistant. The user is speaking to you, and your responses will be converted to speech, so follow these rules:

1. Keep responses short and conversational — 1 to 3 sentences unless the user asks for detail.
2. Never use markdown, bullet points, numbered lists, headers, or special formatting — speak in plain, natural sentences since this will be read aloud, not displayed as text.
3. Avoid abbreviations, symbols, or anything hard to pronounce (e.g. say "for example" instead of "e.g.", say "twenty twenty six" instead of "2026" when it reads more naturally).
4. Be warm, direct, and clear — like a knowledgeable friend, not a formal assistant.
5. If you don't know something or the request is ambiguous, ask a short clarifying question instead of guessing.
6. Don't repeat the user's question back to them before answering — just answer.
7. If the user's message seems like a transcription with minor errors (from speech-to-text), interpret their intended meaning rather than pointing out the errors."""


<<<<<<< HEAD
# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .stApp {
            background: radial-gradient(circle at 15% 0%, #1b1030 0%, #0b0d14 45%) fixed;
        }

        .hero {
            background: linear-gradient(120deg, #6d28d9 0%, #a855f7 50%, #ec4899 100%);
            border-radius: 20px;
            padding: 2.4rem 2.6rem;
            margin-bottom: 1.6rem;
            box-shadow: 0 10px 40px rgba(168, 85, 247, 0.25);
        }
        .hero h1 {
            color: white;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
        }
        .hero p {
            color: rgba(255,255,255,0.9);
            font-size: 1.05rem;
            margin: 0 0 1.1rem 0;
        }
        .pill-row { display: flex; gap: 0.6rem; flex-wrap: wrap; }
        .pill {
            background: rgba(255,255,255,0.16);
            color: white;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            backdrop-filter: blur(4px);
        }

        .sidebar-card {
            background: #151823;
            border: 1px solid rgba(168, 85, 247, 0.25);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
            color: #e5e7eb;
            font-size: 0.92rem;
        }

        .chat-bubble-user {
            background: linear-gradient(120deg, rgba(109,40,217,0.25), rgba(236,72,153,0.15));
            border: 1px solid rgba(168, 85, 247, 0.35);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.6rem;
            color: #f3f4f6;
        }
        .chat-bubble-bot {
            background: #151823;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.6rem;
            color: #e5e7eb;
        }
        .bubble-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.65;
            margin-bottom: 0.25rem;
            display: block;
        }

        .footer-credit {
            text-align: center;
            color: rgba(229,231,235,0.55);
            font-size: 0.85rem;
            margin-top: 2.5rem;
            padding-top: 1.2rem;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .footer-credit a {
            color: #c084fc;
            text-decoration: none;
            font-weight: 600;
        }
        .footer-credit a:hover { text-decoration: underline; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎙️ AI Voice Assistant")
    st.caption("Speak naturally, get a spoken reply back — powered by open-source models.")

    st.markdown("**WHAT IT DOES**")
    st.markdown('<div class="sidebar-card">🎧 In-browser voice recording</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">📝 Whisper speech-to-text</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">🧠 Mistral AI reasoning</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">🔊 Piper text-to-speech reply</div>', unsafe_allow_html=True)

    st.markdown("**HOW TO USE**")
    st.markdown('<div class="sidebar-card">1️⃣ Tap record and speak</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">2️⃣ Wait for transcription</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">3️⃣ Listen to the reply</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎙️ AI Voice Assistant</h1>
        <p>Tap record, speak, and the assistant will reply back to you in voice.</p>
        <div class="pill-row">
            <span class="pill">🎧 Whisper STT</span>
            <span class="pill">🧠 Mistral AI</span>
            <span class="pill">🔊 Piper TTS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


=======
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c
@st.cache_resource
def get_chain():
    llm = ChatMistralAI(model="mistral-medium-3-5")
    parser = StrOutputParser()
    return llm | parser


chain = get_chain()

if "history" not in st.session_state:
    st.session_state.history = []

<<<<<<< HEAD

# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------
st.markdown("**Record your message**")
audio_value = st.audio_input("", label_visibility="collapsed")
=======
audio_value = st.audio_input("Record your message")
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c

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
<<<<<<< HEAD
            st.markdown(
                f'<div class="chat-bubble-user"><span class="bubble-label">🧑 You</span>{user_text}</div>',
                unsafe_allow_html=True,
            )
=======
            st.chat_message("user").write(user_text)
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c

            with st.spinner("Thinking..."):
                response = chain.invoke(
                    [
                        ("system", SYSTEM_PROMPT),
                        ("user", user_text),
                    ]
                )

<<<<<<< HEAD
            st.markdown(
                f'<div class="chat-bubble-bot"><span class="bubble-label">🤖 Assistant</span>{response}</div>',
                unsafe_allow_html=True,
            )
=======
            st.chat_message("assistant").write(response)
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c

            with st.spinner("Generating voice reply..."):
                reply_audio_path = text_speech(response)

            st.audio(reply_audio_path, format="audio/wav")

            st.session_state.history.append((user_text, response))

    finally:
<<<<<<< HEAD
=======
        # clean up temp files so they don't pile up between recordings
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c
        for path in (raw_path, wav_path, reply_audio_path):
            if path and os.path.exists(path):
                os.remove(path)

<<<<<<< HEAD

# ---------------------------------------------------------------------------
# Conversation history
# ---------------------------------------------------------------------------
if st.session_state.history:
    st.divider()
    st.markdown("### Conversation history")
    for user_msg, bot_msg in st.session_state.history:
        st.markdown(
            f'<div class="chat-bubble-user"><span class="bubble-label">🧑 You</span>{user_msg}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="chat-bubble-bot"><span class="bubble-label">🤖 Assistant</span>{bot_msg}</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-credit">
        AI Voice Assistant &nbsp;|&nbsp; Built by <strong>Gaurav Gupta</strong> &nbsp;|&nbsp;
        <a href="https://www.linkedin.com/in/gaurav-gupta-79754a377" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
=======
if st.session_state.history:
    st.divider()
    st.subheader("Conversation history")
    for user_msg, bot_msg in st.session_state.history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Assistant:** {bot_msg}")
>>>>>>> 4b5b55377347f8a4b92eca48d834e4679692069c
