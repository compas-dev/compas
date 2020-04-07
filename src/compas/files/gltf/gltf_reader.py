from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import base64
import json
import os
import re
import struct

from compas.files.gltf.constants import COMPONENT_TYPE_BYTE
from compas.files.gltf.constants import COMPONENT_TYPE_ENUM
from compas.files.gltf.constants import COMPONENT_TYPE_SHORT
from compas.files.gltf.constants import COMPONENT_TYPE_UNSIGNED_BYTE
from compas.files.gltf.constants import COMPONENT_TYPE_UNSIGNED_SHORT
from compas.files.gltf.constants import NUM_COMPONENTS_BY_TYPE_ENUM
from compas.files.gltf.data_classes import ImageData


class GLTFReader(object):
    """Read the contents of a *glTF* or *glb* version 2 file using the json library.
    Uses ideas from Khronos Group's glTF-Blender-IO.
    Caution: Extensions are minimally supported and their data may be lost.

    Parameters
    ----------
    filepath: str
        Path to the file.

    Attributes
    ----------
    filepath : str
        String containing the path to the glTF.
    json : dict
        Dictionary object containing the contents of the glTF.
    data : list
        List of lists containing data read from binary files.
    image_data : list
        List containing image data.
    """
    def __init__(self, filepath):
        self.filepath = filepath

        self.json = None
        self.data = []
        self.image_data = []

        self._bin_content = None
        self._glb_buffer = None
        self._buffers = {}

        self.read()

    def read(self):
        with open(self.filepath, 'rb') as f:
            self._bin_content = self._get_memoryview(f.read())

        is_glb = self._bin_content[:4] == b'glTF'

        if not is_glb:
            content = self._bin_content.tobytes().decode('utf-8')
            self.json = json.loads(content)
        else:
            self._load_from_glb()

        self._release_buffer(self._bin_content)
        self._bin_content = None

        self._check_version()

        if self.json:
            for accessor in self.json.get('accessors', []):
                accessor_data = self._access_data(accessor)
                self.data.append(accessor_data)

            for image in self.json.get('images', []):
                mime_type = self.get_mime_type(image.get('uri'))
                data = None
                if 'bufferView' in image:
                    data = self._get_attr_data(image, 'bufferView')
                if 'uri' in image and self.is_data_uri(image['uri']):
                    data = base64.b64decode(self.get_data_uri_data(image['uri']))

                image_data = ImageData.from_data(image, data, mime_type)
                self.image_data.append(image_data)

        self._release_buffers()

    def _load_from_glb(self):
        header = self._unpack_content('<4sII')
        file_size = header[2]

        if file_size != len(self._bin_content):
            raise Exception('Bad glTF.  File size does not match.')

        offset = 12

        # load json
        type_, _length, json_bytes, offset = self._load_chunk(offset)
        if type_ != b'JSON':
            raise Exception('Bad glTF.  First chunk not in JSON format')
        json_str = json_bytes.tobytes().decode('utf-8')
        self.json = json.loads(json_str)

        # load binary buffer
        if offset < len(self._bin_content):
            type_, _length, bytes_, offset = self._load_chunk(offset)
            if type_ == b'BIN\0':
                self._glb_buffer = bytes_

    def _load_chunk(self, offset):
        chunk_header = self._unpack_content('<I4s', offset)
        length = chunk_header[0]
        type_ = chunk_header[1]
        data = self._bin_content[offset + 8: offset + 8 + length]

        return type_, length, data, offset + 8 + length

    def _unpack_content(self, fmt, offset=0):
        try:
            chunk = struct.unpack_from(fmt, self._bin_content, offset)
        except TypeError:
            # for Python 2.7 compatibility
            chunk = struct.unpack_from(fmt, self._bin_content.tobytes(), offset)
        return chunk

    def _check_version(self):
        version = self.json['asset']['version']
        if version != '2.0':
            raise Exception('Invalid glTF version.  Version 2.0 expected.')

    def _get_attr_data(self, obj, attr):
        if attr not in obj:
            return None
        buffer_view_index = obj[attr]
        buffer_view = self.json['bufferViews'][buffer_view_index]
        buffer = self._get_buffer(buffer_view['buffer'])
        offset = buffer_view.get('byteOffset', 0)
        length = buffer_view['byteLength']
        return buffer[offset: offset + length].tobytes()

    def _access_data(self, accessor):
        count = accessor['count']
        component_type = accessor['componentType']
        type_ = accessor['type']
        accessor_offset = accessor.get('byteOffset', 0)
        num_components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]

        # This situation indicates use of an extension.
        if 'sparse' not in accessor and 'bufferView' not in accessor:
            return None

        if 'bufferView' in accessor:
            buffer_view_index = accessor['bufferView']
            data = self._read_from_buffer_view(
                buffer_view_index,
                count,
                component_type,
                accessor_offset,
                num_components
            )
        else:
            data = self.get_generic_data(num_components, count)

        if 'sparse' in accessor:
            sparse_data = accessor['sparse']
            sparse_count = sparse_data['count']

            sparse_indices_data = sparse_data['indices']
            sparse_indices_buffer_view_index = sparse_indices_data['bufferView']
            sparse_indices_component_type = sparse_indices_data['componentType']
            sparse_indices = self._read_from_buffer_view(
                sparse_indices_buffer_view_index,
                sparse_count,
                sparse_indices_component_type,
                accessor_offset,
                NUM_COMPONENTS_BY_TYPE_ENUM['SCALAR']
            )

            sparse_values_data = sparse_data['values']
            sparse_values_buffer_view_index = sparse_values_data['bufferView']
            sparse_values = self._read_from_buffer_view(
                sparse_values_buffer_view_index,
                sparse_count,
                component_type,
                accessor_offset,
                num_components
            )

            for index, data_index in enumerate(sparse_indices):
                data[data_index] = sparse_values[index]

            if accessor.get('normalized', False):
                for index, tuple_ in enumerate(data):
                    new_tuple = ()
                    for i in tuple_:
                        if component_type == COMPONENT_TYPE_BYTE:
                            new_tuple += (max(float(i / 127.0), -1.0),)
                        elif component_type == COMPONENT_TYPE_UNSIGNED_BYTE:
                            new_tuple += (float(i / 255.0),)
                        elif component_type == COMPONENT_TYPE_SHORT:
                            new_tuple += (max(float(i / 32767.0), -1.0),)
                        elif component_type == COMPONENT_TYPE_UNSIGNED_SHORT:
                            new_tuple += (i / 65535.0,)
                        else:
                            new_tuple += (float(i),)
                    data[index] = new_tuple

        return data

    def _read_from_buffer_view(self, buffer_view_index, count, component_type, accessor_offset, num_components):
        buffer_view = self.json['bufferViews'][buffer_view_index]

        buffer_view_offset = buffer_view.get('byteOffset', 0)
        offset = accessor_offset + buffer_view_offset

        format_char = COMPONENT_TYPE_ENUM[component_type]
        format_ = '<' + format_char * num_components

        expected_length = struct.calcsize(format_)

        component_size = struct.calcsize('<' + format_char)
        if component_type == 'MAT2' and component_size == 1:
            format_ = '<FFxxFF'.replace('F', format_char)
            expected_length = 8
        elif component_type == 'MAT3' and component_size == 1:
            format_ = '<FFFxFFFxFFF'.replace('F', format_char)
            expected_length = 12
        elif component_type == 'MAT3' and component_size == 2:
            format_ = '<FFFxxFFFxxFFF'.replace('F', format_char)
            expected_length = 24

        byte_stride = buffer_view.get('byteStride', expected_length)

        unpack_from = struct.Struct(format_).unpack_from

        buffer_index = buffer_view['buffer']
        buffer = self._get_buffer(buffer_index)

        data = [
            unpack_from(buffer[i: i + byte_stride].tobytes())
            for i in range(offset, offset + count * byte_stride, byte_stride)
        ]

        if num_components == 1:
            data = [item[0] for item in data]  # unwrap scalars from tuple

        return data

    def _get_buffer(self, buffer_index):
        if buffer_index in self._buffers:
            return self._buffers[buffer_index]

        uri = self.json['buffers'][buffer_index].get('uri', None)

        if not uri:
            buffer = self._glb_buffer
        elif self.is_data_uri(uri):
            string = self.get_data_uri_data(uri)
            buffer = self._get_memoryview(base64.b64decode(string))
        else:
            filepath = self.get_filepath(uri)
            with open(filepath, 'rb') as f:
                buffer = self._get_memoryview(f.read())

        self._buffers[buffer_index] = buffer

        return buffer

    def _release_buffer(self, buffer):
        try:
            buffer.release()
        except AttributeError:
            # AttributeError indicates using Python <3.2
            pass

    def _release_buffers(self):
        self._release_buffer(self._glb_buffer)
        self._glb_buffer = None
        for i in range(len(self._buffers)):
            self._release_buffer(self._buffers[i])
        self._buffers = {}

    def _get_memoryview(self, content):
        try:
            mv = memoryview(content)
        except TypeError:
            # Exception occurs when using IronPython 2.7.8.
            # See https://github.com/IronLanguages/ironpython2/issues/374#issuecomment-390658569
            mv = memoryview(bytearray(content))
        return mv

    def get_filepath(self, uri):
        dir_path = os.path.dirname(self.filepath)
        return os.path.join(dir_path, uri)

    def get_mime_type(self, string):
        if string is None or not self.is_data_uri(string):
            return None
        pattern = r'data:([\w/]+)(?<![;,])'
        result = re.search(pattern, string)
        return result.group(1)

    def get_generic_data(self, num_components, count):
        return [(0, ) * num_components for _ in range(count)]

    def is_data_uri(self, uri):
        return uri.startswith('data:')

    def get_data_uri_data(self, uri):
        split_uri = uri.split(',')
        return split_uri[-1]
