from __future__ import print_function

import os

import pytest

HERE = os.path.dirname(__file__)

if __name__ == '__main__':
    # Fake Rhino modules
    pytest.load_fake_module('Rhino')
    pytest.load_fake_module('Rhino.Geometry', fake_types=['RTree', 'Sphere', 'Point3d'])

    pytest.run(HERE, ['tests/compas/files/test_base_reader.py'])
