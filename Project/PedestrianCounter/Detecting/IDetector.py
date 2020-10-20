from abc import ABC, abstractmethod, abstractproperty


class IDetectorWithModel(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def __init__(self, confidenceThreshold=0.45):
        pass

    @abstractmethod
    def processFrame(self, frame, frameWidth, frameHeight):
        """
        returns [(startX, startY, width, height),...]
        """
        pass

    @abstractmethod
    def setConfidenceThreshold(self, conf):
        pass

    @abstractmethod
    def setModelPath(self, path, name):
        pass
