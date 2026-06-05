# Capstone · Page 1 — Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Dashboard · Sales Intelligence", page_icon="📊", layout="wide")

# ── Sidebar (shared controls) ─────────────────────────────────
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=48)
    st.markdown("## 📈 Sales Intelligence")
    st.divider()

    import datetime
    st.subheader("📅 Date Range")
    st.session_state.setdefault("date_start", datetime.date(2024, 1, 1))
    st.session_state.setdefault("date_end",   datetime.date(2024, 12, 31))
    st.session_state.date_start = st.date_input("From", value=st.session_state.date_start)
    st.session_state.date_end   = st.date_input("To",   value=st.session_state.date_end)

    st.divider()
    region_filter = st.multiselect(
        "Region", ["North", "South", "East", "West"],
        default=["North", "South", "East", "West"]
    )
    product_filter = st.multiselect(
        "Product", ["Widget A", "Widget B", "Widget C", "Widget D"],
        default=["Widget A", "Widget B", "Widget C", "Widget D"]
    )

# ── Cached data generation ─────────────────────────────────────
@st.cache_data
def generate_sales_data(seed: int = 42) -> pd.DataFrame:
    """Simulates a full year of daily sales transactions."""
    np.random.seed(seed)
    n = 1200
    dates = pd.date_range("2024-01-01", "2024-12-31")
    return pd.DataFrame({
        "date":    np.random.choice(dates, n),
        "rep":     np.random.choice(["Alice","Bob","Carol","Dan","Eve","Frank"], n),
        "region":  np.random.choice(["North","South","East","West"], n),
        "product": np.random.choice(["Widget A","Widget B","Widget C","Widget D"], n),
        "units":   np.random.randint(1, 20, n),
        "price":   np.random.uniform(50, 500, n).round(2),
    })

df_raw = generate_sales_data()
df_raw["revenue"] = df_raw["units"] * df_raw["price"]

# Apply filters
df = df_raw[
    (df_raw["date"] >= pd.Timestamp(st.session_state.date_start)) &
    (df_raw["date"] <= pd.Timestamp(st.session_state.date_end)) &
    (df_raw["region"].isin(region_filter)) &
    (df_raw["product"].isin(product_filter))
]

# ── Page title ────────────────────────────────────────────────
st.title("📊 Dashboard")
st.caption(f"Showing {len(df):,} transactions · "
           f"{st.session_state.date_start} → {st.session_state.date_end} · "
           f"{len(region_filter)} region(s) · {len(product_filter)} product(s)")

if df.empty:
    st.warning("No data matches the current filters. Adjust the sidebar.")
    st.stop()

# ── KPI Row ────────────────────────────────────────────────────
total_rev   = df["revenue"].sum()
total_units = df["units"].sum()
avg_deal    = df["revenue"].mean()
n_reps      = df["rep"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue",  f"${total_rev:,.0f}",  "+12.4%")
c2.metric("📦 Units Sold",     f"{total_units:,}",     "+8.1%")
c3.metric("🤝 Avg Deal Size",  f"${avg_deal:,.0f}",   "+3.2%")
c4.metric("👤 Active Reps",    str(n_reps))

st.divider()

# ── Charts Row 1 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

# Revenue over time
with col1:
    monthly = (df.groupby(df["date"].dt.to_period("M"))["revenue"]
               .sum().reset_index())
    monthly["date"] = monthly["date"].dt.to_timestamp()
    fig = px.area(monthly, x="date", y="revenue",
                  title="Monthly Revenue", template="plotly_white",
                  color_discrete_sequence=["#4A90D9"])
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

# Revenue by region
with col2:
    by_region = df.groupby("region")["revenue"].sum().reset_index()
    fig = px.pie(by_region, names="region", values="revenue",
                 title="Revenue by Region", template="plotly_white",
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

# Product comparison
with col1:
    by_product = df.groupby("product").agg(
        revenue=("revenue", "sum"),
        units=("units", "sum"),
    ).reset_index()
    fig = px.bar(by_product, x="product", y="revenue", color="product",
                 title="Revenue by Product", template="plotly_white",
                 text_auto="$,.0f")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Rep leaderboard (horizontal bar)
with col2:
    by_rep = df.groupby("rep")["revenue"].sum().sort_values().reset_index()
    fig = px.bar(by_rep, y="rep", x="revenue", orientation="h",
                 title="Revenue by Rep", template="plotly_white",
                 color="revenue", color_continuous_scale="Blues",
                 text_auto="$,.0f")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Data Table ────────────────────────────────────────────────
st.divider()
with st.expander("📋 View raw transactions"):
    st.dataframe(
        df.sort_values("date", ascending=False),
        column_config={
            "date":    st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
            "revenue": st.column_config.NumberColumn("Revenue", format="$%.2f"),
            "price":   st.column_config.NumberColumn("Unit Price", format="$%.2f"),
        },
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "⬇️ Export filtered CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales.csv",
        mime="text/csv",
    )
