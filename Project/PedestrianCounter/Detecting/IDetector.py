from abc import ABC, abstractmethod, abstractproperty


class IDetectorWithModel(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def __init__(self, confidence=0.45):
        pass

    @abstractmethod
    def processFrame(self, frame, frameWidth, frameHeight):
        """
        returns [(startX, startY, width, height),...]
        """
        pass

    @abstractmethod
    def setConfidence(self, conf):
        pass

    @abstractmethod
    def setNMSThreshold(self, threshold):
        pass

    @abstractmethod
    def setModelPath(self, path, name):
        pass
