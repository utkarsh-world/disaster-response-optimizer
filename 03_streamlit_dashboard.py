import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# --- Set page config ---
st.set_page_config(
    page_title="Disaster Response Optimizer",
    page_icon="🌊",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/clean/flood_cleaned.csv')
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['year'] = df['start_date'].dt.year
    df['human_fatality_filled'] = df['human_fatality'].fillna(0).astype(int)
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("📅 Filter by Year Range（年の範囲で絞り込み）")
min_year, max_year = int(df['year'].min()), int(df['year'].max())
year_range = st.sidebar.slider("Select Year Range（年を選択してください）", min_year, max_year, (2010, 2020))

st.sidebar.subheader("📍 Select State(s)（州を選択）")
states = df['state'].dropna().unique().tolist()
selected_states = st.sidebar.multiselect("Choose states（複数選択可能）", states, default=states)

# --- Filter the dataframe ---
filtered_df = df[
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1]) &
    (df['state'].isin(selected_states))
]

# --- Main layout ---
st.title("🌊 Disaster Response Optimizer")
st.markdown("Visualizing Flood Disasters in India（インドの洪水災害の可視化）")

# --- Flood Events per Year ---
st.subheader("📈 Flood Events Per Year（年別洪水件数）")
yearly_counts = filtered_df.groupby('year').size()
fig, ax = plt.subplots()
yearly_counts.plot(kind='bar', ax=ax)
ax.set_xlabel("Year（年）")
ax.set_ylabel("Number of Events（件数）")
st.pyplot(fig)

# --- Most Deadly Floods Table ---
st.subheader("💀 Most Deadly Floods（最も致命的な洪水）")
top_deaths = filtered_df.sort_values(by='human_fatality_filled', ascending=False).head(10)
st.dataframe(top_deaths[['year', 'state', 'durationdays', 'human_fatality_filled']].rename(columns={
    'year': 'Year（年）',
    'state': 'State（州）',
    'durationdays': 'Duration (days)（継続日数）',
    'human_fatality_filled': 'Fatalities（死亡者数）'
}))

# --- Map of Events ---
st.subheader("🗺️ Flood Map（洪水マップ）")
map_data = filtered_df[['latitude', 'longitude']].dropna()
st.map(map_data)

# --- PyDeck advanced map (optional) ---
if not map_data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=map_data['latitude'].mean(),
            longitude=map_data['longitude'].mean(),
            zoom=4,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=map_data,
                get_position='[longitude, latitude]',
                radius=10000,
                elevation_scale=50,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    ))

# --- Download filtered data ---
st.download_button(
    label="📄 Download filtered data as CSV（CSVデータをダウンロード）",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_flood_data.csv',
    mime='text/csv',
)
