from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from matplotlib.patches import Circle

from compas_plotters.core.drawing import draw_xpoints_xy
from compas_plotters.core.drawing import draw_xlines_xy
from compas_plotters.core.drawing import draw_xpolygons_xy
from compas_plotters.artists import Artist

from matplotlib.patches import Polygon
from compas.utilities import color_to_rgb
from compas_plotters.plotter import Plotter, valuedict

from copy import deepcopy

__all__ = ['DatastructureArtist']


class DatastructureArtist(Artist):
    """"""

    zorder = 1000

    _VERTEX_DEFAULTS =      {
                            0:             {
                                            'radius': 0.5,
                                            'facecolor': '#ffffff',
                                            'edgecolor': '#000000',
                                            'edgewidth': 0.5,
                                            'text': 'key',
                                            'textcolor': '#000000',
                                            'fontsize': 6
                                            },
                            'is_fixed':     {
                                            'identifier': lambda k, a: a.get('is_fixed', False) is True or a.get('is_anchor', False) is True,
                                            'radius': lambda k, v, d: d * 1.5,
                                            'facecolor': '#FFFF00',
                                            }
                            }
    _EDGE_DEFAULTS  =       {
                            0:             {
                                            'width': 1.0,
                                            'color': '#000000',
                                            'textcolor': '#000000',
                                            'fontsize': 10,
                                            },
                            }
    _FACE_DEFAULTS  =       {
                            0:             {
                                            'facecolor': '#eeeeee',
                                            'edgecolor': '#000000',
                                            'edgewidth': 0.1,
                                            'textcolor': '#000000',
                                            'fontsize': 10,
                                            },
                            }

    def __init__(self, datastruct, defaults={}, **kwargs):
        super(DatastructureArtist, self).__init__(datastruct)
        # self._mpl_mesh = None
        self.plotter
        self.item = self.datastruct = datastruct
        self._set_defaults('vertex', defaults, '_VERTEX_DEFAULTS')
        self._set_defaults('edge', defaults, '_EDGE_DEFAULTS')
        self._set_defaults('face', defaults, '_FACE_DEFAULTS')
        self._mpl_vertex_collection = None
        self._mpl_edge_collection = None
        self._mpl_face_collection = None

    def _set_defaults(self, elem, user_defaults, predef_defaults):
        dflts = {} if 'elem' not in user_defaults else user_defaults.pop(elem)
        dflts_0 = deepcopy(getattr(self.__class__, predef_defaults))
        dflts.update(dflts_0)
        setattr(self, '_' + elem + '_defaults', dflts)

    def _get_settings(self, key, attr, defaults_attr):
        dflts   = getattr(self, defaults_attr)
        dflts_0 = dflts[0]
        for _k_1, _v_1a in dflts.items():
            # elements with special settings
            if _k_1 != 0 and _v_1a['identifier'](key, attr) is True:
                dflts_1b = {}
                for _k_0 in dflts_0:
                    _v_0 = dflts_0[_k_0]
                    _v_1b = _v_1a.get(_k_0, _v_0)
                    if callable(_v_1b):
                        _v_1b = _v_1b(key, attr, _v_0)
                    dflts_1b[_k_0] = _v_1b
                return dflts_1b
            # elements to hide
            elif _k_1 != 0 and _v_1a['identifier'](key, attr) is None:
                return None
        # elements with default settings
        return dflts_0

    def get_vertex_settings(self, key, attr):
        return self._get_settings(key, attr, '_vertex_defaults')

    def get_edge_settings(self, key, attr):
        return self._get_settings(key, attr, '_edge_defaults')

    def get_face_settings(self, key, attr):
        return self._get_settings(key, attr, '_face_defaults')

    def draw_vertices(self):
        points = []
        for _k, _a in self.datastruct.vertices(True):
            _settings = self.get_vertex_settings(_k, _a)
            if _settings:
                points.append({
                            'pos': self.datastruct.vertex_attributes(_k, 'xy'),
                            'radius': _settings['radius'],
                            'text': None,
                            'facecolor': _settings['facecolor'],
                            'edgecolor': _settings['edgecolor'],
                            'edgewidth': _settings['edgewidth'],
                            'textcolor': _settings['textcolor'],
                            'fontsize': _settings['fontsize']
                            })
        collection = draw_xpoints_xy(points, self.plotter.axes)
        self._mpl_vertexcollection = collection

    def draw_edges(self):
        lines = []
        for _k, _a in self.datastruct.edges(True):
            _settings = self.get_edge_settings(_k, _a)
            _u, _v = _k
            if _settings:
                lines.append({
                    'start': self.datastruct.vertex_attributes(_u, 'xy'),
                    'end': self.datastruct.vertex_attributes(_v, 'xy'),
                    'width': _settings['width'],
                    'color': _settings['color']
                })
        collection = draw_xlines_xy(lines, self.plotter.axes)
        self._mpl_edgecollection = collection

    def draw_faces(self):
        polygons = []
        for _k, _a in self.datastruct.faces(True):
            _settings = self.get_face_settings(_k, _a)
            if _settings:
                polygons.append({
                    'points': self.datastruct.face_coordinates(_k),
                    'facecolor': _settings['facecolor'],
                    'edgecolor': _settings['edgecolor'],
                })
        collection = draw_xpolygons_xy(polygons, self.plotter.axes)
        self._mpl_facecollection = collection

    def redraw_vertices(self):
        circles = []
        for _k, _a in self.datastruct.vertices(True):
            _settings = self.get_vertex_settings(_k, _a)
            if _settings:
                _c = self.datastruct.vertex_coordinates(_k, 'xy')
                _r = _settings['radius']     #0.25  # radius[key]
                circles.append(Circle(_c, _r))
        self._mpl_vertexcollection.set_paths(circles)

    def redraw_edges(self):
        segments = []
        for u, v in self.datastruct.edges():
            segments.append([self.datastruct.vertex_coordinates(u, 'xy'), self.datastruct.vertex_coordinates(v, 'xy')])
        self._mpl_edgecollection.set_segments(segments)

    def redraw_faces(self, facecolor=None):
        facecolor = valuedict(self.datastruct.faces(), facecolor, '#ffffff')
        polygons = []
        facecolors = []
        for fkey in self.datastruct.faces():
            points = self.datastruct.face_coordinates(fkey, 'xy')
            polygons.append(Polygon(points))
            facecolors.append(color_to_rgb(facecolor[fkey], normalize=True))
        self._mpl_facecollection.set_paths(polygons)
        self._mpl_facecollection.set_facecolor(facecolors)

    def draw(self):
        # add faces
        self.draw_faces()
        # add edges
        self.draw_edges()
        # add vertices
        self.draw_vertices()

    def redraw(self):
        self.redraw_vertices()
        self.redraw_edges()
        self.redraw_faces()

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas_plotters import GeometryPlotter

    mesh = Mesh()
    mesh.add_vertex(x=0., y=0., z=0.)
    mesh.add_vertex(x=10., y=0., z=0.)
    mesh.add_vertex(x=10., y=10., z=0.)
    mesh.add_vertex(x=0., y=10., z=0.)
    mesh.add_vertex(x=5., y=5., z=0., is_fixed=True)
    mesh.add_face([0, 1, 4])
    mesh.add_face([1, 2, 4])
    mesh.add_face([2, 3, 4])
    mesh.add_face([3, 0, 4])

    from compas.geometry import Vector, Point
    from compas.geometry import Rotation

    plotter = GeometryPlotter()

    meshart = plotter.add(mesh)
    plotter.draw()

    from math import radians

    R = Rotation.from_axis_and_angle(Vector(0.0, 0.0, 1.0), radians(5), point=Point(5., 5., 0.))
    for i in range(9):
        mesh.transform(R)
        plotter.redraw(pause=0.1)

    plotter.show()
