from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry._primitives import Vector
from compas.geometry._primitives import Frame
from compas.geometry import subtract_vectors


__all__ = ['Box']


class Box(object):
    """A box is a three-dimensional geometric shape with 8 vertices, 12 edges
        and 6 faces.

    The edges of a box meet at its vertices at 90 degree angles.
    The faces of a box are planar.
    Faces which do not share an edge are parallel.

    Parameters
    ----------
    vertices : list of point
        The XYZ coordinates of the vertices of the box.
    faces : list of list
        The faces of the box defined as lists of vertex indices.

    Examples
    --------
    .. code-block:: python

        pass

    """

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
        return self.xsize

    @property
    def depth(self):
        return self.ysize

    @property
    def height(self):
        return self.zsize

    @property
    def vertices(self):
        point = self.frame.point
        xaxis = self.frame.xaxis
        yaxis = self.frame.yaxis
        zaxis = self.frame.zaxis
        width, depth, height = self.xsize, self.ysize, self.zsize

        a = point
        b = point + yaxis * depth
        c = point + xaxis * width + yaxis * depth
        d = point + xaxis * width

        e = a + zaxis * height
        f = d + zaxis * height
        g = c + zaxis * height
        h = b + zaxis * height

        return [list(pt) for pt in [a, b, c, d, e, f, g, h]]

    @property
    def faces(self):
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
        .. code-block:: python

            box = Box.from_width_height_depth(1.0, 2.0, 3.0)

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
        a = bbox[0]
        b = bbox[1]
        d = bbox[3]
        e = bbox[4]
        xaxis = Vector(*subtract_vectors(d, a))
        yaxis = Vector(*subtract_vectors(b, a))
        zaxis = Vector(*subtract_vectors(e, a))
        xsize = xaxis.length
        ysize = yaxis.length
        zsize = zaxis.length
        frame = Frame(a, xaxis, yaxis)
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
        .. code-block:: python

            box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)

        """
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
        .. code-block:: python

            box = Box.from_diagonal([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])

        """
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
        return cls(frame, width, depth, height)


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    from compas.datastructures import Mesh

    box = Box.from_diagonal([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])
    box = Box.from_corner_corner_height([0., 0., 0.], [1., 1., 0.], 4.0)
    box = Box.from_width_height_depth(5, 4, 6)
    print(box.vertices)

    mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

    print(mesh)
