Implementing a New Data Type
============================

COMPAS data types are classes that are based on :class:`compas.data.Data`.

Data types can be serialised to JSON with

* :func:`compas.json_dump`
* :func:`compas.json_dumps`
* :func:`compas.json_dumpz`

and deserialised with the corresponding "load" functions

* :func:`compas.json_load`
* :func:`compas.json_loads`
* :func:`compas.json_loadz`

All geometry objects and data structures,
and also, for example, the visualisation scene,
are serializable data types.


Creating a new data type
========================

A new data type can be created in a few simple steps.

.. code-block:: python

    class CustomData(Data):

        def __init__(self, a=None, b=None, name=None)
            super().__init__(name=name)
            self.a = a
            self.b = b

        @property
        def __data__(self):
            data = super().__data__
            data['a'] = self.a
            data['b'] = self.b
            return data


>>> data = CustomData(a=1, b=2)
>>> compas.json_dump(data, "custom.json")
>>> result = compas.json_load("custom.json")
>>> isinstance(result, CustomData)
True
>>> result.a
1
>>> result.b
2


Attribute types
===============

More info coming soon...

.. note::

    Note that this process can be further simplified
    by leveraging the ``__annotations__`` infrastructure of Python 3.
    This will be introduced in the next major COMPAS release.


Extending an existing data type
===============================

More info coming soon...


Special Cases
=============

More info coming soon...
