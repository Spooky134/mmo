from abc import ABC, abstractmethod
from copy import deepcopy
from model.point import Point


class Classifier(ABC):
    def __init__(self, dataset: list[Point], zero_point: Point) -> None:
        self.dataset = dataset
        self._data = None
        self.zero_point = zero_point

    @property
    def dataset(self):
        return self._dataset
    
    @dataset.setter
    def dataset(self, dataset):
        self._dataset = deepcopy(dataset)
    
    @property
    def data(self):
        return self._data
    
    @property
    def zero_point(self):

        return self._zero_point
    
    @zero_point.setter
    def zero_point(self, point):
        self._zero_point = point 
    
    @abstractmethod
    def evalute(self):
        pass

    @staticmethod
    def count_different_points(points: list[Point]) -> dict[str, int]:
        groups = Classifier.group_points(points)
        for label in groups:
            groups[label] = len(groups[label])

        return groups
    
    
    @staticmethod
    def group_points(points: list[Point]) -> dict[str, list[Point]]:
        groups = dict()

        for point in points:
            if point.label not in groups:
                groups[point.label] = [point]
            else:
                groups[point.label].append(point)
    
        return groups