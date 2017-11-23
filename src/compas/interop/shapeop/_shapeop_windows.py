from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import ctypes

import compas

from compas.utilities import flatten

dll = os.path.join(compas.LIBS, "ShapeOp/bindings/python/_ShapeOp.0.1.0.dll")

shapeopPython = ctypes.cdll.LoadLibrary(dll)


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'int_array',
    'float_array',
    'ShapeOpSolver',
]


# replace this by interop.core functionality
def int_array(data):
    try:
        len(data[0])
    except TypeError:
        pass
    else:
        raise
    array = (ctypes.c_int * len(data))()
    for index, value in enumerate(data):
        array[index] = int(value)
    return array


# replace this by interop.core functionality
def float_array(data):
    try:
        len(data[0])
    except TypeError:
        pass
    else:
        data = list(flatten(data))
    array = (ctypes.c_double * len(data))()
    for index, value in enumerate(data):
        array[index] = float(value)
    return array


class ShapeOpSolver(object):
    """"""

    def __init__(self, kmax=100):
        self.solver = shapeopPython.shapeop_create()
        self.number_of_points = 0
        self.points = 0
        self.kmax = kmax

    def init(self):
        shapeopPython.shapeop_init(self.solver)

    def delete(self):
        shapeopPython.shapeop_delete(self.solver)

    def solve(self):
        self.init()
        shapeopPython.shapeop_solve(self.solver, self.kmax)

    def set_points(self, xyz):
        self.number_of_points = len(xyz)
        self.points = float_array(xyz)
        shapeopPython.shapeop_setPoints(self.solver, ctypes.byref(self.points), self.number_of_points)

    def get_points(self):
        shapeopPython.shapeop_getPoints(self.solver, ctypes.byref(self.points), self.number_of_points)
        return self.points

    def add_plane_constraint(self, vertices, weight):
        n = len(vertices)
        vertices_array = int_array(vertices)
        constraint_id = shapeopPython.shapeop_addConstraint(self.solver,
                                                            ctypes.c_char_p('Plane'),
                                                            ctypes.byref(vertices_array),
                                                            ctypes.c_int(n),
                                                            ctypes.c_double(weight))
        return constraint_id

    def add_closeness_constraint(self, vertex, weight):
        n = 1
        vertices_array = int_array([vertex])
        constraint_id = shapeopPython.shapeop_addConstraint(self.solver,
                                                            ctypes.c_char_p('Closeness'),
                                                            ctypes.byref(vertices_array),
                                                            ctypes.c_int(n),
                                                            ctypes.c_double(weight))
        return constraint_id


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
