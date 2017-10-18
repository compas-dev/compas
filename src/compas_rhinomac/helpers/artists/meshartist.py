import time

from compas.utilities import to_valuedict
from compas.cad import ArtistInterface

import compas_rhinomac

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['MeshArtist']


class MeshArtist(ArtistInterface):
    """"""

    def __init__(self, mesh, layer=None):
        self.mesh = mesh
        self.layer = layer
        self.defaults = {
            'vertex.color' : (255, 0, 0),
            'face.color'   : (255, 255, 255),
            'edge.color'   : (0, 0, 0),
        }

    def redraw(self, timeout=None):
        """Redraw the Rhino view."""
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhinomac.clear_layer(self.layer)

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()

    def clear_vertices(self, keys=None):
        if not keys:
            name = '{}.vertex.*'.format(self.mesh.attributes['name'])
            guids = compas_rhinomac.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.{}'.format(self.attributes['name'], key)
                guid = compas_rhinomac.get_object(name=name)
                guids.append(guid)
        compas_rhinomac.delete_objects(guids)

    def clear_faces(self, keys=None):
        if not keys:
            name = '{}.face.*'.format(self.mesh.attributes['name'])
            guids = compas_rhinomac.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.face.{}'.format(self.attributes['name'], key)
                guid = compas_rhinomac.get_object(name=name)
                guids.append(guid)
        compas_rhinomac.delete_objects(guids)

    def clear_edges(self, keys=None):
        if not keys:
            name = '{}.edge.*'.format(self.mesh.attributes['name'])
            guids = compas_rhinomac.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = '{}.edge.{}-{}'.format(self.attributes['name'], u, v)
                guid = compas_rhinomac.get_object(name=name)
                guids.append(guid)
        compas_rhinomac.delete_objects(guids)

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices of the mesh.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default vertex
            color (``self.defaults['vertex.color']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        Notes
        -----
        The vertices are named using the following template:
        ``"{}.vertex.{}".format(self.mesh.attributes['name'], key)``.
        This name is used afterwards to identify vertices of the meshin the Rhino model.

        Examples
        --------
        >>>

        """
        keys = keys or list(self.mesh.vertices())
        colordict = to_valuedict(keys, color, self.defaults['vertex.color'])
        points = []
        for key in keys:
            points.append({
                'pos'  : self.mesh.vertex_coordinates(key),
                'name' : self.mesh.vertex_name(key),
                'color': colordict[key]
            })
        return compas_rhinomac.xdraw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self, fkeys=None, color=None):
        """Draw a selection of faces of the mesh.

        Parameters
        ----------
        fkeys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all faces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.defaults['face.color']``).
            The default is ``None``, in which case all faces are assigned the
            default vertex color.

        Notes
        -----
        The faces are named using the following template:
        ``"{}.face.{}".format(self.mesh.attributes['name'], key)``.
        This name is used afterwards to identify faces of the mesh in the Rhino model.

        Examples
        --------
        >>>

        """
        fkeys = fkeys or list(self.mesh.faces())
        colordict = to_valuedict(fkeys, color, self.defaults['face.color'])
        faces = []
        for fkey in fkeys:
            faces.append({
                'points': self.mesh.face_coordinates(fkey),
                'name'  : "{}.face.{}".format(self.mesh.attributes['name'], fkey),
                'color' : colordict[fkey],
            })
        return compas_rhinomac.xdraw_faces(faces, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges of the mesh.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all faces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.defaults['face.color']``).
            The default is ``None``, in which case all faces are assigned the
            default vertex color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.mesh.attributes['name'], u, v)``.
        This name is used afterwards to identify edges of the mesh in the Rhino model.

        Examples
        --------
        >>> artist.draw_edges()
        >>> artist.draw_edges(color='#ff0000')
        >>> artist.draw_edges(color=(255, 0, 0))
        >>> artist.draw_edges(keys=self.mesh.edges_on_boundary())
        >>> artist.draw_edges(color={(u, v): '#00ff00' for u, v in self.mesh.edges_on_boundary()})

        """
        keys = keys or list(self.mesh.edges())
        colordict = to_valuedict(keys, color, self.defaults['edge.color'])
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.mesh.vertex_coordinates(u),
                'end'  : self.mesh.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name' : self.mesh.edge_name(u, v)
            })
        return compas_rhinomac.xdraw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for selected vertices of the mesh.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as key-text pairs.
            The default value is ``None``, in which case every vertex of the mesh
            will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to vertex keys in the mesh and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default vertex color (``self.defaults['vertex.color']``).

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.vertex.{}".format(self.mesh.attributes['name'], key)``.

        Examples
        --------
        >>>

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.vertices()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        colordict = to_valuedict(list(textdict.keys()), color, self.defaults['vertex.color'])
        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos'  : self.mesh.vertex_coordinates(key),
                'name' : self.mesh.vertex_name(key),
                'color': colordict[key],
                'text' : textdict[key],
            })
        return compas_rhinomac.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for selected faces of the mesh.

        Parameters
        ----------

        Notes
        -----

        Examples
        --------

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        colordict = to_valuedict(list(textdict.keys()), color, self.defaults['face.color'])
        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos'  : self.mesh.face_center(key),
                'name' : self.mesh.face_name(key),
                'color': colordict[key],
                'text' : textdict[key],
            })
        return compas_rhinomac.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for selected edges of the mesh.

        Parameters
        ----------

        Notes
        -----

        Examples
        --------

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        colordict = to_valuedict(list(textdict.keys()), color, self.defaults['edge.color'])
        labels = []
        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos'  : self.mesh.edge_midpoint(u, v),
                'name' : self.mesh.edge_name(u, v),
                'color': colordict[(u, v)],
                'text' : textdict[(u, v)],
            })
        return compas_rhinomac.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import Polyhedron

    from compas_rhinomac.helpers.artists.meshartist import MeshArtist

    poly = Polyhedron.generate(12)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    artist = MeshArtist(mesh, layer='MeshArtist')

    artist.clear_layer()

    artist.draw_vertices()
    artist.redraw(0.0)

    artist.draw_vertexlabels()
    artist.redraw(1.0)

    artist.draw_faces()
    artist.redraw(1.0)

    artist.draw_facelabels()
    artist.redraw(1.0)

    artist.draw_edges()
    artist.redraw(1.0)

    artist.draw_edgelabels()
    artist.redraw(1.0)
