from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.geometry import centroid_points
from compas.geometry import transform_points
from compas.tolerance import TOL

from ..geometry import reset_computed
from .shape import Shape


class Box(Shape):
    """A box is defined by a frame and its dimensions along the frame's x-, y- and z-axes.

    The center of the box is positioned at the origin of the
    coordinate system defined by the frame. The box is axis-aligned to the frame.

    A box is a three-dimensional geometric shape with 8 vertices, 12 edges and 6
    faces. The edges of a box meet at its vertices at 90 degree angles. The
    faces of a box are planar. Faces which do not share an edge are parallel.

    Parameters
    ----------
    xsize : float
        The size of the box in the box frame's x direction.
    ysize : float, optional
        The size of the box in the box frame's y direction.
        Defaults to the value of ``xsize``.
    zsize : float, optional
        The size of the box in the box frame's z direction.
        Defaults to the value of ``xsize``.
    frame : :class:`compas.geometry.Frame`, optional
        The frame of the box.
        Defaults to ``Frame.worldXY()``.
    name : str, optional
        The name of the shape.

    Attributes
    ----------
    area : float, read-only
        The surface area of the box.
    depth : float, read-only
        The depth of the box in Y direction.
    diagonal : :class:`compas.geometry.Line`, read-only
        Diagonal of the box.
    dimensions : list[float], read-only
        The dimensions of the box in the local frame.
    frame : :class:`compas.geometry.Frame`
        The box's frame.
    height : float, read-only
        The height of the box in Z direction.
    points : list[:class:`compas.geometry.Point`]
        The corner points of the box.
    volume : float, read-only
        The volume of the box.
    width : float, read-only
        The width of the box in X direction.
    xmax : float, read-only
        Maximum value along local X axis.
    xmin : float, read-only
        Minimum value along local X axis.
    xsize : float
        The size of the box in the box frame's x direction.
    ymax : float, read-only
        Maximum value along local Y axis.
    ymin : float, read-only
        Minimum value along local Y axis.
    ysize : float
        The size of the box in the box frame's y direction.
    zmax : float, read-only
        Maximum value along local Z axis.
    zmin : float, read-only
        Minimum value along local Z axis.
    zsize : float
        The size of the box in the box frame's z direction.

    Examples
    --------
    >>> box = Box(1)
    >>> box.xsize
    1.0
    >>> box.ysize
    1.0
    >>> box.zsize
    1.0
    >>> box.volume
    1.0
    >>> box.area
    6.0

    >>> box = Box(1, 2, 3)
    >>> box.xsize
    1.0
    >>> box.ysize
    2.0
    >>> box.zsize
    3.0
    >>> box.volume
    6.0
    >>> box.area
    22.0

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "xsize": {"type": "number", "minimum": 0},
            "ysize": {"type": "number", "minimum": 0},
            "zsize": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "additionalProperties": False,
        "minProperties": 4,
    }

    @property
    def __data__(self):
        return {
            "xsize": self.xsize,
            "ysize": self.ysize,
            "zsize": self.zsize,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            xsize=data["xsize"],
            ysize=data["ysize"],
            zsize=data["zsize"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, xsize=1.0, ysize=None, zsize=None, frame=None, name=None):
        super(Box, self).__init__(frame=frame, name=name)
        self._xsize = None
        self._ysize = None
        self._zsize = None
        self.xsize = xsize
        self.ysize = xsize if ysize is None else ysize
        self.zsize = xsize if zsize is None else zsize
        self._points = None

    def __repr__(self):
        return "{0}(xsize={1}, ysize={2}, zsize={3}, frame={4!r})".format(
            type(self).__name__,
            self.xsize,
            self.ysize,
            self.zsize,
            self.frame,
        )

    def _reset_computed(self):
        super(Box, self)._reset_computed()
        self._points = None

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def xsize(self):
        if self._xsize is None:
            raise ValueError("The size of the box along the local X axis is not set.")
        return self._xsize

    @xsize.setter
    @reset_computed
    def xsize(self, xsize):
        if xsize < 0:
            raise ValueError("The minimum value of the size of the box along the local X axis is zero.")
        self._xsize = float(xsize)

    @property
    def ysize(self):
        if self._ysize is None:
            raise ValueError("The size of the box along the local Y axis is not set.")
        return self._ysize

    @ysize.setter
    @reset_computed
    def ysize(self, ysize):
        if ysize < 0:
            raise ValueError("The minimum value of the size of the box along the local Y axis is zero.")
        self._ysize = float(ysize)

    @property
    def zsize(self):
        if self._zsize is None:
            raise ValueError("The size of the box along the local Z axis is not set.")
        return self._zsize

    @zsize.setter
    @reset_computed
    def zsize(self, zsize):
        if zsize < 0:
            raise ValueError("The minimum value of the size of the box along the local Z axis is zero.")
        self._zsize = float(zsize)

    @property
    def xmin(self):
        return self.frame.point.x - 0.5 * self.xsize

    @property
    def xmax(self):
        return self.frame.point.x + 0.5 * self.xsize

    @property
    def ymin(self):
        return self.frame.point.y - 0.5 * self.ysize

    @property
    def ymax(self):
        return self.frame.point.y + 0.5 * self.ysize

    @property
    def zmin(self):
        return self.frame.point.z - 0.5 * self.zsize

    @property
    def zmax(self):
        return self.frame.point.z + 0.5 * self.zsize

    @property
    def width(self):
        return self.xsize

    @property
    def depth(self):
        return self.ysize

    @property
    def height(self):
        return self.zsize

    @property
    def diagonal(self):
        a = self.frame.point + self.frame.xaxis * -0.5 * self.xsize + self.frame.yaxis * -0.5 * self.ysize + self.frame.zaxis * -0.5 * self.zsize
        b = self.frame.point + self.frame.xaxis * 0.5 * self.xsize + self.frame.yaxis * 0.5 * self.ysize + self.frame.zaxis * 0.5 * self.zsize
        return Line(a, b)

    @property
    def dimensions(self):
        return [self.xsize, self.ysize, self.zsize]

    @property
    def area(self):
        return 2 * self.xsize * self.ysize + 2 * self.ysize * self.zsize + 2 * self.zsize * self.xsize

    @property
    def volume(self):
        return self.xsize * self.ysize * self.zsize

    @property
    def bottom(self):
        return [0, 1, 2, 3]

    @property
    def front(self):
        return [0, 3, 5, 4]

    @property
    def right(self):
        return [3, 2, 6, 5]

    @property
    def back(self):
        return [2, 1, 7, 6]

    @property
    def left(self):
        return [1, 0, 4, 7]

    @property
    def top(self):
        return [4, 5, 6, 7]

    @property
    def points(self):
        if not self._points:
            self._points = self.compute_points()
        return self._points

    def compute_points(self):
        """Compute the points at the corners of the box.

        Returns
        -------
        list[:class:`compas.geometry.Point`]

        """
        point = self.frame.point
        xaxis = self.frame.xaxis
        yaxis = self.frame.yaxis
        zaxis = self.frame.zaxis

        dx = 0.5 * self.xsize
        dy = 0.5 * self.ysize
        dz = 0.5 * self.zsize

        a = point + xaxis * -dx + yaxis * -dy + zaxis * -dz
        b = point + xaxis * -dx + yaxis * +dy + zaxis * -dz
        c = point + xaxis * +dx + yaxis * +dy + zaxis * -dz
        d = point + xaxis * +dx + yaxis * -dy + zaxis * -dz
        e = a + zaxis * self.zsize
        f = d + zaxis * self.zsize
        g = c + zaxis * self.zsize
        h = b + zaxis * self.zsize

        return [a, b, c, d, e, f, g, h]

    def compute_aabb(self):
        """Compute the axis-aligned bounding box of the box.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        x, y, z = zip(*self.points)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        zmin = min(z)
        zmax = max(z)
        xsize = xmax - xmin
        ysize = ymax - ymin
        zsize = zmax - zmin
        x = xmin + 0.5 * xsize
        y = ymin + 0.5 * ysize
        z = zmin + 0.5 * zsize
        return Box(xsize, ysize, zsize, point=[x, y, z])

    def compute_obb(self):
        """Compute the oriented bounding box of the box.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        return self

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_width_height_depth(cls, width, height, depth):  # type: (...) -> Box
        """Construct a box from its width, height and depth.

        Note that width is along the X-axis, height along Z-axis, and depth along the Y-axis.

        Parameters
        ----------
        width : float
            Width of the box.
        height : float
            Height of the box.
        depth : float
            Depth of the box.

        Returns
        -------
        :class:`compas.geometry.Box`
            The resulting box.

        Notes
        -----
        The box is axis-aligned to the world coordinate system and centered at the origin.

        Examples
        --------
        >>> box = Box.from_width_height_depth(1.0, 2.0, 3.0)

        """
        width = float(width)
        height = float(height)
        depth = float(depth)

        return cls(width, depth, height)

    @classmethod
    def from_bounding_box(cls, bbox):  # type: (...) -> Box
        """Construct a box from the result of a bounding box calculation.

        Parameters
        ----------
        bbox : list[[float, float, float] | :class:`compas.geometry.Point`]
            A list of 8 point locations, representing the corners of the bounding box.
            Positions 0, 1, 2, 3 are the bottom corners.
            Positions 4, 5, 6, 7 are the top corners.
            Both the top and bottom face are oriented in CCW direction, starting at the bottom, left-most point.

        Returns
        -------
        :class:`compas.geometry.Box`
            The box shape.

        Examples
        --------
        >>> from compas.geometry import bounding_box
        >>> bbox = bounding_box([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        >>> box = Box.from_bounding_box(bbox)
        >>> box.width
        1.0
        >>> box.height
        1.0
        >>> box.depth
        1.0

        """
        a = bbox[0]
        b = bbox[1]
        d = bbox[3]
        e = bbox[4]
        xaxis = Vector.from_start_end(a, b)
        yaxis = Vector.from_start_end(a, d)
        zaxis = Vector.from_start_end(a, e)
        xsize = xaxis.length
        ysize = yaxis.length
        zsize = zaxis.length
        frame = Frame(centroid_points(bbox), xaxis, yaxis)
        return cls(xsize=xsize, ysize=ysize, zsize=zsize, frame=frame)

    @classmethod
    def from_corner_corner_height(cls, corner1, corner2, height):  # type: (...) -> Box
        """Construct a box from the opposite corners of its base and its height.

        Parameters
        ----------
        corner1 : [float, float, float] | :class:`compas.geometry.Point`
            The XYZ coordinates of the bottom left corner of the base of the box.
        corner2 : [float, float, float] | :class:`compas.geometry.Point`
            The XYZ coordinates of the top right corner of the base of the box.
        height : float
            The height of the box.

        Returns
        -------
        :class:`compas.geometry.Box`
            The resulting box.

        Examples
        --------
        >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)

        """
        if height == 0:
            raise Exception("The box should have a height.")

        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        if z1 != z2:
            raise Exception("Corners should be in the same horizontal plane.")

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        width = xaxis.length
        depth = yaxis.length
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), z1 + 0.5 * height]
        frame = Frame(point, xaxis, yaxis)

        return cls(xsize=width, ysize=depth, zsize=height, frame=frame)

    @classmethod
    def from_diagonal(cls, diagonal):  # type: (...) -> Box
        """Construct a box from its main diagonal.

        Parameters
        ----------
        diagonal : [point, point] | :class:`compas.geometry.Line`
            The diagonal of the box, represented by a pair of points in space.

        Returns
        -------
        :class:`compas.geometry.Box`
            The resulting box.

        Examples
        --------
        >>> diagonal = [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
        >>> box = Box.from_diagonal(diagonal)

        """
        d1, d2 = diagonal

        x1, y1, z1 = d1
        x2, y2, z2 = d2

        if z1 == z2:
            raise Exception("The box has no height.")

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        zaxis = Vector(0, 0, z2 - z1)
        width = xaxis.length
        depth = yaxis.length
        height = zaxis.length
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), 0.5 * (z1 + z2)]
        frame = Frame(point, xaxis, yaxis)

        return cls(width, depth, height, frame)

    @classmethod
    def from_points(cls, points):  # type: (...) -> Box
        """Construct a box from a set of points.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]
            A list of points.

        Returns
        -------
        :class:`compas.geometry.Box`
            The resulting box.

        """
        from compas.geometry import bounding_box

        bbox = bounding_box(points)
        return cls.from_bounding_box(bbox)

    @classmethod
    def from_corner_and_sizes(cls, corner, xsize, ysize=None, zsize=None):
        """Construct a box from the nearest, bottom left corner and the szes in X, Y, Z direction.

        Parameters
        ----------
        corner : :class:`compas.geometry.Point`
            The nearest, bottom left corner point.
        xsize : float
            The size in the X direction.
        ysize : float, optional
            The size in the Y direction.
        zsize : float, optional
            The size in the Z direction.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        ysize = ysize if ysize is not None else xsize
        zsize = zsize if zsize is not None else xsize
        box = cls(xsize, ysize, zsize, point=corner)
        box.frame.point += [0.5 * xsize, 0.5 * ysize, 0.5 * zsize]
        return box

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_vertices_and_faces(self, triangulated=False):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        triangulated: bool, optional
            If True, triangulate the faces.

        Returns
        -------
        list[list[float]], list[list[int]]
            A list of vertex locations, and a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        vertices = self.points
        _faces = [self.bottom, self.front, self.right, self.back, self.left, self.top]

        if triangulated:
            faces = []
            for a, b, c, d in _faces:
                faces.append([a, b, c])
                faces.append([a, c, d])
        else:
            faces = _faces

        return vertices, faces

    def to_mesh(self, triangulated=False):
        """Returns a mesh representation of the box.

        Parameters
        ----------
        triangulated: bool, optional
            If True, triangulate the faces.

        Returns
        -------
        :class:`compas.datastructures.Mesh`

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(triangulated=triangulated)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        return mesh

    def to_brep(self):
        """Returns a BREP representation of the box.

        Returns
        -------
        :class:`compas.brep.Brep`

        """
        from compas.geometry import Brep

        return Brep.from_box(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def scale(self, factor):
        """Scale the box.

        Parameters
        ----------
        factor : float
            The scaling factor.

        Returns
        -------
        None

        """
        self.xsize *= factor
        self.ysize *= factor
        self.zsize *= factor

    # ==========================================================================
    # Methods
    # ==========================================================================

    def corner(self, index):
        """Return one of the eight corners of the box.

        Parameters
        ----------
        index : int
            The index of the corner.

        Returns
        -------
        :class:`compas.geometry.Point`
            The corner point.

        Raises
        ------
        ValueError
            If the index is not between 0 and 7.

        """
        if index < 0 or index > 7:
            raise ValueError("Index should be between 0 and 7.")

        return self.points[index]

    def contains_point(self, point, tol=None):
        """Verify if the box contains a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point to test.
        tol : float, optional
            The tolerance for the point containment check.
            Defaults to ``compas.tolerance.Tolerance.absolute``.

        Returns
        -------
        bool

        See Also
        --------
        contains_points

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        x, y, z = transform_points([point], T)[0]

        tol = tol or TOL.absolute

        dx = 0.5 * self.xsize + tol
        if x < -dx or x > +dx:
            return False

        dy = 0.5 * self.ysize + tol
        if y < -dy or y > +dy:
            return False

        dz = 0.5 * self.zsize + tol
        if z < -dz or z > +dz:
            return False

        return True

    def contains_points(self, points, tol=None):
        """Verify if the box contains the given points.

        Parameters
        ----------
        points : list[[float, float, float]] | list[:class:`compas.geometry.Point`]
            A list of points.
        tol : float, optional
            The tolerance for the point containment check.
            Defaults to ``compas.tolerance.Tolerance.absolute``.

        Returns
        -------
        list[bool]

        See Also
        --------
        contains_point

        Examples
        --------
        >>> from compas.geometry import Point, Box
        >>> box = Box(Frame.worldXY(), 2.0, 2.0, 2.0)
        >>> points = [Point(0.0, 0.0, 0.0), Point(1.0, 1.0, 1.0)]
        >>> results = box.contains_points(points)
        >>> all(results)
        True

        """
        tol = tol or TOL.absolute

        dx = 0.5 * self.xsize + tol
        dy = 0.5 * self.ysize + tol
        dz = 0.5 * self.zsize + tol

        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        points = transform_points(points, T)
        results = [False] * len(points)

        for index, (x, y, z) in enumerate(points):
            if x < -dx or x > +dx:
                continue

            if y < -dy or y > +dy:
                continue

            if z < -dz or z > +dz:
                continue

            results[index] = True

        return results
