.. _example_mesh-stanford-armadillo:

********************************************************************************
The Stanford Armadillo
********************************************************************************

.. figure:: /_images/example-mesh-stanford-armadillo.jpg
    :figclass: figure
    :class: figure-img img-fluid

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`mesh-stanford-armadillo.py </_examples/mesh-stanford-armadillo.py>`

.. raw:: html

    </div>
    </div>

.. literalinclude:: /_examples/mesh-stanford-armadillo.py

.. code-block:: none
    
    ply
    format binary_big_endian 1.0
    comment author: Paraform
    obj_info 3D colored patch boundaries
    element vertex 172974
    property float x
    property float y
    property float z
    element face 345944
    property uchar intensity
    property list uchar int vertex_indices
    end_header
