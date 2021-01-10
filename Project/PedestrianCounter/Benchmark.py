import csv
import json
import numpy as np


class Benchmark:
    def __init__(self):
        self.fps = []
        self.frame_time = []
        self.disappeared = []
        self.up = []
        self.down = []

        self.scores_dict = {}
        self.scores_dict["scores"] = []

    def add(self, fps, time, dis, up, down):
        self.fps.append(fps)
        self.frame_time.append(time)
        self.disappeared.append(dis)
        self.up.append(up)
        self.down.append(down)

    def save_to_file(self, name):
        with open("Tests/CSV/CSV-{}.csv".format(name), "w+", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["Frame", "FPS", "Frame Time", "Dis", "Up", "Down"])
            for i in range(0, len(self.fps)):
                writer.writerow(
                    [
                        i,
                        self.fps[i],
                        self.frame_time[i],
                        self.disappeared[i],
                        self.up[i],
                        self.down[i],
                    ]
                )

        self.calculate(name)

        self.fps = []
        self.frame_time = []
        self.disappeared = []
        self.up = []
        self.down = []
        print("BENCHMARK DONE")

    def calculate(self, name):
        one_len = round(len(self.fps) / 100)

        mean_fps = np.mean(np.array(self.fps).astype(np.float))
        self.fps.sort()
        mean_one_fps = np.mean(np.array(self.fps[:one_len]).astype(np.float))

        mean_time = np.mean(np.array(self.frame_time).astype(np.float))
        self.frame_time.sort(reverse=True)
        mean_one_time = np.mean(np.array(self.frame_time[:one_len]).astype(np.float))

        final_disappeared = self.disappeared[-1]
        final_up = self.up[-1]
        final_down = self.down[-1]
        final_crossed = final_up - final_down

        scores = {
            "test_name": name,
            "mean_fps": mean_fps,
            "mean_1low_fps": mean_one_fps,
            "mean_frame_time": mean_time,
            "mean_1low_frame_time": mean_one_time,
            "up": final_up,
            "down": final_down,
            "crossed": final_crossed,
            "disappeared": final_disappeared,
        }

        self.scores_dict["scores"].append(scores)

    def save_scores(self):
        with open("Tests/scores.json", "w+") as score_file:
            json.dump(self.scores_dict, score_file)