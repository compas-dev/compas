---
name: update-docstrings
description: Migrate or improve COMPAS Python docstrings using MkDocs-compatible NumPy style without unintentionally changing runtime behavior.
---

# Update COMPAS docstrings

Apply the repository-wide rules in `AGENTS.md`, especially **Documentation and Public API** and **Tests and Validation**.

## Requirements

- Keep NumPy-style sections, but write their content as MkDocs-compatible Markdown.
- Omit parameter types when the signature is annotated. Keep explicit canonical Python types in `Returns`.
- Document each overload return independently and state the argument condition selecting it.
- Document a tuple return as one tuple matching the return annotation.
- Omit `Returns` when the function returns `None`.
- Remove Sphinx roles, directives, citations, and math syntax from every touched docstring. Use backticks, Markdown links, admonitions, fenced code, Markdown footnotes, and `$...$` or `$$...$$` instead.
- Use mkdocstrings cross-references in `See Also` entries when useful.
- Do not add manual class `Attributes` lists that mkdocstrings can generate.
- Document every touched public property on its getter, including copying, normalization, cache invalidation, and coupled setter side effects where applicable.
- Keep public examples short, executable, and valuable. Remove empty `Examples` sections.
- Leave a blank line before the closing quotes of a multiline docstring.
- Do not change runtime behavior while editing documentation.

## Validation

Run focused doctests for executable examples, Ruff on touched Python files, and `git diff --check`. When a rendered API page is affected, build the relevant MkDocs documentation and inspect warnings for signature or section-parsing problems.
