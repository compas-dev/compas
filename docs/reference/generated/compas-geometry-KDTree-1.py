from compas.geometry import KDTree
from compas.geometry import pointcloud_xy
from compas.visualization import Plotter

plotter = Plotter()

cloud = pointcloud_xy(999, (-500, 500))
point = cloud[0]

tree = KDTree(cloud)

n       = 50
nnbrs   = []
exclude = set()

for i in range(n):
    nnbr = tree.nearest_neighbour(point, exclude)
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