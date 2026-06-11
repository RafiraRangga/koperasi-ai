# 🌾 KoperasiAI — Asisten Cerdas Koperasi Indonesia

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/streamlit-1.41.1-FF4B4B?style=flat-square&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=flat-square&logo=google" alt="Gemini">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<p align="center">
  <b>LLM-Based Tools & Gemini API Integration for Data Scientists</b><br>
  <i>Final Project · Membangun infrastruktur digital gotong royong untuk koperasi Indonesia</i>
</p>

---

## 📖 Overview

**KoperasiAI** is an intelligent AI assistant designed for **Koperasi Simpan Pinjam (KSP)** in Indonesia. Built on **Google Gemini API** and **Streamlit**, it provides 24/7 customer support, loan simulations, and cooperative education — all through a natural chat interface.

> "Bayangkan setiap koperasi di Indonesia punya asisten AI sendiri. KoperasiAI membawa itu selangkah lebih nyata."

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💰 **Simulasi Pinjaman** | Auto-generate flat-rate loan amortization tables (Pokok, Bunga, Total, Sisa) |
| 📋 **Produk Koperasi** | Information on Simpanan Wajib, Sukarela, Berjangka & all loan types |
| 🧠 **Conversation Memory** | Retains up to 20 messages of chat context — semakin chat, semakin pintar |
| 🎯 **Domain Knowledge** | AD/ART, SHU, RAT, UU No. 25/1992 — deep understanding of Indonesian cooperative law |
| 🎚️ **Adjustable Parameters** | Temperature, Top-P, Max Tokens, and 3 language styles (Santai/Formal/Campuran) |
| 🔑 **Bring Your Own Key** | Uses your Gemini API key — no server-side secrets, fully client-side |
| 📥 **Export Chat** | Download conversations as `.txt` for documentation |
| 🎨 **Professional UI** | Glass-morphism navbar, gradient hero, card grid, responsive design |

---

## 🎬 Demo

![KoperasiAI Screenshot](https://via.placeholder.com/800x500/0f766e/ffffff?text=KoperasiAI+Screenshot)

*Coming soon: live demo on Streamlit Community Cloud*

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Streamlit UI                       │
│  ┌─────────┐  ┌──────────┐  ┌───────────────────┐   │
│  │ Sidebar │  │   Hero   │  │   Chat Interface   │   │
│  │ Config  │  │  Cards   │  │   Messages + Input │   │
│  └─────────┘  └──────────┘  └───────────────────┘   │
├──────────────────────────────────────────────────────┤
│                   Session State                       │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────┐   │
│  │  Messages[]  │  │  Config  │  │  Parameters  │   │
│  └──────────────┘  └──────────┘  └──────────────┘   │
├──────────────────────────────────────────────────────┤
│               Gemini API (google-generativeai)        │
│  ┌──────────────────────────────────────────────┐    │
│  │  System Prompt → Domain Knowledge Injection  │    │
│  │  Chat History  → Conversation Continuity     │    │
│  │  Generation    → Response + Amortization     │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

---

## 🌐 Live Demo

| Platform | URL |
|---|---|
| 🌍 **Landing Page** | **[rafirarangga.github.io/koperasi-ai](https://rafirarangga.github.io/koperasi-ai/)** |
| 🤖 **Live App** | **[rafirarangga-koperasi-ai.streamlit.app](https://rafirarangga-koperasi-ai.streamlit.app/)** *(deploy dulu)* |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Gemini API Key](https://aistudio.google.com/apikey) (free)

### Installation

```bash
# Clone the repo
git clone https://github.com/RafiraRangga/koperasi-ai.git
cd koperasi-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

Open **http://localhost:8501** — enter your Gemini API key in the sidebar and start chatting!

Or run with your API key:

```bash
GEMINI_API_KEY="your-key-here" streamlit run app.py
```

---

## 🧪 Example Conversations

**Simulasi Pinjaman:**
> **User:** "Simulasi pinjaman Rp 10 juta, 12 bulan"
>
> **KoperasiAI:**
>
> | Bulan | Pokok | Bunga (2%) | Total | Sisa |
> |-------|-------|-----------|-------|------|
> | 1 | Rp 833.333 | Rp 200.000 | Rp 1.033.333 | Rp 9.166.667 |
> | 2 | Rp 833.333 | Rp 183.333 | Rp 1.016.667 | Rp 8.333.333 |
> | ... | ... | ... | ... | ... |

**SHU Explanation:**
> **User:** "Apa itu SHU dan gimana cara ngitungnya?"
>
> **KoperasiAI:** explains Sisa Hasil Usaha, pembagian berdasarkan jasa modal & jasa anggota, with formula and examples.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Custom CSS (Glass-morphism, Inter font) |
| **AI/LLM** | Google Gemini 2.5 Flash / 2.0 Flash / 2.5 Pro |
| **SDK** | `google-generativeai` v0.8.4 |
| **State** | Streamlit Session State |
| **Language** | Python 3.10+ |

---

## 🔧 Configuration

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `temperature` | 0.0 – 1.5 | 0.7 | Response creativity |
| `top_p` | 0.0 – 1.0 | 0.95 | Nucleus sampling |
| `max_tokens` | 256 – 4096 | 2048 | Max response length |
| `gaya_bahasa` | Santai / Formal / Campuran | Santai | Language style |
| `max_history` | 2 – 20 | 10 | Conversation memory depth |

---

## 🗂️ Project Structure

```
koperasi-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🧠 Domain Knowledge

KoperasiAI is trained on Indonesian cooperative regulations and practices:

- **UU No. 25/1992** — Perkoperasian Indonesia
- **Simpanan:** Wajib (bulanan), Sukarela, Berjangka (3/6/12 bln), Pendidikan
- **Pinjaman:** Modal Kerja, Konsumtif, Mikro, Multiguna
- **Ketentuan:** Bunga maks 2%/bulan (flat), tenor 1-60 bln, agunan > Rp10jt
- **SHU:** Formula pembagian berdasarkan jasa modal & jasa anggota

---

## 📝 License

MIT © 2025 RafiraRangga

---

<p align="center">
  <sub>🌾 Built for KSP Credit Union Mandiri Probolinggo · Final Project LLM-Based Tools</sub>
</p>
