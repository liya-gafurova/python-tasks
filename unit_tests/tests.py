import unittest
from decimal import Decimal

from unit_tests.functions import Triangle

"""
Список подобных готовых функций такой:

setUp – подготовка прогона теста; вызывается перед каждым тестом.
tearDown – вызывается после того, как тест был запущен и результат записан. Метод запускается даже в случае исключения (exception) в теле теста.
setUpClass – метод вызывается перед запуском всех тестов класса.
tearDownClass – вызывается после прогона всех тестов класса.
setUpModule – вызывается перед запуском всех классов модуля.
tearDownModule – вызывается после прогона всех тестов модуля.
"""


class GeometricTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """
        Метод def setUp(self) вызывается ПЕРЕД каждым тестом.
        :return:
        """
        self.triangle = Triangle(0, 0, 0, 3, 2, 0)

    def tearDown(self) -> None:
        """
        Метод def tearDown(self) вызывается ПОСЛЕ каждого теста
        :return:
        """
        pass

    @staticmethod
    def _round(number: float, format: str):
        number = Decimal(number)
        return number.quantize(Decimal(format))

    def test_get_area(self):
        expected_area = self._round(4.0, "0.00")
        triangle_area = self._round(self.triangle.get_area(), "0.00")
        self.assertEqual(triangle_area, expected_area)

    def test_get_perimeter(self):
        expected_perimeter = self._round(8.61, "0.00")
        triangle_perimeter = self._round(self.triangle.get_perimeter(), "0.00")
        self.assertEqual(triangle_perimeter, expected_perimeter)