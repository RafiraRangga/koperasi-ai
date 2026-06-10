"""
KoperasiAI — Asisten Koperasi Indonesia 🇮🇩

Chatbot AI berbasis Gemini API untuk membantu anggota dan pengurus koperasi:
- Informasi produk simpanan & pinjaman
- Simulasi pinjaman
- FAQ seputar koperasi
- Penjelasan AD/ART koperasi

Dibuat untuk Final Project: LLM-Based Tools and Gemini API Integration
"""

import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ═══════════════════════════════════════════
# KONFIGURASI HALAMAN
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="KoperasiAI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════
# SIDEBAR — PARAMETER KREATIF
# ═══════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bank-building.png", width=64)
    st.title("KoperasiAI 🏦")
    st.caption("Asisten Cerdas Koperasi Indonesia")
    st.divider()

    # API Key
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        placeholder="Masukkan API Key Gemini",
        help="Dapatkan di https://aistudio.google.com/apikey"
    )

    st.divider()
    st.subheader("⚙️ Parameter Kreatif")

    # Model selection
    model_name = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        index=0,
        help="Gemini 2.5 Flash = cepat & hemat, Pro = akurat & mahal"
    )

    # Temperature
    temperature = st.slider(
        "Temperature (Kreativitas)",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1,
        help="0 = kaku/faktual, 1.5 = sangat kreatif"
    )

    # Gaya Bahasa
    gaya_bahasa = st.selectbox(
        "Gaya Bahasa",
        ["Santai & Ramah", "Formal & Profesional", "Campuran"],
        index=0
    )

    # Fitur tambahan
    st.subheader("🔧 Fitur Tambahan")
    enable_memory = st.toggle("Memory Percakapan", value=True,
                              help="Bot mengingat konteks percakapan")
    enable_simulation = st.toggle("Simulasi Pinjaman", value=True,
                                  help="Hitung simulasi angsuran otomatis")
    max_history = st.slider("Riwayat Chat", 4, 20, 10,
                            help="Jumlah pesan yang diingat")

    st.divider()
    st.caption(f"© {datetime.now().year} KoperasiAI • Final Project")
    st.caption("LLM-Based Tools & Gemini API Integration")

    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# ═══════════════════════════════════════════
# SYSTEM PROMPT — DOMAIN KOPERASI
# ═══════════════════════════════════════════
GAYA_PROMPT = {
    "Santai & Ramah": "Gunakan bahasa Indonesia santai, ramah, dan akrab. Boleh pakai kata 'kak', 'sahabat', sesekali emoticon. Nada bicara seperti teman yang membantu.",
    "Formal & Profesional": "Gunakan bahasa Indonesia formal dan profesional. Sapa dengan 'Bapak/Ibu', nada sopan dan informatif. Hindari singkatan tidak baku.",
    "Campuran": "Gunakan bahasa Indonesia semi-formal. Ramah tapi tetap informatif. Sesuaikan dengan konteks pertanyaan."
}

SYSTEM_PROMPT = f"""Kamu adalah KoperasiAI, asisten virtual untuk koperasi simpan pinjam (KSP) di Indonesia.

DOMAIN PENGETAHUAN:
- Produk simpanan: sukarela, wajib, berjangka, pendidikan
- Produk pinjaman: modal kerja, konsumtif, mikro, multiguna
- Prosedur menjadi anggota koperasi
- Simulasi pinjaman & Bunga (maks 2% per bulan sesuai regulasi)
- AD/ART koperasi & prinsip koperasi Indonesia
- SHU (Sisa Hasil Usaha) dan RAT (Rapat Anggota Tahunan)
- Perhitungan bagi hasil dan angsuran

{GAYA_PROMPT[gaya_bahasa]}

ATURAN:
1. Jika ditanya simulasi pinjaman, buatkan tabel angsuran lengkap
2. Jika user minta info produk, sebutkan manfaat, syarat, dan ketentuan
3. Semua nominal dalam Rupiah (Rp), gunakan format Indonesia
4. Jika ada pertanyaan di luar domain koperasi/keuangan, arahkan kembali ke topik koperasi dengan sopan
5. Jawaban maksimal 500 kata, kecuali simulasi/tabel"""

# ═══════════════════════════════════════════
# FUNGSI GEMINI API
# ═══════════════════════════════════════════
def init_model():
    """Inisialisasi model Gemini dengan parameter kreatif."""
    if not api_key:
        return None
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )
    return model

def build_conversation(messages, max_hist):
    """Bangun konteks percakapan dengan memory."""
    conversation = [{"role": "user", "parts": [SYSTEM_PROMPT]},
                    {"role": "model", "parts": ["Siap! Saya KoperasiAI, asisten koperasi kamu. Ada yang bisa saya bantu seputar simpanan, pinjaman, atau info koperasi?"]}]

    if enable_memory and len(messages) > 0:
        recent = messages[-max_hist:]
        for msg in recent:
            role = "model" if msg["role"] == "assistant" else "user"
            conversation.append({"role": role, "parts": [msg["content"]]})

    return conversation

# ═══════════════════════════════════════════
# INISIALISASI SESSION STATE
# ═══════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

# ═══════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://img.icons8.com/color/96/bank-building.png", width=80)
with col2:
    st.title("KoperasiAI 🏦")
    st.caption("Asisten Cerdas untuk Koperasi Simpan Pinjam Indonesia | Powered by Gemini API")

st.divider()

# ═══════════════════════════════════════════
# QUICK ACTIONS
# ═══════════════════════════════════════════
cols = st.columns(4)
quick_prompts = [
    "📋 Cara jadi anggota koperasi?",
    "💰 Simulasi pinjaman Rp 5 juta",
    "🏦 Produk simpanan apa saja?",
    "📊 Apa itu SHU dan RAT?",
]

for i, prompt in enumerate(quick_prompts):
    with cols[i]:
        if st.button(prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt.split(" ", 1)[1]})
            st.rerun()

# ═══════════════════════════════════════════
# CHAT HISTORY
# ═══════════════════════════════════════════
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ═══════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════
if prompt := st.chat_input("Tanya seputar koperasi...", key="chat_input"):
    if not api_key:
        st.error("⚠️ Masukkan Gemini API Key di sidebar terlebih dahulu!")
        st.stop()

    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            try:
                model = init_model()
                if model is None:
                    st.error("Gagal inisialisasi model. Cek API Key.")
                    st.stop()

                conversation = build_conversation(
                    st.session_state.messages, max_history
                )

                response = model.generate_content(conversation)
                reply = response.text

                # Simulasi pinjaman detection
                if enable_simulation and any(k in prompt.lower() for k in
                    ["simulasi", "pinjam", "angsuran", "cicilan", "kredit"]):
                    reply += "\n\n---\n*💡 Tips: Mau simulasi lebih detail? Sebutkan jumlah pinjaman dan tenor (bulan). Contoh: \"Simulasi pinjaman Rp 10 juta 12 bulan\"*"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════
# STATUS BAR
# ═══════════════════════════════════════════
st.divider()
status_cols = st.columns(4)
with status_cols[0]:
    st.metric("Model", model_name)
with status_cols[1]:
    st.metric("Temperature", f"{temperature:.1f}")
with status_cols[2]:
    st.metric("Gaya", gaya_bahasa.split(" ")[0])
with status_cols[3]:
    st.metric("Riwayat", f"{len(st.session_state.messages)} pesan")
