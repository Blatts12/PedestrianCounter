import cv2
from Project.PedestrianCounter.Tracking.ITracker import ITracker
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase


class KCFTracker(ITracker, IGeneratorBase):
    name = "KCF"
    values = {}

    def __init__(self):
        self.trackers = None

    def new_tracker(self):
        self.trackers = cv2.MultiTracker_create()

    def add_tracker(self, frame, box):
        self.trackers.add(cv2.TrackerKCF_create(), frame, box)

    def update_trackers(self, frame):
        success, boxes = self.trackers.update(frame)
        return boxes