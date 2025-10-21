import streamlit as st
from openai_helper import ask_openai  # your function
import base64

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
st.markdown("<h1>AssyaBot AI 🤖🧠</h1>", unsafe_allow_html=True)

# -----------------------
# Initialize messages
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Chat input area (clean version)
# -----------------------
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])  # Input (wide) + Send button (small)
    with col1:
        user_input = st.text_input("Ask me anything...", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("➤")

    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = ask_openai(user_input)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot'>{msg['content']}</div>", unsafe_allow_html=True)
