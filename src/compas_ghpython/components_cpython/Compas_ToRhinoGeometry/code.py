"""
Draws COMPAS geometry in Grasshopper.
"""
# r: compas

from ghpythonlib.componentbase import executingcomponent as component

from compas.scene import SceneObject


class CompasToRhinoGeometry(component):
    def RunScript(self, cg):
        if not cg:
            return None

        return SceneObject(item=cg).draw()
