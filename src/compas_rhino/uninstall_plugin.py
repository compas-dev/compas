from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas_rhino

from compas._os import remove_symlink


__all__ = ['uninstall_plugin']


def uninstall_plugin(plugin, version=None):
    """Uninstall a Rhino Python Command Plugin.

    Parameters
    ----------
    plugin : str
        The name of the plugin.
    version : str, optional
        The version of Rhino for which the plugin should be uninstalled.
        Default is ``'6.0'``.

    Notes
    -----
    The version info is only relevant for Rhino on Windows.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_rhino.uninstall_plugin XXX{520ddb34-e56d-4a37-9c58-1da10edd1d62}

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    python_plugins_path = compas_rhino._get_python_plugins_path(version)

    destination = os.path.join(python_plugins_path, plugin)

    print('Uninstalling PlugIn {} from Rhino PythonPlugIns.'.format(plugin))

    if os.path.exists(destination):
        remove_symlink(destination)

    print('PlugIn {} Uninstalled.'.format(plugin))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('plugin', help="The path to the plugin.")
    parser.add_argument('-v', '--version', help="The version of Rhino.")

    args = parser.parse_args()

    uninstall_plugin(args.plugin, version=args.version)
