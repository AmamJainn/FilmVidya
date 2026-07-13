import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="FilmVidya",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Styling — "screening room" theme: charcoal background, marquee-gold accent,
# editorial serif title card, clapperboard-striped output header.
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #14131b;
        --bg-panel: #1b1a24;
        --bg-panel-raised: #211f2c;
        --gold: #d4a24c;
        --gold-soft: #e8c98a;
        --ivory: #f4f1ea;
        --muted: #9c98ab;
        --border: rgba(212, 162, 76, 0.18);
        --divider: rgba(244, 241, 234, 0.08);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse 900px 500px at 15% -10%, rgba(212,162,76,0.09), transparent),
            radial-gradient(ellipse 700px 400px at 100% 0%, rgba(212,162,76,0.05), transparent),
            var(--bg-primary);
        color: var(--ivory);
    }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}

    /* ---------------- Hero / Title card ---------------- */
    .fv-hero {
        padding: 2.2rem 2.5rem 2rem 2.5rem;
        border: 1px solid var(--border);
        border-radius: 4px;
        background: linear-gradient(180deg, var(--bg-panel-raised), var(--bg-panel));
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .fv-hero::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: repeating-linear-gradient(
            -35deg,
            #0e0d13, #0e0d13 14px,
            var(--gold) 14px, var(--gold) 28px
        );
        opacity: 0.85;
    }
    .fv-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: var(--gold-soft);
        margin: 0.9rem 0 0.6rem 0;
        font-weight: 600;
    }
    .fv-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4.2rem;
        letter-spacing: 0.04em;
        line-height: 1;
        margin: 0;
        color: var(--ivory);
        background: linear-gradient(180deg, #ffffff 0%, var(--gold-soft) 120%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .fv-subtitle {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-size: 1.08rem;
        color: var(--muted);
        margin-top: 0.6rem;
        max-width: 560px;
        line-height: 1.5;
    }

    /* ---------------- Sidebar ---------------- */
    section[data-testid="stSidebar"] {
        background: var(--bg-panel);
        border-right: 1px solid var(--divider);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    .fv-sidebar-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.6rem;
        letter-spacing: 0.06em;
        color: var(--gold-soft);
        margin-bottom: 0.2rem;
    }
    .fv-sidebar-caption {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: var(--muted);
        line-height: 1.6;
        margin-bottom: 1.4rem;
    }
    .fv-sidebar-step {
        display: flex;
        gap: 0.7rem;
        margin-bottom: 1rem;
        align-items: flex-start;
    }
    .fv-step-num {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        color: var(--gold);
        font-size: 0.95rem;
        border: 1px solid var(--border);
        border-radius: 50%;
        width: 24px; height: 24px;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .fv-step-text {
        font-size: 0.85rem;
        color: var(--muted);
        line-height: 1.5;
    }

    /* ---------------- Input area ---------------- */
    .fv-section-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--gold-soft);
        font-weight: 600;
        margin-bottom: 0.6rem;
    }

    .stTextArea textarea {
        background: var(--bg-panel-raised) !important;
        color: var(--ivory) !important;
        border: 1px solid var(--divider) !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold) !important;
    }
    .stTextArea textarea::placeholder {
        color: #5f5c6e !important;
    }

    div[data-testid="stForm"] {
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1.8rem;
        background: var(--bg-panel);
    }

    .stButton button, .stFormSubmitButton button {
        background: linear-gradient(180deg, var(--gold-soft), var(--gold)) !important;
        color: #1a1610 !important;
        border: none !important;
        border-radius: 3px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        font-size: 0.82rem !important;
        padding: 0.65rem 1.8rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        box-shadow: 0 2px 12px rgba(212,162,76,0.15) !important;
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 18px rgba(212,162,76,0.3) !important;
    }

    /* ---------------- Output "slate" card ---------------- */
    .fv-slate {
        border: 1px solid var(--border);
        border-radius: 4px;
        background: var(--bg-panel-raised);
        margin-top: 2rem;
        overflow: hidden;
    }
    .fv-slate-header {
        background: repeating-linear-gradient(
            -35deg,
            #0e0d13, #0e0d13 12px,
            #1c1a24 12px, #1c1a24 24px
        );
        border-bottom: 2px solid var(--gold);
        padding: 0.8rem 1.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .fv-slate-header-title {
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 0.08em;
        font-size: 1.15rem;
        color: var(--gold-soft);
    }
    .fv-slate-body {
        padding: 1.8rem 2rem;
    }

    .fv-movie-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2rem;
        color: var(--ivory);
        margin-bottom: 0.2rem;
    }
    .fv-movie-year {
        font-family: 'Inter', sans-serif;
        color: var(--gold-soft);
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }

    .fv-field-label {
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 600;
        margin-top: 1.1rem;
        margin-bottom: 0.35rem;
    }
    .fv-field-value {
        font-size: 0.98rem;
        color: var(--ivory);
        line-height: 1.6;
    }
    .fv-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .fv-chip {
        background: rgba(212,162,76,0.12);
        border: 1px solid var(--border);
        color: var(--gold-soft);
        padding: 0.3rem 0.85rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .fv-rating {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.3rem;
        color: var(--gold);
    }
    .fv-summary {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-size: 1.02rem;
        color: #d9d5e6;
        line-height: 1.75;
        border-left: 2px solid var(--gold);
        padding-left: 1.1rem;
        margin-top: 0.4rem;
    }

    .fv-divider {
        height: 1px;
        background: var(--divider);
        margin: 1.4rem 0;
    }

    /* Spinner text */
    .stSpinner > div {
        color: var(--gold-soft) !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
    }

    /* ---------------- Credit / footer ---------------- */
    .fv-credit {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: var(--muted);
    }
    .fv-credit-name {
        color: var(--ivory);
        font-weight: 600;
    }
    .fv-credit a {
        color: var(--gold-soft);
        text-decoration: none;
        border-bottom: 1px solid var(--border);
        transition: color 0.15s ease, border-color 0.15s ease;
    }
    .fv-credit a:hover {
        color: var(--gold);
        border-bottom-color: var(--gold);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="fv-sidebar-title">🎬 FilmVidya</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fv-sidebar-caption">'
        'Structured movie data, extracted from plain language. '
        'Paste a paragraph describing a film and FilmVidya returns it as '
        'clean, structured fields.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="fv-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fv-sidebar-step">'
        '<div class="fv-step-num">1</div>'
        '<div class="fv-step-text">Write or paste a paragraph about a movie.</div>'
        '</div>'
        '<div class="fv-sidebar-step">'
        '<div class="fv-step-num">2</div>'
        '<div class="fv-step-text">FilmVidya extracts title, year, genre, director, cast, rating, and a summary.</div>'
        '</div>'
        '<div class="fv-sidebar-step">'
        '<div class="fv-step-num">3</div>'
        '<div class="fv-step-text">Review the structured result on the slate.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="fv-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fv-sidebar-caption">Powered by Mistral Small, via LangChain.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="fv-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fv-credit">'
        'Built by <span class="fv-credit-name">Amam Jain</span><br/>'
        '<a href="https://www.linkedin.com/in/amam-jain-216082386" target="_blank">'
        'linkedin.com/in/amam-jain-216082386</a>'
        '</div>',
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="fv-hero">
        <div class="fv-eyebrow">Scene · Structure · Story</div>
        <div class="fv-title">FilmVidya</div>
        <div class="fv-subtitle">Turn a paragraph of movie talk into a clean, structured record —
        title, year, genre, director, cast, rating, and summary, extracted automatically.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Original backend logic (UNCHANGED)
# ----------------------------------------------------------------------------


class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
Extract movie information from the paragraph
     {format_instructions}
"""),
    ("human", "{paragraph}")
])

model = ChatMistralAI(model="mistral-small-2506")

# ----------------------------------------------------------------------------
# UI: input + trigger (replaces the original input() call)
# ----------------------------------------------------------------------------
st.markdown('<div class="fv-section-label">Paragraph</div>', unsafe_allow_html=True)

with st.form("filmvidya_form"):
    para = st.text_area(
        label="Paragraph input",
        label_visibility="collapsed",
        placeholder="Please give your paragraph : ",
        height=180,
    )
    submitted = st.form_submit_button("Extract movie data")

# ----------------------------------------------------------------------------
# Processing + output (same logic/flow as the original script)
# ----------------------------------------------------------------------------
if submitted:
    if not para or not para.strip():
        st.warning("Please give your paragraph.")
    else:
        with st.spinner("Extracting movie details..."):
            final_prompt = prompt.invoke(
                {
                    "paragraph": para,
                    "format_instructions": parser.get_format_instructions()
                }
            )

            response = model.invoke(final_prompt)
            movie_data = parser.parse(response.content)

        # ---- Render result on the "slate" ----
        st.markdown('<div class="fv-slate">', unsafe_allow_html=True)
        st.markdown(
            '<div class="fv-slate-header">'
            '<div class="fv-slate-header-title">Extraction Result</div>'
            '<div class="fv-slate-header-title">FilmVidya</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="fv-slate-body">', unsafe_allow_html=True)

        year_str = str(movie_data.release_year) if movie_data.release_year is not None else "Year unknown"
        st.markdown(f'<div class="fv-movie-title">{movie_data.title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fv-movie-year">{year_str}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="fv-field-label">Genre</div>', unsafe_allow_html=True)
            if movie_data.genre:
                chips = "".join(f'<span class="fv-chip">{g}</span>' for g in movie_data.genre)
                st.markdown(f'<div class="fv-chip-row">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fv-field-value">—</div>', unsafe_allow_html=True)

            st.markdown('<div class="fv-field-label">Director</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="fv-field-value">{movie_data.director if movie_data.director else "—"}</div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown('<div class="fv-field-label">Cast</div>', unsafe_allow_html=True)
            if movie_data.cast:
                chips = "".join(f'<span class="fv-chip">{c}</span>' for c in movie_data.cast)
                st.markdown(f'<div class="fv-chip-row">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fv-field-value">—</div>', unsafe_allow_html=True)

            st.markdown('<div class="fv-field-label">Rating</div>', unsafe_allow_html=True)
            if movie_data.rating is not None:
                st.markdown(f'<div class="fv-rating">★ {movie_data.rating}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fv-field-value">—</div>', unsafe_allow_html=True)

        st.markdown('<div class="fv-field-label">Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fv-summary">{movie_data.summary}</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)