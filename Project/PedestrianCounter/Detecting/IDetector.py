from abc import ABC, abstractmethod, abstractproperty


class IDetectorWithModel(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_frame(self, frame, frame_width, frame_height):
        """
        returns [(startX, startY, width, height),...]
        """
        pass

    @abstractmethod
    def set_model_path(self, path, name):
        pass
