from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise

__all__ = [
    'mesh_unweld_vertices',
]


def mesh_unweld_vertices(mesh, fkey, where=None):
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

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.datastructures import mesh_unweld_vertices
        from compas.plotters import MeshPlotter
        from compas.geometry import subtract_vectors

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices = set(mesh.vertices())

        fkey  = 12
        where = mesh.face_vertices(fkey)[0:1]
        centroid = mesh.face_centroid(fkey)

        face = mesh_unweld_vertices(mesh, fkey, where)

        for key in face:
            if key in vertices:
                continue
            xyz = mesh.vertex_coordinates(key)
            v = subtract_vectors(centroid, xyz)
            mesh.vertex[key]['x'] += 0.3 * v[0]
            mesh.vertex[key]['y'] += 0.3 * v[1]
            mesh.vertex[key]['z'] += 0.3 * v[2]

        plotter = MeshPlotter(mesh, figsize=(10, 7))

        plotter.draw_vertices()
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    """
    face = []
    vertices = mesh.face_vertices(fkey)

    if not where:
        where = vertices

    for u, v in pairwise(vertices + vertices[0:1]):
        if u in where:
            x, y, z = mesh.vertex_coordinates(u)
            u = mesh.add_vertex(x=x, y=y, z=z)
        if u in where or v in where:
            mesh.halfedge[v][u] = None
        face.append(u)

    mesh.add_face(face, fkey=fkey)

    return face

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_unweld_vertices
    from compas.plotters import MeshPlotter
    from compas.geometry import subtract_vectors

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    vertices = set(mesh.vertices())

    fkey  = 12
    where = mesh.face_vertices(fkey)[0:2]
    centroid = mesh.face_centroid(fkey)

    face = mesh_unweld_vertices(mesh, fkey, where)

    for key in face:
        if key in vertices:
            continue
        xyz = mesh.vertex_coordinates(key)
        v = subtract_vectors(centroid, xyz)
        mesh.vertex[key]['x'] += 0.3 * v[0]
        mesh.vertex[key]['y'] += 0.3 * v[1]
        mesh.vertex[key]['z'] += 0.3 * v[2]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()
