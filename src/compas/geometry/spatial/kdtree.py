from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import collections

from compas.geometry.distance import distance_point_point_sqrd


__all__ = [
    'KDTree'
]


Node = collections.namedtuple("Node", 'point axis label left right')


class KDTree(object):
    """A tree for nearest neighbor search in a k-dimensional space.

    Parameters
    ----------
    objects : list, optional
        A list of objects to populate the tree with.
        If objects are provided, the tree is built automatically.
        Defaults to ``None``.

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
    .. plot::
        :include-source:

        from compas.geometry import KDTree
        from compas.geometry import pointcloud_xy
        from compas.plotters import Plotter

        plotter = Plotter()

        cloud = pointcloud_xy(999, (-500, 500))
        point = cloud[0]

        tree = KDTree(cloud)

        n       = 50
        nnbrs   = []
        exclude = set()

        for i in range(n):
            nnbr = tree.nearest_neighbor(point, exclude)
            nnbrs.append(nnbr)
            exclude.add(nnbr[1])

        for nnbr in nnbrs:
            print(nnbr)

        points = []
        for index, (x, y, z) in enumerate(cloud):
            points.append({
                'pos'      : [x, y],
                'facecolor': '#000000',
                'edgecolor': '#000000',
                'radius'   : 1.0
            })
        points.append({
            'pos'      : point[0:2],
            'facecolor': '#ff0000',
            'edgecolor': '#ff0000',
            'radius'   : 5.0
        })

        lines = []
        for xyz, label, dist in nnbrs:
            points[label]['facecolor'] = '#00ff00'
            points[label]['edgecolor'] = '#00ff00'
            points[label]['radius'] = 3.0

            lines.append({
                'start' : point[0:2],
                'end'   : xyz[0:2],
                'color' : '#000000',
                'width' : 0.1,
            })

        plotter.draw_lines(lines)
        plotter.draw_points(points)
        plotter.show()

    """

    def __init__(self, objects=None):
        """Initialise a KDTree object."""
        self.root = None
        if objects:
            self.root = self.build(list([(objects[i], i) for i in range(len(objects))]))

    def build(self, objects, axis=0):
        """Populate a kd-tree with given objects.

        Parameters
        ----------
        objects : list
            The tree objects.
        axis : int, optional
            The axis along which to build.

        Returns
        -------
        Node
            The root node.

        """
        if not objects:
            return None

        objects.sort(key=lambda o: o[0][axis])
        median_idx = len(objects) // 2
        median_point, median_label = objects[median_idx]
        next_axis = (axis + 1) % 3

        return Node(
            median_point,
            axis,
            median_label,
            self.build(objects[:median_idx], next_axis),
            self.build(objects[median_idx + 1:], next_axis))

    def nearest_neighbor(self, point, exclude=None):
        """Find the nearest neighbor to a given point,
        excluding neighbors that have already been found.

        Parameters
        ----------
        point : list
            XYZ coordinates of the base point.
        exclude : set, optional
            A set of points to exclude from the search.
            Defaults to an empty set.

        Returns
        -------
        list:
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
            if d ** 2 < best[2]:
                search(far)

        exclude = exclude or set()
        best = [None, None, float('inf')]
        search(self.root)
        best[2] **= 0.5
        return best

    def nearest_neighbors(self, point, number, distance_sort=False):
        """Find the N nearest neighbors to a given point.

        Parameters
        ----------
        point : list
            XYZ coordinates of the bbase point.
        number : int
            The number of nearest neighbors.
        distance_sort : bool, optional
            Sort the nearest neighbors by distance to the base point.
            Default is ``False``.

        Returns
        -------
        list
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import pointcloud_xy
    from compas.plotters import Plotter

    plotter = Plotter()

    cloud = pointcloud_xy(999, (-500, 500))
    point = cloud[0]

    tree = KDTree(cloud)

    n       = 50
    nnbrs   = []
    exclude = set()

    for i in range(n):
        nnbr = tree.nearest_neighbor(point, exclude)
        nnbrs.append(nnbr)
        exclude.add(nnbr[1])

    for nnbr in nnbrs:
        print(nnbr)

    points = []
    for index, (x, y, z) in enumerate(cloud):
        points.append({
            'pos'      : [x, y],
            'facecolor': '#000000',
            'edgecolor': '#000000',
            'radius'   : 1.0
        })
    points.append({
        'pos'      : point[0:2],
        'facecolor': '#ff0000',
        'edgecolor': '#ff0000',
        'radius'   : 5.0
    })

    lines = []
    for xyz, label, dist in nnbrs:
        points[label]['facecolor'] = '#00ff00'
        points[label]['edgecolor'] = '#00ff00'
        points[label]['radius'] = 3.0

        lines.append({
            'start' : point[0:2],
            'end'   : xyz[0:2],
            'color' : '#000000',
            'width' : 0.1,
        })

    plotter.draw_lines(lines)
    plotter.draw_points(points)
    plotter.show()
