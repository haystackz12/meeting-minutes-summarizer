import streamlit as st
import openai
import tempfile
import os
from fpdf import FPDF

# Load API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page config
st.set_page_config(page_title="Meeting Minutes Summarizer", layout="centered")
st.title("📝 Meeting Minutes Summarizer")
st.markdown(
    "Upload an audio file of your meeting and select a summary style. "
    "We'll transcribe and summarize it for you using OpenAI's Whisper and GPT-4."
)

# UI controls
summary_style = st.selectbox(
    "Choose summary style:", ["Executive", "Bullet Points", "Email-style"]
)
uploaded_file = st.file_uploader(
    "Upload audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"]
)

# Audio preview & action button
if uploaded_file:
    st.audio(uploaded_file)
    if st.button("Transcribe & Summarize"):

        # Save upload to a temp file for Whisper
        with st.spinner("Transcribing audio with Whisper..."):
            suffix = "." + uploaded_file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
                tmp_audio.write(uploaded_file.read())
                tmp_audio_path = tmp_audio.name

            with open(tmp_audio_path, "rb") as af:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=af,
                ).text

        # Summarize with GPT-4
        with st.spinner("Generating summary with GPT-4..."):
            prompt = (
                f"Please summarize the following meeting transcript in "
                f"{summary_style.lower()} style:\n\n{transcript}"
            )
            reply = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            summary = reply.choices[0].message.content.strip()

        # Show summary (dark card)
        cleaned = "<br>".join(line.strip() for line in summary.splitlines() if line.strip())
        st.markdown(
            f'<div style="background:#000;color:#fff;padding:15px;border-radius:10px;">{cleaned}</div>',
            unsafe_allow_html=True,
        )

        # Download options
        st.markdown("#### 📥 Download summary")
        fmt = st.radio("Format", ["Text (.txt)", "PDF (.pdf)"])

        def as_txt(text: str) -> bytes:
            return text.encode("utf-8")

        def as_pdf(text: str) -> bytes:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in text.splitlines():
                pdf.multi_cell(0, 6, line)
            data = pdf.output(dest="S").encode("latin1")
            return data

        i
