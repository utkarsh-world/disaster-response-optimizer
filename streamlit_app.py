# streamlit_app.py
# ============================================================
# Disaster Response Optimizer – India 🇮🇳 & Japan 🇯🇵 Dashboard
# English + 日本語 labels
# ============================================================

import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib as mpl
from relief_optimizer import allocate_relief

# ── Suppress font spam ───────────────────────────────────────
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
mpl.font_manager._log.setLevel("ERROR")

# ---------- Page config ----------
st.set_page_config(
    page_title="Disaster Response Optimizer",
    page_icon=" ",
    layout="wide"
)

st.title("Disaster Response Optimizer")
st.markdown("Flood data insights for **India** and **Japan** (1967–2023)")

# ============================================================
# Sidebar
# ============================================================
st.sidebar.header("🧰 Filters（フィルター）")

# View-mode selector
view_mode = st.sidebar.radio(
    "View Mode / 表示モード",
    ("Single Country / 単一国", "Compare India vs Japan / 比較"),
    index=0
)

# ------------------------------------------------------------
# SINGLE-COUNTRY MODE
# ------------------------------------------------------------
if view_mode.startswith("Single"):

    # Country selector
    country = st.sidebar.radio(
        "Country / 国を選択",
        ("India", "Japan"),
        horizontal=True
    )

    # Cached data loader
    @st.cache_data
    def load_data(selected_country: str) -> pd.DataFrame:
        if selected_country == "India":
            path = "data/clean/flood_cleaned.csv"
        else:
            path = "data/clean/japan_floods_cleaned.csv"

        df = pd.read_csv(path)

        # Numeric cleanup for Japan
        if selected_country == "Japan" and "human_fatality" in df.columns:
            df["human_fatality"] = (
                pd.to_numeric(df["human_fatality"], errors="coerce")
                  .fillna(0).astype(int)
            )

        if "year" not in df.columns and "start_date" in df.columns:
            df["year"] = pd.to_datetime(df["start_date"], errors="coerce").dt.year

        return df

    df = load_data(country)

    # Sidebar filters: year range & states/prefectures
    years = df["year"].dropna().astype(int)
    min_y, max_y = int(years.min()), int(years.max())

    year_range = st.sidebar.slider(
        "Year Range（年を選択）",
        min_y, max_y,
        (min_y, max_y),
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

    st.sidebar.write(f"🔍 **Rows / 行数:** {filtered_df.shape[0]}")

    # CSV download
    st.sidebar.download_button(
        "⬇️ CSV ダウンロード",
        data=filtered_df.to_csv(index=False).encode(),
        file_name=f"{country.lower()}_floods_filtered.csv",
        mime="text/csv"
    )

    # ---------- Charts (single-country) ----------
    st.subheader(f"📈 Flood Events per Year / 年別洪水件数 – {country}")
    yearly_counts = (
        filtered_df["year"]
        .value_counts()
        .sort_index()
    )

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    yearly_counts.plot(ax=ax1, color="steelblue")
    ax1.set_xlabel("Year / 年")
    ax1.set_ylabel("Events / 件数")
    ax1.grid(alpha=0.3, linestyle="--")
    st.pyplot(fig1)

    st.subheader(f"🏆 Top 10 Regions / 洪水が多い地域 – {country}")
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

    # ----------------- Relief Optimizer (India only) -----------------
    if country == "India":
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚑 Relief Optimizer（救援最適化）")

        enable_optimizer = st.sidebar.checkbox("Run Relief Optimizer / 救援割当を実行", value=False)

        if enable_optimizer:
            optimizer_years = st.sidebar.slider(
                "Select Year Range / 年を選択",
                min_y, max_y,
                (max_y - 4, max_y),
                step=1
            )
            total_resources = st.sidebar.number_input(
                "Total Relief Units（総資源数）",
                min_value=100,
                max_value=20000,
                value=7800,
                step=100
            )

            st.subheader("🚑 Relief Allocation Results / 救援割当結果")

            allocation = allocate_relief(df, optimizer_years[0], optimizer_years[1], total_resources)

            if allocation.empty:
                st.warning("⚠️ No data available for the selected range / データがありません")
            else:
                total_need = allocation["need_units"].sum()
                total_allocated = allocation["allocated_units"].sum()
                overall_coverage = round(total_allocated / total_need * 100, 1) if total_need > 0 else 0

                # Summary bilingual
                st.markdown(f"""
                **Years / 年:** {optimizer_years[0]} – {optimizer_years[1]}  
                **Total Need（必要資源数）:** {total_need}  
                **Allocated（配分済み）:** {total_allocated}  
                **Coverage（カバー率）:** {overall_coverage}%
                """)

                st.write("### 🔻 Lowest Coverage States / カバー率が低い地域")
                st.dataframe(allocation.head(10), use_container_width=True)

                # Download button
                csv_path = f"relief_allocation_{optimizer_years[0]}_{optimizer_years[1]}.csv"
                st.download_button(
                    "⬇️ Download Allocation CSV / 割当CSVダウンロード",
                    data=allocation.to_csv(index=False).encode(),
                    file_name=csv_path,
                    mime="text/csv"
                )

                # Bar chart allocation vs need
                st.write("### 📉 Allocation vs Need / 割当と必要度の比較")
                top_alloc = allocation.sort_values("need_units", ascending=False).head(15)
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(top_alloc["state"], top_alloc["need_units"], label="Need / 必要", alpha=0.7, color="indianred")
                ax.bar(top_alloc["state"], top_alloc["allocated_units"], label="Allocated / 割当", alpha=0.7, color="steelblue")
                ax.set_xlabel("State / 州")
                ax.set_ylabel("Units / ユニット")
                ax.set_title("Relief Allocation vs Need / 救援配分と必要度")
                ax.legend()
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)

    st.stop()   # prevent Compare code from running below

# ------------------------------------------------------------
# COMPARE MODE (India vs Japan)
# ------------------------------------------------------------
# Load both datasets
df_india = pd.read_csv("data/clean/flood_cleaned.csv")
df_japan = pd.read_csv("data/clean/japan_floods_cleaned.csv")

df_india["country"] = "India"
df_japan["country"] = "Japan"

for df_tmp in (df_india, df_japan):
    if "year" not in df_tmp.columns:
        df_tmp["year"] = pd.to_datetime(df_tmp["start_date"], errors="coerce").dt.year
df_japan["human_fatality"] = (
    pd.to_numeric(df_japan["human_fatality"], errors="coerce")
      .fillna(0).astype(int)
)

df_all = pd.concat([df_india, df_japan], ignore_index=True)

# ---------- Fatalities over time ----------
st.subheader("Annual Flood Fatalities (India vs Japan) / 年別洪水死亡者数（比較）")

yearly = (
    df_all.groupby(["year", "country"])["human_fatality"]
          .sum().reset_index()
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.lineplot(
    data=yearly,
    x="year",
    y="human_fatality",
    hue="country",
    marker="o",
    errorbar=None,
    ax=ax3
)
ax3.set_xlabel("Year / 年")
ax3.set_ylabel("Total Fatalities / 死亡者数")
ax3.grid(alpha=0.3, linestyle="--")
st.pyplot(fig3)

# ---------- Top 10 regions for each country ----------
st.subheader("Top 10 Flood-Prone Regions by Country / 国別上位10地域")

top_india = (
    df_india["state"].value_counts().head(10).sort_values(ascending=True)
)
top_japan = (
    df_japan["state"].value_counts().head(10).sort_values(ascending=True)
)

fig4, (ax4, ax5) = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
top_india.plot(kind="barh", ax=ax4, color="steelblue")
ax4.set_title("India")
ax4.set_xlabel("Events / 件数")
ax4.set_ylabel("State")

top_japan.plot(kind="barh", ax=ax5, color="indianred")
ax5.set_title("Japan")
ax5.set_xlabel("Events / 件数")
ax5.set_ylabel("Prefecture")

plt.tight_layout()
st.pyplot(fig4)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("---")
st.markdown("Data sources: India Flood Inventory v3, EM-DAT Japan subset  |  © 2025 Utkarsh Sharma")
