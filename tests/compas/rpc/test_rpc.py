import os

from compas.geometry import allclose
from compas.rpc import Proxy


def test_basic_rpc_call():
    python_exec = os.environ.get('TRAVIS_RPC_PYTHON_EXE')
    with Proxy('numpy', python=python_exec) as p:
        assert p.arange(20) == list(range(20))


def test_switch_package():
    python_exec = os.environ.get('TRAVIS_RPC_PYTHON_EXE')
    with Proxy('numpy', python=python_exec) as proxy:

        A = proxy.array([[1, 2], [3, 4]])

        proxy.package = 'scipy.linalg'
        r = proxy.inv(A)

    assert allclose(r, [[-2, 1], [1.5, -0.5]])
