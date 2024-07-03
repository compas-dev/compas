from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def download_file_from_remote(source, target, overwrite=True):
    """Download a file from a remote source and save it to a local destination.

    Parameters
    ----------
    source : str
        The url of the source file.
    target : str
        The path of the local destination.
    overwrite : bool, optional
        If True, overwrite `target` if it already exists.

    Examples
    --------
    .. code-block:: python

        import os
        import compas
        from compas.utilities.remote import download_file_from_remote

        source = "https://raw.githubusercontent.com/compas-dev/compas/main/data/faces.obj"
        target = os.path.join(compas.APPDATA, "data", "faces.obj")

        download_file_from_remote(source, target)

    """
    parent = os.path.abspath(os.path.dirname(target))

    if not os.path.exists(parent):
        os.makedirs(parent)

    if not os.path.isdir(parent):
        raise Exception("The target path is not a valid file path: {}".format(target))

    if not os.access(parent, os.W_OK):
        raise Exception("The target path is not writable: {}".format(target))

    if not os.path.exists(target):
        urlretrieve(source, target)
    else:
        if overwrite:
            urlretrieve(source, target)
