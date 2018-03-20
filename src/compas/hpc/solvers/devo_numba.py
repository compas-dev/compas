
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import i8
from numba import jit
from numba import prange

from numpy import argmin
from numpy import array
from numpy import empty
from numpy import min
from numpy.random import rand
from numpy.random import choice


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'devo_numba',
]


args = 0


@jit(nogil=True, nopython=True, parallel=True)
def _fn(u, args):
    # Booth's function, fopt=0, uopt=(1, 3)
    x = u[0]
    y = u[1]
    z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
    return z


@jit((f8[:, :], i8, i8), nogil=True, nopython=True, parallel=False)
def devo_numba(bounds, population, generations):

    """ Call the Numba accelerated Differential Evolution solver.

    Parameters
    ----------
    bounds : array
        Lower and upper bounds for each DoF.
    population : int
        Number of agents in the population.
    generations : int
        Number of cross-over cycles/steps to perform.
    F : float
        Differential evolution parameter.
    CR : float
        Differential evolution cross-over ratio parameter.

    Returns
    -------
    array
        Values that give the optimum (minimised) function.

    """

    # Heading

    print('\n---------------------------------')
    print('Differential Evolution started...')
    print('---------------------------------')

    F = 0.8
    CR = 0.9

    # Setup population

    k = bounds.shape[0]
    agents = rand(k, population)
    for i in prange(k):
        for j in prange(population):
            agents[i, j] *= bounds[i, 1] - bounds[i, 0]
            agents[i, j] += bounds[i, 0]

    candidates = empty((population, population - 1))
    for i in prange(population):
        c = 0
        for j in prange(population - 1):
            if j == i:
                c += 1
            candidates[i, j] = c
            c += 1

    # Initial conditions

    f = empty(population)
    for i in prange(population):
        f[i] = _fn(agents[:, i], args)
    fopt = min(f)
    agents_ = empty((k, population))

    ts = 0
    print('\nGeneration: ', ts, '  fopt: ', fopt)

    # Start evolution

    while ts < generations + 1:

        ind = rand(k, population) < CR

        for i in prange(population):
            choices = choice(population - 1, 3, replace=False)
            ind0 = int(candidates[i, choices[0]])
            ind1 = int(candidates[i, choices[1]])
            ind2 = int(candidates[i, choices[2]])
            ac = agents[:, ind0]
            bc = agents[:, ind1]
            cc = agents[:, ind2]

            for j in prange(k):
                if ind[j, i]:
                    val = ac[j] + F * (bc[j] - cc[j])
                    if val < bounds[j, 0]:
                        val = bounds[j, 0]
                    elif val > bounds[j, 1]:
                        val = bounds[j, 1]
                    agents_[j, i] = val
                else:
                    agents_[j, i] = agents[j, i]

            f_ = _fn(agents_[:, i], args)
            if f_ < f[i]:
                agents[:, i] = agents_[:, i]
                f[i] = f_

        fopt = min(f)
        xopt = agents[:, argmin(f)]

        ts += 1

        print('Generation: ', ts, '  fopt: ', fopt)

    # Summary

    print('\n-------------------------------')
    print('Differential Evolution finished')
    print('fopt: ', fopt)
    print('-------------------------------')

    return xopt


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from time import time

    tic = time()

    bounds = array([[-10., 10.], [-10., 10.]])
    devo_numba(bounds=bounds, population=1000, generations=1000)

    print(time() - tic)
