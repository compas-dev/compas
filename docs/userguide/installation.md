# Installation

COMPAS can be easily installed on multiple platforms,
using popular package managers such as conda or pip.

## Install with conda (recommended)

Create an environment named `research` and install COMPAS from the package channel `conda-forge`.

```bash
conda create -n research -c conda-forge compas
```

Activate the environment.

```bash
conda activate research
```

Verify that the installation was successful.

```bash
python -m compas
```

```
Yay! COMPAS is installed correctly!
```

### Installation options

Install COMPAS in an environment with a specific version of Python.

```bash
conda create -n research python=3.9 compas
```

Install COMPAS in an existing environment.

```bash
conda install -n research compas
```

## Install with pip

Install COMPAS using `pip` from the Python Package Index.

```bash
pip install compas
```

Install an editable version from local source.

```bash
cd path/to/compas
pip install -e .
```

## Update with conda

Update COMPAS to the latest version with `conda`.

```bash
conda update compas
```

Install a specific version.

```bash
conda install compas=1.17.9
```

## Update with pip

Update COMPAS to the latest version with `pip`.

```bash
pip install --upgrade compas
```

Install a specific version.

```bash
pip install compas==1.17.9
```
