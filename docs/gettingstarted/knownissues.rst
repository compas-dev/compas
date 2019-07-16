********************************************************************************
Known Issues
********************************************************************************

.. highlight:: bash

Installing Planarity
--------------------

**Problem** The installation of ``Cython`` fails.

Install ```Cython`` separately using pip.

::

    pip install Cython --install-option="--no-cython-compile"


Microsoft Visual C++ Build Tools
--------------------------------

**Problem** Microsoft Visual C++ Build Tools are missing.

To install the Microsoft Visual C++ Build Tools choose one of the options provided
here: https://www.scivision.dev/python-windows-visual-c-14-required/
and just follow the instructions.


Plotter errors
--------------

**Problem** You get an error similar to the following when trying to run
anything involving a `Plotter` (or even just `matplotlib`)

.. code-block:: none

    2019-04-02 16:10:39.181 python[2619:857913] -[NSApplication _setup:]: unrecognized selector sent to instance 0x7f8c389244b0
    2019-04-02 16:10:39.183 python[2619:857913] *** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '-[NSApplication _setup:]: unrecognized selector sent to instance 0x7f8c389244b0'
    *** First throw call stack:
    (
        0   CoreFoundation                      0x00007fff33adbecd __exceptionPreprocess + 256
        1   libobjc.A.dylib                     0x00007fff5fba3720 objc_exception_throw + 48
        2   CoreFoundation                      0x00007fff33b59275 -[NSObject(NSObject) __retain_OA] + 0
        3   CoreFoundation                      0x00007fff33a7db40 ___forwarding___ + 1486
        4   CoreFoundation                      0x00007fff33a7d4e8 _CF_forwarding_prep_0 + 120
        5   libtk8.6.dylib                      0x000000011c566154 TkpInit + 324
        6   libtk8.6.dylib                      0x000000011c4be0ee Initialize + 2622
        7   _tkinter.cpython-37m-darwin.so      0x0000000118bf3a3f _tkinter_create + 1183
        8   python                              0x000000010a706fe6 _PyMethodDef_RawFastCallKeywords + 230
        9   python                              0x000000010a8438b2 call_function + 306
        10  python                              0x000000010a841565 _PyEval_EvalFrameDefault + 46165

        ...

        60  python                              0x000000010a6d942d main + 125
        61  libdyld.dylib                       0x00007fff60c71ed9 start + 1
        62  ???                                 0x0000000000000002 0x0 + 2
    )
    libc++abi.dylib: terminating with uncaught exception of type NSException
    Abort trap: 6


The default python provided in (Ana)conda is not a framework build.
However, a framework build can easily be installed,
both in the main environment and in conda envs:
install python.app (``conda install python.app``)
and use ``pythonw`` rather than ``python`` (https://matplotlib.org/faq/osx_framework.html).

To install python.app when you create an environment do

::

    conda create -n compas-dev -c conda-forge python=3.7 python.app COMPAS


To install python.app in an already existing environment

::

    conda activate compas-dev
    conda install python.app
