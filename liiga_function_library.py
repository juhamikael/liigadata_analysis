# -*- coding: cp1252 -*-

import requests
import json
import pandas as pd
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from prettytable import PrettyTable
import time
import os


def return_team(data, team):
    team_id = data["game"][team]["teamId"]
    team_id = team_id.split(":")
    return team_id[1].capitalize()


def return_goals(data, team):
    team_id = data["game"][team]
    return team_id["goals"]


# def change_time(date: str):
#     print("D: ", date)
#     year = int(date[0:4])
#     month = int(date[5:7])
#     day = int(date[8:10])
#     return datetime(year, month, day)


def return_results(*argv):
    data: dict = argv[0]
    home_team = "homeTeam"
    away_team = "awayTeam"
    winner = ""
    date = data["game"]["start"][0:10]
    game_id = data["game"]["id"]
    home_team_id = return_team(data, home_team)
    away_team_id = return_team(data, away_team)
    home_team_goals = return_goals(data, home_team)
    away_team_goals = return_goals(data, away_team)
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
    for i in league_table_data:
        league_table.append(i)
    for i in range(len(league_table)):
        write_json('./league_table_data/', f'team{i + 1}.json', league_table[i])
    return league_table


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


def return_team_table(teams_list: list):
    my_table = PrettyTable(["index", "team"])
    for ind, val in enumerate(teams_list):
        my_table.add_row([ind, val])
    my_table.align = "l"
    my_table.align["index"] = "c"
    return my_table


def clear_console():
    return os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def command_line_ui(team_dict_lower):
    teams = team_list()
    team_table = return_team_table(teams)
    clear_console()

    while True:
        print(team_table)
        team_choice = int(input("CHOOSE TEAM FROM TABLE ABOVE (0-14) : "))
        while True:
            if team_choice > 14 or team_choice < 0:
                team_choice = int(input("CHOOSE TEAM FROM TABLE ABOVE (0-14) : "))
            else:
                break
        team = teams[team_choice]

        played_games_data = team_dict_lower[team]['games']['played_games']
        upcoming_games_data = team_dict_lower[team]['games']['upcoming_games']
        results_data = team_dict_lower[team]['results']

        print(f"\n{team.upper()}")
        print(f"\nCHOOSE DATA TO SHOW(1-3) : \n"
              f"1 - Show played games\n"
              f"2 - Show upcoming games\n"
              f"3 - Show league table data\n")
        inspect_data_choice = int(input())
        while True:
            if inspect_data_choice < 1 or inspect_data_choice > 3:
                inspect_data_choice = int(input("CHOOSE DATA TO SHOW(0-3) : "))
            else:
                break
        if inspect_data_choice == 1:
            print(f"\n\nShowing played games by: {team.upper()}", )
            df = pd.DataFrame(played_games_data)
            print(df)
        elif inspect_data_choice == 2:
            print(f"\n\nShowing upcoming games by: {team.upper()}")
            df = pd.DataFrame(upcoming_games_data)
            print(df)
        elif inspect_data_choice == 3:
            print(f"\n\nShowing league table data by: {team.upper()}")
            df = pd.DataFrame(results_data, index=[""]).T
            print(df)

        stop = input("\n\n\nExit? y/n ")
        if stop == "y":
            break
        elif stop == "n":
            pass
        elif stop != "n" or stop == "y":
            while True:
                stop = input("Exit? y/n ")
                if stop == "y" or stop == "n":
                    break
                else:
                    pass

        print("\n\n---Clearing console\n\n")
        time.sleep(1)
        clear_console()
