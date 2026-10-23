from compas.geometry import scalarfield_contours


def test_scalarfield_contours_accepts_explicit_levels():
    points = [[0, 0], [1, 0], [0, 1], [1, 1]]
    values = [0, 1, 0, 1]

    levels, contours = scalarfield_contours(points, values, levels=[0.25, 0.5, 0.75], density=11)

    assert levels == [0.25, 0.5, 0.75]
    assert len(contours) == 3
    for level, paths in zip(levels, contours):
        assert len(paths) == 1
        assert all(abs(point[0] - level) < 1e-12 for point in paths[0])
        assert paths[0][0][1] == 0
        assert paths[0][-1][1] == 1


def test_scalarfield_contours_generates_requested_number_of_levels():
    points = [[0, 0], [1, 0], [0, 1], [1, 1]]
    values = [0, 1, 0, 1]

    levels, contours = scalarfield_contours(points, values, levels=3, density=11)

    assert levels == [0.25, 0.5, 0.75]
    assert len(contours) == 3


def test_scalarfield_contours_joins_closed_paths():
    points = [[x, y] for y in range(-2, 3) for x in range(-2, 3)]
    values = [x**2 + y**2 for x, y in points]

    levels, contours = scalarfield_contours(points, values, levels=[1.5], density=41)

    assert levels == [1.5]
    assert len(contours[0]) == 1
    assert contours[0][0][0] == contours[0][0][-1]
