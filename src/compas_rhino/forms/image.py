from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.forms import Form

try:
    from System.Windows.Forms import PictureBox
    from System.Windows.Forms import PictureBoxSizeMode
    from System.Windows.Forms import DockStyle
    from System.Drawing import Image
    from System.Net import WebClient
    from System.IO import MemoryStream

except ImportError:
    if compas.is_ironpython() and compas.is_windows():
        raise

try:
    basestring
except NameError:
    basestring = str


__all__ = ['ImageForm', 'image_from_remote', 'image_from_local']


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
    return Image.FromStream(m)


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
    return Image.FromFile(source)


class ImageForm(Form):
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
    .. code-block:: python

        from compas_rhino.forms import ImageForm

        form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
        form.show()

    """

    def __init__(self, image, title='ImageForm', width=None, height=None):
        self._image = None
        self.image = image
        super(ImageForm, self).__init__(title, width, height)

    @property
    def image(self):
        """System.Drawing.Image: An instance of ``System.Drawing.Image``.
        """
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, basestring):
            if image.startswith('http'):
                self._image = image_from_remote(image)
            else:
                self._image = image_from_local(image)
        elif isinstance(image, Image):
            self._image = image
        else:
            raise NotImplementedError

    def init(self):
        box = PictureBox()
        box.Dock = DockStyle.Fill
        box.SizeMode = PictureBoxSizeMode.AutoSize
        box.Image = self.image
        self.image = box.Image
        self.Controls.Add(box)
        self.ClientSize = box.Size

    def on_form_closed(self, sender, e):
        self.image.Dispose()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
    form.show()
