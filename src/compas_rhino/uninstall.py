from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import os
import sys

import compas_rhino
from compas_rhino.install import installable_rhino_packages

import compas._os

__all__ = ['uninstall']


def uninstall(version=None, packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0', '7.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to uninstall.
        Default is to uninstall all packages installed by the COMPAS installer.

    Examples
    --------
    .. code-block:: python

        import compas_rhino
        compas_rhino.uninstall('6.0')

    .. code-block:: bash

        python -m compas_rhino.uninstall -v 6.0

    """
    if version not in ('5.0', '6.0', '7.0'):
        version = '6.0'

    packages = _filter_installed_packages(version, packages)

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)
    scripts_path = compas_rhino._get_scripts_path(version)

    print('Uninstalling COMPAS packages from Rhino {0} scripts folder:'.format(version))
    print('Location scripts folder: {}'.format(scripts_path))
    print()

    print('The following packages have been detected and will be uninstalled:')

    results = []
    symlinks_to_uninstall = []
    exit_code = 0

    for package in packages:
        symlink_path = os.path.join(scripts_path, package)
        if os.path.exists(symlink_path):
            symlinks_to_uninstall.append(dict(name=package, link=symlink_path))

        legacy_path = os.path.join(ipylib_path, package)
        if os.path.exists(legacy_path):
            symlinks_to_uninstall.append(dict(name=package, link=legacy_path))

    symlinks = [link['link'] for link in symlinks_to_uninstall]
    uninstall_results = compas._os.remove_symlinks(symlinks)

    for uninstall_data, success in zip(symlinks_to_uninstall, uninstall_results):
        result = 'OK' if success else 'ERROR: Cannot remove symlink, try to run as administrator.'
        results.append((uninstall_data['name'], result))

    if not all(uninstall_results):
        exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not uninstall bootstrapper.'))
    else:
        if compas_rhino._try_remove_bootstrapper(scripts_path):
            results.append(('compas_bootstrapper', 'OK'))
        else:
            results.append(('compas_bootstrapper', 'ERROR: Cannot remove compas_bootstrapper, try to run as administrator.'))

        if not compas_rhino._try_remove_bootstrapper(ipylib_path):
            results.append(('compas_bootstrapper', 'ERROR: Cannot remove legacy compas_bootstrapper, try to run as administrator.'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status != 'OK':
            exit_code = -1

    print('\nUninstall completed.')
    if exit_code != 0:
        sys.exit(exit_code)


def _filter_installed_packages(version, packages):
    ipylib_path = compas_rhino._get_ironpython_lib_path(version)
    scripts_path = compas_rhino._get_scripts_path(version)

    compas_bootstrapper = compas_rhino._get_bootstrapper_path(scripts_path)
    bootstrapper_data = compas_rhino._get_bootstrapper_data(compas_bootstrapper)

    # Don't modify the original list if we have one
    if packages:
        packages = packages[:]
    else:
        packages = bootstrapper_data.get('INSTALLED_PACKAGES', None)

        # No info, fall back to installable packages list
        if packages is None:
            packages = list(itertools.chain.from_iterable(installable_rhino_packages()))

    # Handle legacy install
    legacy_bootstrapper = compas_rhino._get_bootstrapper_path(ipylib_path)
    if os.path.exists(legacy_bootstrapper):
        bootstrapper_data = compas_rhino._get_bootstrapper_data(legacy_bootstrapper)
        legacy_packages = bootstrapper_data.get('INSTALLED_PACKAGES', None)

        if legacy_packages:
            packages.extend(legacy_packages)

    return packages


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', choices=['5.0', '6.0', '7.0'], default='6.0', help="The version of Rhino to install the packages in.")
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to uninstall.")

    args = parser.parse_args()

    uninstall(version=args.version, packages=args.packages)
