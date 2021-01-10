import numpy as np
from math import pi, atan2, cos, sin
from collections import OrderedDict, deque
from scipy.spatial import distance as dist


class TrackedObject:
    def __init__(self, _id, centroid, deque_cen_len=36, deque_theta_len=36):
        self.id = _id
        self.centroids = deque(maxlen=deque_cen_len)
        self.centroids.appendleft(centroid)
        self.counted = False
        self.theta = deque(maxlen=deque_theta_len)
        self.disappear = 0
        self.update_time = 0

    def get_centroid(self):
        return self.centroids[0]

    def set_new_centroid(self, centroid):
        self.update_time += 1
        self.centroids.appendleft(centroid)

    def get_direction(self):
        return self.centroids[0][1] - self.centroids[-1][1]

    # get_directional_vector
    def get_movement_vector(self, length=18):
        (x1, y1) = self.centroids[0]
        (x2, y2) = self.centroids[-1]
        if x1 == x2 and y1 == y2:
            return (x1, y1)

        theta = atan2(y1 - y2, x1 - x2)

        x = x1 + length * cos(theta)
        y = y1 + length * sin(theta)

        self.theta.appendleft(theta)

        return (int(x), int(y))


class CentroidTracker:
    def __init__(self, max_distance=35, max_disappearance=30):
        self.next_object_id = 0
        self.tracked_objects = OrderedDict()
        self.max_distance = max_distance
        self.max_disappearance = max_disappearance
        self.disappeared_counter = 0

    def set_max_distance(self, distance):
        self.max_distance = distance

    def set_max_disappearance(self, disappearance):
        self.max_disappearance = disappearance

    def reset(self):
        self.next_object_id = 0
        self.disappeared_counter = 0
        self.tracked_objects = OrderedDict()

    def register(self, centroid):
        self.tracked_objects[self.next_object_id] = TrackedObject(
            self.next_object_id, centroid
        )
        self.next_object_id += 1

    def deregister(self, object_id):
        if not self.tracked_objects[object_id].counted:
            self.disappeared_counter += 1
        del self.tracked_objects[object_id]

    def update(self, rects):
        if len(rects) == 0:
            for object_id in list(self.tracked_objects.keys()):
                self.tracked_objects[object_id].disappear += 1
                if self.tracked_objects[object_id].disappear > self.max_disappearance:
                    self.deregister(object_id)

            return list(self.tracked_objects.values())

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (start_x, start_y, end_x, end_y)) in enumerate(rects):
            c_x = int(start_x + (end_x / 2.0))
            c_y = int(start_y + (end_y / 2.0))
            input_centroids[i] = (c_x, c_y)

        if len(self.tracked_objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i])

        else:
            object_ids = list(self.tracked_objects.keys())
            object_centroids = [
                o.get_centroid() for o in list(self.tracked_objects.values())
            ]

            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                if D[row, col] > self.max_distance:
                    continue

                object_id = object_ids[row]
                self.tracked_objects[object_id].set_new_centroid(input_centroids[col])
                self.tracked_objects[object_id].disappear = 0

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.tracked_objects[object_id].disappear += 1

                    if (
                        self.tracked_objects[object_id].disappear
                        > self.max_disappearance
                    ):
                        self.deregister(object_id)

            else:
                for col in unused_cols:
                    self.register(input_centroids[col])

        return list(self.tracked_objects.values())