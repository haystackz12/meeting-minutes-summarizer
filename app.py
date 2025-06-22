import streamlit as st
import openai
import tempfile
import os
from fpdf import FPDF
from pathlib import Path
from pydub import AudioSegment

# Load API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page config
st.set_page_config(page_title="Meeting Minutes Summarizer", layout="centered")
st.title("📝 Meeting Minutes Summarizer")
st.markdown("Upload an audio file of your meeting and select a summary style. We'll transcribe and summarize it for you using OpenAI's Whisper and GPT-4.")

# UI Controls
summary_style = st.selectbox("Choose summary style:", ["Executive", "Bullet Points", "Email-style"])
uploaded_file = st.file_uploader("Upload audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

# Audio preview
if uploaded_file:
    st.audio(uploaded_file, format='audio/mp3')
    transcribe_button = st.button("Transcribe & Summarize")

    if transcribe_button:
        with st.spinner("Transcribing audio with Whisper..."):
            # Convert to correct format for Whisper
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_audio.write(uploaded_file.read())
            temp_audio.close()

            # Transcribe
            with open(temp_audio.name, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

        with st.spinner("Generating summary with GPT-4..."):
            user_prompt = f"Please summarize the following meeting transcript in {summary_style.lower()} style:\n\n{transcript.text}"
            chat_response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.3
            )
            summary = chat_response.choices[0].message.content.strip()

        # Clean & format
        cleaned = "<br>".join([line.strip() for line in summary.splitlines() if line.strip()])
        st.markdown(
            f'<div style="background-color:#000000;color:#FFFFFF;padding:15px;border-radius:10px;">{cleaned}</div>',
            unsafe_allow_html=True
        )

        # Download options
        download_format = st.radio("Download format", ["Text (.txt)", "PDF (.pdf)"])

        def make_txt(summary_text):
            return summary_text.encode()

        def make_pdf(summary_text):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in summary_text.splitlines():
                pdf.multi_cell(0, 10, line)
            tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(tmp_path.name)
            return tmp_path.name

        st.markdown("---")

        if download_format == "Text (.txt)":
            txt_file = make_txt(summary)
            st.download_button("📄 Download TXT", data=txt_file, file_name="summary.txt", mime="text/plain")
        else:
            pdf_path = make_pdf(summary)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download PDF", data=f, file_name="summary.pdf", mime="application/pdf")

        # Cleanup temp file
        os.remove(temp_audio.name)
