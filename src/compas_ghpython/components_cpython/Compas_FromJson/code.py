# r: compas>=2.8.1
"""
Deserializes JSON into COMPAS objects.
"""

import Grasshopper

import compas


class CompasLoadFromJson(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, json: str):
        if not json:
            return None

        try:
            return compas.json_load(json)
        except Exception:
            ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, f"Failed to load JSON from path: {json}, Trying as string.")  # noqa: F821
            return compas.json_loads(json)
