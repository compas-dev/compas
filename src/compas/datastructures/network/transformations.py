from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.geometry import transform_points


__all__ = [
    'network_transform',
    'network_transformed',
]


def network_transform(network, transformation):
    """Transform a network.

    Parameters
    ----------
    network : network
        The network.
    transformation : Transformation
        The transformation.

    Notes
    -----
    The network is modified in-place.

    Examples
    --------
    >>> network = network.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tnetwork = network.copy()
    >>> network_transform(tnetwork, T)
    >>> viewer.network = tnetwork  # this should be a list of networkes
    >>> viewer.show()

    """
    vertices = [network.vertex_coordinates(key) for key in network.vertices()]
    xyz = transform_points(vertices, transformation)
    for index, (key, attr) in enumerate(network.vertices(True)):
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]


def network_transformed(network, transformation):
    """Transform a copy of ``network``.

    Parameters
    ----------
    network : network
        The network.
    transformation : Transformation
        The transformation.

    Returns
    -------
    network
        A transformed independent copy of ``network``.

    Notes
    -----
    The original network is not modified.
    Instead a transformed independent copy is returned.

    Examples
    --------
    >>> network = network.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tnetwork = network_transformed(network, T)
    >>> viewer.network = tnetwork  # this should be a list of networkes
    >>> viewer.show()

    """
    network_copy = network.copy()
    network_transform(network_copy, transformation)
    return network_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from math import pi

    from compas.utilities import print_profile
    from compas.geometry import Box
    from compas.geometry import matrix_from_translation
    from compas.geometry import Translation
    from compas.geometry import Rotation
    from compas.datastructures import network
    from compas.datastructures import network_transform


    network_transform = print_profile(network_transform)

    box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    network = network.from_vertices_and_faces(box.vertices, box.faces)

    T = matrix_from_translation([-2.0, 0.0, 3.0])
    T = Translation([-2.0, 0.0, 3.0])
    R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], pi / 2)

    network_transform(network, R)

    print(network.get_vertices_attribute('x'))
