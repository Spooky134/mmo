from abc import ABC, abstractmethod
from copy import deepcopy
from generatorId import GenerarorID
from point import Point



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
    

class ReferenceMethod(Classifier):
    def __init__(self, zero_point: Point, dataset: list[Point]) -> None:
        super().__init__(dataset, zero_point)

    def evalute(self):
        self._data = dict()
        mid_points = self.__calculate_mid_points(self.dataset)

        mid_point_distance = []
        for mid_point in mid_points:
            mid_point_distance.append((mid_point,
                                       Point.distance_between_points(self.zero_point, mid_point)))

        self.zero_point.label = min(mid_point_distance, key=lambda x: x[1])[0].label

        gen_id = GenerarorID([point.id_point for point in self._dataset])
        self.zero_point.id_point = gen_id.generate_id()

        self._data['zero_point'] = self.zero_point
        self._data['mid_points'] = [el[0] for el in mid_point_distance]
        self._data['distances'] = [el[1] for el in mid_point_distance]

    def __calculate_mid_points(self, points: list[Point]) -> list[Point]:
        groups = self.group_points(points)

        mid_points = []
        for label in groups:
            mid_points.append(Point.mid_point(*groups[label]))
            
        return mid_points


class ParzenWindow(Classifier):
    def __init__(self, dataset: list[Point], zero_point: Point, radius: float=0) -> None:
        super().__init__(dataset, zero_point)
        self.__radius = radius

    @property
    def radius(self):

        return self.__radius
    
    @radius.setter
    def radius(self, r: float):
        self.__radius = r

    def evalute(self):
        points_distance = []
        self._data = dict()

        for point in self.dataset:
            points_distance.append((point,
                                    Point.distance_between_points(self.zero_point, point)))
            
        self._data['distances_all'] = [el[1] for el in points_distance]
        
        points_distance = list(filter(lambda x: x[1] and x[1] < self.radius, points_distance))

        if len(points_distance) == 0:
            raise Exception(f'the radius should be larger')
            
        class_count = self.count_different_points([el[0] for el in points_distance])
        
        self.zero_point.label = max(class_count, key=lambda label: class_count[label])
        
        gen_id = GenerarorID([point.id_point for point in self._dataset])
        self.zero_point.id_point = gen_id.generate_id()

        self._data['zero_point'] = self.zero_point
        self._data['points_in_window'] = [el[0] for el in points_distance]
        self._data['distances_in_window'] = [el[1] for el in points_distance]
        self._data['class_count'] = class_count
        self._data['radius'] = self.radius


class KMeans(Classifier):
    def __init__(self, dataset: list[Point], zero_point: Point, k: int=3) -> None:
        super().__init__(dataset, zero_point)
        self.__k = k

    @property
    def k(self):

        return self.__k
    
    @k.setter
    def k(self, k):
        self.__k = k

    def evalute(self):
        self._data = dict()
        points_distance = []

        for point in self.dataset:
            points_distance.append((point,
                                    Point.distance_between_points(self.zero_point, point)))
        
        self._data['distances_all'] = [el[1] for el in points_distance]

        points_distance.sort(key=lambda x: x[1])
        points_distance = list(filter(lambda x: x[1], points_distance))
        
        if self.k <= len(points_distance):
            k_means = points_distance[:self.k]
        else:
            raise Exception(f'k may be <= {len(points_distance)}')
        
        class_count = self.count_different_points([el[0] for el in k_means])
        
        self.zero_point.label = max(class_count, key=lambda label: class_count[label])
        
        gen_id = GenerarorID([point.id_point for point in self._dataset])
        self.zero_point.id_point = gen_id.generate_id()

        self._data['zero_point'] = self.zero_point
        self._data['k_means'] = [el[0] for el in k_means]
        self._data['distances'] = [el[1] for el in k_means]
        self._data['class_count'] =  class_count


class Clusterizer(ABC):
    def __init__(self, points_dataset: list[Point], count_cluster: int) -> None:
        self.dataset = points_dataset
        self.count_cluster = count_cluster
        self._data=None

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
        dataset = self.dataset[:]
        start_point = self.__find_point_by_id(self.id_start_point)
        dataset.remove(start_point)
        points_que = [start_point]
        differences = []
        min_distances = []
        clusters = []
        
        while len(dataset) != 0: 
            buffer = dict()
            for point in dataset:
                buffer[point.id_point] = Point.distance_between_points(start_point, point)

            id_near_point = min(buffer, key=lambda k: buffer[k])
            min_distances.append(buffer[id_near_point])

            near_point = self.__find_point_by_id(id_near_point)

            points_que.append(near_point)
            dataset.remove(near_point)

            start_point = Point.mid_point(*points_que)

        for i in range(1, len(min_distances)-1):
            differences.append(min_distances[i] - min_distances[i-1])
        
        step_up_indexs = []
        buf_diff = sorted(differences, reverse=True)
        step_up_values = buf_diff[:self.count_cluster - 1]
        for step_value in step_up_values:
            step_up_indexs.append(differences.index(step_value))

        step_up_indexs.sort()

        intervals = [0, *step_up_indexs, len(points_que)]

        for i in range(len(intervals)-1):
            clusters.append(points_que[intervals[i]:intervals[i+1]])

        for i, cluster in enumerate(clusters, start=1):
            for point in cluster:
                point.label = str(i)
        points = sum(*clusters)
        
        print([point.id_point for point in points])
    


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
    pass


class GraphAlgo(Clusterizer):
    pass
    
    

