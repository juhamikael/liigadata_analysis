# -*- coding: cp1252 -*-

from re import A
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


def return_results(*argv):
    data: dict = argv[0]
    home_team = "homeTeam"
    away_team = "awayTeam"
    winner = ""
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

    dict_to_return = {
        "Game ID": game_id,
        "Date": calendar_date,
        "Time": time,
        "Home": home_team_id,
        "Away": away_team_id,
        f"Home team goals": home_team_goals,
        f"Away team goals": away_team_goals,
        "Winner": winner}
    if len(argv) == 1:
        return dict_to_return
    if len(argv) == 2:
        # print(dict_to_return["Home"])
        team_name = argv[1]

        if dict_to_return["Home"].lower() == team_name or dict_to_return["Away"].lower() == team_name:
            return dict_to_return


def fetch_data(*argv):
    custom_url: str = argv[0]
    data_list = []
    if len(argv) == 1:
        return requests.get(custom_url).json()
    if len(argv) > 1:
        f_game: int = argv[1]
        l_game: int = argv[2]
        with FuturesSession() as session:
            futures = [session.get(f"{custom_url}{_}")
                       for _ in range(f_game, l_game)]
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


def return_league_table(url):
    league_table = []
    league_table_data = fetch_data(url)
    for i in league_table_data: league_table.append(i)
    for i in range(len(league_table)): write_json('./league_table_data/', f'team{i + 1}.json', league_table[i])
    return league_table


def team_list():
    return ["HIFK",
            "HPK",
            "Ilves",
            "Jukurit",
            "JYP",
            "KalPa",
            "KooKoo",
            "Kärpät",
            "Lukko",
            "Pelicans",
            "SaiPa",
            "Sport",
            "Tappara",
            "TPS",
            "Ässät"]


def team_list_utf8():
    teams = team_list()
    team_list_as_utf8 = []
    for x in teams:
        x = x.lower()
        if x == "ässät":
            x = "assat"
        if x == "kärpät":
            x = "karpat"
        team_list_as_utf8.append(x)
    return team_list_as_utf8
