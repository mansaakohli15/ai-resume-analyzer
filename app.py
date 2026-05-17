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

Give a detailed analysis with these sections:

1. MATCH SCORE (out of 100)
2. STRONG POINTS (what the resume does well)
3. MISSING KEYWORDS (important keywords from JD missing in resume)
4. WEAK SECTIONS (parts that need improvement)
5. IMPROVEMENT SUGGESTIONS (specific rewrites or additions)
6. FINAL VERDICT (should they apply? what to fix first?)

Be specific, honest, and helpful.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste the job description to get AI-powered feedback.")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze My Resume"):
    if resume_file is None:
        st.warning("Please upload your resume.")
    elif job_description.strip() == "":
        st.warning("Please paste the job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(resume_file)
            result = analyze_resume(resume_text, job_description)
        st.success("Analysis Complete!")
        st.markdown(result)