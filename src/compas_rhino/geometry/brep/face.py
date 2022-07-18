from compas.data import Data
from compas_rhino.geometry import RhinoNurbsSurface

from .loop import RhinoBrepLoop


class RhinoBrepFace(Data):

    TOLERANCE = 1e-6

    def __init__(self, rhino_face=None):
        super(RhinoBrepFace, self).__init__()
        self.loops = None
        self.surface = None
        self._face = None
        if rhino_face:
            self._set_face(rhino_face)

    def _set_face(self, native_face):
        self._face = native_face
        self.loops = [RhinoBrepLoop(l) for l in self._face.Brep.Loops]
        self.surface = RhinoNurbsSurface.from_rhino(self._face.ToNurbsSurface())

    @property
    def data(self):
        boundary = self.loops[0].data
        holes = None
        if len(self.loops) > 1:
            holes = [loop.data for loop in self.loops[1:]]
        return {"boundary": boundary, "surface": self.surface, "holes": holes}

    @data.setter
    def data(self, value):
        boundary = RhinoBrepLoop.from_data(value["boundary"])
        holes = [RhinoBrepLoop.from_data(l) for l in value["holes"]]
        self.loops = boundary + holes
        self.surface = RhinoNurbsSurface.from_data(value["surface"])
