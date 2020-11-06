from abc import ABC, abstractmethod, abstractproperty


class IGeneratorBase(ABC):
    @property
    @abstractproperty
    def values(self):
        raise NotImplementedError

    """
        values = {
            name: (value, (desc), value set modifier)
            "Confidence": (50, ("Slider", 0, 100, 50, "%"), lambda value: value / 100)
        }
    """