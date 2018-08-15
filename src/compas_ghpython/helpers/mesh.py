from __future__ import print_function

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise

from compas.datastructures.mesh import Mesh
from compas_ghpython.utilities import xdraw_mesh
from compas.utilities.colours import colour_to_colourdict


def mesh_draw(mesh, 
              show_faces=False, 
              show_vertices=False, 
              show_edges=False,
              vertexcolour=None, 
              edgecolour=None, 
              facecolour=None):
    """
    Draw a mesh object in Grasshopper.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        show_faces : bool (True) Draw the faces.
        show_vertices : bool (False) Draw the vertices.
        show_edges : bool (False) Draw the edges.
        vertexcolour (str, tuple, list, dict): Optional. The vertex colour
          specification. Default is ``None``.
        edgecolour (str, tuple, list, dict): Optional. The edge colour
          specification. Default is ``None``.
        facecolour (str, tuple, list, dict): Optional. The face colour
          specification. Default is ``None``.

    Note:
        colours can be specified in different ways:

        * str: A hexadecimal colour that will be applied to all elements subject
          to the specification.
        * tuple, list: RGB colour that will be applied to all elements subject
          to the specification.
        * dict: RGB or hex colour dict with a specification for some or all of
          the related elements.

    Important:
        RGB colours should specify colour values between 0 and 255.

    """

    vertexcolour = colour_to_colourdict(vertexcolour,
                                     mesh.vertices(),
                                     default=mesh.attributes['colour.vertex'],
                                     colourformat='rgb',
                                     normalize=False)

    """
    edgecolour = colour_to_colourdict(edgecolour,
                                   mesh.edges(),
                                   default=mesh.attributes['colour.edge'],
                                   colourformat='rgb',
                                   normalize=False)
    """

    facecolour = colour_to_colourdict(facecolour,
                                   mesh.faces(),
                                   default=mesh.attributes['colour.face'],
                                   colourformat='rgb',
                                   normalize=False)

    key_index = {key: index for index, key in enumerate(mesh.vertices())}
    xyz = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    faces = []

    for fkey in mesh.face:
        face = mesh.face_vertices(fkey)  # ordered=True
        faces.append([key_index[k] for k in face])

    colour = None

    if show_faces:
        colour = facecolour
    if show_edges:
        colour = edgecolour
    if show_vertices:
        colour = vertexcolour

    return xdraw_mesh(xyz, faces, vertex_colours=colour)
