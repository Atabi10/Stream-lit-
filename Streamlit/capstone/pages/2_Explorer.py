# Capstone · Page 2 — Data Explorer (File Upload + Edit + Download)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

st.set_page_config(page_title="Explorer · Sales Intelligence", page_icon="🔍", layout="wide")

with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=48)
    st.markdown("## 📈 Sales Intelligence")
    st.divider()
    st.caption("Upload your own CSV to explore it here.")

st.title("🔍 Data Explorer")
st.markdown("Upload any CSV file. Filter, edit, visualise, and export it.")

# ── Upload ────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload a CSV file", type="csv")

@st.cache_data
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))

if uploaded:
    df = load_csv(uploaded.read())
    st.success(f"**{uploaded.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")

    # ── Quick Profile ─────────────────────────────────────────
    with st.expander("📊 Data Profile", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows",    f"{df.shape[0]:,}")
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing values", int(df.isnull().sum().sum()))
        col4.metric("Numeric cols",   len(df.select_dtypes("number").columns))
        st.dataframe(df.describe(), use_container_width=True)

    # ── Column Selector ───────────────────────────────────────
    st.subheader("Column Selector")
    all_cols = df.columns.tolist()
    selected_cols = st.multiselect("Keep columns", all_cols, default=all_cols)
    df_view = df[selected_cols] if selected_cols else df

    # ── Filter Form ───────────────────────────────────────────
    st.subheader("Row Filter")
    numeric_cols = df_view.select_dtypes("number").columns.tolist()
    categorical_cols = df_view.select_dtypes("object").columns.tolist()

    with st.form("filter_form"):
        col1, col2 = st.columns(2)

        num_col = col1.selectbox("Numeric column to filter", ["(none)"] + numeric_cols)
        if num_col != "(none)":
            lo = float(df_view[num_col].min())
            hi = float(df_view[num_col].max())
            num_range = col1.slider(f"{num_col} range", lo, hi, (lo, hi))
        else:
            num_range = None

        cat_col = col2.selectbox("Categorical column to filter", ["(none)"] + categorical_cols)
        if cat_col != "(none)":
            cat_vals = col2.multiselect(f"{cat_col} values",
                                         df_view[cat_col].dropna().unique().tolist(),
                                         default=df_view[cat_col].dropna().unique().tolist())
        else:
            cat_vals = None

        apply = st.form_submit_button("Apply Filters", type="primary")

    df_filtered = df_view.copy()
    if apply:
        if num_col != "(none)" and num_range:
            df_filtered = df_filtered[df_filtered[num_col].between(*num_range)]
        if cat_col != "(none)" and cat_vals:
            df_filtered = df_filtered[df_filtered[cat_col].isin(cat_vals)]

    st.write(f"**{len(df_filtered):,}** rows after filter")

    # ── Editable Table ────────────────────────────────────────
    st.subheader("Edit Data")
    edited = st.data_editor(df_filtered.head(100), use_container_width=True,
                             num_rows="dynamic", hide_index=True)

    # ── Quick Chart ───────────────────────────────────────────
    if len(numeric_cols) >= 1:
        st.subheader("Quick Visualisation")
        chart_col1, chart_col2 = st.columns(2)
        x_col = chart_col1.selectbox("X axis", df_filtered.columns.tolist())
        y_col = chart_col2.selectbox("Y axis", numeric_cols)
        chart_type = st.radio("Chart type", ["Bar", "Line", "Scatter"], horizontal=True)

        if chart_type == "Bar":
            fig = px.bar(df_filtered.head(50), x=x_col, y=y_col, template="plotly_white")
        elif chart_type == "Line":
            fig = px.line(df_filtered.head(50), x=x_col, y=y_col, template="plotly_white")
        else:
            fig = px.scatter(df_filtered.head(200), x=x_col, y=y_col, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # ── Download ──────────────────────────────────────────────
    st.divider()
    col1, col2 = st.columns(2)
    col1.download_button(
        "⬇️ Download filtered CSV",
        df_filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv", mime="text/csv",
    )
    col2.download_button(
        "⬇️ Download edited CSV",
        edited.to_csv(index=False).encode("utf-8"),
        file_name="edited_data.csv", mime="text/csv",
    )

else:
    st.info("Upload a CSV file above to get started.")

    # Show a sample to download and test with
    st.subheader("Don't have a CSV? Download this sample:")
    np.random.seed(0)
    sample = pd.DataFrame({
        "date":    pd.date_range("2024-01", periods=50, freq="W").strftime("%Y-%m-%d"),
        "region":  np.random.choice(["North","South","East","West"], 50),
        "product": np.random.choice(["Widget A","Widget B","Widget C"], 50),
        "revenue": np.random.randint(1000, 50000, 50),
        "units":   np.random.randint(1, 100, 50),
    })
    st.download_button(
        "⬇️ Download sample.csv",
        sample.to_csv(index=False).encode("utf-8"),
        file_name="sample.csv", mime="text/csv",
    )
