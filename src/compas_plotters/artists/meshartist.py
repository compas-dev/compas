from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters.core.drawing import draw_xpoints_xy
from compas_plotters.core.drawing import draw_xlines_xy
from compas_plotters.core.drawing import draw_xpolygons_xy
from compas_plotters.artists import Artist

__all__ = ['MeshArtist']


class MeshArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__()
        self._mpl_mesh = None
        self.mesh = mesh
        self._vertex_keys = None
        self._mpl_vertex_collection = None

    def vertices_color(self, keys, color):
        colors = self._mpl_vertexcollection.get_facecolor()
        for index, key in enumerate(self.mesh.vertices()):
            if key in keys:
                colors[index] = color
        self._mpl_vertexcollection.set_facecolor(colors)

    def draw(self):
        # add faces
        polygons = []
        for key in self.mesh.faces():
            polygons.append({
                'points': self.mesh.face_coordinates(key),
                'facecolor': '#eeeeee',
                'edgecolor': '#cccccc'
            })
        collection = draw_xpolygons_xy(polygons, self.plotter.axes)
        self._mpl_facecollection = collection
        # add vertices
        points = []
        for key in self.mesh.vertices():
            points.append({
                'pos': self.mesh.vertex_attributes(key, 'xy'),
                'radius': 0.1,
                'text': None,
                'facecolor': '#ffffff',
                'edgecolor': '#000000',
                'edgewidth': 0.5,
                'textcolor': '#000000',
                'fontsize': 6
            })
        collection = draw_xpoints_xy(points, self.plotter.axes)
        self._mpl_vertexcollection = collection
        # add edges
        lines = []
        for key in self.mesh.edges():
            u, v = key
            lines.append({
                'start': self.mesh.vertex_attributes(u, 'xy'),
                'end': self.mesh.vertex_attributes(v, 'xy'),
                'width': 1.0,
                'color': (0, 0, 0)
            })
        collection = draw_xlines_xy(lines, self.plotter.axes)
        self._mpl_edgecollection = collection

    # def redraw(self):
    #     # self._mpl_vertexcollection.set_...
    #     pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas_plotters import Plotter2

    mesh = Mesh.from_polyhedron(6)

    plotter = Plotter2()

    plotter.add(mesh)
    plotter.draw()

    plotter.zoom_extents()
    plotter.show()
