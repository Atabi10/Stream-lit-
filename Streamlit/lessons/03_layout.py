# ============================================================
# LESSON 03 — Layout: Columns, Sidebar, Tabs, Expanders
# Run: streamlit run lessons/03_layout.py
# ============================================================
#
# KEY CONCEPT: Layout as Context Managers
# -----------------------------------------
# Most layout elements are used as context managers (with blocks)
# OR by calling methods directly on the returned object:
#
#   col1, col2 = st.columns(2)
#   col1.write("Left")         # method style
#
#   with col2:
#       st.write("Right")      # context manager style
#
# Both are equivalent. Choose what feels more readable.

import streamlit as st
import random

st.set_page_config(page_title="Lesson 03 · Layout", page_icon="🏗️", layout="wide")
st.title("🏗️ Lesson 03: Layout")

# ── 1. Columns ───────────────────────────────────────────────
st.header("1. Columns")
st.markdown("Divide the page into side-by-side sections.")

# Equal-width columns
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$42,000", "+8%")
col2.metric("Users", "1,240", "+12%")
col3.metric("Churn", "3.2%", "-0.5%", delta_color="inverse")

st.divider()

# Custom-width columns (ratios)
st.subheader("Custom-width columns [3, 1]")
main_col, side_col = st.columns([3, 1])

with main_col:
    st.info("This is the wide main column (ratio 3).")
    st.write("Put your primary content here.")

with side_col:
    st.warning("Side column (ratio 1)")
    st.write("Sidebar-like narrow column.")

st.divider()

# gap parameter
st.subheader("Columns with gap='large'")
a, b = st.columns(2, gap="large")
a.write("Left — wide gap separates us from right.")
b.write("Right — wide gap separates us from left.")

# Nested columns
st.subheader("Nested columns")
outer_left, outer_right = st.columns(2)
with outer_left:
    inner_l, inner_r = st.columns(2)
    inner_l.button("Nested L")
    inner_r.button("Nested R")
with outer_right:
    st.write("Regular right column")

# ── 2. Sidebar ───────────────────────────────────────────────
st.header("2. Sidebar")
st.markdown("Put filters and controls in `st.sidebar` so the main area stays clean.")

# Add widgets to the sidebar
with st.sidebar:
    st.title("⚙️ Controls")
    st.divider()
    theme = st.selectbox("Theme", ["Light", "Dark", "Ocean"])
    num_items = st.slider("Number of items", 1, 20, 5)
    show_details = st.checkbox("Show details", value=True)
    st.divider()
    st.caption("Sidebar widgets work exactly like normal widgets.")

st.info(f"Sidebar selected → Theme: **{theme}** | Items: **{num_items}** | Details: **{show_details}**")

# ── 3. Tabs ───────────────────────────────────────────────────
st.header("3. Tabs")
st.markdown("Organize related content into tabs — only one is visible at a time.")

tab_overview, tab_data, tab_settings = st.tabs(["📊 Overview", "📋 Data", "⚙️ Settings"])

with tab_overview:
    st.subheader("Overview Tab")
    st.write("This is the overview content.")
    c1, c2 = st.columns(2)
    c1.metric("Total Sales", "$128,000")
    c2.metric("Active Users", "3,400")

with tab_data:
    st.subheader("Data Tab")
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.randn(5, 3), columns=["Alpha", "Beta", "Gamma"])
    st.dataframe(df)

with tab_settings:
    st.subheader("Settings Tab")
    st.text_input("API Key", type="password", placeholder="sk-...")
    st.toggle("Enable notifications")
    st.button("Save settings")

# ── 4. Expander ───────────────────────────────────────────────
st.header("4. Expander (Accordion)")
st.markdown("Collapse sections to keep the page tidy. Great for advanced options or long content.")

with st.expander("📖 Show explanation", expanded=False):
    st.write("""
    Expanders are collapsed by default (`expanded=False`).
    Set `expanded=True` to open them automatically on page load.

    Use them for:
    - Advanced settings / filters
    - Long text sections
    - Optional details the user may not always need
    """)

with st.expander("🔧 Advanced Configuration", expanded=False):
    timeout = st.number_input("Timeout (seconds)", value=30)
    retry = st.number_input("Max retries", value=3)
    st.button("Apply settings")

# ── 5. Container ─────────────────────────────────────────────
st.header("5. Container")
st.markdown("`st.container()` groups elements and lets you write to them out of order.")

# Containers let you "pre-declare" a spot and fill it later
placeholder_box = st.container(border=True)

st.write("This text appears AFTER the container in the code...")
st.write("...but the container above gets filled next:")

with placeholder_box:
    st.subheader("I was filled after the text below was written!")
    st.write("Containers are useful when you need to build UI top-down "
             "but compute content in a different order.")

# ── 6. Empty (Dynamic Placeholder) ────────────────────────────
st.header("6. st.empty — Dynamic Single-slot Placeholder")
st.markdown("`st.empty()` creates a single slot that can be **replaced** with new content.")

import time

slot = st.empty()
slot.info("⏳ Click the button below to start a countdown.")

if st.button("Start 3-second countdown"):
    for i in range(3, 0, -1):
        slot.warning(f"⏱️ {i}...")
        time.sleep(1)
    slot.success("🎉 Done!")

# ── 7. st.popover ─────────────────────────────────────────────
st.header("7. Popover")
st.markdown("A floating panel that appears on click — good for inline detail or mini forms.")

with st.popover("ℹ️ What's this?"):
    st.markdown("**Popover explanation**")
    st.write("This is a floating panel. You can put any widgets here.")
    st.button("OK, got it")

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Create a 3-column layout showing name, age, and city using `st.text_input` in each column.
2. Add a sidebar with a `st.date_input` and display the selected date in the main area.
3. Build a tabbed interface with 3 tabs: "Profile", "Posts", "Settings" — put at least one widget in each.
4. Use `st.expander` to hide a long markdown block (paste any text).
5. Use `st.empty` + `st.button` to toggle between two messages.
""")
