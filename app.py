import html as html_lib
import os

import requests
import streamlit as st

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

GITHUB_URL = "https://github.com/gituserc1140/MicroMystery-Generator"
SPONSOR_URL = "https://github.com/sponsors/gituserc1140"

_CSS = """
<style>
/* ── Page background ───────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hero banner ───────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f9a8d4, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Compliment card ───────────────────────────────────────────── */
.compliment-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(249,168,212,0.35);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    color: #e2e8f0;
    font-size: 1.15rem;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
    margin-top: 1.2rem;
    text-align: center;
}
.compliment-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f9a8d4;
    margin-bottom: 0.4rem;
    text-align: center;
}

/* ── Error card ────────────────────────────────────────────────── */
.error-card {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.45);
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    color: #fca5a5;
    font-size: 0.97rem;
    margin-top: 1rem;
}

/* ── Buttons ───────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #be185d, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* ── Sidebar ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.85);
    border-right: 1px solid rgba(249,168,212,0.2);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h2 {
    color: #f9a8d4 !important;
    font-size: 1.1rem;
}

/* ── Inputs ────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(249,168,212,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Spinner text ──────────────────────────────────────────────── */
[data-testid="stSpinner"] p { color: #f9a8d4 !important; }

/* ── Warning text ──────────────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }
</style>
"""


def get_configured_api_key():
    if "MISTRAL_API_KEY" in st.secrets:
        return st.secrets["MISTRAL_API_KEY"]
    return os.getenv("MISTRAL_API_KEY", "")


def generate_compliment(api_key: str, name: str, details: str) -> dict:
    personal_context = f" Here are some things about them: {details.strip()}." if details.strip() else ""
    prompt = (
        f"Write a single short, warm, and genuine personalised compliment for someone named {name}.{personal_context} "
        "Keep it under 40 words. Make it specific, uplifting, and heartfelt. Do not add any preamble or "
        "explanation — just the compliment itself."
    )
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "model": MISTRAL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 80,
        "temperature": 0.9,
    }
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"].strip()
            return {"text": text, "has_error": False}
        error_body = response.json() if response.content else {}
        message = error_body.get("message") or error_body.get("error", {}).get("message", response.text)
        return {"text": f"API error {response.status_code}: {message}", "has_error": True}
    except requests.exceptions.Timeout:
        return {"text": "Request timed out. Please try again.", "has_error": True}
    except Exception as exc:
        return {"text": f"Unexpected error: {exc}", "has_error": True}


def main():
    st.set_page_config(
        page_title="Compliment Generator",
        page_icon="✨",
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero header ────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero">
            <h1>✨ Compliment Generator</h1>
            <p>Generate a short, personalised compliment powered by Mistral AI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ────────────────────────────────────────────────────
    st.sidebar.header("Settings")
    api_key_input = st.sidebar.text_input(
        "Mistral API Key",
        type="password",
        help="Enter your Mistral API key. Get one at https://console.mistral.ai/",
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f'<a href="{GITHUB_URL}" target="_blank">'
        '<img src="https://img.shields.io/badge/View%20on-GitHub-181717?logo=github&style=flat-square" '
        'alt="View on GitHub"></a>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f'<a href="{SPONSOR_URL}" target="_blank">'
        '<img src="https://img.shields.io/badge/Sponsor%20me%20on-GitHub-EA4AAA?logo=githubsponsors&style=flat-square" '
        'alt="Sponsor me on GitHub"></a>',
        unsafe_allow_html=True,
    )

    stripped_key = api_key_input.strip()
    api_key = stripped_key if stripped_key else get_configured_api_key()

    if not api_key:
        st.warning("Please enter your Mistral API key in the sidebar to continue.")
        st.stop()

    # ── Main form ──────────────────────────────────────────────────
    name = st.text_input("Your name", placeholder="e.g. Alex")
    details = st.text_area(
        "Tell us a little about yourself (optional)",
        placeholder="e.g. I love hiking, I'm a software engineer, I just finished a big project…",
        height=100,
    )

    if st.button("✨ Generate Compliment"):
        if not name.strip():
            st.warning("Please enter your name so we can personalise your compliment.")
        else:
            with st.spinner("Crafting your compliment…"):
                result = generate_compliment(api_key, name.strip(), details)
            if result["has_error"]:
                st.markdown(
                    f'<div class="error-card">⚠️ {html_lib.escape(result["text"])}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<div class="compliment-label">💬 Your Compliment</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="compliment-card">✨ {html_lib.escape(result["text"])}</div>',
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    main()
