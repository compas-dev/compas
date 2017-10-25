""""""

from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from compas.utilities import to_valuedict
from compas.visualization.plotters.plotter import Plotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


class MeshPlotter(Plotter):
    """Definition of a plotter object based on matplotlib for compas Networks.

    Parameters
    ----------
    mesh: object
        The mesh to plot.

    Attributes
    ----------
    title : str
        Title of the plot.
    mesh : object
        The mesh to plot.
    vertexcollection : object
        The matplotlib collection for the mesh vertices.
    edgecollection : object
        The matplotlib collection for the mesh edges.
    facecollection : object
        The matplotlib collection for the mesh faces.
    defaults : dict
        Dictionary containing default attributes for vertices and edges.

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.visualization import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text='key')
        plotter.draw_edges()
        plotter.draw_faces()

        plotter.show()


    References
    ----------
    * Hunter, J. D., 2007. Matplotlib: A 2D graphics environment. Computing In Science & Engineering (9) 3, p.90-95.
      Available at: http://ieeexplore.ieee.org/document/4160265/citations

    """

    def __init__(self, mesh, **kwargs):
        """Initialises a mesh plotter object"""
        super(MeshPlotter, self).__init__(**kwargs)
        self.title = 'MeshPlotter'
        self.mesh = mesh
        self.vertexcollection = None
        self.edgecollection = None
        self.facecollection = None
        self.defaults = {
            'vertex.radius'    : 0.15,
            'vertex.facecolor' : '#ffffff',
            'vertex.edgecolor' : '#000000',
            'vertex.edgewidth' : 0.1,
            'vertex.textcolor' : '#000000',
            'vertex.fontsize'  : 10.0,

            'edge.width'    : 0.5,
            'edge.color'    : '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize' : 10.0,

            'face.facecolor' : '#eeeeee',
            'face.edgecolor' : '#eeeeee',
            'face.edgewidth' : 0.1,
            'face.textcolor' : '#000000',
            'face.fontsize'  : 12.0,
        }

    def clear(self):
        """Clears the mesh plotter vertices, edges and faces."""
        self.clear_vertices()
        self.clear_edges()
        self.clear_faces()

    def draw_vertices(self,
                      keys=None,
                      radius=None,
                      text=None,
                      facecolor=None,
                      edgecolor=None,
                      edgewidth=None,
                      textcolor=None,
                      fontsize=None):
        """Draws the mesh vertices.

        Parameters
        ----------
        keys : list
            The keys of the vertices to plot.
        radius : list
            A list of radii for the vertices.
        text : list
            Strings to be displayed on the vertices.
        facecolor : list
            Color for the vertex circle fill.
        edgecolor : list
            Color for the vertex circle edge.
        edgewidth : list
            Width for the vertex circle edge.
        textcolor : list
            Color for the text to be displayed on the vertices.
        fontsize : list
            Font size for the text to be displayed on the vertices.

        Returns
        -------
        object
            The matplotlib vertex collection object.
        """
        keys = keys or list(self.mesh.vertices())

        if text == 'key':
            text = {key: str(key) for key in self.mesh.vertices()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.mesh.vertices())}
        else:
            pass

        radiusdict    = to_valuedict(keys, radius, self.defaults['vertex.radius'])
        textdict      = to_valuedict(keys, text, '')
        facecolordict = to_valuedict(keys, facecolor, self.defaults['vertex.facecolor'])
        edgecolordict = to_valuedict(keys, edgecolor, self.defaults['vertex.edgecolor'])
        edgewidthdict = to_valuedict(keys, edgewidth, self.defaults['vertex.edgewidth'])
        textcolordict = to_valuedict(keys, textcolor, self.defaults['vertex.textcolor'])
        fontsizedict  = to_valuedict(keys, fontsize, self.defaults['vertex.fontsize'])

        points = []
        for key in keys:
            points.append({
                'pos'      : self.mesh.vertex_coordinates(key, 'xy'),
                'radius'   : radiusdict[key],
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_points(points)
        self.vertexcollection = collection
        return collection

    def clear_vertices(self):
        """Clears the mesh plotter vertices."""
        self.vertexcollection.remove()

    def update_vertices(self):
        """Updates the plotter vertex collection based on the mesh."""
        circles = []
        for key in self.mesh.vertices():
            center = self.mesh.vertex_coordinates(key, 'xy')
            radius = 0.1
            circles.append(Circle(center, radius))
        self.vertexcollection.set_paths(circles)

    def draw_edges(self,
                   keys=None,
                   width=None,
                   color=None,
                   text=None,
                   textcolor=None,
                   fontsize=None):
        """Draws the mesh edges.

        Parameters
        ----------
        keys : list
            The keys of the edges to plot.
        width : list
            Width of the mesh edges.
        color : list
            Color for the edge lines.
        text : list
            Strings to be displayed on the edges.
        textcolor : list
            Color for the text to be displayed on the edges.
        fontsize : list
            Font size for the text to be displayed on the edges.

        Returns
        -------
        object
            The matplotlib edge collection object.

        """
        keys = keys or list(self.mesh.edges())

        if text == 'key':
            text = {(u, v): '{}-{}'.format(u, v) for u, v in self.mesh.edges()}
        elif text == 'index':
            text = {(u, v): str(index) for index, (u, v) in enumerate(self.mesh.edges())}
        else:
            pass

        widthdict     = to_valuedict(keys, width, self.defaults['edge.width'])
        colordict     = to_valuedict(keys, color, self.defaults['edge.color'])
        textdict      = to_valuedict(keys, text, '')
        textcolordict = to_valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict  = to_valuedict(keys, fontsize, self.defaults['edge.fontsize'])

        lines = []
        for u, v in keys:
            lines.append({
                'start'    : self.mesh.vertex_coordinates(u, 'xy'),
                'end'      : self.mesh.vertex_coordinates(v, 'xy'),
                'width'    : widthdict[(u, v)],
                'color'    : colordict[(u, v)],
                'text'     : textdict[(u, v)],
                'textcolor': textcolordict[(u, v)],
                'fontsize' : fontsizedict[(u, v)]
            })

        collection = self.draw_lines(lines)
        self.edgecollection = collection
        return collection

    def clear_edges(self):
        """Clears the mesh plotter edges."""
        self.edgecollection.remove()

    def update_edges(self):
        """Updates the plotter edge collection based on the mesh."""
        segments = []
        for u, v in self.mesh.edges():
            segments.append([self.mesh.vertex_coordinates(u, 'xy'), self.mesh.vertex_coordinates(v, 'xy')])
        self.edgecollection.set_segments(segments)

    def draw_faces(self,
                   keys=None,
                   text=None,
                   facecolor=None,
                   edgecolor=None,
                   edgewidth=None,
                   textcolor=None,
                   fontsize=None):
        """Draws the mesh faces.

        Parameters
        ----------
        keys : list
            The keys of the edges to plot.
        text : list
            Strings to be displayed on the edges.
        facecolor : list
            Color for the face fill.
        edgecolor : list
            Color for the face edge.
        edgewidth : list
            Width for the face edge.
        textcolor : list
            Color for the text to be displayed on the edges.
        fontsize : list
            Font size for the text to be displayed on the edges.

        Returns
        -------
        object
            The matplotlib face collection object.
        """
        keys = keys or list(self.mesh.faces())

        if text == 'key':
            text = {key: str(key) for key in self.mesh.faces()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.mesh.faces())}
        else:
            pass

        textdict      = to_valuedict(keys, text, '')
        facecolordict = to_valuedict(keys, facecolor, self.defaults['face.facecolor'])
        edgecolordict = to_valuedict(keys, edgecolor, self.defaults['face.edgecolor'])
        edgewidthdict = to_valuedict(keys, edgewidth, self.defaults['face.edgewidth'])
        textcolordict = to_valuedict(keys, textcolor, self.defaults['face.textcolor'])
        fontsizedict  = to_valuedict(keys, fontsize, self.defaults['face.fontsize'])

        polygons = []
        for key in keys:
            polygons.append({
                'points'   : self.mesh.face_coordinates(key, 'xy'),
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_polygons(polygons)
        self.facecollection = collection
        return collection

    def clear_faces(self):
        """Clears the mesh plotter faces."""
        self.facecollection.remove()

    def update_faces(self):
        """Updates the plotter face collection based on the mesh."""
        polygons = []
        for fkey in self.mesh.faces():
            points = self.mesh.face_coordinates(fkey, 'xy')
            polygons.append(Polygon(points))
        self.facecollection.set_paths(polygons)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text='key')
    plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
