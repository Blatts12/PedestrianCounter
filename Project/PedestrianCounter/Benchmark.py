import csv
from datetime import date


class Benchmark:
    def __init__(self):
        self.fps = ["FPS"]
        self.frame_time = ["Frame time"]
        self.disappeared = ["Disappeared Objects"]
        self.up = ["Counted Up"]
        self.down = ["Counted Down"]

    def add(self, fps, time, dis, up, down):
        self.fps.append(fps)
        self.frame_time.append(time)
        self.disappeared.append(dis)
        self.up.append(up)
        self.down.append(down)

    def save_to_file(self, name):
        with open(
            "Benchmark-{}-{}.csv".format(name, date.today()), "w+", newline=""
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            for i in range(0, len(self.fps)):
                writer.writerow(
                    [
                        "Frame" if i == 0 else i,
                        self.fps[i],
                        self.frame_time[i],
                        self.disappeared[i],
                        self.up[i],
                        self.down[i],
                    ]
                )

        self.fps = ["FPS"]
        self.frame_time = ["Frame time"]
        self.disappeared = ["Disappeared Objects"]
        self.up = ["Counted Up"]
        self.down = ["Counted Down"]

        print("BENCHMARK DONE")
