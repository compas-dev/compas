from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.artists import Artist


__all__ = ['Scene', 'SceneNode']


class SceneNode(object):

    def __init__(self, scene, item, **kwargs):
        self.scene = scene
        self.item = item
        self.artist = Artist.build(item, **kwargs)
        self.nodes = []


class Scene(object):
    """Rhino scene object for managing the visualisation of COMPAS data and geometry.

    Notes
    -----
    * Add "display mode": `Shaded`, `Ghosted`, ...
    * Add "projection": `Perspective`, `Orthogonal`, ...
    * Add "viewport": `Front`, `Left`, `Top`, `Perpsective`
    * Add "camera": ...
    """

    def __init__(self):
        self.nodes = []

    def add(self, item, **kwargs):
        node = SceneNode(self, item, **kwargs)
        self.nodes.append(node)
        return node

    def update(self):
        compas_rhino.rs.EnableRedraw(False)
        for node in self.nodes:
            node.artist.draw()
        compas_rhino.rs.EnableRedraw(True)

    def screenshot(self, path, width=1920, height=1080, scale=1,
                   draw_grid=False, draw_world_axes=False, draw_cplane_axes=False, background=False):
        """Save the current screen view.

        Parameters
        ----------
        path : str
            The path where the screenshot should be saved.
        width : int, optional
            The width of the saved image.
            Default is ``1920``.
        height : int, optional
            The height of the saved image.
            Default is ``1080``.
        scale : float, optional
            Scaling factor for the saved view.
            Default is ``1``.
        draw_grid : bool, optional
            Include the grid in the screenshot.
            Default is ``False``.
        draw_world_axes : bool, optional
            Include the world axes in the screenshot.
            Default is ``False``.
        draw_cplane_axes : bool, optional
            Include the CPlane axes in the screenshot.
            Default is ``False``.
        background : bool, optional
            Include the current background in the screenshot.
            Default is ``False``.

        Returns
        -------
        str
            The path where the file was saved.
        """
        return compas_rhino.screenshot_current_view(path,
                                                    width=width,
                                                    height=height,
                                                    scale=scale,
                                                    draw_grid=draw_grid,
                                                    draw_world_axes=draw_world_axes,
                                                    draw_cplane_axes=draw_cplane_axes,
                                                    background=background)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Line
    from compas.geometry import Frame

    from compas.datastructures import Mesh

    scene = Scene()

    a = Point(1.0, 1.0, 0.0)
    b = Point(5.0, 5.0, 0.0)
    ab = Line(a, b)
    world = Frame.worldXY()

    mesh = Mesh.from_polyhedron(6)

    scene.add(a, name="A", color=(0, 0, 0), layer="A")
    scene.add(b, name="B", color=(255, 255, 255), layer="B")
    scene.add(ab, name="AB", color=(128, 128, 128), layer="AB")
    scene.add(world, name="World", layer="World")
    scene.add(mesh, name="Cube", layer="Cube")

    scene.update()
