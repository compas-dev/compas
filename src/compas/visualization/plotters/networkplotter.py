""""""

from matplotlib.patches import Circle

from compas.visualization.plotters.plotter import Plotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def to_valuedict(keys, value, default):
    value = value or default

    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}

    return valuedict


class NetworkPlotter(Plotter):
    """"""

    def __init__(self, network, **kwargs):
        super(NetworkPlotter, self).__init__(**kwargs)
        self.title = 'NetworkPlotter'
        self.network = network
        self.vertexcollection = None
        self.edgecollection = None
        self.facecollection = None
        self.defaults = {
            'vertex.radius'    : 0.1,
            'vertex.facecolor' : '#ffffff',
            'vertex.edgecolor' : '#000000',
            'vertex.edgewidth' : 1.0,
            'vertex.textcolor' : '#000000',
            'vertex.fontsize'  : 10.0,

            'edge.width'    : 1.0,
            'edge.color'    : '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize' : 10.0,

            'face.facecolor' : '#ffffff',
            'face.edgecolor' : '#000000',
            'face.edgewidth' : 1.0,
            'face.textcolor' : '#000000',
            'face.fontsize'  : 10.0,
        }

    def draw_vertices(self,
                      keys=None,
                      radius=None,
                      text=None,
                      facecolor=None,
                      edgecolor=None,
                      edgewidth=None,
                      textcolor=None,
                      fontsize=None):

        keys = keys or list(self.network.vertices())

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
                'pos'      : self.network.vertex_coordinates(key, 'xy'),
                'radius'   : radiusdict[key],
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_xpoints(points)
        self.vertexcollection = collection
        return collection

    def clear_vertices(self):
        self.vertexcollection.remove()

    def update_vertices(self):
        circles = []
        for key in self.network.vertices():
            center = self.network.vertex_coordinates(key, 'xy')
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

        keys = keys or list(self.network.edges())

        widthdict     = to_valuedict(keys, width, self.defaults['edge.width'])
        colordict     = to_valuedict(keys, color, self.defaults['edge.color'])
        textdict      = to_valuedict(keys, text, '')
        textcolordict = to_valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict  = to_valuedict(keys, fontsize, self.defaults['edge.fontsize'])

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

        collection = self.draw_xlines(lines)
        self.edgecollection = collection
        return collection

    def clear_edges(self):
        self.edgecollection.remove()

    def update_edges(self):
        segments = []
        for u, v in self.network.edges():
            segments.append([self.network.vertex_coordinates(u, 'xy'), self.network.vertex_coordinates(v, 'xy')])
        self.edgecollection.set_segments(segments)

    # move to face network!
    def draw_faces(self,
                   keys=None,
                   text=None,
                   facecolor=None,
                   edgecolor=None,
                   edgewidth=None,
                   textcolor=None,
                   fontsize=None):

        keys = keys or list(self.network.faces())

        textdict      = to_valuedict(keys, text, '')
        facecolordict = to_valuedict(keys, facecolor, self.defaults['face.facecolor'])
        edgecolordict = to_valuedict(keys, edgecolor, self.defaults['face.edgecolor'])
        edgewidthdict = to_valuedict(keys, edgewidth, self.defaults['face.edgewidth'])
        textcolordict = to_valuedict(keys, textcolor, self.defaults['face.textcolor'])
        fontsizedict  = to_valuedict(keys, fontsize, self.defaults['face.fontsize'])

        polygons = []
        for key in keys:
            polygons.append({
                'points'   : self.network.face_coordinates(key, 'xy'),
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_xpolygons(polygons)
        self.facecollection = collection
        return collection


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('lines.obj'))

    plotter = NetworkPlotter(network)

    plotter.defaults['vertex.facecolor'] = '#000000'
    plotter.defaults['vertex.edgecolor'] = '#ffffff'

    plotter.defaults['face.facecolor'] = '#eeeeee'
    plotter.defaults['face.edgewidth'] = 0.0

    plotter.draw_vertices(facecolor={key: '#ff0000' for key in network.vertices() if network.vertex_degree(key) == 2},
                          edgecolor={key: '#ffffff' for key in network.vertices() if network.vertex_degree(key) == 2})

    plotter.draw_edges()

    plotter.show()
