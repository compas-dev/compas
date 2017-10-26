""""""

from matplotlib.patches import Circle

from compas.utilities import valuedict
from compas.visualization.plotters.plotter import Plotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['NetworkPlotter', ]


class NetworkPlotter(Plotter):
    """Definition of a plotter object based on matplotlib for compas Networks.

    Parameters
    ----------
    network: object
        The network to plot.

    Attributes
    ----------
    title : str
        Title of the plot.
    network : object
        The network to plot.
    vertexcollection : object
        The matplotlib collection for the network vertices.
    edgecollection : object
        The matplotlib collection for the network edges.
    defaults : dict
        Dictionary containing default attributes for vertices and edges.

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.visualization import NetworkPlotter

        network = Network.from_obj(compas.get('lines.obj'))

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(
            text='key',
            facecolor={key: '#ff0000' for key in network.leaves()}
        )
        plotter.draw_edges()

        plotter.show()

    References
    ----------
    * Hunter, J. D., 2007. Matplotlib: A 2D graphics environment. Computing In Science & Engineering (9) 3, p.90-95.
      Available at: http://ieeexplore.ieee.org/document/4160265/citations

    """

    def __init__(self, network, **kwargs):
        """Initialises a network plotter object"""
        super(NetworkPlotter, self).__init__(**kwargs)
        self.title = 'NetworkPlotter'
        self.network = network
        self.vertexcollection = None
        self.edgecollection = None
        self.defaults = {
            'vertex.radius'    : 0.15,
            'vertex.facecolor' : '#ffffff',
            'vertex.edgecolor' : '#000000',
            'vertex.edgewidth' : 1.0,
            'vertex.textcolor' : '#000000',
            'vertex.fontsize'  : 10.0,

            'edge.width'    : 1.0,
            'edge.color'    : '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize' : 10.0,
        }

    def clear(self):
        """Clears the network plotter edges and vertices."""
        self.clear_vertices()
        self.clear_edges()

    def clear_vertices(self):
        """Clears the netwotk plotter vertices."""
        self.vertexcollection.remove()

    def clear_edges(self):
        """Clears the network object edges."""
        self.edgecollection.remove()

    def draw_vertices(self,
                      keys=None,
                      radius=None,
                      text=None,
                      facecolor=None,
                      edgecolor=None,
                      edgewidth=None,
                      textcolor=None,
                      fontsize=None):
        """Draws the network vertices.

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
            The matplotlib point collection object.

        """
        keys = keys or list(self.network.vertices())

        radiusdict    = valuedict(keys, radius, self.defaults['vertex.radius'])
        textdict      = valuedict(keys, text, '')
        facecolordict = valuedict(keys, facecolor, self.defaults['vertex.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.defaults['vertex.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.defaults['vertex.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.defaults['vertex.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['vertex.fontsize'])

        points = []
        for key in keys:
            points.append({
                'pos'      : self.network.vertex_coordinates(key, 'xy'),
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

    def update_vertices(self):
        """Updates the plotter vertex collection based on the network."""
        circles = []
        for key in self.network.vertices():
            center = self.network.vertex_coordinates(key, 'xy')
            radius = 0.15
            circles.append(Circle(center, radius))
        self.vertexcollection.set_paths(circles)

    def draw_edges(self,
                   keys=None,
                   width=None,
                   color=None,
                   text=None,
                   textcolor=None,
                   fontsize=None):
        """Draws the network edges.

        Parameters
        ----------
        keys : list
            The keys of the edges to plot.
        width : list
            Width of the network edges.
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
            The matplotlib line collection object.

        """
        keys = keys or list(self.network.edges())

        widthdict     = valuedict(keys, width, self.defaults['edge.width'])
        colordict     = valuedict(keys, color, self.defaults['edge.color'])
        textdict      = valuedict(keys, text, '')
        textcolordict = valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['edge.fontsize'])

        lines = []
        for u, v in keys:
            lines.append({
                'start'    : self.network.vertex_coordinates(u, 'xy'),
                'end'      : self.network.vertex_coordinates(v, 'xy'),
                'width'    : widthdict[(u, v)],
                'color'    : colordict[(u, v)],
                'text'     : textdict[(u, v)],
                'textcolor': textcolordict[(u, v)],
                'fontsize' : fontsizedict[(u, v)]
            })

        collection = self.draw_lines(lines)
        self.edgecollection = collection
        return collection

    def update_edges(self):
        """Updates the plotter edge collection based on the network."""
        segments = []
        for u, v in self.network.edges():
            segments.append([self.network.vertex_coordinates(u, 'xy'), self.network.vertex_coordinates(v, 'xy')])
        self.edgecollection.set_segments(segments)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network

    network = Network.from_obj(compas.get('lines.obj'))

    plotter = NetworkPlotter(network)

    plotter.draw_vertices()
    plotter.draw_edges()

    plotter.show()
