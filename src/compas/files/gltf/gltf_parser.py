from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.data_classes import AnimationData
from compas.files.gltf.data_classes import AnimationSamplerData
from compas.files.gltf.data_classes import CameraData
from compas.files.gltf.data_classes import ChannelData
from compas.files.gltf.data_classes import MaterialData
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.data_classes import SamplerData
from compas.files.gltf.data_classes import SkinData
from compas.files.gltf.data_classes import TextureData
from compas.files.gltf.gltf_content import GLTFContent
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene


class GLTFParser(object):
    """Parse the contents of the reader into a :class:`compas.files.GLTFContent` object.

    Parameters
    ----------
    reader : :class:`compas.files.GLTFReader`

    Attributes
    ----------
    reader : :class:`compas.files.GLTFReader`
    content : :class:`compas.files.GLTFContent`
    """
    def __init__(self, reader):
        self.reader = reader
        self.content = GLTFContent()

        self.parse()

    def parse(self):
        self.content.default_scene_key = self._get_default_scene()
        self.content.extras = self._get_extras()
        self.content.extensions = self._get_extensions()

        self.content.images = {key: image_data for key, image_data in enumerate(self.reader.image_data)}
        self.content.samplers = {key: SamplerData.from_data(sampler) for key, sampler in enumerate(self.reader.json.get('samplers', []))}
        self.content.textures = {key: TextureData.from_data(texture) for key, texture in enumerate(self.reader.json.get('textures', []))}
        self.content.materials = {key: MaterialData.from_data(material) for key, material in enumerate(self.reader.json.get('materials', []))}
        self.content.cameras = {key: CameraData.from_data(camera) for key, camera in enumerate(self.reader.json.get('cameras', []))}
        self.content.skins = {key: SkinData.from_data(skin, self.reader.data[skin['inverseBindMatrices']]) for key, skin in enumerate(self.reader.json.get('skins', []))}
        self.content.animations = {key: self._get_animation_data(animation) for key, animation in enumerate(self.reader.json.get('animations', []))}

        for mesh in self.reader.json.get('meshes', []):
            self._add_gltf_mesh(mesh)
        for node in self.reader.json.get('nodes', []):
            self._add_gltf_node(node)
        for scene in self.reader.json.get('scenes', []):
            self._add_gltf_scene(scene)

        self.content.update_node_transforms_and_positions()

    def _get_animation_data(self, animation):
        sampler_data_dict = {}
        for index, sampler in enumerate(animation['samplers']):
            input_ = self.reader.data[sampler['input']]
            output = self.reader.data[sampler['output']]
            sampler_data_dict[index] = AnimationSamplerData.from_data(sampler, input_, output)
        channel_data_list = [ChannelData.from_data(channel) for channel in animation['channels']]
        return AnimationData.from_data(animation, channel_data_list, sampler_data_dict)

    def _get_extras(self):
        return self.reader.json.get('extras')

    def _get_default_scene(self):
        return self.reader.json.get('scene')

    def _get_extensions(self):
        return self.reader.json.get('extensions')

    def _add_gltf_scene(self, scene):
        GLTFScene.from_data(scene, self.content)

    def _add_gltf_node(self, node):
        GLTFNode.from_data(node, self.content)

    def _add_gltf_mesh(self, mesh):
        primitive_data_list = []
        for primitive in mesh['primitives']:
            if 'POSITION' not in primitive['attributes']:
                continue

            attributes = {}
            for attr, attr_accessor_index in primitive['attributes'].items():
                attributes[attr] = self.reader.data[attr_accessor_index]

            indices = self._get_indices(primitive, len(attributes['POSITION']))

            target_list = []
            for target in primitive.get('targets', []):
                target_data = {attr: self.reader.data[accessor_index] for attr, accessor_index in target.items()}
                target_list.append(target_data)

            primitive_data = PrimitiveData.from_data(primitive, attributes, indices, target_list)

            primitive_data_list.append(primitive_data)

        GLTFMesh.from_data(mesh, self.content, primitive_data_list)

    def _get_indices(self, primitive, num_vertices):
        if 'indices' not in primitive:
            return self.get_generic_indices(num_vertices)
        indices_accessor_index = primitive['indices']
        return self.reader.data[indices_accessor_index]

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))
