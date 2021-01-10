import json
import numpy as np
import matplotlib.pyplot as plt


class Data:
    def __init__(self, scores):
        self.r = []
        self.names = []
        self.mean_fps_bar = []
        self.mean_1low_fps_bar = []
        self.mean_frame_time = []
        self.mean_1low_frame_time = []
        self.up = []
        self.down = []
        self.disappeared = []
        self.time = []
        self.bar_width = 0.75

        for score in scores:
            if score["test_name"] == "":
                continue
            self.r.append(int(score["test_name"]))
            self.names.append(score["test_name"])
            self.mean_fps_bar.append(score["mean_fps"] - score["mean_1low_fps"])
            self.mean_1low_fps_bar.append(score["mean_1low_fps"])
            self.mean_1low_frame_time.append(
                score["mean_1low_frame_time"] - score["mean_frame_time"]
            )
            self.mean_frame_time.append(score["mean_frame_time"])
            self.up.append(score["up"])
            self.down.append(score["down"])
            self.disappeared.append(score["disappeared"])
            self.time.append(score["time"])


def draw_mean_fps_chart(data: Data):
    plt.clf()
    plt.figure(figsize=(12, 5))
    plt.bar(
        data.r,
        data.mean_1low_fps_bar,
        color="#e8e78e",
        edgecolor="white",
        width=data.bar_width,
        label="Mean 1% Low FPS",
    )
    plt.bar(
        data.r,
        data.mean_fps_bar,
        bottom=data.mean_1low_fps_bar,
        color="#32a848",
        edgecolor="white",
        width=data.bar_width,
        label="Mean FPS",
    )

    plt.legend(loc="upper left")
    plt.xticks(data.r, data.names)
    plt.xlabel("Test ID")
    plt.ylabel("FPS")

    plt.savefig("FPS.png")


def draw_mean_fps_time_chart(data: Data):
    plt.clf()
    plt.figure(figsize=(12, 5))
    plt.bar(
        data.r,
        data.mean_frame_time,
        color="#e8e78e",
        edgecolor="white",
        width=data.bar_width,
        label="Mean Frame Time",
    )
    plt.bar(
        data.r,
        data.mean_1low_frame_time,
        bottom=data.mean_frame_time,
        color="#32a848",
        edgecolor="white",
        width=data.bar_width,
        label="Mean 1% High Frame Time",
    )

    plt.legend(loc="upper left")
    plt.xticks(data.r, data.names)
    plt.xlabel("Test ID")
    plt.ylabel("Frame time (s)")

    plt.savefig("Frame Time.png")


def draw_crossed(data: Data):
    bar_width = 0.30
    r1 = np.arange(len(data.up))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    plt.clf()
    plt.figure(figsize=(12, 5))
    plt.bar(
        r1,
        data.up,
        color="#e8e78e",
        width=bar_width,
        edgecolor="white",
        label="Crossed Up",
    )
    plt.bar(
        r2,
        data.down,
        color="#32a848",
        width=bar_width,
        edgecolor="white",
        label="Crossed Down",
    )
    plt.bar(
        r3,
        data.disappeared,
        color="#a84e32",
        width=bar_width,
        edgecolor="white",
        label="Disappeared",
    )
    plt.xlabel("Test ID")
    plt.ylabel("Number of pedestrians")
    plt.xticks([r + bar_width for r in range(len(data.up))], data.r)

    plt.legend()
    plt.savefig("Crossed.png")


def draw_time(data: Data):
    plt.clf()
    plt.figure(figsize=(12, 5))
    plt.bar(
        data.r,
        data.time,
        color="#e8e78e",
        edgecolor="white",
        width=data.bar_width,
    )

    plt.xticks(data.r, data.names)
    plt.xlabel("Test ID")
    plt.ylabel("Time (s)")

    plt.savefig("Time.png")


data = None

with open("Tests\scores.json") as scores_file:
    file_data = json.load(scores_file)
    data = Data(file_data["scores"])


draw_mean_fps_chart(data)
draw_mean_fps_time_chart(data)
draw_crossed(data)
draw_time(data)