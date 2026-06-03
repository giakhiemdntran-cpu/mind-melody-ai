import tempfile
import os
import streamlit as st
from faster_whisper import WhisperModel


@st.cache_resource
def load_whisper_model():

    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )


def speech_to_text(audio_file):

    if audio_file is None:
        return ""

    model = load_whisper_model()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp_file:

        tmp_file.write(audio_file.getvalue())
        audio_path = tmp_file.name

    try:

        segments, info = model.transcribe(
            audio_path,
            language="vi"
        )

        text = " ".join(
            segment.text
            for segment in segments
        )

        return text.strip()

    except Exception as e:

        return f"Lỗi Whisper: {e}"

    finally:

        if os.path.exists(audio_path):
            os.remove(audio_path)