import streamlit as st
import pickle
import json
import numpy as np
import pandas as pd
from PIL import Image
import os

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MentalCheck",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f172a 0%, #1e3a5f 60%, #0f4c75 100%);
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio > label { color: #94a3b8 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 0.65rem 1rem !important;
    margin-bottom: 0.4rem !important;
    transition: all 0.2s ease !important;
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(99,179,237,0.15) !important;
    border-color: rgba(99,179,237,0.4) !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] [aria-checked="true"] ~ label,
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(99,179,237,0.25), rgba(99,217,205,0.2)) !important;
    border-color: rgba(99,179,237,0.6) !important;
    color: #ffffff !important;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0f4c75 0%, #1b6ca8 40%, #187498 80%, #0a9396 100%);
    border-radius: 20px;
    padding: 2.5rem 2.8rem;
    color: white;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-banner h1 { font-size: 2.2rem; font-weight: 800; margin: 0 0 0.4rem; letter-spacing: -0.02em; }
.hero-banner p  { font-size: 1rem; margin: 0; opacity: 0.85; font-weight: 400; }
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 100px;
    padding: 0.25rem 0.85rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Section headers ── */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0f172a;
    margin: 2rem 0 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-sub {
    color: #64748b;
    font-size: 0.92rem;
    margin-bottom: 1.4rem;
}

/* ── Variable Cards ── */
.var-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.var-card {
    background: #ffffff;
    border: 1px solid #e8edf5;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s, box-shadow 0.2s;
    border-left: 4px solid #1b6ca8;
}
.var-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.09); }
.var-card.cat  { border-left-color: #0a9396; }
.var-card.spec { border-left-color: #9333ea; }
.var-card-title { font-size: 0.88rem; font-weight: 700; color: #1e3a5f; margin-bottom: 0.3rem; }
.var-card-type  { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; color: #94a3b8; margin-bottom: 0.4rem; }
.var-card-desc  { font-size: 0.83rem; color: #475569; line-height: 1.55; }
.var-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 100px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-top: 0.5rem;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}
.var-badge.green { background: #f0fdf4; color: #15803d; border-color: #bbf7d0; }
.var-badge.purple { background: #faf5ff; color: #7c3aed; border-color: #ddd6fe; }

/* ── Metric cards ── */
.metric-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.metric-card .val { font-size: 2rem; font-weight: 800; color: #1b6ca8; font-family: 'Plus Jakarta Sans'; }
.metric-card .lbl { font-size: 0.82rem; color: #64748b; font-weight: 500; margin-top: 0.2rem; }
.metric-card .sub { font-size: 0.75rem; color: #94a3b8; margin-top: 0.1rem; }

/* ── Info boxes ── */
.info-box {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.87rem;
    color: #0369a1;
    margin-bottom: 1rem;
    line-height: 1.6;
}
.warn-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.87rem;
    color: #c2410c;
    margin-bottom: 1.2rem;
    line-height: 1.6;
}
.success-box {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.87rem;
    color: #15803d;
    margin-bottom: 1rem;
    line-height: 1.6;
}

/* ── Form Sections ── */
.form-section {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.form-section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Result card ── */
.result-positive {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    color: white;
    text-align: center;
    box-shadow: 0 8px 25px rgba(220,38,38,0.3);
    margin: 1.5rem 0;
}
.result-negative {
    background: linear-gradient(135deg, #0a9396 0%, #0f766e 100%);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    color: white;
    text-align: center;
    box-shadow: 0 8px 25px rgba(10,147,150,0.3);
    margin: 1.5rem 0;
}
.result-icon  { font-size: 3.5rem; margin-bottom: 0.5rem; }
.result-title { font-size: 1.6rem; font-weight: 800; margin: 0 0 0.4rem; letter-spacing: -0.02em; }
.result-prob  { font-size: 0.95rem; opacity: 0.9; margin: 0; }

/* ── Progress bar ── */
.prob-bar-wrap {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-top: 0.8rem;
}
.prob-bar-label { font-size: 0.82rem; font-weight: 600; color: #374151; margin-bottom: 0.4rem; display: flex; justify-content: space-between; }
.prob-bar-bg { background: #f1f5f9; border-radius: 100px; height: 10px; overflow: hidden; }
.prob-bar-fill-red  { background: linear-gradient(90deg, #f87171, #dc2626); height: 100%; border-radius: 100px; transition: width 1s ease; }
.prob-bar-fill-teal { background: linear-gradient(90deg, #2dd4bf, #0a9396); height: 100%; border-radius: 100px; transition: width 1s ease; }

/* ── Disclaimer ── */
.disclaimer {
    background: #fefce8;
    border: 1px solid #fde047;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #713f12;
    line-height: 1.65;
    margin-top: 1.2rem;
}

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #1b6ca8, #0a9396) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(27,108,168,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(27,108,168,0.45) !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label { font-weight: 600 !important; font-size: 0.88rem !important; color: #374151 !important; }

hr { border: none !important; border-top: 1px solid #e2e8f0 !important; margin: 1.8rem 0 !important; }

/* ── Hide Streamlit default elements (keep sidebar toggle visible) ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="stToolbar"]    { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Load assets ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    with open("best_depression_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("preprocessor.pkl", "rb") as f:
        preprocessor = pickle.load(f)
    with open("model_metadata.json", "r") as f:
        metadata = json.load(f)
    return model, preprocessor, metadata

model, preprocessor, metadata = load_assets()


# ── Helper: Degree grouping ───────────────────────────────────────────────────
def get_degree_category(degree_label: str) -> str:
    mapping = {
        "Class 12 / SMA / High School": "High School",
        "Bachelor (S1 / B.Tech / BA / dll.)": "Bachelor",
        "Master (S2 / M.Tech / MBA / dll.)": "Master",
        "Doktor / Medis (S3 / PhD / MD / MBBS)": "Doctorate/Medical",
        "Lainnya": "Others",
    }
    return mapping.get(degree_label, "Others")


# ── Helper: Preprocessing ─────────────────────────────────────────────────────
def preprocess_input(raw: dict) -> np.ndarray:
    """
    Reproduces the exact preprocessing pipeline from training:

    ColumnTransformer(transformers=[('num', StandardScaler(), num_features)],
                      remainder='passthrough')

    Input must be a DataFrame with the SAME column names and order as X_train
    (i.e. original df_clean minus 'Depression'). The transformer selects columns
    by name, scales the 6 numericals, and passes through the rest unchanged.

    X_train original column order (from df_clean.drop('Depression')):
      Gender | Age | Academic Pressure | CGPA | Study Satisfaction |
      Have you ever had suicidal thoughts ? | Work/Study Hours | Financial Stress |
      Family History of Mental Illness | is_student |
      Dietary Habits_Moderate | Dietary Habits_Others | Dietary Habits_Unhealthy |
      Sleep Duration_7-8 hours | Sleep Duration_Less than 5 hours |
      Sleep Duration_More than 8 hours | Sleep Duration_Others |
      Degree_Category_Doctorate/Medical | Degree_Category_High School |
      Degree_Category_Master | Degree_Category_Others
    """
    # 1. Manual binary mappings
    gender   = 0 if raw["Gender"] == "Male" else 1
    suicidal = 1 if raw["Suicidal"] == "Ya / Yes" else 0
    family   = 1 if raw["Family History"] == "Ya / Yes" else 0

    # 2. Feature engineering
    is_student = 1 if raw["Profession"] == "Mahasiswa / Pelajar (Student)" else 0
    degree_cat = get_degree_category(raw["Degree"])

    # 3. One-hot encoding (drop_first=True → reference categories dropped)
    # Dietary Habits  → reference: Healthy
    diet = raw["Dietary Habits"]
    dh_moderate  = 1 if diet == "Moderate"  else 0
    dh_others    = 1 if diet == "Others"    else 0
    dh_unhealthy = 1 if diet == "Unhealthy" else 0

    # Sleep Duration  → reference: 5-6 hours
    sleep = raw["Sleep Duration"]
    sl_7_8    = 1 if sleep == "7-8 hours"         else 0
    sl_lt5    = 1 if sleep == "Less than 5 hours"  else 0
    sl_gt8    = 1 if sleep == "More than 8 hours"  else 0
    sl_others = 1 if sleep == "Others"             else 0

    # Degree Category → reference: Bachelor
    deg_doc  = 1 if degree_cat == "Doctorate/Medical" else 0
    deg_hs   = 1 if degree_cat == "High School"       else 0
    deg_mast = 1 if degree_cat == "Master"            else 0
    deg_oth  = 1 if degree_cat == "Others"            else 0

    # 4. Build DataFrame matching ORIGINAL X_train column order
    #    (ColumnTransformer selects 'num_features' by name → must match exactly)
    input_df = pd.DataFrame([{
        "Gender"                                : gender,
        "Age"                                   : raw["Age"],
        "Academic Pressure"                     : raw["Academic Pressure"],
        "CGPA"                                  : raw["CGPA"],
        "Study Satisfaction"                    : raw["Study Satisfaction"],
        "Have you ever had suicidal thoughts ?" : suicidal,
        "Work/Study Hours"                      : raw["Work Study Hours"],
        "Financial Stress"                      : raw["Financial Stress"],
        "Family History of Mental Illness"      : family,
        "is_student"                            : is_student,
        "Dietary Habits_Moderate"               : dh_moderate,
        "Dietary Habits_Others"                 : dh_others,
        "Dietary Habits_Unhealthy"              : dh_unhealthy,
        "Sleep Duration_7-8 hours"              : sl_7_8,
        "Sleep Duration_Less than 5 hours"      : sl_lt5,
        "Sleep Duration_More than 8 hours"      : sl_gt8,
        "Sleep Duration_Others"                 : sl_others,
        "Degree_Category_Doctorate/Medical"     : deg_doc,
        "Degree_Category_High School"           : deg_hs,
        "Degree_Category_Master"                : deg_mast,
        "Degree_Category_Others"                : deg_oth,
    }])

    # 5. Pass DataFrame to ColumnTransformer — it knows which columns to scale
    return preprocessor.transform(input_df)


# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.2rem 0 1.6rem;'>
      <div style='font-size:2.5rem; margin-bottom:0.4rem;'>🧠</div>
      <div style='font-size:1.4rem; font-weight:800; color:#f8fafc; letter-spacing:-0.02em;'>MentalCheck</div>
      <div style='font-size:0.75rem; color:#94a3b8; margin-top:0.2rem;'>Depression Detection Tool</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:0.6rem;'>NAVIGASI</p>", unsafe_allow_html=True)

    # Separate state var controls which page is active (0 or 1)
    if "active_page" not in st.session_state:
        st.session_state.active_page = 0

    _pages = ["📚  Penjelasan Variabel", "🔍  Prediksi Depresi"]
    menu = st.radio(
        "Pilih halaman",
        _pages,
        index=st.session_state.active_page,
        label_visibility="collapsed",
    )
    # Keep active_page in sync when user clicks the radio directly
    st.session_state.active_page = _pages.index(menu)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#64748b; line-height:1.6; padding:0 0.2rem;'>
    <strong style='color:#94a3b8;'>⚠️ Disclaimer</strong><br>
    Aplikasi ini bersifat edukatif dan <em>bukan</em> pengganti diagnosis profesional.
    Jika kamu membutuhkan bantuan, segera hubungi psikolog atau psikiater terdekat.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#475569; line-height:1.6;'>
    🏥 <strong style='color:#7dd3fc;'>Into The Light Indonesia</strong><br>
    📞 119 ext 8 (Hotline Kesehatan Jiwa)<br><br>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PENJELASAN VARIABEL
# ══════════════════════════════════════════════════════════════════════════════
if "Penjelasan" in menu:

    # Hero
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-tag">📚 Dokumentasi Model</div>
      <h1>Penjelasan Variabel & Performa Model</h1>
      <p>Pelajari variabel yang digunakan model, cara kerjanya, dan seberapa baik performa prediksinya.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA button → navigate to Prediksi page
    col_btn, col_spacer = st.columns([1, 3])
    with col_btn:
        if st.button("🔍  Mulai Prediksi Sekarang", use_container_width=True):
            st.session_state.active_page = 1
            st.rerun()

    # ── Variable Descriptions ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Variabel Numerik</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Nilai angka yang langsung digunakan setelah dinormalisasi dengan StandardScaler.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="var-grid">
      <div class="var-card">
        <div class="var-card-type">Numerik — Rentang: 18–60</div>
        <div class="var-card-title">🎂 Age (Usia)</div>
        <div class="var-card-desc">Usia responden dalam tahun. Digunakan untuk memahami konteks kehidupan dan fase perkembangan yang dialami.</div>
        <span class="var-badge">Skala Kontinu</span>
      </div>
      <div class="var-card">
        <div class="var-card-type">Numerik — Skala: 1–5</div>
        <div class="var-card-title">📚 Academic Pressure</div>
        <div class="var-card-desc">Tingkat tekanan akademik yang dirasakan. Nilai tinggi menunjukkan beban akademik yang berat dan berpotensi meningkatkan risiko depresi.</div>
        <span class="var-badge">Skala Likert</span>
      </div>
      <div class="var-card">
        <div class="var-card-type">Numerik — Rentang: 0–10</div>
        <div class="var-card-title">🎓 CGPA</div>
        <div class="var-card-desc">Nilai rata-rata akademik (Cumulative Grade Point Average). Mencerminkan performa akademik keseluruhan responden.</div>
        <span class="var-badge">Skala Kontinu</span>
      </div>
      <div class="var-card">
        <div class="var-card-type">Numerik — Skala: 1–5</div>
        <div class="var-card-title">😊 Study Satisfaction</div>
        <div class="var-card-desc">Tingkat kepuasan terhadap studi. Kepuasan rendah berkorelasi dengan tingkat stres lebih tinggi dan potensi depresi.</div>
        <span class="var-badge">Skala Likert</span>
      </div>
      <div class="var-card">
        <div class="var-card-type">Numerik — Jam/hari: 1–12</div>
        <div class="var-card-title">⏰ Work/Study Hours</div>
        <div class="var-card-desc">Rata-rata jam kerja atau belajar per hari. Beban waktu yang berlebih dapat memicu kelelahan mental (burnout).</div>
        <span class="var-badge">Skala Kontinu</span>
      </div>
      <div class="var-card">
        <div class="var-card-type">Numerik — Skala: 1–5</div>
        <div class="var-card-title">💰 Financial Stress</div>
        <div class="var-card-desc">Tingkat stres akibat kondisi keuangan. Tekanan finansial merupakan salah satu pemicu signifikan gangguan kesehatan mental.</div>
        <span class="var-badge">Skala Likert</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🏷️ Variabel Kategorikal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Variabel yang dikonversi menjadi angka melalui binary mapping atau one-hot encoding.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="var-grid">
      <div class="var-card cat">
        <div class="var-card-type">Kategorikal Biner — Mapping: Male=0, Female=1</div>
        <div class="var-card-title">🚻 Gender</div>
        <div class="var-card-desc">Jenis kelamin responden. Penelitian menunjukkan perbedaan prevalensi depresi antara pria dan wanita.</div>
        <span class="var-badge green">Binary Encoded</span>
      </div>
      <div class="var-card cat">
        <div class="var-card-type">Kategorikal Biner — Mapping: Yes=1, No=0</div>
        <div class="var-card-title">💭 Suicidal Thoughts</div>
        <div class="var-card-desc">Riwayat pikiran untuk menyakiti diri sendiri. Merupakan salah satu indikator klinis paling kuat untuk deteksi depresi.</div>
        <span class="var-badge green">Binary Encoded</span>
      </div>
      <div class="var-card cat">
        <div class="var-card-type">Kategorikal Biner — Mapping: Yes=1, No=0</div>
        <div class="var-card-title">🧬 Family History of Mental Illness</div>
        <div class="var-card-desc">Riwayat anggota keluarga dengan gangguan kesehatan mental. Faktor genetik berperan dalam kerentanan seseorang terhadap depresi.</div>
        <span class="var-badge green">Binary Encoded</span>
      </div>
      <div class="var-card cat">
        <div class="var-card-type">Kategorikal Multi-kelas — One-Hot (ref: Healthy)</div>
        <div class="var-card-title">🥗 Dietary Habits</div>
        <div class="var-card-desc">Kebiasaan pola makan (Healthy, Moderate, Unhealthy, Others). Nutrisi berpengaruh langsung pada kesehatan otak dan suasana hati.</div>
        <span class="var-badge green">One-Hot Encoded</span>
      </div>
      <div class="var-card cat">
        <div class="var-card-type">Kategorikal Multi-kelas — One-Hot (ref: 5-6 hours)</div>
        <div class="var-card-title">😴 Sleep Duration</div>
        <div class="var-card-desc">Durasi tidur per malam. Kualitas dan kuantitas tidur memiliki hubungan timbal balik yang erat dengan kondisi kesehatan mental.</div>
        <span class="var-badge green">One-Hot Encoded</span>
      </div>
      <div class="var-card spec">
        <div class="var-card-type">Feature Engineering — is_student: Student=1, lainnya=0</div>
        <div class="var-card-title">👤 Profession → is_student</div>
        <div class="var-card-desc">Pekerjaan diubah menjadi fitur biner: apakah responden seorang pelajar/mahasiswa? Tekanan akademik berbeda dengan tekanan kerja.</div>
        <span class="var-badge purple">Feature Engineering</span>
      </div>
      <div class="var-card spec">
        <div class="var-card-type">Feature Engineering — Degree_Category (5 grup)</div>
        <div class="var-card-title">🏫 Degree → Degree_Category</div>
        <div class="var-card-desc">Jenjang pendidikan dikelompokkan: High School, Bachelor, Master, Doctorate/Medical, Others — lalu di-encode (ref: Bachelor).</div>
        <span class="var-badge purple">Feature Engineering</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model Performance ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Performa Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Model terbaik: <strong>Logistic Regression (Tuned)</strong> — dioptimalkan dengan Randomized Search Cross-Validation.</div>', unsafe_allow_html=True)

    # Metric cards
    st.markdown("""
    <div class="metric-row">
      <div class="metric-card">
        <div class="val">84.8%</div>
        <div class="lbl">Akurasi Training</div>
        <div class="sub">Train Set (22.318 data)</div>
      </div>
      <div class="metric-card">
        <div class="val">84.6%</div>
        <div class="lbl">Akurasi Testing</div>
        <div class="sub">Test Set (5.580 data)</div>
      </div>
      <div class="metric-card">
        <div class="val">84.8%</div>
        <div class="lbl">CV Accuracy</div>
        <div class="sub">Cross-Validation (Best)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    ℹ️ <strong>Interpretasi Akurasi:</strong> Model berhasil mengklasifikasikan <strong>~84–85% kasus dengan benar</strong>. 
    Selisih kecil antara akurasi train (84.84%) dan test (84.61%) menunjukkan model <strong>tidak overfit</strong> — artinya model mampu generalisasi dengan baik pada data baru.
    Nilai Best CV Accuracy (84.83%) dari cross-validation mengonfirmasi konsistensi performa ini.
    </div>
    """, unsafe_allow_html=True)

    # F1-Score detail
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="form-section">
          <div class="form-section-title">🎯 F1-Score per Kelas (Test Set)</div>
          <div style='margin-top:0.5rem;'>
            <div class="prob-bar-label"><span>Tidak Depresi (Kelas 0)</span><span style='color:#0a9396; font-weight:700;'>F1 = 0.81</span></div>
            <div class="prob-bar-bg"><div class="prob-bar-fill-teal" style="width:81%"></div></div>
            <div style='font-size:0.78rem; color:#64748b; margin:0.4rem 0 1rem;'>Precision: 0.83 | Recall: 0.79</div>
            <div class="prob-bar-label"><span>Depresi (Kelas 1)</span><span style='color:#dc2626; font-weight:700;'>F1 = 0.87</span></div>
            <div class="prob-bar-bg"><div class="prob-bar-fill-red" style="width:87%"></div></div>
            <div style='font-size:0.78rem; color:#64748b; margin:0.4rem 0 0;'>Precision: 0.86 | Recall: 0.89</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
        💡 <strong>Kenapa F1 kelas 1 lebih tinggi?</strong><br>
        Model sedikit lebih baik mendeteksi kasus <em>depresi</em> (recall 89%) daripada <em>tidak depresi</em> (recall 79%). 
        Ini menguntungkan secara klinis — lebih baik "false alarm" daripada melewatkan kasus depresi nyata.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="form-section">
          <div class="form-section-title">⚙️ Parameter Model Terbaik</div>
          <div style='font-size:0.85rem; color:#374151; line-height:2;'>
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding:0.2rem 0;'>
              <span style='color:#64748b;'>Algoritma</span>
              <strong>Logistic Regression</strong>
            </div>
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding:0.2rem 0;'>
              <span style='color:#64748b;'>Regularization (C)</span>
              <strong>21.54</strong>
            </div>
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding:0.2rem 0;'>
              <span style='color:#64748b;'>Penalty</span>
              <strong>L2 (Ridge)</strong>
            </div>
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid #f1f5f9; padding:0.2rem 0;'>
              <span style='color:#64748b;'>Solver</span>
              <strong>Newton-CG</strong>
            </div>
            <div style='display:flex; justify-content:space-between; padding:0.2rem 0;'>
              <span style='color:#64748b;'>Scaling</span>
              <strong>StandardScaler</strong>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Confusion Matrix & Feature Importance ────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🗺️ Visualisasi Model</div>', unsafe_allow_html=True)

    col_cm, col_fi = st.columns(2)

    with col_cm:
        st.markdown('<div style="font-weight:700; color:#1e3a5f; font-size:0.95rem; margin-bottom:0.6rem;">Confusion Matrix</div>', unsafe_allow_html=True)
        if os.path.exists("confusion_matrix.png"):
            img = Image.open("confusion_matrix.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📂 Letakkan file `confusion_matrix.png` di folder yang sama.")
        st.markdown("""
        <div class="info-box" style="margin-top:0.8rem;">
        📊 <strong>Membaca Confusion Matrix:</strong><br>
        • <strong>True Negative (TN):</strong> Benar diprediksi tidak depresi<br>
        • <strong>True Positive (TP):</strong> Benar diprediksi depresi<br>
        • <strong>False Positive (FP):</strong> Diprediksi depresi padahal tidak (false alarm)<br>
        • <strong>False Negative (FN):</strong> Diprediksi tidak depresi padahal depresi (paling berbahaya)
        </div>
        """, unsafe_allow_html=True)

    with col_fi:
        st.markdown('<div style="font-weight:700; color:#1e3a5f; font-size:0.95rem; margin-bottom:0.6rem;">Feature Importance</div>', unsafe_allow_html=True)
        if os.path.exists("feature_importance.png"):
            img2 = Image.open("feature_importance.png")
            st.image(img2, use_container_width=True)
        else:
            st.info("📂 Letakkan file `feature_importance.png` di folder yang sama.")
        st.markdown("""
        <div class="info-box" style="margin-top:0.8rem;">
        🔍 <strong>Membaca Feature Importance:</strong><br>
        Menunjukkan seberapa besar kontribusi masing-masing variabel dalam prediksi model.<br>
        • <strong>Nilai positif:</strong> variabel meningkatkan probabilitas depresi<br>
        • <strong>Nilai negatif:</strong> variabel menurunkan probabilitas depresi<br>
        • <strong>Magnitude besar:</strong> pengaruh lebih kuat
        </div>
        """, unsafe_allow_html=True)

    # ── Preprocessing Pipeline ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🔧 Pipeline Preprocessing</div>', unsafe_allow_html=True)
    steps = metadata.get("preprocessing_steps", [])
    cols = st.columns(min(3, len(steps)))
    icons = ["🗑️", "🧹", "🔢", "⚙️", "🔄", "📏"]
    for i, step in enumerate(steps):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:12px; padding:0.9rem 1rem; margin-bottom:0.8rem; box-shadow:0 1px 4px rgba(0,0,0,0.04);'>
              <div style='font-size:1.3rem; margin-bottom:0.3rem;'>{icons[i % len(icons)]}</div>
              <div style='font-size:0.78rem; font-weight:700; color:#374151;'>Step {i+1}</div>
              <div style='font-size:0.8rem; color:#64748b; margin-top:0.2rem; line-height:1.5;'>{step}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PREDIKSI
# ══════════════════════════════════════════════════════════════════════════════
elif "Prediksi" in menu:

    # Hero
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-tag">🔍 Prediksi</div>
      <h1>Cek Risiko Depresi Kamu</h1>
      <p>Isi form di bawah ini dengan jujur. Semua data hanya digunakan untuk prediksi dan tidak disimpan.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
    ⚠️ <strong>Perhatian:</strong> Hasil prediksi ini bersifat <strong>indikatif</strong> berdasarkan model machine learning, bukan diagnosis medis resmi.
    Jika kamu atau orang di sekitarmu membutuhkan bantuan, segera hubungi profesional kesehatan mental.
    </div>
    """, unsafe_allow_html=True)

    # ── FORM ──────────────────────────────────────────────────────────────────
    with st.form("prediction_form"):

        # Section 1: Demografis
        st.markdown('<div class="form-section"><div class="form-section-title">👤 Informasi Demografis</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Usia (tahun)", min_value=10, max_value=80, value=21, step=1,
                                  help="Masukkan usia kamu saat ini")
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female"],
                                  help="Pilih jenis kelamin")
        with c3:
            profession = st.selectbox("Status / Profesi",
                                      ["Mahasiswa / Pelajar (Student)", "Profesional / Karyawan", "Lainnya"],
                                      help="Apakah kamu saat ini seorang pelajar atau mahasiswa?")
        st.markdown("</div>", unsafe_allow_html=True)

        # Section 2: Akademik
        st.markdown('<div class="form-section"><div class="form-section-title">🎓 Akademik & Pendidikan</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            degree = st.selectbox("Jenjang Pendidikan",
                                  ["Bachelor (S1 / B.Tech / BA / dll.)",
                                   "Master (S2 / M.Tech / MBA / dll.)",
                                   "Class 12 / SMA / High School",
                                   "Doktor / Medis (S3 / PhD / MD / MBBS)",
                                   "Lainnya"],
                                  help="Jenjang pendidikan yang sedang/terakhir ditempuh")
        with c2:
            cgpa = st.number_input("CGPA / IPK", min_value=0.0, max_value=10.0, value=7.50, step=0.01,
                                   format="%.2f", help="Nilai rata-rata akademik (0.00–10.00)")
        with c3:
            academic_pressure = st.slider("Tekanan Akademik", 0, 5, 3,
                                          help="0 = Tidak ada tekanan sama sekali, 5 = Sangat tinggi")
        c1, c2 = st.columns(2)
        with c1:
            study_satisfaction = st.slider("Kepuasan Studi", 0, 5, 3,
                                           help="0 = Sangat tidak puas, 5 = Sangat puas")
        with c2:
            work_study_hours = st.number_input("Jam Belajar/Kerja per Hari", min_value=0, max_value=12,
                                               value=6, step=1,
                                               help="Rata-rata jam belajar atau bekerja per hari (0–12)")
        st.markdown("</div>", unsafe_allow_html=True)

        # Section 3: Gaya Hidup
        st.markdown('<div class="form-section"><div class="form-section-title">🌙 Gaya Hidup & Kesehatan</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            sleep_dur = st.selectbox("Durasi Tidur per Malam",
                                     ["5-6 hours", "7-8 hours", "Less than 5 hours",
                                      "More than 8 hours", "Others"],
                                     help="Pilih rata-rata durasi tidurmu per malam")
        with c2:
            diet = st.selectbox("Kebiasaan Makan",
                                ["Healthy", "Moderate", "Unhealthy", "Others"],
                                help="Healthy = pola makan sehat dan teratur")
        with c3:
            financial_stress = st.slider("Stres Finansial", 1, 5, 2,
                                         help="1 = Tidak ada masalah keuangan, 5 = Tekanan finansial sangat berat")
        st.markdown("</div>", unsafe_allow_html=True)

        # Section 4: Riwayat Kesehatan Mental
        st.markdown('<div class="form-section"><div class="form-section-title">💜 Riwayat Kesehatan Mental</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            suicidal = st.selectbox("Pernah Punya Pikiran Bunuh Diri?",
                                    ["Tidak / No", "Ya / Yes"],
                                    help="Jawab dengan jujur. Informasi ini bersifat anonim.")
        with c2:
            family_hist = st.selectbox("Riwayat Gangguan Mental di Keluarga?",
                                       ["Tidak / No", "Ya / Yes"],
                                       help="Apakah ada anggota keluarga inti dengan riwayat gangguan mental?")
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🔍  Prediksi Sekarang", use_container_width=True)

    # ── PREDICTION RESULT ─────────────────────────────────────────────────────
    if submitted:
        raw_input = {
            "Age": age,
            "Academic Pressure": academic_pressure,
            "CGPA": cgpa,
            "Study Satisfaction": study_satisfaction,
            "Work Study Hours": work_study_hours,
            "Financial Stress": financial_stress,
            "Gender": gender,
            "Suicidal": suicidal,
            "Family History": family_hist,
            "Profession": profession,
            "Degree": degree,
            "Dietary Habits": diet,
            "Sleep Duration": sleep_dur,
        }

        try:
            X = preprocess_input(raw_input)
            pred = model.predict(X)[0]
            prob = model.predict_proba(X)[0]
            prob_depresi    = prob[1] * 100
            prob_no_depresi = prob[0] * 100

            st.markdown("---")
            st.markdown('<div class="section-title">📋 Hasil Prediksi</div>', unsafe_allow_html=True)

            if pred == 1:
                st.markdown(f"""
                <div class="result-positive">
                  <div class="result-icon">⚠️</div>
                  <div class="result-title">Terindikasi Depresi</div>
                  <div class="result-prob">Probabilitas depresi: <strong>{prob_depresi:.1f}%</strong> — Segera konsultasikan dengan profesional.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-negative">
                  <div class="result-icon">✅</div>
                  <div class="result-title">Tidak Terindikasi Depresi</div>
                  <div class="result-prob">Probabilitas tidak depresi: <strong>{prob_no_depresi:.1f}%</strong> — Tetap jaga kesehatan mentalmu!</div>
                </div>
                """, unsafe_allow_html=True)

            # Probability bars
            st.markdown(f"""
            <div class="prob-bar-wrap">
              <div class="prob-bar-label"><span>🔴 Depresi</span><span>{prob_depresi:.1f}%</span></div>
              <div class="prob-bar-bg"><div class="prob-bar-fill-red" style="width:{prob_depresi:.1f}%"></div></div>
              <div style="margin-top:1rem;"></div>
              <div class="prob-bar-label"><span>🟢 Tidak Depresi</span><span>{prob_no_depresi:.1f}%</span></div>
              <div class="prob-bar-bg"><div class="prob-bar-fill-teal" style="width:{prob_no_depresi:.1f}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

            # Input summary
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📝 Lihat Ringkasan Input Kamu"):
                summary_data = {
                    "Variabel": [
                        "Usia", "Gender", "Status", "Jenjang Pendidikan", "CGPA",
                        "Tekanan Akademik", "Kepuasan Studi", "Jam Belajar/Kerja",
                        "Durasi Tidur", "Pola Makan", "Stres Finansial",
                        "Riwayat Pikiran Bunuh Diri", "Riwayat Keluarga",
                    ],
                    "Nilai": [
                        age, gender, profession, degree, cgpa,
                        f"{academic_pressure}/5", f"{study_satisfaction}/5", f"{work_study_hours} jam",
                        sleep_dur, diet, f"{financial_stress}/5",
                        suicidal, family_hist,
                    ]
                }
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

            # Recommendations
            st.markdown("---")
            if pred == 1:
                st.markdown("""
                <div class="warn-box">
                <strong>💬 Langkah Selanjutnya:</strong><br>
                1. Jangan sendirian — bicarakan perasaanmu dengan orang yang kamu percaya<br>
                2. Hubungi layanan kesehatan mental: <strong>119 ext 8</strong> (Hotline Kemenkes RI)<br>
                3. Konsultasikan dengan psikolog atau psikiater di fasilitas kesehatan terdekat<br>
                4. Ingat: mencari bantuan adalah tanda keberanian, bukan kelemahan 💜
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box">
                <strong>💚 Tips Menjaga Kesehatan Mental:</strong><br>
                1. Pertahankan pola tidur yang baik (7–8 jam/malam)<br>
                2. Tetap aktif secara fisik dan jaga pola makan sehat<br>
                3. Luangkan waktu untuk hobi dan bersosialisasi<br>
                4. Jangan ragu konsultasi dengan psikolog jika merasa terbebani
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="disclaimer">
            ⚠️ <strong>Disclaimer:</strong> Hasil ini dihasilkan oleh model machine learning dengan akurasi ~84.6% dan bukan merupakan diagnosis medis.
            Prediksi ini dapat keliru. Jika kamu merasa tertekan atau khawatir dengan kondisi mentalmu, 
            konsultasikan dengan <strong>profesional kesehatan mental yang berlisensi</strong>. 
            Informasi yang kamu masukkan tidak disimpan oleh aplikasi ini.
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses prediksi: {e}")
            st.info("Pastikan file `best_depression_model.pkl` dan `preprocessor.pkl` berada di folder yang sama dengan `app.py`.")