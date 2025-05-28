import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# ---------------------- Title ----------------------
st.title("📄 AI Resume Analyzer")

# ---------------------- File Uploader ----------------------
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# ---------------------- Functions ----------------------

# Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Skill extraction
def extract_skills(text):
    SKILL_KEYWORDS = [
        "python", "java", "c++", "machine learning", "deep learning",
        "nlp", "data science", "sql", "excel", "communication",
        "teamwork", "html", "css", "javascript", "power bi",
        "tensorflow", "pandas", "numpy", "linux", "problem solving"
    ]
    text = text.lower()
    found_skills = set()
    for skill in SKILL_KEYWORDS:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)

# Plot chart
def plot_skill_frequency(skills):
    skill_counts = pd.Series(skills).value_counts().reset_index()
    skill_counts.columns = ['Skill', 'Frequency']
    chart = alt.Chart(skill_counts).mark_bar().encode(
        x=alt.X('Skill', sort='-y'),
        y='Frequency',
        tooltip=['Skill', 'Frequency']
    ).properties(width=600, height=400)
    st.altair_chart(chart, use_container_width=True)

# Job role suggestions
JOB_ROLE_MAP = {
    "Data Scientist": ["python", "machine learning", "deep learning", "nlp", "pandas", "numpy", "tensorflow"],
    "Data Analyst": ["sql", "excel", "power bi", "tableau"],
    "Frontend Developer": ["html", "css", "javascript", "react", "angular"],
    "Backend Developer": ["python", "java", "c++", "nodejs", "django", "flask"],
    "Software Engineer": ["java", "c++", "python", "problem solving", "linux"],
    "AI Engineer": ["machine learning", "deep learning", "tensorflow", "pytorch", "nlp"],
    "Business Analyst": ["communication", "teamwork", "excel", "sql", "presentation"]
}

def suggest_job_roles(skills):
    suggested_roles = set()
    for role, required_skills in JOB_ROLE_MAP.items():
        if any(skill in skills for skill in required_skills):
            suggested_roles.add(role)
    return list(suggested_roles)

# Resume score
def score_resume(skills):
    max_possible = 20  # number of predefined keywords
    score = int((len(skills) / max_possible) * 100)
    return min(score, 100)

# Feedback
def provide_feedback(score):
    if score >= 80:
        return "Excellent resume! You're well-prepared for most roles."
    elif score >= 60:
        return "Good resume! Try adding a few more relevant skills."
    elif score >= 40:
        return "Average resume. Consider strengthening your skills section."
    else:
        return "Needs improvement. Focus on gaining key skills in your domain."

# Company role expectations
COMPANY_ROLE_SKILLS = {
    "Google": ["python", "data structures", "algorithms", "system design", "machine learning", "communication"],
    "Microsoft": ["c++", "azure", "oop", "cloud computing", "problem solving", "sql"],
    "Amazon": ["java", "scalability", "distributed systems", "aws", "leadership principles", "databases"],
    "TCS": ["java", "html", "css", "sql", "communication", "agile"],
    "Infosys": ["python", "sql", "data analysis", "presentation", "client handling"]
}

def compare_with_company(skills, company):
    required = COMPANY_ROLE_SKILLS.get(company, [])
    matched = list(set(skills) & set(required))
    missing = list(set(required) - set(skills))
    score = int((len(matched) / len(required)) * 100) if required else 0
    return matched, missing, score

# ---------------------- Main Logic ----------------------
if uploaded_file:
    st.success("Resume uploaded successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📄 Extracted Resume Text:")
    st.text_area("Here's what we found in your resume:", resume_text, height=400)

    skills = extract_skills(resume_text)
    st.subheader("✅ Detected Skills")
    if skills:
        st.write(skills)
        plot_skill_frequency(skills)

        # Job roles
        job_roles = suggest_job_roles(skills)
        st.subheader("💼 Suggested Job Roles")
        for role in job_roles:
            st.write(f"- {role}")

        # Resume score and feedback
        st.subheader("📊 Resume Score")
        score = score_resume(skills)
        st.metric(label="Skill Match Score", value=f"{score} / 100")

        st.subheader("💡 Feedback")
        feedback = provide_feedback(score)
        st.write(feedback)

        # Company match
        company = st.selectbox("🎯 Choose Target Company", list(COMPANY_ROLE_SKILLS.keys()))
        st.subheader(f"🏢 Match with {company} Requirements")
        matched, missing, match_score = compare_with_company(skills, company)
        st.success(f"✅ Matched Skills: {', '.join(matched) if matched else 'None'}")
        st.error(f"❌ Missing Skills: {', '.join(missing) if missing else 'None'}")
        st.metric(f"{company} Resume Match Score", f"{match_score}%")

    else:
        st.warning("No matching skills found.")
