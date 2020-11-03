from Project.PedestrianCounter.Tracking.ITracker import ITracker
from Project.Components.Generator.IGeneratorBase import IGeneratorBase
import cv2


class KCFTracker(ITracker, IGeneratorBase):
    name = "KCF"
    values = {"None": [None, ("None")]}

    def set_value(self, name, value):
        self.values[name][0] = self.values[name][2](value)

    def __init__(self):
        self.trackers = None

    def new_tracker(self):
        self.trackers = cv2.MultiTracker_create()

    def add_tracker(self, frame, box):
        self.trackers.add(cv2.TrackerKCF_create(), frame, box)

    def update_trackers(self, frame):
        success, boxes = self.trackers.update(frame)
        return boxes