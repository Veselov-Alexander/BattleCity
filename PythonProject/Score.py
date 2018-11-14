from GameObjects import *

INF = int(1e10)

def to_minutes(seconds):
    if seconds == INF or seconds == 0:
        return "unknown"
    minutes = seconds // 60
    seconds = seconds % 60
    return "{:02}:{:02}".format(minutes, seconds)

class Score:
    def __init__(self):
        self.current_score = INF
        self.load_records()    

    def load_records(self):
        self.stats = list()
        with open("records.dat") as records:
            for record in records:
                self.stats.append(int(record))
                if self.stats[-1] == -1:
                    self.stats[-1] = INF


    def update_record(self, level):
        if 0 <= level <= 3:
            self.stats[level] = min(self.stats[level], self.current_score)
        else:
            self.stats[4] = max(self.stats[4], self.current_score)
        self.save_records()


    def update_scene(self, game_end, leaderboard):
        game_end.static_objects[1].text = "  result: " + to_minutes(self.current_score)
        for i, score in enumerate(self.stats):
            leaderboard.static_objects[i + 5].text = to_minutes(score)

    def set_score(self, score):
        self.current_score = score

    def update(self, level, score, game_end, leaderboard):
        self.set_score(score)
        self.update_record(level)
        self.update_scene(game_end, leaderboard)

    def save_records(self):
        with open("records.dat", "w") as records:
            for stat in self.stats:
                if stat == INF:
                    records.write("-1\n")
                else:
                    records.write(str(stat) + "\n")
            #if self.stats[-1] == INF:
            #    records.write("0\n")
            #else:
            #    records.write(str(self.stats[-1]) + "\n")

score_object = Score()