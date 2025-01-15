from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Point
from compas.itertools import linspace
from compas.itertools import meshgrid
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .surface import Surface


@pluggable(category="factories")
def nurbssurface_from_cylinder(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_extrusion(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_fill(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_frame(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_interpolation(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_native(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_parameters(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_plane(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_points(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_revolution(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_sphere(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_step(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_torus(cls, *args, **kwargs):
    raise PluginNotInstalledError


class NurbsSurface(Surface):
    """A NURBS surface is defined by control points, weights, knots, and a degree, in two directions U and V.

    Parameters
    ----------
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    points : list[list[:class:`compas.geometry.Point`]], read-only
        The control points as rows along the U direction.
    weights : list[list[float]], read-only
        The weights of the control points.
    knots_u : list[float], read-only
        The knots in the U direction, without multiplicity.
    knots_v : list[float], read-only
        The knots in the V direction, without multiplicity.
    mults_u : list[int], read-only
        Multiplicity of the knots in the U direction.
    mults_v : list[int], read-only
        Multiplicity of the knots in the V direction.
    degree_u : list[int], read-only
        The degree of the surface in the U direction.
    degree_v : list[int], read-only
        The degree of the surface in the V direction.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "items": {"type": "array", "items": Point.DATASCHEMA}},
            "weights": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
            "knots_u": {"type": "array", "items": {"type": "number"}},
            "knots_v": {"type": "array", "items": {"type": "number"}},
            "mults_u": {"type": "array", "items": {"type": "integer"}},
            "mults_v": {"type": "array", "items": {"type": "integer"}},
            "degree_u": {"type": "integer", "exclusiveMinimum": 0},
            "degree_v": {"type": "integer", "exclusiveMinimum": 0},
            "is_periodic_u": {"type": "boolean"},
            "is_periodic_v": {"type": "boolean"},
        },
        "additionalProperties": False,
        "minProperties": 10,
    }

    @property
    def __dtype__(self):
        return "compas.geometry/NurbsSurface"

    @property
    def __data__(self):
        return {
            "points": [[point.__data__ for point in row] for row in self.points],  # type: ignore
            "weights": self.weights,
            "knots_u": self.knots_u,
            "knots_v": self.knots_v,
            "mults_u": self.mults_u,
            "mults_v": self.mults_v,
            "degree_u": self.degree_u,
            "degree_v": self.degree_v,
            "is_periodic_u": self.is_periodic_u,
            "is_periodic_v": self.is_periodic_v,
        }

    @classmethod
    def __from_data__(cls, data):
        """Construct a Nurbs surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
            The constructed surface.

        """
        points = data["points"]  # conversion is not needed because point data can be provided in their raw form as well
        weights = data["weights"]
        knots_u = data["knots_u"]
        knots_v = data["knots_v"]
        mults_u = data["mults_u"]
        mults_v = data["mults_v"]
        degree_u = data["degree_u"]
        degree_v = data["degree_v"]
        is_periodic_u = data["is_periodic_u"]
        is_periodic_v = data["is_periodic_v"]
        return cls.from_parameters(
            points,
            weights,
            knots_u,
            knots_v,
            mults_u,
            mults_v,
            degree_u,
            degree_v,
            is_periodic_u,
            is_periodic_v,
        )

    def __new__(cls, *args, **kwargs):
        if cls is NurbsSurface:
            raise TypeError("Making an instance of `NurbsSurface` using `NurbsSurface()` is not allowed. Please use one of the factory methods instead (`NurbsSurface.from_...`)")
        return object.__new__(cls)

    def __repr__(self):
        return "{0}(points={1!r}, weigths={2}, knots_u={3}, knots_v={4}, mults_u={5}, mults_v={6}, degree_u={7}, degree_v={8}, is_periodic_u={9}, is_periodic_v={10})".format(
            type(self).__name__,
            self.points,
            self.weights,
            self.knots_u,
            self.knots_v,
            self.mults_u,
            self.mults_v,
            self.degree_u,
            self.degree_v,
            self.is_periodic_u,
            self.is_periodic_v,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        raise NotImplementedError

    @property
    def weights(self):
        raise NotImplementedError

    @property
    def knots_u(self):
        raise NotImplementedError

    @property
    def mults_u(self):
        raise NotImplementedError

    @property
    def knotvector_u(self):
        raise NotImplementedError

    @property
    def knots_v(self):
        raise NotImplementedError

    @property
    def mults_v(self):
        raise NotImplementedError

    @property
    def knotvector_v(self):
        raise NotImplementedError

    @property
    def degree_u(self):
        raise NotImplementedError

    @property
    def degree_v(self):
        raise NotImplementedError

    @property
    def domain_u(self):
        raise NotImplementedError

    @property
    def domain_v(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_cylinder(cls, cylinder, *args, **kwargs):
        """Construct a surface from a cylinder.

        Parameters
        ----------
        cylinder : :class:`compas.geometry.Cylinder`
            The cylinder.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_cylinder(cls, cylinder, *args, **kwargs)

    @classmethod
    def from_extrusion(cls, curve, vector, *args, **kwargs):
        """Construct a NURBS surface from an extrusion of a basis curve.

        Note that the extrusion surface is constructed by generating an infill
        between the basis curve and a translated copy with :meth:`from_fill`.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The basis curve for the extrusion.
        vector : :class:`compas.geometry.Vector`
            The extrusion vector, which serves as a translation vector for the basis curve.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_extrusion(cls, curve, vector, *args, **kwargs)

    @classmethod
    def from_fill(cls, curve1, curve2, curve3=None, curve4=None, style="stretch"):
        """Construct a NURBS surface from the infill between two, three or four contiguous NURBS curves.

        Parameters
        ----------
        curve1 : :class:`compas.geometry.NurbsCurve`
        curve2 : :class:`compas.geometry.NurbsCurve`
        curve3 : :class:`compas.geometry.NurbsCurve`, optional.
        curve4 : :class:`compas.geometry.NurbsCurve`, optional.
        style : Literal['stretch', 'coons', 'curved'], optional.

            * ``'stretch'`` produces the flattest patch.
            * ``'curved'`` produces a rounded patch.
            * ``'coons'`` is between stretch and coons.

        Raises
        ------
        ValueError
            If the fill style is not supported.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_fill(cls, curve1, curve2, curve3, curve4, style)

    @classmethod
    def from_frame(cls, frame, *args, **kwargs):
        """Construct a surface from a frame.

        Parameters
        ----------
        frame : :class:`compas.geometry.Frame`
            The plane.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_frame(cls, frame, *args, **kwargs)

    @classmethod
    def from_interpolation(cls, points, *args, **kwargs):
        """Construct a surface from a frame.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]
            The interpolation points.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_interpolation(cls, points, *args, **kwargs)

    @classmethod
    def from_meshgrid(cls, nu=10, nv=10):
        """Construct a NURBS surface from a mesh grid.

        Parameters
        ----------
        nu : int, optional
            Number of control points in the U direction.
        nv : int, optional
            Number of control points in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        UU, VV = meshgrid(linspace(0, nu, nu + 1), linspace(0, nv, nv + 1))
        points = []
        for U, V in zip(UU, VV):
            row = []
            for u, v in zip(U, V):
                row.append(Point(u, v, 0.0))
            points.append(row)
        return cls.from_points(points=points)

    @classmethod
    def from_native(cls, surface):
        """Construct a NURBS surface from a native surface geometry.

        Parameters
        ----------
        surface
            A CAD native surface object.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_native(cls, surface)

    @classmethod
    def from_parameters(
        cls,
        points,
        weights,
        knots_u,
        knots_v,
        mults_u,
        mults_v,
        degree_u,
        degree_v,
        is_periodic_u=False,
        is_periodic_v=False,
    ):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : list[list[[float, float, float] | :class:`compas.geometry.Point`]]
            The control points.
        weights : list[list[float]]
            The weights of the control points.
        knots_u : list[float]
            The knots in the U direction, without multiplicity.
        knots_v : list[float]
            The knots in the V direction, without multiplicity.
        mults_u : list[int]
            Multiplicity of the knots in the U direction.
        mults_v : list[int]
            Multiplicity of the knots in the V direction.
        degree_u : int
            Degree in the U direction.
        degree_v : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_parameters(
            cls,
            points,
            weights,
            knots_u,
            knots_v,
            mults_u,
            mults_v,
            degree_u,
            degree_v,
            is_periodic_u=is_periodic_u,
            is_periodic_v=is_periodic_v,
        )

    @classmethod
    def from_plane(cls, plane, *args, **kwargs):
        """Construct a surface from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_plane(cls, plane, *args, **kwargs)

    @classmethod
    def from_points(cls, points, degree_u=3, degree_v=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : list[list[[float, float, float] | :class:`compas.geometry.Point`]]
            The control points.
        degree_u : int
            Degree in the U direction.
        degree_v : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_points(cls, points, degree_u=degree_u, degree_v=degree_v)

    @classmethod
    def from_sphere(cls, sphere, *args, **kwargs):
        """Construct a surface from a sphere.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`
            The sphere.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_sphere(cls, sphere, *args, **kwargs)

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath : str

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_step(cls, filepath)

    @classmethod
    def from_torus(cls, torus, *args, **kwargs):
        """Construct a surface from a torus.

        Parameters
        ----------
        torus : :class:`compas.geometry.Torus`
            The torus.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return nurbssurface_from_torus(cls, torus, *args, **kwargs)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the surface.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return NurbsSurface.from_parameters(
            self.points,
            self.weights,
            self.knots_u,
            self.knots_v,
            self.mults_u,
            self.mults_v,
            self.degree_u,
            self.degree_v,
            self.is_periodic_u,
            self.is_periodic_v,
        )
