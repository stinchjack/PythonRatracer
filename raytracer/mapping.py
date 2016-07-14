import math
import gmpy2
from PIL import Image


class MappedImage:

    def colour(self, uv_tuple):
        return None


class MappedPILImage(MappedImage):

    __image = None

    def __init__(self, filename):
        self.__image__ = Image.open(filename)
        self.__pixels__ = self.__image__.load()

    def colour(self, uv_tuple):
        x = uv_tuple[0] * self.__image__.width
        y = uv_tuple[1] * self.__image__.height
        clr = self.__pixels__[x, y]

        return ('colour', clr[0] / 255.0, clr[1] / 255.0, clr[2] / 255.0)


def sphere_map_to_rect(shape, intersect_result):
    p = intersect_result['raw_point']
    a1 = math.degrees(math.asin(p[1]))
    if (p[1] >= 0 and p[3] >= 0):
        a1 = (90.0 - a1) + 90.0
    elif (p[1] <= 0 and p[3] <= 0):
        a1 = (-90.0 - a1) - 90.0

    a1 = a1 + 180.0

    x = a1 / mprf(360.0)
    y = p[2]
