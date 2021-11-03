from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.datastructures import Mesh
from ._geometry import RhinoGeometry


__all__ = ['RhinoMesh']


class RhinoMesh(RhinoGeometry):
    """Wrapper for Rhino mesh objects.
    """

    @property
    def vertices(self):
        if self.geometry:
            vertices = [[point.X, point.Y, point.Z] for point in self.geometry.Vertices]
        else:
            vertices = []
        return vertices

    @property
    def faces(self):
        if self.geometry:
            faces = [[face.A, face.B, face.C] if face.IsTriangle else [face.A, face.B, face.C, face.D] for face in self.geometry.Faces]
        else:
            faces = []
        return faces

    # @property
    # def vertex_colors(self):
    #     return map(list, compas_rhino.rs.MeshVertexColors(self.guid))

    # @vertex_colors.setter
    # def vertex_colors(self, colors):
    #     compas_rhino.rs.MeshVertexColors(self.guid, colors)

    # @property
    # def border(self):
    #     return compas_rhino.rs.DuplicateMeshBorder(self.guid)

    @classmethod
    def from_selection(cls):
        """Construct a mesh wrapper by selecting an existing Rhino mesh object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`RhinoMesh`
            The wrapped line.
        """
        guid = compas_rhino.select_mesh()
        return cls.from_guid(guid)

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a mesh wrapper from an existing Rhino geometry object.

        Parameters
        ----------
        geometry: :class:`Rhino.Geometry.Mesh`
            A Rhino mesh geometry.

        Returns
        -------
        :class:`RhinoMesh`
            The wrapped line.
        """
        mesh = cls()
        mesh.geometry = geometry
        return mesh

    def to_compas(self, cls=None):
        """Convert a Rhino mesh to a COMPAS mesh.

        Parameters
        ----------
        cls: :class:`compas.datastructures.Mesh`, optional
            The mesh type.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The equivalent COMPAS mesh.
        """
        cls = cls or Mesh
        mesh = cls()

        for vertex in self.geometry.Vertices:
            mesh.add_vertex(attr_dict=dict(x=float(vertex.X), y=float(vertex.Y), z=float(vertex.Z)))

        for face in self.geometry.Faces:
            if face.A == face.D or face.C == face.D:
                mesh.add_face([face.A, face.B, face.C])
            else:
                mesh.add_face([face.A, face.B, face.C, face.D])

        mesh.name = self.name

        return mesh

    def closest_point(self, point, maxdist=0.0):
        """Compute the closest point on the mesh to a given point.

        Parameters
        ----------
        point: point
            A point location.
        maxdist: float, optional
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
