"""
Draws COMPAS geometry in Grasshopper.
"""
from ghpythonlib.componentbase import executingcomponent as component

from compas.artists import Artist


class CompasToRhinoGeometry(component):
    def RunScript(self, cg):
        if not cg:
            return None

        return Artist(cg).draw()
