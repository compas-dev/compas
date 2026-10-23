from collections.abc import Collection
from collections.abc import Sequence
from typing import NamedTuple

from compas._typing import CoordinateType

from ._core.distance import distance_point_point_sqrd


class Node(NamedTuple):
    """A node in a `KDTree`."""

    point: CoordinateType
    axis: int
    label: int
    left: "Node | None"
    right: "Node | None"


class Neighbor(NamedTuple):
    """A nearest-neighbor search result."""

    point: CoordinateType
    label: int
    distance: float


class KDTree:
    """A three-dimensional tree for nearest-neighbor searches.

    Parameters
    ----------
    objects
        Points used to populate the tree. Their positions in the sequence are
        used as labels. If omitted, the tree is initially empty.

    Notes
    -----
    `build` also accepts explicitly labeled points when indices from another
    sequence are required.

    References
    ----------
    * [k-d tree](https://en.wikipedia.org/wiki/K-d_tree)
    * [KD-tree for nearest-neighbor search](https://code.activestate.com/recipes/577497-kd-tree-for-nearest-neighbor-search-in-a-k-dimensional-space/)

    Examples
    --------
    >>> tree = KDTree([[0, 0, 0], [2, 0, 0]])
    >>> tree.nearest_neighbor([0.5, 0, 0])
    Neighbor(point=[0, 0, 0], label=0, distance=0.5)

    """

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, objects: Sequence[CoordinateType] | None = None) -> None:
        self.root: Node | None = None
        if objects:
            self.root = self.build([(point, index) for index, point in enumerate(objects)])

    # ==========================================================================
    # Methods
    # ==========================================================================

    def build(self, objects: list[tuple[CoordinateType, int]], axis: int = 0) -> Node | None:
        """Build a tree from labeled points.

        Parameters
        ----------
        objects
            Point-label pairs. The list is sorted in place while building the
            tree.
        axis
            The initial splitting axis.

        Returns
        -------
        Node | None
            The root node, or `None` when `objects` is empty.

        """
        if not objects:
            return None

        objects.sort(key=lambda item: item[0][axis])
        median = len(objects) // 2
        point, label = objects[median]
        next_axis = (axis + 1) % 3
        return Node(
            point,
            axis,
            label,
            self.build(objects[:median], next_axis),
            self.build(objects[median + 1 :], next_axis),
        )

    def nearest_neighbor(
        self,
        point: CoordinateType,
        exclude: Collection[int] | None = None,
    ) -> Neighbor | None:
        """Find the nearest non-excluded point.

        Parameters
        ----------
        point
            The query point.
        exclude
            Labels to exclude from the search.

        Returns
        -------
        Neighbor | None
            The nearest neighbor, or `None` when no eligible point exists.

        """
        excluded = set(exclude or ())
        best: Neighbor | None = None
        best_distance_sqrd = float("inf")

        def search(node: Node | None) -> None:
            nonlocal best
            nonlocal best_distance_sqrd

            if node is None:
                return

            distance_sqrd = distance_point_point_sqrd(point, node.point)
            if distance_sqrd < best_distance_sqrd and node.label not in excluded:
                best = Neighbor(node.point, node.label, distance_sqrd)
                best_distance_sqrd = distance_sqrd

            delta = point[node.axis] - node.point[node.axis]
            close, far = (node.left, node.right) if delta <= 0 else (node.right, node.left)
            search(close)
            if delta**2 < best_distance_sqrd:
                search(far)

        search(self.root)
        if best is None:
            return None
        return Neighbor(best.point, best.label, best.distance**0.5)

    def nearest_neighbors(self, point: CoordinateType, number: int, distance_sort: bool = False) -> list[Neighbor]:
        """Find up to a requested number of nearest neighbors.

        Parameters
        ----------
        point
            The query point.
        number
            The maximum number of neighbors.
        distance_sort
            Sort the result by increasing distance.

        Returns
        -------
        list[Neighbor]
            The available neighbors. The list can contain fewer than `number`
            items when the tree is exhausted.

        """
        neighbors = []
        excluded: set[int] = set()
        for _ in range(number):
            neighbor = self.nearest_neighbor(point, excluded)
            if neighbor is None:
                break
            neighbors.append(neighbor)
            excluded.add(neighbor.label)
        if distance_sort:
            neighbors.sort(key=lambda neighbor: neighbor.distance)
        return neighbors
