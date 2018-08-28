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

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')
