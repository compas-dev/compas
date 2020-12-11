.. _tut-serialization:

******************
Data Serialization
******************

* basis for RPC communication
* data persistence
* work sessions
* undo/redo


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
