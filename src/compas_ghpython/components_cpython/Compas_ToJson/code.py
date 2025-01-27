"""
Serializes COMPAS objects to JSON.
"""

# r: compas==2.8.1
import Grasshopper

import compas


class CompasInfo(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, data, filepath, pretty):
        json = filepath

        if filepath:
            compas.json_dump(data, filepath, pretty)
        else:
            json = compas.json_dumps(data, pretty)

        return json
