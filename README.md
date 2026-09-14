# Problem Solving Coach — MVP v0.2

Prototype of an AI-assisted industrial IS / IS-NOT Problem Solving Coach.

## Main web app

Run locally (when network access to the API is available):

```bash
streamlit run streamlit_app.py
```

## Streamlit Community Cloud

Deploy `streamlit_app.py` from the GitHub repository and add this secret in the app settings:

```toml
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-5.6-sol"
```

`OPENAI_MODEL` is optional; the code defaults to `gpt-5.6-sol`.

## Important

Do not commit API keys, `.env`, `.streamlit/secrets.toml`, or confidential plant data to the repository.
For prototyping, use synthetic or appropriately anonymized cases unless external processing of real data is authorized.
