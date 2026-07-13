# FilmVidya 🎬

Turn a paragraph of movie talk into a clean, structured record — title, release
year, genre, director, cast, rating, and summary — extracted automatically
using Mistral (via LangChain) and displayed in a polished Streamlit interface.

Built by **Amam Jain** · [linkedin.com/in/amam-jain-216082386](https://www.linkedin.com/in/amam-jain-216082386)

---

## How it works

1. Paste a paragraph describing a movie into the text box.
2. FilmVidya sends it to a Mistral model with a structured-output prompt.
3. The response is parsed into a `Movie` object (title, release_year, genre,
   director, cast, rating, summary) and rendered on the result panel.

## Project structure

```
filmvidya/
├── env/                  # Local virtual environment (not committed)
├── .env                  # Your API key (not committed)
├── core.py                # Original CLI script — same extraction logic, run from the terminal
├── UI.py                  # Streamlit app — the same extraction logic, wrapped in a UI
├── requirements.txt       # Python dependencies
└── README.md
```

- **`core.py`** is the original command-line version: it prompts for a
  paragraph with `input()`, calls the model, and prints the parsed `Movie`
  object to the terminal.
- **`UI.py`** is the Streamlit version of the exact same pipeline (model,
  prompt, parser, `Movie` schema) — instead of `input()`/`print()`, it takes
  the paragraph from a text box and renders the result on a styled panel.

Both files work independently; you don't need to run `core.py` to use `UI.py`.

## Run locally

1. Clone the repo and move into it:
   ```bash
   git clone <your-repo-url>
   cd filmvidya
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate      # Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Mistral API key:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run UI.py
   ```

   Or run the original CLI script directly:
   ```bash
   python core.py
   ```

## Deploy on Streamlit Community Cloud (free)

1. Push this project to a **public** GitHub repository.
   Make sure `.env` and `env/` are **not** committed — add them to
   `.gitignore` first:
   ```
   env/
   .env
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub.

3. Click **New app**, then select:
   - Repository: your FilmVidya repo
   - Branch: `main` (or whichever you use)
   - Main file path: `UI.py`

4. Before deploying, open **Advanced settings → Secrets** and add:
   ```
   MISTRAL_API_KEY = "your_mistral_api_key_here"
   ```

5. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and
   launch the app. You'll get a shareable URL like:
   ```
   https://<your-app-name>.streamlit.app
   ```

### Notes on the free tier
- The repo must be public for the free tier.
- Idle apps may go to sleep and wake up on the next visit — normal for the
  free tier, no action needed.
- To update the live app, just push new commits to GitHub; Streamlit Cloud
  redeploys automatically.
