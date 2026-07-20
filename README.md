# Micro-Mystery Generator

A Streamlit app that generates eerie, self-contained micro-mysteries using the Mistral API. Each mystery is under 40 words, featuring a strange detail, a subtle clue, and an atmospheric tone.

## Setup
1. Install dependencies:
   ```bash
pip install -r requirements.txt
```
2. Add your Mistral API key to Streamlit secrets:
   ```bash
echo 'MISTRAL_API_KEY="your_api_key_here"' > .streamlit/secrets.toml
```
3. Run the app:
   ```bash
streamlit run app.py
```

## Usage
Click the "Generate Mystery" button to create a new micro-mystery. Each mystery is designed to be clever, unsettling, and solvable without explanation.