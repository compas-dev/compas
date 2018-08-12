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

except ImportError:
    compas.raise_if_ironpython()


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['ImageForm', ]


class ImageForm(Form):
    """"""

    def __init__(self, imagepath, title='ImageForm', width=None, height=None):
        self.imagepath = imagepath
        super(ImageForm, self).__init__(title, width, height)

    def init(self):
        box = PictureBox()
        box.Dock = DockStyle.Fill
        box.SizeMode = PictureBoxSizeMode.AutoSize
        box.Image = Image.FromFile(self.imagepath)
        self.image = box.Image
        self.Controls.Add(box)
        self.ClientSize = box.Size

    def on_form_closed(self, sender, e):
        self.image.Dispose()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    form = ImageForm('../../../docs/source/_images/smoothing_01.jpg')
    form.show()
