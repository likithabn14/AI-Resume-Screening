import streamlit as st
import plotly.express as px

from resume_parser import extract_text
from matcher import analyze_resume
from ats_score import calculate_ats_score
from pdf_report import generate_pdf
from ai_tips import generate_ai_tips

st.set_page_config(
    page_title="🤖 AI Resume Screening & ATS Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

/* Entire App Background */
.stApp{
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#161B22;
}

/* Main Title */
h1{
    color:white;
    text-align:center;
    font-weight:700;
}

/* Headings */
h2,h3{
    color:#58A6FF;
}

/* Paragraphs */
p, label{
    color:white !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:#1E1E2F;
    border-radius:15px;
    padding:18px;
    border:1px solid #30363D;
    box-shadow:0px 4px 12px rgba(0,0,0,0.4);
}

/* File Uploader */
section[data-testid="stFileUploader"]{
    background:#1E1E2F;
    border-radius:12px;
    padding:15px;
}

/* Text Area */
textarea{
    background:#1E1E2F !important;
    color:white !important;
    border-radius:10px !important;
    border:1px solid #30363D !important;
}

/* Text Input */
input{
    background:#1E1E2F !important;
    color:white !important;
}

/* Buttons */
.stButton>button{
    width:100%;
    height:50px;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#3B82F6,#9333EA);
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:linear-gradient(90deg,#2563EB,#7E22CE);
}

/* Success Boxes */
div[data-testid="stAlert"]{
    border-radius:10px;
}

/* Progress Bar */
.stProgress > div > div > div{
    background:linear-gradient(90deg,#3B82F6,#9333EA);
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.image("https://img.icons8.com/color/96/resume.png", width=80)

    st.title("ATS Analyzer")

    st.markdown("---")

    st.write("""
### 👨‍💼 About

This project helps recruiters and job seekers compare resumes with job descriptions using NLP.

### 💻 Technologies

- Python
- Streamlit
- Scikit-Learn
- Plotly
- ReportLab
- NLP
""")

    st.markdown("---")

    st.success("Version 2.0")

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="🤖 AI Resume Screening & ATS Analyzer",
    page_icon="📄",
    layout="wide"
)
# -------------------------------
# Title
# -------------------------------
st.title("🤖 AI Resume Screening & ATS Analyzer")
st.write("Upload a resume and upload or paste a Job Description to analyze the match.")

# -------------------------------
# Resume Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx", "txt"]
)

# -------------------------------
# Job Description
# -------------------------------
st.subheader("📋 Job Description")

jd_file = st.file_uploader(
    "Upload Job Description (Optional)",
    type=["pdf", "docx", "txt"],
    key="jd"
)

job_description = st.text_area(
    "Or Paste Job Description",
    height=20
)

word_count = len(job_description.split())

if word_count > 1000:
    st.error("Job Description should not exceed 1000 words.")
    st.stop()

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("🚀 Analyze Resume"):

    # Resume validation
    if uploaded_file is None:
        st.error("Please upload a Resume.")

    # JD validation
    elif jd_file is None and job_description.strip() == "":
        st.error("Please upload or paste a Job Description.")

    else:

        # -------------------------------
        # Extract Resume Text
        # -------------------------------
        resume_text = extract_text(uploaded_file)

        # -------------------------------
        # Extract JD Text
        # -------------------------------
        if jd_file is not None:
            job_description = extract_text(jd_file)

        # -------------------------------
        # Analyze Resume
        # -------------------------------
        match_percentage, matched_skills, missing_skills, recommendation = analyze_resume(
         job_description,
         resume_text
)

        ats_score, suggestions, checks, breakdown, words = calculate_ats_score(
    resume_text,
    matched_skills,
    missing_skills
)

        # -------------------------------
        # Overall Recommendation
        # -------------------------------

        overall_score = (match_percentage + ats_score) / 2

        if overall_score >= 85:
            recommendation = "🌟 Excellent Match"
            reason = "Your resume is highly optimized and closely matches the job description."

        elif overall_score >= 70:
            recommendation = "✅ Good Match"
            reason = "Your resume matches most of the required skills. A few improvements can make it stronger."

        elif overall_score >= 50:
            recommendation = "⚠️ Average Match"
            reason = "Your resume has potential but is missing some important skills or ATS elements."

        else:
            recommendation = "❌ Poor Match"
            reason = "Your resume needs significant improvements to match this job description."

        # -------------------------------
        # AI Tips
        # -------------------------------

        ai_tips = generate_ai_tips(
            matched_skills,
            missing_skills,
            ats_score
        )

        # -------------------------------
        # Analysis Completed
        # -------------------------------

        st.success("✅ Analysis Completed!")

        if ats_score >= 85:
            st.success("🌟 Excellent ATS Score")
        elif ats_score >= 70:
            st.info("👍 Good ATS Score")
        elif ats_score >= 50:
            st.warning("⚠️ Average ATS Score")
        else:
            st.error("❌ Low ATS Score")

        # ===============================
        # Dashboard
        # ===============================

        st.subheader("📊 Analysis Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Resume Match", f"{match_percentage}%")
            st.progress(min(int(match_percentage), 100))

        with col2:
            st.metric("ATS Score", f"{ats_score}/100")
            st.progress(min(int(ats_score), 100))

        with col3:
            st.metric("Recommendation", recommendation)
            st.caption(reason)

        with col4:
            st.metric("Word Count", words)

        if words < 150:
            st.caption("🔴 Too Short")

        elif words <= 600:
            st.caption("🟢 Ideal Length")

        else:
            st.caption("🟠 Too Long")   

        st.divider()

        # ===============================
        # Skills
        # ===============================

        col4, col5 = st.columns(2)

        with col4:

            st.subheader("✅ Matching Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.write(f"✔ {skill}")
            else:
                st.info("No matching skills found.")

        with col5:

            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"✖ {skill}")
            else:
                st.success("No missing skills.")

        st.divider()
        

        # ===============================
        # Pie Chart
        # ===============================

        st.subheader("📈 Skill Distribution")

        chart_data = {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [
                len(matched_skills),
                len(missing_skills)
            ]
        }

        fig = px.pie(
            chart_data,
            names="Category",
            values="Count",
            hole=0.4,
            title="Resume Skill Analysis"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()


        # ===============================
        # Suggestions
        # ===============================

        st.subheader("💡 Suggestions")

        if missing_skills:
            st.warning("Your resume can be improved by adding or strengthening these skills:")

        for skill in missing_skills:
            st.write(f"• Learn or add **{skill}**")

        if suggestions:
            for suggestion in suggestions:
                st.write(f"• {suggestion}")

        if not missing_skills and not suggestions:
            st.success("🎉 Excellent Resume! No major improvements needed.")

        # ===============================
        # AI Resume Tips
        # ===============================

        st.subheader("🤖 AI Resume Tips")

        if matched_skills:
            st.success(
                f"Great! Your resume already matches {len(matched_skills)} required skill(s)."
            )

        if missing_skills:
            st.warning(
                "Consider learning or mentioning these important skills:"
            )

            for skill in missing_skills:
                st.write(f"📌 {skill}")

    

        st.divider()

        # ===============================
        # Resume Analysis
        # ===============================

        st.subheader("📄 Resume Analysis")

        for item, status in checks.items():

            if status:
                st.success(f"✅ {item}")
            else:
                st.error(f"❌ {item}")

        st.divider()

        st.divider()

        st.subheader("🤖 AI Career Coach")

        for tip in ai_tips:
            st.info(tip)

        # ===============================
        # ATS Score Breakdown
        # ===============================

        st.subheader("📈 ATS Score Breakdown")

        import pandas as pd

        df = pd.DataFrame({
            "Category": list(breakdown.keys()),
            "Score": list(breakdown.values())
        })

        fig = px.bar(
            df,
            x="Category",
            y="Score",
            text="Score",
            title="ATS Score Breakdown"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ===============================
        # PDF Download
        # ===============================

        generate_pdf(
            "Resume_Report.pdf",
            match_percentage,
            ats_score,
            recommendation,
            matched_skills,
            missing_skills,
            suggestions
        )

        with open("Resume_Report.pdf", "rb") as pdf_file:
            st.download_button(
                label="📄 Download Analysis Report",
                data=pdf_file,
                file_name="Resume_Report.pdf",
                mime="application/pdf"
            )