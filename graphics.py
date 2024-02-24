import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from point import Point
from matplotlib.patches import Circle
from abc import ABC, abstractmethod


class Graphic2D(ABC):
    @abstractmethod
    def draw(self):
        pass


class ReferenceMethodGraphic(Graphic2D):
    def __init__(self, points: list[Point], data: dict) -> None:
        self.__data = data 
        self.__points = points
        
        unique_labels = np.unique([point.label for point in self.__points])
        self.__colors = {label: plt.cm.viridis(i / len(unique_labels)) for i, label in enumerate(unique_labels)}


    def draw(self):
        for point in self.__points:
            color = self.__colors[point.label]
            plt.scatter(*point.coords, color=color, marker='o', label=point.label)
            plt.annotate(point.label, (point.coords[0], point.coords[1]), textcoords="offset points", xytext=(0,10), ha='center')
        

        for mid_point in self.__data['mid_points']:
                plt.scatter(*mid_point.coords, color='black', marker='+', s=200)
                plt.plot([self.__data['zero_point'].coords[0], mid_point.coords[0]],
                        [self.__data['zero_point'].coords[1], mid_point.coords[1]],  color='black')

        plt.scatter(*self.__data['zero_point'].coords, label=self.__data['zero_point'].label, color='yellow', marker='o', s=100)
        plt.annotate(self.__data['zero_point'].label, 
                    (self.__data['zero_point'].coords[0], self.__data['zero_point'].coords[1]),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
        
        plt.title('graphics')
        plt.show()

class KMeansMethodGraphic(Graphic2D):
    def __init__(self, points: list[Point], data: dict) -> None:
        self.__data = data 
        self.__points = points
        
        unique_labels = np.unique([point.label for point in self.__points])
        self.__colors = {label: plt.cm.viridis(i / len(unique_labels)) for i, label in enumerate(unique_labels)}

    def draw(self):
        for point in self.__points:
            color = self.__colors[point.label]
            plt.scatter(*point.coords, color=color, marker='o', label=point.label)
            plt.annotate(point.label, (point.coords[0], point.coords[1]), textcoords="offset points", xytext=(0,10), ha='center')
        
        for mean_point in self.__data['k_means']:
            plt.plot([self.__data['zero_point'].coords[0], mean_point.coords[0]],
                     [self.__data['zero_point'].coords[1], mean_point.coords[1]],  color='black')

        plt.scatter(*self.__data['zero_point'].coords, label=self.__data['zero_point'].label, color='yellow', marker='o', s=100)
        plt.annotate(self.__data['zero_point'].label, (self.__data['zero_point'].coords[0], self.__data['zero_point'].coords[1]), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('graphics')
        plt.show()

class ParzenWindowMethodGraphic(Graphic2D):
    def __init__(self, points: list[Point], data: dict) -> None:
        self.__data = data 
        self.__points = points
        
        unique_labels = np.unique([point.label for point in self.__points])
        self.__colors = {label: plt.cm.viridis(i / len(unique_labels)) for i, label in enumerate(unique_labels)}

    def draw(self):
        fig, ax = plt.subplots()
        circle = Circle(self.__data['zero_point'].coords, self.__data['radius'], edgecolor='black', facecolor='none', linewidth=2)
        ax.add_patch(circle)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
     
        plt.scatter(*self.__data['zero_point'].coords, label=self.__data['zero_point'].label, color='yellow', marker='o', s=100)
        plt.annotate(self.__data['zero_point'].label, (self.__data['zero_point'].coords[0], self.__data['zero_point'].coords[1]), textcoords="offset points", xytext=(0,10), ha='center')

        for point in self.__points:
            color = self.__colors[point.label]
            plt.scatter(*point.coords, color=color, marker='o', label=point.label)
            plt.annotate(point.label, (point.coords[0], point.coords[1]), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('graphics')
        plt.show()


def draw_2D_graphics(self):
        for point in self.__points:
            color = self.__colors[point.label]
            plt.scatter(*point.coords, color=color, marker='o', label=point.label)
            plt.annotate(point.label, (point.coords[0], point.coords[1]), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('graphics')
        plt.show()

def draw_3D_graphics(self):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for point in self.__points:
        color = self.__colors[point.class_point]
        ax.scatter(*point.coords, color=color, marker='o', label=point.class_point)
        ax.text(*point.coords, point.class_point)

    ax.set_title('graphics')
    plt.show()