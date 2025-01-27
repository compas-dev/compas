"""
Deserializes JSON into COMPAS objects.
"""

# r: compas==2.8.1

import Grasshopper

import compas


class CompasLoadFromJson(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, json):
        if not json:
            return None

        try:
            return compas.json_load(json)
        except Exception:
            return compas.json_loads(json)
