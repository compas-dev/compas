**************
Data
**************

.. rst-class:: lead

    The data package provides a base class (:class:`compas.data.Data`) for all data objects in the COMPAS framework (see :ref:`Inheritance Diagrams`),
    the mechanism for serialization of data to JSON format,
    and the base infrastructure for validation of the data of COMPAS objects in both the original Python and serialized JSON formats.

::

    >>> from compas.data import Data
    >>> from compas.geometry import Point, Box, Rotation
    >>> from compas.datastructures import Mesh
    >>> from compas.robots import RobotModel

::

    >>> issubclass(Point, Data)
    True
    >>> issubclass(Box, Data)
    True
    >>> issubclass(Rotation, Data)
    True
    >>> issubclass(Mesh, Data)
    True
    >>> issubclass(RobotModel, Data)
    True


.. note::

    This tutorial is loosely based on the COMPAS exchange meeting about :mod:`compas.data` that is available here
    `COMPAS exchange: data <https://github.com/compas-dev/compas-exchange>`_

Interface
=========

The base data class defines a common data interface for all objects.
Among other things, this interface provides a read-only GUID (:attr:`compas.data.Data.guid`),
a modifiable object name (:attr:`compas.data.Data.name`) that defaults to the class name,
a read-only data type (:attr:`compas.data.Data.dtype`),
and, most importantly, an attribute containing the underlying data of the object (:attr:`compas.data.Data.data`).

::

    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> point.guid
    UUID('48613a5b-4c9b-4d7c-8c88-59c28297fd75')
    >>> point.name
    'Point'
    >>> point.dtype
    'compas.geometry/Point'
    >>> point.data
    [0.0, 0.0, 0.0]


JSON Serialization
==================

All objects inheriting the data interface, can be serialized to a JSON string or file.

::

    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> point.to_jsonstring()
    '[0.0, 0.0, 0.0]'
    >>> point.to_json('point.json')

::

    >>> from compas.geometry import Frame
    >>> frame = Frame.worldXY()
    >>> frame.to_jsonstring()
    '{"point": [0.0, 0.0, 0.0], "xaxis": [1.0, 0.0, 0.0], "yaxis": [0.0, 1.0, 0.0]}'
    >>> frame.to_json('frame.json')

Conversely, COMPAS data objects can be reconstructed from a compatible JSON string or file.

::

    >>> from compas.geometry import Frame, Box
    >>> box = Box(Frame.worldXY(), 1, 1, 1)
    >>> jsonstring = box.to_jsonstring()
    >>> other = Box.from_jsonstring(jsonstring)
    >>> box == other
    True

::

    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj('faces.obj')
    >>> mesh.to_json('mesh.json')
    >>> other = Mesh.from_json('mesh.json')

The serialization mechanism applies recursively to nested structures of objects as well.

::

    >>> from compas.datastructures import Network, Mesh
    >>> from compas.geometry import Point, Transformation, Box, Frame
    >>> point = Point(0, 0, 0)
    >>> xform = Transformation()
    >>> mesh = Mesh.from_shape(Box(Frame.worldXY(), 1, 1, 1))
    >>> network = Network()
    >>> a = network.add_node(point=point)
    >>> b = network.add_node(transformation=xform)
    >>> c = network.add_node(box=mesh)
    >>> network.to_json('network.json')

::

    >>> other = Network.from_json('network.json')
    >>> other.node_attribute(a, 'point') == network.node_attribute(a, 'point')
    True
    >>> other.node_attribute(b, 'transformation') == network.node_attribute(b, 'transformation')
    True


Working Sessions
================

One of the most useful features of the serialization meshanisms provided by the data package is the ability to store and load entire COMPAS working sessions.

.. code-block:: python

    # script A

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import Pointcloud, Box

    box = Box.from_width_height_depth(1, 1, 1)
    mesh = Mesh.from_poyhedron(12)

    boxes = []
    for point in Pointcloud.from_bounds(10, 10, 10, 100):
        boxcopy = box.copy()
        boxcopy.frame.point = point

    session = {'mesh': mesh, 'boxes': boxes}
    compas.json_dump(session, 'session.json')

.. code-block:: python

    # script B

    import compas

    session = compas.json_load('session.json')
    mesh = session['mesh']
    boxes = session['boxes']

Note that if you are working in Python 3.6 or higher, you could add some type information to script B
such that your editor knows what kind of objects have been loaded,
which will help with IntelliSense and code completion.

.. code-block:: python

    # script B

    from typing import List
    import compas
    from compas.datastructures import Mesh
    from compas.geometry import Box

    session = compas.json_load('session.json')
    mesh: Mesh = session['mesh']
    boxes: List[Box] = session['boxes']


Validation
==========

A somewhat experimental feature of the data package is data validation.
The base data class defines two unimplemented attributes :attr:`compas.data.Data.JSONSCHEMA` and :attr:`compas.data.Data.DATASCHEMA`.
The former is meant to define the name of the json schema in the ``schema`` folder of :mod:`compas.data`,
and the latter a Python schema using :mod:`schema.Schema`.

If a deriving class implements those attributes, data sources can be validated against the two schemas to verify compatibility
of the available data with the object type.

::

    >>> from compas.data import validate_data
    >>> from compas.geometry import Frame
    >>> data = {'point': [0.0, 0.0, 0.0], 'xaxis': [1.0, 0.0, 0.0], 'zaxis': [0.0, 0.0, 1.0]}
    >>> validate_data(data, Frame)
    Validation against the JSON schema of this object failed.
    Traceback (most recent call last):
       ...

    jsonschema.exceptions.ValidationError: 'yaxis' is a required property

    Failed validating 'required' in schema:
        {'$compas': '1.7.1',
         '$id': 'frame.json',
         '$schema': 'http://json-schema.org/draft-07/schema#',
         'properties': {'point': {'$ref': 'compas.json#/definitions/point'},
                        'xaxis': {'$ref': 'compas.json#/definitions/vector'},
                        'yaxis': {'$ref': 'compas.json#/definitions/vector'}},
         'required': ['point', 'xaxis', 'yaxis'],
         'type': 'object'}

    On instance:
        {'point': [0.0, 0.0, 0.0],
         'xaxis': [1.0, 0.0, 0.0],
         'zaxis': [0.0, 0.0, 1.0]}


Custom Objects
==============

To add a new object class that implements the data interface, only a few attributes have to be implemented.

.. code-block:: python

    class MyObject(Data):

        def __init__(self, a, b, **kwargs):
            super(MyObject, self).__init__(**kwargs)
            self.a = a
            self.b = b

        @property
        def data(self):
            """dict : The data dictionary that represents the data of the object."""
            return {'a': self.a, 'b': self.b}

        @data.setter
        def data(self, data):
            self.a = data['a']
            self.b = data['b']

        @classmethod
        def from_data(cls, data):
            return cls(data['a'], data['b'])


GH Components
=============

*Coming soon...*

Inheritance Diagrams
====================

.. currentmodule:: compas.geometry

.. inheritance-diagram:: Bezier Circle Ellipse Frame Line Plane Point Polygon Polyline Quaternion Vector Box Capsule Cone Cylinder Polyhedron Sphere Torus Projection Reflection Rotation Shear Transformation Translation
    :parts: 1

.. currentmodule:: compas.datastructures

.. inheritance-diagram:: Mesh Network VolMesh
    :parts: 1

.. currentmodule:: compas.robots

.. inheritance-diagram:: RobotModel Joint Link ToolModel Configuration
    :parts: 1
