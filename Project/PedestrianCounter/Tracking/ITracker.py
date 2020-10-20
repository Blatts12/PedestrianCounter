from abc import ABC, abstractmethod, abstractproperty


class ITracker(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

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
