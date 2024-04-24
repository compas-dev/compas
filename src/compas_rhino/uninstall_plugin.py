from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas_rhino
from compas._os import remove_symlink


def uninstall_plugin(plugin, version=None):
    """Uninstall a Rhino Python Command Plugin.

    Parameters
    ----------
    plugin : str
        The name of the plugin.
    version : {'5.0', '6.0', '7.0', '8.0'}, optional
        The version of Rhino for which the plugin should be uninstalled.
        Default is ``'7.0'``.

    Notes
    -----
    The version info is only relevant for Rhino on Windows.

    Examples
    --------
    .. code-block:: bash

        python -m compas_rhino.uninstall_plugin XXX

    """
    version = compas_rhino._check_rhino_version(version)

    python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)
    plugin_name = plugin.split("{")[0]

    symlinks = []
    dirs = []

    for name in os.listdir(python_plugins_path):
        path = os.path.join(python_plugins_path, name)

        if os.path.islink(path):
            if name.split("{")[0] == plugin_name:
                symlinks.append(name)

        elif os.path.isdir(path):
            if name.split("{")[0] == plugin_name:
                dirs.append(name)

    print("\nUninstalling PlugIn {} from Rhino PythonPlugIns:".format(plugin_name))

    if not symlinks and not dirs:
        print("Nothing to uninstall...\n")

    else:
        for name in symlinks:
            print("- {}".format(name))
            destination = os.path.join(python_plugins_path, name)
            remove_symlink(destination)

        for name in dirs:
            print("- {}".format(name))
            destination = os.path.join(python_plugins_path, name)
            os.rmdir(destination)

        print("\nPlugIn {} Uninstalled.\n".format(plugin_name))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("plugin", help="The name of the plugin.")
    parser.add_argument(
        "-v",
        "--version",
        choices=compas_rhino.SUPPORTED_VERSIONS,
        default=compas_rhino.DEFAULT_VERSION,
        help="The version of Rhino.",
    )

    args = parser.parse_args()

    uninstall_plugin(args.plugin, version=args.version)
