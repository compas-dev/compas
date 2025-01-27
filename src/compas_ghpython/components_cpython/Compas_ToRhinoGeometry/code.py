"""
Draws COMPAS geometry in Grasshopper.
"""

# r: compas==2.8.1
import Grasshopper

from compas.scene import SceneObject


class CompasToRhinoGeometry(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, cg):
        if not cg:
            return None

        return SceneObject(item=cg).draw()
