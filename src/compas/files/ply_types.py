"""PLY scalar type definitions and codecs."""

import struct
from typing import Literal
from typing import NamedTuple
from typing import Optional
from typing import Union

PLYFormat = Literal["ascii", "binary_little_endian", "binary_big_endian"]
PLYDataType = Literal[
    "char",
    "int8",
    "uchar",
    "uint8",
    "short",
    "int16",
    "ushort",
    "uint16",
    "int",
    "int32",
    "uint",
    "uint32",
    "int64",
    "uint64",
    "float",
    "float32",
    "double",
    "float64",
]
PLYByteOrder = Literal["<", ">"]
PLYScalar = Union[int, float]
PLYValue = Union[PLYScalar, list[PLYScalar]]
PLYRecord = dict[str, PLYValue]


class PLYScalarType(NamedTuple):
    """Storage and value constraints of a PLY scalar type."""

    format: str
    integer: bool
    minimum: Optional[int] = None
    maximum: Optional[int] = None


PLY_SCALAR_TYPES: dict[PLYDataType, PLYScalarType] = {
    "char": PLYScalarType("b", True, -128, 127),
    "int8": PLYScalarType("b", True, -128, 127),
    "uchar": PLYScalarType("B", True, 0, 255),
    "uint8": PLYScalarType("B", True, 0, 255),
    "short": PLYScalarType("h", True, -32768, 32767),
    "int16": PLYScalarType("h", True, -32768, 32767),
    "ushort": PLYScalarType("H", True, 0, 65535),
    "uint16": PLYScalarType("H", True, 0, 65535),
    "int": PLYScalarType("i", True, -2147483648, 2147483647),
    "int32": PLYScalarType("i", True, -2147483648, 2147483647),
    "uint": PLYScalarType("I", True, 0, 4294967295),
    "uint32": PLYScalarType("I", True, 0, 4294967295),
    "int64": PLYScalarType("q", True, -9223372036854775808, 9223372036854775807),
    "uint64": PLYScalarType("Q", True, 0, 18446744073709551615),
    "float": PLYScalarType("f", False),
    "float32": PLYScalarType("f", False),
    "double": PLYScalarType("d", False),
    "float64": PLYScalarType("d", False),
}


def validate_scalar(value: PLYScalar, data_type: PLYDataType) -> None:
    """Validate a scalar value against a PLY type."""
    scalar_type = PLY_SCALAR_TYPES.get(data_type)
    if scalar_type is None:
        raise ValueError(f"Unsupported PLY scalar type: {data_type}")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid value for PLY scalar type: {data_type}")
    if scalar_type.integer:
        if not isinstance(value, int):
            raise ValueError(f"PLY {data_type} values must be integers.")
        minimum = scalar_type.minimum
        maximum = scalar_type.maximum
        if minimum is None or maximum is None:
            raise ValueError(f"PLY integer type has no defined range: {data_type}")
        if value < minimum or value > maximum:
            raise ValueError(f"PLY value is outside the range of {data_type}.")


def parse_scalar(value: str, data_type: PLYDataType) -> PLYScalar:
    """Parse and validate an ASCII PLY scalar."""
    scalar_type = PLY_SCALAR_TYPES.get(data_type)
    if scalar_type is None:
        raise ValueError(f"Unsupported PLY scalar type: {data_type}")
    result = int(value) if scalar_type.integer else float(value)
    validate_scalar(result, data_type)
    return result


def pack_scalar(value: PLYScalar, byte_order: PLYByteOrder, data_type: PLYDataType) -> bytes:
    """Pack a validated binary PLY scalar."""
    validate_scalar(value, data_type)
    return struct.pack(byte_order + PLY_SCALAR_TYPES[data_type].format, value)


def unpack_scalar(data: bytes, offset: int, byte_order: PLYByteOrder, data_type: PLYDataType) -> tuple[PLYScalar, int]:
    """Unpack a binary PLY scalar and return its new offset."""
    scalar_type = PLY_SCALAR_TYPES.get(data_type)
    if scalar_type is None:
        raise ValueError(f"Unsupported PLY scalar type: {data_type}")
    format = byte_order + scalar_type.format
    value = struct.unpack_from(format, data, offset)[0]
    return value, offset + struct.calcsize(format)
