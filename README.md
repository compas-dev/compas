# The COMPAS framework

![build](https://github.com/compas-dev/compas/workflows/build/badge.svg)
[![GitHub - License](https://img.shields.io/github/license/compas-dev/compas.svg)](https://github.com/compas-dev/compas)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/COMPAS.svg)](https://pypi.python.org/project/COMPAS)
[![PyPI - Latest Release](https://img.shields.io/pypi/v/COMPAS.svg)](https://pypi.python.org/project/COMPAS)
[![Conda - Latest Release](https://anaconda.org/conda-forge/compas/badges/version.svg)](https://anaconda.org/conda-forge/compas)
[![DOI](https://zenodo.org/badge/104857648.svg)](https://zenodo.org/badge/latestdoi/104857648)

The **COMPAS** framework is an open-source, Python-based framework for computational research and collaboration in architecture, engineering and digital fabrication.

The main library consists of a core package (**compas**) and several additional
packages for integration of the core functionality in CAD software (currently: **compas_blender**, **compas_rhino**, **compas_ghpython**).

The core package defines all *real* functionality.
The CAD packages simply provide a unified framework for processing, visualising, and interacting with geometry and datastructures, and for building user interfaces in different CAD software.

## Getting Started

The recommended way to install **COMPAS** is to use [Anaconda/conda](https://conda.io/docs/):

```bash
conda config --add channels conda-forge
conda install COMPAS
```

But it can also be installed using `pip`:

```bash
pip install COMPAS
```

To verify your setup, run the following:

```bash
python -m compas
```

## First Steps

* <https://compas.dev/compas/latest/gettingstarted.html>
* <https://compas.dev/compas/latest/tutorial.html>
* <https://compas.dev/compas/latest/api.html>

## Questions and feedback

The **COMPAS** framework has a forum: <https://forum.compas-framework.org/>
for questions and discussions.

## Issue tracker

If you find a bug, please help us solve it by [filing a report](https://github.com/compas-dev/compas/issues).

## Contributing

If you want to contribute, check out the [contribution guidelines](https://compas.dev/compas/latest/devguide.html).

## Changelog

See changes between releases on the [changelog](https://compas.dev/compas/latest/changelog.html).

## License

The main library of **COMPAS** is [released under the MIT license](https://compas.dev/compas/latest/license.html).
