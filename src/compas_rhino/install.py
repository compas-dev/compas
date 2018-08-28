from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import compas
import compas_rhino


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def install(version='5.0'):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}
        The version number of Rhino.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.install('5.0')

    .. code-block:: python

        $ python -m compas_rhino.install 5.0

    """

    print('Installing COMPAS packages to Rhino IronPython lib:')

    base_path = os.path.abspath(os.path.join(
        os.path.dirname(compas.__file__), '..'))
    ipylib_path = compas_rhino.get_ironpython_lib_path(version)

    for package in ('compas', 'compas_ghpython', 'compas_rhino'):
        package_path = os.path.join(base_path, package)
        symlink_path = os.path.join(ipylib_path, package)

        if os.path.exists(symlink_path):
            raise Exception(
                'Package "{}" already found in Rhino lib, try uninstalling first'.format(package))

        try:
            compas_rhino.create_symlink(package_path, symlink_path)
            print('   {}: OK'.format(package))
        except OSError:
            raise Exception(
                'Cannot create symlink, try to run as administrator.')

    print('Completed.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import sys

    print('\nusage: python -m compas_rhino.install [version]\n')
    print('  version       Rhino version (5.0 or 6.0)\n')

    try:
        version = sys.argv[1]
    except IndexError:
        version = '5.0'
    else:
        try:
            version = str(version)
        except Exception:
            version = '5.0'

    install(version=version)
