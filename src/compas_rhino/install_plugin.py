from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas_rhino

from compas._os import create_symlink
from compas._os import remove_symlink


__all__ = ['install_plugin']


def install_plugin(plugin, version=None):
    """Install a Python plugin for Rhino.

    Parameters
    ----------
    plugin : str
        The path to the plugin folder.
        For example, ``'path/to/RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}'``.

    Examples
    --------
    .. code-block:: bash

        >>> import compas_rhino
        >>> compas_rhino.install_plugin('path/to/RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}')

    .. code-block:: bash

        $ python -m compas_rhino.install_plugin path/to/RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}

    """
    if version not in ('5.0', '6.0'):
        version = '5.0'

    plugin_path, plugin_name = os.path.split(plugin)
    if not plugin_path:
        plugin_path = os.getcwd()
    source = os.path.join(plugin_path, plugin_name)

    if not os.path.isdir(source):
        raise Exception('Cannot find the plugin: {}'.format(source))

    if not os.path.isdir(os.path.join(source, 'dev')):
        raise Exception('The plugin does not contain a dev folder.')

    if not os.path.isfile(os.path.join(source, 'dev', '__plugin__.py')):
        raise Exception('The plugin does not contain plugin info.')

    python_plugins_path = compas_rhino._get_python_plugins_path(version)

    if not os.path.exists(python_plugins_path):
        os.mkdir(python_plugins_path)

    destination = os.path.join(python_plugins_path, plugin_name)

    print('Installing PlugIn {} to RhinoMac PythonPlugIns.'.format(plugin_name))

    if os.path.exists(destination):
        remove_symlink(destination)
    create_symlink(source, destination)

    print('PlugIn {} Installed.'.format(plugin_name))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('plugin_path', help="The path to the plugin.")

    args = parser.parse_args()

    install_plugin(args.plugin_path)
