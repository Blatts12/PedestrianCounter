from abc import ABC, abstractmethod, abstractproperty


class ISource(ABC):
    @property
    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def ready_for_start(self):
        raise NotImplementedError

    @abstractmethod
    def read_frame(self):
        raise NotImplementedError

    @abstractmethod
    def start_cap(self):
        raise NotImplementedError

    @abstractmethod
    def stop_cap(self):
        raise NotImplementedError