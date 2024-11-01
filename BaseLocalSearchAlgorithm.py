from abc import ABC, abstractmethod
from Cube import Cube
from typing import Type

class BaseLocalSearchAlgorithm(ABC):
    def __init__(self, cube: Cube):
        self.cube = cube
    
    @abstractmethod
    def run(self):
        pass
    
