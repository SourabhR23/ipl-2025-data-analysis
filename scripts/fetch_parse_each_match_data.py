"""
Daily IPL 2025 Match Data Fetcher and Parser

This script runs daily, fetches up to 10 new IPL 2025 match scorecards 
from CricAPI, stores them in memory as a list, and parses into DataFrames.
"""

import os
import pandas as pd
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# ========== Load Environment Variables ==========
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ========== API Configuration ==========
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"
MATCH_LIST_CSV = "../data/IPL_2025_Match_List.csv"
OUTPUT_DIR = "../data/parsed_csv/"
FETCH_LIMIT = 10  # Max 10 matches per day
TIMEOUT = 10  # seconds

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== Helper Functions ==========

def extract_pending_ids(csv_path, cutoff_date=None):
    """Extract match IDs till a cutoff date."""
    match_list = pd.read_csv(csv_path)
    match_list['date'] = pd.to_datetime(match_list['date'])
    
    if cutoff_date:
        match_list = match_list[match_list['date'] <= cutoff_date]
    
    return match_list['id'].tolist()

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

def parse_match_data(match_list):
    """Parse match JSONs into DataFrames."""
    matches_data = []
    innings_data = []
    batting_data = []
    bowling_data = []
    fielding_data = []
    extras_data = []

    for match in match_list:
        match_id = match.get('id')
        series_id = match.get('series_id')
        name = match.get('name')
        match_type = match.get('matchType')
        status = match.get('status')
        venue = match.get('venue')
        date = match.get('date')
        teams = match.get('teams', [])
        team1 = teams[0] if len(teams) > 0 else None
        team2 = teams[1] if len(teams) > 1 else None
        toss_winner = match.get('tossWinner')
        toss_choice = match.get('tossChoice')
        match_winner = match.get('matchWinner')

        matches_data.append({
            'match_id': match_id,
            'series_id': series_id,
            'match_name': name,
            'match_type': match_type,
            'status': status,
            'venue': venue,
            'date': date,
            'team1': team1,
            'team2': team2,
            'toss_winner': toss_winner,
            'toss_choice': toss_choice,
            'match_winner': match_winner
        })

        for score in match.get('score', []):
            innings_data.append({
                'match_id': match_id,
                'inning_name': score.get('inning'),
                'runs': score.get('r'),
                'wickets': score.get('w'),
                'overs': score.get('o')
            })

        for innings in match.get('scorecard', []):
            inning_name = innings.get('inning')

            for batter in innings.get('batting', []):
                batsman = batter.get('batsman', {})
                bowler = batter.get('bowler', {})
                catcher = batter.get('catcher', {})
                batting_data.append({
                    'match_id': match_id,
                    'inning_name': inning_name,
                    'batsman_id': batsman.get('id'),
                    'batsman_name': batsman.get('name'),
                    'runs': batter.get('r'),
                    'balls': batter.get('b'),
                    'fours': batter.get('4s'),
                    'sixes': batter.get('6s'),
                    'strike_rate': batter.get('sr'),
                    'dismissal': batter.get('dismissal'),
                    'dismissal_text': batter.get('dismissal-text'),
                    'bowler_id': bowler.get('id'),
                    'bowler_name': bowler.get('name'),
                    'catcher_id': catcher.get('id'),
                    'catcher_name': catcher.get('name')
                })

            for bowler in innings.get('bowling', []):
                bowler_info = bowler.get('bowler', {})
                bowling_data.append({
                    'match_id': match_id,
                    'inning_name': inning_name,
                    'bowler_id': bowler_info.get('id'),
                    'bowler_name': bowler_info.get('name'),
                    'overs': bowler.get('o'),
                    'maidens': bowler.get('m'),
                    'runs_conceded': bowler.get('r'),
                    'wickets': bowler.get('w'),
                    'no_balls': bowler.get('nb'),
                    'wides': bowler.get('wd'),
                    'economy': bowler.get('eco')
                })

            for fielder in innings.get('catching', []):
                catcher_info = fielder.get('catcher', {})
                fielding_data.append({
                    'match_id': match_id,
                    'inning_name': inning_name,
                    'fielder_id': catcher_info.get('id'),
                    'fielder_name': catcher_info.get('name'),
                    'catches': fielder.get('catch'),
                    'stumpings': fielder.get('stumped'),
                    'runouts': fielder.get('runout'),
                    'bowled': fielder.get('bowled')
                })

            extras = innings.get('extras', {})
            extras_data.append({
                'match_id': match_id,
                'inning_name': inning_name,
                'extra_runs': extras.get('r', 0),
                'byes': extras.get('b', 0)
            })

    return {
        'matches_df': pd.DataFrame(matches_data),
        'innings_df': pd.DataFrame(innings_data),
        'batting_df': pd.DataFrame(batting_data),
        'bowling_df': pd.DataFrame(bowling_data),
        'fielding_df': pd.DataFrame(fielding_data),
        'extras_df': pd.DataFrame(extras_data)
    }

# ========== Main Execution ==========

def main():
    today = datetime.today().strftime('%Y-%m-%d')
    print(f"🏏 Running daily fetch for {today}")

    pending_ids = extract_pending_ids(MATCH_LIST_CSV, cutoff_date=today)
    print(f"📝 Pending matches to fetch: {len(pending_ids)}")

    if not pending_ids:
        print("🎉 No new matches to fetch today.")
        return

    match_data_list = []
    count = 0

    for match_id in pending_ids[:FETCH_LIMIT]:
        match_data = fetch_match_data(match_id)
        if match_data:
            match_data_list.append(match_data)
            count += 1
    
    print(f"🚀 Fetched {count} matches. Now parsing...")

    if match_data_list:
        dataframes = parse_match_data(match_data_list)
        for name, df in dataframes.items():
            output_file = os.path.join(OUTPUT_DIR, f"{name}.csv")
            df.to_csv(output_file, index=False)
            print(f"✅ Saved {name}.csv with {len(df)} records.")

if __name__ == "__main__":
    main()
