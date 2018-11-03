
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'xdraw_labels',
    'xdraw_points',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_polylines',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
]


def wrap_xdrawfunc(f):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_labels(labels, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_points(points, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_lines(lines, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_geodesics(geodesics, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_polylines(polylines, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_breps(faces, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_cylinders(cylinders, cap=False, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_pipes(pipes, cap=2, fit=1.0, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_forces(forces, color, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_spheres(spheres, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_mesh(vertices, faces, name=None, color=None, **kwargs):

    raise NotImplementedError


@wrap_xdrawfunc
def xdraw_faces(faces, **kwargs):

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
