"""
******************
scene
******************

.. currentmodule:: compas_rhino.scene

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
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
    Basic scene management in Rhino.

    .. code-block:: python

        from compas.geometry import Frame, Box
        from compas_rhino.scene import Scene

        box = Box(Frame.worldXY(), 1, 1, 1)

        scene = Scene()
        scene.add(box, name='Box', color=(255, 0, 0))
        scene.update()


    Note that, after adding objects, at least one call has to be made to the update method of the scene
    to make sure the objects are placed in the Rhino model.

    Object attributes can be set at the time when the data item is added to the scene,
    as above, with additional keyword arguments in the ``add`` call,
    or afterwards, by modyfying the attributes of the object directly.

    Only attributes that were modified before the call to the update method of the scene object will have an effect.

    .. code-block:: python

        from compas.geometry import Frame, Box
        from compas_rhino.scene import Scene

        box = Box(Frame.worldXY(), 1, 1, 1)

        scene = Scene()

        boxobj = scene.add(box)
        boxobj.name = 'Box'
        boxobj.color = (255, 0, 0)

        scene.update()


    Multiple scene objects can share a single item of COMPAS data.

    .. code-block:: python

        from compas.geometry import Frame, Box
        from compas_rhino.scene import Scene

        box = Box(Frame.worldXY(), 1, 1, 1)

        scene = Scene()

        boxobj = scene.add(box)
        boxobj.name = 'Box'
        boxobj.color = (255, 0, 0)

        scene.update()


    Dynamic scenes.

    .. code-block:: python

        from compas_rhino.scene import Scene

        scene = Scene()


    Synchronize modified objects.

    .. code-block:: python

        from compas_rhino.scene import Scene

        scene = Scene()

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

    def update(self):
        """Redraw the entire scene."""
        compas_rhino.rs.EnableRedraw(False)
        for guid in self.objects:
            self.objects[guid].draw()
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()
