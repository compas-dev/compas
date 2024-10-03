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

In most cases, to create a new data type it is sufficient to implement the ``__data__`` property
of your custom data class.

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
are different from the initialisation parameters of the class,
you also have to customise the ``__from_data__`` class method to compensate for the difference.

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


Data schema
===========

Optionally, you can provide a data schema that describes
the internal serialisation data of your class more precisely.

.. code-block:: python

    class CustomData(Data):

        DATASCHEMA = {}

