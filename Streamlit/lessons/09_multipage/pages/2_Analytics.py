# Page 2 — Analytics
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analytics", page_icon="🔬", layout="wide")

with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', 'Guest')}")
    st.divider()
    region = st.selectbox("Region", ["All", "North", "South", "East", "West"])
    year   = st.selectbox("Year", [2024, 2023, 2022])

st.title("🔬 Analytics")
st.caption("This is Page 2 — note sidebar filters defined here, on this page only.")

np.random.seed(year)
df = pd.DataFrame({
    "Region":   np.random.choice(["North", "South", "East", "West"], 200),
    "Product":  np.random.choice(["Widget A", "Widget B", "Widget C"], 200),
    "Sales":    np.random.uniform(100, 5000, 200).round(2),
    "Units":    np.random.randint(1, 50, 200),
})

if region != "All":
    df = df[df["Region"] == region]

col1, col2 = st.columns(2)

fig1 = px.box(df, x="Product", y="Sales", color="Product",
              title=f"Sales Distribution by Product — {region}, {year}",
              template="plotly_white")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(df, x="Units", y="Sales", color="Region",
                   title="Units vs Sales", template="plotly_white")
col2.plotly_chart(fig2, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(df.head(30), use_container_width=True, hide_index=True)
