from abc import abstractmethod

import pytest
import compas
from compas.plugins import IncompletePluginImplError
from compas.plugins import PluginValidator


class TestBaseClass(object):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def bar(self):
        pass

    def baz(self):
        pass


class IncompleteImpl(TestBaseClass):
    def bar(self):
        pass


class CompleteImpl(IncompleteImpl):
    def foo(self):
        pass


def test_ensure_implementations_fails_with_incomplete_impl():
    with pytest.raises(IncompletePluginImplError):
        PluginValidator.ensure_implementations(IncompleteImpl)


def test_ensure_implementations_with_valid_impl():
    PluginValidator.ensure_implementations(CompleteImpl)


def test_dot_net_exception_with_rhino():
    if not compas.RHINO:
        return

    from compas.plugins import DotNetException

    assert DotNetException is not None

    import System

    assert DotNetException == System.Exception


def test_dot_net_exception_without_rhino():
    if compas.RHINO:
        return

    from compas.plugins import DotNetException

    assert DotNetException is not None
    assert issubclass(DotNetException, BaseException)


def test_importer_fail_silently():
    from compas.plugins import Importer

    importer = Importer()

    is_importable = importer.check_importable("compas")
    assert is_importable

    is_importable = importer.check_importable("module_which_does_not_exist")
    assert not is_importable
