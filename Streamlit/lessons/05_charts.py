# ============================================================
# LESSON 05 — Charts & Visualizations
# Run: streamlit run lessons/05_charts.py
# ============================================================
#
# Three tiers of charts in Streamlit:
#   1. Built-in (st.line_chart, st.bar_chart, etc.) — quick, zero config
#   2. Matplotlib/Seaborn — full control, static
#   3. Plotly — interactive, production-quality

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Lesson 05 · Charts", page_icon="📊", layout="wide")
st.title("📊 Lesson 05: Charts & Visualizations")

# ── Shared data ───────────────────────────────────────────────
np.random.seed(7)
dates = pd.date_range("2024-01-01", periods=52, freq="W")
sales_df = pd.DataFrame({
    "Date":    dates,
    "Product A": np.random.randint(50, 200, 52).cumsum(),
    "Product B": np.random.randint(30, 150, 52).cumsum(),
    "Product C": np.random.randint(10, 100, 52).cumsum(),
}).set_index("Date")

category_df = pd.DataFrame({
    "Category": ["Electronics", "Clothing", "Food", "Books", "Sports"],
    "Sales":    [42000, 28000, 35000, 15000, 22000],
    "Profit":   [8000, 5000, 4200, 3800, 4500],
})

# ═══════════════════════════════════════════════════════════
# TIER 1: Built-in Streamlit Charts
# ═══════════════════════════════════════════════════════════
st.header("Tier 1 — Built-in Charts (Quick)")
st.markdown("Pass a DataFrame and Streamlit handles everything. Limited customisation but very fast to write.")

# ── st.line_chart ─────────────────────────────────────────────
st.subheader("st.line_chart")
st.line_chart(sales_df)

col1, col2 = st.columns(2)

# ── st.bar_chart ──────────────────────────────────────────────
col1.subheader("st.bar_chart")
col1.bar_chart(category_df.set_index("Category")["Sales"])

# ── st.area_chart ─────────────────────────────────────────────
col2.subheader("st.area_chart")
col2.area_chart(sales_df[["Product A", "Product B"]])

# ── st.scatter_chart ──────────────────────────────────────────
st.subheader("st.scatter_chart")
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "size": np.random.uniform(10, 100, 100),
    "color": np.random.choice(["A", "B", "C"], 100),
})
st.scatter_chart(scatter_data, x="x", y="y", size="size", color="color")

# ── st.map ─────────────────────────────────────────────────────
st.subheader("st.map — World Cities")
map_data = pd.DataFrame({
    "lat": [35.68, 51.51, 40.71, 48.85, -33.87, 55.75],
    "lon": [139.69, -0.13, -74.01, 2.35, 151.21, 37.62],
    "city": ["Tokyo", "London", "New York", "Paris", "Sydney", "Moscow"],
})
st.map(map_data, zoom=1)

# ═══════════════════════════════════════════════════════════
# TIER 2: Matplotlib
# ═══════════════════════════════════════════════════════════
st.divider()
st.header("Tier 2 — Matplotlib (Full Control)")
st.markdown("""
Create a `fig, ax` pair with Matplotlib, then pass `fig` to `st.pyplot(fig)`.
Never use `plt.show()` in Streamlit — use `st.pyplot` instead.
""")

col1, col2 = st.columns(2)

# ── Line chart ────────────────────────────────────────────────
with col1:
    st.subheader("Matplotlib Line Chart")
    fig, ax = plt.subplots(figsize=(6, 3))
    for col in sales_df.columns:
        ax.plot(sales_df.index, sales_df[col], label=col, linewidth=2)
    ax.set_title("Weekly Cumulative Sales", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Units")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)   # always close to free memory

# ── Bar chart ─────────────────────────────────────────────────
with col2:
    st.subheader("Matplotlib Bar Chart")
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(len(category_df))
    width = 0.35
    bars1 = ax.bar(x - width/2, category_df["Sales"],   width, label="Sales",  color="#4A90D9")
    bars2 = ax.bar(x + width/2, category_df["Profit"],  width, label="Profit", color="#7ED321")
    ax.set_xticks(x)
    ax.set_xticklabels(category_df["Category"], rotation=20)
    ax.set_title("Sales vs Profit by Category")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ── Histogram ─────────────────────────────────────────────────
st.subheader("Matplotlib Histogram")
col1, col2 = st.columns(2)

bins = col1.slider("Number of bins", 5, 50, 20)
data = np.random.normal(100, 15, 1000)

fig, ax = plt.subplots(figsize=(6, 3))
ax.hist(data, bins=bins, edgecolor="white", color="#9B59B6", alpha=0.85)
ax.axvline(data.mean(), color="red", linestyle="--", label=f"Mean = {data.mean():.1f}")
ax.set_title("Distribution of Scores")
ax.set_xlabel("Score")
ax.set_ylabel("Frequency")
ax.legend()
plt.tight_layout()
col2.pyplot(fig)
plt.close(fig)

# ═══════════════════════════════════════════════════════════
# TIER 3: Plotly (Interactive, Production-Quality)
# ═══════════════════════════════════════════════════════════
st.divider()
st.header("Tier 3 — Plotly (Interactive)")
st.markdown("""
Plotly charts are fully **interactive**: hover tooltips, zoom, pan, download PNG.
`plotly.express` (px) is the high-level API — use it 90% of the time.
`plotly.graph_objects` (go) is the low-level API — for full control.
""")

# ── px.line ───────────────────────────────────────────────────
st.subheader("Plotly Express — Line Chart")
sales_long = sales_df.reset_index().melt(id_vars="Date", var_name="Product", value_name="Sales")
fig = px.line(sales_long, x="Date", y="Sales", color="Product",
              title="Weekly Cumulative Sales by Product",
              template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ── px.bar ────────────────────────────────────────────────────
st.subheader("Plotly Express — Grouped Bar")
fig = px.bar(category_df, x="Category", y=["Sales", "Profit"],
             barmode="group", title="Sales vs Profit",
             color_discrete_sequence=["#4A90D9", "#7ED321"],
             template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ── px.scatter ────────────────────────────────────────────────
st.subheader("Plotly Express — Scatter with Trendline")
gapminder_sample = pd.DataFrame({
    "Country": ["USA", "China", "India", "Germany", "UK", "France", "Brazil", "Japan"],
    "GDP":     [65000, 12000, 6000, 48000, 42000, 40000, 15000, 40000],
    "LifeExp": [79, 77, 70, 81, 81, 82, 75, 84],
    "Pop":     [331, 1439, 1380, 83, 67, 65, 213, 126],
    "Region":  ["Americas","Asia","Asia","Europe","Europe","Europe","Americas","Asia"],
})
fig = px.scatter(gapminder_sample, x="GDP", y="LifeExp", size="Pop",
                 color="Region", hover_name="Country", text="Country",
                 title="GDP vs Life Expectancy",
                 labels={"GDP": "GDP per Capita ($)", "LifeExp": "Life Expectancy"},
                 template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ── Plotly go — Gauge Chart ───────────────────────────────────
st.subheader("Plotly graph_objects — Gauge + Indicator")
col1, col2 = st.columns(2)

gauge_val = col1.slider("Gauge value", 0, 100, 72)

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=gauge_val,
    delta={"reference": 60},
    title={"text": "Performance Score"},
    gauge={
        "axis": {"range": [0, 100]},
        "steps": [
            {"range": [0, 40],  "color": "salmon"},
            {"range": [40, 70], "color": "gold"},
            {"range": [70, 100],"color": "lightgreen"},
        ],
        "threshold": {"line": {"color": "red", "width": 4}, "value": 90},
        "bar": {"color": "#4A90D9"},
    }
))
col2.plotly_chart(fig, use_container_width=True)

# ── Plotly go — Funnel Chart ─────────────────────────────────
st.subheader("Plotly — Funnel (Sales Pipeline)")
funnel_df = pd.DataFrame({
    "Stage": ["Leads", "Qualified", "Demo", "Proposal", "Closed"],
    "Count": [1000, 450, 200, 80, 32],
})
fig = px.funnel(funnel_df, x="Count", y="Stage",
                color_discrete_sequence=["#4A90D9"],
                template="plotly_white", title="Sales Funnel")
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Use `st.line_chart` to plot a random walk (cumsum of random values).
2. Create a Matplotlib pie chart for the `category_df` Sales column.
3. Use `px.histogram` to plot a distribution with a slider controlling bins.
4. Build a `px.pie` chart for category shares.
5. Use `go.Bar` with custom colors (green for positive, red for negative values).
""")
