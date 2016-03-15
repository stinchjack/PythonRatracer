from cartesian import *
from colour import *
from matrix import *
from transformation import *


class Shape:

    def __init__(self, colour, reflection, transform=None):
        if transform != None:
            self.setTransform(transform)

        self.basicColour = colour
        self.refelectColour = reflection

    def setTransform(self, transform):

        if isinstance(transform, Transform):
            self.__transform = transform
        elif type(transform) is dict:
            self.__transform = Transform(transform)

        else:
            self.__transform = None

    def transform(self):
        return self.__transform

    def setBasicColour(self, basicColour=None, refelectColour=None):
        self.basicColour = basicColour
        self.refelectColour = refelectColour

    def diffuseColour(self, intersectResult):
        return self.basicColour

    def refelectColour(self, intersectResult):
        return self.refelctColour

    def testIntersect(self, ray):
        transform = self.__transform
        if transform != None:
            result = self.intersect(transform.transform(ray))
            if result != False:

                if 'raw_point' in result:
                    result['raw_intersect_point'] = result['raw_point']
                    result['point'] = transform.inverseTransform(
                        result['raw_point'], True)

                if 'raw_normal' in result:
                    if not ray[RAY_ISSHADOW]:
                        result['normal'] = cartesian_normalise(
                            transform.inverseTransform(result['raw_normal']))

                return result
        else:
            result = self.intersect(ray)
            if result != False:
                if 'raw_normal' in result:
                    result['normal'] = result['raw_normal']
                if 'raw_point' in result:
                    result['point'] = result['raw_point']
                return result

SHAPE_SHAPE = 1
SHAPE_DIFFUSECOLOUR = 2
SHAPE_SPECULARCOLOUR = 3
SHAPE_INTERSECT_FUNC = 4
SHAPE_INSIDE_FUNC = 5
SHAPE_DIFFUSECOLOUR_FUNC = 6
SHAPE_SPECULARCOLOUR_FUNC = 7
SHAPE_TRANSFORM = 8
SHAPE_DATA = 9


def shape_set_transform(shape, transform):
    if isinstance(transform, Transform):
        shape[SHAPE_TRANSFORM] = transform
    elif type(transform) is dict:
        shape[SHAPE_TRANSFORM] = Transform(transform)
    else:
        shape[SHAPE_TRANSFORM] = None


def shape_diffuse_colour(shape, intersectResult):
	if 'colour' in shape[SHAPE_DIFFUSECOLOUR]:
		return shape[SHAPE_DIFFUSECOLOUR]
	else:
		return None

def shape_reflect_colour(shape, intersectResult):
	if 'colour' in shape[SHAPE_SPECULARCOLOUR]:
		return shape[SHAPE_SPECULARCOLOUR]
	else:
		return None

def shape_empty_shape():
    return ['shape', None, None, None, None, None, shape_diffuse_colour, shape_reflect_colour, None, {}]

def shape_point_inside(shape, cartesian):
    if shape[SHAPE_INSIDE_FUNC] != None:
        return shape[SHAPE_INSIDE_FUNC](cartesian)


def shape_test_intersect(shape, ray):
    if shape[SHAPE_TRANSFORM] != None:
        result = shape[SHAPE_INTERSECT_FUNC](
            shape, shape[SHAPE_TRANSFORM].transform(ray))
    else:
        result = shape[SHAPE_INTERSECT_FUNC](shape, ray)

    return result

def shape_reverse_transform(result):
    shape = result['shape']
    if shape[SHAPE_TRANSFORM] != None:
        if 'raw_point' in result:
            result['raw_intersect_point'] = result['raw_point']
            #result['point'] = shape[SHAPE_TRANSFORM].inverseTransform(result['raw_point'], True)

        if 'raw_normal' in result:
            if not result['ray'][RAY_ISSHADOW]:
                result['normal'] = cartesian_normalise(
                    shape[SHAPE_TRANSFORM].inverse_transform(result['raw_normal']))
                #print ("result['normal']:")
                #print(result['normal'])
                #print ("result['raw_normal']")
                #print(result['raw_normal'])

                #print ("result['raw_point']")
                #print(result['raw_point'])	
                #banana
    else:
        if 'raw_normal' in result:
            result['normal'] = result['raw_normal']
        if 'raw_point' in result:
            result['point'] = result['raw_point']

    return result
