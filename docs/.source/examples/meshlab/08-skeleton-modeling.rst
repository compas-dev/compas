.. _example_mesh-skeleton-modeling:

********************************************************************************
Skeleton mesh modeling
********************************************************************************

.. figure:: /_images/example-mesh-skeleton-modeling.gif
    :figclass: figure
    :class: figure-img img-fluid

.. raw:: html

    <div class="card bg-light">
    <div class="card-body">
    <div class="card-title">Downloads</div>

* :download:`mesh-skeleton-modeling.3dm </../../examples/mesh-skeleton-modeling.3dm>`
* :download:`mesh-skeleton-modeling.py </../../examples/mesh-skeleton-modeling.py>`

.. raw:: html

    </div>
    </div>

.. note::

    The simple implementation shown does not include angle checks between edges 
    meeting in one node. Hence, depending on the diameter of the cross section of 
    the "tubes", the location of the "inner cross sections" and the angles, the 
    code might produce incompatible convex hull geometries and therefore 
    degenerate subdivision meshes.  
 
.. literalinclude:: /../../examples/mesh-subd-modeling.py
