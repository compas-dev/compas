from compas.geometry import Geometry
from compas_rhino.conversions import box_to_rhino

from Rhino.Geometry import Brep

from .face import RhinoBRepFace
from .edge import RhinoBRepEdge
from .vertex import RhinoBRepVertex
from .loop import RhinoBRepLoop


class RhinoBRep(Geometry):
    def __init__(self):
        super(RhinoBRep, self).__init__()
        self.rhino_brep = None

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
            face = RhinoBRepFace.from_data(facedata)
            faces.append(face)
        self.rhino_brep = BRep.from_faces(faces).rhino_brep

    @classmethod
    def from_faces(cls, faces):
        brep = Brep()

    @property
    def points(self):
        if self.rhino_brep:
            return [RhinoBRepVertex(v) for v in self.rhino_brep.Vertices]

    @property
    def edges(self):
        if self.rhino_brep:
            return [RhinoBRepEdge(e) for e in self.rhino_brep.Edges]

    @property
    def loops(self):
        if self.rhino_brep:
            return [RhinoBRepLoop(l) for l in self.rhino_brep.Loops]

    @property
    def faces(self):
        if self.rhino_brep:
            return [RhinoBRepFace(f) for f in self.rhino_brep.Faces]

    @property
    def frame(self):
        """TODO: what to do here? Brep has no Frame/plane information"""
        # if self.rhino_brep:
        #     return self.rhino_brep.Frame
        pass

    @property
    def area(self):
        if self.rhino_brep:
            return self.rhino_brep.GetArea()

    @property
    def volume(self):
        if self.rhino_brep:
            return self.rhino_brep.GetVolume()

    @classmethod
    def from_shape(cls, shape):
        brep = cls()
        brep.rhino_brep = shape
        return brep

    @classmethod
    def from_box(cls, box):
        rhino_box = box_to_rhino(box)
        return cls.from_shape(rhino_box.ToBrep())
