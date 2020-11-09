from abc import ABC, abstractmethod, abstractproperty


class IDetector(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def process_frame(self, frame, frame_width, frame_height):
        """
        returns [(startX, startY, width, height),...]
        """
        raise NotImplementedError

    @abstractmethod
    def activate(self):
        raise NotImplementedError