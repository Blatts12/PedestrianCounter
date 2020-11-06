from abc import ABC, abstractmethod, abstractproperty


class ISource(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def ready_for_start(self):
        pass

    @abstractmethod
    def read_frame(self):
        pass

    @abstractmethod
    def start_cap(self):
        pass

    @abstractmethod
    def stop_cap(self):
        pass