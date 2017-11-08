from __future__ import print_function
from __future__ import absolute_import

from numba import jit

from numpy import array
from numpy import argmin
from numpy import min
from numpy import random
from numpy import zeros


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


args = 0


@jit(nogil=True, nopython=True)
def numba_devo(bounds, population, iterations):
    """ Call the Numba accelerated differential evolution solver.

    Parameters:
        bounds (array): Lower and upper bounds for each DoF.
        population (int): Number of agents in the population.
        iterations (int): Number of cross-over cycles or steps to perform.

    Returns:
        array: Values that give the optimum (minimised) function.
    """

    F = 0.8
    CR = 0.9

    # Heading

    print('\n---------------------------------')
    print('Differential Evolution started...')
    print('---------------------------------')

    # Setup population

    k = bounds.shape[0]
    agents = random.rand(k, population)
    for i in range(k):
        for j in range(population):
            agents[i, j] *= bounds[i, 1] - bounds[i, 0]
            agents[i, j] += bounds[i, 0]
    candidates = zeros((population, population - 1))
    for i in range(population):
        c = 0
        for j in range(population - 1):
            if j == i:
                c += 1
            candidates[i, j] = c
            c += 1
    ts = 0
    fun = zeros(population)
    for i in range(population):
        fun[i] = _fn(agents[:, i], args)
    fopt = min(fun)

    # print(' ')
    # print('Generation: ', ts, '  fopt: ', fopt)

    # Start evolution

    agents_ = zeros((k, population))
    while ts < iterations:
        ind = random.rand(k, population) < CR
        for i in range(population):
            rands = candidates[i, :]
            random.shuffle(rands)
            ind0 = int(candidates[i, int(rands[0])])
            ind1 = int(candidates[i, int(rands[1])])
            ind2 = int(candidates[i, int(rands[2])])
            ac = agents[:, ind0]
            bc = agents[:, ind1]
            cc = agents[:, ind2]
            for j in range(k):
                if ind[j, i]:
                    agents_[j, i] = ac[j] + F * (bc[j] - cc[j])
            fun_ = _fn(agents_[:, i], args)
            if fun_ < fun[i]:
                agents[:, i] = agents_[:, i]
                fun[i] = fun_
        fopt = min(fun)
        xopt = agents[:, argmin(fun)]
        ts += 1

        # print('Generation: ', ts, '  fopt: ', fopt)

    # Summary

    # print('\n-------------------------------')
    # print('Differential Evolution finished')
    # print('fopt: ', fopt)
    # print('-------------------------------')

    return xopt


@jit(nogil=True, nopython=True)
def _fn(u, args):
    # Booth's function, fopt=0, uopt=(1, 3)
    x = u[0]
    y = u[1]
    z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
    return z


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    bounds = array([[-10., 10.], [-10., 10.]])
    xopt = numba_devo(bounds, population=20, iterations=100)
    print(xopt)
