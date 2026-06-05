# ============================================================
# LESSON 07 — Forms, File Upload & Download
# Run: streamlit run lessons/07_forms_files.py
# ============================================================
#
# KEY CONCEPT: Why Forms Exist
# ------------------------------
# Without a form, EVERY widget interaction reruns the whole script.
# This means typing in a text box triggers a rerun on each keystroke.
#
# st.form groups widgets together and ONLY reruns when the
# submit button is clicked — giving you a "collect all values,
# then act" pattern identical to a traditional HTML form.

import streamlit as st
import pandas as pd
import numpy as np
import io
import json

st.set_page_config(page_title="Lesson 07 · Forms & Files", page_icon="📁")
st.title("📁 Lesson 07: Forms, File Upload & Download")

# ── 1. Basic Form ────────────────────────────────────────────
st.header("1. Basic Form")
st.markdown("""
Inside `with st.form(key)`, all widgets are collected.
The script only reruns when the submit button is clicked.
""")

with st.form("contact_form"):
    st.subheader("Contact Form")
    name    = st.text_input("Full name *")
    email   = st.text_input("Email address *")
    subject = st.selectbox("Subject", ["General", "Support", "Billing", "Other"])
    message = st.text_area("Message", height=120)
    urgency = st.slider("Urgency", 1, 5, 3)

    submitted = st.form_submit_button("📧 Send Message", type="primary")

if submitted:
    if name and email:
        st.success(f"✅ Message sent by **{name}** ({email}) — Subject: {subject}")
        st.json({"name": name, "email": email, "subject": subject,
                 "message": message, "urgency": urgency})
    else:
        st.error("Please fill in Name and Email.")

# ── 2. Form with clear_on_submit ─────────────────────────────
st.header("2. Form with clear_on_submit")
st.markdown("`clear_on_submit=True` resets widgets to defaults after submission.")

with st.form("quick_add", clear_on_submit=True):
    item = st.text_input("Add item to list")
    qty  = st.number_input("Quantity", min_value=1, value=1)
    submitted2 = st.form_submit_button("Add")

if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []

if submitted2 and item:
    st.session_state.shopping_list.append({"item": item, "qty": qty})

if st.session_state.shopping_list:
    st.subheader("Shopping List")
    df_list = pd.DataFrame(st.session_state.shopping_list)
    st.dataframe(df_list, use_container_width=True, hide_index=True)
    if st.button("Clear list"):
        st.session_state.shopping_list = []
        st.rerun()

# ── 3. File Uploader ─────────────────────────────────────────
st.header("3. File Uploader")
st.markdown("""
`st.file_uploader` returns a file-like object (or `None` if nothing uploaded).
You can pass it directly to `pd.read_csv`, `json.load`, etc.
""")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"],
    help="Max size: 200 MB by default",
)

if uploaded_file is not None:
    st.success(f"File: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")

    df_uploaded = pd.read_csv(uploaded_file)
    st.write(f"Shape: {df_uploaded.shape[0]} rows × {df_uploaded.shape[1]} cols")
    st.dataframe(df_uploaded.head(20), use_container_width=True)

    # Column summary
    with st.expander("Column Summary"):
        st.dataframe(df_uploaded.describe(), use_container_width=True)
else:
    st.info("Upload a CSV to see it parsed here.")
    # Show what a CSV looks like for testing
    with st.expander("Need a sample CSV?"):
        sample = pd.DataFrame({
            "name":   ["Alice", "Bob", "Carol"],
            "score":  [88, 92, 76],
            "dept":   ["Sales", "Eng", "Sales"],
        })
        st.dataframe(sample)
        st.caption("Copy this to a .csv file to test the uploader.")

# ── 4. Multiple File Upload ────────────────────────────────────
st.header("4. Multiple File Upload")

multi_files = st.file_uploader(
    "Upload multiple JSON files",
    type=["json"],
    accept_multiple_files=True,
)

if multi_files:
    st.write(f"Uploaded {len(multi_files)} file(s):")
    for f in multi_files:
        try:
            data = json.load(f)
            with st.expander(f"📄 {f.name}"):
                st.json(data)
        except Exception as e:
            st.error(f"{f.name}: {e}")

# ── 5. Image Upload ───────────────────────────────────────────
st.header("5. Image Upload")

img_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "gif", "webp"])
if img_file:
    st.image(img_file, caption=img_file.name, use_container_width=True)

# ── 6. Download Button ────────────────────────────────────────
st.header("6. Download Button")
st.markdown("""
`st.download_button` lets users download any data as a file.
Common patterns: export a DataFrame as CSV, download a report as JSON.
""")

# Generate sample data
np.random.seed(42)
export_df = pd.DataFrame({
    "Month":   pd.date_range("2024-01", periods=12, freq="MS").strftime("%b %Y"),
    "Revenue": np.random.randint(30_000, 100_000, 12),
    "Costs":   np.random.randint(20_000, 60_000, 12),
})
export_df["Profit"] = export_df["Revenue"] - export_df["Costs"]

st.dataframe(export_df, use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns(3)

# Download as CSV
csv_data = export_df.to_csv(index=False).encode("utf-8")
col1.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name="monthly_report.csv",
    mime="text/csv",
)

# Download as JSON
json_data = export_df.to_json(orient="records", indent=2).encode("utf-8")
col2.download_button(
    label="⬇️ Download JSON",
    data=json_data,
    file_name="monthly_report.json",
    mime="application/json",
)

# Download as Excel (requires openpyxl)
try:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="Report")
    col3.download_button(
        label="⬇️ Download Excel",
        data=buffer.getvalue(),
        file_name="monthly_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
except ImportError:
    col3.warning("Install openpyxl for Excel export")

# ── 7. Upload → Process → Download Pipeline ──────────────────
st.header("7. Full Pipeline — Upload → Process → Download")
st.markdown("Upload a CSV, apply a transformation, download the result.")

pipeline_file = st.file_uploader("Upload CSV for processing", type="csv", key="pipeline")

if pipeline_file:
    df_raw = pd.read_csv(pipeline_file)
    st.write("**Original data:**")
    st.dataframe(df_raw.head(), use_container_width=True)

    numeric_cols = df_raw.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        col_to_normalize = st.selectbox("Column to normalize (0-1 scale)", numeric_cols)

        df_processed = df_raw.copy()
        col_min = df_processed[col_to_normalize].min()
        col_max = df_processed[col_to_normalize].max()
        df_processed[f"{col_to_normalize}_normalized"] = (
            (df_processed[col_to_normalize] - col_min) / (col_max - col_min)
        )

        st.write("**Processed data:**")
        st.dataframe(df_processed.head(), use_container_width=True)

        st.download_button(
            "⬇️ Download processed CSV",
            data=df_processed.to_csv(index=False).encode("utf-8"),
            file_name="processed.csv",
            mime="text/csv",
        )
    else:
        st.warning("No numeric columns found to normalize.")

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Build a "User Registration" form with: name, email, password (masked), age slider, agree checkbox.
   Show a summary card on submit.
2. Upload a CSV, let the user pick which columns to keep, and download the filtered version.
3. Upload an image and display it with a caption the user types.
4. Build a "notes" app: a `st.text_area` in a form, stored in session state, with a download button
   that exports all notes as a `.txt` file.
""")
