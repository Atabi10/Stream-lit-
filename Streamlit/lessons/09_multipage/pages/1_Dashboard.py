# Page 1 — Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', 'Guest')}")

st.title("📊 Dashboard")
st.caption("This is Page 1, defined in pages/1_Dashboard.py")

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue",    "$84,320",  "+14%")
c2.metric("Orders",     "1,240",    "+8%")
c3.metric("Avg Order",  "$67.98",   "+5%")
c4.metric("Returns",    "3.2%",     "-0.5%", delta_color="inverse")

# Chart
np.random.seed(1)
dates = pd.date_range("2024-01", periods=12, freq="MS")
df = pd.DataFrame({
    "Month":   dates,
    "Revenue": np.random.randint(60_000, 120_000, 12),
    "Costs":   np.random.randint(40_000, 80_000, 12),
})
df["Profit"] = df["Revenue"] - df["Costs"]
df_long = df.melt("Month", var_name="Metric", value_name="Amount")

fig = px.bar(df_long, x="Month", y="Amount", color="Metric",
             barmode="group", title="Monthly Revenue, Costs & Profit",
             template="plotly_white")
st.plotly_chart(fig, use_container_width=True)
