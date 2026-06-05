# 🎈 Learn Streamlit — From Scratch

A complete, hands-on Streamlit curriculum for Python intermediates.
Each lesson is a **runnable `.py` file** — just `streamlit run <file>` and explore.

---

## 🚀 Quick Start

```bash
pip install streamlit pandas numpy matplotlib plotly
streamlit run lessons/01_text_elements.py
```

---

## 📚 Curriculum

| # | File | What You'll Learn |
|---|------|-------------------|
| 01 | `lessons/01_text_elements.py` | `st.write`, `st.title`, markdown, code blocks, magic |
| 02 | `lessons/02_widgets.py` | Buttons, sliders, inputs, selectbox, checkbox, date picker |
| 03 | `lessons/03_layout.py` | Columns, sidebar, tabs, expanders, containers |
| 04 | `lessons/04_data_display.py` | DataFrames, tables, metrics, JSON, styling |
| 05 | `lessons/05_charts.py` | Built-in charts, Matplotlib, Plotly |
| 06 | `lessons/06_session_state.py` | Session state, callbacks, counter patterns |
| 07 | `lessons/07_forms_files.py` | Forms, file upload, download button |
| 08 | `lessons/08_caching.py` | `@st.cache_data`, `@st.cache_resource`, performance |
| 09 | `lessons/09_multipage/` | Multi-page app structure |
| 10 | `capstone/` | Full sales dashboard combining everything |

---

## 💡 How to Use This Course

1. **Read the comments** — every file is heavily commented explaining the *why*, not just the *what*.
2. **Run it first**, then tweak values and re-run to see what changes.
3. **Do the exercises** at the bottom of each file.
4. **Build the capstone** once you've finished all lessons.

---

## 🧠 Key Concepts at a Glance

| Concept | Short Answer |
|---------|-------------|
| How does Streamlit work? | It **reruns your entire script top-to-bottom** every time a user interacts |
| How do I persist state between reruns? | `st.session_state` |
| How do I avoid recomputing expensive data? | `@st.cache_data` decorator |
| How do I group inputs so they don't trigger reruns mid-form? | `st.form` |
| How do I make a multi-page app? | Put pages in a `pages/` folder or use `st.navigation` |

---

## 📦 Requirements

```
streamlit>=1.35
pandas
numpy
matplotlib
plotly
```
