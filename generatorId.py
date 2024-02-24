from abc import ABC, abstractmethod

class GenerarorID:
    def __init__(self, ids: list[int]=None) -> None:
        if ids != None:
            self.__count_id = max(ids)
        else:
            self.__count_id = 0
            

    def generate_id(self):
        self.__count_id += 1
        return self.__count_id
