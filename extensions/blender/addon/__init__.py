# SPDX-License-Identifier: MIT
"""COMPAS for Blender.

This extension only bundles COMPAS and its dependencies as Python wheels.
Blender installs them into the extensions site-packages folder, so once the
extension is enabled, ``compas`` and ``compas_blender`` can be imported from
any script, the Python console, or other add-ons.
"""

import os

import bpy


class COMPAS_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        try:
            import compas
        except ImportError as error:
            layout.label(text="COMPAS could not be imported: {}".format(error), icon="ERROR")
            return

        column = layout.column(align=True)
        column.label(text="COMPAS {}".format(compas.__version__), icon="CHECKMARK")
        column.label(text=os.path.dirname(os.path.dirname(compas.__file__)))


classes = (COMPAS_AddonPreferences,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
