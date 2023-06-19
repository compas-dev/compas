from abc import abstractmethod

import pytest

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
