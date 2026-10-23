from collections.abc import Mapping
from typing import Any
from typing import Self
from typing import overload

from compas.colors.color import ColorInput
from compas.colors.colordict import ColorDict


class ColorDictAttribute:
    """Descriptor for color dictionaries."""

    def __init__(self, default: ColorInput = None) -> None:
        super().__init__()
        self.default = default

    def __set_name__(self, owner: type[object], name: str) -> None:
        """Record the public and private attribute names.

        Parameters
        ----------
        owner
            The class owning the attribute.
        name
            The name of the attribute.

        """
        self.name = name
        self.private_name = "_" + name

    @overload
    def __get__(self, obj: None, otype: type[object]) -> Self: ...

    @overload
    def __get__(self, obj: object, otype: type[object] | None = None) -> ColorDict: ...

    def __get__(self, obj: object | None, otype: type[object] | None = None) -> Self | ColorDict:
        """Get the stored color dictionary, creating it when necessary.

        Parameters
        ----------
        obj
            The instance owning the descriptor.
        otype
            The type owning the descriptor.

        Returns
        -------
        ColorDictAttribute
            The descriptor itself when accessed on the owner class.
        ColorDict
            The color dictionary stored by the descriptor.

        """
        if obj is None:
            return self

        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, None)

        colordict = getattr(obj, self.private_name)

        if colordict is None:
            colordict = ColorDict(default=self.default)
            setattr(obj, self.private_name, colordict)

        return colordict

    def __set__(
        self,
        obj: object,
        value: Mapping[Any, ColorInput] | ColorDict | ColorInput,
    ) -> None:
        """Set a new value for the descriptor.

        Parameters
        ----------
        obj
            The owner of the descriptor.
        value
            A color mapping, color dictionary, or default color. `None` leaves
            the current value unchanged. An empty mapping clears stored items.

        """
        if value is None:
            return

        colordict = getattr(obj, self.name)

        if isinstance(value, ColorDict):
            colordict.clear()
            colordict.default = value.default
            colordict.update(value)

        elif isinstance(value, Mapping):
            colordict.clear()
            colordict.update(value)

        else:
            colordict.clear()
            colordict.default = value
