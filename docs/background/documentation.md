# Contributing to the Documentation

The documentation is written in Markdown and built with MkDocs Material.
API reference pages are generated from Python docstrings with mkdocstrings.

Build the site locally with:

```bash
invoke docs
```

Follow the repository's NumPy-style, MkDocs-compatible docstring conventions.
Keep examples executable and update navigation in `mkdocs.yml` when adding or
moving pages.
