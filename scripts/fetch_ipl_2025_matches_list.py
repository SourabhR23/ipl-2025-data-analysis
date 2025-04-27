"""
IPL 2025 Series Info Fetcher

This script fetches IPL 2025 match data from CricAPI, processes it, and prepares it
for data analysis. API keys are securely managed using environment variables (.env).
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

# ========== Load Environment Variables ==========
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ========== Configuration ==========
SERIES_ID = "d5a498c8-7596-4b93-8ab0-e0efc3345312"
BASE_URL = "https://api.cricapi.com/v1"
SERIES_INFO_URL = f"{BASE_URL}/series_info"
TIMEOUT = 10  # seconds

# ========== Functions ==========

def fetch_series_info(api_key, series_id):
    """Fetch series information from CricAPI."""
    params = {"apikey": api_key, "id": series_id}
    try:
        response = requests.get(SERIES_INFO_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        print("✅ Successfully fetched series info!")
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching series info: {e}")
        return None

def process_match_list(series_info):
    """Process the match list and sort by match number."""
    if not (series_info and series_info.get("status") == "success"):
        print("⚠️ Invalid series info data.")
        return None

    match_list = series_info.get("data", {}).get("matchList", [])
    df = pd.json_normalize(match_list)

    # Extract match number
    df['Match Number'] = df['name'].str.extract(r'(\d{1,3}(?:st|nd|rd|th) Match)')
    df['Match Number Int'] = df['Match Number'].str.extract(r'(\d{1,3})').astype(float)

    # Sort and clean
    df_sorted = df.sort_values(by='Match Number Int').reset_index(drop=True)
    df_sorted = df_sorted.drop(columns=['Match Number Int'])

    return df_sorted

def save_match_list(df, output_path="../data/IPL_2025_Match_List.csv"):
    """Save the sorted match list to a CSV file."""
    df.to_csv(output_path, index=False)
    print(f"✅ Saved match list to {output_path}")

def preview_matches(df, columns=["name", "venue", "date", "Match Number"]):
    """Display a preview of sorted matches."""
    print("\n📋 Sorted Match List Preview:")
    print(df[columns])

# ========== Main Execution ==========
def main():
    """Main function to orchestrate fetching and saving match data."""
    series_info = fetch_series_info(API_KEY, SERIES_ID)
    match_df = process_match_list(series_info)

    if match_df is not None:
        preview_matches(match_df)
        save_match_list(match_df)
    else:
        print("\n❌ No match data to save.")

if __name__ == "__main__":
    main()
