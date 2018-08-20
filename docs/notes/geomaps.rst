********************************************************************************
Geometric maps
********************************************************************************

Exercise
--------

Compute the connectivity of a set of lines defined by pairs of point coordinates.


**Lines**

* :download:`lines.json </../../examples/workshops/acadia2017/lines.json>`
* :download:`lines_big.json </../../examples/workshops/acadia2017/lines_big.json>`
* :download:`lines_bigger.json </../../examples/workshops/acadia2017/lines_bigger.json>`


**Approach 1.** Compare the distances between points

* :download:`python_comparison.py </../../examples/workshops/acadia2017/python_distance.py>`

.. code-block:: python

    import json

    with open('lines.json', 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = 0.001

    vertices = []
    edges = []

    for sp, ep in lines:

        # do something magical here


    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))


**Approach 2.** Map points to locations

* :download:`python_geomap.py </../../examples/workshops/acadia2017/python_geomap.py>`

.. code-block:: python

    import json

    with open('lines.json', 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = '3f'

    vertexdict = {}
    edges = []

    for sp, ep in lines:

        # do something magical here


    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))
