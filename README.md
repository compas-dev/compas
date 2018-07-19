# The COMPAS framework

This is the public repository of the main library of the **COMPAS** framework.
The **COMPAS** framework is an open-source, Python-based framework for computational research and collaboration in architecture, engineering and digital fabrication.

The main library consists of a core package (**compas**) and several additional
packages for integration of the core functionality in CAD software (**compas_blender**, **compas_rhino**, **compas_ghpython**). The core package defines all *real* functionality.
The CAD packages simply provide a unified framework for processing, visualising, and interacting with datastructures, and for building user interfaces in different CAD software.

The complete documentation of the compas framework is available here: https://compas-dev.github.io/.


## Getting Started

The recommended way to install **COMPAS** is to use [Anaconda/conda](https://conda.io/docs/) which takes care of all dependencies:

    conda config --add channels conda-forge
    conda install COMPAS

But it can also be installed using `pip`:

    pip install COMPAS

Once installed, you can verify your setup. Start Python from the command line and run the following:

```python

>>> import compas
>>> import compas_rhino
>>> import compas_blender
>>> import compas_ghpython

```

Optionally, you can also install from source. Check the [documentation for more details](https://compas-dev.github.io/gettingstarted.html).


## First Steps

Some useful resources for first explorations:

* https://compas-dev.github.io/main/examples.html
* https://compas-dev.github.io/main/tutorial.html
* https://compas-dev.github.io/main/reference.html


## Questions and feedback

The **COMPAS** framework has a forum: http://forum.compas-framework.org/
for questions and discussions.


## Issue tracker

If you find a bug, please [file a report](https://github.com/compas-dev/compas/issues).


## Contributing

Make sure you setup your local development environment correctly:

* Clone the [compas](https://github.com/compas-dev/compas) repository.
* Create a virtual environment.
* Install development dependencies:

        pip install -r requirements-dev.txt

**You're ready to start coding!**

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests and checks in one swift command.
* `invoke`: Show available tasks.


### Releasing this project

Ready to release a new version **compas**? Here's how to do it:

* We use [semver](http://semver.org), i.e. we bump versions as follows:

  * `patch`: bugfixes.
  * `minor`: backwards-compatible features added.
  * `major`: backwards-incompatible changes.

* Ready? Release everything:

        invoke release [patch|minor|major]


## License

The main library of **COMPAS** is [released under the MIT license](https://compas-dev.github.io/license.html).


## Contact

The **COMPAS** framework is developed by the Block Research Group at ETH Zurich,
with the support of the NCCR (National Centre for Competence in Research) in *Digital fabrication*.
Main contributors are Tom Van Mele, Andrew Liew, Tomás Méndez and Matthias Rippmann.

For questions, comments, requests, ..., please [contact the main developers directly](mailto:van.mele@arch.ethz.ch,liew@arch.ethz.ch,mendez@arch.ethz.ch,rippmann@arch.ethz.ch).
