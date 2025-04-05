import streamlit as st
import tempfile
from agents.cv_parser_2 import extract_text_from_pdf
from match_score import calculate_match_score

# 🎨 Page Configuration
st.set_page_config(
    page_title="AI Resume Matcher",
    layout="wide",
    page_icon="🎯"
)

# Custom CSS
st.markdown("""
    <style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1128, #1e3799);
        color: #ffffff;
    }

    .stApp {
        max-width: 100%;
    }

    /* Header Styles */
    .header-container {
        padding: 3rem 2rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(120deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.5;
    }

    /* Content Container */
    .content-container {
        padding: 1rem;
        max-width: 800px;
        margin: 1rem auto;
    }

    /* Upload Section */
    .upload-section {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Button Styles */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4338ca, #3b82f6) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #3730a3, #2563eb) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-2px);
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.1);
        color: white !important;
    }

    [data-testid="stFileUploader"] label {
        color: white !important;
    }

    [data-testid="stFileUploader"] span {
        color: white !important;
    }

    /* Make all text in the upload area white */
    [data-testid="stFileUploader"] p {
        color: white !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
        background: rgba(255, 255, 255, 0.15);
    }

    /* Score Display */
    .score-container {
        background: linear-gradient(135deg, #0a1128, #1e3799);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 2rem;
    }

    .score-value {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
    }

    .score-label {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
    }

    /* Expander Customization */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        border-radius: 8px !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Recruitment Optimizer</h1>
        <p class="subtitle">
            Upload a JD and a Resume — our AI scans, scores, and sparks instant hiring decisions. 
        </p>
    </div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# File Upload Section
jd_file = st.file_uploader("📄 Upload Job Description (PDF)", type=["pdf"])
resume_file = st.file_uploader("👤 Upload Resume (PDF)", type=["pdf"])

# Analysis Button
if st.button("🎯 Analyze Match", use_container_width=True):
    if not jd_file or not resume_file:
        st.error("⚠️ Please upload both the Job Description and Resume to proceed.")
    else:
        with st.spinner("🔄 Analyzing documents..."):
            # Process files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_jd:
                tmp_jd.write(jd_file.read())
                jd_path = tmp_jd.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_resume:
                tmp_resume.write(resume_file.read())
                resume_path = tmp_resume.name

            # Extract text
            jd_text = extract_text_from_pdf(jd_path)
            resume_text = extract_text_from_pdf(resume_path)

            # Calculate score
            score = calculate_match_score(jd_text, resume_text)

            # Display Score
            st.markdown(f"""
                <div class="score-container">
                    <div class="score-label">Match Score</div>
                    <div class="score-value">{score}%</div>
                    <div class="score-label">Compatibility between the resume and job description</div>
                </div>
            """, unsafe_allow_html=True)

            # Document Previews
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📋 Job Description Content"):
                st.markdown(jd_text)
            
            with st.expander("📄 Resume Content"):
                st.markdown(resume_text)

st.markdown('</div>', unsafe_allow_html=True)

