class Ear(object):
    """Represents an Ear of a polygon. An Ear is a triangle formed by three consecutive vertices of the polygon.

    Parameters
    ----------
    points : list
        List of points representing the polygon.
    indexes : list
        List of indices of the points representing the polygon.
    ind : int
        Index of the vertex of the Ear triangle.

    Attributes
    ----------
    index : int
        Index of the vertex of the Ear triangle.
    coords : list
        Coordinates of the vertex of the Ear triangle.
    next : int
        Index of the next vertex of the Ear triangle.
    prev : int
        Index of the previous vertex of the Ear triangle.
    neighbour_coords : list
        Coordinates of the next and previous vertices of the Ear triangle.

    """

    def __init__(self, points, indexes, ind):
        self.index = ind
        self.coords = points[ind]
        length = len(indexes)
        index_in_indexes_arr = indexes.index(ind)
        self.next = indexes[(index_in_indexes_arr + 1) % length]
        if index_in_indexes_arr == 0:
            self.prev = indexes[length - 1]
        else:
            self.prev = indexes[index_in_indexes_arr - 1]
        self.neighbour_coords = [points[self.prev], points[self.next]]

    def is_inside(self, point):
        """Check if a given point is inside the triangle formed by the Ear.

        Returns
        -------
        bool
            True, if the point is inside the triangle, False otherwise.

        """
        p1 = self.coords
        p2 = self.neighbour_coords[0]
        p3 = self.neighbour_coords[1]
        p0 = point

        d = [
            (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p2[0] - p1[0]) * (p1[1] - p0[1]),
            (p2[0] - p0[0]) * (p3[1] - p2[1]) - (p3[0] - p2[0]) * (p2[1] - p0[1]),
            (p3[0] - p0[0]) * (p1[1] - p3[1]) - (p1[0] - p3[0]) * (p3[1] - p0[1]),
        ]

        if d[0] * d[1] >= 0 and d[2] * d[1] >= 0 and d[0] * d[2] >= 0:
            return True
        return False

    def is_ear_point(self, p):
        """Check if a given point is one of the vertices of the Ear triangle.

        Returns
        -------
        bool
            True, if the point is a vertex of the Ear triangle, False otherwise.

        """
        if p == self.coords or p in self.neighbour_coords:
            return True
        return False

    def validate(self, points, indexes, ears):
        """Validate if the Ear triangle is a valid Ear by checking its convexity and that no points lie inside.

        Returns
        -------
        bool
            True if the Ear triangle is valid, False otherwise.

        """

        not_ear_points = [points[i] for i in indexes if points[i] != self.coords and points[i] not in self.neighbour_coords]
        insides = [self.is_inside(p) for p in not_ear_points]
        if self.is_convex() and True not in insides:
            for e in ears:
                if e.is_ear_point(self.coords):
                    return False
            return True
        return False

    def is_convex(self):
        """Check if the Ear triangle is convex.

        Returns
        -------
        bool
            True if the Ear triangle is convex, False otherwise.

        """
        a = self.neighbour_coords[0]
        b = self.coords
        c = self.neighbour_coords[1]
        ab = [b[0] - a[0], b[1] - a[1]]
        bc = [c[0] - b[0], c[1] - b[1]]
        if ab[0] * bc[1] - ab[1] * bc[0] <= 0:
            return False
        return True

    def get_triangle(self):
        """Get the indices of the vertices forming the Ear triangle.

        Returns
        -------
        list
            List of vertex indices forming the Ear triangle.

        """
        return [self.prev, self.index, self.next]


class Earcut(object):
    """A class for triangulating points forming a polygon using the Ear-cutting algorithm.

    Parameters
    ----------
    points : list
        List of points representing the polygon.

    Attributes
    ----------
    vertices : list
        List of points representing the polygon.
    ears : list
        List of Ear objects representing the Ears of the polygon.
    neighbours : list
        List of indices of the neighbouring vertices.
    triangles : list
        List of triangles forming the triangulation of the polygon.
    length : int
        Number of vertices of the polygon.

    """

    def __init__(self, points):
        self.vertices = points
        self.ears = []
        self.neighbours = []
        self.triangles = []
        self.length = len(points)

    def update_neighbours(self):
        """Update the list of neighboring vertices."""
        neighbours = []
        self.neighbours = neighbours

    def add_ear(self, new_ear):
        """Add a new Ear to the list of Ears and update neighboring vertices.

        Parameters
        ----------
        new_ear : Ear
            Ear object to be added to the list of Ears.

        """
        self.ears.append(new_ear)
        self.neighbours.append(new_ear.prev)
        self.neighbours.append(new_ear.next)

    def find_ears(self):
        """Find valid Ear triangles among the vertices and add them to the Ears list."""
        i = 0
        indexes = list(range(self.length))
        while True:
            if i >= self.length:
                break
            new_ear = Ear(self.vertices, indexes, i)
            if new_ear.validate(self.vertices, indexes, self.ears):
                self.add_ear(new_ear)
                indexes.remove(new_ear.index)
            i += 1

    def triangulate(self):
        """Triangulate the polygon using the Ear-cutting algorithm.

        Returns
        -------
        list[list[int]]
            List of triangles forming the triangulation of the polygon.

        Raises
        ------
        ValueError
            If no Ears were found for triangulation.
        IndexError
            If no more Ears were found for triangulation.

        """

        if self.length < 3:
            raise ValueError("Polygon must have at least 3 vertices.")
        elif self.length == 3:
            self.triangles.append([0, 1, 2])
            return self.triangles

        indexes = list(range(self.length))
        self.find_ears()

        num_of_ears = len(self.ears)

        if num_of_ears == 0:
            raise ValueError("No ears found for triangulation.")
        if num_of_ears == 1:
            self.triangles.append(self.ears[0].get_triangle())
            return

        while True:
            if len(self.ears) == 2 and len(indexes) == 4:
                self.triangles.append(self.ears[0].get_triangle())
                self.triangles.append(self.ears[1].get_triangle())
                break

            if len(self.ears) == 0:
                raise IndexError("Unable to find more Ears for triangulation.")
            current = self.ears.pop(0)

            indexes.remove(current.index)
            self.neighbours.remove(current.prev)
            self.neighbours.remove(current.next)

            self.triangles.append(current.get_triangle())

            # Check if prev and next vertices form new ears
            prev_ear_new = Ear(self.vertices, indexes, current.prev)
            next_ear_new = Ear(self.vertices, indexes, current.next)
            if prev_ear_new.validate(self.vertices, indexes, self.ears) and prev_ear_new.index not in self.neighbours:
                self.add_ear(prev_ear_new)
                continue
            if next_ear_new.validate(self.vertices, indexes, self.ears) and next_ear_new.index not in self.neighbours:
                self.add_ear(next_ear_new)
                continue

        return self.triangles


def earclip_polygon(polygon):
    """Triangulate a polygon using the ear clipping method.
    The polygon is assumed to be planar and non-self-intersecting and position on XY plane.
    The winding direction is checked. If the polygon is not oriented counter-clockwise, it is reversed.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A polygon defined by a sequence of points.

    Returns
    -------
    list[[int, int, int]]
        A list of triangles referencing the points of the original polygon.

    Raises
    ------
    ValueError
        If no ears were found for triangulation.
    IndexError
        If no more ears were found for triangulation.

    """
    from compas.geometry import Frame  # Avoid circular import.
    from compas.geometry import Plane  # Avoid circular import.
    from compas.geometry import Transformation  # Avoid circular import.

    frame = Frame.from_plane(Plane(polygon.points[0], polygon.normal))
    xform = Transformation.from_frame_to_frame(frame, Frame.worldXY())
    points = [point.transformed(xform) for point in polygon.points]

    # Check polygon winding by signed area of all current and next points pairs.
    sum_val = 0.0
    for p0, p1 in zip(points, points[1:] + [points[0]]):
        sum_val += (p1[0] - p0[0]) * (p1[1] + p0[1])

    if sum_val > 0.0:
        points.reverse()

    # Run the Earcut algorithm.
    ear_cut = Earcut(points)
    triangles = ear_cut.triangulate()

    # Reverse the triangles to match the original polygon winding.
    if sum_val > 0.0:
        n = len(points) - 1
        for i in range(len(triangles)):
            triangles[i] = [abs(triangles[i][j % 3] - n) for j in range(3)]
    return triangles
