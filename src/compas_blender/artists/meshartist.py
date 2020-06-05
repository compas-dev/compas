from compas_blender.artists import Artist
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist
from compas_blender.artists.mixins import FaceArtist
from compas_blender.utilities import draw_mesh


__all__ = [
    'MeshArtist',
]


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist, Artist):
    """Artist for COMPAS meshes.

    Parameters
    ----------
    mesh: compas.datastructures.Mesh
        A COMPAS mesh data structure.
    layer (optional): str
        The layer in which the components of the mesh should be drawn.
        Default is None.

    Notes
    -----
    There is no such thing as a "layer" in Blender.
    Instead, objects are added to collections.
    Vertices will automatically be added to a vertex collection,
    edges to an edge collection, and faces to a face collection.
    These collections are added to a mesh collection for the current mesh.
    What is specified as "layer" will be the collection this overal mesh
    collection is added to.

    """

    def __init__(self, mesh, layer=None):
        super().__init__(layer=layer)
        self.mesh = mesh
        self.defaults.update({
            'color.vertex': [255, 255, 255],
            'color.edge':   [0, 0, 0],
            'color.face':   [110, 110, 110],
        })

    @property
    def mesh(self):
        return self.datastructure

    @mesh.setter
    def mesh(self, mesh):
        self.datastructure = mesh

    def draw_mesh(self):
        vertices = self.mesh.vertices_attributes('xyz')
        edges = []
        faces = [self.mesh.face_vertices(key) for key in self.mesh.faces()]
        draw_mesh(vertices, edges, faces)

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
