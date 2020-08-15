from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import array
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


# This fails on IronPython 2.7.8 (eg. Rhino 6 on Windows)
# but works on IronPython 2.7.9 (Rhino 6 on Mac)
try:
    struct.pack_into('<I', bytearray(4), 0, 0)
    USE_BYTEARRAY_BUFFERS = True
except TypeError:
    USE_BYTEARRAY_BUFFERS = False


class GLTFExporter(object):
    """Export a glTF or glb file based on the supplied scene and ancillary data.

    Parameters
    ----------
    filepath : str
        Location where the glTF or glb is to be written. The extension of the filepath
        determines which format will be used. If there will be an accompanying binary file,
        it will be written in the same directory.
    content : :class:`compas.files.GLTFContent`
    embed_data : bool
        When ``True``, all mesh and other data will be embedded as data uri's in the glTF json,
        with the exception of external image data.
        When ``False``, the data will be written to an external binary file or chunk.

    """

    def __init__(self, filepath, content, embed_data=False):
        self.gltf_filepath = filepath
        self._dirname = None
        self._filename = None
        self._ext = None

        self._embed_data = embed_data
        self._content = content

        self._gltf_dict = {}
        self._mesh_index_by_key = {}
        self._node_index_by_key = {}
        self._scene_index_by_key = {}
        self._camera_index_by_key = {}
        self._skin_index_by_key = {}
        self._material_index_by_key = {}
        self._texture_index_by_key = {}
        self._sampler_index_by_key = {}
        self._image_index_by_key = {}
        self._buffer = b''

        self.load()

    @property
    def embed_data(self):
        return self._embed_data

    @embed_data.setter
    def embed_data(self, value):
        if value != self._embed_data:
            self._embed_data = value
            self.load()

    def load(self):
        """Creates the json object and the binary data (if any) to be written.

        Returns
        -------
        None

        """
        self._content.remove_orphans()
        self._content.check_if_forest()

        self._set_initial_gltf_dict()
        self._mesh_index_by_key = self._get_index_by_key(self._content.meshes)
        self._node_index_by_key = self._get_index_by_key(self._content.nodes)
        self._scene_index_by_key = self._get_index_by_key(self._content.scenes)
        self._camera_index_by_key = self._get_index_by_key(self._content.cameras)
        self._skin_index_by_key = self._get_index_by_key(self._content.skins)
        self._material_index_by_key = self._get_index_by_key(self._content.materials)
        self._texture_index_by_key = self._get_index_by_key(self._content.textures)
        self._sampler_index_by_key = self._get_index_by_key(self._content.samplers)
        self._image_index_by_key = self._get_index_by_key(self._content.images)
        self._buffer = b''

        self._set_path_attributes()
        self._add_meshes()
        self._add_nodes()
        self._add_scenes()
        self._add_cameras()
        self._add_skins()
        self._add_materials()
        self._add_textures()
        self._add_samplers()
        self._add_images()
        self._add_animations()
        self._add_buffer()

    def _get_index_by_key(self, d):
        return {key: index for index, key in enumerate(d)}

    def export(self):
        """Writes the json to *.gltf* or *.glb*, and binary data to *.bin* as required.

        Returns
        -------
        None

        """
        gltf_json = json.dumps(self._gltf_dict, indent=4)

        if self._ext == '.gltf':
            with open(self.gltf_filepath, 'w') as f:
                f.write(gltf_json)
            if not self._embed_data and len(self._buffer) > 0:
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

    def _add_images(self):
        if not self._content.images:
            return
        images_list = [None] * len(self._content.images)
        for key, image_data in self._content.images.items():
            uri = self._construct_image_data_uri(image_data) if self.embed_data else None
            buffer_view = self._construct_buffer_view(image_data.data) if not self.embed_data else None
            images_list[self._image_index_by_key[key]] = image_data.to_data(uri, buffer_view)
        self._gltf_dict['images'] = images_list

    def _construct_image_data_uri(self, image_data):
        if image_data.data is None:
            return None
        return (
            'data:'
            + (image_data.mime_type if image_data.mime_type else '')
            + ';base64,' + base64.b64encode(image_data.data).decode('ascii')
        )

    def _add_samplers(self):
        if not self._content.samplers:
            return
        samplers_list = [None] * len(self._content.samplers)
        for key, sampler_data in self._content.samplers.items():
            samplers_list[self._sampler_index_by_key[key]] = sampler_data.to_data()
        self._gltf_dict['samplers'] = samplers_list

    def _add_textures(self):
        if not self._content.textures:
            return
        textures_list = [None] * len(self._content.textures)
        for key, texture_data in self._content.textures.items():
            textures_list[self._texture_index_by_key[key]] = texture_data.to_data(self._sampler_index_by_key, self._image_index_by_key)
        self._gltf_dict['textures'] = textures_list

    def _add_materials(self):
        if not self._content.materials:
            return
        materials_list = [None] * len(self._content.materials)
        for key, material_data in self._content.materials.items():
            materials_list[self._material_index_by_key[key]] = material_data.to_data(self._texture_index_by_key)
        self._gltf_dict['materials'] = materials_list

    def _add_skins(self):
        if not self._content.skins:
            return
        skins_list = [None] * len(self._content.skins)
        for key, skin_data in self._content.skins.items():
            accessor_index = self._construct_accessor(skin_data.inverse_bind_matrices, COMPONENT_TYPE_FLOAT, TYPE_MAT4)
            skins_list[self._skin_index_by_key[key]] = skin_data.to_data(self._node_index_by_key, accessor_index)
        self._gltf_dict['skins'] = skins_list

    def _add_cameras(self):
        if not self._content.cameras:
            return
        camera_list = [None] * len(self._content.cameras)
        for key, camera_data in self._content.cameras.items():
            camera_list[self._camera_index_by_key[key]] = camera_data.to_data()
        self._gltf_dict['cameras'] = camera_list

    def _add_meshes(self):
        if not self._content.meshes:
            return
        mesh_list = [None] * len(self._content.meshes)
        for key, mesh_data in self._content.meshes.items():
            primitives = self._construct_primitives(mesh_data)
            mesh_list[self._mesh_index_by_key[key]] = mesh_data.to_data(primitives)
        self._gltf_dict['meshes'] = mesh_list

    def _add_buffer(self):
        if not self._buffer:
            return
        buffer = {'byteLength': len(self._buffer)}
        if self._embed_data:
            buffer['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(self._buffer).decode('ascii')
        elif self._ext == '.gltf':
            buffer['uri'] = self.get_bin_filename()
        self._gltf_dict['buffers'] = [buffer]

    def _add_animations(self):
        if not self._content.animations:
            return None
        animation_list = []
        for animation_data in self._content.animations.values():
            samplers_list = self._construct_animation_samplers_list(animation_data)
            animation_list.append(animation_data.to_data(samplers_list, self._node_index_by_key))
        self._gltf_dict['animations'] = animation_list

    def _construct_animation_samplers_list(self, animation_data):
        sampler_index_by_key = animation_data.get_sampler_index_by_key()
        samplers_list = [None] * len(sampler_index_by_key)
        for key, sampler_data in animation_data.samplers_dict.items():
            input_accessor = self._construct_accessor(sampler_data.input, COMPONENT_TYPE_FLOAT, TYPE_SCALAR, include_bounds=True)
            type_ = TYPE_VEC3
            if isinstance(sampler_data.output[0], int) or isinstance(sampler_data.output[0], float):
                type_ = TYPE_SCALAR
            elif len(sampler_data.output[0]) == 4:
                type_ = TYPE_VEC4
            output_accessor = self._construct_accessor(sampler_data.output, COMPONENT_TYPE_FLOAT, type_)
            samplers_list[sampler_index_by_key[key]] = sampler_data.to_data(input_accessor, output_accessor)
        return samplers_list

    def _set_initial_gltf_dict(self):
        asset_dict = {'version': '2.0'}
        gltf_dict = {'asset': asset_dict}
        if self._content.extras:
            gltf_dict['extras'] = self._content.extras
        if self._content.extensions:
            gltf_dict['extensions'] = self._content.extensions
        self._gltf_dict = gltf_dict

    def _add_scenes(self):
        if not self._content.scenes:
            return
        if self._content.default_scene_key is not None:
            self._gltf_dict['scene'] = self._scene_index_by_key[self._content.default_scene_key]
        scene_list = [None] * len(self._content.scenes.values())
        for key, scene in self._content.scenes.items():
            scene_list[self._scene_index_by_key[key]] = scene.to_data(self._node_index_by_key)
        self._gltf_dict['scenes'] = scene_list

    def _add_nodes(self):
        if not self._content.nodes:
            return
        node_list = [None] * len(self._content.nodes)
        for key, node in self._content.nodes.items():
            node_list[self._node_index_by_key[key]] = node.to_data(
                self._node_index_by_key,
                self._mesh_index_by_key,
                self._camera_index_by_key,
                self._skin_index_by_key,
            )
        self._gltf_dict['nodes'] = node_list

    def _construct_primitives(self, mesh_data):
        primitives = []
        for primitive_data in mesh_data.primitive_data_list:
            indices_accessor = self._construct_accessor(primitive_data.indices, COMPONENT_TYPE_UNSIGNED_INT, TYPE_SCALAR)

            attributes = {}
            for attr in primitive_data.attributes:
                component_type = COMPONENT_TYPE_UNSIGNED_INT if attr.startswith('JOINT') else COMPONENT_TYPE_FLOAT
                type_ = TYPE_VEC3
                if len(primitive_data.attributes[attr][0]) == 4:
                    type_ = TYPE_VEC4
                if len(primitive_data.attributes[attr][0]) == 2:
                    type_ = TYPE_VEC2
                attributes[attr] = self._construct_accessor(primitive_data.attributes[attr], component_type, type_, True)

            targets = []
            for target in primitive_data.targets or []:
                target_dict = {}
                for attr in target:
                    component_type = COMPONENT_TYPE_FLOAT
                    type_ = TYPE_VEC3
                    target_dict[attr] = self._construct_accessor(target[attr], component_type, type_, True)
                targets.append(target_dict)

            primitive_dict = primitive_data.to_data(indices_accessor, attributes, targets, self._material_index_by_key)

            primitives.append(primitive_dict)
        return primitives

    def _construct_accessor(self, data, component_type, type_, include_bounds=False):
        if data is None:
            return None
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

        if USE_BYTEARRAY_BUFFERS:
            bytes_ = bytearray(size)
        else:
            bytes_ = array.array('B', [0] * size)

        for i, datum in enumerate(data):
            if isinstance(datum, int) or isinstance(datum, float):
                struct.pack_into(fmt, bytes_, (i * component_len), datum)
            else:
                struct.pack_into(fmt, bytes_, (i * component_len), *datum)

        buffer_view_index = self._construct_buffer_view(bytes_)
        accessor_dict = {
            'bufferView': buffer_view_index,
            'count': count,
            'componentType': component_type,
            'type': type_,
        }
        if include_bounds:
            try:
                # Here we check if ``data`` contains tuples,
                # and compute min/max per coordinate.
                _ = [e for e in data[0]]
                minimum = tuple(map(min, zip(*data)))
                maximum = tuple(map(max, zip(*data)))
            except TypeError:
                # Here, ``data`` must contain primitives and not tuples,
                # so min and max are more simply computed.
                minimum = (min(data),)
                maximum = (max(data),)
            accessor_dict['min'] = minimum
            accessor_dict['max'] = maximum

        self._gltf_dict.setdefault('accessors', []).append(accessor_dict)

        return len(self._gltf_dict['accessors']) - 1

    def _construct_buffer_view(self, bytes_):
        if not bytes_:
            return None
        byte_offset = self._update_buffer(bytes_)
        buffer_view_dict = {
            'buffer': 0,
            'byteLength': len(bytes_),
            'byteOffset': byte_offset,
        }

        self._gltf_dict.setdefault('bufferViews', []).append(buffer_view_dict)

        return len(self._gltf_dict['bufferViews']) - 1

    def _update_buffer(self, bytes_):
        byte_offset = len(self._buffer)
        # If bytes_ was not created as bytearray, cast now
        if not USE_BYTEARRAY_BUFFERS:
            bytes_ = bytearray(bytes_)
        self._buffer += bytes_
        return byte_offset

    def _set_path_attributes(self):
        dirname, basename = os.path.split(self.gltf_filepath)
        root, ext = os.path.splitext(basename)
        self._dirname = dirname
        self._filename = root
        self._ext = ext.lower()

    def get_bin_path(self):
        return os.path.join(self._dirname, self._filename + '.bin')

    def get_bin_filename(self):
        return self._filename + '.bin'
