from compas.geometry import KDTree


def test_nearest_neighbor():
    tree = KDTree([[0, 0, 0], [2, 0, 0], [5, 0, 0]])

    neighbor = tree.nearest_neighbor([1.5, 0, 0])

    assert neighbor is not None
    assert neighbor.point == [2, 0, 0]
    assert neighbor.label == 1
    assert neighbor.distance == 0.5


def test_nearest_neighbor_returns_none_for_empty_or_exhausted_tree():
    tree = KDTree([[0, 0, 0]])

    assert KDTree().nearest_neighbor([0, 0, 0]) is None
    assert tree.nearest_neighbor([0, 0, 0], exclude={0}) is None


def test_nearest_neighbors_stops_when_tree_is_exhausted():
    tree = KDTree([[2, 0, 0], [0, 0, 0]])

    neighbors = tree.nearest_neighbors([0, 0, 0], 5, distance_sort=True)

    assert [neighbor.label for neighbor in neighbors] == [1, 0]
    assert [neighbor.distance for neighbor in neighbors] == [0.0, 2.0]


def test_build_accepts_explicit_integer_labels():
    tree = KDTree()
    tree.root = tree.build([([0, 0, 0], 10), ([2, 0, 0], 20)])

    neighbor = tree.nearest_neighbor([1.75, 0, 0])

    assert neighbor is not None
    assert neighbor.label == 20
