from compas.utilities import to_valuedict
from compas.visualization.plotters.networkplotter import NetworkPlotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['FaceNetworkPlotter', ]


class FaceNetworkPlotter(NetworkPlotter):
    """"""

    def __init__(self, network, **kwargs):
        super(FaceNetworkPlotter, self).__init__(network, **kwargs)
        self.title = 'FaceNetworkPlotter'
        self.facecollection = None
        self.defaults.update({
            'face.facecolor' : '#eeeeee',
            'face.edgecolor' : '#000000',
            'face.edgewidth' : 0.0,
            'face.textcolor' : '#000000',
            'face.fontsize'  : 10.0,
        })

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

        collection = self.draw_polygons(polygons)
        self.facecollection = collection
        return collection


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import FaceNetwork
    from compas.datastructures import network_find_faces

    network = FaceNetwork.from_obj(compas.get_data('lines.obj'))

    network_find_faces(network, breakpoints=network.leaves())

    plotter = FaceNetworkPlotter(network)

    plotter.draw_vertices()
    plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
