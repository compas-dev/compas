# r: compas>=2.8.1
"""
Displays information about the active COMPAS environment.
"""

import compas_bootstrapper
import Grasshopper

import compas


class CompasInfo(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self):
        ghenv.Component.Message = "COMPAS v{}".format(compas.__version__)  # noqa: F821
        info = "COMPAS Version: {}\nEnvironment: {}"
        return info.format(compas.__version__, compas_bootstrapper.ENVIRONMENT_NAME)
