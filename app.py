import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import altair as alt

# Title
st.title("📄 AI Resume Analyzer - Phase 1")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Skill extraction function
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

# Skill frequency chart
def plot_skill_frequency(skills):
    if not skills:
        st.warning("No skills found to display chart.")
        return

    skill_counts = pd.Series(skills).value_counts().reset_index()
    skill_counts.columns = ['Skill', 'Frequency']

    chart = alt.Chart(skill_counts).mark_bar().encode(
        x=alt.X('Skill', sort='-y'),
        y='Frequency',
        tooltip=['Skill', 'Frequency']
    ).properties(
        title='Skill Frequency Chart',
        width=600,
        height=400
    )

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

# MAIN LOGIC
if uploaded_file:
    st.success("Resume uploaded successfully!")
    
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Resume Text:")
    st.text_area("Here's what we found in your resume:", resume_text, height=400)
    
    # Extract skills
    skills = extract_skills(resume_text)
    st.subheader("✅ Detected Skills")
    if skills:
        st.write(skills)
        plot_skill_frequency(skills)
    else:
        st.write("No matching skills found.")
    
    # Suggest job roles
    job_roles = suggest_job_roles(skills)
    st.subheader("💼 Suggested Job Roles")
    if job_roles:
        for role in job_roles:
            st.write(f"- {role}")
    else:
        st.write("No job roles found based on detected skills.")
