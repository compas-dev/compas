# Documentation

This section covers how to write and build documentation for COMPAS.

## Building the docs

To build the documentation locally:

```bash
mkdocs serve
```

This will start a local server and you can view the documentation at `http://localhost:8000`.

To build the documentation for deployment:

```bash
mkdocs build
```

## Writing documentation

Documentation is written in Markdown and stored in the `docs/` directory.

### API documentation

API documentation is automatically generated from docstrings using mkdocstrings.

To reference a class or function in the documentation:

```markdown
See [`Point`][compas.geometry.Point] for more information.
```

### Admonitions

Use admonitions to highlight important information:

```markdown
!!! note

    This is a note.

!!! warning

    This is a warning.

!!! tip

    This is a tip.
```
