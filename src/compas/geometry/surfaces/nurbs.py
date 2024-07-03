from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Point
from compas.itertools import linspace
from compas.itertools import meshgrid
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .surface import Surface


@pluggable(category="factories")
def new_nurbssurface_from_native(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_nurbssurface_from_plane(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_nurbssurface_from_points(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_nurbssurface_from_fill(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_nurbssurface_from_step(cls, *args, **kwargs):
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
        data = super(NurbsSurface, self).__data__
        data["points"] = [[point.__data__ for point in row] for row in self.points]  # type: ignore
        data["weights"] = self.weights
        data["knots_u"] = self.knots_u
        data["knots_v"] = self.knots_v
        data["mults_u"] = self.mults_u
        data["mults_v"] = self.mults_v
        data["degree_u"] = self.degree_u
        data["degree_v"] = self.degree_v
        data["is_periodic_u"] = self.is_periodic_u
        data["is_periodic_v"] = self.is_periodic_v
        return data

    @classmethod
    def __from_data__(cls, data):
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`
            The constructed surface.

        """
        frame = Frame.__from_data__(data["frame"])
        domain_u = data["domain_u"]
        domain_v = data["domain_v"]
        points = [[Point.__from_data__(point) for point in row] for row in data["points"]]
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
            frame,
            domain_u,
            domain_v,
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
        raise AssertionError("NurbsSurface() is protected. Use NurbsSurface.from_...() to construct a NurbsSurface object.")

    def __init__(self, name=None):
        super(NurbsSurface, self).__init__(name=name)

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

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, surface):
        """Construct a NURBS surface from a surface object.

        Parameters
        ----------
        surface : :class:`Rhino.Geometry.NurbsSurface`
            A CAD native surface object.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
            A COMPAS NURBS surface.

        """
        return new_nurbssurface_from_native(cls, surface)

    @classmethod
    def from_parameters(
        cls,
        frame,
        domain_u,
        domain_v,
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
        return new_nurbssurface_from_parameters(
            cls,
            frame,
            domain_u,
            domain_v,
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
        return new_nurbssurface_from_points(cls, points, degree_u=degree_u, degree_v=degree_v)

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
    def from_step(cls, filepath):
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath : str

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_step(cls, filepath)

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
        return new_nurbssurface_from_fill(cls, curve1, curve2, curve3, curve4, style)

    @classmethod
    def from_plane(cls, plane, u_degree=1, v_degree=1):
        return new_nurbssurface_from_plane(cls, plane, u_degree, v_degree)

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
