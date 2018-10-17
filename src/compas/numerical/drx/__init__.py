from __future__ import absolute_import

import importlib


class NotSupportedError(Exception):
    pass


class DynamicRelaxationX(object):
    """Extenced Dynamic relaxation algorithm with different backends.

    Parameters
    ----------
    backend : {'numpy'}, optional
        The backend to use for the algorithm.
        Default is ``'numpy'``.

    Examples
    --------
    ...

    """

    backends = {
        'numpy' : None
    }

    def __init__(self, backend='python'):
        self._backend = None
        self.backend = backend

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend):
        if backend not in self.backends:
            raise NotSupportedError

        m = importlib.import_module(".drx_{}".format(backend), package="compas.numerical.drx")
        f = getattr(m, "drx_{}".format(backend))
        self.backends[backend] = f
        self._backend = backend

    @property
    def solver(self):
        return self.backends[self.backend]

    def __call__(self, structure, callback=None, callback_args=None, **kwargs):
        return self.solver(structure, callback=callback, callback_args=callback_args, **kwargs)


__all__ = ['DynamicRelaxationX']

