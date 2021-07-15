import json


class Scoreboard:
    def __init__(self, jsonfile) -> None:
        self.scores = json.load(jsonfile)

    def addScore(self, username, score):
        self.scores[username] = score

    def toJSON(self):
        return json.dumps(self.scores)
