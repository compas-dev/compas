from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import io
import importlib
import os
import sys

import compas_rhino

from compas._os import system
from compas._os import remove_symlink
from compas._os import create_symlink


__all__ = ['install']


INSTALLABLE_PACKAGES = ['compas', 'compas_rhino']

if system == 'win32':
    INSTALLABLE_PACKAGES.append('compas_ghpython')


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


def _get_bootstrapper_data(compas_bootstrapper):
    data = {}

    if not os.path.exists(compas_bootstrapper):
        return data

    content = io.open(compas_bootstrapper, encoding='utf8').read()
    exec(content, data)

    return data


def install(version=None, packages=None):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to install or None to use default package list.
        Default is ``['compas', 'compas_rhino', 'compas_ghpython']``.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.install('6.0')

    .. code-block:: python

        $ python -m compas_rhino.install -v 6.0

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    if system == 'win32':
        print('Installing COMPAS packages to Rhino {0} IronPython lib:'.format(version))
    elif system == 'darwin':
        print('Installing COMPAS packages to Rhino IronPython lib.')

    if not packages:
        packages = INSTALLABLE_PACKAGES

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)

    results = []
    exit_code = 0

    for package in packages:
        package_path = _get_package_path(importlib.import_module(package))
        symlink_path = os.path.join(ipylib_path, package)

        # Broken links return False on .exists(), so we need to check .islink() as well
        if os.path.islink(symlink_path) or os.path.exists(symlink_path):
            try:
                remove_symlink(symlink_path)
            except OSError:
                results.append((package, 'ERROR: Cannot remove symlink, try to run as administrator.'))

        try:
            create_symlink(package_path, symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot create symlink, try to run as administrator.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not install bootstrapper, try uninstalling first'))
    else:
        # Take either the CONDA environment directory or the current Python executable's directory
        python_directory = os.environ.get('CONDA_PREFIX', None) or os.path.dirname(sys.executable)
        environment_name = os.environ.get('CONDA_DEFAULT_ENV', '')
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')

        try:
            bootstrapper_data = _get_bootstrapper_data(compas_bootstrapper)
            installed_packages = bootstrapper_data.get('INSTALLED_PACKAGES', [])
            installed_packages = list(set(installed_packages + list(packages)))

            with open(compas_bootstrapper, 'w') as f:
                f.write('ENVIRONMENT_NAME = r"{}"\n'.format(environment_name))
                f.write('PYTHON_DIRECTORY = r"{}"\n'.format(python_directory))
                f.write('INSTALLED_PACKAGES = {}'.format(repr(installed_packages)))
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(('compas_bootstrapper', 'ERROR: Could not create compas_bootstrapper to auto-determine Python environment'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status is not 'OK':
            exit_code = -1

    print('\nCompleted.')
    sys.exit(exit_code)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', choices=['5.0', '6.0'], default='6.0', help="The version of Rhino to install the packages in.")
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to install.")

    args = parser.parse_args()

    install(version=args.version, packages=args.packages)
