from __future__ import absolute_import

import importlib


class NotSupportedError(Exception):
    pass


class ForceDensity(object):
    """Force-density algorithm with different backends.

    Parameters
    ----------
    backend : {'alglib', 'numpy', 'cpp'}, optional
        The backend to use for the algorithm.
        Default is ``'alglib'``.

    Examples
    --------
    ...

    """

    backends = {
        'alglib' : None,
        'numpy'  : None,
        'cpp'    : None,
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

        if not self.backends[backend]:
            m = importlib.import_module(".fd_{}".format(backend), package="compas.numerical.fd")
            f = getattr(m, "fd_{}".format(backend))
            self.backends[backend] = f

        self._backend = backend

    @property
    def solver(self):
        return self.backends[self.backend]

    def __call__(self, vertices, edges, fixed, q, loads, callback=None, callback_args=None, **kwargs):
        return self.solver(vertices, edges, fixed, q, loads, callback=callback, callback_args=callback_args, **kwargs)


__all__ = ['ForceDensity']
