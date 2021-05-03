"""
Deserializes JSON into COMPAS objects.
"""
import os

from ghpythonlib.componentbase import executingcomponent as component

import compas


class CompasInfo(component):
    def RunScript(self, json_file_or_string):
        try:
            return compas.json_load(json_file_or_string)
        except:
            return compas.json_loads(json_file_or_string)
