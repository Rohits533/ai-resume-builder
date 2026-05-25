import streamlit as st
from groq import Groq

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

education = st.text_area("Education", placeholder="BTech in AI & ML, XYZ University, 2024-2028\nClass 12 - 90%, ABC School, 2024", height=100)
skills = st.text_area("Skills", placeholder="Python, Machine Learning, Streamlit, LangChain, GitHub, SQL", height=80)
projects = st.text_area("Projects", placeholder="AI Chatbot Platform — Built a multi-feature AI app with web search, PDF reader, code explainer deployed on Streamlit\nStudent Performance Analyzer — ML model to predict student grades", height=120)
experience = st.text_area("Experience / Internships", placeholder="Leave blank if none, or add any internships, freelance work, etc.", height=80)
achievements = st.text_area("Achievements & Certifications", placeholder="Google AI Essentials Certificate\nTop 10 in School Hackathon 2024", height=80)

st.divider()

if st.button("🚀 Generate Resume", use_container_width=True):
    if name and education and skills:
        with st.spinner("Building your resume..."):
            prompt = f"""
Create a professional resume for the following person. Format it cleanly with proper sections.

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
- Use proper sections with headers
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
        st.download_button(
            label="📥 Download Resume as Text",
            data=resume,
            file_name=f"{name}_Resume.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.warning("Please fill in at least Name, Education and Skills!")
