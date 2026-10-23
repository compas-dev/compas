---
name: update-type-hints
description: Add, modernize, or review Python type hints in COMPAS for Python 3.12+ without unintentionally changing runtime behavior.
---

# Update COMPAS type hints

Apply the repository-wide rules in `AGENTS.md`, especially **Compatibility and Typing**, **Runtime-Behavior Preservation**, and **Tests and Validation**.

## Requirements

- Use Python 3.12 syntax, including `X | Y` and `X | None` instead of `Union` and `Optional`.
- Prefer built-in generics such as `list[tuple[...]]` over legacy `typing` aliases.
- Use `Self` for methods and classmethods that preserve the receiver or subclass type.
- Use overloads for argument-dependent public return types instead of `Any`.
- Model the values accepted by the existing runtime API; do not add conversions or validation merely to satisfy an annotation.
- Keep low-level `compas.geometry._core` annotations based on raw numerical data and primitives. Keep geometry-aware unions at public geometry boundaries.
- Prefer correcting a protocol, alias, overload, or source annotation over using `cast`. Avoid broad `Any`.
- Put reusable raw-data protocols and aliases in `compas._typing`, and geometry-aware aliases in `compas.geometry._typing`.
- Avoid runtime imports of optional or heavy dependencies used only for typing; use `TYPE_CHECKING` when necessary.
- Preserve subclass behavior, defaults, accepted inputs, return values, ordering, side effects, and exception behavior unless the task explicitly authorizes a change.

## Validation

Run the narrowest relevant tests first. Run Pyright or an equivalent focused static check for changed annotations, Ruff on touched Python files, and `git diff --check`. Use AST-based searches when type comments or less obvious annotation sites may remain.
