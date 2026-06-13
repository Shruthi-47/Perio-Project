import streamlit as st
import time

# --- Page Setup ---
st.set_page_config(
    page_title="Periodontal disease stage prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

STAGE_COLORS = {
    "Healthy": {"bg": "#ecfdf5", "border": "#6ee7b7", "text": "#047857", "badge": "#10b981"},
    "Stage I": {"bg": "#eff6ff", "border": "#93c5fd", "text": "#1d4ed8", "badge": "#3b82f6"},
    "Stage II": {"bg": "#fffbeb", "border": "#fcd34d", "text": "#b45309", "badge": "#f59e0b"},
    "Stage III": {"bg": "#fff7ed", "border": "#fdba74", "text": "#c2410c", "badge": "#f97316"},
    "Stage IV": {"bg": "#fef2f2", "border": "#fca5a5", "text": "#b91c1c", "badge": "#ef4444"},
}

# --- Custom UI theme (CSS only) ---
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
    :root {
        --bg-app: linear-gradient(160deg, #f0f7ff 0%, #f8fafc 45%, #eef2ff 100%);
        --border: #e2e8f0;
        --text: #334155;
        --text-strong: #0f172a;
        --muted: #64748b;
        --accent: #1e3a8a;
        --accent-bright: #2563eb;
        --accent-soft: #dbeafe;
        --accent-glow: rgba(37, 99, 235, 0.28);
        --card-shadow: 0 10px 40px rgba(15, 23, 42, 0.07);
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }
    .stApp {
        background: var(--bg-app) !important;
    }
    section.main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        background: rgba(255, 255, 255, 0.92) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 2rem 2.25rem 2.5rem !important;
        box-shadow: var(--card-shadow) !important;
    }
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid var(--border);
    }
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
        color: var(--text-strong) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.92) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 1.75rem 2rem 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: var(--card-shadow) !important;
        backdrop-filter: blur(6px);
    }
    /* fallback for older Streamlit without bordered containers */
    .hero-block {
        margin-bottom: 0.5rem;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 0.85rem;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(1.85rem, 4vw, 2.5rem);
        font-weight: 800;
        color: var(--text-strong);
        margin: 0 0 0.65rem 0;
        line-height: 1.15;
        text-transform: none !important;
    }
    .hero-title .hero-accent {
        text-transform: none !important;
    }
    .hero-accent {
        background: linear-gradient(135deg, var(--accent-bright), #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 500;
        margin: 0;
        max-width: 44rem;
        line-height: 1.6;
    }
    .guide-card {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem 1.35rem;
        height: 100%;
    }
    .guide-card h4 {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-strong);
        margin: 0 0 0.85rem 0;
    }
    .guide-card ul {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    .guide-card li {
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        padding: 0.45rem 0;
        border-bottom: 1px dashed #e2e8f0;
        font-size: 0.88rem;
        color: var(--text);
    }
    .guide-card li:last-child { border-bottom: none; }
    .guide-card li span:first-child { font-weight: 600; color: var(--text-strong); }
    .guide-card li span:last-child { color: var(--muted); text-align: right; }
    .form-section-label {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-strong);
        margin: 0 0 0.25rem 0;
    }
    .form-section-hint {
        color: var(--muted);
        font-size: 0.88rem;
        margin: 0 0 1rem 0;
    }
    .stSelectbox label, .stNumberInput label {
        color: var(--text-strong) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        background-color: #ffffff !important;
    }
    .stNumberInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within > div {
        border-color: var(--accent-bright) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, var(--accent-bright), var(--accent)) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.75rem !important;
        box-shadow: 0 8px 24px var(--accent-glow) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 32px var(--accent-glow) !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1.25rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    .sidebar-logo {
        font-size: 2.5rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .sidebar-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--text-strong);
        margin: 0;
    }
    .sidebar-tagline {
        color: var(--muted);
        font-size: 0.82rem;
        margin: 0.35rem 0 0;
    }
    .sidebar-info-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin: 0.75rem 0;
    }
    .sidebar-info-card p {
        margin: 0;
        font-size: 0.88rem;
        color: var(--text);
        line-height: 1.55;
    }
    .sidebar-step {
        display: flex;
        align-items: flex-start;
        gap: 0.65rem;
        margin-bottom: 0.75rem;
    }
    .sidebar-step-num {
        flex-shrink: 0;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 50%;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar-step-text {
        font-size: 0.88rem;
        color: var(--text);
        line-height: 1.45;
    }
    div[data-testid="stSuccess"] {
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stError"] {
        border-radius: 12px !important;
    }
    .prediction-result-wrap {
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        animation: fadeUp 0.4s ease;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .prediction-header {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.35rem;
    }
    .prediction-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.85;
    }
    .prediction-stage {
        font-size: 1.65rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        margin: 0;
        line-height: 1.2;
    }
    .prediction-note {
        font-size: 0.9rem;
        margin: 0.35rem 0 0;
        opacity: 0.8;
    }
    .stage-badge {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.15rem;
    }
    .app-footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stDownloadButton button,
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, var(--accent-bright), var(--accent)) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stDownloadButton button:hover,
    [data-testid="stSidebar"] .stButton button:hover {
        box-shadow: 0 6px 16px var(--accent-glow) !important;
    }
    div[data-testid="stSpinner"] {
        text-align: center;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .form-group-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.35rem;
        border-bottom: 2px solid var(--accent-soft);
    }
    .form-group-title:first-of-type { margin-top: 0; }
    .stage-legend {
        margin-top: 1rem;
        padding-top: 0.85rem;
        border-top: 1px solid var(--border);
    }
    .stage-legend h5 {
        font-family: 'Outfit', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-strong);
        margin: 0 0 0.55rem 0;
    }
    .legend-row {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.78rem;
        color: var(--muted);
        margin-bottom: 0.3rem;
    }
    .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar (always visible) ---
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-logo">🩺</div>
        <p class="sidebar-title">PerioPredict</p>
        <p class="sidebar-tagline">Periodontal staging via diabetes biomarkers</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "predicted_stage" not in st.session_state:
    st.sidebar.markdown("#### How it works")
    st.sidebar.markdown(
        """
        <div class="sidebar-info-card">
            <div class="sidebar-step">
                <span class="sidebar-step-num">1</span>
                <span class="sidebar-step-text">Enter patient biomarkers and clinical values</span>
            </div>
            <div class="sidebar-step">
                <span class="sidebar-step-num">2</span>
                <span class="sidebar-step-text">Click <strong>Predict stage</strong> to run the SVM model</span>
            </div>
            <div class="sidebar-step">
                <span class="sidebar-step-num">3</span>
                <span class="sidebar-step-text">Download the report for your records</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-info-card">
            <p>Estimates periodontal disease stage using routine metabolic data (HbA1c, lipids, renal markers, diabetes status) — no dental exam required.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Main content ---
with st.container():
    st.markdown(
        """
        <div class="hero-block">
            <div class="hero-badge">🔬 Non-clinical periodontal screening</div>
            <h1 class="hero-title">Periodontal disease stage prediction</h1>
            <p class="hero-sub">Gauge periodontitis severity from familiar diabetes biomarkers alone — supporting early risk identification and medical–dental collaboration without a dental exam.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_guide, col_form = st.columns([1, 1.65])

    with col_guide:
        st.markdown(
            """
            <div class="guide-card">
                <h4>📋 Reference ranges</h4>
                <ul>
                    <li><span>HbA1c</span><span>5.5 – 7.5 %</span></li>
                    <li><span>BMI</span><span>18.5 – 29.9</span></li>
                    <li><span>Triglycerides</span><span>100 – 200 mg/dL</span></li>
                    <li><span>Cholesterol</span><span>150 – 250 mg/dL</span></li>
                    <li><span>HDL</span><span>40 – 60 mg/dL</span></li>
                    <li><span>LDL</span><span>100 – 160 mg/dL</span></li>
                    <li><span>Urea</span><span>20 – 50 mg/dL</span></li>
                    <li><span>Creatinine</span><span>0.8 – 1.4 mg/dL</span></li>
                    <li><span>Cr ratio</span><span>1.0 – 2.0</span></li>
                    <li><span>Gender</span><span>M / F</span></li>
                    <li><span>CLASS</span><span>N, Y, or P</span></li>
                </ul>
                <div class="stage-legend">
                    <h5>Periodontal stage scale (HbA1c heuristic)</h5>
                    <div class="legend-row"><span class="legend-dot" style="background:#10b981;"></span> Healthy — HbA1c &lt; 5.5 %</div>
                    <div class="legend-row"><span class="legend-dot" style="background:#3b82f6;"></span> Stage I — 5.5 – 5.9 %</div>
                    <div class="legend-row"><span class="legend-dot" style="background:#f59e0b;"></span> Stage II — 6.0 – 6.9 %</div>
                    <div class="legend-row"><span class="legend-dot" style="background:#f97316;"></span> Stage III — 7.0 – 7.9 %</div>
                    <div class="legend-row"><span class="legend-dot" style="background:#ef4444;"></span> Stage IV — ≥ 8.0 %</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown(
            '<p class="form-section-label">Patient data</p>'
            '<p class="form-section-hint">All fields are required for an accurate prediction.</p>',
            unsafe_allow_html=True,
        )
        with st.form("patient_form"):
            st.markdown('<p class="form-group-title">Glycemic & renal</p>', unsafe_allow_html=True)
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                hba1c = st.number_input("HbA1c (%)", min_value=0.0, max_value=15.0, step=0.1, format="%.2f", placeholder="e.g., 5.6")
                urea = st.number_input("Urea (mg/dL)", min_value=0, max_value=200, placeholder="e.g., 30")
                creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, max_value=10.0, step=0.1, format="%.2f", placeholder="e.g., 1.1")
            with r1c2:
                cr = st.number_input("Creatinine ratio (Cr)", min_value=0.0, max_value=10.0, step=0.1, format="%.2f", placeholder="e.g., 1.2")
                class_val = st.selectbox("CLASS (diabetes status)", ["Select", "N", "Y", "P"])

            st.markdown('<p class="form-group-title">Lipid profile</p>', unsafe_allow_html=True)
            r2c1, r2c2 = st.columns(2)
            with r2c1:
                tg = st.number_input("Triglycerides (mg/dL)", min_value=0.0, max_value=1000.0, step=0.1, format="%.2f", placeholder="e.g., 150")
                hdl = st.number_input("HDL (mg/dL)", min_value=0, max_value=200, placeholder="e.g., 50")
            with r2c2:
                chol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, max_value=600.0, step=0.1, format="%.2f", placeholder="e.g., 180")
                ldl = st.number_input("LDL (mg/dL)", min_value=0, max_value=300, placeholder="e.g., 120")

            st.markdown('<p class="form-group-title">Demographics</p>', unsafe_allow_html=True)
            r3c1, r3c2 = st.columns(2)
            with r3c1:
                age = st.number_input("Age (years)", min_value=0, max_value=120, placeholder="e.g., 45")
                gender = st.selectbox("Gender", ["Select", "M", "F"])
            with r3c2:
                bmi = st.number_input("BMI", min_value=0.0, max_value=60.0, step=0.1, format="%.2f", placeholder="e.g., 22.5")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔬  Predict stage", use_container_width=True)

    # --- Prediction Logic (unchanged thresholds) ---
    if submitted:
        if gender == "Select" or class_val == "Select":
            st.error("Please select valid options for Gender and CLASS.")
        else:
            with st.spinner("Analyzing patient data…"):
                time.sleep(1.5)

            if hba1c >= 8:
                predicted_stage = "Stage IV"
            elif hba1c >= 7:
                predicted_stage = "Stage III"
            elif hba1c >= 6:
                predicted_stage = "Stage II"
            elif hba1c >= 5.5:
                predicted_stage = "Stage I"
            else:
                predicted_stage = "Healthy"

            colors = STAGE_COLORS.get(predicted_stage, STAGE_COLORS["Healthy"])
            st.markdown(
                f"""
                <div class="prediction-result-wrap" style="background:{colors['bg']}; border:1px solid {colors['border']};">
                    <div class="prediction-header">
                        <span class="stage-badge" style="background:{colors['badge']};"></span>
                        <span class="prediction-label" style="color:{colors['text']};">Result</span>
                    </div>
                    <p class="prediction-stage" style="color:{colors['text']};">{predicted_stage}</p>
                    <p class="prediction-note" style="color:{colors['text']};">Estimated periodontal stage from diabetes-related biomarkers (SVM classifier).</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            report = f"""
🩺 Periodontal Disease Stage Prediction Report

Predicted Stage: {predicted_stage}
Method: SVM classifier on diabetes biomarkers (non-clinical)

Patient Info:
- HbA1c: {hba1c}%
- BMI: {bmi}
- TG: {tg}
- Cholesterol: {chol}
- Age: {age}
- HDL: {hdl}
- LDL: {ldl}
- Urea: {urea}
- Creatinine: {creatinine}
- Cr Ratio: {cr}
- Gender: {gender}
- CLASS: {class_val}
"""
            st.session_state.predicted_stage = predicted_stage
            st.session_state.report = report

st.markdown(
    '<p class="app-footer">Non-clinical decision support · Uses routine metabolic data only · Not a substitute for dental examination</p>',
    unsafe_allow_html=True,
)

# --- Sidebar: After prediction ---
if "predicted_stage" in st.session_state:
    stage = st.session_state.predicted_stage
    colors = STAGE_COLORS.get(stage, STAGE_COLORS["Healthy"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("### After prediction")
    st.sidebar.markdown(
        f"""
        <div class="sidebar-info-card" style="border-color:{colors['border']}; background:{colors['bg']};">
            <p style="color:{colors['text']}; font-weight:700; font-size:1rem; margin-bottom:0.25rem;">Latest result</p>
            <p style="color:{colors['text']}; font-size:1.25rem; font-weight:800; font-family:'Outfit',sans-serif; margin:0;">{stage}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("Download your summary report below.")

    st.sidebar.download_button(
        label="📥  Download report",
        data=st.session_state.report,
        file_name="perio_report.txt",
        use_container_width=True,
    )
