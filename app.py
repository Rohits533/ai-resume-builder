import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
import io

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f1117; }
    h1 { color: #00d4ff; text-align: center; }
    p { color: #888; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📄 AI Resume Builder</h1>", unsafe_allow_html=True)
st.markdown("<p>Fill in your details — AI generates a professional resume</p>", unsafe_allow_html=True)
st.divider()

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name", placeholder="Rohit Savan")
    email = st.text_input("Email", placeholder="rohit@email.com")
    phone = st.text_input("Phone", placeholder="+91 9876543210")

with col2:
    linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/rohit")
    github = st.text_input("GitHub URL", placeholder="github.com/Rohits533")
    location = st.text_input("Location", placeholder="Mumbai, India")

st.divider()

education = st.text_area("Education", placeholder="BTech in AI & ML, XYZ University, 2024-2028", height=100)
skills = st.text_area("Skills", placeholder="Python, Machine Learning, Streamlit, LangChain, GitHub", height=80)
projects = st.text_area("Projects", placeholder="AI Chatbot Platform — Built a multi-feature AI app deployed on Streamlit", height=120)
experience = st.text_area("Experience / Internships", placeholder="Leave blank if none", height=80)
achievements = st.text_area("Achievements & Certifications", placeholder="Google AI Essentials Certificate", height=80)

st.divider()

def generate_pdf(resume_text, candidate_name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=20*mm, leftMargin=20*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                fontSize=16, textColor=colors.HexColor('#00d4ff'),
                                spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                               fontSize=10, spaceAfter=4, leading=14)
    story = []
    for line in resume_text.split('\n'):
        if line.strip() == '':
            story.append(Spacer(1, 4*mm))
        elif line.startswith('#'):
            story.append(Paragraph(line.replace('#', '').strip(), title_style))
        else:
            story.append(Paragraph(line.strip(), body_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("🚀 Generate Resume", use_container_width=True):
    if name and education and skills:
        with st.spinner("Building your resume..."):
            prompt = f"""
Create a professional resume for the following person. Format it cleanly with proper sections.
Use # for section headers.

Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}
Location: {location}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Achievements & Certifications:
{achievements}

Instructions:
- Format as a clean professional resume
- Use # for each section header
- Make it ATS friendly
- Keep it concise and impactful
- Use action verbs for project descriptions
- Make it suitable for a BTech student applying for internships
"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer. Create professional, ATS-friendly resumes for students and fresh graduates."},
                    {"role": "user", "content": prompt}
                ]
            )
            resume = response.choices[0].message.content

        st.markdown("### ✅ Your Resume")
        st.markdown(resume)
        st.divider()

        pdf_buffer = generate_pdf(resume, name)
        st.download_button(
            label="📥 Download Resume as PDF",
            data=pdf_buffer,
            file_name=f"{name}_Resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.warning("Please fill in at least Name, Education and Skills!")
