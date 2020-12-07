from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os

from compas.files.gltf.gltf_exporter import GLTFExporter
from compas.files.gltf.gltf_parser import GLTFParser
from compas.files.gltf.gltf_reader import GLTFReader


class GLTF(object):
    """Read and create files in glTF format.

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Mesh, mesh_transformed
    from compas.utilities import download_file_from_remote
    from compas_viewers.multimeshviewer import MultiMeshViewer

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxInterleaved/glTF-Binary/BoxInterleaved.glb'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'BoxInterleaved.glb')

    download_file_from_remote(source_glb, filepath_glb, overwrite=False)

    gltf = GLTF(filepath_glb)
    gltf.read()

    default_scene = gltf.content.default_or_first_scene

    transformed_meshes = []

    for vertex_name, gltf_node in default_scene.nodes.items():
        if gltf_node.mesh_data is None:
            continue
        t = gltf_node.transform
        m = Mesh.from_vertices_and_faces(gltf_node.vertices, gltf_node.faces)
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
