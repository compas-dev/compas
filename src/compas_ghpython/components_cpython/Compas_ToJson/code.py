"""
Serializes COMPAS objects to JSON.
"""

from ghpythonlib.componentbase import executingcomponent as component

import compas


class CompasInfo(component):
    def RunScript(self, data, filepath, pretty):
        json = filepath

        if filepath:
            compas.json_dump(data, filepath, pretty)
        else:
            json = compas.json_dumps(data, pretty)

        return json
