from abc import ABC, abstractmethod, abstractproperty


class IGeneratorComponent(ABC):
    @property
    @abstractproperty
    def has_buddy(self):
        raise NotImplementedError

    @abstractmethod
    def get_widget(self):
        raise NotImplementedError

    @abstractmethod
    def get_buddy(self, name=""):
        pass