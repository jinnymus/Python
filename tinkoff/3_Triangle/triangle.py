#!/usr/bin/python3

'''
Задание:

Есть интерфейс:
public interface ITriangle {
int getX1();
int getY1();
int getX2();
int getY2();
int getX3();
int getY3();
}
Методы возвращают 6 чисел — координаты трех вершин прямоугольного треугольника в
декартовой системе координат.
Есть метод, возвращающий прямоугольный треугольник:
public final class ITriangleProvider {
public static ITriangle getTriangle() {
...
}
}
Напишите JUnit-тесты, которые будут проверять, действительно ли метод getTriangle()
возвращает прямоугольный треугольник.

'''

import logging
import sys
import unittest
import math


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

class ITriangle():
    '''
    Class that return triangle object
    '''
    def __init__(self):
        self.X1 = 0
        self.Y1 = 0
        self.X2 = 2
        self.Y2 = 2
        # self.X2 = 1
        # self.Y2 = 3
        self.X3 = 4
        self.Y3 = 0


def getTriangle():
    '''

    :return: ITriangle return trianlge object
    '''
    return ITriangle()


class TestTriangle(unittest.TestCase):
    '''

    Test class

    '''

    @classmethod
    def setUpClass(cls):
        '''
        get triangle once for test suite
        '''
        cls.triangle = cls.triagle_extended()

    class triagle_extended():
        def __init__(self):
            '''
            Get basic triangle and add sides
            '''
            self.triangle = getTriangle()
            self.A = math.sqrt((self.triangle.X2 - self.triangle.X1) ** 2 + (self.triangle.Y2 - self.triangle.Y1) ** 2)
            self.B = math.sqrt((self.triangle.X3 - self.triangle.X2) ** 2 + (self.triangle.Y3 - self.triangle.Y2) ** 2)
            self.C = math.sqrt((self.triangle.X3 - self.triangle.X1) ** 2 + (self.triangle.Y3 - self.triangle.Y1) ** 2)
            sides = [self.A, self.B, self.C]
            sides.sort(reverse=True)
            self.hypot = sides[0]
            self.sides = sides
            logging.debug('A: ' + str(self.A))
            logging.debug('B: ' + str(self.B))
            logging.debug('C: ' + str(self.C))
            logging.debug('hypot: ' + str(self.hypot))
            logging.debug('sides: ' + str(self.sides))

    def test_sides(self):
        '''
        Test that sum of two sides more than third
        '''
        msg = 'this is not triagle, sides assert'
        self.assertGreater(self.triangle.A + self.triangle.B, self.triangle.C, msg)
        self.assertGreater(self.triangle.A + self.triangle.C, self.triangle.B, msg)
        self.assertGreater(self.triangle.C + self.triangle.B, self.triangle.A, msg)


    def test_angles(self):
        '''
        Test summ of angles
        '''
        msg = 'this is not triagle, 90 angle assert'
        angle1 = math.degrees(math.asin(self.triangle.sides[1] / self.triangle.sides[0]))
        angle2 = math.degrees(math.asin(self.triangle.sides[1] / self.triangle.sides[0]))
        self.assertEqual(round(angle1 + angle2), 90, msg)


    def test_pifagor(self):
        '''

        Test pifagor theory

        '''
        msg = 'this is not triagle, pifagor assert'
        self.assertEqual(math.sqrt((self.triangle.sides[1]) ** 2 + (self.triangle.sides[2]) ** 2), self.triangle.sides[0], msg)

if __name__ == '__main__':
    unittest.main()