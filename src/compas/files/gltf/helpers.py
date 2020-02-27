from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


def get_matrix_from_col_major_list(matrix_as_list):
    return [[matrix_as_list[i + j * 4] for j in range(4)] for i in range(4)]


def matrix_to_col_major_order(matrix):
    return [matrix[i][j] for j in range(4) for i in range(4)]
