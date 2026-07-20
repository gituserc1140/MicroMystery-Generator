# ✨ Compliment Generator

A Streamlit app that instantly generates a short, personalised compliment using the [Mistral AI](https://mistral.ai/) API. Enter your name and optionally a little about yourself, and receive a unique, heartfelt compliment in seconds.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://micromystery-generator.streamlit.app/)
[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?logo=github&style=flat-square)](https://github.com/gituserc1140/MicroMystery-Generator)
[![Sponsor me on GitHub](https://img.shields.io/badge/Sponsor%20me%20on-GitHub-EA4AAA?logo=githubsponsors&style=flat-square)](https://github.com/sponsors/gituserc1140)

## About

Enter your name (and optionally a few sentences about yourself) and the app uses the Mistral AI language model to craft a personalised, uplifting compliment just for you. Each compliment is under 40 words and generated fresh every time you click the button.

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
3. Type your **name** in the main input field.
4. Optionally add a sentence or two **about yourself** (interests, achievements, mood).
5. Click **✨ Generate Compliment** and enjoy your personalised message.
6. Click the button again to generate a fresh compliment.

## Tech stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Mistral AI](https://mistral.ai/) — language model API (`mistral-small-latest`)
- [Requests](https://requests.readthedocs.io/) — HTTP client
