from Project.PedestrianCounter.Tracking.ITracker import ITracker
import cv2


class KCFTracker(ITracker):
    def __init__(self):
        self.trackers = None

    def newTracker(self):
        self.trackers = cv2.MultiTracker_create()

    def addTracker(self, frame, box):
        self.trackers.add(cv2.TrackerKCF_create(), frame, box)

    def updateTrackers(self, frame):
        success, boxes = self.trackers.update(frame)
        return boxes