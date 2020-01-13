from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.geometry import oriented_bounding_box_numpy
from compas.geometry import oriented_bounding_box_xy_numpy


__all__ = [
    'mesh_oriented_bounding_box_numpy',
    'mesh_oriented_bounding_box_xy_numpy',
]


def mesh_oriented_bounding_box_numpy(mesh):
    """Compute the (axis aligned) bounding box of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.

    Returns
    -------
    list
        The bounding box of the mesh as a list of corner vertex coordinates.

    Examples
    --------
    >>> box = mesh_oriented_bounding_box_numpy(hypar)
    >>> len(box)
    8

    """
    xyz = mesh.vertices_attributes('xyz')
    return oriented_bounding_box_numpy(xyz)


def mesh_oriented_bounding_box_xy_numpy(mesh):
    """Compute the (axis aligned) bounding box of a projection of the mesh in the XY plane.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.

    Returns
    -------
    box_xy
        The bounding box.

    Examples
    --------
    >>> mesh_oriented_bounding_box_xy_numpy(mesh)
    [[10.0, 0.0], [0.0, 0.0], [0.0, 10.0], [10.0, 10.0]]

    """
    xyz = mesh.vertices_attributes('xyz')
    return oriented_bounding_box_xy_numpy(xyz)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    import compas
    from compas.datastructures import Mesh

    hypar = Mesh.from_obj(compas.get('hypar.obj'))
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    doctest.testmod()
