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
Copy
Edit
python -m venv venv
```
Activate the environment:
Linux/Mac:

```bash
Copy
Edit
source venv/bin/activate
```