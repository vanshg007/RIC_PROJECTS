# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI library with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_career_guidance_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Keywords for different career counseling categories
# Updated Keywords for Career Exploration
career_exploration_keywords = [
    "interest", "passion", "explore", "career options", "field", "industry", "path", 
    "opportunity", "profession", "skills", "strengths", "weaknesses", "career test", 
    "self-assessment", "goal", "aspiration", "dream job", "ambition", 
    "future", "motivation", "decision making", "career growth", "work-life balance", 
    "career change", "career shift", "job roles", "job sectors", "job trends", 
    "market demand", "potential", "salary expectations", "job stability", "learning", 
    "certifications", "training", "qualifications", "higher education", 
    "undergraduate", "postgraduate", "vocational training", "career fairs", 
    "workshops", "webinars", "career counseling", "aptitude", "personality", 
    "entrepreneurship", "business", "creative arts", "STEM", "humanities", "career advancement","field","fields"
]

# Updated Keywords for Mentor Connection
mentor_connection_keywords = [
    "mentor", "guidance", "advice", "support", "connect", "network", "industry expert", 
    "career advice", "consultation", "career coach", "experience", "insights", 
    "professional", "shadowing", "internship", "apprenticeship", 
    "career development", "career mentor", "role model", "leadership", 
    "mentorship programs", "peer mentoring", "alumni", "industry leader", 
    "job shadowing", "career coaching", "career goals", "job search strategies", 
    "career growth", "personal development", "career guidance", "career planning", 
    "resume building", "interview preparation", "job applications", "career transitions", 
    "career success", "industry trends", "networking events", "career workshops", 
    "career services", "career opportunities", "career counseling", "job referrals", 
    "career pathways", "job market insights", "professional network", "career resources", 
    "online mentoring", "career management", "mentoring relationships","profile","linkedin"
]

# Updated Keywords for Personalized Guidance
personalized_guidance_keywords = [
    "personalized", "customized", "tailored", "specific", "situation", "individual", 
    "background", "experience", "qualification", "academic", "education", 
    "degree", "course", "certification", "career change", "job market", 
    "job search", "resume", "cover letter", "interview", "career plan", "career development", 
    "career path", "career objective", "skill set", "career goals", "job offers", 
    "job market trends", "career opportunities", "job placement", "employment history", 
    "job readiness", "career satisfaction", "career fulfillment", "personal interests", 
    "job fit", "work experience", "career advancement", "career decisions", "job search strategy", 
    "career trajectory", "career options", "professional development", "career assessment", 
    "strengths", "weaknesses", "career growth", "career counseling", "job opportunities", 
    "career exploration", "personal growth", "career success", "career transition"
]
category_keywords = {
    "Career Exploration": career_exploration_keywords,
    "Mentor Connection": mentor_connection_keywords,
    "Personalized Guidance": personalized_guidance_keywords
}

def validate_input(category, user_input):
    keywords = category_keywords.get(category, [])
    for keyword in keywords:
        if keyword.lower() in user_input.lower():
            return True
    return False

# Initialize Streamlit app
st.set_page_config(page_title="Career Counseling Tool")

st.header("Career Counseling Tool")

# Ask for the student's name if not already provided
if 'name' not in st.session_state:
    with st.form(key='name_form'):
        name = st.text_input("What is your name?", key="name_input")
        submit_name = st.form_submit_button(label='Submit')
        if submit_name and name:
            st.session_state['name'] = name
            st.session_state['chat_history'] = [("Bot", f"Hello {name}, how can I assist you with your career today?")]
            st.rerun()
else:
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [("Bot", f"Hello {st.session_state['name']}, how can I assist you with your career today?")]

    # Add sections for different types of career counseling
    st.sidebar.header("Career Counseling Categories")
    categories = ["Career Exploration", "Mentor Connection", "Personalized Guidance"]
    category = st.sidebar.selectbox("Select a category", categories)

    # Input text box for student input
    input = st.text_input(f"How can we assist you {st.session_state['name']}?", key="input")
    submit = st.button("Ask")

    # If the submit button is clicked and there is input
    if submit and input:
        if validate_input(category, input):
            st.session_state['chat_history'].append((st.session_state['name'], input))
            response = get_career_guidance_response(f"[{category}] {input}")
            st.subheader("Response")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            message = f"Sorry {st.session_state['name']}, please ask questions related to {category}."
            st.write(message)
            st.session_state['chat_history'].append((st.session_state['name'], input))
            st.session_state['chat_history'].append(("Bot", message))

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    # Add logging (optional)
    if submit and input:
        with open("chat_log.txt", "a") as log_file:
            log_file.write(f"Category: {category}\nUser: {input}\nResponse: {chunk.text}\n\n")