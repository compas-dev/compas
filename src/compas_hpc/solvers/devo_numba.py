from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import i8
from numba import jit
from numba import prange

from numpy import argsort
from numpy import array
from numpy import min
from numpy import zeros
from numpy.random import rand
from numpy.random import choice


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'devo_numba',
]

# Note: Numba does not currently support a function as an argument, it must already exist and be jitted.

args = ()


@jit(nogil=True, nopython=True, parallel=True)
def fn(u, args):
    # Booth's function, fopt=0, uopt=(1, 3)
    x = u[0]
    y = u[1]
    z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
    return z


@jit(f8[:](f8[:, :], i8, i8, i8), nogil=True, nopython=True, parallel=False, cache=True)
def devo_numba(bounds, population, generations, printout):

    """ Call the Numba accelerated Differential Evolution solver.

    Parameters
    ----------
    bounds : array
        Lower and upper bounds for each DoF [[lb, ub], ...].
    population : int
        Number of agents in the population.
    generations : int
        Number of cross-over cycles/steps to perform.
    printout : int
        Print progress to screen.

    Returns
    -------
    array
        Values that give the optimum (minimized) function.

    """

    # Heading

    if printout:
        print('---------------------------------')
        print('Differential Evolution started...')
        print('---------------------------------')

    F = 0.8
    CR = 0.5

    # Population

    k = bounds.shape[0]
    agents = rand(k, population)
    for i in range(k):
        for j in range(population):
            agents[i, j] *= bounds[i, 1] - bounds[i, 0]
            agents[i, j] += bounds[i, 0]
    agents_ = zeros((k, population))

    candidates = zeros((population, population - 1))
    for i in range(population):
        c = 0
        for j in range(population - 1):
            if j == i:
                c += 1
            candidates[i, j] = c
            c += 1

    # Initial

    f = zeros(population)
    for i in range(population):
        f[i] = fn(agents[:, i], args)
    fopt = min(f)

    ts = 0

    if printout:
        print('Generation: ', ts, '  fopt: ', fopt)

    # Evolution

    while ts < generations + 1:

        ind = rand(k, population) < CR

        for i in prange(population):

            # Pick candidates

            choices = choice(population - 1, 3, replace=False)
            ac = agents[:, int(candidates[i, choices[0]])]
            bc = agents[:, int(candidates[i, choices[1]])]
            cc = agents[:, int(candidates[i, choices[2]])]

            # Update agents

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

            # Update f values

            f_ = fn(agents_[:, i], args)
            if f_ < f[i]:
                agents[:, i] = agents_[:, i]
                f[i] = f_

        fopt = min(f)

        # Reset

        ts += 1

        if printout and (ts % printout == 0):
            print('Generation: ', ts, '  fopt: ', fopt)

    # Summary

    if printout:
        print('-------------------------------')
        print('Differential Evolution finished')
        print('fopt: ', fopt)
        print('-------------------------------')

    return agents[:, argsort(f)[0]]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    bounds = array([[-10., 10.], [-15., 15.]])
    devo_numba(bounds=bounds, population=300, generations=1000, printout=10)
