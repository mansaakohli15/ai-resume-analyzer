# 🚀 AI Career Copilot

An AI-powered career preparation platform that helps students land internships and jobs through resume analysis, mock interviews, and personalized learning roadmaps.

## 🌐 Live Demo
[Click here to try it live](https://ai-resume-analyzer-ld5fielfxf5zdsibczeavu.streamlit.app/)

## 🎯 What it does

### 📄 AI Resume Analyzer
- Upload your resume as PDF
- Paste any job description
- Get ATS match score out of 100
- See missing keywords, weak sections, and improvement suggestions

### 🎤 AI Mock Interview
- Choose your target role
- Answer 5 AI-generated interview questions
- Get scored and evaluated on every answer
- See what was good, what was missing, and ideal answer hints

### 🗺️ Personalized Learning Roadmap
- Select your target role and timeframe
- Enter your current skills
- Get a week-by-week preparation plan with resources and projects

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | LLaMA 3.3 70B via Groq API |
| PDF Parsing | PyMuPDF |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

## 🚀 Run Locally

1. Clone the repo
git clone https://github.com/mansaakohli15/ai-resume-analyzer.git

2. Install dependencies
pip install -r requirements.txt

3. Create a `.env` file and add your Groq API key
GROQ_API_KEY=your_key_here

4. Run the app
streamlit run app.py

## 📸 Features Preview

- Resume analyzed against real job descriptions
- Visual ATS match score with color coding
- 5-question adaptive mock interview
- Custom roadmap based on your timeline and skills

## 👩‍💻 Author
Mansaa Kohli — [GitHub](https://github.com/mansaakohli15)

