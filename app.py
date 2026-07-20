import streamlit as st
import requests

# Mistral API endpoint and parameters
MISTRAL_API_URL = "https://api.mistral.ai/v1/generate"
API_KEY = st.secrets["MISTRAL_API_KEY"]  # Store API key in Streamlit secrets

def generate_mystery():
    prompt = (
        "Create a micro-mystery in under 40 words. Include: "
        "a strange or impossible detail, one subtle clue hinting at the solution, "
        "an atmospheric tone, and no explanation or resolution. "
        "Make it clever, unsettling, and self-contained."
    )
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return "Failed to generate mystery."

st.title("Micro-Mystery Generator")
st.write("Click below to generate a tiny, eerie mystery.")

if st.button("Generate Mystery"):
    with st.spinner("Crafting your mystery..."):
        mystery = generate_mystery()
    st.success(mystery)