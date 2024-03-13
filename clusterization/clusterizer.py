from abc import ABC, abstractmethod
from copy import deepcopy
from model.point import Point

class Clusterizer(ABC):
    def __init__(self, points_dataset: list[Point], count_cluster: int) -> None:
        self.dataset = points_dataset
        self.count_cluster = count_cluster
        self._data=dict()

    @property
    def count_cluster(self):
        return self._count_cluster
    
    @count_cluster.setter
    def count_cluster(self, cluster_count: int):
        self._count_cluster = cluster_count

    @property
    def dataset(self):
        return self._dataset
    
    @dataset.setter
    def dataset(self, dataset: list[Point]):
        dataset = deepcopy(dataset)
        self._dataset = sorted(dataset, key=lambda point: point.id_point)
        self._size = len(self.dataset)

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size

    @abstractmethod
    def evalute() -> None:
        pass