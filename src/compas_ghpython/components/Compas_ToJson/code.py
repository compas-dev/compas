"""
Serializes COMPAS objects to JSON.
"""
from ghpythonlib.componentbase import executingcomponent as component

import compas


class CompasInfo(component):
    def RunScript(self, data, filepath, pretty):
        result = filepath

        if filepath:
            compas.json_dump(data, filepath, pretty)
        else:
            result = compas.json_dumps(data, pretty)

        return result
