from collections.abc import Callable
from functools import wraps
from inspect import signature
from typing import ParamSpec
from typing import TypeVar

from compas.plugins import pluggable

P = ParamSpec("P")
R = TypeVar("R")


def tessellation_pluggable(
    *,
    category: str,
    inputs: tuple[str, ...],
    result: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a pluggable with the canonical tessellation boundary."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        extension = pluggable(category=category)(func)
        func_signature = signature(func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            from .tessellation import Tessellation

            arguments = func_signature.bind(*args, **kwargs).arguments
            for name in inputs:
                if not isinstance(arguments[name], Tessellation):
                    raise TypeError(f"{name} should be a Tessellation.")
            value = extension(*args, **kwargs)
            if result and not isinstance(value, Tessellation):
                raise TypeError(f"{func.__name__} should return a Tessellation.")
            return value

        return wrapper

    return decorator
