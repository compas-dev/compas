"""
Deserializes JSON into COMPAS objects.
"""

from ghpythonlib.componentbase import executingcomponent as component

import compas


class CompasInfo(component):
    def RunScript(self, json):
        if not json:
            return None

        try:
            return compas.json_load(json)
        except:  # noqa: E722
            return compas.json_loads(json)
