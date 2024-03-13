from classification.classifier import Classifier
from model.point import Point
from utils.generatorId import GenerarorID


class Standard(Classifier):
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