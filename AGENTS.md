# COMPAS Agent Guide

## Goal

Modernize the codebase by:

- removing or upgrading parts related to compatibility with IronPython or older versions of CPython
- adding type hints
- migrating docstrings from Sphinx conventions to mkdocs
- increasing test coverage

## Scope

These instructions apply to the entire repository. Preserve unrelated working-tree changes and keep modernization patches focused.

## Compatibility and Typing

- Support Python 3.9 as declared in `pyproject.toml`.
- Replace Python 2 compatibility forms such as `super(Class, self)` with zero-argument `super()` when touching a class. Preserve explicit arguments to `super(...)` only where they are semantically required, such as selecting a different point in the MRO.
- Use `typing.Union[...]` for type unions in annotations and type comments. Do not use PEP 604 `X | Y` unions for now. The `|` notation may remain in docstrings and prose.
- Prefer annotations that describe what runtime code already accepts. Do not add conversions solely to satisfy a narrow annotation.
- Numeric coordinate and component parameters should be annotated as `float`, not as `Union[float, str]`. Integer arguments are valid for parameters annotated as `float` under Python's numeric typing rules; accepting integers does not require adding strings to the type or adding a runtime conversion.
- Direct `Point` and `Vector` construction may accept two components and default `z` to zero. Coordinate inputs consumed by other geometry objects and their methods must provide all three components; do not add `len(...)` checks that silently promote 2D input to 3D.
- Model fixed-size coordinate data as having three components outside the direct `Point` and `Vector` construction APIs whenever the type system can express that constraint. Do not broaden a fixed-size coordinate alias to an arbitrary-length collection merely to accommodate a lower-level function.
- Geometry objects such as `Point` and `Vector` are iterable and support indexing/unpacking. Pass them directly when an API consumes coordinate iterables; avoid unnecessary `list(...)` allocation.
- Functions in `compas.geometry._core` should be typed against raw numerical data structures and primitives. They should remain unaware of geometry object types and should not import geometry classes.
- Put broadly reusable structural and raw-data typing helpers in `compas._typing`. Keep unions that mention geometry classes, such as `LineType` and `PlaneType`, in `compas.geometry._typing`; define an alias locally only when it is genuinely private to one module.
- At public geometry API boundaries, use the appropriate object-aware union such as `LineType` when callers may pass either a geometry object or raw data. Coordinate-like objects that already satisfy the shared structural `CoordinateType` do not need separate `PointType` or `VectorType` unions. Do not solve boundary typing by progressively broadening every low-level helper.
- When a public method has getter/setter modes or return types controlled by arguments, use overloads to describe the distinct call shapes rather than falling back to `Any`.
- Preserve subclass behavior. Constructors and algorithms that accept or infer `cls` should continue returning the expected subclass.
- Prefer standard library types over typing imports: `list[tuple[...]]` instead of `List[Tuple[...]]`.
- Prefer correcting the source annotation, protocol, or overload over using `cast`. Use `cast` only when the type system cannot express a valid runtime invariant cleanly.
- Avoid broad `Any` unless unavoidable.
- Avoid importing heavy optional dependencies only for typing; use `TYPE_CHECKING` when needed.
- Use `Self` for the return type of (class)methods that return an instance of the current type or a subtype.
- Replace string-quoted return annotations with `Self` whenever the result is the current instance type and subclass preservation is intended. Keep a quoted concrete class only when the method deliberately returns that exact class rather than the receiver's type.

## Runtime-Behavior Preservation

- Modernization should not silently change valid-input behavior, return types, ordering, orientation, side effects, or error behavior.
- Before changing an implementation, compare old and new control flow and identify any equivalence that depends on data-structure invariants.
- Prefer fixing types at API boundaries over changing runtime values inside algorithms.
- When modernization or typing requires a small, non-obvious change to a function body, add a concise comment explaining why the change is necessary and which input contract or invariant it preserves.
- Keep diffs narrow. Do not fold speculative architecture changes into typing, documentation, or compatibility patches.
- Remove obsolete compatibility parameters when their removal is explicitly part of the task instead of preserving hidden aliases or branching logic. Update the implementation, documentation, and tests together.
- Use names that reflect cardinality: a collection of returned points should have a plural name such as `points`, not `point`.
- Keep a short expression on one line when it remains within the formatter's line-length limit and splitting it does not improve readability.

## Tests and Validation

- Use the `compas3` Conda environment for tests and checks.
- Run the smallest relevant test selection first, then broaden validation when practical.
- Use the repository commands documented in `CONTRIBUTING.md`: `invoke test`, `invoke lint`, and `invoke format`. Direct `pytest` and `ruff` invocations are appropriate for focused checks.
- Always run `git diff --check` for changed patches.
- For annotation work, supplement tests with AST/static checks where useful so type comments and less obvious annotation sites are not missed.
- Add direct tests for modernized public classes, including construction, sequence behavior, operators, reflected and in-place operators, property setters, transformations, and subclass-preserving constructors where applicable.
- Prefer behavioral tests over tests that merely assert the presence or shape of implementation metadata.

## Documentation and Public API

- Keep docstrings consistent with the repository's current conventions and Ruff configuration.
- Docstrings are being migrated from Sphinx/reStructuredText markup to MkDocs/mkdocstrings-compatible Markdown. Apply the new convention whenever touching a docstring, even where the surrounding documentation still contains legacy Sphinx files.
- Keep the existing NumPy-style section structure (`Parameters`, `Returns`, `Raises`, `Notes`, `Examples`, `References`, and `See Also`), but write the content of those sections as Markdown.
- Once a function or method parameter is annotated in the signature, omit its type from the docstring's `Parameters` entry. Document the parameter name and description only; do not duplicate signature types in the parameter list.
- Keep explicit types in the `Returns` section even when the return annotation is present in the signature. Mkdocstrings/Griffe otherwise does not parse the return documentation correctly.
- Write return types using the same canonical Python-style syntax as annotations, for example `list[float]`, `list[list[float]]`, `tuple[float, float]`, and `Sequence[float]`. Do not use prose or shorthand forms such as `list of list`, `[float, float, float]`, or `list[[float, float, float]]`.
- When a function returns a tuple, document it as one tuple return entry matching the return annotation, not as separate return entries for each tuple element. Describe the elements and their order in the entry's description.
- Omit the `Returns` section entirely when the function returns `None`. Remove empty `Returns` sections and entries that merely document `None`.
- Do not introduce Sphinx roles or directives such as `:class:`, `:meth:`, `:func:`, `:attr:`, `:mod:`, `.. note::`, or `.. code-block::` in docstrings. Replace existing occurrences in touched docstrings with plain or backticked identifiers, Markdown links, admonitions, and fenced code blocks as appropriate.
- Use single backticks for inline code, literals, parameter names, and identifiers. Use Markdown link syntax (`[label](URL)`) rather than reStructuredText inline links.
- Refer to Python and COMPAS API objects by an unambiguous qualified name when useful; let mkdocstrings resolve supported cross-references rather than embedding Sphinx-specific roles.
- Format `See Also` as a NumPy-style section so Griffe recognizes its `see-also` admonition kind, and use mkdocstrings cross-references for API objects:

  ```text
  See Also
  --------
  [`Mesh.from_obj`][compas.datastructures.Mesh.from_obj] for the inverse operation.
  ```

- Use Markdown footnotes for cited references because the MkDocs `footnotes` extension is enabled. Use descriptive, globally unique footnote labels rather than numeric labels because multiple docstrings can be rendered on one page:

  ```text
  Notes
  -----
  This follows the method described by Nurnberg.[^volume-polyhedron-nurnberg]

  References
  ----------
  [^volume-polyhedron-nurnberg]: [Calculating the Area and Centroid of a Polygon in 2D](https://example.com/paper.pdf)
  ```

- For uncited further reading, use a Markdown list in `References`. Do not use reStructuredText citations such as `[1]_` or `.. [1]`.
- Use `$...$` for inline mathematics and `$$...$$` for display mathematics. Math rendering is provided by `pymdownx.arithmatex` and MathJax; do not use `:math:` roles or `.. math::` directives.
- Keep examples valid as doctests where they are intended to execute. A Markdown migration must not change the example's runtime meaning.
- Document public dunder behavior in the class docstring when it forms part of the user-facing API. Cover ordinary, reflected, and in-place arithmetic variants as applicable, and include a short executable example for each behavior.
- Add short examples for public classmethods that serve as alternative constructors. Do not add `from_data` or implementation-level deserialization hooks to this constructor overview.
- Do not manually add `Attributes` lists to class docstrings when mkdocstrings can generate them from the class members.
- Document every public property on the property's getter. Include setter input, copying, normalization, cache invalidation, and coupled side effects in `Notes` where applicable; properties without setters still require a concise description. Add short executable examples for computed, cached, or otherwise non-obvious behavior.
- Document non-obvious setter side effects. In particular, note when setting one frame axis normalizes it or recomputes another axis to preserve orthonormality.
- Do not expose implementation-only payload, encoder, or helper types without a clear public use case.
- Remove `DATASCHEMA` declarations from modernized objects and remove tests that exist only to validate those declarations. Do not introduce replacement schema metadata unless a current public use case requires it.
- Preserve existing convenience APIs during architectural refactors unless the task explicitly includes a deprecation or breaking-change plan.
- When compatibility requires accepting both documents and native COMPAS objects, make the behavior explicit with overloads or documented wrappers rather than untyped `Any`.
- Remove empty `Examples` sections.
- Except for single-line docstrings, leave a blank line at the end of the docstring.

## Known Modernization Follow-ups

- Before changing the corresponding functions in `compas.linalg.vectors` or `compas.linalg.matrices`, add regression tests and resolve the intended behavior of the following existing edge cases:
  - `vector_variance` currently computes the square root of the variance, and `vector_standard_deviation` takes another square root.
  - `orthonormalize_vectors` tests residual components with `axis > 1e-10` rather than `abs(axis) > 1e-10`, which can discard residuals containing only negative components.
  - `matrix_determinant` and `matrix_inverse` do not correctly support 0x0 or 1x1 matrices.
  - Singular-matrix checks use exact determinant comparisons rather than the repository tolerance policy.
  - `decompose_matrix` is implemented specifically for 4x4 matrices despite broader wording in its docstring.
  - `sum_vectors` treats every axis other than `0` as row-wise summation.
  - Normalization, projection, and rotation helpers need explicit boundary tests for zero-length vectors, zero normals or axes, and projection directions parallel to the target plane.
- Revisit the long-standing `close` and `allclose` deprecations before removing them; preserve the public API unless the work includes an explicit deprecation or breaking-change plan.
