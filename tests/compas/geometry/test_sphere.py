# from compas.geometry import Frame
# from compas.geometry import Point
# from compas.geometry import Scale
# from compas.geometry import Sphere


# def test_sphere_scaling():
#     frame = Frame.worldXY()
#     frame.point = Point(1, 1, 1)
#     s = Sphere(frame, radius=10)
#     s.transform(Scale.from_factors([2, 3, 4]))
#     assert s.point.x == 2
#     assert s.point.y == 3
#     assert s.point.z == 4
#     assert s.radius == 40
