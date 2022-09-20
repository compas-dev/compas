from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

# import io

# import compas

try:
    # from urllib.request import urlopen
    from urllib.request import urlretrieve
except ImportError:
    # from urllib2 import urlopen
    from urllib import urlretrieve

# try:
#     from PIL import Image
# except ImportError:
#     if compas.is_windows():
#         compas.raise_if_not_ironpython()
#     elif not compas.is_mono():
#         raise


__all__ = ["download_file_from_remote"]


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

        source = 'https://raw.githubusercontent.com/compas-dev/compas/main/data/faces.obj'
        target = os.path.join(compas.APPDATA, 'data', 'faces.obj')

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


# def download_image_from_remote(source, target, show=False):
#     """Download an image from a remote source and save it to a local destination.

#     Parameters
#     ----------
#     source : str
#         The url of the source file.
#     target : str
#         The path of the local destination.
#     show : bool, optional
#         Show the downloaded image.
#         Default is ``False``

#     Examples
#     --------
#     .. code-block:: python

#         import os
#         import compas
#         from compas.utilities.remote import download_image_from_remote

#         source = 'http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg'
#         target = os.path.join(compas.APPDATA, 'data', 'theblock.jpg')

#         download_image_from_remote(source, target, show=True)

#     """
#     # response = requests.get(source)
#     # response.raise_for_status()

#     response = urlopen(source)
#     image = Image.open(io.BytesIO(response.read()))

#     if show:
#         image.show()
#     image.save(target)
