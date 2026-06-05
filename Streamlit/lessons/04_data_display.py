# ============================================================
# LESSON 04 — Data Display: DataFrames, Tables, Metrics
# Run: streamlit run lessons/04_data_display.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Lesson 04 · Data Display", page_icon="📋", layout="wide")
st.title("📋 Lesson 04: Data Display")

# Sample data we'll reuse throughout the lesson
np.random.seed(42)
df = pd.DataFrame({
    "Name":     ["Alice", "Bob", "Carol", "Dan", "Eve", "Frank", "Grace", "Hank"],
    "Dept":     ["Sales", "Eng", "Sales", "Marketing", "Eng", "HR", "Sales", "Eng"],
    "Score":    np.random.randint(60, 100, 8),
    "Revenue":  np.random.uniform(10_000, 100_000, 8).round(2),
    "Active":   [True, True, False, True, False, True, True, False],
    "Joined":   pd.date_range("2021-01-01", periods=8, freq="90D"),
})

# ── 1. st.dataframe ───────────────────────────────────────────
st.header("1. st.dataframe — Interactive Table")
st.markdown("""
`st.dataframe` renders an interactive, sortable, scrollable table.
Users can click column headers to sort, and select rows.
""")

st.dataframe(df, use_container_width=True)

# With height limit
st.subheader("With fixed height (scroll)")
st.dataframe(df, height=200, use_container_width=True)

# ── 2. st.dataframe with column_config ────────────────────────
st.header("2. Column Configuration — Richer Cells")
st.markdown("""
`st.column_config` lets you customise how each column looks:
progress bars, links, images, sparklines, etc.
""")

styled_df = df.copy()
styled_df["Progress"] = styled_df["Score"] / 100   # 0-1 for progress bar

st.dataframe(
    styled_df,
    column_config={
        "Score": st.column_config.NumberColumn(
            "Score 🎯",
            format="%d pts",
            min_value=0, max_value=100,
        ),
        "Revenue": st.column_config.NumberColumn(
            "Revenue 💰",
            format="$%.2f",
        ),
        "Progress": st.column_config.ProgressColumn(
            "Progress Bar",
            min_value=0, max_value=1,
            format="%.0f%%",
        ),
        "Active": st.column_config.CheckboxColumn("Active?"),
        "Joined": st.column_config.DateColumn("Join Date", format="MMM DD, YYYY"),
    },
    use_container_width=True,
    hide_index=True,
)

# ── 3. st.data_editor ─────────────────────────────────────────
st.header("3. st.data_editor — Editable Table")
st.markdown("""
`st.data_editor` lets users **edit** the table directly in the browser.
Returns the edited DataFrame.
""")

edited_df = st.data_editor(
    df[["Name", "Score", "Active"]],
    column_config={
        "Score": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Active": st.column_config.CheckboxColumn(),
    },
    num_rows="dynamic",   # allows adding/deleting rows
    use_container_width=True,
    hide_index=True,
)
st.write("Edited data:", edited_df)

# ── 4. st.table — Static Table ────────────────────────────────
st.header("4. st.table — Static (Non-Interactive) Table")
st.markdown("`st.table` renders a plain HTML table — no sorting, no scrolling.")
st.table(df[["Name", "Dept", "Score"]].head(4))

# ── 5. st.metric ─────────────────────────────────────────────
st.header("5. st.metric — KPI Cards")
st.markdown("""
`st.metric` shows a big KPI number with optional delta indicator.
The `delta_color` controls whether positive deltas are green or red.
""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue",  "$428,000", "+12.4%")
c2.metric("Active Users",   "8,340",    "+230")
c3.metric("Avg Score",      f"{df['Score'].mean():.1f}", "-2.1")
c4.metric("Churn Rate",     "3.8%",     "+0.3%", delta_color="inverse")

# ── 6. st.json ───────────────────────────────────────────────
st.header("6. st.json — Pretty-print JSON")

sample_json = {
    "user": {"id": 101, "name": "Atabi", "roles": ["admin", "viewer"]},
    "settings": {"theme": "dark", "notifications": True},
    "last_login": "2026-06-05T09:15:00Z",
}
st.json(sample_json, expanded=1)   # expanded=1 means open 1 level deep

# ── 7. Pandas Styling ─────────────────────────────────────────
st.header("7. Pandas Styling (Heatmap, Highlights)")
st.markdown("""
Pass a styled DataFrame (`.style`) to `st.dataframe` for
colour-coded cells, gradient fills, and more.
""")

numeric_df = df[["Name", "Score", "Revenue"]].set_index("Name")

styled = (
    numeric_df.style
    .background_gradient(subset=["Score"], cmap="RdYlGn")
    .format({"Revenue": "${:,.0f}"})
    .highlight_max(subset=["Score"], color="lightgreen")
    .highlight_min(subset=["Score"], color="salmon")
)

st.dataframe(styled, use_container_width=True)

# ── 8. Filtering + Display Pattern ───────────────────────────
st.header("8. Filter → Display Pattern")
st.markdown("Common pattern: sidebar filter → main area shows filtered DataFrame.")

dept_filter = st.multiselect("Filter by Department", options=df["Dept"].unique(),
                              default=df["Dept"].unique())
filtered = df[df["Dept"].isin(dept_filter)]

st.write(f"Showing **{len(filtered)}** of **{len(df)}** rows")
st.dataframe(filtered, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Load any CSV file into a DataFrame and display it with `st.dataframe`.
2. Add `column_config` to format a currency column with `$` prefix.
3. Use `st.data_editor` to make a simple to-do list (columns: Task, Done?).
4. Display 4 `st.metric` cards for a made-up sales report (Revenue, Orders, Avg Order Value, Returns).
5. Apply `.background_gradient` styling to a numeric DataFrame column.
""")
