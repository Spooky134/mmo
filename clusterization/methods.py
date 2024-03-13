from abc import ABC, abstractmethod
from copy import deepcopy
from model.point import Point
import heapq
import networkx as nx


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
        

class SpektrAlgo(Clusterizer):
    def __init__(self, dataset: list[Point], id_start_point: int=1, count_cluster: int=2) -> None:
        super().__init__(deepcopy(dataset), count_cluster)
        self.id_start_point = id_start_point
    
    @property
    def id_start_point(self):
        return self._id_start_point
    
    @id_start_point.setter
    def id_start_point(self, id_start_point: int):
        self._id_start_point = id_start_point

    def evalute(self) -> None:
        start_point = self.__find_point_by_id(self.id_start_point)
        dataset = [point for point in self.dataset if point != start_point]
        points_que = [start_point]
        start_points = [start_point]
        differences = []
        distances = []
        
        while dataset:
            min_dist = None
            near_point = None 
            for point in dataset:
                dist = Point.distance_between_points(start_point, point)
                if min_dist is None or dist < min_dist :
                    min_dist = dist
                    near_point = point

            distances.append(min_dist)
            points_que.append(near_point)
            dataset = [point for point in dataset if point != near_point]

            start_point = Point.mid_point(*points_que)
            start_points.append(start_point)

        differences = [abs(next_dist - prev_dist) for prev_dist, next_dist in zip(distances[:-1], distances[1:])]

        step_up_values = heapq.nlargest(self.count_cluster - 1, differences)
        step_up_indexs = [differences.index(value)+1 for value in step_up_values]
        step_up_indexs.sort()

        intervals = [0, *step_up_indexs, len(points_que)]
        
        labels = []
        for i in range(len(intervals)-1):
            for j in range(intervals[i], intervals[i+1]):
                # points_que[j].label = str(i+1)
                labels.append(str(i+1))


        self._data['labels'] = labels
        self._data['distances'] = ['-'] + distances
        self._data['differences'] = ['-'] + differences
        self._data['query'] = [point.id_point for point in points_que]
        self._data['count cluster'] = [self.count_cluster]

    def __find_point_by_id(self, id: int) -> Point:
        left = 0
        right = self.size - 1

        while left <= right:
            mid = (left + right) // 2
            if self.dataset[mid].id_point == id:
                return self.dataset[mid]
            elif self.dataset[mid].id_point < id:
                left = mid + 1
            else:
                right = mid - 1

        return -1


class UnionAlgo(Clusterizer):
    def __init__(self, dataset: list[Point], count_cluster: int=2) -> None:
        super().__init__(deepcopy(dataset), count_cluster)
    
    def evalute(self) -> None:
        steps = []
        clusters = []
        for point in self.dataset:
            clusters.append([point])
        steps.append([[point.id_point] for point in self.dataset])

        for _ in range(self.size - self.count_cluster):
            nearest_cluster = None
            min_dist = None
            for i, first_cluster in enumerate(clusters):
                first_center = Point.mid_point(*first_cluster)
                for second_cluster in clusters[i+1:]:
                    second_centr = Point.mid_point(*second_cluster)
                    dist = Point.distance_between_points(first_center, second_centr)
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        nearest_cluster = (first_cluster, second_cluster)
            
            clusters = [cluster for cluster in clusters if cluster not in nearest_cluster]
            clusters.append(nearest_cluster[0] + nearest_cluster[1])

            all_ids = []
            for cluster in clusters:
                all_ids.append([point.id_point for point in cluster])
            steps.append(all_ids)

        labels = []
        for i, cluster in enumerate(clusters):
            for point in cluster:
                labels.append(str(i+1))

        self._data['labels'] = labels

        for step in steps:
            print(step)


class GraphAlgo(Clusterizer):
    def __init__(self, points_dataset: list[Point], count_cluster: int) -> None:
        super().__init__(points_dataset, count_cluster)

    def evalute() -> None:

        for i, first_cluster in enumerate(clusters):
                for second_cluster in clusters[i+1:]:
                    second_centr = Point.mid_point(*second_cluster)
                    dist = Point.distance_between_points(first_center, second_centr)
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        nearest_cluster = (first_cluster, second_cluster)