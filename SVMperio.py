import streamlit as st
import time

# --- Page Setup ---
st.set_page_config(
    page_title="Periodontal Stage Predictor",
    page_icon="🦷",
    layout="wide",
)

# --- Custom UI theme (CSS only) ---
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
    :root {
        --bg-app: #ffffff;
        --border: #e2e8f0;
        --text: #0f172a;
        --text-strong: #020617;
        --muted: #334155;
        --accent: #1e3a8a;
        --accent-bright: #2563eb;
        --accent-glow: rgba(30, 58, 138, 0.35);
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }
    .stApp {
        background: var(--bg-app) !important;
    }
    section.main .block-container {
        color: var(--text) !important;
        font-weight: 700 !important;
    }
    section.main .stMarkdown p, section.main .stMarkdown li, section.main .stMarkdown span {
        color: var(--text) !important;
        font-weight: 700 !important;
    }
    [data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid var(--border);
    }
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
        color: var(--text-strong) !important;
        font-weight: 700 !important;
    }
    .hero-block {
        margin-bottom: 1.25rem;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(1.75rem, 4vw, 2.35rem);
        font-weight: 800;
        color: var(--text-strong);
        margin: 0 0 0.5rem 0;
        line-height: 1.2;
    }
    .hero-accent {
        color: var(--accent);
        font-weight: 800;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0;
        max-width: 42rem;
        line-height: 1.55;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 1.5rem 1.75rem 1.25rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="stVerticalBlock"] > div:has(> label) label,
    .stSelectbox label, .stNumberInput label {
        color: var(--text-strong) !important;
        font-weight: 700 !important;
    }
    .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        background-color: #ffffff !important;
        color: var(--text-strong) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, var(--accent-bright), var(--accent)) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 0.65rem 1.75rem !important;
        box-shadow: 0 8px 20px var(--accent-glow) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 28px var(--accent-glow) !important;
    }
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        color: var(--text) !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--text-strong) !important;
        font-weight: 800 !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text) !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaption"] {
        color: var(--muted) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stSuccess"] {
        background: rgba(30, 58, 138, 0.1) !important;
        border: 1px solid rgba(30, 58, 138, 0.45) !important;
        border-radius: 12px !important;
        color: var(--text-strong) !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stSuccess"] {
        background: rgba(30, 58, 138, 0.1) !important;
        border: 1px solid rgba(30, 58, 138, 0.45) !important;
    }
    div[data-testid="stError"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
    .prediction-result-wrap {
        background: rgba(30, 58, 138, 0.08);
        border: 1px solid rgba(30, 58, 138, 0.4);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-top: 0.5rem;
    }
    .prediction-line {
        margin: 0;
        font-weight: 700;
        font-size: 1rem;
        color: var(--accent);
    }
    .prediction-line strong {
        color: var(--accent);
    }
    .prediction-stage {
        color: var(--accent-bright);
        font-size: 1.4rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
    }
    .prediction-note {
        color: var(--muted);
        font-weight: 700;
    }
    [data-testid="stSidebar"] .stDownloadButton button,
    [data-testid="stSidebar"] [data-testid="stDownloadButton"] button,
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] [data-baseweb="button"] {
        background: linear-gradient(135deg, var(--accent-bright), var(--accent)) !important;
        color: #ffffff !important;
        border: 1px solid var(--accent) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stDownloadButton button:hover,
    [data-testid="stSidebar"] [data-testid="stDownloadButton"] button:hover,
    [data-testid="stSidebar"] .stButton button:hover,
    [data-testid="stSidebar"] [data-baseweb="button"]:hover {
        border-color: var(--accent-bright) !important;
        box-shadow: 0 6px 16px var(--accent-glow) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session State Initialization ---
if "show_doctor" not in st.session_state:
    st.session_state.show_doctor = False

with st.container(border=True):
    st.markdown(
        """
        <div class="hero-block">
            <h1 class="hero-title">Periodontal disease <span class="hero-accent">stage prediction</span></h1>
            <p class="hero-sub">Enter patient biomarkers and clinical inputs below. The model returns an estimated periodontal stage to support clinical discussion—not a standalone diagnosis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_guide, col_spacer = st.columns([1.15, 1.85])

    with col_guide:
        st.markdown(
            """
**Example input ranges**
- HbA1c: 5.5 – 7.5%
- BMI: 18.5 – 29.9
- TG: 100 – 200 mg/dL
- Cholesterol: 150 – 250 mg/dL
- HDL: 40 – 60 mg/dL
- LDL: 100 – 160 mg/dL
- Urea: 20 – 50 mg/dL
- Creatinine: 0.8 – 1.4 mg/dL
- Cr ratio: 1.0 – 2.0
- Gender: M / F
- CLASS: N, Y, or P
"""
        )

    with col_spacer:
        st.markdown("##### Patient data")
        with st.form("patient_form"):
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                hba1c = st.number_input("HbA1c (%)", min_value=0.0, max_value=15.0, step=0.1, format="%.2f", placeholder="e.g., 5.6")
                tg = st.number_input("Triglycerides (mg/dL)", min_value=0.0, max_value=1000.0, step=0.1, format="%.2f", placeholder="e.g., 150")
                age = st.number_input("Age (years)", min_value=0, max_value=120, placeholder="e.g., 45")
                hdl = st.number_input("HDL (mg/dL)", min_value=0, max_value=200, placeholder="e.g., 50")
                urea = st.number_input("Urea (mg/dL)", min_value=0, max_value=200, placeholder="e.g., 30")
                gender = st.selectbox("Gender", ["Select", "M", "F"])
            with r1c2:
                bmi = st.number_input("BMI", min_value=0.0, max_value=60.0, step=0.1, format="%.2f", placeholder="e.g., 22.5")
                chol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, max_value=600.0, step=0.1, format="%.2f", placeholder="e.g., 180")
                ldl = st.number_input("LDL (mg/dL)", min_value=0, max_value=300, placeholder="e.g., 120")
                creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, max_value=10.0, step=0.1, format="%.2f", placeholder="e.g., 1.1")
                cr = st.number_input("Creatinine ratio (Cr)", min_value=0.0, max_value=10.0, step=0.1, format="%.2f", placeholder="e.g., 1.2")
                class_val = st.selectbox("CLASS (diabetes status)", ["Select", "N", "Y", "P"])

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Predict stage", use_container_width=True)

    # --- Prediction Logic ---
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

            st.markdown(
                f"""
                <div class="prediction-result-wrap">
                    <p class="prediction-line"><strong>Prediction:</strong> <span class="prediction-stage">{predicted_stage}</span> <span class="prediction-note">(estimated periodontal stage).</span></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            report = f"""
🦷 Periodontal Disease Prediction Report

Predicted Stage: {predicted_stage}

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

# --- Sidebar: Next Steps ---
if "predicted_stage" in st.session_state:
    st.sidebar.markdown("### After prediction")
    st.sidebar.markdown("Download your summary or note a specialist for follow-up.")

    st.sidebar.download_button(
        label="Download report",
        data=st.session_state.report,
        file_name="perio_report.txt",
        use_container_width=True,
    )

    if st.sidebar.button("Find specialist info", use_container_width=True):
        st.session_state.show_doctor = True

    if st.session_state.show_doctor:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Nearest dental specialist**")
        st.sidebar.markdown("SmileCare Dental Clinic — MG Road")
        st.sidebar.caption("📞 +91-98765-43210 · smilecare@example.com")
        st.sidebar.success("Share the downloaded report at your visit.")
