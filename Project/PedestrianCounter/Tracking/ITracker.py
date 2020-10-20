from abc import ABC, abstractmethod


class ITracker(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def newTracker(self):
        pass

    @abstractmethod
    def addTracker(self, frame, box):
        pass

    @abstractmethod
    def updateTrackers(self, frame):
        pass
