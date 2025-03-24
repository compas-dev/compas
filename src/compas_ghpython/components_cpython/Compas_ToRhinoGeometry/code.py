# r: compas>=2.8.1
"""
Draws COMPAS geometry in Grasshopper.
"""

from typing import Any

import Grasshopper

from compas.scene import SceneObject


class CompasToRhinoGeometry(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, cg: Any):
        if not cg:
            return None

        return SceneObject(item=cg).draw()
