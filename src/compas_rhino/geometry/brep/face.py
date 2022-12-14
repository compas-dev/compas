from compas.geometry import BrepFace
from compas.geometry import Sphere
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas_rhino.geometry import RhinoNurbsSurface
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import sphere_to_compas
from compas_rhino.conversions import cylinder_to_compas
from compas_rhino.conversions import cylinder_to_rhino

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
        self._surface = self._face.UnderlyingSurface()

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        surface_type, surface, uv_domain = self._get_surface_geometry(self._surface)
        return {
            "surface_type": surface_type,
            "surface": surface.data,
            "uv_domain": uv_domain,
            "loops": [loop.data for loop in self._loops],
        }

    @data.setter
    def data(self, value):
        # TODO: using the new serialization mechanism, surface.to_nurbs() should replace all this branching..
        # TODO: given that Plane, Sphere, Cylinder etc. all implement to_nurbs()
        surface = self._make_surface_from_data(value["surface_type"], value["surface"], value["uv_domain"])
        face_builder = self._builder.add_face(surface)
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
        # Some conversions from Surface to NurbsSurface cause info loss (e.g. Cylinder)
        return RhinoNurbsSurface.from_rhino(self._surface.ToNurbsSurface())

    @property
    def boundary(self):
        return self._loops[0]

    @property
    def holes(self):
        return self._loops[1:]

    @property
    def is_plane(self):
        return self._surface.IsPlanar()

    @staticmethod
    def _get_surface_geometry(surface):
        # Rhino has many surface types. We know how to serialize NURBS and otherwise can serialize primitives
        uv_domain = [[surface.Domain(0)[0], surface.Domain(0)[1]], [surface.Domain(1)[0], surface.Domain(1)[1]]]
        success, cast_surface = surface.TryGetSphere()
        if success:
            return "sphere", sphere_to_compas(cast_surface), uv_domain
        success, cast_surface = surface.TryGetCylinder()
        if success:
            cylinder = cylinder_to_compas(cast_surface)
            return "cylinder", cylinder, uv_domain
        success, cast_surface = surface.TryGetTorus()
        if success:
            raise NotImplementedError("Support for torus surface is not yet implemented!")
        success, cast_surface = surface.TryGetPlane()
        if success:
            return "plane", plane_to_compas_frame(cast_surface), uv_domain
        return "nurbs", RhinoNurbsSurface.from_rhino(surface.ToNurbsSurface()), uv_domain

    def _make_surface_from_data(self, surface_type, surface_data, uv_domain):
        u_domain, v_domain = uv_domain
        if surface_type == "plane":
            frame = Frame.from_data(surface_data)
            return RhinoNurbsSurface.from_frame(frame, u_domain, v_domain).rhino_surface
        elif surface_type == "sphere":
            # TODO: check if information is lost during this conversion, similarly to cylinder
            return RhinoNurbsSurface.from_sphere(Sphere.from_data(surface_data)).rhino_surface
        elif surface_type == "cylinder":
            return self._make_cylinder_surface(surface_data, u_domain, v_domain)
        elif surface_type == "nurbs":
            return RhinoNurbsSurface.from_data(surface_data).rhino_surface
        elif surface_type == "torus":
            raise NotImplementedError("Support for torus surface is not yet implemented!")
        raise ValueError("Unknown surface type: {}".format(surface_type))

    @staticmethod
    def _make_cylinder_surface(surface_data, u_domain, v_domain):
        cylinder = Cylinder.from_data(surface_data)
        cylinder = cylinder_to_rhino(cylinder)
        surface = RevSurface.CreateFromCylinder(cylinder)
        surface.SetDomain(0, Interval(*u_domain))
        surface.SetDomain(1, Interval(*v_domain))
        return surface
