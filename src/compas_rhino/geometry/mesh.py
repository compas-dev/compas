from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.geometry.base import BaseRhinoGeometry

if compas.RHINO:
    import Rhino


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
        if not cls:
            cls = Mesh
        faces = []
        for face in self.faces:
            if face[0] == face[-1]:
                faces.append(face[:-1])
            elif face[-2] == face[-1]:
                faces.append(face[:-1])
            else:
                faces.append(face)
        return cls.from_vertices_and_faces(self.vertices, faces)

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

    # def get_vertex_index(self):
    #     guid = self.guid

    #     class CustomGetObject(Rhino.Input.Custom.GetObject):
    #         def CustomGeometryFilter(self, rhino_object, geometry, component_index):
    #             # return True if selection is on current mesh object (guid)
    #             return guid == rhino_object.Id

    #     go = CustomGetObject()
    #     go.SetCommandPrompt('Select a vertex of the mesh.')
    #     go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshVertex
    #     go.AcceptNothing(True)
    #     if go.Get() != Rhino.Input.GetResult.Object:
    #         return None
    #     objref = go.Object(0)
    #     if not objref:
    #         return None
    #     tvindex = objref.GeometryComponentIndex.Index
    #     mesh = sc.doc.Objects.Find(guid)
    #     temp = mesh.Geometry.TopologyVertices.MeshVertexIndices(tvindex)
    #     vindex = temp[0]
    #     go.Dispose()
    #     return vindex

    # def get_face_index(self):
    #     guid = self.guid

    #     class CustomGetObject(Rhino.Input.Custom.GetObject):
    #         def CustomGeometryFilter(self, rhino_object, geometry, component_index):
    #             # return True if selecion is on current mesh object (guid)
    #             return guid == rhino_object.Id

    #     go = CustomGetObject()
    #     go.SetCommandPrompt('Select a face of the mesh.')
    #     go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshFace
    #     go.AcceptNothing(True)
    #     if go.Get() != Rhino.Input.GetResult.Object:
    #         return None
    #     objref = go.Object(0)
    #     if not objref:
    #         return None
    #     findex = objref.GeometryComponentIndex.Index
    #     go.Dispose()
    #     return findex

    # def get_edge_index(guid):
    #     class CustomGetObject(Rhino.Input.Custom.GetObject):
    #         def CustomGeometryFilter(self, rhino_object, geometry, component_index):
    #             return guid == rhino_object.Id
    #     go = CustomGetObject()
    #     go.SetCommandPrompt('Select an edge of the mesh.')
    #     go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    #     go.AcceptNothing(True)
    #     if go.Get() != Rhino.Input.GetResult.Object:
    #         return None
    #     objref = go.Object(0)
    #     if not objref:
    #         return None
    #     eindex = objref.GeometryComponentIndex.Index
    #     go.Dispose()
    #     return eindex
    #
    # def get_vertex_indices(guid):
    #     tvindices = rs.GetMeshVertices(guid, 'Select mesh vertices.')
    #     if not tvindices:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     vindices = []
    #     for tvindex in tvindices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    #         vindices.append(temp[0])
    #     return vindices
    #
    # def get_face_indices(guid):
    #     return rs.GetMeshFaces(guid, 'Select mesh faces.')
    #
    # def get_vertex_face_indices(guid):
    #     vindex = get_mesh_vertex_index(guid)
    #     if vindex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     findices = mgeo.TopologyVertices.ConnectedFaces(vindex)
    #     return findices

    # def get_face_vertex_indices(guid):
    #     findex = compas_rhino.get_mesh_face_index(guid)
    #     if findex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     tvertices = mgeo.Faces.GetTopologicalVertices(findex)
    #     vindices = []
    #     for tvertex in tvertices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvertex)
    #         vindices.append(temp[0])
    #     return vindices

    # def get_edge_vertex_indices(guid):
    #     eindex = get_mesh_edge_index(guid)
    #     if eindex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     temp = mgeo.TopologyEdges.GetTopologyVertices(eindex)
    #     tvindices = temp.I, temp.J
    #     vindices = []
    #     for tvindex in tvindices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    #         vindices.append(temp[0])
    #     return vindices

    # def normal(self, point):
    #     pass

    # def normals(self, points):
    #     pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
