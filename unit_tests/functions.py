from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    x: float
    y: float


class Geometric(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def _get_side_length(point1: Point, point2: Point):
        return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @abstractmethod
    def get_area(self):
        pass

    @abstractmethod
    def get_perimeter(self):
        pass


class Triangle(Geometric):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        A = Point(x1, y1)
        B = Point(x2, y2)
        C = Point(x3, y3)

        self.ab = self._get_side_length(A, B)
        self.ac = self._get_side_length(A, C)
        self.bc = self._get_side_length(B, C)

    def get_area(self):
        """
        Формула Герона: S = sqrt(p(p-a)(p-b)(p-c))
        :return:
        """
        p = self._get_half_perimeter()
        s = sqrt(p * (p - self.ab) * (p - self.bc) * (p - self.ac))
        return s

    def get_perimeter(self):
        return sum([self.ab, self.bc, self.ac])

    def _get_half_perimeter(self):
        return self.get_perimeter() / 2


