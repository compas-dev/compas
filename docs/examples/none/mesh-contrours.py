import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_contours_numpy

mesh = Mesh.from_obj(compas.get('saddle.obj'))

# res = mesh_contours_pymesh(mesh)
# print(res)

levels, contours = mesh_contours_numpy(mesh)

for i in range(len(contours)):
    level = levels[i]
    contour = contours[i]
    print(level)
    for path in contour:
        for polygon in path:
            print([point.tolist() for point in polygon])
