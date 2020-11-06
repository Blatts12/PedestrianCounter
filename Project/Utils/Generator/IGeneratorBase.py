from abc import ABC, abstractmethod, abstractproperty


class IGeneratorBase(ABC):
    @property
    @abstractproperty
    def values(self):
        raise NotImplementedError