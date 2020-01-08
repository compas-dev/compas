import os

import pytest

import compas
from compas.files import GLTF

compas.PRECISION = '12f'

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'SimpleMeshes.gltf')


def test_from_gltf_edges_loaded(gltf):
    loaded_gltf = GLTF(gltf)
    assert len(loaded_gltf.parser.scene_data['edges']) > 0


# gltf and bin
#   simple
#   with sparse
#   with morph targets
# gltf with data uri
# glb
