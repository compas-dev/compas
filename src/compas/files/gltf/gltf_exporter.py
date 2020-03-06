from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import base64
import json
import os
import struct

from compas.files.gltf.constants import COMPONENT_TYPE_ENUM
from compas.files.gltf.constants import COMPONENT_TYPE_FLOAT
from compas.files.gltf.constants import COMPONENT_TYPE_UNSIGNED_INT
from compas.files.gltf.constants import NUM_COMPONENTS_BY_TYPE_ENUM
from compas.files.gltf.constants import TYPE_MAT4
from compas.files.gltf.constants import TYPE_SCALAR
from compas.files.gltf.constants import TYPE_VEC2
from compas.files.gltf.constants import TYPE_VEC3
from compas.files.gltf.constants import TYPE_VEC4
from compas.files.gltf.helpers import matrix_to_col_major_order
from compas.geometry import identity_matrix


class GLTFExporter(object):
    """Export a glTF or glb file based on the supplied scene and ancillary data.
    Parameters
    ----------
    filepath : str
        Location where the glTF or glb is to be written. The extension of the filepath
        determines which format will be used. If there is an accompanying binary file,
        it will be written in the same directory.
    content : :class:`compas.files.GLTFContent`
    embed_data : bool
        When True, all mesh and other data will be embedded as data uri's in the glTF json.
        When False, the data will be written to an external binary file or chunk.
    """

    def __init__(self, filepath, content, embed_data=False):
        self.gltf_filepath = filepath
        self._dirname = None
        self._filename = None
        self._ext = None

        self.embed_data = embed_data
        self._content = content

        self._gltf_dict = self.get_generic_gltf_dict()
        self._mesh_index_by_key = {key: index for index, key in enumerate(self._content.meshes.keys())}
        self._node_index_by_key = {key: index for index, key in enumerate(self._content.nodes.keys())}
        self._buffer = b''

        self.load()

    def load(self):
        self.set_path_attributes()
        # self.validate_scenes()
        self.add_meshes()
        self.add_nodes()
        self.add_scenes()
        self.add_ancillaries()
        self.add_buffer()

    def export(self):
        gltf_json = json.dumps(self._gltf_dict, indent=4)

        if self._ext == '.gltf':
            with open(self.gltf_filepath, 'w') as f:
                f.write(gltf_json)
            if not self.embed_data and len(self._buffer) > 0:
                with open(self.get_bin_path(), 'wb') as f:
                    f.write(self._buffer)

        if self._ext == '.glb':
            with open(self.gltf_filepath, 'wb') as f:
                gltf_data = gltf_json.encode()

                length_gltf = len(gltf_data)
                spaces_gltf = (4 - (length_gltf & 3)) & 3
                length_gltf += spaces_gltf

                length_bin = len(self._buffer)
                zeros_bin = (4 - (length_bin & 3)) & 3
                length_bin += zeros_bin

                length = 12 + 8 + length_gltf
                if length_bin > 0:
                    length += 8 + length_bin

                f.write('glTF'.encode('ascii'))
                f.write(struct.pack('<I', 2))
                f.write(struct.pack('<I', length))

                f.write(struct.pack('<I', length_gltf))
                f.write('JSON'.encode('ascii'))
                f.write(gltf_data)
                for i in range(0, spaces_gltf):
                    f.write(' '.encode())

                if length_bin > 0:
                    f.write(struct.pack('<I', length_bin))
                    f.write('BIN\0'.encode())
                    f.write(self._buffer)
                    for i in range(0, zeros_bin):
                        f.write('\0'.encode())

    def add_meshes(self):
        # list comprehension would be enough for later versions of python
        mesh_list = [None] * len(self._content.meshes.values())
        for key, mesh_data in self._content.meshes.items():
            mesh_list[self._mesh_index_by_key[key]] = self.get_mesh_dict(mesh_data)
        self._gltf_dict['meshes'] = mesh_list

    def get_mesh_dict(self, mesh_data):
        mesh_dict = {'primitives': self.get_primitives(mesh_data)}
        if mesh_data.mesh_name:
            mesh_dict['name'] = mesh_data.mesh_name
        if mesh_data.weights:
            mesh_dict['weights'] = mesh_data.weights
        if mesh_data.extras and self.is_jsonable(mesh_data.extras, 'mesh extras object'):
            mesh_dict['extras'] = mesh_data.extras
        return mesh_dict

    def add_buffer(self):
        buffer = {'byteLength': len(self._buffer)}
        if self.embed_data:
            buffer['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(self._buffer).decode('ascii')
        elif self._ext == '.gltf':
            buffer['uri'] = self.get_bin_filename()
        self._gltf_dict['buffers'] = [buffer]

    def add_ancillaries(self):
        for attr in ['cameras', 'materials', 'textures', 'samplers']:
            if not self._content.ancillaries.get(attr):
                continue
            if self.is_jsonable(self._content.ancillaries[attr], '{} list'.format(attr)):
                self._gltf_dict[attr] = self._content.ancillaries[attr]

        images_list = self.get_images_list()
        if images_list:
            self._gltf_dict['images'] = images_list

        skins_list = self.get_skins_list()
        if skins_list:
            self._gltf_dict['skins'] = skins_list

        animations_list = self.get_animations_list()
        if animations_list:
            self._gltf_dict['animations'] = animations_list

    def get_images_list(self):
        return [self.get_image_dict(image_data) for image_data in self._content.ancillaries.get('images', [])]

    def get_image_dict(self, image_data):
        image_dict = {}
        if image_data.name:
            image_dict['name'] = image_data.name
        if image_data.extras:
            image_dict['extras'] = image_data.extras
        if image_data.mime_type:
            image_dict['mimeType'] = image_data.mime_type
        if image_data.uri:
            image_dict['uri'] = image_data.uri
        if image_data.data and self.embed_data:
            image_dict['uri'] = self.get_image_data_uri(image_data)
        if image_data.data and not self.embed_data:
            image_dict['bufferView'] = self.get_buffer_view(image_data.data)
        return image_dict

    def get_image_data_uri(self, image_data):
        return (
            'data:'
            + (image_data.media_type if image_data.media_type else '')
            + ';base64,' + base64.b64encode(image_data.data).decode('ascii')
        )

    def get_skins_list(self):
        return [self.get_skin_dict(skin_data) for skin_data in self._content.ancillaries.get('skins', [])]

    def get_skin_dict(self, skin_data):
        skin_dict = {'joints': [
            self._node_index_by_key.get(item)
            for item in skin_data.joints
            if self._node_index_by_key.get(item)
        ]}
        if skin_data.skeleton:
            skin_dict['skeleton'] = skin_data.skeleton
        if skin_data.name:
            skin_dict['name'] = skin_data.name
        if skin_data.extras:
            skin_dict['extras'] = skin_data.extras
        if skin_data.inverse_bind_matrices:
            skin_dict['inverseBindMatrices'] = self.get_accessor(skin_data.inverse_bind_matrices, COMPONENT_TYPE_FLOAT, TYPE_MAT4)
        return skin_dict

    def get_animations_list(self):
        return [self.get_animation_dict(animation_data) for animation_data in self._content.ancillaries.get('animations', [])]

    def get_animation_dict(self, animation_data):
        animation_dict = {
            'channels': animation_data.channels,
            'samplers': self.get_samplers_list(animation_data)
        }
        if animation_data.name:
            animation_dict['name'] = animation_data.name
        if animation_data.extras:
            animation_dict['extras'] = animation_data.extras
        return animation_dict

    def get_samplers_list(self, animation_data):
        return [self.get_sampler_dict(sampler_data) for sampler_data in animation_data.samplers]

    def get_sampler_dict(self, sampler_data):
        input_accessor = self.get_accessor(sampler_data.input, COMPONENT_TYPE_FLOAT, TYPE_SCALAR, include_bounds=True)
        type_ = TYPE_VEC3
        if isinstance(sampler_data.output[0], int) or isinstance(sampler_data.output[0], float):
            type_ = TYPE_SCALAR
        elif len(sampler_data.output[0]) == 4:
            type_ = TYPE_VEC4
        output_accessor = self.get_accessor(sampler_data.output, COMPONENT_TYPE_FLOAT, type_)
        sampler_dict = {
            'input': input_accessor,
            'output': output_accessor,
        }
        if sampler_data.interpolation:
            sampler_dict['interpolation'] = sampler_data.interpolation
        if sampler_data.extras:
            sampler_dict['extras'] = sampler_data.extras
        return sampler_dict

    def is_jsonable(self, obj, obj_name):
        try:
            json.dumps(obj)
        except (TypeError, OverflowError):
            raise Exception('The {} is not a valid JSON object.'.format(obj_name))
        return True

    def get_generic_gltf_dict(self):
        asset_dict = {'version': '2.0'}
        gltf_dict = {'asset': asset_dict}
        if self._content.extras:
            gltf_dict['extras'] = self._content.extras
        return gltf_dict

    def add_scenes(self):
        if not self._content.scenes:
            return
        if self._content.default_scene_index is not None:
            self._gltf_dict['scene'] = self._content.default_scene_index
        self._gltf_dict['scenes'] = [self.get_scene_dict(gltf_scene) for gltf_scene in self._content.scenes]

    def get_scene_dict(self, gltf_scene):
        scene_dict = {}
        if gltf_scene.nodes:
            scene_dict['nodes'] = [self._node_index_by_key[key] for key in gltf_scene.nodes]
        if gltf_scene.name:
            scene_dict['name'] = gltf_scene.name
        if gltf_scene.extras:
            scene_dict['extras'] = gltf_scene.extras
        return scene_dict

    def add_nodes(self):
        # list comprehension would be enough for later versions of python
        node_list = [None] * len(self._content.nodes.values())
        for key, node in self._content.nodes.items():
            node_list[self._node_index_by_key[key]] = self.get_node_dict(node)
        self._gltf_dict['nodes'] = node_list

    def get_node_dict(self, node):
        node_dict = {}
        if node.name:
            node_dict['name'] = node.name
        if node.children:
            node_dict['children'] = [self._node_index_by_key[key] for key in node.children]
        if node.matrix and node.matrix != identity_matrix(4):
            node_dict['matrix'] = matrix_to_col_major_order(node.matrix)
        else:
            if node.translation:
                node_dict['translation'] = node.translation
            if node.rotation:
                node_dict['rotation'] = node.rotation
            if node.scale:
                node_dict['scale'] = node.scale
        if node.mesh_key is not None:
            node_dict['mesh'] = self._mesh_index_by_key[node.mesh_key]
        if node.camera is not None and self.camera_exists(node.camera):
            node_dict['camera'] = node.camera
        if node.skin is not None and self.skin_exists(node.skin):
            node_dict['skin'] = node.skin
        if node.extras:
            node_dict['extras'] = node.extras
        return node_dict

    def camera_exists(self, index):
        return 0 <= index < len(self._content.ancillaries.get('cameras', []))

    def skin_exists(self, index):
        return 0 <= index < len(self._content.ancillaries.get('skins', []))

    def material_exists(self, index):
        return 0 <= index < len(self._content.ancillaries.get('materials', []))

    def get_primitives(self, mesh_data):
        primitives = []
        for primitive_data in mesh_data.primitive_data_list:
            primitive = {'indices': self.get_accessor(primitive_data.indices, COMPONENT_TYPE_UNSIGNED_INT, TYPE_SCALAR)}
            if primitive_data.material is not None and self.material_exists(primitive_data.material):
                primitive['material'] = primitive_data.material
            if primitive_data.mode is not None:
                primitive['mode'] = primitive_data.mode
            if primitive_data.extras:
                primitive['extras'] = primitive_data.extras
            attributes = {}
            for attr in primitive_data.attributes:
                component_type = COMPONENT_TYPE_UNSIGNED_INT if attr.startswith('JOINT') else COMPONENT_TYPE_FLOAT
                type_ = TYPE_VEC3
                if len(primitive_data.attributes[attr][0]) == 4:
                    type_ = TYPE_VEC4
                if len(primitive_data.attributes[attr][0]) == 2:
                    type_ = TYPE_VEC2
                attributes[attr] = self.get_accessor(primitive_data.attributes[attr], component_type, type_, True)
            if attributes:
                primitive['attributes'] = attributes

            targets = []
            for target in primitive_data.targets or []:
                target_dict = {}
                for attr in target:
                    component_type = COMPONENT_TYPE_FLOAT
                    type_ = TYPE_VEC3
                    target_dict[attr] = self.get_accessor(target[attr], component_type, type_, True)
                targets.append(target_dict)
            if targets:
                primitive['targets'] = targets

            primitives.append(primitive)
        return primitives

    def get_accessor(self, data, component_type, type_, include_bounds=False):
        count = len(data)

        fmt_char = COMPONENT_TYPE_ENUM[component_type]
        fmt = '<' + fmt_char * NUM_COMPONENTS_BY_TYPE_ENUM[type_]

        component_size = struct.calcsize('<' + fmt_char)
        if component_type == 'MAT2' and component_size == 1:
            fmt = '<FFxxFFxx'.replace('F', fmt_char)
        elif component_type == 'MAT3' and component_size == 1:
            fmt = '<FFFxFFFxFFFx'.replace('F', fmt_char)
        elif component_type == 'MAT3' and component_size == 2:
            fmt = '<FFFxxFFFxxFFFxx'.replace('F', fmt_char)

        component_len = struct.calcsize(fmt)

        # ensure bytes_ length is divisible by 4
        size = count * component_len
        size += (4 - size % 4) % 4

        bytes_ = bytearray(size)

        for i, datum in enumerate(data):
            if isinstance(datum, int) or isinstance(datum, float):
                struct.pack_into(fmt, bytes_, (i * component_len), datum)
            else:
                struct.pack_into(fmt, bytes_, (i * component_len), *datum)

        buffer_view_index = self.get_buffer_view(bytes_)
        accessor_dict = {
            'bufferView': buffer_view_index,
            'count': count,
            'componentType': component_type,
            'type': type_,
        }
        if include_bounds:
            try:
                _ = [e for e in data[0]]
                minimum = tuple(map(min, zip(*data)))
                maximum = tuple(map(max, zip(*data)))
            except TypeError:
                minimum = (min(data),)
                maximum = (max(data),)
            accessor_dict['min'] = minimum
            accessor_dict['max'] = maximum

        self._gltf_dict.setdefault('accessors', []).append(accessor_dict)

        return len(self._gltf_dict['accessors']) - 1

    def get_buffer_view(self, bytes_):
        byte_offset = self.update_buffer(bytes_)
        buffer_view_dict = {
            'buffer': 0,
            'byteLength': len(bytes_),
            'byteOffset': byte_offset,
        }

        self._gltf_dict.setdefault('bufferViews', []).append(buffer_view_dict)

        return len(self._gltf_dict['bufferViews']) - 1

    def update_buffer(self, bytes_):
        byte_offset = len(self._buffer)
        self._buffer += bytes_
        return byte_offset

    def get_bin_path(self):
        return os.path.join(self._dirname, self._filename + '.bin')

    def get_bin_filename(self):
        return self._filename + '.bin'

    def set_path_attributes(self):
        dirname, basename = os.path.split(self.gltf_filepath)
        root, ext = os.path.splitext(basename)
        self._dirname = dirname
        self._filename = root
        self._ext = ext.lower()
