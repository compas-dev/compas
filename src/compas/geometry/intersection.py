from collections.abc import Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from typing import overload


@dataclass(frozen=True)
class IntersectionResult[T](Sequence[T]):
    """The results of an intersection operation.

    Parameters
    ----------
    results
        The intersection results.

    Examples
    --------
    >>> result = IntersectionResult(("first", "second"))
    >>> result.number_of_results
    2
    >>> result.is_multiple
    True
    >>> list(result)
    ['first', 'second']

    """

    results: tuple[T, ...] = ()

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __bool__(self) -> bool:
        return bool(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __iter__(self) -> Iterator[T]:
        return iter(self.results)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[T, ...]: ...

    def __getitem__(self, index: int | slice) -> T | tuple[T, ...]:
        return self.results[index]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def number_of_results(self) -> int:
        """The number of returned intersection results."""
        return len(self)

    @property
    def is_empty(self) -> bool:
        """Whether the result contains no intersections."""
        return not self

    @property
    def is_single(self) -> bool:
        """Whether the result contains exactly one intersection."""
        return len(self) == 1

    @property
    def is_multiple(self) -> bool:
        """Whether the result contains more than one intersection."""
        return len(self) > 1

    @property
    def is_unique(self) -> bool:
        """Whether exactly one result was returned."""
        return self.is_single
