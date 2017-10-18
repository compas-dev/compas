import compas
from compas.datastructures import Mesh
from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.numerical import plot_scalarfield_contours

mesh = Mesh.from_obj(compas.get_data('faces.obj'))
points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
centroid = centroid_points(points)
d = [distance_point_point(point, centroid) for point in points]
xy = [[points[i][0], points[i][1]] for i in range(len(points))]

plot_scalarfield_contours(xy, d)