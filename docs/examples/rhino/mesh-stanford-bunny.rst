********************************************************************************
The Stanford Bunny
********************************************************************************

.. figure:: mesh-stanford-bunny.jpg
    :figclass: figure
    :class: figure-img img-fluid


.. literalinclude:: mesh-stanford-bunny.py

.. code-block:: none

    ply
    format ascii 1.0
    comment zipper output
    element vertex 35947
    property float x
    property float y
    property float z
    property float confidence
    property float intensity
    element face 69451
    property list uchar int vertex_indices
    end_header
