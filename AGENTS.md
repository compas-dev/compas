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
- Use `typing.Union[...]` for type unions in annotations and type comments. Do not use PEP 604 `X | Y` unions for now. The `|` notation may remain in docstrings and prose.
- Prefer annotations that describe what runtime code already accepts. Do not add conversions solely to satisfy a narrow annotation.
- Geometry objects such as `Point` and `Vector` are iterable and support indexing/unpacking. Pass them directly when an API consumes coordinate iterables; avoid unnecessary `list(...)` allocation.
- When a public method has getter/setter modes or return types controlled by arguments, use overloads to describe the distinct call shapes rather than falling back to `Any`.
- Preserve subclass behavior. Constructors and algorithms that accept or infer `cls` should continue returning the expected subclass.
- Prefer standard library types over typing imports: `list[tuple[...]]` instead of `List[Tuple[...]]`.
- Use `cast` only when absolutely necessary.
- Avoid broad `Any` unless unavoidable.
- Avoid importing heavy optional dependencies only for typing; use `TYPE_CHECKING` when needed.
- Use `Self` for the return type of (class)methods that return an instance of the current type or a subtype.

## Runtime-Behavior Preservation

- Modernization should not silently change valid-input behavior, return types, ordering, orientation, side effects, or error behavior.
- Before changing an implementation, compare old and new control flow and identify any equivalence that depends on data-structure invariants.
- Prefer fixing types at API boundaries over changing runtime values inside algorithms.
- Keep diffs narrow. Do not fold speculative architecture changes into typing, documentation, or compatibility patches.

## Tests and Validation

- Use the `compas3` Conda environment for tests and checks.
- Run the smallest relevant test selection first, then broaden validation when practical.
- Use the repository commands documented in `CONTRIBUTING.md`: `invoke test`, `invoke lint`, and `invoke format`. Direct `pytest` and `ruff` invocations are appropriate for focused checks.
- Always run `git diff --check` for changed patches.
- For annotation work, supplement tests with AST/static checks where useful so type comments and less obvious annotation sites are not missed.

## Documentation and Public API

- Keep docstrings consistent with the repository's current conventions and Ruff configuration.
- Docstrings are being migrated from Sphinx/reStructuredText markup to MkDocs/mkdocstrings-compatible Markdown. Apply the new convention whenever touching a docstring, even where the surrounding documentation still contains legacy Sphinx files.
- Keep the existing NumPy-style section structure (`Parameters`, `Returns`, `Raises`, `Notes`, `Examples`, `References`, and `See Also`), but write the content of those sections as Markdown.
- Once a function or method parameter is annotated in the signature, omit its type from the docstring's `Parameters` entry. Document the parameter name and description only; do not duplicate signature types in the parameter list.
- Keep explicit types in the `Returns` section even when the return annotation is present in the signature. Mkdocstrings/Griffe otherwise does not parse the return documentation correctly.
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

- Keep examples valid as doctests where they are intended to execute. A Markdown migration must not change the example's runtime meaning.
- Do not expose implementation-only payload, encoder, or helper types without a clear public use case.
- Preserve existing convenience APIs during architectural refactors unless the task explicitly includes a deprecation or breaking-change plan.
- When compatibility requires accepting both documents and native COMPAS objects, make the behavior explicit with overloads or documented wrappers rather than untyped `Any`.
