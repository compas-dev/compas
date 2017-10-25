.. _acadia2017_day2_formfinding_simple:

********************************************************************************
Form Finding - Simple script
********************************************************************************

.. plot:: workshops/acadia2017/day2/formfinding/formfinding_simple-result.py

Before developing a form finding app in Rhino, we will prototype its functionality
using a script and a plotter for visualization.

We will do this in several steps.

First, we use all functionality provided by the framework *out-of-the-box*.
Then, we explore the visualization options, and customize the data structure.
Finally, we find the boundaries of the mesh to change the geometry of the equilibrium result.

Below is the initial version of the code we will further develop.
The parts related to form finding are highlighted.

.. literalinclude:: formfinding_simple.py
    :emphasize-lines: 5, 23-31, 35

