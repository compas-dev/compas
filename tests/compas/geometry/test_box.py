from compas.geometry import Box, Frame


def test_intersection_with_box_parallel_face():
    frame0 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([1, 0, 0], [1, 0, 0], [0, 1, 0])
    box0 = Box(frame=frame0, xsize=1, ysize=1, zsize=1)
    box1 = Box(frame=frame1, xsize=1, ysize=1, zsize=1)
    assert box0.intersection_with_box(box1) is True


def test_intersection_with_box_edge():
    frame0 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([1, 1, 0], [1, 0, 0], [0, 1, 0])
    box0 = Box(frame=frame0, xsize=1, ysize=1, zsize=1)
    box1 = Box(frame=frame1, xsize=1, ysize=1, zsize=1)
    assert box0.intersection_with_box(box1) is True


def test_intersection_with_box_vertex():
    frame0 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([1, 1, 1], [1, 0, 0], [0, 1, 0])
    box0 = Box(frame=frame0, xsize=1, ysize=1, zsize=1)
    box1 = Box(frame=frame1, xsize=1, ysize=1, zsize=1)
    assert box0.intersection_with_box(box1) is True


def test_intersection_with_box_rotated():
    frame0 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([0.0, 0.85, 0.92], [1, 0, 0], [0, 0.87, 0.48])
    box0 = Box(frame=frame0, xsize=1, ysize=1, zsize=1)
    box1 = Box(frame=frame1, xsize=1, ysize=1, zsize=1)
    assert box0.intersection_with_box(box1) is False


def test_intersection_with_box_inside():
    frame0 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    box0 = Box(frame=frame0, xsize=1, ysize=1, zsize=1)
    box1 = Box(frame=frame1, xsize=0.5, ysize=0.5, zsize=0.5)
    assert box0.intersection_with_box(box1) is True
