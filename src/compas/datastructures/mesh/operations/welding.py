from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_unweld_vertices',
]


def mesh_unweld_vertices(self, fkey, where=None):
    """Unweld a face of the mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fkey : hashable
        The identifier of a face.
    where : list (None)
        A list of vertices to unweld.
        Default is to unweld all vertices of the face.

    Example
    -------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        fkey  = 12
        where = mesh.face_vertices(fkey)[0:1]
        xyz   = mesh.face_centroid(fkey)

        mesh.unweld_vertices(fkey, where)

        mesh.vertex[36]['x'] = xyz[0]
        mesh.vertex[36]['y'] = xyz[1]
        mesh.vertex[36]['z'] = xyz[2]

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices()
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    """
    face = []
    vertices = self.face_vertices(fkey)

    if not where:
        where = vertices

    for key in vertices:
        if key in where:
            x, y, z = self.vertex_coordinates(key)
            key = self.add_vertex(x=x, y=y, z=z)
        face.append(key)

    self.add_face(face)

    for key in where:
        d = self.face_vertex_descendant(fkey, key)
        a = self.face_vertex_ancestor(fkey, key)
        self.halfedge[a][key] = None
        self.halfedge[key][d] = None
    del self.face[fkey]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    fkey  = 12
    where = mesh.face_vertices(fkey)[0:1]
    xyz   = mesh.face_centroid(fkey)

    mesh.unweld_vertices(fkey, where)

    mesh.vertex[36]['x'] = xyz[0]
    mesh.vertex[36]['y'] = xyz[1]
    mesh.vertex[36]['z'] = xyz[2]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()
