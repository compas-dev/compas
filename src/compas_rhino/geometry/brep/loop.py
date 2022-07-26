from compas.geometry import BrepLoop

import Rhino

from .edge import RhinoBrepEdge


class LoopType(object):
    UNKNOWN = 0
    OUTER = 1
    INNTER = 2
    SLIT = 3
    CURVE_ON_SURFACE = 4
    POINT_ON_SURFACE = 5


class RhinoBrepLoop(BrepLoop):
    """A wrapper for Rhino.Geometry.BrepLoop"""

    def __init__(self, rhino_loop=None):
        super(RhinoBrepLoop, self).__init__()
        self._loop = None
        self._edges = None
        self._type = LoopType.UNKNOWN
        if rhino_loop:
            self._set_loop(rhino_loop)

    def _set_loop(self, native_loop):
        self._loop = native_loop
        self._type = int(self._loop.LoopType)
        self._edges = [RhinoBrepEdge(t.Edge) for t in self._loop.Trims]

    @property
    def data(self):
        return [e.data for e in self._edges]

    @data.setter
    def data(self, value):
        self._edges = [RhinoBrepEdge.from_data(e_data) for e_data in value]

    @property
    def edges(self):
        return self._edges

    @property
    def is_outer(self):
        return self._type == LoopType.OUTER

    @property
    def is_inner(self):
        return self._type == LoopType.INNTER

    @property
    def loop_type(self):
        return Rhino.Geometry.BrepLoopType(self._type)
