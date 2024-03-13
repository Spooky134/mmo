from clusterization.methods.clusterizer import Clusterizer
from model.point import Point
import networkx as nx

class GraphAlgo(Clusterizer):
    def __init__(self, points_dataset: list[Point], count_cluster: int) -> None:
        super().__init__(points_dataset, count_cluster)

    def evalute() -> None:
        pass