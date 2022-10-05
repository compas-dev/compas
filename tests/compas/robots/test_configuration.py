import math
import pytest
import copy

from compas.robots import Joint
from compas.robots import Configuration
from compas.robots.configuration import FixedLengthList


def test_bool():
    config = Configuration(
        joint_values=[1, 2, 3],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    assert config

    config = Configuration(joint_values=[1, 2, 3], joint_types=[Joint.REVOLUTE] * 3)
    assert config

    config = Configuration()
    assert config


def test_len():
    config = Configuration(
        joint_values=[1, 2, 3],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    assert len(config) == 3

    config = Configuration(joint_values=[1, 2, 3], joint_types=[Joint.REVOLUTE] * 3)
    assert len(config) == 0


def test_revolute_ctor():
    q = [4.5, 1.7, 0.5, 2.1, 0.1, 2.1]
    config = Configuration.from_revolute_values(q)
    assert config.joint_types == [Joint.REVOLUTE] * 6

    config = Configuration.from_revolute_values([math.pi / 2, 0.0, 0.0])
    assert [math.degrees(value) for value in config.joint_values] == [90, 0, 0]


def test_prismatic_revolute_ctor():
    config = Configuration.from_prismatic_and_revolute_values([8.312], [1.5, 0.0, 0.0, 0.0, 1.0, 0.8])
    assert config.joint_values == [8.312, 1.5, 0.0, 0.0, 0.0, 1.0, 0.8]
    assert config.joint_types == [Joint.PRISMATIC] + [Joint.REVOLUTE] * 6


def test_ctor():
    values = [1.0, 3.0, 0.1]
    joint_types = [Joint.REVOLUTE, Joint.PRISMATIC, Joint.PLANAR]
    config = Configuration(values, joint_types)
    assert config.joint_values == values
    assert config.joint_types == joint_types


def test_scale():
    values = [1.5, 1.0, 2.0]
    joint_types = [Joint.REVOLUTE, Joint.PRISMATIC, Joint.PLANAR]
    config = Configuration(values, joint_types)
    config.scale(1000.0)

    assert config.joint_values == [1.5, 1000.0, 2000.0]


def test_cast_to_str():
    config = Configuration([math.pi / 2, 3.0, 0.1], [Joint.REVOLUTE, Joint.PRISMATIC, Joint.PLANAR])
    assert str(config) == "Configuration((1.571, 3.000, 0.100), (0, 2, 5))"


def test_from_data():
    config = Configuration.from_data(dict(joint_values=[8.312, 1.5], joint_types=[Joint.PRISMATIC, Joint.REVOLUTE]))
    assert str(config) == "Configuration((8.312, 1.500), (2, 0))"


def test_to_data():
    config = Configuration.from_prismatic_and_revolute_values([8.312], [1.5, 0.0, 0.0, 0.0, 1.0, 0.8])
    # joint_types=[Joint.PRISMATIC, Joint.REVOLUTE]))
    data = config.to_data()

    assert data["joint_values"] == [8.312, 1.5, 0.0, 0.0, 0.0, 1.0, 0.8]
    assert data["joint_types"] == [Joint.PRISMATIC] + [Joint.REVOLUTE] * 6


def test_config_merged():
    config = Configuration(
        joint_values=[1, 2, 3],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    other_config = Configuration(
        joint_values=[3, 2, 0],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "d"],
    )
    new_config = config.merged(other_config)
    assert new_config.joint_dict == {"a": 3, "b": 2, "c": 3, "d": 0}


def test_joint_names():
    with pytest.raises(ValueError):
        config = Configuration(
            joint_values=[1, 2],
            joint_types=[Joint.REVOLUTE] * 2,
            joint_names=["a", "a"],
        )

    config = Configuration(joint_values=[1, 2], joint_types=[Joint.REVOLUTE] * 2, joint_names=["a", "b"])
    with pytest.raises(ValueError):
        config.joint_names = ["a", "a"]

    with pytest.raises(ValueError):
        config.joint_names[1] = config.joint_names[0]


def test_dict_iterables():
    config = Configuration(
        joint_values=[1, 2, 0],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    assert list(config.items()) == [("a", 1), ("b", 2), ("c", 0)]
    assert list(config.keys()) == ["a", "b", "c"]
    assert list(config.values()) == [1, 2, 0]


def test___getitem__():
    config = Configuration(
        joint_values=[1, 2, 0],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    with pytest.raises(KeyError):
        _ = config["DNE"]
    assert config["a"] == 1
    config.joint_values[0] = 4
    assert config["a"] == 4


def test_get():
    config = Configuration(
        joint_values=[1, 2, 0],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    assert config.get("a") == 1
    assert config.get("DNE") is None
    assert config.get("DNE", 5) == 5
    assert config.get("c", 5) == 0


def test_fixed_length():
    config = Configuration(
        joint_values=[1, 2, 0],
        joint_types=[Joint.REVOLUTE] * 3,
        joint_names=["a", "b", "c"],
    )
    with pytest.raises(TypeError):
        config.joint_names.append("d")
    with pytest.raises(TypeError):
        config.joint_types[1:1] = range(5)


def test_fixed_length_list():
    fll = FixedLengthList([1, 2, 3])
    assert len(fll) == 3


def test_fixed_length_list_copy():
    fll = FixedLengthList([[1, 2, 3] for _ in range(3)])
    fll_copy = copy.copy(fll)
    assert fll_copy[0][0] == 1
    fll_copy[0][0] = 0
    assert fll_copy[0][0] == 0
    assert fll[0][0] == 0


def test_fixed_length_list_deepcopy():
    fll = FixedLengthList([[1, 2, 3] for _ in range(3)])
    fll_copy = copy.deepcopy(fll)
    assert fll_copy[0][0] == 1
    fll_copy[0][0] = 0
    assert fll_copy[0][0] == 0
    assert fll[0][0] == 1


def test_configuration_deepcopy():
    c = Configuration([1, 2, 3], [0, 0, 0])
    c_copy = copy.deepcopy(c)
    assert c is not c_copy
    assert c_copy.joint_values[0] == 1
    c_copy.joint_values[0] = 0
    assert c_copy.joint_values[0] == 0
    assert c.joint_values[0] == 1


def test___setitem__():
    fll = FixedLengthList([1, 2, 3])
    fll[2] = 4
    assert fll[2] == 4
    fll[:1] = [5]
    assert fll[0] == 5
    with pytest.raises(TypeError):
        fll[1:1] = range(10)


def test___setitem___with_validator():
    def validator(fixed_length_list, key=None, value=None):
        new_fixed_length_list = list(fixed_length_list)
        if key is not None and value is not None:
            new_fixed_length_list.__setitem__(key, value)
        if len(new_fixed_length_list) != len(set(new_fixed_length_list)):
            raise ValueError("This list cannot have repeated values.")

    fll = FixedLengthList([1, 2, 3], validator=validator)
    with pytest.raises(ValueError):
        _ = FixedLengthList([1, 1, 1], validator=validator)
    fll[2] = 4
    assert fll[2] == 4
    fll[1:] = [0, -1]
    assert fll[0] == 1
    assert fll[1] == 0
    assert fll[2] == -1
    with pytest.raises(TypeError):
        fll[1:1] = range(10)
    with pytest.raises(TypeError):
        fll[1:] = [1]
    with pytest.raises(TypeError):
        fll[:] = [1, 2]
    with pytest.raises(TypeError):
        fll[:1] = [1, 2]
    with pytest.raises(ValueError):
        fll[1] = 1
    with pytest.raises(ValueError):
        fll[1:] = [0, 0]


def test_length_altering_ops():
    fll = FixedLengthList([1, 2, 3])
    with pytest.raises(TypeError):
        fll.append(4)
    with pytest.raises(TypeError):
        fll.extend([4])
    with pytest.raises(TypeError):
        _ = fll.pop()
    with pytest.raises(TypeError):
        fll.clear()
    with pytest.raises(TypeError):
        fll.insert(1, 7)
    with pytest.raises(TypeError):
        fll.remove(1)
    with pytest.raises(TypeError):
        fll.remove(7)
