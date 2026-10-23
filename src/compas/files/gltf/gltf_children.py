"""Validated node-key collection used by glTF scenes and nodes."""

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import MutableSequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gltf_document import GLTFDocument


class GLTFChildren(MutableSequence[int]):
    """Mutable node-key sequence validated against a document."""

    # =============================================================================
    # Dunder methods
    # =============================================================================

    def __init__(self, context: "GLTFDocument", values: Iterable[int] = ()) -> None:
        self._values = list(values)
        self._context = context
        for value in self._values:
            self._validate(value)

    def __repr__(self) -> str:
        return repr(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value) -> None:
        if isinstance(index, slice):
            values = list(value)
            for item in values:
                self._validate(item)
            self._values[index] = values
        else:
            self._validate(value)
            self._values[index] = value

    def __delitem__(self, index) -> None:
        del self._values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[int]:
        return iter(self._values)

    def insert(self, index: int, value: int) -> None:
        self._validate(value)
        self._values.insert(index, value)

    # =============================================================================
    # Methods
    # =============================================================================

    def pop(self, index: int = -1) -> int:
        """Remove and return a node key.

        Returns
        -------
        int
            Removed node key.

        """
        return self._values.pop(index)

    def index(self, value: int, start: int = 0, stop: int | None = None) -> int:
        """Return the position of a node key.

        Returns
        -------
        int
            Position of the first matching key.

        """
        return self._values.index(value, start, len(self._values) if stop is None else stop)

    def count(self, value: int) -> int:
        """Count occurrences of a node key.

        Returns
        -------
        int
            Number of occurrences.

        """
        return self._values.count(value)

    def copy(self) -> list[int]:
        """Return an independent list of node keys.

        Returns
        -------
        list[int]
            Copied node keys.

        """
        return self._values.copy()

    # =============================================================================
    # Private helpers
    # =============================================================================

    def _validate(self, value: int) -> None:
        if value not in self._context.nodes:
            raise ValueError(f"Cannot find glTF node {value}.")
