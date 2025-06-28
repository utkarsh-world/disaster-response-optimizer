# 03_streamlit_dashboard.py
# -------------------------------------------------------------
# Streamlit dashboard for the “Disaster Response Optimizer” project
# -------------------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# Page setup
# -------------------------------------------------------------
st.set_page_config(page_title="Disaster Response Optimizer",
                   layout="wide",
                   page_icon="🌊")

st.title("🌊 Disaster Response Optimizer")
st.markdown(
    "Explore 50 + years of Indian flood data to spot patterns in frequency, "
    "location and severity.  \n"
    "_Built by Utkarsh Sharma as part of my METI Japan Internship prep._"
)

# -------------------------------------------------------------
# Load data
# -------------------------------------------------------------
DATA_PATH = "data/clean/flood_cleaned.csv"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["year"] = (
        pd.to_datetime(df["start_date"], errors="coerce")
        .dt.year
        .astype("Int64")             # keep as nullable int
    )
    return df.dropna(subset=["year", "state"])

df = load_data(DATA_PATH)

# -------------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------------
st.sidebar.header("🧰 Filters")

# Year slider
years = df["year"].dropna().astype(int)
min_year, max_year = int(years.min()), int(years.max())

year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# State multiselect
state_options = sorted(df["state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "Select states (optional)",
    options=state_options,
    default=state_options    # all selected by default
)

# Apply filters
filtered_df = df[
    (df["year"] >= year_range[0])
    & (df["year"] <= year_range[1])
    & df["state"].isin(selected_states)
]

st.sidebar.write(f"🔍 **Filtered rows:** {filtered_df.shape[0]}")

# -------------------------------------------------------------
# Data preview (optional)
# -------------------------------------------------------------
with st.expander("🔎 Preview filtered data", expanded=False):
    st.dataframe(filtered_df.head())

# -------------------------------------------------------------
# Flood events per year (line chart)
# -------------------------------------------------------------
st.subheader("📈 Flood Events per Year")

year_counts = (
    filtered_df["year"]
    .value_counts()
    .sort_index()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
year_counts.plot(ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Events")
ax1.set_title("Number of Flood Events per Year")
ax1.grid(alpha=0.3, linestyle="--")
st.pyplot(fig1)

# -------------------------------------------------------------
# Top 10 flood‑prone states (bar chart)
# -------------------------------------------------------------
st.subheader("🏆 Top 10 Most Flood‑Prone States")

top_states = (
    filtered_df["state"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
top_states.plot(kind="barh", ax=ax2, color="steelblue")
ax2.set_xlabel("Number of Events")
ax2.set_ylabel("State")
ax2.set_title("Top 10 States by Number of Flood Events")
st.pyplot(fig2)

# ---------------- Monthly seasonality ----------------
st.subheader("📅 Flood Seasonality (Events per Month)")

filtered_df['month'] = pd.to_datetime(filtered_df['start_date']).dt.month

month_order = range(1, 13)
monthly_counts = (
    filtered_df['month']
    .value_counts()
    .reindex(month_order, fill_value=0)
)

fig_month, ax_month = plt.subplots(figsize=(10, 4))
monthly_counts.plot(kind="bar", ax=ax_month, color="teal")
ax_month.set_xlabel("Month (1 = Jan … 12 = Dec)")
ax_month.set_ylabel("Events")
ax_month.set_title("Flood Events by Month")
st.pyplot(fig_month)

# -------------------------------------------------------------
# Footer
# -------------------------------------------------------------
st.markdown("---")
st.markdown(
    "Data source: Public flood records (1967‑2023)  \n"
    "Dashboard author: **Utkarsh Sharma**"
)
# Toggle to hide extreme floods
hide_outliers = st.sidebar.checkbox(
    "Hide extreme floods (duration > 60 days OR fatalities > 300)", value=False)

# Apply outlier filter
if hide_outliers:
    filtered_df = filtered_df[
        (filtered_df["durationdays"] <= 60) &
        (filtered_df["human_fatality_filled"] <= 300)
    ]
      
import io
csv_buffer = io.BytesIO()
filtered_df.to_csv(csv_buffer, index=False)
st.sidebar.download_button(
    label="⬇️ Download filtered CSV",
    data=csv_buffer.getvalue(),
    file_name="filtered_flood_data.csv",
    mime="text/csv"
)


