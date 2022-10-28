from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas.plugins
from compas_ghpython.components import install_userobjects


@compas.plugins.plugin(category="install")
def installable_rhino_packages():
    return ["compas_ghpython"]


@compas.plugins.plugin(category="install")
def after_rhino_install(installed_packages):
    if "compas_ghpython" not in installed_packages:
        return []

    installed_objects = install_userobjects(os.path.join(os.path.dirname(__file__), "components", "ghuser"))

    return [
        (
            "compas_ghpython",
            "Installed {} GH User Objects".format(len(installed_objects)),
            True,
        )
    ]
