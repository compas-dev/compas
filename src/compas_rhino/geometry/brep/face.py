from compas.geometry import BrepFace
from compas_rhino.geometry import RhinoNurbsSurface
from compas_rhino.conversions import plane_to_compas
from compas_rhino.conversions import sphere_to_compas
from compas_rhino.conversions import cylinder_to_compas
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import cylinder_to_rhino

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
        self._surface = self._face.UnderlyingSurface()

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        boundary = self._loops[0].data
        holes = [loop.data for loop in self._loops[1:]]
        surface_type, surface = self._get_surface_geometry(self._surface)
        return {"boundary": boundary, "holes": holes, "surface_type": surface_type, "surface": surface}

    @data.setter
    def data(self, value):
        boundary = RhinoBrepLoop.from_data(value["boundary"])
        holes = [RhinoBrepLoop.from_data(loop) for loop in value["holes"]]
        self._loops = [boundary] + holes
        type_ = value["surface_type"]
        # TODO: using the new serialization mechanism, surface.to_nurbs() should replace all this branching..
        # TODO: given that Plane, Sphere, Cylinder etc. all implement to_nurbs()
        surface = value["surface"]
        if type_ == "plane":
            surface = self._make_surface_from_plane_loop(surface, boundary)
        elif type_ == "sphere":
            surface = RhinoNurbsSurface.from_sphere(surface)
        elif type_ == "cylinder":
            surface = RhinoNurbsSurface.from_cylinder(surface)
        elif type_ == "torus":
            raise NotImplementedError("Support for torus surface is not yet implemented!")
        self._surface = surface.rhino_surface

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_surface(self):
        return self._surface

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

    @staticmethod
    def _get_surface_geometry(surface):
        # success, cast_surface = surface.TryGetPlane()
        # if success:
        #     return "plane", plane_to_compas(cast_surface)
        # success, cast_surface = surface.TryGetSphere()
        # if success:
        #     return "sphere", sphere_to_compas(cast_surface)
        # success, cast_surface = surface.TryGetCylinder()
        # if success:
        #     return "cylinder", cylinder_to_compas(cast_surface)
        # success, cast_surface = surface.TryGetTorus()
        # if success:
        #     raise NotImplementedError("Support for torus surface is not yet implemented!")
        return "nurbs", RhinoNurbsSurface.from_rhino(surface.ToNurbsSurface())

    # @staticmethod
    # def _make_surface_from_plane_loop(plane, loop):
    #     # TODO: replace guesswork here with an actual calculation..
    #     u_degree, v_degree = 1, 1
    #     u_p_count, v_p_count = 2, 2
    #     curve_lengths = [edge.curve.GetLength() for edge in loop.edges]
    #     max_length = max(curve_lengths)
    #     u_interval, v_interval = (0.0, max_length), (0.0, max_length)
    #     return RhinoNurbsSurface.from_plane(plane, u_interval, v_interval, u_degree, v_degree, u_p_count, v_p_count)

    @staticmethod
    def _make_surface_from_plane_loop(plane, loop):
        # TODO: replace guesswork here with an actual calculation..
        c0 = loop.edges[0].start_point
        c1 = loop.edges[1].start_point
        c2 = loop.edges[2].start_point
        c3 = loop.edges[3].start_point
        surface = RhinoNurbsSurface.from_corners([c3, c2, c1, c0])
        return surface
