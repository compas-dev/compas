"""Structured representation of a PLY document."""

from dataclasses import dataclass
from dataclasses import field
from typing import Literal
from typing import Optional
from typing import Union

PLYFormat = Literal["ascii", "binary_little_endian", "binary_big_endian"]
PLYScalar = Union[int, float]
PLYValue = Union[PLYScalar, list[PLYScalar]]


@dataclass(frozen=True)
class PLYProperty:
    """Property in a PLY element schema."""

    name: str
    data_type: str
    list_count_type: Optional[str] = None

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
    data: list[dict[str, PLYValue]] = field(default_factory=list)


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
        names = set()
        for element in self.elements:
            if element.name in names:
                raise ValueError(f"Duplicate PLY element: {element.name}")
            names.add(element.name)
            property_names = [prop.name for prop in element.properties]
            if len(property_names) != len(set(property_names)):
                raise ValueError(f"Duplicate property in PLY element: {element.name}")
            for record in element.data:
                if set(record) != set(property_names):
                    raise ValueError(f"PLY record does not match the {element.name} schema.")
                for prop in element.properties:
                    if prop.is_list != isinstance(record[prop.name], list):
                        raise ValueError(f"Invalid value for PLY property: {prop.name}")
