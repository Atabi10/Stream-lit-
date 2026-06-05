# ============================================================
# CAPSTONE — Sales Intelligence Dashboard
# Run: streamlit run capstone/Home.py
#
# This app combines EVERYTHING from Lessons 1–9:
#   ✓ Text elements & page config       (L01)
#   ✓ Widgets with reactive output       (L02)
#   ✓ Columns, sidebar, tabs             (L03)
#   ✓ DataFrames, metrics, column config (L04)
#   ✓ Plotly charts                      (L05)
#   ✓ Session state                      (L06)
#   ✓ File upload & download             (L07)
#   ✓ Caching                            (L08)
#   ✓ Multi-page structure               (L09)
# ============================================================

import streamlit as st


st.set_page_config(
    page_title="Sales Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared sidebar ────────────────────────────────────────────
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=48)
    st.markdown("## 📈 Sales Intelligence")
    st.divider()
    st.caption("Capstone App · All 9 lessons combined")
    st.divider()

    # Global date filter (L06 - session state)
    import datetime
    st.subheader("📅 Date Range")
    default_start = datetime.date(2024, 1, 1)
    default_end   = datetime.date(2024, 12, 31)

    st.session_state.setdefault("date_start", default_start)
    st.session_state.setdefault("date_end",   default_end)

    st.session_state.date_start = st.date_input("From", value=st.session_state.date_start)
    st.session_state.date_end   = st.date_input("To",   value=st.session_state.date_end)

    st.divider()
    st.caption("Navigate pages using the menu above.")

# ── Home content ──────────────────────────────────────────────
st.title("📈 Sales Intelligence Dashboard")
st.markdown("A complete multi-page Streamlit app — your **Lesson 9 capstone**.")

col1, col2, col3 = st.columns(3)
col1.info("**📊 Dashboard**\nKPIs, revenue trends, regional breakdown")
col2.info("**🔍 Explorer**\nUpload your own data, filter, export")
col3.info("**🏆 Leaderboard**\nTop reps, product rankings, quota tracking")

st.divider()
st.markdown("""
### What's inside this app

| Page | Concepts Demonstrated |
|------|-----------------------|
| **Dashboard** | `@st.cache_data`, `st.metric`, Plotly charts, sidebar filters |
| **Explorer** | `st.file_uploader`, `st.data_editor`, `st.download_button`, `st.form` |
| **Leaderboard** | `st.dataframe` + `column_config`, session state, tabs |

### How to use
1. Click **Dashboard** in the sidebar to see KPIs and charts
2. Click **Explorer** to upload a CSV and explore it interactively
3. Click **Leaderboard** for rep rankings

> **Tip**: The date range filter in the sidebar is shared across all pages via `st.session_state`.
""")
