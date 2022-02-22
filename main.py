# -*- coding: cp1252 -*-
# !pip install requests
# !pip install --upgrade pip
# !pip install faster_than_request
# !pip install pandas
from functions import fetch_data, write_json, return_results
import json
import pandas as pd
from datetime import date

first_game = 1
last_game = 451
url = f"https://liiga.fi/api/v1/games/2022/"
data_list = fetch_data(url, first_game, last_game)

for i in range(1, len(data_list)):
    write_json('./json_data/', f'game{i}.json', data_list[i])

teams = ["HIFK",
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

team_dict = {}
for i in teams:
    team_dict[i] = {}

broken_files = []
files_ok = []

for i in range(1, 450):
    file_name = f"./json_data/game{i}.json"
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
    print(return_results(all_games[i]))
