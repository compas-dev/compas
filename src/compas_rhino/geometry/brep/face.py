from compas.geometry import BrepFace
from compas.geometry import Sphere
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas_rhino.geometry import RhinoNurbsSurface
from compas_rhino.geometry.surfaces import RhinoSurface
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import sphere_to_compas
from compas_rhino.conversions import cylinder_to_compas
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane

import Rhino
from Rhino.Geometry import Interval
from Rhino.Geometry import RevSurface

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

    def __init__(self, rhino_face=None, builder=None):
        super(RhinoBrepFace, self).__init__()
        self._builder = builder
        self._loops = None
        self._surface = None
        self._face = None
        if rhino_face:
            self._set_face(rhino_face)

    def _set_face(self, native_face):
        self._face = native_face
        self._loops = [RhinoBrepLoop(loop) for loop in native_face.Loops]
        self._surface = RhinoNurbsSurface.from_rhino(self._face.UnderlyingSurface().ToNurbsSurface())

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        surface_type, surface, uv_domain, plane = self._get_surface_geometry(self._face.UnderlyingSurface())
        return {
            "surface_type": surface_type,
            "surface": surface.data,
            "uv_domain": uv_domain,
            "frame": plane_to_compas_frame(plane).data,  # until all shapes have a frame
            "loops": [loop.data for loop in self._loops],
        }

    @data.setter
    def data(self, value):
        self._surface = self._make_surface_from_data(
            value["surface_type"], value["surface"], value["uv_domain"], value["frame"]
        )
        face_builder = self._builder.add_face(self._surface)
        for loop_data in value["loops"]:
            RhinoBrepLoop.from_data(loop_data, face_builder)
        self._set_face(face_builder.result)

    @classmethod
    def from_data(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`~compas_rhino.geometry.BrepBuilder`
            The object reconstructing the current Brep.

        Returns
        -------
        :class:`~compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """

        obj = cls(builder=builder)
        obj.data = data
        return obj

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
        uv_domain = [[surface.Domain(0)[0], surface.Domain(0)[1]], [surface.Domain(1)[0], surface.Domain(1)[1]]]
        if isinstance(surface, Rhino.Geometry.PlaneSurface):
            _, plane = surface.FrameAt(0.0, 0.0)
            return "plane", plane_to_compas_frame(plane), uv_domain, plane
        if isinstance(surface, Rhino.Geometry.NurbsSurface):
            _, plane = surface.FrameAt(0.0, 0.0)
            return "nurbs", RhinoNurbsSurface.from_rhino(surface), uv_domain, plane
        if isinstance(surface, Rhino.Geometry.RevSurface):
            success, cast_surface = surface.TryGetSphere()
            if success:
                return "sphere", sphere_to_compas(cast_surface), uv_domain, cast_surface.EquatorialPlane
            success, cast_surface = surface.TryGetCylinder()
            if success:
                return "cylinder", cylinder_to_compas(cast_surface), uv_domain, cast_surface.BasePlane
            success, cast_surface = surface.TryGetTorus()
        raise NotImplementedError(
            "Support for surface type: {} is not yet implemented.".format(surface.__class__.__name__)
        )

    def _make_surface_from_data(self, surface_type, surface_data, uv_domain, frame_data):
        u_domain, v_domain = uv_domain
        frame = Frame.from_data(frame_data)  # workaround until all shapes have a frame
        if surface_type == "plane":
            frame = Frame.from_data(surface_data)  # redundancy in shapes which already have a frame
            surface = RhinoSurface.from_frame(frame, u_domain, v_domain)
        elif surface_type == "sphere":
            sphere = self._make_sphere_surface(surface_data, u_domain, v_domain, frame)
            surface = RhinoSurface.from_rhino(sphere)
        elif surface_type == "cylinder":
            cylinder = self._make_cylinder_surface(surface_data, u_domain, v_domain, frame)
            surface = RhinoSurface.from_rhino(cylinder)
        elif surface_type == "nurbs":
            surface = RhinoNurbsSurface.from_data(surface_data)
        elif surface_type == "torus":
            raise NotImplementedError("Support for torus surface is not yet implemented!")
        surface.rhino_surface.SetDomain(0, Interval(*u_domain))
        surface.rhino_surface.SetDomain(1, Interval(*v_domain))
        return surface

    @staticmethod
    def _make_cylinder_surface(surface_data, u_domain, v_domain, frame):
        cylinder = Cylinder.from_data(surface_data)
        cylinder = cylinder_to_rhino(cylinder)
        cylinder.BasePlane = frame_to_rhino_plane(frame)
        surface = RevSurface.CreateFromCylinder(cylinder)
        surface.SetDomain(0, Interval(*u_domain))
        surface.SetDomain(1, Interval(*v_domain))
        return surface

    @staticmethod
    def _make_sphere_surface(surface_data, u_domain, v_domain, frame):
        sphere = Sphere.from_data(surface_data)
        sphere = sphere_to_rhino(sphere)
        # seems Sphere => RevSurface conversion modifies the orientation of the sphere
        # setting the plane here is overriden by this modification and surface ends up oriented differntly than
        # original.
        # sphere.EquatorialPlane = frame_to_rhino_plane(frame)
        surface = RevSurface.CreateFromSphere(sphere)
        surface.SetDomain(0, Interval(*u_domain))
        surface.SetDomain(1, Interval(*v_domain))
        return surface
