from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Brep
from compas_rhino.conversions import box_to_rhino

import Rhino

from .face import RhinoBrepFace
from .edge import RhinoBrepEdge
from .vertex import RhinoBrepVertex
from .loop import RhinoBrepLoop


class RhinoBrep(Brep):

    def __new__(cls, *args, **kwargs):
        # This breaks the endless recursion when calling `compas.geometry.Brep()` and allows
        # having Brep here as the parent class. Otherwise RhinoBrep() calls Brep.__new__()
        # which calls RhinoBrep() and so on...
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, brep=None):
        super(RhinoBrep, self).__init__()
        self._brep = brep or Rhino.Geometry.Brep()

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_brep(cls, rhino_brep):
        brep = cls(rhino_brep)
        return brep

    @classmethod
    def from_box(cls, box):
        rhino_box = box_to_rhino(box)
        return cls.from_brep(rhino_box.ToBrep())

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def dtype(self):
        # this should make de-serialization backend-agnostic
        # The deserializing type is determined by plugin availability when de-serializing
        # regardless of the context available when serializing.
        return super(RhinoBrep, self).dtype

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @data.setter
    def data(self, data):
        faces = []
        for facedata in data["faces"]:
            face = RhinoBrepFace.from_data(facedata)
            faces.append(face)
        self._brep = self._create_rhino_brep(faces)

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self._brep:
            return [RhinoBrepVertex(v) for v in self._brep.Vertices]

    @property
    def edges(self):
        if self._brep:
            return [RhinoBrepEdge(e) for e in self._brep.Edges]

    @property
    def loops(self):
        if self._brep:
            return [RhinoBrepLoop(l) for l in self._brep.Loops]

    @property
    def faces(self):
        if self._brep:
            return [RhinoBrepFace(f) for f in self._brep.Faces]

    @property
    def frame(self):
        return Frame.worldXY()

    @property
    def area(self):
        if self._brep:
            return self._brep.GetArea()

    @property
    def volume(self):
        if self._brep:
            return self._brep.GetVolume()

    def _create_rhino_brep(self, faces):
        brep = Rhino.Geometry.Brep()
        # TODO re-construct the Brep from the serialized faces
        return brep

