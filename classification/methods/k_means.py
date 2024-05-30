from classification.methods.classifier import Classifier
from model.point import Point
from utils.generatorId import GenerarorID


class KMeans(Classifier):
    # вынести zeropoint из конструктора и закинуть в метод вычесления
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


# сохранение обьекта происходит с помощью создания класса сохранения типо датафрейма или датафрейма есть базовый класс котороый можно сохранять классом для сохранения