# r: compas>=2.8.1
"""
Serializes COMPAS objects to JSON.
"""

from typing import Any

import Grasshopper

import compas


class CompasDumpToJson(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, data: Any, filepath: str, pretty: bool):
        json = filepath

        if filepath:
            compas.json_dump(data, filepath, pretty)
        else:
            json = compas.json_dumps(data, pretty)

        return json
