from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface


class PlanarSurface(Surface):
    """A planar surface is defined by a local coordinate system and a size.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the surface.
        Default is ``None``, in which case the world coordinate system is used.
    xsize : float, optional
        The size of the surface in the local X-direction.
    ysize : float, optional
        The size of the surface in the local Y-direction.
    name : str, optional
        The name of the surface.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "xsize": {"type": "number", "minimum": 0},
            "ysize": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["xsize", "ysize", "frame"],
    }

    @property
    def __data__(self):
        return {
            "xsize": self.xsize,
            "ysize": self.ysize,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            xsize=data["xsize"],
            ysize=data["ysize"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, xsize=1.0, ysize=1.0, frame=None, name=None):
        super(PlanarSurface, self).__init__(frame=frame, name=name)
        self._xsize = None
        self._ysize = None
        self.xsize = xsize
        self.ysize = ysize

    def __repr__(self):
        return "{0}(xsize={1}, ysize={2}, frame={3!r})".format(
            type(self).__name__,
            self.xsize,
            self.ysize,
            self.frame,
        )

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_xsize = other.xsize
            other_ysize = other.ysize
        except Exception:
            return False
        return self.xsize == other_xsize and self.ysize == other_ysize and self.frame == other_frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def xsize(self):
        if self._xsize is None:
            raise ValueError("The size of the surface in the local X-direction is not set.")
        return self._xsize

    @xsize.setter
    def xsize(self, xsize):
        if xsize < 0:
            raise ValueError("The size of the surface in the local X-direction should be at least zero.")
        self._xsize = float(xsize)

    @property
    def ysize(self):
        if self._ysize is None:
            raise ValueError("The size of the surface in the local Y-direction is not set.")
        return self._ysize

    @ysize.setter
    def ysize(self, ysize):
        if ysize < 0:
            raise ValueError("The size of the surface in the local Y-direction should be at least zero.")
        self._ysize = float(ysize)

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_size(cls, plane, xsize, ysize):
        """Construct a planar surface from a plane and x and y sizes.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the sphere.
        xsize : float
            The size of the sphere in the local X-direction.
        ysize : float
            The size of the sphere in the local Y-direction.

        Returns
        -------
        :class:`compas.geometry.PlanarSurface`
            A planar surface.

        """
        return cls(xsize, ysize, frame=Frame.from_plane(plane))

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_plane(self):
        """Convert the planar surface to a plane.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The plane of the planar surface.

        """
        return Plane(self.frame.point, self.frame.zaxis)

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, u, v, world=True):
        """Construct a point on the planar surface.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.
        world : bool, optional
            If ``True``, return the point in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Point`
            A point on the sphere.

        """
        point = Point(u, v, 0)
        if world:
            point.transform(self.transformation)
        return point
        # return self.frame.point + self.frame.xaxis * u + self.frame.yaxis * v

    def normal_at(self, u=None, v=None, world=True):
        """Construct the normal at a point on the planar surface.

        Parameters
        ----------
        u : float, optional
            The first parameter.
            The parameter is optional, because the normal is the same everywhere.
        v : float, optional
            The second parameter.
            The parameter is optional, because the normal is the same everywhere.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector.

        """
        if world:
            return self.frame.zaxis
        return Vector(0, 0, 1)

    def frame_at(self, u=None, v=None):
        """Construct a frame at a point on the planar surface.

        Parameters
        ----------
        u : float, optional
            The first parameter.
            The parameter is optional, because the frame is the same everywhere.
        v : float, optional
            The second parameter.
            The parameter is optional, because the frame is the same everywhere.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The frame.

        """
        return self.frame
