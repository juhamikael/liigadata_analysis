# -*- coding: cp1252 -*-
from functions import fetch_data, write_json, return_results, return_team
from functions import return_league_table, team_list, team_list_utf8
from teams import team_dict
import json
import pandas as pd
from datetime import date

####
fetch_game_data = 0
print_all_played_games = 0
write_json_file = 0
teams = team_list()
# Fetching league data
league_table_url = "https://liiga.fi/api/v1/teams/stats/2022/runkosarja/"
league_table = return_league_table(league_table_url)
####

# Fetch data
first_game = 1
last_game = 451
if fetch_game_data != 0:
    url = f"https://liiga.fi/api/v1/games/2022/"
    game_data_list = fetch_data(url, first_game, last_game)
    for i in range(1, len(game_data_list)): write_json('./game_data/', f'game{i}.json', game_data_list[i])
####

broken_files = []
files_ok = []

for i in range(1, 450):
    file_name = f"./game_data/game{i}.json"
    file = open(file_name)
    json_dictionary = str(json.load(file))
    file.close()
    if json_dictionary == "Remote server error":
        broken_files.append(file_name)
    else:
        files_ok.append(file_name)

print("Broken Files: ", len(broken_files))
print("Files OK: ", len(files_ok), "\n")

all_games = []

for i in files_ok:
    with open(i) as jsonFile:
        jsonObject = json.load(jsonFile)
        all_games.append(jsonObject)
        jsonFile.close()

for i in range(0, len(all_games)):
    return_results(all_games[i])

####

played_games = []
not_played = []
#

for i in range(1, len(all_games)):
    if return_results(all_games[i])["Winner"] == "":
        not_played.append(return_results(all_games[i]))
    else:
        played_games.append(return_results(all_games[i]))
z = 1
for x in teams:
    for i in played_games:
        if i["Home"].lower() == x.lower() or played_games[5]["Away"].lower() == x.lower():
            team_dict[x]["games"]["played_games"].append(i)

if print_all_played_games != 0:
    print(f"Played games: {len(played_games)}")
    print(f"Not played yet: {len(not_played)}")
    print("\nPlayed Games: ")
    for i in played_games:
        if i is None:
            continue
        else:
            print(i)

if write_json_file != 0:
    write_json('./team_results/', f'team_dict.json', team_dict)

####
# print(type(played_games))
df = pd.DataFrame(played_games)
df = df.sort_values("Game ID")
df.to_excel("output.xlsx")

####


team_dictionary = []
team_name = "slug"
rank = "standings_ranking"
played_games = "games"
points = "points"
points_per_game = "points_per_game"
games_won = "games_won"
games_lost = "games_lost"
games_tied = "games_tied"
ot_wins = "ot_ps_won"
ot_loses = "ot_ps_lost"
pp_percentage = "powerplay_percentage"
pp_goals = "powerplay_goals_for"

parsing_data = [
    team_name,
    rank,
    played_games,
    points,
    points_per_game,
    games_won,
    games_lost,
    games_tied,
    ot_wins,
    ot_loses,
    pp_percentage,
    pp_goals
]
utf_team_list = team_list_utf8()

# print(team_dict["Ilves"]["results"][i])
for x in range(len(league_table)):
    for i in parsing_data:
        print(f"{i} : {league_table[x][i]}")
    print("\n\n\n")

