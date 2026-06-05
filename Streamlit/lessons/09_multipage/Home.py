# ============================================================
# LESSON 09 — Multi-Page Apps
# Run: streamlit run lessons/09_multipage/Home.py
# ============================================================
#
# KEY CONCEPT: How Multi-Page Apps Work
# ----------------------------------------
# Streamlit supports multi-page apps natively via a "pages/" folder.
#
# Structure:
#   Home.py          ← your entry point (this file)
#   pages/
#       1_Dashboard.py
#       2_Analytics.py
#       3_Settings.py
#
# Rules:
# - Files in pages/ appear in the sidebar automatically
# - File names become page titles (underscores → spaces, leading
#   numbers are stripped and used for ordering)
# - Each page is a full independent Python script
# - st.session_state is SHARED across all pages
# - @st.cache_data / @st.cache_resource are SHARED across pages

import streamlit as st

st.set_page_config(
    page_title="My Multi-Page App",
    page_icon="🏠",
    layout="wide",
)

# Shared sidebar content
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=60)
    st.title("My App")
    st.caption("Lesson 09 — Multi-page demo")
    st.divider()
    # You can put shared controls here — they'll appear on every page
    st.session_state.setdefault("username", "Atabi")
    st.session_state.username = st.text_input("Username", value=st.session_state.username)

# Home page content
st.title("🏠 Home")
st.markdown(f"Welcome back, **{st.session_state.username}**! 👋")

st.info("""
### How this multi-page app is structured

```
lessons/09_multipage/
│
├── Home.py              ← you are here
└── pages/
    ├── 1_Dashboard.py   ← Page 1
    ├── 2_Analytics.py   ← Page 2
    └── 3_Settings.py    ← Page 3
```

Navigate using the **sidebar** on the left.
""")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pages", "4 (incl. Home)")
col2.metric("Shared State", "session_state ✓")
col3.metric("Shared Cache", "cache_data ✓")

st.markdown("""
### Key things to notice

- The **sidebar** automatically lists all pages from the `pages/` folder
- **Session state** set on Home (your username) is visible on other pages
- Each page is a **separate .py file** — clean separation of concerns
- You can put shared UI elements (logo, username) in the sidebar on every page
  by importing a shared `sidebar.py` module
""")
