import numpy as np
from math import pi

_HALF_PI = pi / 2


class Counter:
    def __init__(self, horizontal=False, margin=0, min_update_time=3):
        self.horizontal = horizontal
        self.margin = margin
        self.min_update_time = min_update_time
        self.up = 0  # or right
        self.down = 0  # or left
        self.inverted = False

    def reset(self):
        self.up = 0
        self.down = 0

    def set_margin(self, margin):
        self.margin = margin

    def set_min_update_time(self, min_update_time):
        self.min_update_time = min_update_time

    def set_horizontal(self, horizontal):
        self.horizontal = horizontal

    def set_inverted(self, inverted):
        self.inverted = inverted

    def get_crossed(self):
        if self.inverted:
            return self.down - self.up
        return self.up - self.down

    def process_person(self, person, frame_width, frame_height):
        if self.horizontal:
            self._process_horizontal(person, frame_width)
        else:
            self._process_vertical(person, frame_height)

    def _process_horizontal(self, person, frame_width):
        centroid = tuple(person.get_centroid())
        x = [c[0] for c in person.centroids]
        direction = centroid[0] - np.mean(x)
        mean_theta = _HALF_PI if not person.theta else np.mean(person.theta) + _HALF_PI

        half_width = frame_width // 2

        if not person.counted and person.update_time > self.min_update_time:
            if (
                direction < 0
                and mean_theta < 0
                and centroid[1] < half_width
                and centroid[1] > self.margin
            ):
                print("[{}]LEFT-MEAN_THETA: {}".format(person.id, mean_theta))
                self.up += 1
                person.counted = True

            elif (
                direction > 0
                and mean_theta > 0
                and centroid[1] > half_width
                and centroid[1] < frame_width - self.margin
            ):
                print("[{}]RIGHT-MEAN_THETA: {}".format(person.id, mean_theta))
                self.down += 1
                person.counted = True

    def _process_vertical(self, person, frame_height):
        centroid = tuple(person.get_centroid())
        y = [c[1] for c in person.centroids]
        direction = centroid[1] - np.mean(y)
        mean_theta = 0 if not person.theta else np.mean(person.theta)
        half_height = frame_height // 2

        if not person.counted and person.update_time > self.min_update_time:
            if (
                direction < 0
                and mean_theta < 0
                and centroid[1] < half_height
                and centroid[1] > self.margin
            ):
                print("[{}]UP-MEAN_THETA: {}".format(person.id, mean_theta))
                self.up += 1
                person.counted = True

            elif (
                direction > 0
                and mean_theta > 0
                and centroid[1] > half_height
                and centroid[1] < frame_height - self.margin
            ):
                print("[{}]DOWN-MEAN_THETA: {}".format(person.id, mean_theta))
                self.down += 1
                person.counted = True