# 03_streamlit_dashboard.py
# -----------------------------------------------------------
# Streamlit dashboard (English + Japanese labels, no map)
# -----------------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ---------- Page configuration ----------
st.set_page_config(
    page_title="Disaster Response Optimizer",
    page_icon="🌊",
    layout="wide"
)

# ---------- Load data ----------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["year"] = df["start_date"].dt.year
    df["human_fatality_filled"] = df["human_fatality"].fillna(0).astype(int)
    df["durationdays"] = df["durationdays"].fillna(0)
    return df.dropna(subset=["year", "state"])

DATA_PATH = "data/clean/flood_cleaned.csv"
df = load_data(DATA_PATH)

# ---------- Sidebar filters ----------
st.sidebar.header("🧰 Filters（フィルター）")

# Year range slider
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Select Year Range（年を選択）",
    min_year, max_year,
    (min_year, max_year),
    step=1
)

# State multiselect
state_options = sorted(df["state"].unique())
selected_states = st.sidebar.multiselect(
    "Select States（州を選択）",
    options=state_options,
    default=state_options
)

# Apply filters
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["state"].isin(selected_states))
]

st.sidebar.write(f"🔍 **Filtered rows（行数）:** {filtered_df.shape[0]}")

# Download CSV
csv_buffer = io.BytesIO()
filtered_df.to_csv(csv_buffer, index=False)
st.sidebar.download_button(
    label="⬇️ Download filtered CSV（CSVをダウンロード）",
    data=csv_buffer.getvalue(),
    file_name="filtered_flood_data.csv",
    mime="text/csv"
)

# ---------- Main title ----------
st.title("🌊 Disaster Response Optimizer")
st.markdown("Flood Insights for India（インド洪水データの洞察）")

# ---------- Flood events per year ----------
st.subheader("📈 Flood Events per Year（年別洪水件数）")
year_counts = filtered_df["year"].value_counts().sort_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
year_counts.plot(ax=ax1, color="steelblue")
ax1.set_xlabel("Year（年）")
ax1.set_ylabel("Events（件数）")
ax1.grid(alpha=0.3, linestyle="--")
st.pyplot(fig1)

# ---------- Top‑10 states ----------
st.subheader("🏆 Top 10 Flood‑Prone States（洪水が多い州）")
top_states = (
    filtered_df["state"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
)
fig2, ax2 = plt.subplots(figsize=(8, 4))
top_states.plot(kind="barh", ax=ax2, color="teal")
ax2.set_xlabel("Events（件数）")
ax2.set_ylabel("State（州）")
st.pyplot(fig2)

# ---------- Deadliest floods table ----------
st.subheader("💀 Deadliest Floods（最も致命的な洪水）")
deadliest = (
    filtered_df[["year", "state", "durationdays", "human_fatality_filled"]]
    .rename(columns={
        "year": "Year（年）",
        "state": "State（州）",
        "durationdays": "Duration (days)（継続日数）",
        "human_fatality_filled": "Fatalities（死亡者数）"
    })
    .sort_values("Fatalities（死亡者数）", ascending=False)
    .head(15)
)
st.dataframe(deadliest, use_container_width=True)

# ---------- Footer ----------
st.markdown("---  \nData source: Public flood datasets  \n© 2025 Utkarsh Sharma")
