from __future__ import print_function
from __future__ import absolute_import

import os
import sys

import compas

from compas.utilities import flatten

sys.path.insert(0, os.path.join(compas.LIBS, "ShapeOp/bindings/python"))

import shapeopPython


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'int_array',
    'float_array',
    'ShapeOpSolver',
]


def int_array(data):
    try:
        len(data[0])
    except TypeError:
        pass
    else:
        data = list(flatten(data))
    n = len(data)
    array = shapeopPython.intArray(n)
    for index, value in enumerate(data):
        array[index] = int(value)
    return array


def float_array(data):
    try:
        len(data[0])
    except TypeError:
        pass
    else:
        data = list(flatten(data))
    n = len(data)
    array = shapeopPython.doubleArray(n)
    for index, value in enumerate(data):
        array[index] = float(value)
    return array


class ShapeOpSolver(object):
    """"""

    def __init__(self):
        self.solver = shapeopPython.shapeop_create()
        self.number_of_points = 0
        self.points = 0
        self.kmax = 1

    def init(self):
        shapeopPython.shapeop_init(self.solver)

    def delete(self):
        shapeopPython.shapeop_delete(self.solver)

    def solve(self, kmax=1):
        self.kmax = kmax
        self.init()
        shapeopPython.shapeop_solve(self.solver, self.kmax)

    def set_points(self, xyz):
        self.number_of_points = len(xyz)
        self.points = float_array(xyz)
        shapeopPython.shapeop_setPoints(self.solver, self.points, self.number_of_points)

    def get_points(self):
        shapeopPython.shapeop_getPoints(self.solver, self.points, self.number_of_points)
        return self.points

    def add_plane_constraint(self, vertices, weight):
        vertices_array = int_array(vertices)
        constraint_id = shapeopPython.shapeop_addConstraint(self.solver, 'Plane', vertices_array, len(vertices), weight)
        return constraint_id

    def add_circle_constraint(self, vertices, weight):
        vertices_array = int_array(vertices)
        constraint_id = shapeopPython.shapeop_addConstraint(self.solver, 'Circle', vertices_array, len(vertices), weight)
        return constraint_id

    def add_closeness_constraint(self, vertex, weight):
        vertices_array = int_array([vertex])
        constraint_id = shapeopPython.shapeop_addConstraint(self.solver, 'Closeness', vertices_array, 1, weight)
        return constraint_id


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
