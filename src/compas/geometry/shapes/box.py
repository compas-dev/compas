from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.geometry import transform_points
from compas.geometry import Transformation
from compas.geometry import Frame
from compas.geometry import Vector

from ._shape import Shape


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

    def __init__(self, frame, xsize, ysize, zsize):
        super(Box, self).__init__()
        self._frame = None
        self._xsize = None
        self._ysize = None
        self._zsize = None
        self.frame = frame
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize

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
    def points(self):
        return self.vertices

    @property
    def vertices(self):
        """list of point: The XYZ coordinates of the vertices of the box."""
        point = self.frame.point
        xaxis = self.frame.xaxis
        yaxis = self.frame.yaxis
        zaxis = self.frame.zaxis
        width, depth, height = self.xsize, self.ysize, self.zsize

        a = point + (xaxis * (-0.5 * width) + yaxis * (-0.5 * depth) + zaxis * (-0.5 * height))
        b = point + (xaxis * (-0.5 * width) + yaxis * (+0.5 * depth) + zaxis * (-0.5 * height))
        c = point + (xaxis * (+0.5 * width) + yaxis * (+0.5 * depth) + zaxis * (-0.5 * height))
        d = point + (xaxis * (+0.5 * width) + yaxis * (-0.5 * depth) + zaxis * (-0.5 * height))

        e = a + zaxis * height
        f = d + zaxis * height
        g = c + zaxis * height
        h = b + zaxis * height

        return [a, b, c, d, e, f, g, h]

    @property
    def faces(self):
        """list of list: The faces of the box defined as lists of vertex indices."""
        return [self.bottom,
                self.front,
                self.right,
                self.back,
                self.left,
                self.top]

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
    def edges(self):
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        edges += [(4, 5), (5, 6), (6, 7), (7, 4)]
        edges += [(0, 4), (1, 7), (2, 6), (3, 5)]
        return edges

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Box({0}, {1}, {2}, {3})'.format(self.frame, self.xsize, self.ysize, self.zsize)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.xsize
        elif key == 2:
            return self.ysize
        elif key == 3:
            return self.zsize
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.xsize = value
        elif key == 2:
            self.ysize = value
        elif key == 3:
            self.zsize = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.xsize, self.ysize, self.zsize])

    # ==========================================================================
    # constructors
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
        return cls(Frame.from_data(data['frame']), data['xsize'], data['ysize'], data['zsize'])

    @classmethod
    def from_width_height_depth(cls, width, height, depth):
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
        Box
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
        xaxis = Vector.from_start_end(a, b)
        yaxis = Vector.from_start_end(a, d)
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
        if height == 0:
            raise Exception('The box should have a height.')

        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        if z1 != z2:
            raise Exception('Corners should be in the same horizontal plane.')

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        width = xaxis.length
        depth = yaxis.length
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), z1 + 0.5 * height]
        frame = Frame(point, xaxis, yaxis)

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
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), 0.5 * (z1 + z2)]
        frame = Frame(point, xaxis, yaxis)

        return cls(frame, width, depth, height)

    # ==========================================================================
    # methods
    # ==========================================================================

    def contains(self, point):
        """Verify if the box contains a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point` or (float, float, float)

        Returns
        -------
        bool
        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        point = transform_points([point], T)[0]
        if -0.5 * self.xsize < point[0] < + 0.5 * self.xsize:
            if -0.5 * self.ysize < point[1] < +0.5 * self.ysize:
                if -0.5 * self.zsize < point[2] < +0.5 * self.zsize:
                    return True
        return False

    def to_vertices_and_faces(self):
        """Returns a list of vertices and faces.

        Returns
        -------
        (vertices, faces)
            A list of vertex locations and a list of faces,
            with each face defined as a list of indices into the list of vertices.
        """
        return self.vertices, self.faces

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


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    import doctest

    from compas.geometry import Transformation  # noqa : F401

    doctest.testmod(globs=globals())
