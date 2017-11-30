# compas

This is the public repository of the main library of the **compas** framework.
The **compas** framework is an open-source, Python-based framework for computational
research and collaboration in architecture, engineering and digital fabrication.

The main library consists of a core package (**compas**) and several additional
packages for integration of the core functionality in CAD software (**compas_blender**,
**compas_maya** and **compas_rhino**). The core package defines all *real* functionality.
The CAD packages simply provide a unified framework for processing, visualising,
and interacting with datastructures, and for building user interfaces in different
CAD software.

The complete documentation of the compas framework is available here: https://compas-dev.github.io/.


## Getting Started

**compas** does not yet have an installer or setup script. A detailed description
of how to get started by cloning the repository and configuring your system
is available through the documentation: https://compas-dev.github.io/gettingstarted.html

In short:

* clone the repository
* add the compas source folder to your ``PYTHONPATH``
* verify your setup

For example, start Python from the command line, and try

```python
>>> import compas
>>> compas.verify()
```


This will produce something like the following:

```
-------------------------------------------------------------------------------
Checking required packages...

All required packages are installed!

Checking optional packages...

The following optional packages are not installed:
- pycuda
- pyopengl
- pyside

-------------------------------------------------------------------------------
```


## Dependencies

**compas** has very few dependencies and most of them are included in a scientific
Python distribution such as Anaconda or EPD.

| package               | dependencies             | exceptions
| --------------------- | ------------------------ | -------------------------- 
| compas.com            | -                        | matlab (``MatlabEngine``, ``MatlabSession``), paramiko (``ssh``)
| compas.datastructures | -                        |
| compas.files          | -                        |
| compas.geometry       | -                        | NumPy, SciPy (all functions with a ``_numpy`` suffix)
| compas.hpc            | Numba, PyCuda, PyOpenCL  | 
| compas.interop        | -                        |
| compas.numerical      | NumPy, SciPy             |
| compas.plotters       | Matplotlib               |
| compas.topology       | -                        | NumPy, SciPy (all functions with a ``_numpy`` suffix), planarity (``network_is_planar``), NetworkX (``network_embed_in_plane``)
| compas.utilities      | -                        | imageio (``gif_from_images``)
| compas.viewers        | PyOpenGL, PySide         |


## First Steps

Some useful resources for first explorations:

* https://compas-dev.github.io/main/examples.html
* https://compas-dev.github.io/main/tutorial.html
* https://compas-dev.github.io/main/reference.html


## Questions and feedback

The **compas** framework has a forum: http://forum.compas-framework.org/
for questions and discussions.


## Issue tracker

If you find a bug, please [file a report](https://github.com/compas-dev/compas/issues).


## License

The main library of **compas** is [released under the MIT license](https://compas-dev.github.io/license.html).


## Contact

The **compas** framework is developed by the Block Research Group at ETH Zurich,
with the support of the NCCR (National Centre for Competence in Research) in *Digital fabrication*.
Main contributors are Tom Van Mele, Andrew Liew, Tomás Méndez and Matthias Rippmann.

For questions, comments, requests, ..., please [contact the main developers directly](mailto:van.mele@arch.ethz.ch,liew@arch.ethz.ch,mendez@arch.ethz.ch,rippmann@arch.ethz.ch).


