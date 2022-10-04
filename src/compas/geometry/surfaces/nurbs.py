from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable
from compas.geometry import Point
from compas.utilities import linspace
from compas.utilities import meshgrid

from .surface import Surface


@pluggable(category="factories")
def new_nurbssurface(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_nurbssurface_from_points(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_nurbssurface_from_fill(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_nurbssurface_from_step(cls, *args, **kwargs):
    raise NotImplementedError


class NurbsSurface(Surface):
    """A NURBS surface is defined by control points, weights, knots, and a degree, in two directions U and V.

    Parameters
    ----------
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    points : list[list[:class:`~compas.geometry.Point`]], read-only
        The control points as rows along the U direction.
    weights : list[list[float]], read-only
        The weights of the control points.
    u_knots : list[float], read-only
        The knots in the U direction, without multiplicity.
    v_knots : list[float], read-only
        The knots in the V direction, without multiplicity.
    u_mults : list[int], read-only
        Multiplicity of the knots in the U direction.
    v_mults : list[int], read-only
        Multiplicity of the knots in the V direction.
    u_degree : list[int], read-only
        The degree of the surface in the U direction.
    v_degree : list[int], read-only
        The degree of the surface in the V direction.

    """

    def __new__(cls, *args, **kwargs):
        return new_nurbssurface(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(NurbsSurface, self).__init__(name=name)

    def __str__(self):
        lines = [
            "NurbsSurface",
            "------------",
            "Points: {}".format(self.points),
            "Weights: {}".format(self.weights),
            "U Knots: {}".format(self.u_knots),
            "V Knots: {}".format(self.v_knots),
            "U Mults: {}".format(self.u_mults),
            "V Mults: {}".format(self.v_mults),
            "U Degree: {}".format(self.u_degree),
            "V Degree: {}".format(self.v_degree),
            "U Domain: {}".format(self.u_domain),
            "V Domain: {}".format(self.v_domain),
            "U Periodic: {}".format(self.is_u_periodic),
            "V Periodic: {}".format(self.is_v_periodic),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : The schema of the data representation."""
        from schema import Schema
        from compas.data import is_float3
        from compas.data import is_sequence_of_int
        from compas.data import is_sequence_of_float

        return Schema(
            {
                "points": lambda points: all(is_float3(point) for point in points),
                "weights": is_sequence_of_float,
                "u_knots": is_sequence_of_float,
                "v_knots": is_sequence_of_float,
                "u_mults": is_sequence_of_int,
                "v_mults": is_sequence_of_int,
                "u_degree": int,
                "v_degree": int,
                "is_u_periodic": bool,
                "is_v_periodic": bool,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """dict : The schema of the data representation in JSON format."""
        raise NotImplementedError

    @property
    def dtype(self):
        """str : The type of the object in the form of a '2-level' import and a class name."""
        return "compas.geometry/NurbsSurface"

    @property
    def data(self):
        """dict : Representation of the curve as a dict containing only native Python objects."""
        return {
            "points": [[point.data for point in row] for row in self.points],
            "weights": self.weights,
            "u_knots": self.u_knots,
            "v_knots": self.v_knots,
            "u_mults": self.u_mults,
            "v_mults": self.v_mults,
            "u_degree": self.u_degree,
            "v_degree": self.v_degree,
            "is_u_periodic": self.is_u_periodic,
            "is_v_periodic": self.is_v_periodic,
        }

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.NurbsSurface`
            The constructed surface.

        """
        points = [[Point.from_data(point) for point in row] for row in data["points"]]
        weights = data["weights"]
        u_knots = data["u_knots"]
        v_knots = data["v_knots"]
        u_mults = data["u_mults"]
        v_mults = data["v_mults"]
        u_degree = data["u_degree"]
        v_degree = data["v_degree"]
        is_u_periodic = data["is_u_periodic"]
        is_v_periodic = data["is_v_periodic"]
        return cls.from_parameters(
            points,
            weights,
            u_knots,
            v_knots,
            u_mults,
            v_mults,
            u_degree,
            v_degree,
            is_u_periodic,
            is_v_periodic,
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
    def u_knots(self):
        raise NotImplementedError

    @property
    def v_knots(self):
        raise NotImplementedError

    @property
    def u_mults(self):
        raise NotImplementedError

    @property
    def v_mults(self):
        raise NotImplementedError

    @property
    def u_degree(self):
        raise NotImplementedError

    @property
    def v_degree(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(
        cls,
        points,
        weights,
        u_knots,
        v_knots,
        u_mults,
        v_mults,
        u_degree,
        v_degree,
        is_u_periodic=False,
        is_v_periodic=False,
    ):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : list[list[[float, float, float] | :class:`~compas.geometry.Point`]]
            The control points.
        weights : list[list[float]]
            The weights of the control points.
        u_knots : list[float]
            The knots in the U direction, without multiplicity.
        v_knots : list[float]
            The knots in the V direction, without multiplicity.
        u_mults : list[int]
            Multiplicity of the knots in the U direction.
        v_mults : list[int]
            Multiplicity of the knots in the V direction.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`~compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_parameters(
            cls,
            points,
            weights,
            u_knots,
            v_knots,
            u_mults,
            v_mults,
            u_degree,
            v_degree,
            is_u_periodic=is_u_periodic,
            is_v_periodic=is_v_periodic,
        )

    @classmethod
    def from_points(cls, points, u_degree=3, v_degree=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : list[list[[float, float, float] | :class:`~compas.geometry.Point`]]
            The control points.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`~compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_points(cls, points, u_degree=u_degree, v_degree=v_degree)

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
        :class:`~compas.geometry.NurbsSurface`

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
        :class:`~compas.geometry.NurbsSurface`

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
        :class:`~compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_fill(cls, curve1, curve2, curve3, curve4, style)

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
        :class:`~compas.geometry.NurbsSurface`

        """
        return NurbsSurface.from_parameters(
            self.points,
            self.weights,
            self.u_knots,
            self.v_knots,
            self.u_mults,
            self.v_mults,
            self.u_degree,
            self.v_degree,
            self.is_u_periodic,
            self.is_v_periodic,
        )
