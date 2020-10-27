from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.scene import BaseScene

import compas_rhino

# this is necessary to register the artists and objects
import compas_rhino.artists
import compas_rhino.objects


__all__ = ['Scene']


class Scene(BaseScene):
    """A base Rhino scene.

    Attributes
    ----------
    objects : dict
        Mapping between GUIDs and diagram objects added to the scene.
        The GUIDs are automatically generated and assigned.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_rhino.scene import Scene

        mesh = Mesh.from_off(compas.get('tubemesh.off'))

        scene = Scene()
        scene.add(mesh, name="Tubemesh", layer="SceneTest")

        scene.clear_layers()
        scene.update()

    """

    def purge(self):
        """Clear all objects from the scene."""
        compas_rhino.rs.EnableRedraw(False)
        try:
            for guid in list(self.objects.keys()):
                self.objects[guid].clear()
                del self.objects[guid]
        except Exception:
            pass
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear(self):
        """Clear all objects from the scene."""
        compas_rhino.rs.EnableRedraw(False)
        try:
            for guid in list(self.objects.keys()):
                self.objects[guid].clear()
        except Exception:
            pass
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear_layers(self):
        """Clear all object layers of the scene."""
        compas_rhino.rs.EnableRedraw(False)
        try:
            for guid in list(self.objects.keys()):
                self.objects[guid].clear_layer()
        except Exception:
            pass
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def redraw(self):
        """Redraw the entire scene."""
        compas_rhino.rs.EnableRedraw(False)
        try:
            for guid in self.objects:
                self.objects[guid].draw()
        except Exception:
            pass
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
