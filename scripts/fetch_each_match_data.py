"""
Daily IPL 2025 Match Data Fetcher

This script runs daily, fetches up to 10 new IPL 2025 match scorecards 
from CricAPI, and stores them in a local folder.
"""

import os
import pandas as pd
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configuration
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"
MATCH_LIST_CSV = "data/IPL_2025_Match_List.csv"
DATA_DIR = "data/match_json/"
FETCH_LIMIT = 10  # Max 10 matches per day
TIMEOUT = 10  # seconds

# Create data directory if not exists
os.makedirs(DATA_DIR, exist_ok=True)

def extract_pending_ids(csv_path, data_dir, cutoff_date=None):
    """Extract match IDs not yet downloaded."""
    match_list = pd.read_csv(csv_path)
    match_list['date'] = pd.to_datetime(match_list['date'])

    # Filter only completed matches
    if cutoff_date:
        match_list = match_list[match_list['date'] <= cutoff_date]
    
    all_ids = set(match_list['id'].tolist())
    
    # Read existing files
    downloaded_ids = {f.split('.')[0] for f in os.listdir(data_dir) if f.endswith('.json')}
    
    pending_ids = list(all_ids - downloaded_ids)
    return pending_ids

def fetch_match_data(match_id):
    """Fetch a single match JSON from API."""
    params = {"apikey": API_KEY, "id": match_id}
    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        match_info = response.json()
        
        if match_info.get("status") == "success":
            return match_info.get("data", {})
        else:
            print(f"⚠️ API returned non-success status for ID {match_id}")
            return None
        
    except Exception as e:
        print(f"❌ Error fetching match ID {match_id}: {e}")
        return None

def save_match_json(match_data, match_id):
    """Save match JSON to file."""
    file_path = os.path.join(DATA_DIR, f"{match_id}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(match_data, f, indent=2)
    print(f"✅ Saved match data for ID {match_id}")

def main():
    today = datetime.today().strftime('%Y-%m-%d')
    print(f"🏏 Running daily fetch for {today}")

    pending_ids = extract_pending_ids(MATCH_LIST_CSV, DATA_DIR, cutoff_date=today)
    print(f"📝 Pending matches to fetch: {len(pending_ids)}")

    if not pending_ids:
        print("🎉 No new matches to fetch today.")
        return

    count = 0
    for match_id in pending_ids[:FETCH_LIMIT]:
        match_data = fetch_match_data(match_id)
        if match_data:
            save_match_json(match_data, match_id)
            count += 1
    
    print(f"🚀 Fetched and saved {count} matches today!")

if __name__ == "__main__":
    main()
