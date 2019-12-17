from __future__ import print_function
from __future__ import absolute_import


import numpy as np
from trimesh import load


__all__ = [
    'GLTF',
    'GLTFReader',
    'GLTFParser',
]


class GLTF(object):
    """Read and write files in glTF format.

    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath):
        self.reader = GLTFReader(filepath)
        self.parser = GLTFParser(self.reader)


class GLTFReader(object):
    """"Read the contents of a *glTF* file using the trimesh library.

    Parameters
    ----------
    filepath: str
        Path to the file.

    Attributes
    ----------
    scene : trimesh.Scene
        See https://trimsh.org/trimesh.html?highlight=load#trimesh.Scene

    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.scene = None
        self.read()

    def read(self):
        self.scene = load(self.filepath)


class GLTFParser(object):
    """Parse the contents of the reader to objects digestible by compas.

    Parameters
    ----------
    reader : GLTFReader

    Attributes
    ----------
    faces_and_vertices_dict : dict
        Dictionary with mesh names as keys and dictionaries containing vertex and face lists as values.
    root : str
        Name of the root vertex of the scene.
    scene_data : dict
        Dictionary containing vertex and edge (meta)data.
    """
    def __init__(self, reader):
        self.reader = reader
        self.faces_and_vertices_dict = {}
        self.root = None
        self.scene_data = None
        self.parse()

    def parse(self):
        geometries = self.reader.scene.geometry

        for name, trimesh in geometries.items():
            self.faces_and_vertices_dict[name] = {
                'vertices': trimesh.vertices,
                'faces': trimesh.faces,
            }

        edge_list = self.reader.scene.graph.to_edgelist()
        self.root = self.reader.scene.graph.base_frame

        vertex_coordinate_data = {self.root: [0, 0, 0]}
        vertex_data = {}
        edge_data = []

        while edge_list:
            parent, child, attributes = edge_list.pop(0)
            if parent not in vertex_coordinate_data:
                edge_list.append((parent, child, attributes))
                continue

            parent_vector = vertex_coordinate_data[parent]
            matrix = attributes['matrix']

            vertex_coordinate_data[child] = self._inhomogeneous_transformation(matrix, parent_vector)
            vertex_data[child] = attributes
            edge_data.append((parent, child))

        self.scene_data = {
            'vertex_data': vertex_data,  # {child_name: {'matrix': transformation matrix from parent to child, 'geometry': mesh name, 'time': timestamp}}
            'vertices': vertex_coordinate_data,  # {vertex_name: [x, y, z]]}
            'edges': edge_data,  # [(parent_name, child_name])
        }

    def _inhomogeneous_transformation(self, matrix, vector):
        transformation_matrix = np.array(matrix)
        embedded_vector = np.array(self._embed_vector(vector))

        embedded_result = transformation_matrix.dot(embedded_vector)

        return list(self._pullback_vector(embedded_result))

    def _embed_vector(self, vector):
        return vector + [1.0]

    def _pullback_vector(self, vector):
        return vector[:3]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import os
    import compas

    from compas.datastructures import Mesh, Network
    # from compas_viewers import MultiMeshViewer
    from compas.utilities import download_file_from_remote

    source_gltf = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy.gltf'
    source_bin = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy0.bin'
    filepath_gltf = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy.gltf')
    filepath_bin = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy0.bin')

    download_file_from_remote(source_gltf, filepath_gltf, overwrite=False)
    download_file_from_remote(source_bin, filepath_bin, overwrite=False)

    gltf = GLTF(filepath_gltf)

    meshes = {
        name: Mesh.from_vertices_and_faces(data['vertices'], data['faces'])
        for name, data in gltf.parser.faces_and_vertices_dict.items()
    }

    for name in meshes:
        meshes[name].name = name

    scene_tree = Network.from_vertices_and_edges(gltf.parser.scene_data['vertices'], gltf.parser.scene_data['edges'])
    scene_tree.plot()

    # Usage of MultiMeshViewer unclear
    # viewer = MultiMeshViewer()
    # viewer.meshes = meshes.values()
    # viewer.show()
