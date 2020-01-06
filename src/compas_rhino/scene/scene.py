from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.artists import Artist


__all__ = ['Scene']


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
        self._artists = []

    @property
    def artists(self):
        return self._artists

    @artists.setter
    def artists(self, artists):
        self._artists = artists

    def add(self, item, artist=None, **kwargs):
        if not artist:
            artist = Artist.build(item, **kwargs)
        artist.draw()
        self._artists.append(artist)
        return artist

    def find(self, item):
        raise NotImplementedError

    def register_listener(self, listener):
        """Register a listener for pick events.

        Parameters
        ----------
        listener : callable
            The handler for pick events.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        pass

    def draw(self):
        compas_rhino.rs.Redraw(False)
        for artist in self.artists:
            artist.draw()
        compas_rhino.rs.Redraw(True)

    def redraw(self):
        pass

    def save(self, path, width=1920, height=1080, scale=1,
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

    from compas.datastructures import Mesh
    from compas.geometry import Point
    from compas.geometry import Line
    from compas.geometry import Polygon
    from compas.geometry import Box
    
    import compas_rhino
    from compas_rhino.scene import Scene

    scene = Scene()

    mesh = Mesh.from_polyhedron(20)

    # this constructs and returns an artist or a scene object in the background
    mesh_obj = scene.add(mesh, name="Icosahedron")
