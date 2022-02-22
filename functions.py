#pip install requests-futures

import requests
import json
import os
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

def return_team(data, team):
    team_id = data["game"][team]["teamId"]
    team_id = team_id.split(":")
    return team_id[1].capitalize()


def return_goals(data, team):
    team_id = data["game"][team]
    return team_id["goals"]


def return_results(data: dict):
    winner = ""
    home_team = "homeTeam"
    away_team = "awayTeam"
    full_date = data["game"]["start"]
    game_id = data["game"]["id"]
    date = full_date.split("T")
    time = date[1][:-4]
    calendar_date = date[0]
    home_team_id = return_team(data, home_team)
    away_team_id = return_team(data, away_team)
    home_team_goals = return_goals(data, home_team)
    away_team_goals = return_goals(data, away_team)

    if home_team_goals > away_team_goals:
        winner = home_team_id
    elif home_team_goals < away_team_goals:
        winner = away_team_id

    return {
        "Game ID": game_id,
        "Date": calendar_date,
        "Time": time,
        "Home Team": home_team_id,
        "Away Team": away_team_id,
        f"{home_team_id} goals": home_team_goals,
        f"{away_team_id} goals": away_team_goals,
        "Winner": winner}


def fetch_data(custom_url: str, f_game: int, l_game: int):
    data_list = []
    with FuturesSession() as session:
        futures = [session.get(f"{custom_url}{_}") for _ in range(f_game, l_game)]
        for future in as_completed(futures):
            response = future.result()
            data_list.append(response.json())
    return data_list

def write_json(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w') as f:
        json.dump(data, f, ensure_ascii=False)
