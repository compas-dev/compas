# Wikipedia KDTree <http://en.wikipedia.org/wiki/Kd-tree>
# ActiveState KDTree <http://code.activestate.com/recipes/577497-kd-tree-for-nearest-neighbor-search-in-a-k-dimensional-space>

from __future__ import print_function

import collections

from compas.geometry import distance_point_point_sqrd


__author__     = ['Matthias Rippmann <rippmann@arch.ethz.ch>',
                  'Tom Van Mele <van.mele@arch.ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'rippmann@arch.ethz.ch'


__all__ = [
    'KDTree'
]


Node = collections.namedtuple("Node", 'point axis label left right')


class KDTreeError(Exception):
    """"""
    pass


class KDTree(object):
    """A tree for nearest neighbor search in a k-dimensional space.
    """

    def __init__(self, objects=None):
        self.root = None
        if objects:
            self.root = self.build(list([(objects[i], i) for i in xrange(len(objects))]))

    def build(self, objects, axis=0):
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
            self.build(objects[median_idx + 1:], next_axis)
        )

    def nearest_neighbour(self, point, exclude):
        best = [None, None, float('inf')]  # [xyz, label, d2]

        def recursive_search(node):
            if node is None:
                return

            xyz, axis, label, left, right = node

            d2 = distance_point_point_sqrd(point, xyz)

            if d2 < best[2] and label not in exclude:
                best[:] = xyz, label, d2

            diff = point[axis] - xyz[axis]

            if diff <= 0:
                close, far = left, right
            else:
                close, far = right, left

            recursive_search(close)

            if diff ** 2 < best[2]:
                recursive_search(far)

        recursive_search(self.root)

        best[2] **= 0.5

        return best

    def nearest_neighbours(self, point, number, distance_sort=False):
        nnbrs = []
        exclude = set()
        for i in range(number):
            nnbr = self.nearest_neighbour(point, exclude)
            nnbrs.append(nnbr)
            exclude.add(nnbr[1])
        if distance_sort:
            return sorted(nnbrs, key=lambda nnbr: nnbr[2])
        return nnbrs


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import time
    from random import random

    # define random sample data

    cloud = [(random(), random(), 0) for i in xrange(50000)]
    point = (random(), random(), 0)

    # build tree

    tick = time.time()
    tree = KDTree(cloud)
    tock = time.time()

    print("{0} CPU seconds for building tree".format(tock - tick))

    n       = 1000
    nnbrs   = []
    exclude = set()

    tick = time.clock()

    # for i in range(n):
    #     nnbr = tree.nearest_neighbour(point, exclude)
    #     nnbrs.append(nnbr)
    #     exclude.add(nnbr[1])

    nnbrs = tree.nearest_neighbours(point, 1, distance_sort=True)

    print(point)

    for nnbr in nnbrs:
        print(nnbr)

    tock = time.clock()

    print("{0} CPU seconds for {1} nearest neighbor(s)".format(tock - tick, n))
