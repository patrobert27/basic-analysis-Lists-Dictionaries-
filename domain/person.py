from abc import ABC, abstractmethod   

class Person(ABC):
    
    @abstractmethod
    def to_dict(self):
        raise NotImplementedError
        # Why not use pass?
        # NotImplementedError is better because it clearly indicates
        # that this method must be implemented in subclasses
        # If a subclass does not implement it, an error will be raised
