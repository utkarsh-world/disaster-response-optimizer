![Dashboard Preview](banner.png)

# 🌊 Disaster Response Optimizer（インド・日本 洪水ダッシュボード）

> **Live demo:** <https://your‑streamlit‑cloud‑url>  
> **Author:** Utkarsh Sharma &nbsp;|&nbsp; 🇮🇳 India &nbsp;•&nbsp; 🇯🇵 Japan &nbsp;|&nbsp; 2025

Interactive, bilingual (English + 日本語) dashboard that visualises **57 years of flood events** across India and Japan (1967‑2023).  
Built for my portfolio and the METI Japan Internship program to demonstrate real‑world data cleaning, analysis, and cloud deployment.

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **Dual datasets** | India Flood Inventory v3 + EM‑DAT Japan subset |
| **Bilingual UI** | English labels with Japanese subtitles |
| **Interactive filters** | Country, year range, state/prefecture |
| **Single vs Compare view** | Toggle between per‑country analysis and India‑vs‑Japan comparison |
| **Charts** | Yearly flood counts, fatalities, top‑10 regions, deadliest events |
| **CSV export** | Download filtered data with one click |
| **Live on Streamlit Cloud** | Zero‑setup public URL |

---

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/utkarsh-world/disaster-response-optimizer.git
cd disaster-response-optimizer
pip install -r requirements.txt

# Run locally
streamlit run streamlit_app.py


## 📂 Folder Structure
disaster-response-optimizer/
├── data/
│   ├── raw/                          # Original CSV / XLSX
│   └── clean/                        # Cleaned datasets
│       ├── flood_cleaned.csv         # India
│       └── japan_floods_cleaned.csv  # Japan
├── notebooks/                        # Jupyter analysis
│   ├── 01_data_loading.ipynb         # India load & clean
│   ├── 02_eda_india.ipynb            # India EDA
│   ├── 03_japan_data_loading.ipynb   # Japan load & clean
│   └── 04_eda_japan.ipynb            # Japan EDA
├── streamlit_app.py                  # Unified bilingual dashboard
├── requirements.txt                  # Python deps
├── banner.png                        # README banner
├── LICENSE                           # MIT (see below)
└── README.md


## 🧑‍💻 Tech Stack
Python 3.10
pandas, numpy – data wrangling
matplotlib, seaborn – visualisation
Streamlit – interactive web app
GitHub + Streamlit Cloud – CI/CD & hosting


## 🔍 Data Sources
| Country | Years     | Source                   | Licence |
| ------- | --------- | ------------------------ | ------- |
| India   | 1967‑2023 | India Flood Inventory v3 | CC‑BY   |
| Japan   | 1967‑2023 | EM‑DAT “Flood” subset    | CC‑BY   |


⭐ Acknowledgements-
India Flood Inventory team for open data
EM‑DAT team for Japan disaster records
Streamlit community for the awesome library
METI Japan Internship for the motivation


🤝 Contributing-
Pull requests are welcome! For major changes, open an issue first to discuss what you would like to change.


