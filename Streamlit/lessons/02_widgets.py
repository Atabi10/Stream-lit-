# ============================================================
# LESSON 02 — Widgets (Input & Control Elements)
# Run: streamlit run lessons/02_widgets.py
# ============================================================
#
# KEY CONCEPT: Widgets Return Values
# ------------------------------------
# Every widget RETURNS its current value. You capture that
# value in a variable and use it immediately below.
#
#   name = st.text_input("Your name")
#   st.write(f"Hello, {name}!")
#
# When the user types, Streamlit reruns the script and `name`
# gets the new value automatically.

import streamlit as st
import datetime

st.set_page_config(page_title="Lesson 02 · Widgets", page_icon="🎛️")
st.title("🎛️ Lesson 02: Widgets")

# ── 1. Button ────────────────────────────────────────────────
st.header("1. Button")
st.markdown("`st.button` returns `True` only on the rerun triggered by the click — "
            "then goes back to `False`.")

if st.button("Click me!"):
    st.success("Button was clicked! 🎉")
else:
    st.info("Button not clicked yet.")

# Buttons with types
col1, col2, col3 = st.columns(3)
col1.button("Primary", type="primary")
col2.button("Secondary", type="secondary")
col3.button("Danger", type="primary", disabled=True)

# ── 2. Checkbox ──────────────────────────────────────────────
st.header("2. Checkbox")

show_secret = st.checkbox("Show secret message", value=False)
if show_secret:
    st.balloons()
    st.success("🎈 You found the secret!")

# ── 3. Radio ─────────────────────────────────────────────────
st.header("3. Radio")

language = st.radio(
    "Favorite language?",
    options=["Python", "JavaScript", "Go", "Rust"],
    index=0,                  # default selected index
    horizontal=True,          # display horizontally
)
st.write(f"You chose: **{language}**")

# ── 4. Selectbox ─────────────────────────────────────────────
st.header("4. Selectbox (Dropdown)")

city = st.selectbox(
    "Select your city",
    options=["Tehran", "London", "New York", "Tokyo", "Sydney"],
    index=0,
)
st.write(f"Selected city: **{city}**")

# Selectbox with format_func (display different label vs stored value)
MODELS = {"gpt-4o": "GPT-4o (OpenAI)", "claude-3": "Claude 3 (Anthropic)", "gemini": "Gemini (Google)"}
model_key = st.selectbox("Choose an AI model", options=list(MODELS.keys()),
                          format_func=lambda k: MODELS[k])
st.write(f"Selected key: `{model_key}`")

# ── 5. Multiselect ───────────────────────────────────────────
st.header("5. Multiselect")

skills = st.multiselect(
    "Pick your skills",
    options=["Python", "SQL", "Tableau", "Power BI", "Excel", "R", "Spark"],
    default=["Python", "SQL"],
)
st.write(f"Selected {len(skills)} skill(s): {skills}")

# ── 6. Slider ────────────────────────────────────────────────
st.header("6. Slider")

age = st.slider("Your age", min_value=1, max_value=100, value=25, step=1)
st.write(f"Age: {age}")

# Range slider (returns a tuple)
price_range = st.slider("Price range ($)", min_value=0, max_value=1000,
                         value=(100, 500), step=50)
st.write(f"From ${price_range[0]} to ${price_range[1]}")

# Float slider
confidence = st.slider("Confidence threshold", 0.0, 1.0, 0.75, 0.05)
st.write(f"Threshold: {confidence:.2f}")

# ── 7. Number Input ───────────────────────────────────────────
st.header("7. Number Input")

quantity = st.number_input("Quantity", min_value=0, max_value=100, value=10, step=1)
price = st.number_input("Unit price ($)", min_value=0.0, value=9.99, step=0.01, format="%.2f")
st.write(f"Total: **${quantity * price:,.2f}**")

# ── 8. Text Input ────────────────────────────────────────────
st.header("8. Text Input")

name = st.text_input("Your name", placeholder="e.g. Atabi", max_chars=50)
if name:
    st.write(f"Hello, **{name}**! 👋")

# Password input (masks the text)
password = st.text_input("Password", type="password")
if password:
    st.write(f"Password length: {len(password)} characters")

# ── 9. Text Area ─────────────────────────────────────────────
st.header("9. Text Area")

bio = st.text_area("Write a short bio", height=120,
                    placeholder="Tell us about yourself...")
if bio:
    word_count = len(bio.split())
    st.caption(f"{word_count} word(s), {len(bio)} character(s)")

# ── 10. Date & Time ──────────────────────────────────────────
st.header("10. Date & Time Inputs")

dob = st.date_input("Date of birth",
                     value=datetime.date(1990, 1, 1),
                     min_value=datetime.date(1900, 1, 1),
                     max_value=datetime.date.today())

today = datetime.date.today()
age_days = (today - dob).days
st.write(f"That's **{age_days:,} days** ago ({age_days // 365} years).")

meeting_time = st.time_input("Schedule a meeting", value=datetime.time(9, 0))
st.write(f"Meeting at: {meeting_time.strftime('%I:%M %p')}")

# ── 11. Color Picker ─────────────────────────────────────────
st.header("11. Color Picker")

color = st.color_picker("Pick a brand color", value="#4A90D9")
st.markdown(f"<div style='background:{color}; padding:20px; border-radius:8px; "
            f"color:white; text-align:center'>Your color: {color}</div>",
            unsafe_allow_html=True)

# ── 12. Toggle ───────────────────────────────────────────────
st.header("12. Toggle")

dark_mode = st.toggle("Dark mode")
if dark_mode:
    st.info("Dark mode is ON (styling would change in a real app)")

# ── Putting It Together — Live Preview ───────────────────────
st.divider()
st.header("🔗 Live Preview — All Inputs Together")

with st.expander("See a live form using multiple widgets"):
    col1, col2 = st.columns(2)
    first = col1.text_input("First name")
    last = col2.text_input("Last name")
    score = st.slider("Score", 0, 100, 75)
    category = st.selectbox("Category", ["A", "B", "C"])

    if first or last:
        st.success(f"**{first} {last}** — Score: {score} | Category: {category}")

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Create a BMI calculator: two `st.number_input` fields (weight kg, height cm), compute and display BMI.
2. Build a "temperature converter" with a slider (°C) that shows the equivalent in °F.
3. Make a multiselect for toppings and display "Your pizza has X toppings: …"
4. Use `st.date_input` to collect a start/end date range and show the number of days between them.
""")
