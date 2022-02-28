# -*- coding: cp1252 -*-

import requests
import json
import pandas as pd
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from classes import Teams
import os


def return_results(*argv):
    data: dict = argv[0]
    teams = Teams(data)
    winner = ""
    date = data["game"]["start"][0:10]
    game_id = data["game"]["id"]
    home_team_id = teams.return_home_team()
    away_team_id = teams.return_away_team()
    home_team_goals = (teams.return_home_goals())
    away_team_goals = int(teams.return_away_goals())
    karpat = "kärpät"
    assat = "ässät"
    if home_team_id.lower() == karpat:
        home_team_id = "karpat"
    if away_team_id.lower() == karpat:
        away_team_id = "karpat"
    if home_team_id.lower() == assat:
        home_team_id = "assat"
    if away_team_id.lower() == assat:
        away_team_id = "assat"
    if home_team_goals > away_team_goals:
        winner = home_team_id
    elif home_team_goals < away_team_goals:
        winner = away_team_id
    dict_to_return = {
        "game_id": game_id,
        "date": date,
        "home": home_team_id.lower(),
        "away": away_team_id.lower(),
        "home_team_goals": home_team_goals,
        "away_team_goals": away_team_goals,
        "winner": winner.lower()}

    if len(argv) == 1:
        return dict_to_return
    if len(argv) == 2:
        team_name = argv[1]
        if dict_to_return["home"].lower() == team_name or dict_to_return["away"].lower() == team_name:
            return dict_to_return


def return_league_table(url: str):
    league_table = []
    league_table_data = fetch_data(url)
    for i in league_table_data:
        league_table.append(i)
    for i in range(len(league_table)):
        write_json('./league_table_data/', f'team{i + 1}.json', league_table[i])
    return league_table


def fetch_games_data(url: str):
    season_first_game = 1
    season_last_game = 451
    game_data_list = fetch_data(url, season_first_game, season_last_game)
    for i in range(1, len(game_data_list)): write_json('./game_data/', f'game{i}.json', game_data_list[i])


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


def return_team_results(data: list):
    name = data["slug"]
    standing = "standings_ranking"
    pts = "points"
    games = "games"
    pts_game = "points_per_game"
    games_won = "games_won"
    games_lost = "games_lost"
    games_tied = "games_tied"
    ot_wins = "ot_ps_won"
    ot_loses = "ot_ps_lost"
    pp_percentage = "powerplay_percentage"
    pp_goals = "powerplay_goals_for"
    dict_to_return = {
        "results": dict(name=name, standings_ranking=data[standing], points=data[pts],
                        games_played=data[games], points_per_game=data[pts_game], games_won=data[games_won],
                        games_lost=data[games_lost], games_tied=data[games_tied], ot_ps_won=data[ot_wins],
                        ot_ps_lost=data[ot_loses], powerplay_percentage=data[pp_percentage],
                        powerplay_goals_for=data[pp_goals])
    }
    return dict_to_return


def team_list():
    return ["hifk",
            "hpk",
            "ilves",
            "jukurit",
            "jyp",
            "kalpa",
            "kookoo",
            "karpat",
            "lukko",
            "pelicans",
            "saipa",
            "sport",
            "tappara",
            "tps",
            "assat"]


def write_json(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def write_files(data_dict: dict, teams_list: list):
    write_json('./team_results/', f'all_teams_data.json', data_dict)
    for i in teams_list:
        write_json(f'./team_results/{i}/', f'data_{i}_0.json', data_dict[i])
    for i in teams_list:
        played_games = data_dict[i]['games']['played_games']
        upcoming_games = data_dict[i]['games']['upcoming_games']
        results = data_dict[i]['results']
        played_games_df = pd.DataFrame(played_games).sort_values("game_id")
        upcoming_games_df = pd.DataFrame(upcoming_games).sort_values("game_id")
        results_transposed = pd.DataFrame(results, index=[0]).T
        ##########
        played_games_df.to_excel(f"./team_results/{i}/xlsx_{i}_1_played_games_data.xlsx")
        write_json(f'./team_results/{i}/', f'data_{i}_1_played_games_data.json', played_games)
        ##########
        upcoming_games_df.to_excel(f"./team_results/{i}/xlsx_{i}_2_upcoming_games_data.xlsx")
        write_json(f'./team_results/{i}/', f'data_{i}_2_upcoming_games_data.json', upcoming_games)
        ##########
        results_transposed.to_excel(f"./team_results/{i}/xlsx_{i}_3_results_data.xlsx")
        write_json(f'./team_results/{i}/', f'data_{i}_3_results.json', results)
        ##########

# def return_team_table(teams_list: list):
#     my_table = PrettyTable(["index", "team"])
#     for ind, val in enumerate(teams_list):
#         my_table.add_row([ind, val])
#     my_table.align = "l"
#     my_table.align["index"] = "c"
#     return my_table
