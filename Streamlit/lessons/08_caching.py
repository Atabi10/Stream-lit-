# ============================================================
# LESSON 08 — Caching & Performance
# Run: streamlit run lessons/08_caching.py
# ============================================================
#
# KEY CONCEPT: The Caching Problem
# ----------------------------------
# Streamlit reruns your script on every interaction.
# Without caching, EVERY interaction re-fetches data, re-trains
# models, re-reads files — which is slow and wasteful.
#
# Two decorators solve this:
#
#  @st.cache_data    — for data (DataFrames, lists, dicts, JSON)
#                      Returns a COPY each time (safe)
#
#  @st.cache_resource — for shared resources (DB connections,
#                       ML models, API clients)
#                       Returns the SAME object each time (shared)

import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Lesson 08 · Caching", page_icon="⚡")
st.title("⚡ Lesson 08: Caching & Performance")

# ── 1. The Problem Without Caching ────────────────────────────
st.header("1. The Problem — Expensive Function Without Cache")
st.markdown("Click any widget on this page and watch how long the uncached function takes.")

def slow_load_data_UNCACHED(n_rows: int) -> pd.DataFrame:
    """Simulates an expensive database query — 2 seconds every rerun."""
    time.sleep(2)   # simulate network/db latency
    return pd.DataFrame({
        "id":    range(n_rows),
        "value": np.random.randn(n_rows),
    })

if st.button("Run uncached (slow) — 2 sec per click"):
    start = time.time()
    df = slow_load_data_UNCACHED(1000)
    elapsed = time.time() - start
    st.warning(f"Took **{elapsed:.2f}s** — imagine this on every widget interaction!")

# ── 2. @st.cache_data ─────────────────────────────────────────
st.header("2. @st.cache_data — Cache Data Objects")
st.markdown("""
Add `@st.cache_data` and the function runs only when its **arguments change**.
Streamlit hashes the arguments as a cache key.
""")

@st.cache_data
def load_data(n_rows: int) -> pd.DataFrame:
    """
    Called with the same n_rows → returns cached result instantly.
    Called with a new n_rows → re-executes and caches the new result.
    """
    time.sleep(2)   # same expensive operation
    return pd.DataFrame({
        "id":    range(n_rows),
        "value": np.random.randn(n_rows),
        "label": np.random.choice(["A", "B", "C"], n_rows),
    })

n_rows = st.slider("Number of rows", 100, 5000, 1000, step=100,
                    help="Change this to trigger a cache miss.")

start = time.time()
df = load_data(n_rows)
elapsed = time.time() - start

if elapsed > 0.1:
    st.warning(f"⏳ Cache MISS — took {elapsed:.2f}s (first call with n_rows={n_rows})")
else:
    st.success(f"⚡ Cache HIT — took {elapsed:.4f}s (instant!)")

st.dataframe(df.head(5), use_container_width=True)

# ── 3. TTL (Time-to-live) ─────────────────────────────────────
st.header("3. TTL — Auto-expire Cache")
st.markdown("""
`ttl` (time-to-live) expires the cache after N seconds.
Use it for data that changes over time (live feeds, APIs).

```python
@st.cache_data(ttl=600)      # expire after 10 minutes
def fetch_live_prices():
    return requests.get("https://api.example.com/prices").json()

@st.cache_data(ttl="1h")     # human-readable: 1 hour
def fetch_daily_report():
    ...
```
""")

@st.cache_data(ttl=10)   # cache expires after 10 seconds
def get_timestamped_data():
    return {"fetched_at": time.strftime("%H:%M:%S"), "value": np.random.randint(100)}

data = get_timestamped_data()
st.info(f"Data fetched at **{data['fetched_at']}** — value: {data['value']}")
st.caption("This refreshes every 10 seconds (or on a cache miss). Rerun the app after 10s to see.")

# ── 4. max_entries ─────────────────────────────────────────────
st.header("4. max_entries — Limit Cache Size")
st.markdown("""
`max_entries` caps the number of cached argument combinations.
When the limit is reached, the oldest entry is evicted (LRU).

```python
@st.cache_data(max_entries=20)
def load_page(page_number: int):
    ...
```
Useful when users can pass many different values (page numbers, IDs, etc.)
to avoid unbounded memory growth.
""")

# ── 5. @st.cache_resource ─────────────────────────────────────
st.header("5. @st.cache_resource — Shared Global Resources")
st.markdown("""
Use `@st.cache_resource` for objects that:
- Are expensive to initialise (ML models, DB connections)
- Should be **shared** across all users and all reruns
- Should NOT be copied (connections can't be pickled)

The difference from `@st.cache_data`:
| | cache_data | cache_resource |
|---|---|---|
| Returns | A **copy** | The **same** object |
| Use for | Data (DataFrames, lists) | Models, connections, clients |
| Thread safe | Yes (copy) | Requires care |
""")

@st.cache_resource
def get_model():
    """Simulates loading a heavy ML model — runs ONCE per app lifetime."""
    st.write("🔄 Loading model... (you'll only see this once)")
    time.sleep(2)
    return {"model_type": "RandomForest", "n_estimators": 100, "loaded_at": time.time()}

model = get_model()
st.success(f"Model ready: `{model['model_type']}` (loaded at t={model['loaded_at']:.0f})")
st.info("Rerun this app multiple times — the model loads only ONCE.")

# ── 6. cache_data with show_spinner ───────────────────────────
st.header("6. Spinner Control")
st.markdown("By default, Streamlit shows '⚡ Running...' during cache misses. You can customise it.")

@st.cache_data(show_spinner="🔄 Fetching data from database...")
def fetch_with_custom_spinner(n: int):
    time.sleep(1.5)
    return pd.DataFrame({"x": range(n), "y": np.random.randn(n)})

if st.button("Fetch with custom spinner"):
    data2 = fetch_with_custom_spinner(50)
    st.line_chart(data2.set_index("x"))

# ── 7. Clearing the Cache ──────────────────────────────────────
st.header("7. Clearing the Cache")
st.markdown("""
Three ways to clear the cache:
- **From code**: `load_data.clear()` — clears a specific function's cache
- **Globally**: `st.cache_data.clear()` or `st.cache_resource.clear()`
- **From UI**: ☰ menu → "Clear cache"
""")

col1, col2 = st.columns(2)
if col1.button("Clear load_data cache"):
    load_data.clear()
    st.warning("Cache cleared! Next call will be slow again.")

if col2.button("Clear ALL cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.warning("All caches cleared!")

# ── 8. When to Use What ───────────────────────────────────────
st.header("8. Quick Reference — When to Cache")

st.markdown("""
| Situation | Decorator | Example |
|-----------|-----------|---------|
| CSV / DB query | `@st.cache_data` | `pd.read_csv(...)` |
| API response | `@st.cache_data(ttl=300)` | `requests.get(...)` |
| ML model load | `@st.cache_resource` | `joblib.load("model.pkl")` |
| DB connection | `@st.cache_resource` | `psycopg2.connect(...)` |
| Pure computation | `@st.cache_data` | `df.groupby(...).agg(...)` |
| File read | `@st.cache_data` | `open("big_file.json")` |

**Rule of thumb**: if it's serialisable data → `cache_data`. If it's a
connection or model you want to share → `cache_resource`.
""")

# ─────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🏋️ Exercises")
st.markdown("""
1. Wrap a `pd.read_csv(url)` call in `@st.cache_data(ttl="10m")` and verify it only fetches once.
2. Simulate an ML model load with `@st.cache_resource` and a 3-second sleep. Reload the app and
   confirm it only sleeps once.
3. Create a `@st.cache_data` function that takes `(year, month)` as args. Show that changing
   year triggers a miss, but re-selecting the same year/month is a hit.
4. Add a "Refresh data" button that calls `.clear()` on your cached function.
""")
