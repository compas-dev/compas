"""
Displays information about the active COMPAS environment.
"""

import compas_bootstrapper
from ghpythonlib.componentbase import executingcomponent as component

import compas


class CompasInfo(component):
    def RunScript(self):
        self.Message = "COMPAS v{}".format(compas.__version__)
        info = "COMPAS Version: {}\nEnvironment: {}"
        return info.format(compas.__version__, compas_bootstrapper.ENVIRONMENT_NAME)
