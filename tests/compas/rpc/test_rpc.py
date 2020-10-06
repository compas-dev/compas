# import os

from compas.geometry import allclose
from compas.rpc import Proxy


def test_basic_rpc_call():
    with Proxy('numpy', python='python') as proxy:
        assert proxy.arange(20) == list(range(20))


def test_switch_package():
    with Proxy('numpy', python='python') as proxy:

        A = proxy.array([[1, 2], [3, 4]])

        proxy.package = 'scipy.linalg'
        r = proxy.inv(A)

    assert allclose(r, [[-2, 1], [1.5, -0.5]])
