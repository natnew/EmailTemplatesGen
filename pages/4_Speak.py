import io
import os
import sys
from typing import Optional

import av
import numpy as np
import openai
import soundfile as sf
import streamlit as st
from streamlit_webrtc import AudioProcessorBase, WebRtcMode, webrtc_streamer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import init_sidebar

init_sidebar(
    "Talk directly with the AI assistant using your microphone for hands-free guidance."
)

# -------------------------------------------------------------
# 0.  CONFIGURATION – API‑KEY HANDLING (robust to missing secrets.toml)
# -------------------------------------------------------------


def get_openai_key() -> Optional[str]:
    """Return an OpenAI key.

    1. Try to read `OPENAI_API_KEY` from secrets.toml.
    2. If that fails (either the file is missing *or* the key is absent),
       prompt the user for a key in the sidebar.
    """
    # 1️⃣ Attempt to read from secrets.toml *safely*
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (FileNotFoundError, KeyError):
        # secrets.toml not present OR the key wasn’t defined – fall back to input
        pass

    # 2️⃣ Sidebar input as fallback
    with st.sidebar:
        st.subheader("🔑 API Key")
        entered_key = st.text_input(
            "Enter your OpenAI API Key",
            type="password",
            help="Key is kept only for this browser session and not stored on the server.",
        )
    return entered_key or None


openai_key = get_openai_key()
if not openai_key:
    st.warning("Please provide an OpenAI API key to use the voice assistant.")
    st.stop()

openai.api_key = openai_key

# -------------------------------------------------------------
# 1.  PAGE LAYOUT
# -------------------------------------------------------------
st.header("🗣️ Speak with the AI Assistant")

st.markdown(
    "This tab lets you talk to the project mentor in real‑time.\n"
    "1. Click **Start** to open the microphone.\n"
    "2. Speak, then click **Stop**.\n"
    "3. The assistant will transcribe, think and answer back in both text **and** voice."
)


# -------------------------------------------------------------
# 2.  AUDIO CAPTURE COMPONENT
# -------------------------------------------------------------
class WhisperAudioProcessor(AudioProcessorBase):
    """Collect raw microphone frames and expose them as a WAV file."""

    def __init__(self):
        self._buffer: list[np.ndarray] = []
        self._sample_rate: int | None = None

    def recv(self, frame: av.AudioFrame):
        # Convert incoming frame to a 1‑D int16 numpy array
        self._sample_rate = frame.sample_rate
        pcm = frame.to_ndarray().flatten()
        self._buffer.append(pcm)
        return frame  # Must return a frame even if unmodified

    def get_wav_bytes(self):
        if not self._buffer:
            return None
        audio = np.concatenate(self._buffer)
        wav_io = io.BytesIO()
        sf.write(wav_io, audio, self._sample_rate, format="WAV")
        wav_io.seek(0)
        self._buffer = []
        return wav_io


ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=WhisperAudioProcessor,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
)

# -------------------------------------------------------------
# 3.  PIPELINE — ASR  ➜  LLM  ➜  TTS
# -------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if ctx.state.playing is False and ctx.audio_processor is not None:
    wav_data = ctx.audio_processor.get_wav_bytes()

    if wav_data:
        # --- 3a. Speech ➜ Text (Whisper) ----------------------
        with st.spinner("Transcribing…"):
            transcript_resp = openai.audio.transcriptions.create(
                model="whisper-1",
                file=("speech.wav", wav_data, "audio/wav"),
            )
            user_text = transcript_resp.text.strip()

        st.chat_message("user").markdown(user_text)
        st.session_state.history.append({"role": "user", "content": user_text})

        # --- 3b. Text ➜ Text (Chat Completion) ---------------
        with st.spinner("Thinking…"):
            completion_resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful project mentor."},
                    *st.session_state.history,
                ],
            )
            assistant_text = completion_resp.choices[0].message.content.strip()

        st.chat_message("assistant").markdown(assistant_text)
        st.session_state.history.append(
            {"role": "assistant", "content": assistant_text}
        )

        # --- 3c. Text ➜ Speech (TTS) --------------------------
        with st.spinner("Voicing response…"):
            tts_resp = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=assistant_text,
            )
            st.audio(tts_resp.audio, format="audio/mp3")

# -------------------------------------------------------------
# 4.  SIDEBAR – NEW CONVERSATION BUTTON
# -------------------------------------------------------------
with st.sidebar:
    if st.button("🔄  New conversation"):
        st.session_state.history = []
        st.experimental_rerun()
