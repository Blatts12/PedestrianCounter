from abc import ABC, abstractmethod, abstractproperty


class IGeneratorBase(ABC):
    @property
    @abstractproperty
    def values(self):
        raise NotImplementedError

    """
        values = {
            name: (value, (desc))
            "Confidence": (50, ("Slider", 0, 100, 50, "%"))
        }
    """

    @abstractmethod
    def setValue(self, name, value):
        pass

    @abstractmethod
    def getValue(self, name):
        pass