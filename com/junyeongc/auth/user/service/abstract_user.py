from abc import ABCMeta, abstractmethod


class AbstractUser(metaclass=ABCMeta):
    
    @abstractmethod
    def handle(self, **kwargs):
        pass
