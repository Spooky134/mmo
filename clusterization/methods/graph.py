from clusterization.methods.clusterizer import Clusterizer
from model.point import Point
import networkx as nx

class GraphAlgo(Clusterizer):
    def __init__(self, points_dataset: list[Point], count_cluster: int) -> None:
        super().__init__(points_dataset, count_cluster)

    def evalute(self) -> None:
        # Создаем граф
        G = nx.Graph()

        # Добавляем вершины
        G.add_nodes_from(self.dataset)

        # Добавляем рёбра
        G.add_edges_from([(1, 2), (2, 3), (3, 1), (4, 5)])
        G.add_edges_from()
        # Находим компоненты связности
        components = list(nx.connected_components(G))

        # Выводим компоненты связности
        for idx, component in enumerate(components):
            print(f"Компонента связности {idx + 1}: {component}")

        self.data['labels'] = [point.label for point in self.dataset]
