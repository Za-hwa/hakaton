import streamlit as st
from streamlit_audio_recorder import audio_recorder
import whisper
import tempfile
import os
from pydub import AudioSegment
from gtts import gTTS

# Whisper 모델 불러오기
model = whisper.load_model("base")

st.title("🎤 Whisper + gTTS: 말하면 읽어주는 AI")

# 🎙️ 1. 오디오 녹음
audio_bytes = audio_recorder(
    text="눌러서 말하고 다시 눌러서 멈추세요", 
    recording_color="#e74c3c", 
    neutral_color="#2ecc71", 
    icon_name="mic"
)

if audio_bytes:
    # 🔄 2. 녹음된 오디오를 WAV 파일로 저장
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        tmp_wav.write(audio_bytes)
        wav_path = tmp_wav.name

    # 🔁 WAV → MP3 (Whisper는 mp3도 됨, gTTS도 mp3)
    mp3_path = wav_path.replace(".wav", ".mp3")
    AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")

    # 🔍 3. Whisper로 텍스트 변환
    with st.spinner("🧠 음성을 텍스트로 변환 중..."):
        result = model.transcribe(mp3_path, language="ko")
        text = result["text"]

    st.success("✅ 인식 완료!")
    st.markdown(f"**📝 인식된 문장:** {text}")

    # 🔊 4. gTTS로 텍스트 → 음성 생성
    tts = gTTS(text=text, lang="ko")
    tts_path = os.path.join(tempfile.gettempdir(), "tts.mp3")
    tts.save(tts_path)

    # ▶️ 5. 음성 재생
    st.audio(tts_path, format="audio/mp3")

    # 🧹 6. 임시 파일 삭제
    os.remove(wav_path)
    os.remove(mp3_path)
