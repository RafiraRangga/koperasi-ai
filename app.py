"""
KoperasiAI — Asisten Cerdas Koperasi Indonesia
Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists
"""

import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ═══════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="KoperasiAI — Asisten Koperasi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════
# CUSTOM CSS — Professional Web UI
# ═══════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & Base ── */
    * { font-family: 'Inter', sans-serif; }
    body { background: #f8fafc; color: #1e293b; }

    /* ── MAIN CONTAINER ── */
    .main > div { padding-top: 0 !important; }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f0fdf4 0%, #f8fafc 30%, #ffffff 100%);
    }
    [data-testid="stHeader"] { background: transparent !important; }

    /* ── GLASS NAVBAR ── */
    .navbar {
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(15,118,110,0.08);
        padding: 0.7rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky; top: 0; z-index: 100;
    }
    .navbar-brand {
        font-size: 1.25rem; font-weight: 800;
        background: linear-gradient(135deg, #0d9488, #047857);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .navbar-links { display: flex; gap: 2rem; }
    .navbar-link {
        color: #475569; font-size: 0.85rem; font-weight: 500;
        text-decoration: none; transition: color 0.2s;
    }
    .navbar-link:hover { color: #0d9488; }

    /* ── HERO ── */
    .hero {
        text-align: center; padding: 3.5rem 2rem 2rem;
    }
    .hero-badge {
        display: inline-block; background: rgba(13,148,136,0.08);
        color: #0d9488; padding: 0.4rem 1.2rem; border-radius: 100px;
        font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 1.2rem;
        border: 1px solid rgba(13,148,136,0.12);
    }
    .hero h1 {
        font-size: 3.2rem; font-weight: 900; letter-spacing: -1.5px;
        background: linear-gradient(135deg, #0f766e 0%, #059669 50%, #047857 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem;
    }
    .hero p {
        font-size: 1.15rem; color: #64748b; max-width: 560px;
        margin: 0 auto 1.5rem; line-height: 1.7;
    }
    .hero-stats {
        display: flex; justify-content: center; gap: 3rem; margin-top: 2rem;
    }
    .hero-stat { text-align: center; }
    .hero-stat-value { font-size: 1.8rem; font-weight: 800; color: #0f766e; }
    .hero-stat-label { font-size: 0.78rem; color: #94a3b8; margin-top: 0.2rem; }

    /* ── CARDS ── */
    .card-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; padding: 0 1rem 2rem; }
    .card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 16px;
        padding: 1.5rem; transition: all 0.3s ease; cursor: pointer;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .card:hover {
        transform: translateY(-4px); box-shadow: 0 16px 40px rgba(13,148,136,0.1);
        border-color: #5eead4;
    }
    .card-icon { font-size: 2rem; margin-bottom: 0.8rem; }
    .card-title { font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.3rem; }
    .card-desc { font-size: 0.8rem; color: #94a3b8; line-height: 1.5; }

    /* ── CHAT BUBBLES ── */
    [data-testid="stChatMessage"] {
        background: #fff !important; border-radius: 18px !important;
        padding: 1rem 1.4rem !important; margin: 0.4rem 0 !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important;
    }
    [data-testid="stChatMessage"]:has(img[alt="user"]) {
        background: linear-gradient(135deg, #f0fdfa, #e6fffa) !important;
        border-color: #b2f5ea !important;
    }

    /* ── INPUT ── */
    [data-testid="stChatInput"] textarea {
        border-radius: 16px !important; border: 1.5px solid #e2e8f0 !important;
        padding: 0.9rem 1.2rem !important; font-size: 0.95rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04) !important;
        transition: all 0.2s !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #14b8a6 !important; box-shadow: 0 4px 25px rgba(13,148,136,0.1) !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc, #f0fdfa) !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] h3 { color: #0f766e !important; font-weight: 700 !important; }
    [data-testid="stSidebar"] label { font-weight: 600 !important; color: #334155 !important; font-size: 0.82rem !important; }

    /* ── BUTTONS ── */
    .stButton > button {
        border-radius: 12px !important; font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important; transition: all 0.2s !important;
        font-size: 0.85rem !important;
    }
    .stButton > button:hover { transform: translateY(-2px); }

    /* ── METRICS BAR ── */
    .metrics-bar {
        background: rgba(255,255,255,0.6); backdrop-filter: blur(10px);
        border: 1px solid #e2e8f0; border-radius: 16px;
        padding: 1rem 1.5rem; margin: 1rem 0;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center; padding: 2rem 1rem; color: #94a3b8;
        font-size: 0.78rem; border-top: 1px solid #e2e8f0; margin-top: 3rem;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .hero h1 { font-size: 2rem; }
        .card-grid { grid-template-columns: repeat(2,1fr); }
        .hero-stats { flex-direction: column; gap: 0.8rem; }
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 100px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌾 KoperasiAI")
    st.caption("LLM-Based Tools · Gemini API")
    st.divider()

    st.markdown("#### 🔑 API Key")
    api_key = st.text_input(
        "Gemini API Key", type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        placeholder="AIza...",
        label_visibility="collapsed"
    )
    if not api_key:
        st.warning("⚠️ API Key diperlukan")
        st.caption("Dapatkan: aistudio.google.com/apikey")

    st.divider()
    st.markdown("#### 🧠 Model")
    model_name = st.selectbox(
        "Model", ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"],
        index=0, label_visibility="collapsed"
    )

    st.divider()
    st.markdown("#### 🎚️ Parameter")
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    top_p = st.slider("Top-P", 0.0, 1.0, 0.95, 0.05)
    max_tokens = st.slider("Max Tokens", 256, 4096, 2048, 128)

    st.divider()
    st.markdown("#### 💬 Gaya Bahasa")
    gaya_bahasa = st.selectbox(
        "Gaya", ["Santai & Ramah 😊", "Formal & Profesional 👔", "Campuran ✨"],
        index=0, label_visibility="collapsed"
    )

    st.divider()
    st.markdown("#### 🔧 Fitur")
    enable_memory = st.toggle("Memory Percakapan", True)
    max_history = st.slider("Riwayat", 2, 20, 10, disabled=not enable_memory)

    st.divider()
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.messages:
        chat_txt = "\n".join(
            [f"{'👤' if m['role']=='user' else '🤖'}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            "📥 Export Chat", chat_txt,
            file_name=f"koperasiai-{datetime.now():%Y%m%d-%H%M}.txt",
            mime="text/plain", use_container_width=True
        )

    st.divider()
    st.caption(f"© {datetime.now().year} KoperasiAI")

# ═══════════════════════════════════════════
# SYSTEM PROMPT
# ═══════════════════════════════════════════
GAYA_PROMPT = {
    "Santai & Ramah 😊": "Gunakan bahasa Indonesia santai, ramah, personal. Panggil user 'Kak' atau 'Sahabat Koperasi'. Boleh emoticon. Nada hangat seperti teman membantu.",
    "Formal & Profesional 👔": "Gunakan bahasa Indonesia formal. Sapa 'Bapak/Ibu'. Kalimat lengkap, sopan, informatif. Hindari singkatan tidak baku dan emoticon.",
    "Campuran ✨": "Bahasa semi-formal. Ramah tapi informatif. Sesuaikan dengan konteks — santai untuk sapaan, formal untuk teknis. Sapa 'Anda' atau 'Bapak/Ibu'."
}

SYSTEM_PROMPT = f"""Kamu adalah KoperasiAI, asisten AI untuk koperasi simpan pinjam (KSP) di Indonesia.

### Domain Pengetahuan

**Simpanan:** Simpanan Wajib (bulanan), Simpanan Sukarela, Simpanan Berjangka (deposito 3/6/12 bln), Simpanan Pendidikan.

**Pinjaman:** Modal Kerja (usaha), Konsumtif (pribadi), Mikro (plafon kecil), Multiguna.

**Ketentuan:**
- Bunga maksimal 2%/bulan (flat rate) sesuai regulasi koperasi
- Tenor 1-60 bulan
- Agunan untuk pinjaman > Rp10 juta
- Prinsip: keanggotaan sukarela, pengelolaan demokratis, SHU adil

### Gaya Bahasa
{GAYA_PROMPT[gaya_bahasa]}

### Aturan
1. Simulasi pinjaman: tabel angsuran (Bulan, Pokok, Bunga, Total, Sisa) pakai metode flat rate
2. Semua nominal dalam Rupiah (Rp1.000.000)
3. Respons utama 200-400 kata, tabel/simulasi bisa lebih panjang
4. Di luar domain koperasi: arahkan kembali dengan sopan
5. Akhiri dengan ajakan bertanya lebih lanjut"""


def init_model():
    if not api_key: return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": temperature, "top_p": top_p, "top_k": 40, "max_output_tokens": max_tokens},
        safety_settings=[{"category": c, "threshold": "BLOCK_NONE"} for c in [
            "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"
        ]]
    )


def build_conversation(msgs, max_hist):
    conv = [
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": [
            "Halo! Saya KoperasiAI, asisten koperasi kamu. "
            "Saya bisa bantu informasi simpanan, pinjaman, simulasi angsuran, "
            "atau cara daftar anggota koperasi. Ada yang bisa saya bantu? 😊"
        ]}
    ]
    if enable_memory and msgs:
        for m in msgs[-max_hist:]:
            role = "model" if m["role"] == "assistant" else "user"
            conv.append({"role": role, "parts": [m["content"]]})
    return conv


# ═══════════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">🐣 Final Project · LLM-Based Tools & Gemini API</div>
    <h1>KoperasiAI</h1>
    <p>
        Asisten cerdas untuk koperasi simpan pinjam Indonesia.<br>
        Tanya simpanan, simulasi pinjaman, cek SHU — semua lewat chat.
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">24/7</div>
            <div class="hero-stat-label">Siap Membantu</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">100%</div>
            <div class="hero-stat-label">Bahasa Indonesia</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Gemini</div>
            <div class="hero-stat-label">Powered by Google</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# FEATURE CARDS
# ═══════════════════════════════════════════
st.markdown("""
<div class="card-grid">
    <div class="card">
        <div class="card-icon">💰</div>
        <div class="card-title">Simulasi Pinjaman</div>
        <div class="card-desc">Hitung angsuran & bunga otomatis dengan metode flat rate.</div>
    </div>
    <div class="card">
        <div class="card-icon">📋</div>
        <div class="card-title">Produk Koperasi</div>
        <div class="card-desc">Informasi simpanan, pinjaman, deposito & persyaratan.</div>
    </div>
    <div class="card">
        <div class="card-icon">🧠</div>
        <div class="card-title">Memory Cerdas</div>
        <div class="card-desc">Ingat konteks percakapan. Semakin chat, semakin pintar.</div>
    </div>
    <div class="card">
        <div class="card-icon">🎯</div>
        <div class="card-title">Domain Koperasi</div>
        <div class="card-desc">AD/ART, SHU, RAT, UU Perkoperasian No. 25/1992.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# QUICK ACTIONS
# ═══════════════════════════════════════════
st.markdown("### 🚀 Coba Tanyakan")
cols = st.columns(4)
prompts = [
    ("📋", "Syarat jadi anggota koperasi?"),
    ("💰", "Simulasi pinjaman Rp5 juta 12 bulan"),
    ("🏦", "Apa saja produk simpanan koperasi?"),
    ("📊", "Apa itu SHU & cara menghitungnya?"),
]
for i, (icon, text) in enumerate(prompts):
    with cols[i]:
        if st.button(f"{icon} {text}", use_container_width=True, key=f"qp_{i}"):
            st.session_state.messages.append({"role": "user", "content": text})
            st.rerun()

# ═══════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════
st.divider()

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:3rem;color:#94a3b8;">
        <div style="font-size:4rem;margin-bottom:1rem;">🌾</div>
        <h3>Selamat datang di KoperasiAI!</h3>
        <p>Klik quick action di atas atau ketik pertanyaanmu.</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🌾"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik pertanyaan seputar koperasi...", key="chat"):
    if not api_key:
        st.error("⚠️ Masukkan Gemini API Key di sidebar!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌾"):
        with st.spinner("🤔 Berpikir..."):
            try:
                model = init_model()
                conv = build_conversation(st.session_state.messages, max_history)
                reply = model.generate_content(conv).text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                err = str(e)
                if "API_KEY" in err.upper(): st.error("🔑 API Key tidak valid.")
                elif "quota" in err.lower(): st.error("📊 Kuota habis.")
                else: st.error(f"❌ {err}")

# ═══════════════════════════════════════════
# METRICS BAR
# ═══════════════════════════════════════════
st.markdown('<div class="metrics-bar">', unsafe_allow_html=True)
mc = st.columns(5)
mc[0].metric("🧠 Model", model_name.replace("gemini-",""))
mc[1].metric("🌡️ Temp", f"{temperature:.1f}")
mc[2].metric("🎯 Top-P", f"{top_p:.2f}")
mc[3].metric("💬 Gaya", gaya_bahasa.split(" ")[0])
mc[4].metric("📝 Chat", len(st.session_state.messages))
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <strong>KoperasiAI</strong> · Final Project LLM-Based Tools & Gemini API · © {datetime.now().year}<br>
    Membangun infrastruktur digital gotong royong untuk koperasi Indonesia
</div>
""", unsafe_allow_html=True)
