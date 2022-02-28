# -*- coding: cp1252 -*-
from prettytable import PrettyTable
import pandas as pd
import time
import os


class CMD_Program:
    def __init__(self, *argv):
        self.data = argv[0]
        self.teams = Teams(self.data)
        self.team_list = self.teams.return_all_teams_as_list()
        self.team_name = None

    def print_data(self):
        for index in self.team_list:
            print(self.data[index])

    @staticmethod
    def clear_console():
        return os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def choose_team():
        team_choice = int(input("CHOOSE TEAM FROM TABLE ABOVE (0-14) : "))
        while True:
            if team_choice > 14 or team_choice < 0:
                team_choice = int(input("CHOOSE TEAM FROM TABLE ABOVE (0-14) : "))
            else:
                break
        return team_choice

    @staticmethod
    def choose_data_to_show():
        inspect_data_choice = int(input())
        while True:
            if inspect_data_choice < 1 or inspect_data_choice > 3:
                inspect_data_choice = int(input("CHOOSE DATA TO SHOW(0-3) : "))
            else:
                break
        return inspect_data_choice

    @staticmethod
    def data_to_show(data: list, ):
        df = None
        print(data[1])
        if data[2] == 1 or data[2] == 2:
            df = pd.DataFrame(data[0])
        elif data[2] == 3:
            df = pd.DataFrame(data[0], index=[""]).T
        print(df)

    @staticmethod
    def stop_program():
        pass

    def start(self):
        global data_choice
        teams = self.teams.return_all_teams_as_list()
        team_table = self.teams.return_team_table()
        self.clear_console()
        while True:
            print(team_table)
            team_choice = self.choose_team()
            team = teams[team_choice]
            print("User choice:", team.capitalize())

            played_games_data = self.data[team]['games']['played_games']
            upcoming_games_data = self.data[team]['games']['upcoming_games']
            results_data = self.data[team]['results']
            print(f"\n{team.upper()}")
            print(f"\nCHOOSE DATA TO SHOW(1-3) : \n"
                  f"1 - Show played games\n"
                  f"2 - Show upcoming games\n"
                  f"3 - Show league table data\n")
            inspect_data_choice = self.choose_data_to_show()

            print("Played games", played_games_data)
            print("Upcoming games", upcoming_games_data)
            print("Results", results_data)
            if inspect_data_choice == 1:
                inspect_data_choice = [played_games_data,
                                       f"\n\nShowing played games by: {team.upper()}",
                                       inspect_data_choice]
            elif inspect_data_choice == 2:
                inspect_data_choice = [upcoming_games_data,
                                       f"\n\nShowing upcoming games by: {team.upper()}",
                                       inspect_data_choice]
            elif inspect_data_choice == 3:
                inspect_data_choice = [results_data,
                                       f"\n\nShowing league table data by: {team.upper()}",
                                       inspect_data_choice]
            self.data_to_show(inspect_data_choice)

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
            self.clear_console()


class Teams:
    def __init__(self, *args):
        if len(args) == 1:
            self.data = args[0]

        self.home = "homeTeam"
        self.away = "awayTeam"
        self.teams = ["hifk", "hpk", "ilves", "jukurit", "jyp", "kalpa",
                      "kookoo", "karpat", "lukko", "pelicans", "saipa", "sport", "tappara", "tps", "assat"]

    def return_home_team(self):
        return self.data["game"][self.home]["teamId"].split(":")[1].capitalize()

    def return_away_team(self):
        return self.data["game"][self.away]["teamId"].split(":")[1].capitalize()

    def return_home_goals(self):
        return int(self.data["game"][self.home]["goals"])

    def return_away_goals(self):
        return int(self.data["game"][self.away]["goals"])

    def return_all_teams_as_list(self):
        return self.teams

    def return_team_table(self):
        my_table = PrettyTable(["index", "team"])
        my_table.align = "l"
        my_table.align["index"] = "c"
        for ind, val in enumerate(self.teams):
            my_table.add_row([ind, val])
        return my_table



