import json


class Scoreboard:
    def __init__(self, file) -> None:
        self.file = file
        self.scores = json.load(file)

    def addScore(self, username, score):
        if username in self.scores:
            if score < self.scores[username]:
                return
        self.scores[username] = score

    def toJSON(self):
        sortedscore = sorted(self.scores, key=lambda x: x[1], reverse=True)
        return json.dumps(sortedscore)

    def save(self, data):
        self.file.seek(0)
        self.file.write(data)
        self.file.truncate()
