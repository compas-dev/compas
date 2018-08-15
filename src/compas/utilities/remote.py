from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import io
import requests

from PIL import Image

import compas


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


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
    response = requests.get(source)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content))
    if show:
        image.show()
    image.save(target)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    source = 'http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg'
    target = os.path.join(compas.TEMP, 'theblock.jpg')

    download_image_from_remote(source, target, True)
