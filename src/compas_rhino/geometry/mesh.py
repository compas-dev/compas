from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

import compas_rhino
from compas.datastructures import Mesh

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoMesh']


class RhinoMesh(BaseRhinoGeometry):
    """Wrapper for Rhino mesh objects.

    Attributes
    ----------
    vertices (read-only) : list of point
        The coordinates of the vertices of the mesh.
    faces (read-only) : list of list of int
        Faces defined as lists of references into the list of vertices.
    vertex_color : list
        The colors of the vertices.
        Setting this to ``None`` unsets the vertex colors.
    border (read-only) : list
        The GUIDs of the border curves.
    """

    def __init__(self):
        super(RhinoMesh, self).__init__()

    @property
    def vertices(self):
        return [map(float, point) for point in compas_rhino.rs.MeshVertices(self.geometry)]

    @property
    def faces(self):
        return map(list, compas_rhino.rs.MeshFaceVertices(self.geometry))

    @property
    def vertex_colors(self):
        return map(list, compas_rhino.rs.MeshVertexColors(self.guid))

    @vertex_colors.setter
    def vertex_colors(self, colors):
        compas_rhino.rs.MeshVertexColors(self.guid, colors)

    @property
    def border(self):
        return compas_rhino.rs.DuplicateMeshBorder(self.guid)

    @classmethod
    def from_selection(cls):
        """Construct a mesh wrapper by selecting an existing Rhino mesh object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoMesh`
            The wrapped line.
        """
        guid = compas_rhino.select_mesh()
        return cls.from_guid(guid)

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a mesh wrapper from an existing Rhino geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Mesh`
            A Rhino mesh geometry.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoMesh`
            The wrapped line.
        """
        mesh = cls()
        mesh.geometry = geometry
        return mesh

    def to_compas(self, cls=None):
        """Convert a Rhino mesh to a COMPAS mesh.

        Parameters
        ----------
        cls : :class:`compas.datastructures.Mesh`, optional
            The mesh type.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The equivalent COMPAS mesh.
        """
        cls = cls or Mesh
        faces = []
        for face in self.faces:
            if face[0] == face[-1]:
                faces.append(face[:-1])
            elif face[-2] == face[-1]:
                faces.append(face[:-1])
            else:
                faces.append(face)
        mesh = cls.from_vertices_and_faces(self.vertices, faces)
        mesh.name = self.name
        return mesh

    def closest_point(self, point, maxdist=0.0):
        """Compute the closest point on the mesh to a given point.

        Parameters
        ----------
        point : point
            A point location.
        maxdist : float, optional
            The maximum distance between the closest point and the mesh.
            Default is ``0.0``.

        Returns
        -------
        list
            The XYZ coordinates of the closest point.
        """
        face, point = self.geometry.ClosestPoint(Rhino.Geometry.Point3d(*point), maxdist)
        return list(point)

    def closest_points(self, points, maxdist=None):
        """Compute the closest points on the mesh to a list of input points.

        Parameters
        ----------
        points : list of point
            The input points.
        maxdist : float, optional
            The maximum distance between the closest point and the mesh.
            Default is ``0.0``.

        Returns
        -------
        list of point
            The XYZ coordinates of the closest points.
        """
        return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
