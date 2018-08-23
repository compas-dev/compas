from __future__ import absolute_import


from .dr_python import dr_python
from .dr_numpy import dr_numpy


class NotSupportedError(Exception):
    pass


class DynamicRelaxation(object):

    backends = {
        'python' : dr_python,
        'numpy'  : dr_numpy
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
        self._backend = backend

    @property
    def solver(self):
        return self.backends[self.backend]

    def __call__(self, vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                 callback=None, callback_args=None, **kwargs):
        return self.solver(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                           callback=callback, callback_args=callback_args, **kwargs)


__all__ = ['DynamicRelaxation', 'dr_python', 'dr_numpy']
