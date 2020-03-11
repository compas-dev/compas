********************************************************************************
Geometric Maps
********************************************************************************

Geometric maps provide a simple, but effective way to identify points that can be
considered equal up to a specified precision. A geometric map basically divides
3D space into cubes sized according to the specified resolution. Cubes can only
be sized in discrete steps, each step corresponding to an order of magnitude.
All points within the cube collapse to the corner closest to the origin of the
coordinate system.

A geometric map uses a dictionary to map string representations of XYZ coordinates
to an index in a list, a key in another dictionary, or to an actual geometric location.
The keys of a dictionary form a set. Therefore the keys are unique and lookups in
a dictionary are very fast.


Comparing distances
===================

The concept is best explained with an example. Consider a set of line segments defined
by their start and end point coordinates. To determine how the lines are connected,
we could compute the distance between each point and all other points, identifying
a match as soon as the distance is below a tolerance value.


.. code-block:: python

    import json
    import compas

    with open(compas.get('lines.json'), 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = 0.001
    tol2 = tol ** 2

    vertices = []
    edges = []

    for sp, ep in lines:

        u = None
        v = None

        for i, xyz in enumerate(vertices):

            if u is None:
                # no match has been found for the start point yet

                if (xyz[0] - sp[0]) ** 2 < tol and (xyz[1] - sp[1]) ** 2 < tol and (xyz[2] - sp[2]) ** 2 < tol:
                    u = i

            if v is None:
                # no match has been found for the end point yet

                if (xyz[0] - ep[0]) ** 2 < tol and (xyz[1] - ep[1]) ** 2 < tol and (xyz[2] - ep[2]) ** 2 < tol:
                    v = i

            if u is not None and v is not None:
                # if both points have been found
                # in the current list of vertices
                # iteration can stop
                break

        if u is None:
            # the start point is not in the list of vertices
            # that were already identified

            u = len(vertices)
            vertices.append(sp)

        if v is None:
            # the end point is not in the list of vertices
            # that were already identified

            v = len(vertices)
            vertices.append(ep)

        edges.append((u, v))

    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))


.. note::

    We are not really comparing distances between points, but rather the distance
    per coordinate axis. This has the advantage that when the points don't match
    the calculation gets interrupted faster than when calculating the full spatial
    distance.


Geometric mapping
=================

The code above works fine and is fast enough for small sets of lines.
However, computation time grows exponentially when the number of lines increases.
Therefore, things slow down pretty quickly...

A better way is to use a geometric map.


.. code-block:: python

    import json
    import compas

    with open(compas.get('lines.json'), 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = '3f'

    vertexdict = {}
    edges = []

    for sp, ep in lines:

        a = "{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}".format(sp, tol)
        b = "{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}".format(ep, tol)

        vertexdict[a] = sp
        vertexdict[b] = ep

        edges.append((a, b))

    key_index = {key: index for index, key in enumerate(vertexdict)}

    vertices = list(vertexdict.values())
    edges[:] = [(key_index[a], key_index[b]) for a, b in edges]

    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))
