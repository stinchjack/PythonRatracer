import sys
import os
import random
from raytracer.cartesian import *
from raytracer.colour import *
from raytracer.matrix import *
from raytracer.light import *
from raytracer.output import *
from raytracer.shape import *
from raytracer.view import *
from raytracer.scene import *
from raytracer.quadraticshapes import *
from raytracer.planarshapes import *
from raytracer.lighting_model import *

if __name__ == '__main__':
    get_context().precision = 32

    scene = Scene()
    view = view_create(scene, -15, {'left': 0,
                             'right': 300,
                             'top': 0,
                             'bottom': 300},
                       # {'left':.1, 'right':.1, 'top':.1, 'bottom':.1}),
                       {'left': -5, 'right': 5, 'top': -5, 'bottom': 5})
    view_set_output(view, PIL_Output())
    scene.add_view(view, 'view')


    tetra_data = {
        'points': [cartesian_create(-1, -1, 1),
                   cartesian_create(1, -1, 1),
                   cartesian_create(1, 1, 1),
                   cartesian_create(-1, 1, 1),
                   cartesian_create(0, 0, 0)],

        'polygon_point_indices': [[0, 1, 2, 3],
                                  [4, 0, 1],
                                  [4, 1, 2],
                                  [4, 2, 3],
                                  [4, 3, 0]],

        'face_diffuse_colours': [colour_create(0, 1, 0),
                                 colour_create(1, 1, 1),
                                 colour_create(0, 0, 1),
                                 colour_create(0, 1, 1),
                                 colour_create(1, 0, 0)],
    }
    poly_mesh = shape_polymesh_create(tetra_data)

    shape_set_transform(poly_mesh, Transform({
        'scale': {'x': 1.0, 'y': 3.0, 'z': 2.0},
        'rotate': {'vector': cartesian_create(1, 0, 0), 'angle': 90},
        'translate': {'x': 3, 'y': 0, 'z': 0}
    }))

    poly_data = {
        'colour': colour_create(1, 0, 1),
        'points': [cartesian_create(-1, -1, 5),
                   cartesian_create(1, -1, 5),
                   cartesian_create(1, 1, 5),
                   cartesian_create(-1, 1, 5)]}

    polygon = shape_polygon_create(poly_data)
    shape_set_transform(polygon, Transform({
        'scale': {'x': 2.0, 'y': 1.0, 'z': 1.0},
        'rotate': {'vector': cartesian_create(1, 0, 0), 'angle': 30},
    }))

    scene.add_shape(poly_mesh, 'triMesh')

    scene.add_light(light_point_light_create(cartesian_create(
        0, 0, -1.5), colour_create(1, 1, 1)), 'light1')

    image = scene.render('view')
    image.show()
