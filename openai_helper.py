import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

# Use Streamlit secret if available, otherwise fallback to local .env
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # keep the model you want
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content

