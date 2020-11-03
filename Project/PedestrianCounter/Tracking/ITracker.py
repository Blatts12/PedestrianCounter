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
    def new_tracker(self):
        pass

    @abstractmethod
    def add_tracker(self, frame, box):
        pass

    @abstractmethod
    def update_trackers(self, frame):
        pass
