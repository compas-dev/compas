from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .matrices import (  # noqa: F401
    matrix_determinant,
    matrix_inverse,
    decompose_matrix,
    compose_matrix,
    identity_matrix,
    matrix_from_frame,
    matrix_from_frame_to_frame,
    matrix_from_change_of_basis,
    matrix_from_euler_angles,
    matrix_from_axis_and_angle,
    matrix_from_axis_angle_vector,
    matrix_from_basis_vectors,
    matrix_from_translation,
    matrix_from_orthogonal_projection,
    matrix_from_parallel_projection,
    matrix_from_perspective_projection,
    matrix_from_perspective_entries,
    matrix_from_shear_entries,
    matrix_from_shear,
    matrix_from_scale_factors,
    matrix_from_quaternion,
    euler_angles_from_matrix,
    euler_angles_from_quaternion,
    axis_and_angle_from_matrix,
    axis_angle_vector_from_matrix,
    axis_angle_from_quaternion,
    quaternion_from_matrix,
    quaternion_from_euler_angles,
    quaternion_from_axis_angle,
    basis_vectors_from_matrix,
    translation_from_matrix,
)

from .transformation import Transformation  # noqa: F401
from .translation import Translation  # noqa: F401
from .shear import Shear  # noqa: F401
from .scale import Scale  # noqa: F401
from .rotation import Rotation  # noqa: F401
from .reflection import Reflection  # noqa: F401
from .projection import Projection  # noqa: F401
from .transformations import (  # noqa: F401
    local_axes,
    orthonormalize_axes,
    transform_points,
    transform_vectors,
    transform_frames,
    local_to_world_coordinates,
    world_to_local_coordinates,
    translate_points,
    translate_points_xy,
    scale_points,
    scale_points_xy,
    rotate_points,
    rotate_points_xy,
    mirror_vector_vector,
    mirror_points_point,
    mirror_points_point_xy,
    mirror_points_line,
    mirror_points_line_xy,
    mirror_point_plane,
    mirror_points_plane,
    project_point_plane,
    project_points_plane,
    project_point_line,
    project_point_line_xy,
    project_points_line,
    project_points_line_xy,
    reflect_line_plane,
    reflect_line_triangle,
    orient_points,
)

if not compas.IPY:
    from .transformations_numpy import *  # noqa: F401 F403
