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
# Header
# -----------------------
st.markdown("<h1>AssyaBot AI 🤖</h1>", unsafe_allow_html=True)

# -----------------------
# Initialize messages
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Chat input (Enter to send, auto-clear, no button)
# -----------------------

# one-time state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "submitted_text" not in st.session_state:
    st.session_state.submitted_text = ""

st.markdown("""
<style>
.label-small { color:white; font-size:14px; margin-bottom:-6px; }
.input-field { width:100%; max-width:900px; height:48px; padding:10px 14px;
  border-radius:10px; border:1px solid #ccc; background:rgba(255,255,255,0.9);
  font-size:16px; color:black; margin:auto; }
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='label-small'>Ask me anything...</p>", unsafe_allow_html=True)

# --- 1) callback that fires on Enter ---
def _submit():
    # copy the text for processing, then clear the input safely
    st.session_state.submitted_text = st.session_state.user_input
    st.session_state.user_input = ""   # safe here (inside on_change)
    # optional: rerun right away so the cleared UI shows instantly
    # st.rerun()

# --- 2) the input widget ---
st.text_input(
    "",
    key="user_input",
    label_visibility="collapsed",
    on_change=_submit
)

# --- 3) if something was submitted, process it ---
if st.session_state.submitted_text:
    user_input = st.session_state.submitted_text
    st.session_state.submitted_text = ""   # consume it

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Thinking animation (white & minimal)
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

    # Call your model
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

