Implementing a New Data Type
============================

COMPAS data types are classes that are based on :class:`compas.data.Data`.

Data types can be serialized to JSON with

* :func:`compas.json_dump`
* :func:`compas.json_dumps`
* :func:`compas.json_dumpz`

and deserialized with the corresponding "load" functions

* :func:`compas.json_load`
* :func:`compas.json_loads`
* :func:`compas.json_loadz`

All geometry objects and data structures,
and also, for example, the visualization scene,
are serializable data types.


Creating a new data type
========================

In most cases, it is sufficient to implement the ``__data__`` property when creating your custom `Data` class.

.. code-block:: python

    class CustomData(Data):

        def __init__(self, a, b, name=None)
            super(CustomData, self).__init__(name=name)
            self.a = a
            self.b = b

        @property
        def __data__(self):
            data = super(CustomData, self).__data__
            data['a'] = self.a
            data['b'] = self.b
            return data


>>> custom = CustomData(a=1, b=2)
>>> compas.json_dump(custom, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result, CustomData)
True
>>> result.a
1
>>> result.b
2

If the attributes stored in the data dictionary defined by the ``__data__`` property
are different from the initialization parameters of the class,
you must also customize the ``__from_data__`` class method to compensate for the difference.

.. code-block:: python

    class CustomData(Data):

        def __init__(self)
            super().__init__()
            # note that if the code needs to be compatible with IronPython
            # you should write the following:
            # super(CustomData, self).__init__()
            self.items = []

        @property
        def __data__(self):
            data = super().__data__
            # note that if the code needs to be compatible with IronPython
            # you should write the following:
            # data = super(CustomData, self).__data__
            data['items'] = self.items
            return data

        @classmethod
        def __from_data__(cls, data):
            custom = cls()
            for item in data['items']:
                custom.add(item)
            return custom

        def add(self, item):
            self.items.append(item)


>>> custom = CustomData()
>>> custom.add(1)
>>> custom.add(2)
>>> compas.json_dump(custom, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result, CustomData)
True
>>> result.items
[1, 2]


Attribute types
===============

Any attribute that is an instance of a Python base type or a serializable COMPAS data object
can be included in the data dict created by the ``__data__`` property without further processing.
The serialization process will recursively serialize all these attributes.

.. code-block:: python

    class CustomData(Data):
        
        def __init__(self, point, frame, mesh, name=None):
            super().__init__(name=name)
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


>>> import compas
>>> from compas.geometry import Point, Frame
>>> from compas.datastructures import Mesh
>>> point = Point(1, 2, 3)
>>> frame = Frame()
>>> mesh = Mesh.from_meshgrid(10, 10)
>>> custom = CustomData(point, frame, mesh)
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


Note that the the automatic serialization process will incur overhead information
that increases the size of the resulting JSON file.
The performance impact may be significant when many of these instances are serialized.

To avoid this, anticipated conversions can be included explicitly in `__data__` and `__from_data__`.

.. code-block:: python

    class CustomData(Data):
        
        def __init__(self, point, frame, mesh, name=None):
            super().__init__(name=name)
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
                Mesh.__from_data__(data['mesh3']),
            )
