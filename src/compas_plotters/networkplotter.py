from matplotlib.patches import Circle
from compas_plotters.plotter import Plotter, valuedict


__all__ = ['NetworkPlotter']


class NetworkPlotter(Plotter):
    """Plotter for the visualisation of COMPAS Networks.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        The network to plot.

    Attributes
    ----------
    title : str
        Title of the plot.
    network : object
        The network to plot.
    nodecollection : object
        The matplotlib collection for the network nodes.
    edgecollection : object
        The matplotlib collection for the network edges.
    defaults : dict
        Dictionary containing default attributes for nodes and edges.

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
        from compas_plotters import NetworkPlotter

        network = Network.from_obj(compas.get('lines.obj'))

        plotter = NetworkPlotter(network)
        plotter.draw_nodes(
            text='key',
            facecolor={key: '#ff0000' for key in network.leaves()},
            radius=0.15
        )
        plotter.draw_edges()
        plotter.show()

    """

    def __init__(self, network, **kwargs):
        super().__init__(**kwargs)
        self.title = 'NetworkPlotter'
        self.datastructure = network
        self.nodecollection = None
        self.edgecollection = None
        self.defaults = {
            'node.radius': 0.1,
            'node.facecolor': '#ffffff',
            'node.edgecolor': '#000000',
            'node.edgewidth': 0.5,
            'node.textcolor': '#000000',
            'node.fontsize': kwargs.get('fontsize', 10),

            'edge.width': 1.0,
            'edge.color': '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize': kwargs.get('fontsize', 10),
        }

    def clear(self):
        """Clears the network plotter edges and nodes."""
        self.clear_nodes()
        self.clear_edges()

    def clear_nodes(self):
        """Clears the netwotk plotter nodes."""
        if self.nodecollection:
            self.nodecollection.remove()

    def clear_edges(self):
        """Clears the network object edges."""
        if self.edgecollection:
            self.edgecollection.remove()

    # def draw_as_lines(self, color=None, width=None):
    #     # if len(args) > 0:
    #     #     return super(MeshPlotter, self).draw_lines(*args, **kwargs)
    #     lines = []
    #     for u, v in self.datastructure.edges():
    #         lines.append({
    #             'start': self.datastructure.node_coordinates(u, 'xy'),
    #             'end': self.datastructure.node_coordinates(v, 'xy'),
    #             'color': color,
    #             'width': width,
    #         })
    #     return super(NetworkPlotter, self).draw_lines(lines)

    def draw_nodes(self,
                   keys=None,
                   radius=None,
                   text=None,
                   facecolor=None,
                   edgecolor=None,
                   edgewidth=None,
                   textcolor=None,
                   fontsize=None,
                   picker=None):
        """Draws the network nodes.

        Parameters
        ----------
        keys : list
            The keys of the nodes to plot.
        radius : {float, dict}
            A list of radii for the nodes.
        text : {{'index', 'key'}, str, dict}
            Strings to be displayed on the nodes.
        facecolor : {color, dict}
            Color for the node circle fill.
        edgecolor : {color, dict}
            Color for the node circle edge.
        edgewidth : {float, dict}
            Width for the node circle edge.
        textcolor : {color, dict}
            Color for the text to be displayed on the nodes.
        fontsize : {int, dict}
            Font size for the text to be displayed on the nodes.

        Returns
        -------
        object
            The matplotlib point collection object.

        """
        keys = keys or list(self.datastructure.nodes())

        if text == 'key':
            text = {key: str(key) for key in self.datastructure.nodes()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.datastructure.nodes())}
        elif isinstance(text, str):
            if text in self.datastructure.default_node_attributes:
                default = self.datastructure.default_node_attributes[text]
                if isinstance(default, float):
                    text = {key: '{:.1f}'.format(attr[text]) for key, attr in self.datastructure.nodes(True)}
                else:
                    text = {key: str(attr[text]) for key, attr in self.datastructure.nodes(True)}
        else:
            pass

        radiusdict = valuedict(keys, radius, self.defaults['node.radius'])
        textdict = valuedict(keys, text, '')
        facecolordict = valuedict(keys, facecolor, self.defaults['node.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.defaults['node.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.defaults['node.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.defaults['node.textcolor'])
        fontsizedict = valuedict(keys, fontsize, self.defaults['node.fontsize'])

        points = []
        for key in keys:
            points.append({
                'pos': self.datastructure.node_coordinates(key, 'xy'),
                'radius': radiusdict[key],
                'text': textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize': fontsizedict[key]
            })

        collection = self.draw_points(points)
        self.nodecollection = collection

        if picker:
            collection.set_picker(picker)
        return collection

    def update_nodes(self, radius=0.1):
        """Updates the plotter node collection based on the network."""
        circles = []
        for key in self.datastructure.nodes():
            center = self.datastructure.node_coordinates(key, 'xy')
            circles.append(Circle(center, radius))
        self.nodecollection.set_paths(circles)

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
        width : {float, dict}
            Width of the network edges.
        color : {color, dict}
            Color for the edge lines.
        text : {{'index', 'key'}, str, dict}
            Strings to be displayed on the edges.
        textcolor : {color, dict}
            Color for the text to be displayed on the edges.
        fontsize : {int, dict}
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

        widthdict = valuedict(keys, width, self.defaults['edge.width'])
        colordict = valuedict(keys, color, self.defaults['edge.color'])
        textdict = valuedict(keys, text, '')
        textcolordict = valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict = valuedict(keys, fontsize, self.defaults['edge.fontsize'])

        lines = []
        for u, v in keys:
            lines.append({
                'start': self.datastructure.node_coordinates(u, 'xy'),
                'end': self.datastructure.node_coordinates(v, 'xy'),
                'width': widthdict[(u, v)],
                'color': colordict[(u, v)],
                'text': textdict[(u, v)],
                'textcolor': textcolordict[(u, v)],
                'fontsize': fontsizedict[(u, v)]
            })

        collection = self.draw_lines(lines)
        self.edgecollection = collection
        return collection

    def update_edges(self):
        """Updates the plotter edge collection based on the network."""
        segments = []
        for u, v in self.datastructure.edges():
            segments.append([self.datastructure.node_coordinates(u, 'xy'), self.datastructure.node_coordinates(v, 'xy')])
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
    pass
