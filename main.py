# -*- coding: cp1252 -*-
import os

from liiga_function_library import fetch_games_data, return_results, return_team_results
from liiga_function_library import write_files, return_league_table
from teams import team_dict, team_dict_lower
from classes import CMD_Program, Teams, Players
import json
from ffcount import ffcount

####################################################
# Setting uo project and data
# If any of the values below is changed to 1 from 0
# it's going to do exactly that what variable name is
request_game_data = 0
print_all_played_games = 0
write_data_files = 1
start_ui = 0
teams_class = Teams()
teams_list = teams_class.return_all_teams_as_list()
players = Players()
players_list = players.get_player_data_files()
####################################################


####################################################
# if fetch_game_data = 1, fetching league table data
league_table = return_league_table("https://liiga.fi/api/v1/teams/stats/2022/runkosarja/")
# and game result data
if request_game_data != 0:
    fetch_games_data("https://liiga.fi/api/v1/games/2022/")
####################################################


####################################################
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
####################################################


####################################################
all_games = []
for i in files_ok:
    with open(i) as jsonFile:
        jsonObject = json.load(jsonFile)
        all_games.append(jsonObject)
        jsonFile.close()
for i in range(0, len(all_games)):
    return_results(all_games[i])
####################################################


####################################################
played_games = []
not_played = []
for i in range(1, len(all_games)):
    if return_results(all_games[i])["winner"] == "":
        not_played.append(return_results(all_games[i]))
    else:
        played_games.append(return_results(all_games[i]))

for ind, x in enumerate(teams_list):
    for i in played_games:
        if i["home"].lower() == x.lower() or i["away"].lower() == x.lower():
            team_dict[x]["games"]["played_games"].append(i)
    for i in not_played:
        if i["home"].lower() == x.lower() or i["away"].lower() == x.lower():
            team_dict[x]["games"]["upcoming_games"].append(i)
####################################################


####################################################
# if print_all_played_games is turned on
if print_all_played_games != 0:
    print(f"Played games: {len(played_games)}")
    print(f"Not played yet: {len(not_played)}")
    print("\nPlayed Games: ")
    # iterating throug played games list
    for i in played_games:
        if i is None:
            continue
        else:
            print(i)
####################################################

team_result_data = []
for x in range(len(teams_list)):
    team_result_data.append(return_team_results(league_table[x]))

for x in team_dict_lower:
    team_name = x
    for ind in range(15):
        if team_result_data[ind]['results']['name'] == x:
            team_dict_lower[x]['results'] = team_result_data[ind]['results']


for x in team_dict_lower:
    for index in range(len(players_list)):
        if players_list[index]["team"] == x:
            team_dict_lower[x]['players'].append(players_list[index])
            # print(team_dict_lower[x]['players'])

for i in teams_list:
    for x in team_dict_lower[i]['players']:
        del x['team']
    team_dict_lower[i]["results"].pop("name")


if write_data_files != 0:
    write_files(team_dict_lower, teams_list)

# WORK IN PROGRESS
if start_ui != 0:
    start_program = CMD_Program(team_dict_lower)
    start_program.start()

#
# for i in players_list:
#     if i["team"] == "ilves":
#         print(i)
# df.to_excel(f"./team_results/{i}/{i}_data.xlsx")
####


# players_path = "./player_data"
# player_amount = ffcount(players_path)[0]
# players = players.read_player_data_files(player_amount)
# print(type(players))
