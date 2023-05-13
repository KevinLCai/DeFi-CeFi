from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def __init__(self, df, **kwargs):
        pass
    
    @abstractmethod
    def next(self):
        pass
