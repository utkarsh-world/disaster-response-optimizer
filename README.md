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



# 🌊 Disaster Response Optimizer 2.0

**Bilingual (English + 日本語)** — Flood analytics and resource allocation for India & Japan (1967–2023)

---

## 🔑 What’s new in 2.0 / 2.0 の新機能
- Modular allocation logic: `relief_optimizer.py` (single source of truth)  
- Bilingual reporting in the Streamlit UI and CSV exports (English + 日本語)  
- Cleaner Streamlit integration with new allocation visualization and CSV download

---

## 📂 Files / ファイル
- `streamlit_app.py` — Interactive bilingual dashboard (Streamlit)  
- `relief_optimizer.py` — Core allocation logic (functions used by CLI + Streamlit)  
- `relief_optimizer_test.py` — CLI tester to run allocation locally  
- `data/clean/...` — Cleaned datasets and generated allocations CSVs  
- `docs/Disaster_Response_Optimizer_Presentation.pdf` — Presentation (if present)

---

## ⚙️ How to run / 実行方法

### Local (dev)
```bash
# 1. create and activate venv (optional but recommended)
python -m venv .venv
.venv\Scripts\activate         # Windows PowerShell
# or: source .venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
