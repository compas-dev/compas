********************************************************************************
Delaunay triangulation
********************************************************************************

.. figure:: mesh-delaunay-from-points.*
    :figclass: figure
    :class: figure-img img-fluid

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`mesh-delaunay.3dm <mesh-delaunay.3dm>`

.. raw:: html

    </div>
    </div>

.. important::

    This delaunay triangulation algorithm works in the xy-plane. However, the
    input can be 3d points resulting in a 2.5d heightfield mesh.


.. literalinclude:: mesh-delaunay-from-points.py

