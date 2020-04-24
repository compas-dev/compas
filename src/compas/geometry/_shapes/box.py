from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.geometry import Frame
from compas.geometry import Vector

from compas.geometry._shapes import Shape


__all__ = ['Box']


class Box(Shape):
    """A box is defined by a frame and its dimensions along the frame's x-, y- and z-axes.

    The center of the box is positioned at the origin of the
    coordinate system defined by the frame. The box is axis-aligned to the frame.

    A box is a three-dimensional geometric shape with 8 vertices, 12 edges and 6
    faces. The edges of a box meet at its vertices at 90 degree angles. The
    faces of a box are planar. Faces which do not share an edge are parallel.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The frame of the box.
    xsize : float
        The size of the box in the box frame's x direction.
    ysize : float
        The size of the box in the box frame's y direction.
    zsize : float
        The size of the box in the box frame's z direction.

    Attributes
    ----------
    frame : compas.geometry.Frame
        The local coordinate system of the box.
    xsize : float
        The size of the box in the local X direction.
    ysize : float
        The size of the box in the local Y direction.
    zsize : float
        The size of the box in the local Z direction.
    width (read-only) : float
        Alias for ``xsize``.
    depth (read-only) : float
        Alias for ``ysize``.
    height (read-only) : float
        Alias for ``zsize``.
    diagonal (read-only) : tuple of compas.geometry.Point
        The start and end point of the main diagonal of the box.
    dimensions (read-only) : list of float
        List of sizes in local coordinate directions.
    area (read-only) : float
        The surface area of the box.
    volume (read-only) : float
        The volume of the box.
    vertices (read-only) : list of list
        The XYZ coordinates of the corners of the box.
        With respect to the local Z axis, the vertices of the bottom
        face are listed first in clockwise direction, starting at the bottom left corner.
        The vertices of the top face are listed in counterclockwise direction.
    faces (read-only) : list of list
        The vertices of the faces of the box.
        The cycle directions of the faces are such that face normals point outwards.

    Examples
    --------
    >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)

    """

    __module__ = "compas.geometry"

    def __init__(self, frame, xsize, ysize, zsize):
        self._frame = None
        self._xsize = None
        self._ysize = None
        self._zsize = None
        self.frame = frame
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def frame(self):
        """Frame: The box's frame."""
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = Frame(frame[0], frame[1], frame[2])

    @property
    def xsize(self):
        """float: The size of the box in the box frame's x direction."""
        return self._xsize

    @xsize.setter
    def xsize(self, xsize):
        self._xsize = float(xsize)

    @property
    def ysize(self):
        """float: The size of the box in the box frame's y direction."""
        return self._ysize

    @ysize.setter
    def ysize(self, ysize):
        self._ysize = float(ysize)

    @property
    def zsize(self):
        """float: The size of the box in the box frame's z direction."""
        return self._zsize

    @zsize.setter
    def zsize(self, zsize):
        self._zsize = float(zsize)

    @property
    def width(self):
        """float: The width of the box in x direction."""
        return self.xsize

    @property
    def depth(self):
        """float: The depth of the box in y direction."""
        return self.ysize

    @property
    def height(self):
        """float: The height of the box in z direction."""
        return self.zsize

    @property
    def diagonal(self):
        vertices = self.vertices
        return vertices[0], vertices[-2]

    @property
    def dimensions(self):
        return [self.xsize, self.ysize, self.zsize]

    @property
    def area(self):
        """float: The surface area of the box."""
        return 2 * self.xsize * self.ysize + 2 * self.ysize * self.zsize + 2 * self.zsize * self.xsize

    @property
    def volume(self):
        """float: The volume of the box."""
        return self.xsize * self.ysize * self.zsize

    @property
    def vertices(self):
        """list of point: The XYZ coordinates of the vertices of the box."""
        point = self.frame.point
        xaxis = self.frame.xaxis
        yaxis = self.frame.yaxis
        zaxis = self.frame.zaxis
        width, depth, height = self.xsize, self.ysize, self.zsize

        a = point - xaxis * 0.5 * width - yaxis * 0.5 * depth - zaxis * 0.5 * height
        b = point - xaxis * 0.5 * width + yaxis * 0.5 * depth - zaxis * 0.5 * height
        c = point + xaxis * 0.5 * width + yaxis * 0.5 * depth - zaxis * 0.5 * height
        d = point + xaxis * 0.5 * width - yaxis * 0.5 * depth - zaxis * 0.5 * height

        e = a + zaxis * height
        f = d + zaxis * height
        g = c + zaxis * height
        h = b + zaxis * height

        return [list(pt) for pt in [a, b, c, d, e, f, g, h]]

    @property
    def faces(self):
        """list of list: The faces of the box defined as lists of vertex indices."""
        return [[0, 1, 2, 3],
                [0, 3, 5, 4],
                [3, 2, 6, 5],
                [2, 1, 7, 6],
                [1, 0, 4, 7],
                [4, 5, 6, 7]]

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a box from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Box
            The constructed box.

        Examples
        --------
        >>> data = {'frame': Frame.worldXY().data, 'xsize': 1.0, 'ysize': 1.0, 'zsize': 1.0}
        >>> box = Box.from_data(data)
        """
        box = cls(Frame.worldXY(), 1, 1, 1)
        box.data = data
        return box

    @classmethod
    def from_width_height_depth(cls, width, height, depth):
        """Construct a box from its width, height and depth.

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
        Box
            The resulting box.

        Notes
        -----
        The bottom left corner of the box is positioned at the origin of the
        coordinates system. The box is axis-aligned.

        Examples
        --------
        >>> box = Box.from_width_height_depth(1.0, 2.0, 3.0)
        """
        width = float(width)
        height = float(height)
        depth = float(depth)

        if width == 0.0:
            raise Exception('Width cannot be zero.')

        if height == 0.0:
            raise Exception('Height cannot be zero.')

        if depth == 0.0:
            raise Exception('Depth cannot be zero.')

        return cls(Frame.worldXY(), width, depth, height)

    @classmethod
    def from_bounding_box(cls, bbox):
        """Construct a box from the result of a bounding box calculation.

        Parameters
        ----------
        bbox : list
            A list of 8 point locations, representing the corners of the bounding box.
            Positions 0, 1, 2, 3 are the bottom corners.
            Positions 4, 5, 6, 7 are the top corners.
            Both the top and bottom face are oriented in CCW direction, starting at the bottom, left-most point.

        Returns
        -------
        Box
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
        xaxis = Vector.from_start_end(a, d)
        yaxis = Vector.from_start_end(a, b)
        zaxis = Vector.from_start_end(a, e)
        xsize = xaxis.length
        ysize = yaxis.length
        zsize = zaxis.length
        frame = Frame(centroid_points(bbox), xaxis, yaxis)
        return cls(frame, xsize, ysize, zsize)

    @classmethod
    def from_corner_corner_height(cls, corner1, corner2, height):
        """Construct a box from the opposite corners of its base and its height.

        Parameters
        ----------
        corner1 : point
            The XYZ coordinates of the bottom left corner of the base of the box.
        corner2 : point
            The XYZ coordinates of the top right corner of the base of the box.
        height : float
            The height of the box.

        Returns
        -------
        Box
            The resulting box.

        Examples
        --------
        >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)

        """
        # this should put the frame at the centroid of the box
        # not at the bottom left corner
        if height == 0:
            raise Exception('The box should have a height.')

        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        width = xaxis.length
        depth = yaxis.length

        if z1 != z2:
            raise Exception('Corners should be in the same horizontal plane.')

        frame = Frame(corner1, xaxis, yaxis)
        frame.point += frame.xaxis * 0.5 * width + frame.yaxis * 0.5 * depth + frame.zaxis * 0.5 * height
        return cls(frame, width, depth, height)

    @classmethod
    def from_diagonal(cls, diagonal):
        """Construct a box from its main diagonal.

        Parameters
        ----------
        diagonal : segment
            The diagonal of the box, represented by a pair of points in space.

        Returns
        -------
        Box
            The resulting box.

        Examples
        --------
        >>> diagonal = [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
        >>> box = Box.from_diagonal(diagonal)

        """
        # this should put the frame at the centroid of the box
        # not at the bottom left corner
        d1, d2 = diagonal

        x1, y1, z1 = d1
        x2, y2, z2 = d2

        if z1 == z2:
            raise Exception('The box has no height.')

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        zaxis = Vector(0, 0,  z2 - z1)
        width = xaxis.length
        depth = yaxis.length
        height = zaxis.length

        frame = Frame(d1, xaxis, yaxis)
        frame.point += frame.xaxis * 0.5 * width + frame.yaxis * 0.5 * depth + frame.zaxis * 0.5 * height
        return cls(frame, width, depth, height)

    @property
    def data(self):
        """Returns the data dictionary that represents the box.

        Returns
        -------
        dict
            The box data.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> box = Box(frame, 1.0, 2.0, 3.0)
        >>> bdict = {'frame': frame.data, 'xsize': 1.0, 'ysize': 2.0, 'zsize': 3.0}
        >>> bdict == box.to_data()
        True

        """
        return {'frame': self.frame.data,
                'xsize': self.xsize,
                'ysize': self.ysize,
                'zsize': self.zsize}

    @data.setter
    def data(self, data):
        self.frame = Frame.from_data(data['frame'])
        self.xsize = data['xsize']
        self.ysize = data['ysize']
        self.zsize = data['zsize']

    def to_data(self):
        """Returns the data dictionary that represents the box.

        Returns
        -------
        dict
            The box data.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> box = Box(frame, 1.0, 2.0, 3.0)
        >>> bdict = {'frame': frame.data, 'xsize': 1.0, 'ysize': 2.0, 'zsize': 3.0}
        >>> bdict == box.to_data()
        True
        """
        return self.data

    def to_vertices_and_faces(self, **kwargs):
        """Returns a list of vertices and faces"""
        return self.vertices, self.faces

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Box({0}, {1}, {2}, {3})'.format(self.frame, self.xsize, self.ysize, self.zsize)

    def __len__(self):
        return 4

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.point
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.point, self.radius])

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Makes a copy of this ``Box``.

        Returns
        -------
        Box
            The copy.

        Examples
        --------
        >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
        >>> box_copy = box.copy()

        """
        cls = type(self)
        return cls(self.frame.copy(), self.xsize, self.ysize, self.zsize)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the box.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Box.

        Examples
        --------
        >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> box.transform(T)

        """
        self.frame.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current box.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the box.

        Returns
        -------
        :class:`Box`
            The transformed box.

        Examples
        --------
        >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> box_transformed = box.transformed(T)

        """
        box = self.copy()
        box.transform(transformation)
        return box


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    import doctest

    from compas.geometry import Transformation  # noqa : F401

    doctest.testmod(globs=globals())
