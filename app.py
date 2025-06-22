import streamlit as st
import tempfile
import os
from fpdf import FPDF
from openai import OpenAI

# ──────────────────────────────────────────────────────────────
# Load API key and create OpenAI client
# ──────────────────────────────────────────────────────────────
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ──────────────────────────────────────────────────────────────
# Streamlit page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Meeting Minutes Summarizer", layout="centered")
st.title("📝 Meeting Minutes Summarizer")
st.markdown(
    "Upload an audio file of your meeting and select a summary style. "
    "We'll transcribe it with Whisper and summarize it with GPT-4."
)

# ──────────────────────────────────────────────────────────────
# UI controls
# ──────────────────────────────────────────────────────────────
summary_style = st.selectbox(
    "Choose summary style:", ["Executive", "Bullet Points", "Email-style"]
)
uploaded_file = st.file_uploader(
    "Upload audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"]
)

# ──────────────────────────────────────────────────────────────
# Main workflow
# ──────────────────────────────────────────────────────────────
if uploaded_file:
    st.audio(uploaded_file)
    if st.button("Transcribe & Summarize"):

        # Save upload to a temporary file
        suffix = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
            tmp_audio.write(uploaded_file.read())
            tmp_audio_path = tmp_audio.name

        # ────────── Whisper transcription (OpenAI v1.x) ──────────
        with st.spinner("Transcribing audio with Whisper..."):
            with open(tmp_audio_path, "rb") as af:
                transcript_response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=af,
                )
            transcript = transcript_response.text

        # ────────── GPT-4 summary ──────────
        with st.spinner("Generating summary with GPT-4..."):
            prompt = (
                f"Please summarize the following meeting transcript in "
                f"{summary_style.lower()} style:\n\n{transcript}"
            )
            reply = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            summary = reply.choices[0].message.content.strip()

        # ────────── Display summary ──────────
        cleaned = "<br>".join(
            line.strip() for line in summary.splitlines() if line.strip()
        )
        st.markdown(
            f'<div style="background:#000;color:#fff;padding:15px;border-radius:10px;">'
            f"{cleaned}</div>",
            unsafe_allow_html=True,
        )

        # ────────── Download options ──────────
        st.markdown("#### 📥 Download summary")
        fmt = st.radio("Format", ["Text (.txt)", "PDF (.pdf)"])

        def as_txt(text: str) -> bytes:
            return text.encode("utf-8")

        def as_pdf(text: str) -> bytes:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in text.splitlines():
                pdf.multi_cell(0, 6, line)
            return pdf.output(dest="S").encode("latin1")

        if fmt == "Text (.txt)":
            st.download_button(
                "Download TXT",
                data=as_txt(summary),
                file_name="meeting_summary.txt",
                mime="text/plain",
            )
        else:
            st.download_button(
                "Download PDF",
                data=as_pdf(summary),
                file_name="meeting_summary.pdf",
                mime="application/pdf",
            )

        # Clean up temp file
        os.remove(tmp_audio_path)
