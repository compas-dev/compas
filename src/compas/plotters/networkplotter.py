from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
from matplotlib.patches import Circle

from compas.utilities import valuedict
from compas.utilities import pairwise
from compas.plotters.plotter import Plotter

try:
    basestring
except NameError:
    basestring = str


__all__ = ['NetworkPlotter']


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

        * vertex.radius    : ``0.1``
        * vertex.facecolor : ``'#ffffff``
        * vertex.edgecolor : ``'#000000'``
        * vertex.edgewidth : ``0.5``
        * vertex.textcolor : ``'#000000'``
        * vertex.fontsize  : ``10``
        * edge.width       : ``1.0``
        * edge.color       : ``'#000000'``
        * edge.textcolor   : ``'#000000'``
        * edge.fontsize    : ``10``

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Hunter, J. D., 2007. *Matplotlib: A 2D graphics environment*.
           Computing In Science & Engineering (9) 3, p.90-95.
           Available at: http://ieeexplore.ieee.org/document/4160265/citations.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('lines.obj'))

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(
            text='key',
            facecolor={key: '#ff0000' for key in network.leaves()},
            radius=0.15
        )
        plotter.draw_edges()

        plotter.show()

    """

    def __init__(self, network, **kwargs):
        """Initialises a network plotter object"""
        super(NetworkPlotter, self).__init__(**kwargs)
        self.title = 'NetworkPlotter'
        self.datastructure = network
        self.vertexcollection = None
        self.edgecollection = None
        self.defaults = {
            'vertex.radius'    : 0.1,
            'vertex.facecolor' : '#ffffff',
            'vertex.edgecolor' : '#000000',
            'vertex.edgewidth' : 0.5,
            'vertex.textcolor' : '#000000',
            'vertex.fontsize'  : kwargs.get('fontsize', 10),

            'edge.width'    : 1.0,
            'edge.color'    : '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize' : kwargs.get('fontsize', 10),
        }

    def clear(self):
        """Clears the network plotter edges and vertices."""
        self.clear_vertices()
        self.clear_edges()

    def clear_vertices(self):
        """Clears the netwotk plotter vertices."""
        if self.vertexcollection:
            self.vertexcollection.remove()

    def clear_edges(self):
        """Clears the network object edges."""
        if self.edgecollection:
            self.edgecollection.remove()

    def draw_as_lines(self, color=None, width=None):
        # if len(args) > 0:
        #     return super(MeshPlotter, self).draw_lines(*args, **kwargs)
        lines = []
        for u, v in self.datastructure.edges():
            lines.append({
                'start' : self.datastructure.vertex_coordinates(u, 'xy'),
                'end'   : self.datastructure.vertex_coordinates(v, 'xy'),
                'color' : color,
                'width' : width,
            })
        return super(NetworkPlotter, self).draw_lines(lines)

    def draw_vertices(self,
                      keys=None,
                      radius=None,
                      text=None,
                      facecolor=None,
                      edgecolor=None,
                      edgewidth=None,
                      textcolor=None,
                      fontsize=None,
                      picker=None):
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
        keys = keys or list(self.datastructure.vertices())

        if text == 'key':
            text = {key: str(key) for key in self.datastructure.vertices()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.datastructure.vertices())}
        elif isinstance(text, basestring):
            if text in self.datastructure.default_vertex_attributes:
                default = self.datastructure.default_vertex_attributes[text]
                if isinstance(default, float):
                    text = {key: '{:.1f}'.format(attr[text]) for key, attr in self.datastructure.vertices(True)}
                else:
                    text = {key: str(attr[text]) for key, attr in self.datastructure.vertices(True)}
        else:
            pass

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
                'pos'      : self.datastructure.vertex_coordinates(key, 'xy'),
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

        if picker:
            collection.set_picker(picker)
        return collection

    def update_vertices(self, radius=0.1):
        """Updates the plotter vertex collection based on the network."""
        circles = []
        for key in self.datastructure.vertices():
            center = self.datastructure.vertex_coordinates(key, 'xy')
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
        keys = keys or list(self.datastructure.edges())

        if text == 'key':
            text = {(u, v): '{}-{}'.format(u, v) for u, v in self.datastructure.edges()}
        elif text == 'index':
            text = {(u, v): str(index) for index, (u, v) in enumerate(self.datastructure.edges())}
        else:
            pass

        widthdict     = valuedict(keys, width, self.defaults['edge.width'])
        colordict     = valuedict(keys, color, self.defaults['edge.color'])
        textdict      = valuedict(keys, text, '')
        textcolordict = valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['edge.fontsize'])

        lines = []
        for u, v in keys:
            lines.append({
                'start'    : self.datastructure.vertex_coordinates(u, 'xy'),
                'end'      : self.datastructure.vertex_coordinates(v, 'xy'),
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
        for u, v in self.datastructure.edges():
            segments.append([self.datastructure.vertex_coordinates(u, 'xy'), self.datastructure.vertex_coordinates(v, 'xy')])
        self.edgecollection.set_segments(segments)

    # def draw_path(self, path):
    #     edges = []
    #     for u, v in pairwise(path):
    #         if not network.has_edge(u, v):
    #             u, v = v, u
    #         edges.append((u, v))
    #     self.draw_edges(
    #         color={(u, v): '#ff0000' for u, v in edges},
    #         width={(u, v): 5.0 for u, v in edges}
    #     )


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    plotter = NetworkPlotter(network, figsize=(10, 8))

    plotter.draw_vertices(radius=0.1, picker=10)
    plotter.draw_edges()

    default = [plotter.defaults['vertex.facecolor'] for key in network.vertices()]
    highlight = '#ff0000'

    def on_pick(event):
        index = event.ind[0]

        colors = default[:]
        colors[index] = highlight

        plotter.vertexcollection.set_facecolor(colors)
        plotter.update()

    plotter.register_listener(on_pick)
    plotter.show()
