from abc import ABC, abstractmethod, abstractproperty


class ITracker(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def new_tracker(self):
        raise NotImplementedError

    @abstractmethod
    def add_tracker(self, frame, box):
        raise NotImplementedError

    @abstractmethod
    def update_trackers(self, frame):
        raise NotImplementedError
