from compas.geometry import BrepFace
from compas_rhino.geometry import RhinoNurbsSurface

from .loop import RhinoBrepLoop


class RhinoBrepFace(BrepFace):
    """A wrapper for Rhino.Geometry.BrepFace

    Attributes
    ----------
    native_surface : :class:`Rhino.Geometry.Surface`
        The rhino native underlying geometry of this face.
    loops : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise this face.
    surface : :class:`compas_rhino.geometry.RhinoNurbsSurface`
        The compas_rhino wrapper of the underlying geometry of this face.
    boundary : :class:`compas_rhino.geometry.RhinoBrepLoop`, read-only
        The loop which defines the outer boundary of this face.
    holes : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise the holes of this brep, if any.
    is_plane : float, read-only
        True if the geometry of this face is a plane, False otherwise.

    """

    def __init__(self, rhino_face=None):
        super(RhinoBrepFace, self).__init__()
        self._loops = None
        self._surface = None
        self._face = None
        if rhino_face:
            self._set_face(rhino_face)

    def _set_face(self, native_face):
        self._face = native_face
        self._loops = [RhinoBrepLoop(loop) for loop in self._face.Loops]
        self._surface = RhinoNurbsSurface.from_rhino(
            self._face.ToNurbsSurface()
        )  # surface in Rhino will always be NURBS

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        boundary = self._loops[0].data
        holes = [loop.data for loop in self._loops[1:]]
        return {"boundary": boundary, "surface": self._surface.data, "holes": holes}

    @data.setter
    def data(self, value):
        boundary = RhinoBrepLoop.from_data(value["boundary"])
        holes = [RhinoBrepLoop.from_data(loop) for loop in value["holes"]]
        self._loops = [boundary] + holes
        # TODO: should we check surface type here? should we support surfaces other than NURBS?
        self._surface = RhinoNurbsSurface.from_data(value["surface"])

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_surface(self):
        if self._surface:
            return self._surface.rhino_surface

    @property
    def loops(self):
        return self._loops

    @property
    def surface(self):
        return self._surface

    @property
    def boundary(self):
        return self._loops[0]

    @property
    def holes(self):
        return self._loops[1:]

    @property
    def is_plane(self):
        return
