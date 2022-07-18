from compas.data import Data
from compas.geometry import BrepLoop

from .edge import RhinoBrepEdge


class RhinoBrepLoop(BrepLoop):
    def __init__(self, rhino_loop=None):
        super(RhinoBrepLoop, self).__init__()
        self._loop = None
        self._edges = None
        if rhino_loop:
            self._set_loop(rhino_loop)

    def _set_loop(self, native_loop):
        self._loop = native_loop
        self._edges = [RhinoBrepEdge(t.Edge) for t in self._loop.Trims]

    @property
    def data(self):
        return [e.data for e in self._edges]

    @data.setter
    def data(self, value):
        self._edges = [RhinoBrepEdge.from_data(e_data) for e_data in value]
