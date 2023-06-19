from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.datastructures import Mesh

from ._geometry import RhinoGeometry


class RhinoMesh(RhinoGeometry):
    """Wrapper for Rhino meshes."""

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
            faces = [
                [face.A, face.B, face.C] if face.IsTriangle else [face.A, face.B, face.C, face.D]
                for face in self.geometry.Faces
            ]
        else:
            faces = []
        return faces

    @property
    def vertexnormals(self):
        if self.geometry:
            # self.geometry.ComputeNormals()
            # self.geometry.UnitizeNormals()
            normals = [[vector.X, vector.Y, vector.Z] for vector in self.geometry.Normals]
        else:
            normals = []
        return normals

    @property
    def facenormals(self):
        if self.geometry:
            # self.geometry.ComputeFaceNormals()
            # self.geometry.UnitizeFaceNormals()
            normals = [[vector.X, vector.Y, vector.Z] for vector in self.geometry.FaceNormals]
        else:
            normals = []
        return normals

    @property
    def vertexcolors(self):
        if self.geometry:
            colors = [[color.R, color.G, color.B] for color in self.geometry.VertexColors]
        else:
            colors = []
        return colors

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry: :rhino:`Rhino_Geometry_Mesh`
            A Rhino mesh geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a mesh.
        """
        self._geometry = geometry

    def to_compas(self, cls=None):
        """Convert a Rhino mesh to a COMPAS mesh.

        Parameters
        ----------
        cls: :class:`~compas.datastructures.Mesh`, optional
            The mesh type.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
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
