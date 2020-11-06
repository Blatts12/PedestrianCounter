import cv2
import dlib
from Project.PedestrianCounter.Tracking.ITracker import ITracker
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh


class CorrelationTracker(ITracker, IGeneratorBase):
    name = "Correlation"
    values = {"Empty": vh()}

    def __init__(self):
        self.trackers = None

    def new_tracker(self):
        self.trackers = []

    def add_tracker(self, frame, box):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tracker = dlib.correlation_tracker()
        rect = dlib.rectangle(box[0], box[1], box[0] + box[2], box[1] + box[3])
        tracker.start_track(rgb, rect)
        self.trackers.append(tracker)

    def update_trackers(self, frame):
        boxes = []
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        for tracker in self.trackers:
            tracker.update(rgb)
            pos = tracker.get_position()
            start_x = int(pos.left())
            start_y = int(pos.top())
            end_x = int(pos.right())
            end_y = int(pos.bottom())
            boxes.append((start_x, start_y, end_x, end_y))
        return boxes
