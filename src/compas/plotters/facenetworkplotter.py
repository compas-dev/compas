from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import valuedict
from compas.plotters.networkplotter import NetworkPlotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['FaceNetworkPlotter', ]


class FaceNetworkPlotter(NetworkPlotter):
    """Definition of a plotter object based on matplotlib [hunter2007]_ for compas FaceNetworks.

    Parameters
    ----------
    network: object
        The FaceNetwork to plot.

    Attributes
    ----------
    title : str
        Title of the plot.
    facecollection : object
        The matplotlib collection for the mesh faces.
    defaults : dict
        Dictionary containing default attributes for vertices and edges.


    """

    def __init__(self, network, **kwargs):
        """Initialises a facenetwork plotter object"""
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
        """Draws the network faces.

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
        keys = keys or list(self.datastructure.faces())

        textdict      = valuedict(keys, text, '')
        facecolordict = valuedict(keys, facecolor, self.defaults['face.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.defaults['face.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.defaults['face.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.defaults['face.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['face.fontsize'])

        polygons = []
        for key in keys:
            polygons.append({
                'points'   : self.datastructure.face_coordinates(key, 'xy'),
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
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import FaceNetwork
    from compas.topology import network_find_faces

    network = FaceNetwork.from_obj(compas.get('lines.obj'))

    network_find_faces(network, breakpoints=network.leaves())

    plotter = FaceNetworkPlotter(network, figsize=(10, 7))

    plotter.draw_vertices()
    plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
