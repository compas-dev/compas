# COMPAS Agent Guide

## Scope and Principles

These instructions apply to the entire repository.

- Keep COMPAS focused on the host-independent core framework. Host integration
  packages such as `compas_rhino`, `compas_ghpython`, and `compas_blender` do
  not belong in this repository.
- Preserve unrelated working-tree changes and keep patches focused.
- Prefer the simplest Python implementation that expresses the required
  contract. Avoid speculative abstractions and compatibility layers.
- Breaking changes are acceptable when they materially improve architecture,
  API consistency, typing, or maintainability. Update internal consumers,
  tests, documentation, serialization contracts, and change notes together.
- Record deferred design work in `TODO.md`; do not mix it into an unrelated
  patch.

## Python and Typing

- Support Python 3.12 and newer, as declared in `pyproject.toml`.
- Use modern Python syntax, zero-argument `super()`, PEP 604 unions, built-in
  generics, and `Self` for subclass-preserving returns.
- Annotate the values accepted by the runtime API. Do not add conversions or
  validation merely to satisfy a type checker.
- Prefer precise structural types and protocols over `Any`, concrete runtime
  type checks, or casts. Use `cast` only when a valid runtime invariant cannot
  be expressed cleanly.
- Use overloads when arguments determine a public return type.
- Use `TYPE_CHECKING` for dependencies imported only for annotations,
  especially optional or heavy dependencies.
- Numeric coordinate components are annotated as `float`; integers are valid
  under Python's numeric typing rules. Do not advertise numeric strings.
- Direct `Point` and `Vector` construction may default a missing `z` component
  to zero. Other coordinate inputs require three components.
- Pass iterable geometry objects such as `Point` and `Vector` directly to APIs
  accepting coordinates; avoid unnecessary collection conversions.
- Put reusable raw-data protocols and aliases in `compas._typing`. Put aliases
  involving geometry classes in `compas.geometry._typing`.
- Keep `compas.geometry._core` independent of geometry classes and typed in
  terms of raw numerical data and primitives.
- At public geometry boundaries, use the appropriate object-aware structural
  alias. Do not broaden low-level helpers to accommodate one high-level caller.

## Python Semantics and Runtime Contracts

- Prefer standard Python protocols, iteration, unpacking, comprehensions,
  context managers, properties, and special methods over custom equivalents.
- Prefer duck typing. Check concrete runtime types only when identity determines
  semantics, resolves a real ambiguity, or protects a documented invariant.
- Use EAFP when the operation already provides the correct failure behavior.
  Add preconditions when attempting the operation could mutate state, obscure
  the public error contract, or make recovery impractical.
- Let indexing, unpacking, arithmetic, dictionary access, and function calls
  raise their natural exceptions instead of duplicating those checks.
- Preserve valid-input behavior, return types, ordering, orientation, side
  effects, and documented errors unless a change is intentional and scoped.
- Prefer fixing an annotation or API boundary over changing values inside an
  algorithm.
- Use names that reflect cardinality and keep short readable expressions on one
  line when they fit the formatter's limit.

## Class Organization

Organize substantial class bodies in this order:

1. data and serialization hooks
2. dunder methods
3. properties
4. alternative constructors
5. conversions
6. regular public methods
7. transformations
8. private helpers

Keep property accessors and overload groups together. Specialized subsections
such as cache management, topology, or geometric components are appropriate
when they improve navigation. Keep small classes compact and do not add empty
or decorative sections.

## Geometry Architecture

- Distinguish defining geometry from discretization and tessellation.
  `vertices`, `edges`, `faces`, `points`, `lines`, and `polygons` describe the
  geometry's representation at a requested resolution. `Tessellation` contains
  visualization-oriented vertices and triangles.
- Direct `to_mesh()` and `to_polygonal_surface()` conversions preserve the
  source topology. Use `geometry.to_tessellation().to_mesh()` or
  `geometry.to_tessellation().to_polygonal_surface()` for triangulated conversions.
- Cache intrinsic geometry, topology, placement, and tessellation independently
  where possible. Placement changes must not force recomputation of unaffected
  local geometry or topology.
- Mutable objects must not use Python `__hash__` as a geometry revision key.
  Use deterministic equality-comparable fingerprints when introducing cache
  invalidation protocols.
- Shapes are bounded solids; they do not inherit from `Surface`. Surface-patch
  composition must preserve seams, poles, parameter directions, boundary
  ownership, analytic normals, UVs, and shared vertices.
- `Line` and `Polyline` are lightweight `Geometry` primitives, not `Curve`
  subclasses. Dedicated parametric wrappers may be introduced separately
  without weakening the `Curve` contract.
- The canonical `NurbsSurface` layout is `control_points[v][u]` and
  `weights[v][u]`, with full mathematical knot vectors. Backend adapters are
  responsible for transposing or translating their native representation.
- Brep functionality is exposed through operations on the shared
  `compas.geometry.Brep` class. Plugins implement operations; they do not
  replace the public class with backend-specific subclasses.
- Prefer NumPy-backed representations where they materially improve processing
  or interoperability, but avoid conversions when a consumer can use existing
  buffers directly.

## Documentation and Public API

- Every direct `compas.*` package initializer defines an explicit `__all__`.
  Imports and `__all__` together define the official public API.
- Write MkDocs/mkdocstrings-compatible NumPy-style docstrings using Markdown.
- Omit parameter types already present in signatures. Keep explicit canonical
  Python types in `Returns` sections.
- Document a tuple as one tuple return matching its annotation. For overloads,
  document each return and the argument condition selecting it.
- Omit `Returns` for functions returning `None`, and remove empty sections.
- Use backticks for code and identifiers, Markdown links and footnotes, and
  `$...$` or `$$...$$` for mathematics. Do not use Sphinx roles, directives,
  citations, or math syntax.
- Format `See Also` as a NumPy-style section using mkdocstrings references.
- Keep executable examples valid as doctests.
- Document public dunder behavior, alternative constructors, and every public
  property. Explain copying, normalization, cache invalidation, and coupled
  setter side effects when relevant.
- Do not add manual `Attributes` sections when mkdocstrings can generate them.
- Do not expose implementation-only payload or helper types without a public
  use case.
- Except for single-line docstrings, leave a blank line before closing quotes.

## Tests and Validation

- Use the `compas3` Conda environment.
- Run the smallest relevant tests first, then broaden validation in proportion
  to risk.
- Use the commands documented in `CONTRIBUTING.md`: `invoke test`,
  `invoke lint`, and `invoke format`. Focused `pytest`, Ruff, and Pyright
  commands are appropriate during development.
- Always run `git diff --check` for changed patches.
- For typing work, supplement runtime tests with focused static or AST checks
  where annotations may otherwise be missed.
- Test public behavior rather than implementation metadata. Cover construction,
  sequence and operator behavior, property setters, transformations, failure
  boundaries, and subclass-preserving constructors as applicable.
- Build the relevant MkDocs pages when changes can affect rendered API
  documentation, signatures, or section parsing.
