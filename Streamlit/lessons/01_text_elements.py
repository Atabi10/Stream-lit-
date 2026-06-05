# ============================================================
# LESSON 01 — Text Elements & The Streamlit Execution Model
# Run: streamlit run lessons/01_text_elements.py
# ============================================================
#
# KEY CONCEPT: How Streamlit Works
# ---------------------------------
# Every time a user interacts with the app (clicks a button,
# moves a slider), Streamlit RERUNS YOUR ENTIRE SCRIPT from
# top to bottom. Think of it like refreshing a web page, but
# Python re-executes everything.
#
# This is why:
#   - You write Python top-to-bottom like a script
#   - There are no callbacks needed for most things
#   - State management (covered in Lesson 6) is important

import streamlit as st

# ── Page Config ──────────────────────────────────────────────
# Always set this FIRST — it configures browser tab title,
# icon, and layout. Must be the very first Streamlit command.
st.set_page_config(
    page_title="Lesson 01 · Text Elements",
    page_icon="📝",
    layout="centered",   # or "wide"
)

# ── 1. st.title ───────────────────────────────────────────────
# Large H1 heading — use once per page, at the top.
st.title("📝 Lesson 01: Text Elements")

# ── 2. st.header / st.subheader ──────────────────────────────
st.header("Section Headers")
st.subheader("This is a subheader (H3)")

# ── 3. st.write ───────────────────────────────────────────────
# st.write() is Streamlit's Swiss Army knife.
# It intelligently renders strings, dataframes, dicts, charts,
# Markdown, numbers — almost anything you throw at it.
st.header("st.write — The Swiss Army Knife")

st.write("Plain text string")
st.write("You can use **bold**, _italic_, and `inline code` with Markdown")
st.write(42)                         # numbers
st.write({"name": "Atabi", "role": "learner"})   # dicts render as tables
st.write([1, 2, 3, 4, 5])           # lists

# ── 4. st.markdown ────────────────────────────────────────────
# When you want explicit Markdown control (e.g., unsafe HTML).
st.header("st.markdown")

st.markdown("## An H2 inside markdown")
st.markdown("""
- Item one
- Item two
- Item three

> Blockquotes work too!
""")

# unsafe_allow_html lets you embed raw HTML (use carefully)
st.markdown("<span style='color:royalblue; font-size:20px'>Colored text via HTML</span>",
            unsafe_allow_html=True)

# ── 5. st.text & st.code ─────────────────────────────────────
st.header("Preformatted Text & Code")

# st.text — monospace, no markdown, good for raw output
st.text("Fixed-width output:\nLine 1\nLine 2\nLine 3")

# st.code — syntax-highlighted code block
st.code("""
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Atabi"))
""", language="python")

st.code("<h1>HTML example</h1>", language="html")
st.code('SELECT * FROM users WHERE active = TRUE', language="sql")

# ── 6. st.caption & st.divider ────────────────────────────────
st.header("Caption & Divider")
st.write("Main content here.")
st.caption("Small grey caption text — useful for source notes or hints.")
st.divider()   # horizontal rule

# ── 7. Magic Commands ─────────────────────────────────────────
# Any expression or string literal at the top level of your
# script is auto-rendered — called "magic". This is a shortcut.
st.header("Magic Commands (implicit st.write)")

"This string is rendered **automatically** without calling st.write!"

x = 2 + 2
x   # This renders the value 4 automatically

# ── 8. st.latex ───────────────────────────────────────────────
st.header("LaTeX (Math)")
st.latex(r"E = mc^2")
st.latex(r"\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2}")

# ── 9. Alerts ────────────────────────────────────────────────
st.header("Alerts & Messages")
st.success("✅ Operation completed successfully!")
st.info("ℹ️ Here's something useful to know.")
st.warning("⚠️ Careful — this might cause issues.")
st.error("❌ Something went wrong.")

# st.exception renders a full Python traceback nicely
# st.exception(ValueError("Example exception display"))

# ── 10. st.status (progress updates) ─────────────────────────
st.header("Status Box (for long operations)")

with st.status("Running a multi-step process...", expanded=True) as status:
    st.write("Step 1: Loading data...")
    st.write("Step 2: Processing...")
    st.write("Step 3: Done!")
    status.update(label="Process complete!", state="complete", expanded=False)

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Add a `st.title` with your own name.
2. Use `st.markdown` to create a bulleted list of your 3 favorite Python libraries.
3. Display a Python dictionary of your choice using `st.write`.
4. Try `st.code` with a SQL snippet.
5. Add a `st.warning` telling the user "This is a demo app."
""")
