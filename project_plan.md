# 📑 Project Plan – Meeting Minutes Summarizer

> **Version:** 1.0  
> **Owner:** Michael Hastings  
> **Last updated:** 2025-06-22  

---

## 1  Project Overview
The **Meeting Minutes Summarizer** is a Streamlit web application that lets users upload an audio recording of a meeting, transcribe it with OpenAI Whisper, and generate a concise summary with GPT-4. Summaries can be downloaded in **TXT** or **PDF** formats and viewed in-app through a clean, dark-themed UI.

---

## 2  Objectives & Scope
| Goal | Description |
|------|-------------|
| **Rapid MVP** | Build a working prototype in a single dev cycle. |
| **Zero-install UX** | Host on Streamlit Cloud so anyone can run it in a browser. |
| **Configurable summaries** | Provide Executive, Bullet, and Email styles. |
| **Export options** | Permit downloads as `.txt` or `.pdf`. |

Out-of-scope: user authentication, persistent storage, multi-language support (v1 only handles English).

---

## 3  Tech Stack
| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend / UI** | Streamlit | Fast no-boilerplate UI; good for demos. |
| **Language** | Python 3.10+ | Whisper & GPT-4 examples in Python; Streamlit compatibility. |
| **Transcription** | OpenAI Whisper | High accuracy, simple API call. |
| **Summarization** | GPT-4 (`gpt-4` model) | State-of-the-art text summarization. |
| **PDF Generation** | FPDF | Lightweight library for single-page PDF. |
| **Deployment** | Streamlit Community Cloud | Free hosting with GitHub integration. |
| **Version Control** | Git + GitHub | Source-of-truth, automatic Cloud deploy. |

---

## 4  Requirements
### 4.1  Functional
1. Upload MP3, WAV, or M4A ≤ 25 MB.
2. Preview audio in browser.
3. Transcribe via Whisper.
4. Summarize via GPT-4 using selected style.
5. Display summary in dark card.
6. Offer download as `.txt` or `.pdf`.

### 4.2  Non-Functional
- < 30 s cold-start on Streamlit Cloud.
- Secrets stored securely via `.streamlit/secrets.toml`.
- Minimal dependencies (< 10 packages).

---

## 5  Implementation Timeline
| Date | Milestone |
|------|-----------|
| **Day 1** | Initial Streamlit MVP (upload ⟶ summary). |
| **Day 2** | Added TXT/PDF export, style selector. |
| **Day 3** | Cloud deployment; resolved dependency & SDK issues. |
| **Day**
