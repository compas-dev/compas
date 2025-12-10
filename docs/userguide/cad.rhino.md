# Working in Rhino

The core library of COMPAS (`compas`), and the Rhino CAD package (`compas_rhino`)
are backwards compatible with Python 2.7 and written in pure Python,
such that they can be used in Rhino IronPython scripts (Rhino 7 and below),
as well as in the new Rhino CPython scripts (Rhino 8).

## Installation

!!! warning

    These instructions are for Rhino 6 and 7.
    For Rhino 8, please refer to [Rhino 8](cad.rhino8.md).

To use COMPAS in Rhino 6 or 7, you need to make Rhino aware of your COMPAS installation.
This can be done with a simple command on the command line.

!!! note

    Assuming COMPAS is installed in a `conda` environment, make sure to activate the environment before running any of the commands below.
    It is recommended to also close Rhino before running the commands.
    If Rhino was still running, it will have to restarted before the changes take effect.

```bash
python -m compas_rhino.install
```

This will install all Rhino-compatible packages of COMPAS that are present in the current Python environment into Rhino.
It will also automatically install all GH Components that are available for the installed packages.

The default Rhino version is 8.
To install into Rhino 7, use the `-v` flag.

```bash
python -m compas_rhino.install -v 7.0
```

Note that if COMPAS is installed in a `conda` environment, you need to activate the environment before running the command.

```bash
conda activate compas-dev
python -m compas_rhino.install
```

## Verification

To test if the installation was successful, you can run the following script in Rhino.

```python
import compas

print(compas.__version__)
```

## Visualisation

Visualisation of COMPAS objects in Rhino is handled using visualisation scenes.
For more information on visualisation scenes, see [Visualisation](basics.visualisation.md).

```python
import compas
from compas.datastructures import Mesh
from compas.scene import Scene

mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

scene = Scene()
scene.clear()
scene.add(mesh)
scene.draw()
```

## Conversions

For conversion between Rhino objects and COMPAS objects, different scenarios exist.

### Rhino Geometry to COMPAS

Conversions of geometry is straightforward and explicit.

```python
import Rhino.Geometry
import compas_rhino.conversions

point = Rhino.Geometry.Point3d(...)
point = compas_rhino.conversions.point_to_compas(point)

line = Rhino.Geometry.Line(...)
line = compas_rhino.conversions.line_to_compas(line)

plane = Rhino.Geometry.Plane(...)
plane = compas_rhino.conversions.plane_to_compas(plane)

box = Rhino.Geometry.Box(...)
box = compas_rhino.conversions.box_to_compas(box)

mesh = Rhino.Geometry.Mesh(...)
mesh = compas_rhino.conversions.mesh_to_compas(mesh)

curve = Rhino.Geometry.Curve(...)
curve = compas_rhino.conversions.curve_to_compas(curve)

surface = Rhino.Geometry.Surface(...)
surface = compas_rhino.conversions.surface_to_compas(surface)

brep = Rhino.Geometry.Brep(...)
brep = compas_rhino.conversions.brep_to_compas(brep)
```

Note that Rhino doesn't distinguish between a frame and a plane.
Therefore, to convert `Rhino.Geometry.Plane` to `compas.geometry.Frame`:

```python
plane = Rhino.Geometry.Plane(...)
frame = compas_rhino.conversions.plane_to_compas_frame(plane)
```

### Rhino Object to COMPAS

A Rhino Document contains Rhino Objects instead of Rhino Geometry.
The geometry of a Rhino Object is stored in the corresponding attribute (`obj.Geometry`).

Converting point, curve, and mesh objects is straightforward.

```python
import compas_rhino.objects
import compas_rhino.conversions

guid = compas_rhino.objects.select_point()
point = compas_rhino.conversions.pointobject_to_compas(guid)

guid = compas_rhino.objects.select_curve()
curve = compas_rhino.conversions.curveobject_to_compas(guid)

guid = compas_rhino.objects.select_mesh()
mesh = compas_rhino.conversions.meshobject_to_compas(guid)
```

### COMPAS to Rhino Geometry

```python
import compas.geometry
import compas_rhino.conversions

point = compas.geometry.Point(...)
point = compas_rhino.conversions.point_to_rhino(point)

line = compas.geometry.Line(...)
line = compas_rhino.conversions.line_to_rhino(line)

plane = compas.geometry.Plane(...)
plane = compas_rhino.conversions.plane_to_rhino(plane)

box = compas.geometry.Box(...)
box = compas_rhino.conversions.box_to_rhino(box)

curve = compas.geometry.Curve(...)
curve = compas_rhino.conversions.curve_to_rhino(curve)

surface = compas.geometry.Surface(...)
surface = compas_rhino.conversions.surface_to_rhino(surface)

brep = compas.geometry.Brep(...)
brep = compas_rhino.conversions.brep_to_rhino(brep)
```

To convert a `compas.geometry.Frame`:

```python
frame = compas.geometry.Frame(...)
plane = compas_rhino.conversions.frame_to_rhino_plane(frame)
```

### COMPAS to Rhino Object

COMPAS objects are converted to Rhino Objects implicitly, by placing them into a visualisation scene.
However, you can create a Rhino Object in a Rhino Document explicitly from a COMPAS object.

```python
import scriptcontext as sc
import compas.geometry
import compas_rhino.conversions

point = compas.geometry.Point(...)
geometry = compas_rhino.conversions.point_to_rhino(point)

guid = sc.doc.Objects.AddPoint(geometry)
```

## Data Exchange

### JSON

### rhino3dm

## Remote Procedure Calls

## Known Issues
