# 📝 Meeting Minutes Summarizer

The **Meeting Minutes Summarizer** is a lightweight web app built with Streamlit that allows users to upload an audio recording (MP3, WAV, or M4A) of a meeting, transcribe it using OpenAI's Whisper model, and generate a high-quality summary using GPT-4. The final summary can be downloaded in either `.txt` or `.pdf` format.

---

## 🚀 Features

- 🎙 Upload audio files in MP3, WAV, or M4A formats
- 🔊 Audio preview before processing
- 🧠 Transcription using OpenAI Whisper
- 📝 Summarization using GPT-4 in one of three formats:
  - Executive Summary
  - Bullet Points
  - Email-style Recap
- 💾 Download the summary in `.txt` or `.pdf`
- ⚡ Clean and mobile-friendly UI with Streamlit

---

## 📷 Screenshots

> **Note:** Create a folder named `screenshots` in the repo and add these PNG files:

### Home Page  
![Home](screenshots/home.png)

### After Upload & Summary  
![Summary](screenshots/summary.png)

---

## 🛠 Tech Stack

- **Frontend / UI Framework:** [Streamlit](https://streamlit.io/)
- **Language:** Python 3.10+
- **Transcription Engine:** [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- **Summarization Model:** [OpenAI GPT-4](https://platform.openai.com/docs/guides/gpt)
- **PDF Generation:** [FPDF](https://py-pdf.github.io/fpdf2/)
- **Deployment:** [Streamlit Community Cloud](https://streamlit.io/cloud)
- **Version Control:** Git & GitHub

---

meeting-minutes-summarizer/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Python dependencies
├── screenshots/             # Optional screenshots for README
│   ├── home.png
│   └── summary.png
└── .streamlit/
    └── secrets.toml         # API key config (not committed)

---

## ⚙️ Run Locally

Clone the repo and install dependencies:

```bash
git clone https://github.com/haystackz12/meeting-minutes-summarizer.git
cd meeting-minutes-summarizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
