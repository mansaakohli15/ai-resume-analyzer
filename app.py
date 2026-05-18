import streamlit as st
from groq import Groq
import fitz
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert resume coach and ATS specialist.

Analyze this resume against the job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give a detailed analysis in EXACTLY this format, do not deviate:

MATCH_SCORE: [number between 0-100]

STRONG_POINTS:
- [point 1]
- [point 2]
- [point 3]

MISSING_KEYWORDS:
- [keyword 1]
- [keyword 2]
- [keyword 3]

WEAK_SECTIONS:
- [section 1]
- [section 2]

IMPROVEMENT_SUGGESTIONS:
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]

FINAL_VERDICT:
[2-3 sentences on whether they should apply and what to fix first]

Be specific, honest, and helpful.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_result(result):
    sections = {
        "match_score": 0,
        "strong_points": [],
        "missing_keywords": [],
        "weak_sections": [],
        "improvement_suggestions": [],
        "final_verdict": ""
    }
    
    lines = result.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("MATCH_SCORE:"):
            try:
                sections["match_score"] = int(''.join(filter(str.isdigit, line.split(":")[1])))
            except:
                sections["match_score"] = 0
        elif line == "STRONG_POINTS:":
            current_section = "strong_points"
        elif line == "MISSING_KEYWORDS:":
            current_section = "missing_keywords"
        elif line == "WEAK_SECTIONS:":
            current_section = "weak_sections"
        elif line == "IMPROVEMENT_SUGGESTIONS:":
            current_section = "improvement_suggestions"
        elif line == "FINAL_VERDICT:":
            current_section = "final_verdict"
        elif line.startswith("- ") and current_section in ["strong_points", "missing_keywords", "weak_sections", "improvement_suggestions"]:
            sections[current_section].append(line[2:])
        elif current_section == "final_verdict" and line:
            sections["final_verdict"] += line + " "
    
    return sections

# UI
st.set_page_config(page_title="AI Career Copilot", page_icon="🚀", layout="wide")

st.title("🚀 AI Career Copilot")
st.write("Upload your resume and paste the job description to get AI-powered feedback.")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("📋 Paste the Job Description here", height=200)

if st.button("🔍 Analyze My Resume", use_container_width=True):
    if resume_file is None:
        st.warning("Please upload your resume.")
    elif job_description.strip() == "":
        st.warning("Please paste the job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(resume_file)
            result = analyze_resume(resume_text, job_description)
            parsed = parse_result(result)

        st.success("Analysis Complete!")
        st.divider()

        # Match Score
        score = parsed["match_score"]
        st.subheader("📊 Match Score")
        if score >= 75:
            color = "green"
        elif score >= 50:
            color = "orange"
        else:
            color = "red"
        
        st.markdown(f"### :{color}[{score}/100]")
        st.progress(score/100)
        st.divider()

        # Three columns for results
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("✅ Strong Points")
            for point in parsed["strong_points"]:
                st.success(point)

        with col2:
            st.subheader("❌ Missing Keywords")
            for keyword in parsed["missing_keywords"]:
                st.error(keyword)

        with col3:
            st.subheader("⚠️ Weak Sections")
            for section in parsed["weak_sections"]:
                st.warning(section)

        st.divider()
        st.subheader("💡 Improvement Suggestions")
        for i, suggestion in enumerate(parsed["improvement_suggestions"], 1):
            st.info(f"{i}. {suggestion}")

        st.divider()
        st.subheader("🎯 Final Verdict")
        st.markdown(f"> {parsed['final_verdict']}")