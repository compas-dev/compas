# Implementing a New Data Type

COMPAS data types are classes that are based on [`compas.data.Data`][compas.data.Data].

Data types can be serialized to JSON with

- [`compas.json_dump`][compas.json_dump]
- [`compas.json_dumps`][compas.json_dumps]
- [`compas.json_dumpz`][compas.json_dumpz]

and deserialized with the corresponding "load" functions

- [`compas.json_load`][compas.json_load]
- [`compas.json_loads`][compas.json_loads]
- [`compas.json_loadz`][compas.json_loadz]

All geometry objects and data structures,
and also, for example, the visualization scene,
are serializable data types.

# Creating a new data type

In most cases, it is sufficient to implement the `__data__` property when creating your custom `Data` class.

```python
class SomeThing(Data):

    def __init__(self, a, b)
        super().__init__()
        self.a = a
        self.b = b

    @property
    def __data__(self):
        return {
            "a": self.a,
            "b": self.b,
        }
```

```pycon
>>> custom = SomeThing(a=1, b=2)
>>> compas.json_dump(custom, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result, SomeThing)
True
>>> result.a
1
>>> result.b
2
```

If the attributes stored in the data dictionary defined by the `__data__` property
are different from the initialization parameters of the class,
you must also customize the `__from_data__` class method to compensate for the difference.

`__from_data__` is a reconstruction hook for canonical data produced by the
matching `__data__` property. It may trust invariants already established by the
public constructor and omit repeated normalization or validation. Document such
assumptions clearly, and keep the normal constructor as the entry point for
arbitrary or untrusted values. For example, `Frame.__from_data__` assumes its
stored axes are already orthonormal, whereas `Frame(...)` orthonormalizes
arbitrary input axes.

```python
class SomeThing(Data):

    def __init__(self)
        super().__init__()
        self.items = []

    @property
    def __data__(self):
        return {
            "items": self.items,
        }

    @classmethod
    def __from_data__(cls, data):
        custom = cls()
        for item in data['items']:
            custom.add(item)
        return custom

    def add(self, item):
        self.items.append(item)
```

```pycon
>>> custom = SomeThing()
>>> custom.add(1)
>>> custom.add(2)
>>> compas.json_dump(custom, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result, SomeThing)
True
>>> result.items
[1, 2]
```

# Attribute types

Any attribute that is an instance of a Python base type or a serializable COMPAS data object
can be included in the data dict created by the `__data__` property without further processing.
The serialization process will recursively serialize all these attributes.

```python
class SomeThing(Data):

    def __init__(self, point, frame, mesh):
        super().__init__()
        self.point = point
        self.frame = frame
        self.mesh = mesh

    @property
    def __data__(self):
        return {
            "point": self.point,
            "frame": self.frame,
            "mesh": self.mesh,
        }
```

```pycon
>>> import compas
>>> from compas.geometry import Point, Frame
>>> from compas.datastructures import Mesh
>>> point = Point(1, 2, 3)
>>> frame = Frame()
>>> mesh = Mesh.from_meshgrid(10, 10)
>>> custom = SomeThing(point, frame, mesh)
>>> compas.json_dump(custom, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result.point, Point)
True
>>> isinstance(result.frame, Frame)
True
>>> isinstance(result.mesh, Mesh)
True
>>> result.point == point
True
>>> result.point is point
False
```

Note that the the automatic serialization process will incur overhead information
that increases the size of the resulting JSON file.
The performance impact may be significant when many of these instances are serialized.

To avoid this, anticipated conversions can be included explicitly in `__data__` and `__from_data__`.

```python
class SomeThing(Data):

    def __init__(self, point, frame, mesh):
        super().__init__()
        self.point = point
        self.frame = frame
        self.mesh = mesh

    @property
    def __data__(self):
        return {
            "point": self.point.__data__,
            "frame": self.frame.__data__,
            "mesh": self.mesh.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            Point.__from_data__(data['point']),
            Frame.__from_data__(data['frame']),
            Mesh.__from_data__(data['mesh']),
        )
```
