# Contributing to the Documentation

The documentation is written in Markdown and built with MkDocs Material.
API reference pages are generated from Python docstrings with mkdocstrings.

Build the site locally with:

```bash
uv run mkdocs build --strict
```

The convenience task is `uv run invoke docs`; the direct command above is the
required strict check. Preview documentation changes with `uv run mkdocs serve`.

Follow the repository's NumPy-style, MkDocs-compatible docstring conventions.
Keep examples executable and update navigation in `mkdocs.yml` when adding or
moving pages.
