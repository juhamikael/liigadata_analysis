# -*- coding: cp1252 -*-
from liiga_function_library import fetch_data, write_json, return_results, return_team_results
from liiga_function_library import return_league_table, team_list
from teams import team_dict, team_dict_lower
import json
import pandas as pd

####
fetch_game_data = 0
print_all_played_games = 0
write_json_file = 1
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
    if return_results(all_games[i])["winner"] == "":
        not_played.append(return_results(all_games[i]))
    else:
        played_games.append(return_results(all_games[i]))


z = 1

# print(played_games[5]["Away"].lower())

for ind, x  in enumerate(teams):
    for i in played_games:
        if i["home"].lower() == x.lower() or played_games[ind]["away"].lower() == x.lower():
            team_dict[x]["games"]["played_games"].append(i)
    for i in not_played:
        if i["home"].lower() == x.lower() or played_games[ind]["away"].lower() == x.lower():
            team_dict[x]["games"]["upcoming_games"].append(i)


if print_all_played_games != 0:
    print(f"Played games: {len(played_games)}")
    print(f"Not played yet: {len(not_played)}")
    print("\nPlayed Games: ")
    for i in played_games:
        if i is None:
            continue
        else:
            print(i)

team_result_data = []
for x in range(len(teams)):
    team_result_data.append(return_team_results(league_table[x]))
for x in team_result_data:
    print(x)

####

for x in team_dict_lower:
    team_name = x
    for ind in range(15):
        if team_result_data[ind]['results']["name"] == x:
            team_dict_lower[x]['results'] = team_result_data[ind]['results']
            print(f"{team_name}")

if write_json_file != 0:
    write_json('./team_results/', f'team_dict.json', team_dict_lower)

# print(type(played_games))
df = pd.DataFrame(played_games)
df = df.sort_values("game_id")
df.to_excel("output.xlsx")

####
