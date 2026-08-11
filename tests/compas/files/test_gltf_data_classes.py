from dataclasses import is_dataclass

from compas.files import GLTFDocument
from compas.files import GLTFEncoder
from compas.files.gltf.data_classes import MaterialData
from compas.files.gltf.data_classes import OcclusionTextureInfoData
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.data_classes import SkinData
from compas.files.gltf.data_classes import TextureData
from compas.files.gltf.data_classes import TextureInfoData
from compas.files.gltf.extensions import KHR_materials_pbrSpecularGlossiness
from compas.files.gltf.extensions import KHR_materials_transmission
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf import data_classes
from compas.files.gltf import extensions


def test_semantic_values_are_dataclasses():
    for module in (data_classes, extensions):
        for value in vars(module).values():
            if isinstance(value, type) and issubclass(value, data_classes.BaseGLTFDataClass):
                if value is not data_classes.BaseGLTFDataClass:
                    assert is_dataclass(value)


def test_extension_default_lists_are_independent():
    first = KHR_materials_pbrSpecularGlossiness()
    second = KHR_materials_pbrSpecularGlossiness()

    assert first.diffuse_factor is not None
    first.diffuse_factor[0] = 0.0

    assert second.diffuse_factor == [1.0, 1.0, 1.0, 1.0]


def test_material_uses_specification_property_names():
    document = GLTFDocument()
    document.textures[3] = TextureData()
    document.materials[0] = MaterialData(occlusion_texture=OcclusionTextureInfoData(3), alpha_cutoff=0.25)
    primitive = PrimitiveData(
        {"POSITION": [[0, 0, 0], [1, 0, 0], [0, 1, 0]]},
        [0, 1, 2],
        material=0,
    )
    mesh = GLTFMesh([primitive], document)
    scene = document.add_scene()
    scene.add_child().mesh_key = mesh.key

    data = GLTFEncoder(format="glb").encode(document).json["materials"][0]

    assert data["occlusionTexture"]["index"] == 0
    assert data["alphaCutoff"] == 0.25
    assert "materialTexture" not in data
    assert "alphaFactor" not in data


def test_skin_remaps_skeleton_and_joint_keys():
    document = GLTFDocument()
    scene = document.add_scene()
    root = scene.add_child()
    joint = root.add_child()
    document.skins[0] = SkinData(joints=[root.key, joint.key], skeleton=joint.key)
    root.skin = 0

    data = GLTFEncoder(format="glb").encode(document).json["skins"][0]

    assert data["joints"] == [0, 1]
    assert data["skeleton"] == 1


def test_explicit_extension_traversal_finds_nested_extensions():
    material = MaterialData()
    transmission = KHR_materials_transmission(transmission_texture=TextureInfoData(4))
    material.add_extension(transmission)

    assert material.extension_keys() == {"KHR_materials_transmission"}
    assert any(isinstance(item, TextureInfoData) for item in material.iter_data())


def test_zero_glossiness_is_not_replaced_by_default():
    extension = KHR_materials_pbrSpecularGlossiness(glossiness_factor=0.0)

    assert extension.glossiness_factor == 0.0
