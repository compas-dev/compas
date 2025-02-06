# r: compas>=2.8.1
"""
Displays information about the active COMPAS environment.
"""

import os

import Grasshopper

import compas


class CompasInfo(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self):
        try:
            import compas_bootstrapper

            environment_name = compas_bootstrapper.ENVIRONMENT_NAME
        except ImportError:
            environment_name = os.path.dirname(compas.__file__)
            environment_name = os.path.abspath(os.path.join(environment_name, ".."))

        ghenv.Component.Message = "COMPAS v{}".format(compas.__version__)  # noqa: F821
        info = "COMPAS Version: {}\nEnvironment: {}"
        return info.format(compas.__version__, environment_name)
