# -*- coding: cp1252 -*-
from datetime import datetime
from liiga_function_library import team_list

now = datetime.now()
now = now.strftime("%d-%m-%Y %H:%M")
teams = team_list()
team_dict = {}
for i in teams:
    team_dict[i] = {
        "team_name": i.lower(),
        "last_updated": now,
        "games": {
            "played_games": [],
            "upcoming_games": []
        },
        "players":[]

    }
def to_lower(dictionary):
    def try_iterate(k):
        return lower_by_level(k) if isinstance(k, dict) else k

    def try_lower(k):
        return k.lower() if isinstance(k, str) else k

    def lower_by_level(data):
        return dict((try_lower(k), try_iterate(v)) for k, v in data.items())

    return lower_by_level(dictionary)


team_dict_lower = to_lower(team_dict)
