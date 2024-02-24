from abc import ABC, abstractstaticmethod
from generatorId import GenerarorID
from point import Point



class Classifier(ABC):
    def __init__(self, dataset: list[Point], zero_point: Point) -> None:
        self._dataset = dataset[:]
        self._data = None
        self._zero_point = zero_point

    @property
    def dataset(self):
        return self._dataset
    
    @property
    def data(self):
        return self._data
    
    @property
    def zero_point(self):

        return self._zero_point
    
    @zero_point.setter
    def zero_point(self, point):
        self._zero_point = point 
    
    @abstractstaticmethod
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
    def __init__(self, points_dataset: list[Point]) -> None:
        self._dataset = points_dataset[:]
    

    def find_point(self, point_id: int) -> Point:
        for point in self.__dataset:
            if point.id_point == point_id:
                return point
            
        return None


class SpektrAlgo(Clusterizer):
    pass


class UnionAlgo(Clusterizer):
    pass


class GraphAlgo(Clusterizer):
    pass
    
    

