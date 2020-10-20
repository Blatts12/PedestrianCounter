from Project.PedestrianCounter.Tracking.ITracker import ITracker
import cv2
import dlib


class CorrelationTracker(ITracker):
    name = "correlation"

    def __init__(self):
        self.trackers = None

    def newTracker(self):
        self.trackers = []

    def addTracker(self, frame, box):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tracker = dlib.correlation_tracker()
        rect = dlib.rectangle(box[0], box[1], box[0] + box[2], box[1] + box[3])
        tracker.start_track(rgb, rect)
        self.trackers.append(tracker)

    def updateTrackers(self, frame):
        boxes = []
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        for tracker in self.trackers:
            tracker.update(rgb)
            pos = tracker.get_position()
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            boxes.append((startX, startY, endX, endY))
        return boxes
