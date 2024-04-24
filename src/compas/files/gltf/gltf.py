from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files.gltf.gltf_exporter import GLTFExporter
from compas.files.gltf.gltf_parser import GLTFParser
from compas.files.gltf.gltf_reader import GLTFReader


class GLTF(object):
    """Class for working with files in glTF format.

    Caution: Extensions and most other application specific data are unsupported,
    and their data may be lost upon import.

    Attributes
    ----------
    filepath : str
        Path to the location of the glTF file.
    content : :class:`compas.files.GLTFContent`
    reader : :class:`compas.files.GLTFReader`
    parser : :class:`compas.files.GLTFParser`
    exporter : :class:`compas.files.GLTFExporter`

    References
    ----------
    .. [1] https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """

    def __init__(self, filepath=None):
        self.filepath = filepath
        self._content = None

        self._is_parsed = False
        self._reader = None
        self._parser = None

        self._exporter = None

    def read(self):
        """Read the glTF located at :attr:`compas.files.GLTF.filepath` and load its content."""
        self._reader = GLTFReader(self.filepath)
        self._parser = GLTFParser(self._reader)
        self._is_parsed = True

        self._content = self._parser.content

    @property
    def reader(self):
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        if not self._is_parsed:
            self.read()
        return self._parser

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not self._is_parsed:
            self._is_parsed = True
        self._content = value

    @property
    def exporter(self):
        if not self._exporter:
            self._exporter = GLTFExporter(self.filepath, self.content)
        return self._exporter

    def export(self, embed_data=False):
        """Export the content of this :class:`compas.files.GLTF` to the location
        :attr:`compas.files.GLTF.filepath`, with file format determined by the given extension.

        Parameters
        ----------
        embed_data : bool
            When set to ``True``, mesh and other data will be embedded in the glTF,
            and no external binary file will be created.  The default value is ``False``.

        Returns
        -------

        """
        self.exporter.embed_data = embed_data
        self.exporter.export()
