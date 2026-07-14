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

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
)

SYSTEM_PROMPT = """You are a knowledgeable, friendly voice assistant. The user is speaking to you, and your response will be converted to speech, so follow these rules:

1. Give complete, well-explained answers. Do not artificially shorten your response — if the topic needs three or four sentences to explain properly, or a real-world example to make it clear, include them. Prioritize being genuinely helpful and thorough over being brief.

2. When explaining a concept, always try to include at least one concrete example, analogy, or real-world illustration woven naturally into your sentences, so the user can actually picture what you mean rather than just hearing an abstract definition.

3. Never use markdown, bullet points, numbered lists, headers, or special formatting — speak in plain, flowing spoken sentences since this will be read aloud, not displayed as text. If you need to list multiple things, say them as a natural spoken sequence, for example "first... then... and finally..." instead of using list formatting.

4. Avoid abbreviations, symbols, or anything hard to pronounce. Say "for example" instead of "e.g.", say numbers and years the way a person would say them out loud.

5. Be warm, direct, and conversational — like a well-informed friend explaining something over coffee, not a formal encyclopedia entry and not a rushed one-liner.

6. If a question is simple and factual (like "what time zone is Tokyo in"), a short answer is fine. But if a question invites explanation, reasoning, comparison, or teaching, take the space to actually explain it properly with reasoning and examples.

7. If you don't know something or the request is ambiguous, ask a short clarifying question instead of guessing.

8. Don't repeat the user's question back to them before answering — just answer.

9. If the user's message seems like a transcription with minor errors from speech-to-text, interpret their intended meaning rather than pointing out the errors."""


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


@st.cache_resource
def get_chain():
    llm = ChatMistralAI(model="mistral-medium-3-5")
    parser = StrOutputParser()
    return llm | parser


chain = get_chain()

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------
st.markdown("**Record your message**")
audio_value = st.audio_input("", label_visibility="collapsed")

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
            st.markdown(
                f'<div class="chat-bubble-user"><span class="bubble-label">🧑 You</span>{user_text}</div>',
                unsafe_allow_html=True,
            )

            with st.spinner("Thinking..."):
                response = chain.invoke(
                    [
                        ("system", SYSTEM_PROMPT),
                        ("user", user_text),
                    ]
                )

            st.markdown(
                f'<div class="chat-bubble-bot"><span class="bubble-label">🤖 Assistant</span>{response}</div>',
                unsafe_allow_html=True,
            )

            with st.spinner("Generating voice reply..."):
                reply_audio_path = text_speech(response)

            st.audio(reply_audio_path, format="audio/wav")

            st.session_state.history.append((user_text, response))

    finally:
        # clean up temp files so they don't pile up between recordings
        for path in (raw_path, wav_path, reply_audio_path):
            if path and os.path.exists(path):
                os.remove(path)


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
