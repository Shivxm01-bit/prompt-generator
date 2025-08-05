import streamlit as st
import pandas as pd
import random
import os

# ------------------ Configuration ------------------ #
st.set_page_config(page_title="AI Prompt Generator", page_icon="🤖", layout="centered")

# ------------------ Load/Create Users CSV ------------------ #
USER_CSV = "users.csv"
if not os.path.exists(USER_CSV):
    pd.DataFrame(columns=["username", "password", "country", "language"]).to_csv(USER_CSV, index=False)

# ------------------ User Authentication ------------------ #
def load_users():
    return pd.read_csv(USER_CSV)

def save_user(username, password, country, language):
    df = load_users()
    if username in df["username"].values:
        return False
    df = pd.concat([df, pd.DataFrame([{
        "username": username, "password": password,
        "country": country, "language": language
    }])], ignore_index=True)
    df.to_csv(USER_CSV, index=False)
    return True

def check_credentials(username, password):
    df = load_users()
    match = df[(df["username"] == username) & (df["password"] == password)]
    return not match.empty

# ------------------ Prompt Logic ------------------ #
prompt_templates = {
    "Customer Support": [
        "You are a helpful customer support agent. Respond kindly to the user's question: \"{user_input}\"",
        "Politely help the customer resolve: \"{user_input}\""
    ],
    "HR Bot": [
        "You are an HR assistant. Answer this employee's query: \"{user_input}\"",
        "Respond as a friendly HR bot to: \"{user_input}\""
    ],
    "Educational Assistant": [
        "You are a tutor. Explain the concept of: \"{user_input}\"",
        "Teach the user about: \"{user_input}\""
    ],
    "Healthcare Assistant": [
        "You are a virtual health assistant. Give initial advice for: \"{user_input}\"",
        "Help the patient understand symptoms like: \"{user_input}\""
    ]
}

def generate_prompt(domain, user_input):
    template = random.choice(prompt_templates[domain])
    return template.replace("{user_input}", user_input)

def suggest_improvements(domain, user_input, filled_prompt):
    return [
        filled_prompt + "\n- Keep your answer concise and polite.",
        f"Act like an expert in {domain.lower()}. Answer: \"{user_input}\" in a step-by-step manner.",
        f"You are an AI assistant. Based on the following query: \"{user_input}\", provide a detailed yet friendly response."
    ]

def similarity_scores(base_prompt, suggestions):
    def simple_similarity(a, b):
        set_a = set(a.lower().split())
        set_b = set(b.lower().split())
        return round(len(set_a & set_b) / len(set_a | set_b), 2) if set_a | set_b else 0.0
    return [simple_similarity(base_prompt, s) for s in suggestions]

# ------------------ Theme: Dark Mode ------------------ #
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown("<style>body{background-color: #0e1117; color: white;}</style>", unsafe_allow_html=True)

# ------------------ Login/Signup Logic ------------------ #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    mode = st.sidebar.radio("Select Mode", ["Login", "Signup"])
    st.title("🔐 AI Prompt Generator - Auth")

    if mode == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")
    else:
        new_user = st.text_input("Choose a Username")
        new_pass = st.text_input("Choose a Password", type="password")
        country = st.selectbox("Country", ["India", "USA", "Germany", "France", "Other"])
        language = st.selectbox("Language", ["English", "Hindi", "German", "French", "Other"])
        if st.button("Create Account"):
            if save_user(new_user, new_pass, country, language):
                st.success("Account created! Please login now.")
            else:
                st.warning("Username already exists. Try another.")
    st.stop()

# ------------------ Logged-In Interface ------------------ #
st.sidebar.success(f"Welcome, {st.session_state.username}!")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🤖 AI Prompt Generator for Chatbots")

domain = st.selectbox("Select Chatbot Domain", list(prompt_templates.keys()))
user_input = st.text_area("Enter the user query or context")

if st.button("Generate Prompt"):
    base_prompt = generate_prompt(domain, user_input)
    st.subheader("🎯 Generated Prompt")
    st.code(base_prompt)

    suggestions = suggest_improvements(domain, user_input, base_prompt)
    scores = similarity_scores(base_prompt, suggestions)

    st.subheader("✨ Improved Prompt Suggestions")
    for i, suggestion in enumerate(suggestions):
        st.markdown(f"**Option {i+1}**")
        st.code(suggestion)
        st.markdown(f"🧠 Similarity Score: {scores[i]}")
