import json


class Scoreboard:
    def __init__(self, file) -> None:
        self.file = file
        self.scores: dict = json.load(file)

    def addScore(self, username, score):
        if username in self.scores:
            if score < self.scores[username]:
                return
        self.scores[username] = score

    def toJSON(self):
        sortedscore = dict(sorted(
            self.scores.items(), key=lambda x: x[1], reverse=True
        ))
        return json.dumps(sortedscore)

    def save(self):
        sortedscore = dict(sorted(
            self.scores.items(), key=lambda x: x[1], reverse=True
        ))
        self.file.seek(0)
        self.file.write(json.dumps(sortedscore))
        self.file.truncate()
