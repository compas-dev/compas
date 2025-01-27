"""
Draws COMPAS geometry in Grasshopper.
"""

# r: compas==2.8.1

from ghpythonlib.componentbase import executingcomponent as component

from compas.scene import SceneObject


class CompasToRhinoGeometry(component):
    def RunScript(self, cg):
        if not cg:
            return None

        return SceneObject(item=cg).draw()
