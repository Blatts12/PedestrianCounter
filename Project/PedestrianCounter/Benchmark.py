import csv
from operator import invert
import numpy as np


class Benchmark:
    def __init__(self):
        self.fps = []
        self.frame_time = []
        self.disappeared = []
        self.up = []
        self.down = []

    def add(self, fps, time, dis, up, down):
        self.fps.append(fps)
        self.frame_time.append(time)
        self.disappeared.append(dis)
        self.up.append(up)
        self.down.append(down)

    def save_to_file(self, name):
        with open("Tests/CSV-{}.csv".format(name), "w+", newline="") as csv_file:
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

        final_crossed = self.up[-1] - self.down[-1]
        final_disappeared = self.disappeared[-1]
        with open("Tests/SCORE-{}.txt".format(name), "w+") as score_file:
            score_file.write("Mean FPS: {}\n".format(mean_fps))
            score_file.write("Mean 1% Low FPS: {}\n".format(mean_one_fps))
            score_file.write("Mean Frame Time: {}\n".format(mean_time))
            score_file.write("Mean 1% Low Frame Time: {}\n".format(mean_one_time))
            score_file.write("Crossed: {}\n".format(final_crossed))
            score_file.write("Disappeared: {}\n".format(final_disappeared))
