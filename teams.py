# -*- coding: cp1252 -*-

from functions import team_list

teams = team_list()

team_dict = {}
for i in teams:
    team_dict[i] = {
        "team_name:": i,
        "games": {
            "played_games": [],
            "upcoming_games": []
        },
        "results": {
            "standings_ranking": None,
            "points": None,
            "games_played": None,
            "points_per_game": None,
            "games_won": None,
            "games_lost": None,
            "games_tied": None,
            "ot_ps_won": None,
            "ot_ps_lost": None,
            "powerplay_percentage": None
        }
    }
