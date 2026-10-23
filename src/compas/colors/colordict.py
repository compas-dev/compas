from collections.abc import Hashable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import MutableMapping
from typing import Self
from typing import cast

from compas.data import Data

from .color import Color
from .color import ColorError
from .color import ColorInput

type ColorKey = Hashable


def _restore_json_key(key: object) -> ColorKey:
    if isinstance(key, list):
        return tuple(_restore_json_key(item) for item in key)
    # Hashability is enforced by the dictionary operation itself.
    return cast(ColorKey, key)


class ColorDict(Data, MutableMapping[ColorKey, Color]):
    """Class representing a dictionary of colors.

    Parameters
    ----------
    default
        The default color to use if the requested key is not in the dictionary.
    name
        The name of the color dictionary.

    """

    # --------------------------------------------------------------------------
    # Data
    # --------------------------------------------------------------------------

    @property
    def __data__(self) -> dict[str, object]:
        return {
            "default": self.default,
            "items": list(self._dict.items()),
        }

    @classmethod
    def __from_data__(cls, data: dict[str, object]) -> Self:
        colordict = cls(cast(ColorInput, data["default"]))
        items = cast(Iterable[tuple[object, ColorInput]], data["items"])
        for key, color in items:
            colordict[_restore_json_key(key)] = color
        return colordict

    # --------------------------------------------------------------------------
    # Dunder methods
    # --------------------------------------------------------------------------

    def __init__(self, default: ColorInput = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._default: Color | None = None
        self.default = default
        self._dict: dict[ColorKey, Color] = {}

    def __getitem__(self, key: ColorKey) -> Color:
        return self._dict.get(key, self.default)

    def __setitem__(self, key: ColorKey, value: ColorInput) -> None:
        color = Color.coerce(value)
        if color is None:
            raise ColorError("A color dictionary value cannot be None.")
        self._dict[key] = color

    def __delitem__(self, key: ColorKey) -> None:
        del self._dict[key]

    def __iter__(self) -> Iterator[ColorKey]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, key: object) -> bool:
        return key in self._dict

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def default(self) -> Color:
        """The fallback color for keys that are not present.

        Assigning `None` resets the fallback to black. Other supported color
        inputs are coerced to `Color`.

        """
        if not self._default:
            self._default = Color(0, 0, 0)
        return self._default

    @default.setter
    def default(self, default: ColorInput) -> None:
        self._default = Color.coerce(default)

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------

    def clear(self) -> None:
        """Clear the previously stored items."""
        self._dict.clear()
