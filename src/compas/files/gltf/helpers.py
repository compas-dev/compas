from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import math


def get_matrix_from_col_major_list(matrix_as_list):
    return [[matrix_as_list[i + j * 4] for j in range(4)] for i in range(4)]


def matrix_to_col_major_order(matrix):
    return [matrix[i][j] for j in range(4) for i in range(4)]


def get_morph_function(weights):
    # Returns a function which computes for a fixed list w of scalar weights the linear combination
    #                               vertex + sum_i(w[i] * targets[i])
    # where vertex and targets[i] are vectors.

    def apply_weight(weight, target_coordinate):
        return weight * target_coordinate

    def weighted_sum(vertex_coordinate, *targets_coordinate):
        return vertex_coordinate + math.fsum(map(apply_weight, weights, targets_coordinate))

    def apply_morph_target(vertex, *targets):
        return tuple(map(weighted_sum, vertex, *targets)) + ((vertex[-1],) if len(vertex) == 4 else ())

    return apply_morph_target


def get_weighted_mesh_vertices(mesh, weights):
    vertices = []
    for primitive_data in mesh.primitive_data_list:
        position_target_data = [target['POSITION'] for target in primitive_data.targets]
        apply_morph_targets = get_morph_function(weights)
        vertices += list(map(apply_morph_targets, primitive_data.attributes['POSITION'], *position_target_data))
    return vertices
