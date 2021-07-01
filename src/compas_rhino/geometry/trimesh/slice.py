from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from Rhino.Geometry import Point3d, Vector3d, Plane
from Rhino.Geometry.Intersect.Intersection import MeshPlane

from compas.plugins import plugin


__all__ = [
    'trimesh_slice',
]


@plugin(category="trimesh", requires=['Rhino'])
def trimesh_slice(mesh, planes):
    """Slice a mesh by a list of planes.

    Parameters
    ----------
    mesh : tuple of vertices and faces
        The mesh to slice.
    planes : list of (point, normal) tuples or compas.geometry.Plane
        The slicing planes.

    Returns
    -------
    list of arrays
        The points defining the slice polylines.

    Examples
    --------
    >>> from compas.geometry import Sphere, Plane, Point, Vector
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = sphere.to_vertices_and_faces(u=30, v=30)
    >>> P1 = Plane(Point(0, 0, 0), Vector(0, -1, 0))
    >>> P2 = Plane(Point(0, 0, 0), Vector(0.87, -0.5, 0))
    >>> planes = [P1, P2]
    >>> points = trimesh_slice(sphere, planes)

    """
    # (0) see if input is already Rhino.Geometry.Mesh
    M = Rhino.Geometry.Mesh()
    if not isinstance(mesh, Rhino.Geometry.Mesh):
        for x, y, z in mesh[0]:
            M.Vertices.Add(x, y, z)
        for face in mesh[1]:
            M.Faces.AddFace(*face)
    else:
        M = mesh
    # (1) parse to Rhino.Geometry.Plane
    P = []
    for plane in planes:
        point = Point3d(plane[0][0], plane[0][1], plane[0][2])
        normal = Vector3d(plane[1][0], plane[1][1], plane[1][2])
        P.append(Plane(point, normal))
    # (2) Slice
    polylines = MeshPlane(M, P)
    # (3) Return points in a list of arrays
    polyline_pts = []
    for polyline in polylines:
        pts = []
        for i in range(polyline.Count):
            pts.append([polyline.X[i], polyline.Y[i], polyline.Z[i]])
        polyline_pts.append(pts)

    return polyline_pts
