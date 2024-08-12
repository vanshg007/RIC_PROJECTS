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

def get_mental_health_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Combined keywords for mental health, mindfulness, and support
mental_health_keywords = [
    "anxiety", "depression", "stress", "mental health", "well-being", "therapy", 
    "counseling", "psychologist", "psychiatrist", "mental illness", "emotional support", 
    "trauma", "coping", "self-care", "burnout", "mindfulness", "meditation", 
    "breathing exercises", "relaxation", "support groups", "helpline", "crisis line", 
    "emergency support", "mental health resources", "mental wellness", "mental fitness", 
    "mental strength", "positive thinking", "resilience", "mental clarity", "focus", 
    "calmness", "peace of mind", "emotional balance", "mental support", "self-awareness",
    "emotional intelligence", "therapy resources", "mindful breathing", "stress management",
    "guided meditation", "mindful breathing", "inner peace", "present moment", "awareness", 
    "body scan", "visualization", "yoga", "meditative practices", "safe space", "confidential",
    "peer support", "mental health professional", "therapist", "reach out", "mental health advice", 
    "self-help", "well-being support", "mental health guidance", "confidential support",
    "get help", "therapy", "talk therapy", "emotional wellness", "well-being consultation",
    "peer counseling", "emotional care", "mental well-being", "mental health support",
    "panic attack", "grief", "loneliness", "mood swings", "emotional trauma", 
    "post-traumatic stress", "suicide prevention", "mindful eating", "mindful walking",
    "art therapy", "music therapy", "journaling", "self-compassion", "compassion fatigue",
    "social anxiety", "phobia", "insomnia", "sleep disorders", "holistic therapy", 
    "exercise", "nutrition", "self-improvement", "personal growth", "goal setting", 
    "time management", "breath awareness", "emotional resilience", "empathy", "grounding techniques",
    "mindful listening", "gratitude", "self-acceptance", "body image", "self-esteem", 
    "mental toughness", "emotional regulation", "nervousness", "overwhelm", "coping mechanisms",
    "psychosomatic symptoms", "self-isolation", "well-being activities", "emotional crisis", 
    "life balance", "positive affirmations", "inner strength", "emotional exhaustion",
    "mental overload", "digital detox", "unplugging", "mindful technology use", "mindful productivity",
    "emotional burnout", "work-life balance", "social support", "peer mentoring", "emotional intelligence development","feeling","low","sad", # Additional forms
    "panic attack", "panic", "grief", "grieving", "loneliness", "lonely", "mood swings", "moody", "emotional trauma", 
    "post-traumatic stress", "post traumatic stress", "suicide prevention", "prevent suicide", "mindful eating", 
    "eating mindfully", "mindful walking", "walking mindfully", "art therapy", "music therapy", "journaling", 
    "journal", "self-compassion", "self compassion", "compassion fatigue", "social anxiety", "phobia", "phobias", 
    "insomnia", "sleeplessness", "sleep disorder", "sleep disorders", "holistic therapy", "exercise", "exercising", 
    "nutrition", "self-improvement", "self improvement", "improving self", "personal growth", "growing personally", 
    "goal setting", "setting goals", "time management", "managing time", "breath awareness", "aware of breath", 
    "emotional resilience", "resilient emotions", "empathy", "empathetic", "grounding techniques", 
    "grounding", "mindful listening", "listening mindfully", "gratitude", "being grateful", "self-acceptance", 
    "accepting oneself", "body image", "self-esteem", "self esteem", "mental toughness", "tough mind", 
    "emotional regulation", "regulating emotions", "nervousness", "nervous", "overwhelm", "overwhelmed", 
    "coping mechanisms", "coping strategy", "coping strategies", "psychosomatic symptoms", "psychosomatic", 
    "self-isolation", "isolating self", "well-being activities", "wellbeing activities", "emotional crisis", 
    "crisis management", "life balance", "balancing life", "positive affirmations", "affirming positively", 
    "inner strength", "strong inside", "emotional exhaustion", "exhausted emotionally", "mental overload", 
    "overloaded mind", "digital detox", "unplugging", "mindful technology use", "technology use mindfully", 
    "mindful productivity", "being productive mindfully", "emotional burnout", "burned out emotionally", 
    "work-life balance", "balancing work and life", "social support", "support from peers", "peer mentoring", 
    "emotional intelligence development", "developing emotional intelligence","happy", "happiness", "sad", "sadness", "angry", "anger", "frustrated", "frustration", 
    "anxious", "anxiety", "lonely", "loneliness", "excited", "excitement", "nervous", 
    "nervousness", "content", "contentment", "overwhelmed", "overwhelming", "confused", 
    "confusion", "hopeful", "hope", "worried", "worry", "disappointed", "disappointment", 
    "guilty", "guilt", "embarrassed", "embarrassment", "ashamed", "shame", "jealous", 
    "jealousy", "grateful", "gratitude", "proud", "pride", "fearful", "fear", "bored", 
    "boredom", "surprised", "surprise", "energetic", "energy", "tired", "tiredness", 
    "relieved", "relief", "insecure", "insecurity", "motivated", "motivation", "peaceful", 
    "peace", "curious", "curiosity"


]

def validate_input(user_input):
    for keyword in mental_health_keywords:
        if keyword.lower() in user_input.lower():
            return True
    return False

# Initialize Streamlit app
st.set_page_config(page_title="Student Mental Health & Well-being")

st.header("Student Mental Health & Well-being")

# Ask for the student's name if not already provided
if 'name' not in st.session_state:
    with st.form(key='name_form'):
        name = st.text_input("What is your name?", key="name_input")
        submit_name = st.form_submit_button(label='Submit')
        if submit_name and name:
            st.session_state['name'] = name
            st.session_state['chat_history'] = [("Bot", f"Hello {name}, how can I assist you with your mental health and well-being today?")]
            st.rerun()
else:
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [("Bot", f"Hello {st.session_state['name']}, how can I assist you with your mental health and well-being today?")]

    # Input text box for student input
    input = st.text_input(f"How can we assist you {st.session_state['name']}?", key="input")
    submit = st.button("Ask")

    # If the submit button is clicked and there is input
    if submit and input:
        if validate_input(input):
            st.session_state['chat_history'].append((st.session_state['name'], input))
            response = get_mental_health_response(input)
            st.subheader("Response")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            message = f"Sorry {st.session_state['name']}, it seems like your query isn't related to mental health, mindfulness, or support. Please ask a relevant question."
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
            log_file.write(f"User: {input}\nResponse: {chunk.text}\n\n")
