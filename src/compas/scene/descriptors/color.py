from typing import Self
from typing import overload

from compas.colors import Color
from compas.colors.color import ColorInput


class ColorAttribute:
    """A descriptor for color attributes.

    Parameters
    ----------
    default
        The default value of the attribute.

    """

    def __init__(self, default: ColorInput = None) -> None:
        super().__init__()
        self.default = Color.coerce(default)

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
    def __get__(self, obj: object, otype: type[object] | None = None) -> Color | None: ...

    def __get__(self, obj: object | None, otype: type[object] | None = None) -> Self | Color | None:
        """Get the stored color or initialize it from the default.

        Parameters
        ----------
        obj
            The instance owning the descriptor.
        otype
            The type owning the descriptor.

        Returns
        -------
        ColorAttribute
            The descriptor itself when accessed on the owner class.
        Color | None
            The stored color, or the coerced default if no color was stored.

        """
        if obj is None:
            return self

        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, None)

        color = getattr(obj, self.private_name)

        if color is None:
            color = Color.coerce(self.default)
            setattr(obj, self.private_name, color)

        return color

    def __set__(self, obj: object, value: ColorInput) -> None:
        """Set a new value for the descriptor.

        Parameters
        ----------
        obj
            The owner of the descriptor.
        value
            The new color value. `None` leaves the current value unchanged.

        """
        if value is None:
            return

        setattr(obj, self.private_name, Color.coerce(value))
