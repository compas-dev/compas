from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import length_vector_xy
from compas.plotters.core.drawing import draw_xlines_xy


__all__ = ['ForcePlotterMixin']


class ForcePlotterMixin(object):

    def draw_loads(self, scale=1.0, tol=1e-3, color=None):
        color = color or '#00ff00'

        loads = []
        for key in self.datastructure.vertices():
            p = self.datastructure.get_vertex_attributes(key, ('px', 'py'))
            l = length_vector_xy(p)

            if l < tol:
                continue

            sp = self.datastructure.get_vertex_attributes(key, 'xy')
            ep = sp[0] + scale * p[0], sp[1] + scale * p[1]

            loads.append({
                'start': sp,
                'end'  : ep,
                'color': color,
                'arrow': 'end',
                'width': 2.0,
                'text' : '{:.1f}'.format(l)
            })
        draw_xlines_xy(loads, self.axes)

    def draw_residuals(self, scale=1.0, tol=1e-3, color=None, identifier='is_anchor'):
        color = color or '#00ffff'

        residuals = []
        for key, attr in self.datastructure.vertices(True):

            if attr[identifier]:
                continue

            r = self.datastructure.get_vertex_attributes(key, ('rx', 'ry'))
            l = length_vector_xy(r)

            if l < tol:
                continue

            sp = self.datastructure.get_vertex_attributes(key, 'xy')
            ep = sp[0] + scale * r[0], sp[1] + scale * r[1]

            residuals.append({
                'start': sp,
                'end'  : ep,
                'color': color,
                'arrow': 'end',
                'width': 2.0,
                'text' : '{:.1f}'.format(l)
            })
        draw_xlines_xy(residuals, self.axes)

    def draw_reactions(self, scale=1.0, tol=1e-3, color=None, identifier='is_anchor'):
        color = color or '#00ff00'

        reactions = []
        for key, attr in self.datastructure.vertices(True):

            if not attr[identifier]:
                continue

            r = self.datastructure.get_vertex_attributes(key, ('rx', 'ry'))
            l = length_vector_xy(r)

            if l < tol:
                continue

            sp = self.datastructure.get_vertex_attributes(key, 'xy')
            ep = sp[0] - scale * r[0], sp[1] - scale * r[1]

            reactions.append({
                'start': sp,
                'end'  : ep,
                'color': color,
                'arrow': 'end',
                'width': 2.0,
                'text' : '{:.1f}'.format(l)
            })
        draw_xlines_xy(reactions, self.axes)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
