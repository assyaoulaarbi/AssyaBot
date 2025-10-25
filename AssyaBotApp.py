import streamlit as st
from openai_helper import ask_openai  # your function
import base64
from openai import OpenAI
import time


# -----------------------
# Page configuration
# -----------------------
st.set_page_config(
    page_title="AssyaBot AI",
    page_icon="🧠💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Background Image Function
# -----------------------
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background
set_background("Background.png")

# -----------------------
# Custom CSS Styles
# -----------------------
st.markdown(
    """
    <style>
    h1 {
        color: #FF1493;
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    .user {
        background-color: rgba(255, 182, 193, 0.8);
        padding: 10px;
        border-radius: 12px;
        text-align: right;
        margin: 5px;
    }
    .bot {
        background-color: rgba(230, 230, 250, 0.8);
        padding: 10px;
        border-radius: 12px;
        text-align: left;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Sidebar
# -----------------------
st.sidebar.image("CartoonBrain.png", width=250)
st.sidebar.markdown("<h2 style='text-align:center;'>🧠 AssyaBot AI</h2>", unsafe_allow_html=True)
st.sidebar.write("""
💡 *Your futuristic AI educational assistant*  
🎯 Learn, experiment, and explore AI  
🌟 Mind + tech powered
""")

# -----------------------
# Developer Mode Access (Hidden from users)
# -----------------------
DEV_PASSWORD = "25v5mrd4ypyFW"   # <--- CHANGE THIS PASSWORD

if "dev_unlocked" not in st.session_state:
    st.session_state.dev_unlocked = False

if not st.session_state.dev_unlocked:
    dev_pass = st.sidebar.text_input(" ", placeholder="🔒 Developer login", type="password")
    if dev_pass == DEV_PASSWORD:
        st.session_state.dev_unlocked = True
        st.sidebar.success("🟣 Developer Mode Enabled")
else:
    st.sidebar.success("🟣 Developer Mode Active")

    # Reset demo limit button (ONLY visible to you)
    if st.sidebar.button("🔄 Reset My Demo Limit"):
        st.session_state.question_count = 0
        st.session_state.messages.append({
            "role": "assistant",
            "content": "✅ Limit reset! You can chat again 💬"
        })

# -----------------------
# Header
# -----------------------
st.markdown("<h1>AssyaBot AI 🤖</h1>", unsafe_allow_html=True)

# -----------------------
# Initialize messages
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Chat input (Enter to send, auto-clear, no button, demo limit)
# -----------------------

# One-time session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "submitted_text" not in st.session_state:
    st.session_state.submitted_text = ""
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# Style
st.markdown("""
<style>
.label-small { color:white; font-size:14px; margin-bottom:-6px; }
.input-field {
    width:100%; max-width:900px; height:48px; padding:10px 14px;
    border-radius:10px; border:1px solid #ccc;
    background:rgba(255,255,255,0.9); font-size:16px; color:black; margin:auto;
}
</style>
""", unsafe_allow_html=True)

# Label
st.markdown("<p class='label-small'>Ask me anything...</p>", unsafe_allow_html=True)

# --- Input callback (triggered when Enter is pressed) ---
def _submit():
    st.session_state.submitted_text = st.session_state.user_input
    st.session_state.user_input = ""   # safely clear the input field

# Text input box
st.text_input(
    "",
    key="user_input",
    label_visibility="collapsed",
    on_change=_submit
)

# --- Process submitted message ---
if st.session_state.submitted_text:
    user_input = st.session_state.submitted_text
    st.session_state.submitted_text = ""  # consume stored message

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show thinking animation
    placeholder = st.empty()
    placeholder.markdown("""
    <div style="text-align:center; font-size:18px; color:white;">
        💭 Thinking<span class="dots"></span>
    </div>
    <style>
    @keyframes blink { 0%{opacity:.2} 20%{opacity:1} 100%{opacity:.2} }
    .dots::after { content:'...'; animation: blink 1.5s infinite; }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------
    # FREE DEMO LIMIT (3 messages)
    # -----------------------
    if st.session_state.question_count >= 3:
        placeholder.empty()
        st.session_state.messages.append({
            "role": "assistant",
            "content": "✨ Your demo limit has ended.\n\nYou used your 3 free messages 😊\n\nIf you'd like full access to AssyaBot AI:\n👉 Send me a message on LinkedIn 💼💗"
        })
    else:
        st.session_state.question_count += 1  # count usage

        # Get AI response
        answer = ask_openai(user_input)

        placeholder.empty()
        st.session_state.messages.append({"role": "assistant", "content": answer})





# -----------------------
# Display chat history
# -----------------------
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"<div class='user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot'>{msg['content']}</div>", unsafe_allow_html=True)

