from __future__ import absolute_import

import importlib


class NotSupportedError(Exception):
    pass


class DynamicRelaxation(object):
    """Dynamic relaxation algorithm with different backends.

    Parameters
    ----------
    backend : {'python', 'numpy'}, optional
        The backend to use for the algorithm.
        Default is ``'python'``.

    Examples
    --------
    .. plot::
        :include-source:

        import random
        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.utilities import i_to_rgb
        from compas.numerical import DynamicRelaxation

        dva = {
            'is_fixed': False,
            'px': 0.0,
            'py': 0.0,
            'pz': 0.0,
            'rx': 0.0,
            'ry': 0.0,
            'rz': 0.0,
        }

        dea = {
            'qpre': 1.0,
            'fpre': 0.0,
            'lpre': 0.0,
            'linit': 0.0,
            'E': 0.0,
            'radius': 0.0,
        }

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh.update_default_vertex_attributes(dva)
        mesh.update_default_edge_attributes(dea)

        for key, attr in mesh.vertices(True):
            attr['is_fixed'] = mesh.vertex_degree(key) == 2

        for u, v, attr in mesh.edges(True):
            attr['qpre'] = 1.0 * random.randint(1, 7)

        k_i = mesh.key_index()

        vertices = mesh.get_vertices_attributes(('x', 'y', 'z'))
        edges    = [(k_i[u], k_i[v]) for u, v in mesh.edges()]
        fixed    = [k_i[key] for key in mesh.vertices_where({'is_fixed': True})]
        loads    = mesh.get_vertices_attributes(('px', 'py', 'pz'))
        qpre     = mesh.get_edges_attribute('qpre')
        fpre     = mesh.get_edges_attribute('fpre')
        lpre     = mesh.get_edges_attribute('lpre')
        linit    = mesh.get_edges_attribute('linit')
        E        = mesh.get_edges_attribute('E')
        radius   = mesh.get_edges_attribute('radius')

        dr = DynamicRelaxation()

        xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius, kmax=100)

        for key, attr in mesh.vertices(True):
            index = k_i[key]
            attr['x'] = xyz[index][0]
            attr['y'] = xyz[index][1]
            attr['z'] = xyz[index][2]

        for index, (u, v, attr) in enumerate(mesh.edges(True)):
            attr['f'] = f[index]
            attr['l'] = l[index]

        fmax = max(mesh.get_edges_attribute('f'))

        plotter = MeshPlotter(mesh, figsize=(10, 7), fontsize=6)

        plotter.draw_vertices(
            facecolor={key: '#000000' for key in mesh.vertices_where({'is_fixed': True})}
        )

        plotter.draw_edges(
            text={(u, v): '{:.0f}'.format(attr['f']) for u, v, attr in mesh.edges(True)},
            color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in mesh.edges(True)},
            width={(u, v): 10 * attr['f'] / fmax for u, v, attr in mesh.edges(True)}
        )

        plotter.show()

    """

    backends = {
        'python' : None,
        'numpy'  : None
    }

    def __init__(self, backend='python'):
        self._backend = None
        self.backend = backend

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend):
        if backend not in self.backends:
            raise NotSupportedError

        m = importlib.import_module(".dr_{}".format(backend), package="compas.numerical.dr")
        f = getattr(m, "dr_{}".format(backend))
        self.backends[backend] = f
        self._backend = backend

    @property
    def solver(self):
        return self.backends[self.backend]

    def __call__(self, vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                 callback=None, callback_args=None, **kwargs):
        return self.solver(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                           callback=callback, callback_args=callback_args, **kwargs)


__all__ = ['DynamicRelaxation']
