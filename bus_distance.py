import streamlit as st
import whisper
import tempfile
import os
from gtts import gTTS
from pydub import AudioSegment

model = whisper.load_model("base")

st.title("🎤 음성 파일 업로드로 STT + gTTS TTS")

uploaded_file = st.file_uploader("📤 음성 파일을 업로드하세요 (mp3, wav)", type=["mp3", "wav"])

if uploaded_file:
    # 업로드 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(uploaded_file.read())
        audio_path = tmp_audio.name

    # Whisper로 음성 → 텍스트
    result = model.transcribe(audio_path, language="ko")
    text = result["text"]
    st.success("✅ 텍스트 변환 완료")
    st.write(text)

    # gTTS로 텍스트 → 음성
    tts = gTTS(text=text, lang="ko")
    tts_path = os.path.join(tempfile.gettempdir(), "output.mp3")
    tts.save(tts_path)

    st.audio(tts_path, format="audio/mp3")

