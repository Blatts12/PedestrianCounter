from abc import ABC, abstractmethod


class IDetectorWithModel(ABC):
    @abstractmethod
    def __init__(self, confidenceThreshold=0.45):
        pass

    @abstractmethod
    def processFrame(self, frame, frameWidth, frameHeight):
        pass

    @abstractmethod
    def setConfidenceThreshold(self, conf):
        pass

    @abstractmethod
    def setModelPath(self, path, name):
        pass
