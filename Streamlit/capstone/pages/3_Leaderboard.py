# Capstone · Page 3 — Leaderboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

st.set_page_config(page_title="Leaderboard · Sales Intelligence", page_icon="🏆", layout="wide")

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

st.title("🏆 Leaderboard")

@st.cache_data
def generate_sales_data(seed=42):
    np.random.seed(seed)
    n = 1200
    dates = pd.date_range("2024-01-01", "2024-12-31")
    df = pd.DataFrame({
        "date":    np.random.choice(dates, n),
        "rep":     np.random.choice(["Alice","Bob","Carol","Dan","Eve","Frank"], n),
        "region":  np.random.choice(["North","South","East","West"], n),
        "product": np.random.choice(["Widget A","Widget B","Widget C","Widget D"], n),
        "units":   np.random.randint(1, 20, n),
        "price":   np.random.uniform(50, 500, n).round(2),
    })
    df["revenue"] = df["units"] * df["price"]
    return df

df_raw = generate_sales_data()
df = df_raw[
    (df_raw["date"] >= pd.Timestamp(st.session_state.date_start)) &
    (df_raw["date"] <= pd.Timestamp(st.session_state.date_end))
]

# Define quotas per rep
QUOTAS = {"Alice": 180_000, "Bob": 160_000, "Carol": 170_000,
          "Dan": 155_000, "Eve": 165_000, "Frank": 150_000}

tab_reps, tab_products, tab_trends = st.tabs(["👥 Rep Rankings", "📦 Product Rankings", "📈 Trends"])

# ── Tab 1: Rep Rankings ────────────────────────────────────────
with tab_reps:
    rep_df = df.groupby("rep").agg(
        revenue=("revenue", "sum"),
        deals=("revenue", "count"),
        avg_deal=("revenue", "mean"),
    ).reset_index().sort_values("revenue", ascending=False).reset_index(drop=True)

    rep_df["quota"]    = rep_df["rep"].map(QUOTAS)
    rep_df["attainment"] = rep_df["revenue"] / rep_df["quota"]
    rep_df["rank"]     = rep_df["revenue"].rank(ascending=False).astype(int)
    rep_df["medal"]    = rep_df["rank"].map({1: "🥇", 2: "🥈", 3: "🥉"}).fillna("")

    st.dataframe(
        rep_df[["medal","rep","revenue","quota","attainment","deals","avg_deal"]],
        column_config={
            "medal":       st.column_config.TextColumn(""),
            "rep":         st.column_config.TextColumn("Rep"),
            "revenue":     st.column_config.NumberColumn("Revenue",   format="$%,.0f"),
            "quota":       st.column_config.NumberColumn("Quota",     format="$%,.0f"),
            "attainment":  st.column_config.ProgressColumn("Attainment", min_value=0, max_value=1.5,
                                                             format="%.0%"),
            "deals":       st.column_config.NumberColumn("# Deals"),
            "avg_deal":    st.column_config.NumberColumn("Avg Deal",  format="$%,.0f"),
        },
        hide_index=True,
        use_container_width=True,
    )

    fig = px.bar(rep_df, x="rep", y="revenue", color="attainment",
                 color_continuous_scale="RdYlGn",
                 range_color=[0, 1.5],
                 title="Revenue vs Quota Attainment",
                 template="plotly_white")
    fig.add_scatter(x=rep_df["rep"], y=rep_df["quota"],
                    mode="markers+lines", name="Quota",
                    marker_symbol="diamond", marker_size=12,
                    line_dash="dash", marker_color="black")
    st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Product Rankings ────────────────────────────────────
with tab_products:
    prod_df = df.groupby("product").agg(
        revenue=("revenue", "sum"),
        units=("units", "sum"),
        avg_price=("price", "mean"),
        deals=("revenue", "count"),
    ).reset_index().sort_values("revenue", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.treemap(prod_df, path=["product"], values="revenue",
                          color="revenue", color_continuous_scale="Blues",
                          title="Revenue Treemap by Product")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.scatter(prod_df, x="units", y="avg_price", size="revenue",
                          color="product", text="product",
                          title="Units vs Avg Price (bubble = revenue)",
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(prod_df, column_config={
        "revenue":   st.column_config.NumberColumn("Revenue",   format="$%,.0f"),
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%,.2f"),
    }, use_container_width=True, hide_index=True)

# ── Tab 3: Trends ─────────────────────────────────────────────
with tab_trends:
    monthly_rep = (df.groupby([df["date"].dt.to_period("M"), "rep"])["revenue"]
                   .sum().reset_index())
    monthly_rep["date"] = monthly_rep["date"].dt.to_timestamp()

    fig = px.line(monthly_rep, x="date", y="revenue", color="rep",
                  title="Monthly Revenue by Rep", template="plotly_white",
                  markers=True)
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap: rep × month
    pivot = monthly_rep.pivot(index="rep", columns="date", values="revenue").fillna(0)
    pivot.columns = [c.strftime("%b") for c in pivot.columns]

    fig = px.imshow(pivot, color_continuous_scale="Blues",
                    title="Revenue Heatmap (Rep × Month)",
                    aspect="auto", text_auto="$,.0f")
    st.plotly_chart(fig, use_container_width=True)
