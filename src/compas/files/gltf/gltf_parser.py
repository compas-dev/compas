from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.data_classes import MeshData
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.gltf_content import GLTFContent
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_matrix_from_col_major_list


class GLTFParser(object):
    """Parse the contents of the reader and create objects digestible by COMPAS.

    Parameters
    ----------
    reader : :class:`compas.files.GLTFReader`

    Attributes
    ----------
    reader : :class:`compas.files.GLTFReader`
    default_scene_index : int
        Index of the default scene.
    scenes : list of :class:`compas.files.GLTFScene`
        List of dictionaries containing the information of each scene.
    extras : object
    """
    def __init__(self, reader):
        self.reader = reader
        self.default_scene_index = None
        self.content = GLTFContent()

        self.parse()

        ancillaries = {
            attr: self.reader.json.get(attr)
            for attr in ['cameras', 'materials', 'textures', 'samplers']
            if self.reader.json.get(attr)
        }
        ancillaries.update({
            'images': self.reader.image_data,
            'skins': self.reader.skin_data,
            'animations': self.reader.animation_data,
        })

        self.content.ancillaries = ancillaries

    def parse(self):
        self.default_scene_index = self.get_default_scene()
        self.content.extras = self.get_extras()

        # should make dictionaries for everything
        # then the remove orphans method would cull unused cameras, etc...
        self.content.scenes = [self.get_scene(scene, key) for key, scene in enumerate(self.reader.json.get('scenes', []))]
        self.content.meshes = {key: self.get_mesh_data(mesh, key) for key, mesh in enumerate(self.reader.json.get('meshes', []))}
        self.content.nodes = {key: self.get_gltf_node(node, key) for key, node in enumerate(self.reader.json.get('nodes', []))}

    def get_extras(self):
        return self.reader.json.get('extras')

    def get_default_scene(self):
        return self.reader.json.get('scene')

    def get_scene(self, scene, key):
        scene_obj = GLTFScene(self.content)
        scene_obj.name = scene.get('name')
        scene_obj.extras = scene.get('extras')
        scene_obj.nodes = scene.get('nodes', [])
        scene_obj.key = key

        return scene_obj

    def get_gltf_node(self, node, key):
        gltf_node = GLTFNode(self.content)
        gltf_node.name = node.get('name')
        gltf_node.children = node.get('children', [])
        gltf_node.translation = node.get('translation')
        gltf_node.rotation = node.get('rotation')
        gltf_node.scale = node.get('scale')
        gltf_node.matrix = self.get_matrix(node)
        gltf_node.weights = node.get('weights')
        gltf_node.mesh_key = node.get('mesh')
        gltf_node.camera = node.get('camera')
        gltf_node.skin = node.get('skin')
        gltf_node.extras = node.get('extras')
        gltf_node.key = key
        return gltf_node

    def get_matrix(self, node):
        if 'matrix' in node:
            return get_matrix_from_col_major_list(node['matrix'])
        return None

    def get_mesh_data(self, mesh, key):
        mesh_name = mesh.get('name')
        extras = mesh.get('extras')
        primitives = mesh['primitives']
        weights = mesh.get('weights')


        primitive_data_list = []

        for primitive in primitives:
            if 'POSITION' not in primitive['attributes']:
                continue

            attributes = {}
            for attr, attr_accessor_index in primitive['attributes'].items():
                attributes[attr] = self.reader.data[attr_accessor_index]

            indices = self.get_indices(primitive, len(attributes['POSITION']))

            target_list = []
            for target in primitive.get('targets', []):
                target_data = {attr: self.reader.data[accessor_index] for attr, accessor_index in target.items()}
                target_list.append(target_data)

            primitive_data_list.append(PrimitiveData(
                attributes,
                indices,
                primitive.get('material'),
                primitive.get('mode'),
                target_list,
                primitive.get('extras'),
            ))

        return MeshData(primitive_data_list, key, mesh_name, weights, extras)

    def get_indices(self, primitive, num_vertices):
        if 'indices' not in primitive:
            return self.get_generic_indices(num_vertices)
        indices_accessor_index = primitive['indices']
        return self.reader.data[indices_accessor_index]

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))
