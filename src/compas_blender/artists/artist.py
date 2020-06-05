from compas_blender.utilities import draw_points
from compas_blender.utilities import draw_lines
from compas_blender.utilities import draw_faces
from compas_blender.utilities import redraw


__all__ = ['Artist']


class Artist(object):

    def __init__(self, layer=None):
        self.layer = layer
        self.defaults = {
            'color.point': [1.0, 1.0, 1.0],
            'color.line': [0.0, 0.0, 0.0],
            'color.polygon': [0.8, 0.8, 0.8],
        }
        self.vertex_objects = []
        self.edge_objects = []
        self.face_objects = []

    def redraw(self, timeout=None):
        redraw()

    def clear_layer(self):
        # layer is a collection name
        raise NotImplementedError

    def save(self, path, width=1920, height=1080, scale=1,
             draw_grid=False, draw_world_axes=False, draw_cplane_axes=False, background=False):
        raise NotImplementedError

    def draw_points(self, points, layer=None, clear_layer=False, redraw=False):
        # every point must be of the form:
        # - point: XYZ
        # - size: {small, medium, large}
        # - color: RGB
        # - name: None
        # - label?
        draw_points(points, layer=layer)

    def draw_lines(self, lines, layer=None, clear_layer=False, redraw=False):
        # every line must be of the form:
        # - start: XYZ
        # - end: XYZ
        # - or line: start, end
        # - width: float
        # - color: RGB
        # - name: None
        # - label?
        draw_lines(lines, layer=layer)

    def draw_polygons(self, polygons, layer=None, clear_layer=False, redraw=False):
        # every polygon must be of the form:
        # - points: list of XYZ
        # - color: RGB
        # - name: None
        # - label?
        draw_faces(polygons, layer=layer)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
