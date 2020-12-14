.. _tut-serialization:

******************
Data Serialization
******************

.. note::

    Work in Progress...

Data serialization is an important component of the cross-platform design of the COMPAS code base,
since it is the basis for data transfer during Remote Procedure Calls with ``compas.rpc``.

It is also the preferred mechanism for writing COMPAS data to files such that it can be retrieved at a later point in time,
or even store information about entire work sessions during iterative processes.

The mechanism is based on serialization to JSON to ensure maximum compatibility with various use cases and circumstances.
All COMPAS data objects (geometry and data structures) implement the interface provided by ``compas.base.Base``,
which forces them to define the methods and properties that form the backbone of the serialization infrastructure.

* :meth:`compas.base.Base.to_data()`
* :meth:`compas.base.Base.from_data()`

* :meth:`compas.base.Base.to_json()`
* :meth:`compas.base.Base.from_json()`

The "from" methods are class methods (``@classmethod``) and act as alternative constructors.
The "to" methods are their counterparts that produce compatible data from object instances.


Explicit serialisation
======================

Create a mesh, convert it do its data representation, and construct a new mesh from that data.

.. code-block:: python

    # to data

    import compas
    from compas.datastructures import Mesh

    mesh1 = Mesh()

    a = mesh1.add_vertex(x=0, y=0, z=0)
    b = mesh1.add_vertex(x=1, y=0, z=0)
    c = mesh1.add_vertex(x=1, y=1, z=0)
    d = mesh1.add_vertex(x=0, y=1, z=0)

    mesh1.add_face([a, b, c, d])

    data = mesh1.to_data()

    # from data

    mesh2 = Mesh.from_data(data)


Implicit serialisation
======================

.. code-block:: python

    # to json

    import math
    import compas
    from compas.geometry import Point, Vector
    from compas.geometry import Frame, Rotation, Translation
    from compas.geometry import Box

    box = Box(Frame.worldXY(), 1, 1, 1)

    R = Rotation.from_axis_angle_vector(Vector(0, 0, 1), math.radians(45))
    T = Translation.from_vector(Vector(2, 0, 0))
    X = T * R

    box.transform(X)

    compas.json_dump([box, X], 'data.json')


.. code-block:: python

    # from json

    import compas
    from compas.geometry import Transformation

    box, X = compas.json_load('data.json')

    T = Transformation.from_frame(box.frame)

    print(T == X)

    box.transform(T.inverse())

    print(box.frame.point)
    print(box.frame.xaxis)
    print(box.frame.yaxis)
    print(box.frame.zaxis)
