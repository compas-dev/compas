"""Structured representation of a PLY document."""

from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from .ply_types import PLY_SCALAR_TYPES
from .ply_types import PLYDataType
from .ply_types import PLYFormat
from .ply_types import PLYRecord
from .ply_types import validate_scalar


@dataclass(frozen=True)
class PLYProperty:
    """Property in a PLY element schema."""

    name: str
    data_type: PLYDataType
    list_count_type: Optional[PLYDataType] = None

    @property
    def is_list(self) -> bool:
        """Whether the property contains a variable-length list.

        Returns
        -------
        bool
            True if this is a list property.

        """
        return self.list_count_type is not None


@dataclass
class PLYElement:
    """Element schema and records in a PLY document."""

    name: str
    properties: list[PLYProperty] = field(default_factory=list)
    data: list[PLYRecord] = field(default_factory=list)


@dataclass
class PLYDocument:
    """Parsed PLY data independent of file I/O."""

    format: PLYFormat = "ascii"
    version: str = "1.0"
    comments: list[str] = field(default_factory=list)
    object_info: list[str] = field(default_factory=list)
    elements: list[PLYElement] = field(default_factory=list)

    def element(self, name: str) -> Optional[PLYElement]:
        """Find an element by name.

        Parameters
        ----------
        name
            Element name.

        Returns
        -------
        PLYElement, optional
            Matching element, if present.

        """
        return next((element for element in self.elements if element.name == name), None)

    def validate(self) -> None:
        """Validate element records against their schemas.

        Returns
        -------
        None

        """
        if self.format not in ("ascii", "binary_little_endian", "binary_big_endian"):
            raise ValueError(f"Unsupported PLY format: {self.format}")
        names = set()
        for element in self.elements:
            if element.name in names:
                raise ValueError(f"Duplicate PLY element: {element.name}")
            names.add(element.name)
            property_names = [prop.name for prop in element.properties]
            if len(property_names) != len(set(property_names)):
                raise ValueError(f"Duplicate property in PLY element: {element.name}")
            for prop in element.properties:
                if prop.data_type not in PLY_SCALAR_TYPES:
                    raise ValueError(f"Unsupported PLY scalar type: {prop.data_type}")
                if prop.list_count_type and (
                    prop.list_count_type not in PLY_SCALAR_TYPES
                    or not PLY_SCALAR_TYPES[prop.list_count_type].integer
                ):
                    raise ValueError("PLY list counts require a supported integer type.")
            for record in element.data:
                if set(record) != set(property_names):
                    raise ValueError(f"PLY record does not match the {element.name} schema.")
                for prop in element.properties:
                    value = record[prop.name]
                    if prop.is_list != isinstance(value, list):
                        raise ValueError(f"Invalid value for PLY property: {prop.name}")
                    if isinstance(value, list):
                        if prop.list_count_type is None:
                            raise ValueError(f"Missing list count type for PLY property: {prop.name}")
                        validate_scalar(len(value), prop.list_count_type)
                        for item in value:
                            validate_scalar(item, prop.data_type)
                    else:
                        validate_scalar(value, prop.data_type)
