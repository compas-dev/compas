from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from math import pi

from compas.plugins import plugin


__all__ = [
    'trimesh_gaussian_curvature',
]


@pluggable(category="trimesh", requires=['Rhino'])
def trimesh_gaussian_curvature(M):
    """Compute the discrete Gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list
        The discrete Gaussian curvature per vertex.

    Notes
    -----
    Description: The angle defect at a vertex is used to describe the Gaussian curvature in a neighborhood around a vertex.

    Notation Convention:
    :math:`K` - discrete Gaussian curvature
    :math:`j,k` - the vertices from the Star of vertex i
    :math:`e_{ij}, e_{ik}` - the vector from vertex i to j, i to k
    :math:`\theta_{i}^{jk}` - interior angle at vertex i of triangle ijk

    Formula:
    .. math::

        K_{i} = 2\pi-\sum\theta_{i}^{jk}

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete Gaussian curvature
    
    >>> K = trimesh_gaussian_curvature(M)
    """
    # (1) From mesh(list, list) to Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    for vertices, faces in M:
        for x, y, z in vertices:
            mesh.Vertices.Add(x, y, z)
        for face in faces:
            mesh.Faces.AddFace(*face)

    # (2) Prepare ingredient and return list
    pi_2 = 2 * pi
    K = []

    # (3) Main - loop every vertex for angle defect
    for i in range(mesh.Vertices.Count):
        vertex_neighbors = mesh.TopologyVertices.ConnectedTopologyVertices(mesh.TopologyVertices.TopologyVertexIndex(i), True)
        # in case this is not a proper mesh structure
        if vertex_neighbors is None:
            K.append(0)
            continue
        angles = []
        valence = len(vertex_neighbors)
        v_i = mesh.Vertices[i]
        # loop every neighbor
        for j in range(valence):
            v_j = mesh.Vertices[vertex_neighbors[j]]
            v_k = mesh.Vertices[vertex_neighbors[(j + 1) % valence]]
            e_ij = v_j - v_i
            e_ik = v_k - v_i
            angles.append(Rhino.Geometry.Vector3d.VectorAngle(e_ij, e_ik))
        K.append(pi_2 - sum(angles))
    # (4) Output
    return K
