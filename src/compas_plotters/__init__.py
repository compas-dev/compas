"""
********************************************************************************
compas_plotters
********************************************************************************

2D visualization framework based on ``matplotlib`` for COMPAS geometry objects and data structures.

.. currentmodule:: compas_plotters

.. code-block:: python

    import random
    import compas

    from compas.geometry import Point, Line, Polygon, Polyline, Circle, Ellipse
    from compas.datastructures import Mesh
    from compas_plotters import Plotter

    a = Point(0, 0, 0)
    b = Point(-3, 3, 0)

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    points = mesh.vertices_attributes('xyz')

    plotter = Plotter()

    plotter.add(a)
    plotter.add(b)
    plotter.add(Line(a, b))
    plotter.add(b - a)

    plotter.add(Polyline(random.sample(points, 7)), linewidth=3.0, color=(1.0, 0, 0))
    plotter.add(Polygon(random.sample(points, 7)), facecolor=(0, 0, 1.0))

    circles = [Circle([point, [0, 0, 1]], random.random()) for point in random.sample(points, 7)]
    ellipses = [Ellipse([point, [0, 0, 1]], random.random(), random.random()) for point in random.sample(points, 7)]

    plotter.add_from_list(circles, facecolor=(0, 1, 1))
    plotter.add_from_list(ellipses, facecolor=(0, 1, 0))

    plotter.add(mesh)

    plotter.zoom_extents()
    plotter.show()


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Plotter


Deprecated
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GeometryPlotter
    NetworkPlotter
    MeshPlotter

"""

__version__ = '1.8.0'

from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403

from ._plotter import BasePlotter  # noqa: F401
from .networkplotter import NetworkPlotter  # noqa: F401
from .meshplotter import MeshPlotter  # noqa: F401
from .geometryplotter import GeometryPlotter  # noqa: F401

from .plotter import Plotter


__all__ = [
    'Plotter'
]
