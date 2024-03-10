class Point():
    __slots__ = ('__id_point', '__label', '__coords')

    def __init__(self, coords: tuple, id_point: int=0, label: str='') -> None:
        self.__id_point = id_point
        self.__label = label
        self.__coords = coords[:]
    
    @property
    def id_point(self) -> int:

        return self.__id_point
    
    @id_point.setter
    def id_point(self, id_point: int):
        self.__id_point = id_point
    
    @property
    def label(self) -> int:

        return self.__label
    
    @label.setter
    def label(self, label: int):
        self.__label = label

    @property
    def coords(self) -> tuple:

        return self.__coords
    
    @coords.setter
    def coords(self, coords: tuple):
        self.__coords = coords[:]

    def __str__(self) -> str:

        return f'{self.id_point} | {self.label} | {self.coords}'
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Point):
            return self.id_point == value.id_point \
                and self.label == value.label \
                and self.coords == value.coords
        
        return False

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)
    
    @property
    def line(self) -> tuple:
        
        return [self.id_point, *self.coords, self.label]

    @classmethod
    def check_values():
        pass

    @staticmethod
    def distance_between_points(first_point, second_point) -> float:
        distance = 0
        for first_point_cord, second_point_cord in zip(first_point.coords, second_point.coords):
            distance += (first_point_cord - second_point_cord) ** 2

        return distance ** 0.5
    
    @staticmethod
    def mid_point(*points):
        if len(points)==1:
            return point
        coords = [0] * len(points[0].coords)
        for point in points:
            for i, coord in enumerate(point.coords):
                coords[i] += coord
        points_size = len(points)
        for i, coord in enumerate(coords):
            coords[i] = coord / points_size
          
        return Point(coords=coords,
                     label=points[0].label)
    