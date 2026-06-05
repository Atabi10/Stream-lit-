# ============================================================
# LESSON 06 — Session State & Reactivity
# Run: streamlit run lessons/06_session_state.py
# ============================================================
#
# KEY CONCEPT: Why Session State Exists
# ----------------------------------------
# Streamlit reruns your script on every interaction.
# Local variables are RESET each rerun — they don't persist.
#
#   count = 0  ← always resets to 0 on rerun!
#
# st.session_state is a dictionary-like object that PERSISTS
# across reruns for the lifetime of the user's browser session.
#
#   st.session_state["count"] ← survives reruns ✓

import streamlit as st

st.set_page_config(page_title="Lesson 06 · Session State", page_icon="🔄")
st.title("🔄 Lesson 06: Session State & Reactivity")

# ── 1. The Problem Without Session State ─────────────────────
st.header("1. The Problem — Counter Without Session State")
st.markdown("⚠️ This counter is **broken** — it resets to 0 on every click because `count` is a local variable.")

# This will NOT work as a counter:
broken_count = 0
if st.button("Increment (broken)", key="broken_btn"):
    broken_count += 1
st.write(f"Broken count: {broken_count}")   # always 0

# ── 2. Fixing It With Session State ──────────────────────────
st.header("2. The Fix — Session State Counter")

# Initialize once — check before setting to avoid resetting on rerun
if "count" not in st.session_state:
    st.session_state.count = 0   # dot notation works!

col1, col2, col3 = st.columns(3)
if col1.button("➕ Increment"):
    st.session_state.count += 1
if col2.button("➖ Decrement"):
    st.session_state.count -= 1
if col3.button("🔄 Reset"):
    st.session_state.count = 0

st.metric("Counter", st.session_state.count)

# ── 3. Accessing Session State ────────────────────────────────
st.header("3. Reading & Writing Session State")
st.markdown("""
Two equivalent syntaxes:
- **Dot notation**: `st.session_state.my_key = value`
- **Dict notation**: `st.session_state["my_key"] = value`
""")

st.subheader("Inspect current session state")
st.json(dict(st.session_state))   # see all keys

# ── 4. Widget Keys & Session State ────────────────────────────
st.header("4. Widget Keys — Direct Session State Binding")
st.markdown("""
When you give a widget a `key`, its value is **automatically**
stored in `st.session_state[key]` — no need to capture the return value.

```python
st.text_input("Name", key="username")
# Now st.session_state.username always has the current value
```
""")

st.text_input("Enter your name", key="username", placeholder="Atabi")
st.selectbox("Favourite colour", ["Red", "Green", "Blue"], key="fav_color")

if st.session_state.get("username"):
    st.success(f"Hi **{st.session_state.username}**! Your favourite colour is **{st.session_state.fav_color}**.")

# ── 5. Callbacks (on_change / on_click) ───────────────────────
st.header("5. Callbacks — on_change & on_click")
st.markdown("""
Callbacks run BEFORE the rest of the script on each rerun.
Use them to react to a specific widget change without writing an if-block.
""")

def on_slider_change():
    """Called whenever the slider moves."""
    st.session_state.slider_history = st.session_state.get("slider_history", [])
    st.session_state.slider_history.append(st.session_state.temp_slider)

st.slider("Temperature (°C)", -20, 50, 20, key="temp_slider", on_change=on_slider_change)

history = st.session_state.get("slider_history", [])
if history:
    st.write(f"You've visited these temperatures: {history[-5:]}")  # last 5

def on_submit_click():
    if st.session_state.get("search_query"):
        st.session_state.last_search = st.session_state.search_query

st.divider()
st.text_input("Search query", key="search_query")
st.button("Submit search", on_click=on_submit_click)

if "last_search" in st.session_state:
    st.success(f"Last search submitted: **{st.session_state.last_search}**")

# ── 6. Multi-step Wizard Pattern ──────────────────────────────
st.header("6. Pattern — Multi-step Wizard")
st.markdown("Session state makes multi-step flows easy.")

if "step" not in st.session_state:
    st.session_state.step = 1

steps = ["Personal Info", "Preferences", "Confirmation"]
progress = (st.session_state.step - 1) / (len(steps) - 1)
st.progress(progress, text=f"Step {st.session_state.step} of {len(steps)}: {steps[st.session_state.step - 1]}")

if st.session_state.step == 1:
    st.session_state.wizard_name = st.text_input("Full name", value=st.session_state.get("wizard_name", ""))
    if st.button("Next →", key="step1_next") and st.session_state.wizard_name:
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.session_state.wizard_lang = st.selectbox("Preferred language",
        ["Python", "JavaScript", "Go"], index=0)
    col1, col2 = st.columns(2)
    if col1.button("← Back", key="step2_back"):
        st.session_state.step = 1; st.rerun()
    if col2.button("Next →", key="step2_next"):
        st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    st.success(f"""
    **Confirm your details:**
    - Name: {st.session_state.get('wizard_name', '')}
    - Language: {st.session_state.get('wizard_lang', '')}
    """)
    col1, col2 = st.columns(2)
    if col1.button("← Back", key="step3_back"):
        st.session_state.step = 2; st.rerun()
    if col2.button("✅ Submit", key="step3_submit"):
        st.balloons()
        st.session_state.step = 1  # reset

# ── 7. Toggle Pattern ─────────────────────────────────────────
st.header("7. Pattern — Toggle Visibility")

if "show_panel" not in st.session_state:
    st.session_state.show_panel = False

if st.button("Toggle hidden panel"):
    st.session_state.show_panel = not st.session_state.show_panel

if st.session_state.show_panel:
    with st.container(border=True):
        st.subheader("Hidden Panel 🎉")
        st.write("This panel persists across reruns using session state.")

# ── 8. Deleting State ─────────────────────────────────────────
st.header("8. Deleting Session State Keys")
st.code("""
# Delete a specific key
del st.session_state["my_key"]

# Clear ALL session state
st.session_state.clear()
""")

if st.button("Clear all session state (refresh page)"):
    st.session_state.clear()
    st.rerun()

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Build a shopping cart: a `st.selectbox` of items, an "Add to cart" button,
   and a list showing all added items (stored in session state).
2. Build an undo button: every time the user types in a `st.text_area`,
   save the value to a history list; "Undo" pops the last entry.
3. Create a 3-question quiz where each answer is stored in session state
   and the final score is shown at the end.
4. Use `on_change` callback on a number_input to log every value change.
""")
