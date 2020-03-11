from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.geometry._geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoMesh']


class RhinoMesh(RhinoGeometry):
    """Wrapper for Rhino mesh objects."""

    __module__ = 'compas_rhino.geometry'

    def __init__(self):
        super(RhinoMesh, self).__init__()

    @classmethod
    def from_guid(cls, guid):
        obj = compas_rhino.find_object(guid)
        mesh = cls()
        mesh.guid = guid
        mesh.object = obj
        mesh.geometry = obj.Geometry
        return mesh

    @classmethod
    def from_object(cls, obj):
        mesh = cls()
        mesh.guid = obj.Id
        mesh.object = obj
        mesh.geometry = obj.Geometry
        return mesh

    @classmethod
    def from_selection(cls):
        guid = compas_rhino.select_mesh()
        return cls.from_guid(guid)

    @property
    def vertices(self):
        return [map(float, vertex) for vertex in compas_rhino.rs.MeshVertices(self.guid)]

    @property
    def faces(self):
        return map(list, compas_rhino.rs.MeshFaceVertices(self.guid))

    def to_compas(self, cls=None):
        if not cls:
            cls = Mesh
        return cls.from_vertices_and_faces(self.vertices, self.faces)

    # def get_vertex_coordinates(self):
    #     return [map(float, vertex) for vertex in rs.MeshVertices(self.guid)]

    # def get_face_vertices(self):
    #     return map(list, rs.MeshFaceVertices(self.guid))

    # def get_vertex_colors(self):
    #     return map(list, rs.MeshVertexColors(self.guid))

    # def set_vertex_colors(self, colors):
    #     return rs.MeshVertexColors(self.guid, colors)

    # def unset_vertex_colors(self):
    #     return rs.MeshVertexColors(self.guid, None)

    # def get_vertices_and_faces(self):
    #     vertices = [map(float, vertex) for vertex in rs.MeshVertices(self.guid)]
    #     faces = map(list, rs.MeshFaceVertices(self.guid))
    #     return vertices, faces

    # def get_border(self):
    #     return rs.DuplicateMeshBorder(self.guid)

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

    # # def get_edge_index(guid):
    # #     class CustomGetObject(Rhino.Input.Custom.GetObject):
    # #         def CustomGeometryFilter(self, rhino_object, geometry, component_index):
    # #             return guid == rhino_object.Id
    # #     go = CustomGetObject()
    # #     go.SetCommandPrompt('Select an edge of the mesh.')
    # #     go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    # #     go.AcceptNothing(True)
    # #     if go.Get() != Rhino.Input.GetResult.Object:
    # #         return None
    # #     objref = go.Object(0)
    # #     if not objref:
    # #         return None
    # #     eindex = objref.GeometryComponentIndex.Index
    # #     go.Dispose()
    # #     return eindex
    # #
    # # def get_vertex_indices(guid):
    # #     tvindices = rs.GetMeshVertices(guid, 'Select mesh vertices.')
    # #     if not tvindices:
    # #         return
    # #     mobj = sc.doc.Objects.Find(guid)
    # #     mgeo = mobj.Geometry
    # #     vindices = []
    # #     for tvindex in tvindices:
    # #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    # #         vindices.append(temp[0])
    # #     return vindices
    # #
    # # def get_face_indices(guid):
    # #     return rs.GetMeshFaces(guid, 'Select mesh faces.')
    # #
    # # def get_vertex_face_indices(guid):
    # #     vindex = get_mesh_vertex_index(guid)
    # #     if vindex is None:
    # #         return
    # #     mobj = sc.doc.Objects.Find(guid)
    # #     mgeo = mobj.Geometry
    # #     findices = mgeo.TopologyVertices.ConnectedFaces(vindex)
    # #     return findices

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

    # # def get_edge_vertex_indices(guid):
    # #     eindex = get_mesh_edge_index(guid)
    # #     if eindex is None:
    # #         return
    # #     mobj = sc.doc.Objects.Find(guid)
    # #     mgeo = mobj.Geometry
    # #     temp = mgeo.TopologyEdges.GetTopologyVertices(eindex)
    # #     tvindices = temp.I, temp.J
    # #     vindices = []
    # #     for tvindex in tvindices:
    # #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    # #         vindices.append(temp[0])
    # #     return vindices

    # def normal(self, point):
    #     pass

    # def normals(self, points):
    #     pass

    def closest_point(self, point, maxdist=None):
        maxdist = maxdist or 0.0
        face, point = self.geometry.ClosestPoint(Rhino.Geometry.Point3d(*point), maxdist)
        return list(point)

    def closest_points(self, points, maxdist=None):
        # points = List[Point3d](len(points))
        # points = self.geometry.PullPointsToMesh()
        return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    rmesh = RhinoMesh.from_selection()

    print(rmesh.guid)
    print(rmesh.object)
    print(rmesh.geometry)
    print(rmesh.type)
    print(rmesh.name)

    mesh = rmesh.to_compas()
    print(len(rmesh.vertices) == mesh.number_of_vertices())
