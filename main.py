# -*- coding: cp1252 -*-

from liiga_function_library import fetch_data, write_json, return_results, return_team_results
from liiga_function_library import return_league_table, team_list, write_files
from liiga_function_library import return_team_table
from teams import team_dict, team_dict_lower
import json
import pandas as pd
import time
import os

####
fetch_game_data = 0
print_all_played_games = 0
write_data_files = 0
teams = team_list()
# Fetching league data
league_table_url = "https://liiga.fi/api/v1/teams/stats/2022/runkosarja/"
league_table = return_league_table(league_table_url)
clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
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

####
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

for ind, x in enumerate(teams):
    for i in played_games:
        if i["home"].lower() == x.lower() or i["away"].lower() == x.lower():
            team_dict[x]["games"]["played_games"].append(i)
    for i in not_played:
        if i["home"].lower() == x.lower() or i["away"].lower() == x.lower():
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
####

for x in team_dict_lower:
    team_name = x
    for ind in range(15):
        if team_result_data[ind]['results']["name"] == x:
            team_dict_lower[x]['results'] = team_result_data[ind]['results']

if write_data_files != 0:
    write_files(team_dict_lower, teams)

team_table = return_team_table(teams)

##
# WORK IN PROGRESS
time.sleep(2)
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
    inspect_data_choise = int(input())
    while True:
        if inspect_data_choise < 1 or inspect_data_choise > 3:
            inspect_data_choise = int(input("CHOOSE DATA TO SHOW(0-3) : "))
        else:
            break
    if inspect_data_choise == 0:
        break
    elif inspect_data_choise == 1:
        print(f"\n\nShowing played games by: {team.upper()}", )
        new_df = pd.DataFrame(played_games_data)
        print(new_df)
    elif inspect_data_choise == 2:
        print(f"\n\nShowing upcoming games by: {team.upper()}")
        new_df = pd.DataFrame(upcoming_games_data)
        print(new_df)
    elif inspect_data_choise == 3:
        print(f"\n\nShowing league table data by: {team.upper()}")
        new_df = pd.DataFrame(results_data, index=[""]).T
        print(new_df)
    stop = input("\n\n\nExit? y/n ")
    if stop.lower() == "y" or stop.lower() == "":
        break
    else:
        pass

    print("\n\n---Clearing console\n\n")
    time.sleep(1)
    clear_console()

# df.to_excel(f"./team_results/{i}/{i}_data.xlsx")

####
