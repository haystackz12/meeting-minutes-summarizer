
import streamlit as st
from openai import OpenAI
import tempfile
import os

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI: Title and instructions
st.title("Meeting Minutes Summarizer")
st.write("Upload an audio file and choose how you want the meeting summarized:")

# File uploader and summary style selector
audio_file = st.file_uploader("Upload audio file (MP3, M4A, WAV)", type=["mp3", "m4a", "wav"])
summary_style = st.selectbox("Summary style", ["Bullet", "Executive", "Email"])
submit = st.button("Submit")

if submit and audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[-1]) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    # Transcribe using Whisper (OpenAI SDK v1)
    with st.spinner("Transcribing audio..."):
        with open(tmp_path, "rb") as f:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            transcript_text = transcript_response.text

    os.remove(tmp_path)

    st.success("Transcription complete.")
    st.text_area("Transcript", transcript_text, height=200)

    # Summarize using GPT-4
    with st.spinner("Generating summary..."):
        prompt = f"""Please summarize the following meeting transcript in {summary_style.lower()} style:

{transcript_text}
"""
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional meeting assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = completion.choices[0].message.content

    st.markdown("### Summary")
    st.write(summary)
