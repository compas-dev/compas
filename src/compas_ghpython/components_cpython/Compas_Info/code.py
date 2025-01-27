"""
Displays information about the active COMPAS environment.
"""

# r: compas==2.8.1

import compas_bootstrapper
import Grasshopper

import compas


class CompasInfo(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self):
        self.Message = "COMPAS v{}".format(compas.__version__)
        info = "COMPAS Version: {}\nEnvironment: {}"
        return info.format(compas.__version__, compas_bootstrapper.ENVIRONMENT_NAME)
