from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Plane
from .surface import Surface


class PlanarSurface(Surface):
    """A planar surface is defined by a local coordinate system and a size.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the surface.
        Default is ``None``, in which case the world coordinate system is used.
    xsize : float, optional
        The size of the surface in the local X-direction.
    ysize : float, optional
        The size of the surface in the local Y-direction.

    Attributes
    ----------

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "xsize": {"type": "number", "minimum": 0},
            "ysize": {"type": "number", "minimum": 0},
            "frame": Frame.JSONSCHEMA,
        },
        "required": ["xsize", "ysize", "frame"],
    }

    def __init__(self, xsize=1.0, ysize=1.0, frame=None):
        super(PlanarSurface, self).__init__(frame=frame)
        self._xsize = None
        self._ysize = None
        self.xsize = xsize
        self.ysize = ysize

    def __repr__(self):
        return "PlanarSurface(xsize={0!r}, ysize={1!r}, frame={2!r})".format(self.xsize, self.ysize, self.frame)

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_xsize = other.xsize
            other_ysize = other.ysize
        except Exception:
            return False
        return self.xsize == other_xsize and self.ysize == other_ysize and self.frame == other_frame

    @property
    def data(self):
        return {"xsize": self.xsize, "ysize": self.ysize, "frame": self.frame}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.xsize = data["xsize"]
        self.ysize = data["ysize"]

    @property
    def xsize(self):
        if not self._xsize:
            raise ValueError("The size of the surface in the local X-direction is not set.")
        return self._xsize

    @xsize.setter
    def xsize(self, xsize):
        if xsize <= 0:
            raise ValueError("The size of the surface in the local X-direction should be larger than zero.")
        self._xsize = float(xsize)

    @property
    def ysize(self):
        if not self._ysize:
            raise ValueError("The size of the surface in the local Y-direction is not set.")
        return self._ysize

    @ysize.setter
    def ysize(self, ysize):
        if ysize <= 0:
            raise ValueError("The size of the surface in the local Y-direction should be larger than zero.")
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

    def point_at(self, u, v):
        """Construct a point on the planar surface.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.

        Returns
        -------
        :class:`compas.geometry.Point`
            A point on the sphere.

        """
        return self.frame.point + self.frame.xaxis * u + self.frame.yaxis * v

    def normal_at(self, u=None, v=None):
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
        return self.frame.zaxis

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
