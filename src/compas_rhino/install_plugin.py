import os
import imp

import compas_rhino

from compas._os import create_symlink
from compas._os import remove_symlink


__all__ = ['install_plugin']


def install_plugin(plugin, version=None):
    """Install a Rhino Python Command Plugin.

    Parameters
    ----------
    plugin : str
        The path to the plugin folder.
    version : str, optional
        The version of Rhino for which the plugin should be installed.
        Default is ``'6.0'``.

    Notes
    -----
    The version info is only relevant for Rhino on Windows.

    The function creates an *editable install*, which means that the plugin
    folder is *symlinked* into the correct location so Rhino can find and load it.
    The contents of the source folder can still be edited and next time you start
    Rhino those canges will be reflected in the loaded plugin.

    Examples
    --------
    Assuming the plugin folder is at the following location on your computer

    .. code-block:: none

        ~/Code/compas_xxx/ui/Rhino/XXX

    and contains at least a "dev" folder with a ``__plugin__.py`` file with

    * the GUID of the tool: ``id={...}``, and
    * the name of the tool: ``title="RV2"``,

    it can be installed with the following command,

    .. code-block:: bash

        $ cd ~/Code/compas_xxx
        $ python -m compas_rhino.install_plugin ui/Rhino/XXX

    or the following, if the plugin should be installed for Rhino5.

    .. code-block:: bash

        $ cd ~/Code/compas_xxx
        $ python -m compas_rhino.install_plugin -v 5.0 ui/Rhino/XXX

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    if not os.path.isdir(plugin):
        raise Exception('Cannot find the plugin: {}'.format(plugin))

    plugin_dir = os.path.abspath(plugin)

    plugin_path, plugin_name = os.path.split(plugin_dir)
    if not plugin_path:
        plugin_path = os.getcwd()

    plugin_dev = os.path.join(plugin_dir, 'dev')

    if not os.path.isdir(plugin_dev):
        raise Exception('The plugin does not contain a dev folder.')

    plugin_info = os.path.join(plugin_dev, '__plugin__.py')

    if not os.path.isfile(plugin_info):
        raise Exception('The plugin does not contain plugin info.')

    __plugin__ = imp.load_source('__plugin__', plugin_info)

    if not __plugin__.id:
        raise Exception('Plugin id is not set.')

    if not __plugin__.title:
        raise Exception('Plugin title is not set.')

    plugin_fullname = "{}{}".format(__plugin__.title, __plugin__.id)

    python_plugins_path = compas_rhino._get_python_plugins_path(version)

    if not os.path.exists(python_plugins_path):
        os.mkdir(python_plugins_path)

    source = plugin_dir
    destination = os.path.join(python_plugins_path, plugin_fullname)

    print('Installing PlugIn {} to Rhino PythonPlugIns.'.format(plugin_name))

    remove_symlink(destination)
    create_symlink(source, destination)

    print()
    print('PlugIn {} Installed.'.format(plugin_name))
    print()
    print('Restart Rhino and open the Python editor at least once to make it available.')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='COMPAS Rhino PLugin Installation command-line utility.')

    parser.add_argument('plugin', help="The path to the plugin directory.")
    parser.add_argument('-v', '--version', help="The version of Rhino.")

    args = parser.parse_args()

    install_plugin(args.plugin, version=args.version)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    main()
