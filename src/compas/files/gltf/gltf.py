from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os

from compas.files.gltf.gltf_content import GLTFContent
from compas.files.gltf.gltf_exporter import GLTFExporter
from compas.files.gltf.gltf_parser import GLTFParser
from compas.files.gltf.gltf_reader import GLTFReader


class GLTF(object):
    """Read files in glTF format.
    Caution: Extensions and most other application specific data are unsupported,
    and their data may be lost upon import.
    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath=None):
        self.filepath = filepath
        self._content = None

        self._is_parsed = False
        self._reader = None
        self._parser = None

        self._exporter = None

    def read(self):
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
        if not isinstance(value, GLTFContent):
            raise Exception('Object of type GLTFContent expected.')
        if not self._is_parsed:
            self._is_parsed = True
        self._content = value

    @property
    def exporter(self):
        if not self._exporter:
            self._exporter = GLTFExporter(self.filepath, self.content)
        return self._exporter

    def export(self, embed_data=False):
        self.exporter.embed_data = embed_data
        self.content.remove_orphans()  # don't know where this should be called
        self.content.check_is_forest()
        self.exporter.export()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Mesh, Network, mesh_transformed
    from compas.utilities import download_file_from_remote
    from compas_viewers.multimeshviewer import MultiMeshViewer

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxInterleaved/glTF-Binary/BoxInterleaved.glb'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'BoxInterleaved.glb')

    download_file_from_remote(source_glb, filepath_glb, overwrite=False)

    gltf = GLTF(filepath_glb)
    gltf.read()

    default_scene_index = gltf.content.default_scene_index or 0
    nodes = gltf.content.scenes[default_scene_index].nodes

    # change these to the new functions
    nds = {name: gltf_node.position for name, gltf_node in nodes.items()}
    edges = [
        (node.key, child)
        for node in gltf.content.scenes[default_scene_index].nodes.values()
        for child in node.children
    ]

    scene_tree = Network.from_nodes_and_edges(nds, edges)  # !!!
    scene_tree.plot()

    transformed_meshes = []

    for vertex_name, gltf_node in nodes.items():
        if gltf_node.mesh_data is None:
            continue
        t = gltf_node.transform
        m = Mesh.from_vertices_and_faces(gltf_node.mesh_data.vertices, gltf_node.mesh_data.faces)
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
