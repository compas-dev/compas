from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

from ._core.distance import distance_point_point_sqrd

Node = collections.namedtuple("Node", "point axis label left right")


class KDTree(object):
    """A tree for nearest neighbor search in a k-dimensional space.

    Parameters
    ----------
    objects : sequence[[float, float, float] | :class:`compas.geometry.Point`], optional
        A list of objects to populate the tree with.
        If objects are provided, the tree is built automatically.
        Otherwise, use :meth:`build`.

    Attributes
    ----------
    root : Node
        The root node of the built tree.
        This is the median with respect to the different dimensions of the tree.

    Notes
    -----
    For more info, see [1]_ and [2]_.

    References
    ----------
    .. [1] Wikipedia. *k-d tree*.
           Available at: https://en.wikipedia.org/wiki/K-d_tree.
    .. [2] Dell'Amico, M. *KD-Tree for nearest neighbor search in a K-dimensional space (Python recipe)*.
           Available at: http://code.activestate.com/recipes/577497-kd-tree-for-nearest-neighbor-search-in-a-k-dimensional-space/.

    Examples
    --------
    >>>

    """

    def __init__(self, objects=None):
        self.root = None
        if objects:
            self.root = self.build([(o, i) for i, o in enumerate(objects)])

    def build(self, objects, axis=0):
        """Populate a kd-tree with given objects.

        Parameters
        ----------
        objects : sequence[tuple[[float, float, float] | :class:`compas.geometry.Point`, int or str]]
            The tree objects as a sequence of point-label tuples.
        axis : int, optional
            The axis along which to build.

        Returns
        -------
        Node or None
            The root node, or None if the sequence of objects is empty.

        """
        if not objects:
            return

        objects.sort(key=lambda o: o[0][axis])
        median_idx = len(objects) // 2
        median_point, median_label = objects[median_idx]
        next_axis = (axis + 1) % 3

        return Node(
            median_point,
            axis,
            median_label,
            self.build(objects[:median_idx], next_axis),
            self.build(objects[median_idx + 1 :], next_axis),
        )

    def nearest_neighbor(self, point, exclude=None):
        """Find the nearest neighbor to a given point,
        excluding neighbors that have already been found.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            XYZ coordinates of the base point.
        exclude : sequence[int or str], optional
            A sequence of point identified by their label to exclude from the search.

        Returns
        -------
        [[float, float, float], int or str, float]
            XYZ coordinates of the nearest neighbor.
            Label of the nearest neighbor.
            Distance to the base point.

        """

        def search(node):
            if node is None:
                return

            d2 = distance_point_point_sqrd(point, node.point)
            if d2 < best[2]:
                if node.label not in exclude:
                    best[:] = node.point, node.label, d2

            d = point[node.axis] - node.point[node.axis]
            if d <= 0:
                close, far = node.left, node.right
            else:
                close, far = node.right, node.left

            search(close)
            if d**2 < best[2]:
                search(far)

        exclude = set(exclude or [])
        best = [None, None, float("inf")]
        search(self.root)
        best[2] **= 0.5
        return best

    def nearest_neighbors(self, point, number, distance_sort=False):
        """Find the N nearest neighbors to a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            XYZ coordinates of the base point.
        number : int
            The number of nearest neighbors.
        distance_sort : bool, optional
            Sort the nearest neighbors by distance to the base point.

        Returns
        -------
        list[[[float, float, float], int or str, float]]
            A list of N nearest neighbors.

        """
        nnbrs = []
        exclude = set()
        for i in range(number):
            nnbr = self.nearest_neighbor(point, exclude)
            nnbrs.append(nnbr)
            exclude.add(nnbr[1])
        if distance_sort:
            return sorted(nnbrs, key=lambda nnbr: nnbr[2])
        return nnbrs
