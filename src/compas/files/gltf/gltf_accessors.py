"""Buffer, buffer-view, accessor, and image decoding for glTF."""

import base64
import binascii
import re
import struct
from typing import Any
from typing import Optional

from .constants import COMPONENT_TYPE_BYTE
from .constants import COMPONENT_TYPE_ENUM
from .constants import COMPONENT_TYPE_SHORT
from .constants import COMPONENT_TYPE_UNSIGNED_BYTE
from .constants import COMPONENT_TYPE_UNSIGNED_SHORT
from .constants import NUM_COMPONENTS_BY_TYPE_ENUM
from .gltf_container import GLTFParseError
from .gltf_resources import GLTFResourceLoader
from .gltf_types import AccessorData
from .gltf_types import GLTFJson


def is_data_uri(uri: str) -> bool:
    """Determine whether a URI contains embedded data."""
    return uri.startswith("data:")


def decode_data_uri(uri: str) -> bytes:
    """Decode a base64 data URI.

    Returns
    -------
    bytes
        Decoded contents.

    """
    try:
        metadata, encoded = uri.split(",", 1)
        if ";base64" not in metadata:
            raise GLTFParseError("Only base64 glTF data URIs are supported.")
        return base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as error:
        if isinstance(error, GLTFParseError):
            raise
        raise GLTFParseError("Invalid glTF data URI.") from error


def data_uri_mime_type(uri: Optional[str]) -> Optional[str]:
    """Extract the media type from a data URI."""
    if not uri or not is_data_uri(uri):
        return None
    match = re.match(r"data:([^;,]+)", uri)
    return match.group(1) if match else None


class GLTFAccessorDecoder:
    """Resolve buffers and decode accessors from parsed glTF JSON."""

    def __init__(
        self,
        document: GLTFJson,
        binary_chunk: Optional[bytes],
        resource_loader: Optional[GLTFResourceLoader],
    ) -> None:
        self.document = document
        self.binary_chunk = binary_chunk
        self.resource_loader = resource_loader
        self._buffers: dict[int, bytes] = {}

    def decode_all(self) -> list[AccessorData]:
        """Decode every accessor.

        Returns
        -------
        list[AccessorData]
            Decoded accessor values in source order.

        """
        return [self.decode(accessor) for accessor in self.document.get("accessors", [])]

    def decode(self, accessor: GLTFJson) -> AccessorData:
        count = accessor["count"]
        component_type = accessor["componentType"]
        type_ = accessor["type"]
        components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]
        if "sparse" not in accessor and "bufferView" not in accessor:
            return None
        if "bufferView" in accessor:
            values = self._read_buffer_view(
                accessor["bufferView"], count, component_type, accessor.get("byteOffset", 0), type_
            )
        else:
            values = [(0,) * components for _ in range(count)]

        sparse = accessor.get("sparse")
        if sparse:
            indices = sparse["indices"]
            sparse_indices = self._read_buffer_view(
                indices["bufferView"], sparse["count"], indices["componentType"], indices.get("byteOffset", 0), "SCALAR"
            )
            sparse_values_spec = sparse["values"]
            sparse_values = self._read_buffer_view(
                sparse_values_spec["bufferView"],
                sparse["count"],
                component_type,
                sparse_values_spec.get("byteOffset", 0),
                type_,
            )
            for index, value_index in enumerate(sparse_indices):
                values[value_index] = sparse_values[index]

        if accessor.get("normalized", False):
            values = [_normalize(value, component_type) for value in values]
        return values

    def buffer_view_bytes(self, index: int) -> bytes:
        """Read the exact bytes of a buffer view.

        Returns
        -------
        bytes
            Buffer-view contents.

        """
        view = self.document["bufferViews"][index]
        buffer = self._get_buffer(view["buffer"])
        offset = view.get("byteOffset", 0)
        end = offset + view["byteLength"]
        if end > len(buffer):
            raise GLTFParseError("Buffer view exceeds its buffer.")
        return buffer[offset:end]

    def resource_bytes(self, uri: str) -> bytes:
        """Resolve an embedded or external resource URI.

        Returns
        -------
        bytes
            Resource contents.

        """
        if is_data_uri(uri):
            return decode_data_uri(uri)
        if self.resource_loader is None:
            raise GLTFParseError(f"No resource loader is available for {uri!r}.")
        return self.resource_loader.read(uri)

    def _read_buffer_view(
        self, index: int, count: int, component_type: int, accessor_offset: int, type_: str
    ) -> list[Any]:
        view = self.document["bufferViews"][index]
        format_char = COMPONENT_TYPE_ENUM[component_type]
        components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]
        component_size = struct.calcsize("<" + format_char)
        if type_ == "MAT2" and component_size == 1:
            format_ = "<" + (format_char * 2 + "xx") * 2
        elif type_ == "MAT3" and component_size == 1:
            format_ = "<" + (format_char * 3 + "x") * 3
        elif type_ == "MAT3" and component_size == 2:
            format_ = "<" + (format_char * 3 + "xx") * 3
        else:
            format_ = "<" + format_char * components
        item_size = struct.calcsize(format_)
        stride = view.get("byteStride", item_size)
        if stride < item_size:
            raise GLTFParseError("Buffer-view stride is smaller than an accessor item.")
        offset = view.get("byteOffset", 0) + accessor_offset
        buffer = self._get_buffer(view["buffer"])
        if count and offset + (count - 1) * stride + item_size > len(buffer):
            raise GLTFParseError("Accessor exceeds its buffer.")
        unpack = struct.Struct(format_).unpack_from
        values = [unpack(buffer, offset + item * stride) for item in range(count)]
        return [value[0] for value in values] if components == 1 else values

    def _get_buffer(self, index: int) -> bytes:
        if index in self._buffers:
            return self._buffers[index]
        spec = self.document["buffers"][index]
        uri = spec.get("uri")
        if uri is None:
            if self.binary_chunk is None:
                raise GLTFParseError("A buffer has no URI and no GLB binary chunk.")
            data = self.binary_chunk
        elif is_data_uri(uri):
            data = decode_data_uri(uri)
        else:
            if self.resource_loader is None:
                raise GLTFParseError(f"No resource loader is available for {uri!r}.")
            data = self.resource_loader.read(uri)
        if len(data) < spec["byteLength"]:
            raise GLTFParseError("Buffer is shorter than its declared byte length.")
        self._buffers[index] = data
        return data


def _normalize(value: Any, component_type: int) -> Any:
    scalar = not isinstance(value, tuple)
    values = (value,) if scalar else value
    result = []
    for component in values:
        if component_type == COMPONENT_TYPE_BYTE:
            result.append(max(component / 127.0, -1.0))
        elif component_type == COMPONENT_TYPE_UNSIGNED_BYTE:
            result.append(component / 255.0)
        elif component_type == COMPONENT_TYPE_SHORT:
            result.append(max(component / 32767.0, -1.0))
        elif component_type == COMPONENT_TYPE_UNSIGNED_SHORT:
            result.append(component / 65535.0)
        else:
            result.append(float(component))
    return result[0] if scalar else tuple(result)
