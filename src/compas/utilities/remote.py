from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import io

import compas

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib2 import urlopen
    from urllib import urlretrieve

try:
    from PIL import Image
except ImportError:
    compas.raise_if_not_ironpython()



__all__ = []


def download_file_from_remote(source, target):
    """Download a file from a remote source and save it to a local destination.
    
    Parameters
    ----------
    source : str
        The url of the source file.
    target : str
        The path of the local destination.

    Examples
    --------
    .. code-block:: python

        from compas.utilities import download_image_from_remote

        source = 'https://raw.githubusercontent.com/compas-dev/compas/master/data/faces.obj'
        target = os.path.join(compas.APPDATA, 'data', 'faces.obj')

        download_file_from_remote(source, target)

    """
    parent = os.path.abspath(os.path.dirname(target))

    if not os.path.exists(parent):
        os.makedirs(parent)

    if not os.path.isdir(parent):
        raise Exception('The target path is not a valid file path: {}'.format(target))

    if not os.access(parent, os.W_OK):
        raise Exception('The target path is not writable: {}'.format(target))

    urlretrieve(source, target)


def download_image_from_remote(source, target, show=False):
    """Download an image from a remote source and save it to a local destination.

    Parameters
    ----------
    source : str
        The url of the source file.
    target : str
        The path of the local destination.
    show : bool, optional
        Show the downloaded image.
        Default is ``False``

    Examples
    --------
    .. code-block:: python

        from compas.utilities import download_image_from_remote

        source = 'http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg'
        target = os.path.join(compas.TEMP, 'theblock.jpg')

        download_image_from_remote(source, target, True)

    """
    # response = requests.get(source)
    # response.raise_for_status()    

    response = urlopen(source)
    image = Image.open(io.BytesIO(response.read()))

    if show:
        image.show()
    image.save(target)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # source = 'http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg'
    # target = os.path.join(compas.TEMP, 'theblock.jpg')

    # download_image_from_remote(source, target, True)

    filename = 'faces.obj'

    source = compas.get(filename)
    target = os.path.join(compas.APPDATA, 'data', filename)

    download_file_from_remote(source, target)
