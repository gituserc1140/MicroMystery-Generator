# Micro-Mystery Generator

A Streamlit app that generates tiny, eerie mysteries using the [Mistral AI](https://mistral.ai/) API. Each mystery contains a strange detail, a hidden clue, and a reveal — all under 40 words.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://micromystery-generator.streamlit.app/)
[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?logo=github&style=flat-square)](https://github.com/gituserc1140/MicroMystery-Generator)
[![Sponsor me on GitHub](https://img.shields.io/badge/Sponsor%20me%20on-GitHub-EA4AAA?logo=githubsponsors&style=flat-square)](https://github.com/sponsors/gituserc1140)

## About

Click **Unveil a Mystery** and the app uses the Mistral AI language model to craft a tiny, atmospheric mystery. Each mystery is under 40 words and generated fresh every time. Reveal hints progressively, then uncover the full solution when you're ready.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/gituserc1140/MicroMystery-Generator.git
cd MicroMystery-Generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Mistral API key

You can provide your key in any of these ways:

**Option A — Enter it in the sidebar at runtime** *(easiest)*

**Option B — Streamlit secrets file:**

```bash
mkdir -p .streamlit
echo 'MISTRAL_API_KEY = "your_key_here"' > .streamlit/secrets.toml
```

**Option C — Environment variable:**

```bash
export MISTRAL_API_KEY="your_key_here"
```

Get a free Mistral API key at [console.mistral.ai](https://console.mistral.ai/).

### 4. Run the app

```bash
streamlit run app.py
```

## Usage

1. Open the app in your browser (default: `http://localhost:8501`).
2. Enter your **Mistral API key** in the sidebar.
3. Click **Unveil a Mystery** to generate a new micro-mystery.
4. Click **Reveal Hint 1** for a subtle nudge.
5. Click **Reveal Hint 2** for a more direct clue.
6. Click **Reveal Answer** to see the full solution and explanation.
7. Click **Unveil a Mystery** again to start fresh with a new mystery.

## Tech stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Mistral AI](https://mistral.ai/) — language model API (`mistral-small-latest`)
- [Requests](https://requests.readthedocs.io/) — HTTP client
