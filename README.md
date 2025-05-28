#  AI Resume Analyzer

A Streamlit-based web application that intelligently analyzes PDF resumes to extract skills, suggest job roles, evaluate skill match scores, provide improvement feedback, and now even compare your resume against company-specific requirements like Google, Microsoft, etc.

---

##  Features

-  Upload PDF resume
-  Extract skills using keyword matching
-  Visualize skill frequency via bar chart
-  Suggest relevant job roles
-  Calculate resume match score
-  Provide skill-based feedback
-  Match resume with top company expectations (Google, Microsoft, Amazon, etc.)

---

##  Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Libraries**:
  - `PyMuPDF` – Extract text from PDFs
  - `Pandas` – Skill frequency analysis
  - `Altair` – Skill bar chart visualization
  - `Matplotlib` – Optional for future charts

---

##  How to Run

```bash
git clone https://github.com/afreenshannu/resume_analyzer.git
cd resume_analyzer
pip install -r requirements.txt
streamlit run app.py
