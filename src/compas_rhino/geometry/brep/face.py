from compas.data import Data
from compas.geometry import BrepFace
from compas_rhino.geometry import RhinoNurbsSurface

from .loop import RhinoBrepLoop


class RhinoBrepFace(BrepFace):

    TOLERANCE = 1e-6

    def __init__(self, rhino_face=None):
        super(RhinoBrepFace, self).__init__()
        self._loops = None
        self._surface = None
        self._face = None
        if rhino_face:
            self._set_face(rhino_face)

    def _set_face(self, native_face):
        self._face = native_face
        self._loops = [RhinoBrepLoop(l) for l in self._face.Brep.Loops]
        self._surface = RhinoNurbsSurface.from_rhino(self._face.ToNurbsSurface())

    @property
    def data(self):
        boundary = self._loops[0].data
        holes = None
        if len(self._loops) > 1:
            holes = [loop.data for loop in self._loops[1:]]
        return {"boundary": boundary, "surface": self._surface, "holes": holes}

    @data.setter
    def data(self, value):
        boundary = RhinoBrepLoop.from_data(value["boundary"])
        holes = [RhinoBrepLoop.from_data(l) for l in value["holes"]]
        self._loops = boundary + holes
        self._surface = RhinoNurbsSurface.from_data(value["surface"])
