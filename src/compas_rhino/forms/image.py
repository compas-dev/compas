from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from compas_rhino.forms.base import BaseForm

from System.Windows.Forms import PictureBox
from System.Windows.Forms import PictureBoxSizeMode
from System.Windows.Forms import DockStyle
from System.Drawing import Image
from System.Net import WebClient
from System.IO import MemoryStream


__all__ = ["ImageForm", "image_from_remote", "image_from_local"]


def image_from_remote(source):
    """Construct an image from a remote source.

    Parameters
    ----------
    source : str
        The url of the remote source.

    Returns
    -------
    System.Drawing.Image
        Representation of an image in memory.

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
        Representation of an image in memory.

    Examples
    --------
    .. code-block:: python

        image = image_from_local('theblock.jpg')

    """
    return Image.FromFile(source)


class ImageForm(BaseForm):
    """A form for displaying images.

    Parameters
    ----------
    image : str | Image
        The image that should be displayed.
        This can be a url of a remote image file,
        or a local file path,
        or an instance of `System.Drawing.Image`.
    title : str, optional
        Title of the form.
    width : int, optional
        Width of the form.
    height : int, optional
        Height of the form.

    Attributes
    ----------
    image : System.Drawing.Image
        The image displayed by the form.

    Examples
    --------
    .. code-block:: python

        from compas_rhino.forms import ImageForm

        form = ImageForm('http://block.arch.ethz.ch/brg/images/cache/dsc02360_ni-2_cropped_1528706473_624x351.jpg')
        form.show()

    """

    def __init__(self, image, title="Image", width=None, height=None):
        self._image = None
        self.image = image
        super(ImageForm, self).__init__(title, width, height)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, basestring):
            if image.startswith("http"):
                self._image = image_from_remote(image)
            else:
                self._image = image_from_local(image)
        elif isinstance(image, Image):
            self._image = image
        else:
            raise NotImplementedError

    def init(self):
        """Initialize the form.

        Returns
        -------
        None

        """
        box = PictureBox()
        box.Dock = DockStyle.Fill
        box.SizeMode = PictureBoxSizeMode.AutoSize
        box.Image = self.image
        self.image = box.Image
        self.Controls.Add(box)
        self.ClientSize = box.Size

    def on_form_closed(self, sender, e):
        """Callback for the closing event of the form.

        Parameters
        ----------
        sender : System.Object
            The sender object.
        eargs : System.Object.EventArgs
            The event arguments.

        Returns
        -------
        None

        """
        self.image.Dispose()
