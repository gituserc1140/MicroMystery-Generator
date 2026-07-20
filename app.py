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
    background: linear-gradient(160deg, #04020a, #0d0520, #060d18);
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
    background: linear-gradient(90deg, #7c3aed, #0e7490);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Mystery card ──────────────────────────────────────────────── */
.mystery-card {
    background: rgba(12,5,30,0.7);
    border: 1px solid rgba(109,40,217,0.45);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    color: #c4b5fd;
    font-size: 1.15rem;
    line-height: 1.9;
    white-space: pre-wrap;
    word-break: break-word;
    margin-top: 1.2rem;
    text-align: center;
    font-style: italic;
    letter-spacing: 0.01em;
}
.mystery-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6d28d9;
    margin-bottom: 0.4rem;
    text-align: center;
}

/* ── Error card ────────────────────────────────────────────────── */
.error-card {
    background: rgba(127,29,29,0.2);
    border: 1px solid rgba(185,28,28,0.5);
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    color: #fca5a5;
    font-size: 0.97rem;
    margin-top: 1rem;
}

/* ── Buttons ───────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #4c1d95, #0e7490) !important;
    color: #e2e8f0 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: opacity 0.2s !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stButton"] button:hover { opacity: 0.8 !important; }

/* ── Sidebar ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(4,2,10,0.92);
    border-right: 1px solid rgba(109,40,217,0.25);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #94a3b8 !important; }
[data-testid="stSidebar"] h2 {
    color: #7c3aed !important;
    font-size: 1.1rem;
}

/* ── Inputs ────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(12,5,30,0.6) !important;
    border: 1px solid rgba(109,40,217,0.4) !important;
    border-radius: 8px !important;
    color: #c4b5fd !important;
}

/* ── Spinner text ──────────────────────────────────────────────── */
[data-testid="stSpinner"] p { color: #7c3aed !important; }

/* ── Warning / alert text ──────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }
</style>
"""

_SYSTEM_PROMPT = (
    "You are a Micro-Mystery Generator. "
    "Your job is to create tiny, eerie mysteries that can be solved in under 40 words. "
    "Each mystery must contain: "
    "a strange or impossible detail; "
    "one subtle clue that hints at the solution; "
    "an atmospheric tone; "
    "no explanation, no answer, no resolution. "
    "The mystery should feel clever, unsettling, and self-contained. "
    "Output only the mystery text. "
    "No preamble, no formatting, no commentary."
)


def get_configured_api_key():
    if "MISTRAL_API_KEY" in st.secrets:
        return st.secrets["MISTRAL_API_KEY"]
    return os.getenv("MISTRAL_API_KEY", "")


def generate_mystery(api_key: str) -> dict:
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": "Generate a new micro-mystery."},
        ],
        "max_tokens": 120,
        "temperature": 1.0,
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
        page_title="Micro-Mystery Generator",
        page_icon="?",
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero header ────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero">
            <h1>Micro-Mystery Generator</h1>
            <p>Generate a tiny, eerie mystery powered by Mistral AI.</p>
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

    # ── Generate button ────────────────────────────────────────────
    if st.button("Unveil a Mystery"):
        with st.spinner("Summoning the unknown..."):
            result = generate_mystery(api_key)
        if result["has_error"]:
            st.markdown(
                f'<div class="error-card">{html_lib.escape(result["text"])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="mystery-label">The Mystery</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="mystery-card">{html_lib.escape(result["text"])}</div>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
