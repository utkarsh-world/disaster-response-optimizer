![Dashboard Preview](banner.png)
# 🌊 Disaster Response Optimizer (India Flood Analysis)

Hi! I'm Utkarsh Sharma, and this is a data analysis project I built to explore real-world flood events across India.  
The goal is to understand patterns in natural disasters so governments and communities can respond better in the future.

This project was built using:
- 🐍 Python (pandas, matplotlib, seaborn)
- 📊 Jupyter Notebooks (for analysis)
- 🖥️ VS Code & GitHub (version control)
- 📁 Publicly available flood data

---

## 🌏 Supported Datasets

| Country | Years | Source | Clean file |
|---------|-------|--------|-----------|
| 🇮🇳 **India** | 1967 – 2023 | India Flood Inventory v3 | `data/clean/flood_cleaned.csv` |
| 🇯🇵 **Japan** | 1967 – 2023 | EM‑DAT “Flood” subset | `data/clean/japan_floods_cleaned.csv` |

### What’s new (July 2025)
- **🔄 Country toggle** in the Streamlit app (India / Japan)
- New notebook `04_eda_japan.ipynb` for Japan EDA
- Dashboard titles & filters update automatically when you switch countries

> **Live Demo:**  
> https://utkarsh-world-disaster-response-optimizer.streamlit.app


## 🧪 What This Project Does

✔️ Cleans real flood event data from India (1967–2023)  
✔️ Analyzes flood duration, human fatalities, and state-wise trends  
✔️ Visualizes:
- Top 10 most flood-prone states  
- Year-by-year trend of events  
- Distributions of duration and death tolls  
✔️ Flags outliers (like extreme floods or high-fatality events)

Soon I’ll be turning this into an interactive dashboard using **Streamlit**!

---

## 📂 Folder Structure

```bash
disaster-response-optimizer/
├── data/
│   ├── raw/
│   │   ├── india_floods_raw.csv
│   │   └── japan_floods_raw.csv
│   └── clean/
│       ├── flood_cleaned.csv              # India 1967‑2023
│       └── japan_floods_cleaned.csv       # Japan 1967‑2023
│
├── notebooks/
│   ├── 01_data_loading.ipynb              # India raw load
│   ├── 02_eda_india.ipynb                 # India EDA
│   ├── 03_japan_data_loading.ipynb        # Japan raw load
│   └── 04_eda_japan.ipynb                 # Japan EDA
│
├── streamlit_app.py                       # Unified bilingual dashboard
├── requirements.txt
├── banner.png
├── .gitignore
└── README.md