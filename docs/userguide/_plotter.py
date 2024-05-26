# type: ignore

# import compas
from compas.datastructures import Mesh
from compas.colors import Color
from compas.geometry import Circle, Polygon, Line, Point, Vector
from compas_viewer.scene import Tag


def viewer_add_vertex(viewer, mesh, vertex, facecolor=None, edgecolor=None, size=None):
    facecolor = facecolor or Color.white()
    edgecolor = edgecolor or Color.black()
    size = size or 0.1
    point: Point = mesh.vertex_point(vertex) + [0, 0, 0.5]
    viewer.scene.add(
        Circle.from_point_and_radius(point, size),
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=2,
        n =100,
    )


def viewer_add_vertex_label(viewer, mesh, vertex, text, height=None):
    height = height or 50
    point: Point = mesh.vertex_point(vertex) + [0.09, -0.075, 0.6]
    viewer.scene.add(Tag(text, point, height=height, absolute_height=True))


def viewer_add_edge(viewer, mesh, edge, color=None, width=None):
    color = color or Color.black()
    width = width or 10
    viewer.scene.add(
        mesh.edge_line(edge).translated([0, 0, 0.1]),
        linecolor=color,
        linewidth=width,
    )


def viewer_add_face():
    pass


def viewer_add_halfvector(viewer, mesh: Mesh, halfedge, color=None, basewidth=0.01, arrowsize=5, distance=0.1):
    line: Line = mesh.edge_line(halfedge)
    line = line.offset(line.length * distance)

    color = color or Color.black()

    direction = line.direction
    normal = Vector.Zaxis().cross(direction)

    a = line.start + direction * (2 * distance)
    b = line.end - direction * (2 * distance + basewidth * arrowsize)
    c = b + normal * basewidth
    d = a + normal * basewidth

    arrowbase = Polygon([a, b, c, d])
    arrowhead = Polygon([b, b + direction * basewidth * arrowsize, b + normal * basewidth * arrowsize])

    viewer.scene.add(
        [arrowbase.translated([0, 0, 0.6]), arrowhead.translated([0, 0, 0.6])],
        surfacecolor=color,
        linecolor=color,
        show_lines=False,
    )
