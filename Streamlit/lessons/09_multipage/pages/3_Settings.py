# Page 3 — Settings
import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️")

with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', 'Guest')}")

st.title("⚙️ Settings")
st.caption("This is Page 3 — settings saved here persist via session_state.")

st.subheader("Profile")
st.session_state.username = st.text_input("Display name", value=st.session_state.get("username", ""))
st.session_state.email    = st.text_input("Email", value=st.session_state.get("email", ""))

st.subheader("Preferences")
st.session_state.theme    = st.selectbox("Theme", ["Light", "Dark", "System"],
                                          index=["Light","Dark","System"].index(
                                              st.session_state.get("theme", "Light")))
st.session_state.notifs   = st.toggle("Email notifications",
                                       value=st.session_state.get("notifs", True))

if st.button("Save settings", type="primary"):
    st.success("Settings saved to session state! They'll persist while you navigate between pages.")

st.divider()
st.subheader("Current Session State")
st.json({k: v for k, v in st.session_state.items()})
