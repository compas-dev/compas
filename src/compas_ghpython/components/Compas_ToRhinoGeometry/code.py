"""
Draws COMPAS geometry in Grasshopper.
"""

from ghpythonlib.componentbase import executingcomponent as component

from compas.scene import sceneobject_factory


class CompasToRhinoGeometry(component):
    def RunScript(self, cg):
        if not cg:
            return None

        return sceneobject_factory(item=cg).draw()
