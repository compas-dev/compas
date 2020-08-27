from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from System.Net import WebClient
from System.IO import MemoryStream

import clr
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")

import Rhino  # noqa: E402
import Rhino.UI  # noqa: E402

import Eto.Drawing  # noqa: E402
import Eto.Forms  # noqa: E402


__all__ = ['ImageForm']


def image_from_remote(source):
    """Construct an image from a remote source.

    Parameters
    ----------
    source : str
        The url of the remote source.

    Returns
    -------
    System.Drawing.Image
        Representation of an miage in memory.

    Examples
    --------
    .. code-block:: python

        image = image_from_remote('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')

    """
    w = WebClient()
    d = w.DownloadData(source)
    m = MemoryStream(d)
    return Eto.Drawing.Bitmap(m)


def image_from_local(source):
    """Construct an image from a local source.

    Parameters
    ----------
    source : str
        The path to the local source file.

    Returns
    -------
    System.Drawing.Image
        Representation of an miage in memory.

    Examples
    --------
    .. code-block:: python

        image = image_from_local('theblock.jpg')

    """
    return Eto.Drawing.Bitmap(source)


class ImageForm(Eto.Forms.Dialog[bool]):
    """Windows form for displaying images.

    Parameters
    ----------
    image : {str, Image}
        The image that should be displayed.
        This can be a url of a remote image file,
        or a local file path,
        or an instance of ``System.Drawing.Image``.
    title : str, optional
        Title of the form.
        Default is ``ImageForm``.
    width : int, optional
        Width of the form.
        Default is ``None``.
    height : int, optional
        Height of the form.
        Default is ``None``.

    Examples
    --------
    >>> from compas_rhino.forms import ImageForm
    >>> form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
    >>> form.show()

    """

    def __init__(self, image, title='Image', width=None, height=None):
        super(ImageForm, self).__init__(title, width, height)
        self._image = None
        self.image = image

        view = Eto.Forms.ImageView()
        view.Image = self.image
        self.Content = view

        # self.DefaultButton.Click += self.on_ok
        # self.AbortButton.Click += self.on_cancel

    @property
    def image(self):
        """Eto.Drawing.Image: An instance of ``Eto.Drawing.Image``.
        """
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, basestring):
            if image.startswith('http'):
                self._image = image_from_remote(image)
            else:
                self._image = image_from_local(image)
        elif isinstance(image, Eto.Drawing.Image):
            self._image = image
        else:
            raise NotImplementedError

    def on_ok(self, sender, e):
        pass

    def on_cancel(self, sender, e):
        pass

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
    form.show()
