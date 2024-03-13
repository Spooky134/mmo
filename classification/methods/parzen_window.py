from classification.methods.classifier import Classifier
from model.point import Point
from utils.generatorId import GenerarorID



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