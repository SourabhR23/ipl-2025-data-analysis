# 🏏 IPL 2025 Data Analysis Project

Welcome to the **IPL 2025 Data Analysis** project!  
This repository automates **daily match data fetching** from CricAPI, processes the JSON data into structured **DataFrames**, and enables deep **EDA (Exploratory Data Analysis)** on IPL 2025 matches.

---

## 📋 Project Overview

- ✅ Fetches daily IPL 2025 match scorecards (up to 10 matches/day limit).
- ✅ Parses match JSONs into structured CSV files: Matches, Innings, Batting, Bowling, Fielding, Extras.
- ✅ Data ready for analysis, visualization, and reporting.
- ✅ Secure handling of API keys using `.env` file.
- ✅ Clean, modular folder structure following real-world best practices.

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **Pandas** (data manipulation)
- **Requests** (API communication)
- **dotenv** (secure API key management)
- **Matplotlib** and **Seaborn** (for EDA visualization - coming soon!)

---

## 📂 Project Structure

```plaintext
ipl-2025-data-analysis/
├── .env                 # (Your API Key, not uploaded)
├── .gitignore           # (Ignore secrets, cache, checkpoints)
├── README.md
├── requirements.txt
│
├── data/
│   ├── IPL_2025_Match_List.csv
│   ├── parsed_csv/
│       ├── matches_df.csv
│       ├── innings_df.csv
│       ├── batting_df.csv
│       ├── bowling_df.csv
│       ├── fielding_df.csv
│       ├── extras_df.csv
│
├── scripts/
│   ├── fetch_series_info.py         # Fetch full match list
│   ├── fetch_and_parse_daily.py     # Daily fetch + parse latest matches
│
├── notebooks/
│   ├── eda_ipl_2025.ipynb            # (Coming soon: Full visual EDA)
```

---

## ⚡ Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
```
Activate the environment:
Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install project dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a .env file in the project root.
Add your API key like this:

```plaintext
API_KEY=your_actual_api_key_here
✅ .env file should NOT be pushed to GitHub (make sure .gitignore contains .env).
```

📈 How to Use
Fetch Data
```bash
python scripts/fetch_data.py
```

Parse and Process Data
```bash
python scripts/parse_data.py
```

🎯 Features
📈 Automated data extraction from APIs.
🗂 Structured and clean DataFrames storage.
📊 Exploratory Data Analysis (EDA) on real-world datasets.
🛠 Modular, scalable, and secure coding practices.

🚀 Upcoming Work
🚀 Build interactive dashboards using Streamlit or Dash.
🔥 Perform Machine Learning modeling on player performances (optional).
🤖 Automate daily data pulls using GitHub Actions or Cron Jobs (future scope).


