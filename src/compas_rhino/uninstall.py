from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import compas_rhino
import compas_rhino.install

from compas._os import system
from compas._os import remove_symlinks


__all__ = ['uninstall']


def uninstall(version=None, packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to uninstall.
        Default is to uninstall all packages installed by the COMPAS installer.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.uninstall('6.0')

    .. code-block:: python

        $ python -m compas_rhino.uninstall -v 6.0

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    print('Uninstalling COMPAS packages from Rhino {0} IronPython lib:'.format(version))

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)

    compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
    bootstrapper_data = compas_rhino.install._get_bootstrapper_data(compas_bootstrapper)

    if not packages:
        try:
            packages = bootstrapper_data.get('INSTALLED_PACKAGES', None)
        except:  # noqa: E722
            pass

        # No info, fall back to installable packages list
        if packages is None:
            packages = compas_rhino.install.INSTALLABLE_PACKAGES

    environment_name = bootstrapper_data.get('ENVIRONMENT_NAME', '')
    if environment_name:
        print('Packages installed from environment: {}'.format(environment_name))

    results = []
    symlinks = []
    exit_code = 0

    for package in packages:
        symlinks.append(os.path.join(ipylib_path, package))

    removal_results = remove_symlinks(symlinks)

    for package, success in zip(packages, removal_results):
        result = 'OK' if success else 'ERROR: Cannot remove symlink, try to run as administrator.'
        results.append((package, result))

    if not all(removal_results):
        exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not uninstall bootstrapper.'))
    else:
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            if os.path.exists(compas_bootstrapper):
                os.remove(compas_bootstrapper)
                results.append(('compas_bootstrapper', 'OK'))
        except:  # noqa: E722
            results.append(('compas_bootstrapper', 'ERROR: Could not delete compas_bootstrapper'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status != 'OK':
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
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to uninstall.")

    args = parser.parse_args()

    uninstall(version=args.version, packages=args.packages)
