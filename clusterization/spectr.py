from copy import deepcopy
from clusterization.clusterizer import Clusterizer
from model.point import Point
import heapq

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