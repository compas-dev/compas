from __future__ import print_function

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise

from compas.datastructures.mesh import Mesh
from compas_ghpython.utilities import xdraw_mesh
from compas.utilities.colors import color_to_colordict

__all__ = [
    'mesh_draw'
]

def mesh_draw(mesh,
              show_faces=False,
              show_vertices=False,
              show_edges=False,
              vertexcolor=None,
              edgecolor=None,
              facecolor=None):
    """
    Draw a mesh object in Grasshopper.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        show_faces : bool (True) Draw the faces.
        show_vertices : bool (False) Draw the vertices.
        show_edges : bool (False) Draw the edges.
        vertexcolor (str, tuple, list, dict): Optional. The vertex color
          specification. Default is ``None``.
        edgecolor (str, tuple, list, dict): Optional. The edge color
          specification. Default is ``None``.
        facecolor (str, tuple, list, dict): Optional. The face color
          specification. Default is ``None``.

    Note:
        Colors can be specified in different ways:

        * str: A hexadecimal color that will be applied to all elements subject
          to the specification.
        * tuple, list: RGB color that will be applied to all elements subject
          to the specification.
        * dict: RGB or hex color dict with a specification for some or all of
          the related elements.

    Important:
        RGB colors should specify color values between 0 and 255.

    """

    vertexcolor = color_to_colordict(vertexcolor,
                                     mesh.vertices(),
                                     default=mesh.attributes['color.vertex'],
                                     colorformat='rgb',
                                     normalize=False)

    """
    edgecolor = color_to_colordict(edgecolor,
                                   mesh.edges(),
                                   default=mesh.attributes['color.edge'],
                                   colorformat='rgb',
                                   normalize=False)
    """

    facecolor = color_to_colordict(facecolor,
                                   mesh.faces(),
                                   default=mesh.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)

    key_index = {key: index for index, key in enumerate(mesh.vertices())}
    xyz = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    faces = []

    for fkey in mesh.face:
        face = mesh.face_vertices(fkey)  # ordered=True
        faces.append([key_index[k] for k in face])

    color = None

    if show_faces:
        color = facecolor
    if show_edges:
        color = edgecolor
    if show_vertices:
        color = vertexcolor

    return xdraw_mesh(xyz, faces, vertex_colors=color)
