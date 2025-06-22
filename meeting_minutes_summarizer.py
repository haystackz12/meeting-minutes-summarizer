from pathlib import Path

final_script = """\
import streamlit as st
import tempfile
import os
import openai
from openai import OpenAI
from typing import Optional
import io
from fpdf import FPDF
from textwrap import fill

st.set_page_config(page_title="Meeting Minutes Summarizer", layout="centered")

# Apply custom style for dark theme display
st.markdown(\"\"\"
    <style>
        .report-area {
            background:#1e1e1e;
            color:#fff;
            padding:1rem;
            border-radius:6px;
            line-height:1.6;
            font-size: 1rem;
        }
    </style>
\"\"\", unsafe_allow_html=True)

st.title("🎙️ Meeting Minutes Summarizer")

# Instructions
st.info("Upload an audio file and choose a summary style **before** clicking 'Transcribe & Summarize'.")

# Set OpenAI client using secret key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Sidebar options
summary_style = st.sidebar.selectbox(
    "Choose Summary Style",
    options=["Bullet", "Executive", "Email"]
)

download_format = st.sidebar.radio(
    "Choose download format",
    options=[".txt", ".pdf"]
)

# File uploader
uploaded_file = st.file_uploader("Upload your meeting audio file", type=["mp3", "wav", "m4a"])

def transcribe_whisper(binary_data: bytes, file_ext: str, lang_code: Optional[str]):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
        tmp_file.write(binary_data)
        tmp_path = tmp_file.name

    with open(tmp_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=lang_code or "en"
        )
    os.remove(tmp_path)
    return transcript.text

def summarize_transcript(transcript_text: str, style: str):
    prompt = f"Please summarize the following meeting transcript in {style.lower()} style:\\n\\n{transcript_text}"
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

def make_pdf(content: str) -> bytes:
    def safe_wrap(paragraph: str, width=100):
        words = paragraph.split()
        for i, w in enumerate(words):
            if len(w) > width:
                words[i] = "\\u200b".join([w[j : j + 60] for j in range(0, len(w), 60)])
        return fill(" ".join(words), width=width)

    pdf = FPDF(format="Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    for para in content.splitlines():
        wrapped = safe_wrap(para, width=100)
        for line in wrapped.splitlines():
            pdf.multi_cell(0, 6, line)
        pdf.ln(2)

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue()

if uploaded_file and st.button("Transcribe & Summarize"):
    st.subheader("📄 Transcript and Summary")
    
    # Add audio playback
    st.audio(uploaded_file, format='audio/mp3')

    with st.spinner("🔄 Transcribing and summarizing..."):
        ext = uploaded_file.name.split(".")[-1]
        bytes_data = uploaded_file.read()
        transcript = transcribe_whisper(bytes_data, ext, lang_code="en")
        summary = summarize_transcript(transcript, summary_style)

        cleaned = "\\n".join([line.strip() for line in summary.splitlines() if line.strip()])
        html_summary = cleaned.replace("\\n", "<br>")
        st.markdown(f'<div class="report-area">{html_summary}</div>', unsafe_allow_html=True)

        if download_format == ".txt":
            st.download_button(
                label="📥 Download Summary as .txt",
                data=cleaned,
                file_name="meeting_summary.txt",
                mime="text/plain"
            )
        else:
            file_bytes = make_pdf(cleaned)
            st.download_button(
                label="📥 Download Summary as .pdf",
                data=file_bytes,
                file_name="meeting_summary.pdf",
                mime="application/pdf"
            )
"""

# Save it to the user's workspace
file_path = "/mnt/data/meeting_minutes_summarizer_final.py"
Path(file_path).write_text(final_script)

file_path
