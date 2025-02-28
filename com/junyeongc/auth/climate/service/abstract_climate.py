

from abc import ABCMeta, abstractmethod


class AbstractClimate(ABCMeta):
    
    @abstractmethod
    def handle(self, **kwargs):
        pass