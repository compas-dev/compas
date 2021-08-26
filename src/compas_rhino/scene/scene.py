from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import compas_rhino

from compas.scene import BaseScene


__all__ = ['Scene']


class Scene(BaseScene):
    """Implementation of the base scene for Rhino.

    Attributes
    ----------
    objects : dict
        Mapping between GUIDs and diagram objects added to the scene.
        The GUIDs are automatically generated and assigned.

    """

    def purge(self):
        """Purge all objects from the scene."""
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

    def draw(self, pause=None):
        if pause:
            time.sleep(pause)
            compas_rhino.wait()
        compas_rhino.rs.EnableRedraw(False)
        for guid in self.objects:
            self.objects[guid].draw()
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def update(self, pause=None):
        if pause:
            time.sleep(pause)
            compas_rhino.wait()
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def on(self, interval, frames, record=False, recording=None, dpi=150):
        if record:
            if not recording:
                raise Exception('Please provide a path for the recording.')

        def outer(func):
            count = 0
            while count < frames:
                time.sleep(interval)
                func(count)
                self.update()
                compas_rhino.wait()
                count += 1

        return outer
