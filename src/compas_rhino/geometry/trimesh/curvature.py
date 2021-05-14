from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from math import pi
from math import sqrt

from compas.plugins import plugin


__all__ = [
    'trimesh_gaussian_curvature',
    'trimesh_mean_curvature',
    'trimesh_principle_curvature',
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
    # (1) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if type(M) != Rhino.Geometry.Mesh:
        for vertices, faces in M:
            for x, y, z in vertices:
                mesh.Vertices.Add(x, y, z)
            for face in faces:
                mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (2) Prepare ingredient and return list
    pi_2 = 2 * pi
    K = []

    # (3) Main - loop every vertex for angle defect
    for i in range(mesh.Vertices.Count):
        vert_neighbors_topo = mesh.TopologyVertices.ConnectedTopologyVertices(mesh.TopologyVertices.TopologyVertexIndex(i), True)
        vert_neighbors = []
        if vert_neighbors_topo is None:
            K.append(0)
            continue
        for vert in vert_neighbors_topo:
            vert_neighbors.extend(mesh.TopologyVertices.MeshVertexIndices(vert))
        angles = []
        valence = len(vert_neighbors)
        v_i = mesh.Vertices[i]
        # loop every neighbor
        for j in range(valence):
            v_j = mesh.Vertices[vert_neighbors[j]]
            v_k = mesh.Vertices[vert_neighbors[(j + 1) % valence]]
            e_ij = v_j - v_i
            e_ik = v_k - v_i
            angles.append(Rhino.Geometry.Vector3d.VectorAngle(e_ij, e_ik))
        K.append(pi_2 - sum(angles))
    # (4) Output
    return K


@pluggable(category="trimesh", requires=['Rhino'])
def trimesh_mean_curvature(M):
    """Compute the discrete mean curvature of a triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list
        The discrete mean curvature per vertex.

    Notes
    -----
    Description: The discrete mean curvature is computed by edge length and its dihedral angle.

    Notation Convention:
    :math:`H` - discrete mean curvature
    :math:`E` - all the edges connect vertex i
    :math:`j` - the vertex connects vertex i
    :math:`l_{ij}` - the length of edge ij
    :math:`\phi_{ij}` - the dihedral angle of edge ij

    Formula:
    .. math::

        H_{i} = \frac{1}{4}\sum_{ij\in E}l_{ij}\phi_{ij}

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete mean curvature

    >>> H = trimesh_mean_curvature(M)
    """
    # (1) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if type(M) != Rhino.Geometry.Mesh:
        for vertices, faces in M:
            for x, y, z in vertices:
                mesh.Vertices.Add(x, y, z)
            for face in faces:
                mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (2) Prepare ingredient and return list
    H = []
    mesh.FaceNormals.ComputeFaceNormals()
    faces_normal = mesh.FaceNormals

    # (3) Main - loop over all vertices
    for i in range(mesh.Vertices.Count):
        edges = mesh.TopologyVertices.ConnectedEdges(mesh.TopologyVertices.TopologyVertexIndex(i))
        if edges is None:
            H.append(0)
            continue
        x = []
        for edge in edges:
            l_ij = mesh.TopologyEdges.EdgeLine(edge).Length
            faces = mesh.TopologyEdges.GetConnectedFaces(edge)
            if len(faces) != 2:
                x.append(0)
                continue
            angle = Rhino.Geometry.Vector3d.VectorAngle(faces_normal[faces[0]], faces_normal[faces[1]])
            x.append(l_ij * angle)
        H.append(1/4 * sum(x))

    # (4) Output
    return H


@pluggable(category="trimesh", requires=['Rhino'])
def trimesh_principal_curvature(M):
    """Compute the principal curvature of a triangle mesh.
    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.
    Returns
    -------
    Curvature : (k1, k2)
        k1_list, the max curvature per vertex.
        k2_list, the min curvature per vertex.

    Notes
    -----
    Description: The discrete principal curvature is computed by mean curvature, Gaussian curvature, and vertex area.

    Notation Convention:
    :math:`\kappa_1, \kappa_2` - The max principle curvature and the min principle curvature
    :math:`H_i` - the discrete mean curvature of vertex i
    :math:`K_i` - the discrete Gaussian curvature of vertex i
    :math:`A_i` - the vertex area of vertex i

    Formula:
    .. math::

        \frac{H_i}{A_i}\pm\sqrt{( \,\frac{H_i}{A_i})\,^2-\frac{K_i}{A_i}}

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete principle curvature

    >>> H = trimesh_principle_curvature(M)
    """
    # (1) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if type(M) != Rhino.Geometry.Mesh:
        for vertices, faces in M:
            for x, y, z in vertices:
                mesh.Vertices.Add(x, y, z)
            for face in faces:
                mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (2) Prepare ingredient and return list
    k1 = []
    k2 = []
    A = trimesh_barycentric_area(mesh)
    H = trimesh_mean_curvature(mesh)
    K = trimesh_gaussian_curvature(mesh)

    # (3) Main - loop over all vertices
    for i in range(mesh.Vertices.Count):
        if(A[i] == 0):
            k1.append(0)
            k2.append(0)
            continue
        H_ = H[i] / A[i]
        K_ = K[i] / A[i]

        k1.append(H_ + sqrt(max(0, H_ * H_ - K_)))
        k2.append(H_ - sqrt(max(0, H_ * H_ - K_)))

    # (4) Output
    return k1, k2


def trimesh_barycentric_area(mesh):
    # (1) prepare return list
    areas = [0] * mesh.Vertices.Count

    # (2) Main - loop over mesh faces rather than vertices
    for i in range(mesh.Faces.Count):
        # Heron's Formula
        ptA = mesh.Faces.GetFaceVertices(i)[1]
        ptB = mesh.Faces.GetFaceVertices(i)[2]
        ptC = mesh.Faces.GetFaceVertices(i)[3]
        dA = ptB.DistanceTo(ptC)
        dB = ptA.DistanceTo(ptC)
        dC = ptA.DistanceTo(ptB)
        p = (dA+dB+dC)/2
        area = sqrt(p*(p-dA)*(p-dB)*(p-dC)) / 3

        # topology vertices
        verts_topo = mesh.Faces.GetTopologicalVertices(i)
        # vertices
        verts = []
        for vert_topo in verts_topo:
            verts.extend(mesh.TopologyVertices.MeshVertexIndices(vert_topo))
        for vert in verts:
            areas[vert] += area

    # (3) output
    return areas
