import pymongo


class Database_connection:
    def __init__(self):
        from liiga_function_library import team_list
        self.teams = team_list()
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")


    def inser_players_json(self):
        pass

    def get_collections(self):
        db = self.client["liiga_database"]
        for coll in db.list_collection_names():
            print(coll)


    def insert_teams_json(self):
        import json
        db = self.client["liiga_database"]
        for i in self.teams:
            with open(f"./team_results/{i}/data_{i}_0.json") as f:
                data = json.load(f)
            collection = db[i]
            collection.insert_one(data)

# print list of the _id values of the inserted documents:
