"""
Draws COMPAS geometry in Grasshopper.
"""
from ghpythonlib.componentbase import executingcomponent as component

from compas.scene import build_scene_object


class CompasToRhinoGeometry(component):
    def RunScript(self, cg):
        if not cg:
            return None

        return build_scene_object(cg).draw()
