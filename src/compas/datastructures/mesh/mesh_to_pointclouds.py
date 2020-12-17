from __future__ import absolute_import
from __future__ import division
from __future__ import print_function





__all__ = [
    'mesh_to_pointscloud',
]

def mesh_to_pointscloud(mesh, num_points: int = 10000, return_normals: bool = False):
    """Convert a mesh to pointclouds

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.
    num_points : (int) 
        How many points sampled
    return_normals : (bool)
        Return normals for the points, if True

    Returns
    -------
    list
        A list of coordinates.

    Examples
    --------


    """
    


if __name__ == '__main__':

    import doctest
    import compas
    from compas.datastructures import Mesh

    hypar = Mesh.from_obj(compas.get('hypar.obj'))
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    doctest.testmod()