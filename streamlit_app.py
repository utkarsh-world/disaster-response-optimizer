# streamlit_app.py
# ============================================================
# Disaster Response Optimizer – India 🇮🇳 & Japan 🇯🇵
# Bilingual dashboard (English + 日本語)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import warnings

# Hide glyph‑missing warnings if Japanese font isn’t installed
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Disaster Response Optimizer",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 Disaster Response Optimizer")
st.markdown("_Interactive flood‑data dashboard for India and Japan, 1967‑2023_")

# ------------------------------------------------------------
# Sidebar header & country selector
# ------------------------------------------------------------
st.sidebar.header("🧰 Filters（フィルター）")

country = st.sidebar.radio(
    "Country / 国を選択",
    ("India", "Japan"),
    horizontal=True
)

# ------------------------------------------------------------
# Cached data loader (country‑aware)
# ------------------------------------------------------------
@st.cache_data
def load_data(selected_country: str) -> pd.DataFrame:
    """Return cleaned flood dataframe for India or Japan."""
    if selected_country == "India":
        path = "data/clean/flood_cleaned.csv"
    else:
        path = "data/clean/japan_floods_cleaned.csv"

    df = pd.read_csv(path)

    # Ensure numeric types for Japan file
    if selected_country == "Japan":
        df["human_fatality"] = (
        pd.to_numeric(df["human_fatality"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
    
    if "durationdays" not in df.columns:
        df["durationdays"] = 0
    if "human_fatality_filled" not in df.columns:
        df["human_fatality_filled"] = df["human_fatality"]

    # Ensure 'year' column exists
    if "year" not in df.columns and "start_date" in df.columns:
        df["year"] = pd.to_datetime(df["start_date"], errors="coerce").dt.year

    return df

df = load_data(country)

# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
years = df["year"].dropna().astype(int)
min_year, max_year = int(years.min()), int(years.max())

year_range = st.sidebar.slider(
    "Year Range（年を選択）",
    min_year, max_year,
    (min_year, max_year),
    step=1
)

states = sorted(df["state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "States / Prefectures（州 / 都道府県）",
    options=states,
    default=states
)

# Apply filters
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    df["state"].isin(selected_states)
]

st.sidebar.write(f"🔍 **Filtered rows / 行数:** {filtered_df.shape[0]}")

# CSV download of current view
csv_bytes = io.BytesIO()
filtered_df.to_csv(csv_bytes, index=False)
st.sidebar.download_button(
    label="⬇️ Download CSV（CSVをダウンロード）",
    data=csv_bytes.getvalue(),
    file_name=f"{country.lower()}_floods_filtered.csv",
    mime="text/csv"
)

# ------------------------------------------------------------
# Flood Events per Year
# ------------------------------------------------------------
st.subheader(f"📈 Flood Events per Year / 年別洪水件数 – {country}")
year_counts = (
    filtered_df["year"]
    .value_counts()
    .sort_index()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
year_counts.plot(ax=ax1, color="steelblue")
ax1.set_xlabel("Year / 年")
ax1.set_ylabel("Events / 件数")
ax1.grid(alpha=0.3, linestyle="--")
st.pyplot(fig1)

# ------------------------------------------------------------
# Top‑10 Regions
# ------------------------------------------------------------
st.subheader(f"🏆 Top 10 Regions / 洪水が多い地域 – {country}")
top_regions = (
    filtered_df["state"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
top_regions.plot(kind="barh", ax=ax2, color="teal")
ax2.set_xlabel("Events / 件数")
ax2.set_ylabel("State / Prefecture")
st.pyplot(fig2)

# ------------------------------------------------------------
# Deadliest Floods table
# ------------------------------------------------------------
st.subheader(f"💀 Deadliest Flood Events / 重大洪水 – {country}")

if "human_fatality" in filtered_df.columns:
    deadliest = (
        filtered_df[["year", "state", "start_date", "human_fatality"]]
        .sort_values("human_fatality", ascending=False)
        .head(15)
        .reset_index(drop=True)
        .rename(columns={
            "year": "Year / 年",
            "state": "State / Prefecture",
            "start_date": "Start Date",
            "human_fatality": "Fatalities / 死者数"
        })
    )
    st.dataframe(deadliest, use_container_width=True)
else:
    st.info("Fatality data not available for this dataset.")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("---")
st.markdown("Data sources: India Flood Inventory v3, EM‑DAT Japan subset  |  © 2025 Utkarsh Sharma")
