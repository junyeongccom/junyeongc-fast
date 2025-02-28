

from abc import ABCMeta, abstractmethod


class AbstractAdmin(ABCMeta):
    
    @abstractmethod
    def handle(self, **kwargs):
        pass