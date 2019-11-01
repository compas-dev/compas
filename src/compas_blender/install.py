from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

# from compas._os import system
from compas._os import remove_symlink
from compas._os import create_symlink


__all__ = ['install']


def install(blenderpath):
    """Install COMPAS for Blender.

    Parameters
    ----------
    blenderpath : str
        The path to the folder with the version number of Blender.
        For example, on Mac: `'/Applications/blender.app/Contents/Resources/2.80'`.
        On Windows: `'%PROGRAMFILES%\\Blender Foundation\\Blender\\2.80'`.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_blender.install /Applications/blender.app/Contents/Resources/2.80

    """

    version = os.path.split(blenderpath)

    print('Installing COMPAS for Blender {}.'.format(version))

    startup = os.path.join(blenderpath, 'scripts', 'startup')
    exit_code = 0

    sys_version = "\\n".join(sys.version.split("\n"))

    blenderpython_src = os.path.join(blenderpath, 'python')
    blenderpython_dst = os.path.join(blenderpath, 'original_python')
    compas_bootstrapper = os.path.join(startup, 'compas_bootstrapper.py')

    if os.path.exists(blenderpython_dst):
        if os.path.exists(blenderpython_src):
            remove_symlink(blenderpython_src)
        os.rename(blenderpython_dst, blenderpython_src)

    if os.path.exists(compas_bootstrapper):
        os.unlink(compas_bootstrapper)

    try:
        os.rename(blenderpython_src, blenderpython_dst)
        create_symlink(os.environ['CONDA_PREFIX'], 'python')

        with open(compas_bootstrapper, 'w') as f:
            f.write('import sys\n')
            f.write('sys.version = \'{}\'\n'.format(sys_version))

    except Exception:
        print("\nInstalling COMPAS for Blender {} failed.".format(version))
        exit_code = -1

    else:
        print("\nCOMPAS will be available in Blender {} after restarting.".format(version))

    sys.exit(exit_code)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('versionpath', help="The path to the folder with the version number of Blender.")
    args = parser.parse_args()

    install(args.versionpath)
