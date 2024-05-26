from compas.geometry import Point, Vector, Frame, Box, close

from scipy.spatial import cKDTree

boxes = [Box(4.5, 9.5, 3.0, Frame(Point(2.250, 4.750, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))),
Box(3.0, 5.0, 3.0, Frame(Point(1.500, 2.500, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))),
Box(8.0, 4.5, 3.0, Frame(Point(4.000, 2.250, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))),
Box(5.0, 5.0, 3.0, Frame(Point(2.500, 2.500, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))),
Box(7.5, 6.5, 3.0, Frame(Point(3.750, 3.250, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))),
Box(5.0, 6.5, 3.0, Frame(Point(2.500, 3.250, 1.500), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000)))]

tt_faces = [[Point(5.000, 8.000, 6.000), Point(0.000, 8.000, 6.000), Point(5.000, 3.000, 6.000), Point(0.000, 3.000, 6.000)],
[Point(14.500, -1.500, 6.000), Point(14.500, -1.500, 3.000), Point(12.500, -1.500, 6.000), Point(12.500, -1.500, 3.000)],
[Point(12.500, -1.500, 6.000), Point(12.500, 8.000, 6.000), Point(14.500, 8.000, 6.000), Point(14.500, -1.500, 6.000), Point(12.500, -1.500, 6.000)],
[Point(12.500, -1.500, 3.000), Point(12.500, 8.000, 3.000), Point(14.500, 8.000, 3.000), Point(14.500, -1.500, 3.000), Point(12.500, -1.500, 3.000)],
[Point(14.500, 8.000, 4.200), Point(14.500, 8.000, 3.000), Point(14.500, -1.500, 4.200), Point(14.500, -1.500, 3.000)],
[Point(12.500, 8.000, 6.000), Point(12.500, 8.000, 3.000), Point(14.500, 8.000, 6.000), Point(14.500, 8.000, 3.000)],
]

points = []
for box in boxes:
    for pt in box.to_vertices_and_faces()[0]:
        if not len(points):
            points.append(pt)
            continue

        tree = cKDTree(points)
        d, idx = tree.query(pt, k=1)
        if close(d, 0, 1e-3):
            pass
        else:
            points.append(pt)

for face in tt_faces:
    for pt in face:
        tree = cKDTree(points)
        d, idx = tree.query(pt, k=1)
        if close(d, 0, 1e-3):
            pass
        else:
            points.append(pt)

print(len(points))
tree = cKDTree(points)

from compas.datastructures import CellNetwork

network = CellNetwork()

for i, (x, y, z) in enumerate(points):
    network.add_vertex(key=i, x=x, y=y, z=z)

for box in boxes:
    verts, faces = box.to_vertices_and_faces()
    fidxs = []
    for face in faces:
        nface = []
        for idx in face:
            pt = verts[idx]
            d, ni = tree.query(pt, k=1)
            nface.append(ni)
        fidx = None
        for face in network.faces():
            if set( network.face_vertices(face)) == set(nface):
                fidx = face
                break
        else:
            fidx = network.add_face(nface)
        fidxs.append(fidx)
    network.add_cell(fidxs)
    print(fidxs)


for face in tt_faces:

    nface = []
    for pt in face:
        d, ni = tree.query(pt, k=1)
        nface.append(ni)

    fidx = None
    for face in network.faces():
        if set( network.face_vertices(face)) == set(nface):
            fidx = face
            break
    else:
        fidx = network.add_face(nface)


from compas_viewer import Viewer

viewer = Viewer()

viewer.add(network, show_faces=True, show_edges=True, show_vertices=True)
viewer.show()

"""
 [network.add_vertex(x=x, y=y, z=z) for x, y, z in vertices]
    [network.add_edge(u, v) for u, v in edges]
    [network.add_face(fverts) for fverts in faces]
    [network.add_cell(fkeys) for fkeys in cells]
"""
