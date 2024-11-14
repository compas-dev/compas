import os
import compas
from compas.topology import unify_cycles

HERE = os.path.dirname(__file__)


def test_unify_cycles():
    test_data = compas.json_load(os.path.join(HERE, "..", "fixtures", "topology", "vertices_faces.json"))
    vertices = test_data["vertices"]
    faces = test_data["faces"]
    unify_cycles(vertices, faces)
    unify_cycles(vertices, faces, nmax=29, radius=22.4)  # anything below won't work
