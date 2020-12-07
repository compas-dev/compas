from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import itertools
import os
import sys

import compas_rhino

import compas._os
import compas.plugins

__all__ = ['install']


def install(version=None, packages=None):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0', '7.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to install or None to use default package list.
        Default is ``['compas', 'compas_rhino', 'compas_ghpython']``.

    Examples
    --------
    .. code-block:: python

        import compas_rhino
        compas_rhino.install('6.0')

    .. code-block:: bash

        python -m compas_rhino.install -v 6.0

    """

    if version not in ('5.0', '6.0', '7.0'):
        version = '6.0'

    packages = _filter_installable_packages(version, packages)

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)
    scripts_path = compas_rhino._get_scripts_path(version)

    print('Installing COMPAS packages to Rhino {0} scripts folder:'.format(version))
    print('Location scripts folder: {}'.format(scripts_path))
    print()

    results = []
    symlinks_to_install = []
    symlinks_to_uninstall = []
    exit_code = 0

    for package in packages:
        package_path = compas_rhino._get_package_path(importlib.import_module(package))
        symlink_path = os.path.join(scripts_path, package)
        symlinks_to_install.append(dict(name=package, source_path=package_path, link=symlink_path))
        symlinks_to_uninstall.append(dict(name=package, link=symlink_path))

        # Handle legacy install location
        legacy_path = os.path.join(ipylib_path, package)
        if os.path.exists(legacy_path):
            symlinks_to_uninstall.append(dict(name=package, link=legacy_path))

    # First uninstall existing copies of packages requested for installation
    symlinks = [link['link'] for link in symlinks_to_uninstall]
    uninstall_results = compas._os.remove_symlinks(symlinks)

    for uninstall_data, success in zip(symlinks_to_uninstall, uninstall_results):
        if not success:
            results.append((uninstall_data['name'], 'ERROR: Cannot remove symlink, try to run as administrator.'))

    # Handle legacy bootstrapper
    if not compas_rhino._try_remove_bootstrapper(ipylib_path):
        results.append(('compas_bootstrapper', 'ERROR: Cannot remove legacy compas_bootstrapper, try to run as administrator.'))

    # Ready to start installing
    symlinks = [(link['source_path'], link['link']) for link in symlinks_to_install]
    install_results = compas._os.create_symlinks(symlinks)

    for install_data, success in zip(symlinks_to_install, install_results):
        result = 'OK' if success else 'ERROR: Cannot create symlink, try to run as administrator.'
        results.append((install_data['name'], result))

    if not all(install_results):
        exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not install bootstrapper, try uninstalling first'))
    else:
        try:
            _update_bootstrapper(scripts_path, packages)
            results.append(('compas_bootstrapper', 'OK'))
        except:  # noqa: E722
            results.append(('compas_bootstrapper', 'ERROR: Could not create compas_bootstrapper to auto-determine Python environment'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status != 'OK':
            exit_code = -1

    print('\nCompleted.')
    if exit_code != 0:
        sys.exit(exit_code)


@compas.plugins.plugin(category='install', pluggable_name='installable_rhino_packages', tryfirst=True)
def default_installable_rhino_packages():
    # While this list could obviously be hard-coded, I think
    # eating our own dogfood and using plugins to define this, just like
    # any other extension/plugin would be is a better way to ensure consistent behavior.
    return ['compas', 'compas_rhino']


@compas.plugins.pluggable(category='install', selector='collect_all')
def installable_rhino_packages():
    """Provide a list of packages to make available inside Rhino.

    Extensions providing Rhino or Grasshopper features
    can implement this pluggable interface to automatically
    have their packages made available inside Rhino when
    COMPAS is installed into it.

    Examples
    --------
    >>> import compas.plugins
    >>> @compas.plugins.plugin(category='install')
    ... def installable_rhino_packages():
    ...    return ['compas_fab']

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of package names to make available inside Rhino.
    """
    pass


def _update_bootstrapper(install_path, packages):
    # Take either the CONDA environment directory or the current Python executable's directory
    python_directory = os.environ.get('CONDA_PREFIX', None) or os.path.dirname(sys.executable)
    environment_name = os.environ.get('CONDA_DEFAULT_ENV', '')
    conda_exe = os.environ.get('CONDA_EXE', '')

    compas_bootstrapper = compas_rhino._get_bootstrapper_path(install_path)

    bootstrapper_data = compas_rhino._get_bootstrapper_data(compas_bootstrapper)
    installed_packages = bootstrapper_data.get('INSTALLED_PACKAGES', [])
    installed_packages = list(set(installed_packages + list(packages)))

    with open(compas_bootstrapper, 'w') as f:
        f.write('ENVIRONMENT_NAME = r"{}"\n'.format(environment_name))
        f.write('PYTHON_DIRECTORY = r"{}"\n'.format(python_directory))
        f.write('CONDA_EXE = r"{}"\n'.format(conda_exe))
        f.write('INSTALLED_PACKAGES = {}'.format(repr(installed_packages)))


def _filter_installable_packages(version, packages):
    ghpython_incompatible = False

    if compas.OSX and version == 5.0:
        ghpython_incompatible = True

    if not packages:
        # Flatten list of results (resulting from collect_all pluggable)
        packages = list(itertools.chain.from_iterable(installable_rhino_packages()))
    elif 'compas_ghpython' in packages and ghpython_incompatible:
        print('Skipping installation of compas_ghpython since it\'s not supported for Rhino 5 for Mac')

    if ghpython_incompatible:
        packages.remove('compas_ghpython')

    return packages


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', choices=['5.0', '6.0', '7.0'], default='6.0', help="The version of Rhino to install the packages in.")
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to install.")

    args = parser.parse_args()

    install(version=args.version, packages=args.packages)
