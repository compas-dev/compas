from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

try:
    from numpy import array
    from numpy import argmin
    from numpy import delete
    from numpy import eye
    from numpy import min
    from numpy import newaxis
    from numpy import reshape
    from numpy import tile
    from numpy import where
    from numpy import zeros
    from numpy.random import choice
    from numpy.random import rand

    from scipy.optimize import fmin_l_bfgs_b

except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise

from time import time

import json


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'devo_numpy'
]


def devo_numpy(fn, bounds, population, generations, limit=0, results=None, vectored=False, F=0.8, CR=0.9, polish=False,
               args=(), callback=None, **kwargs):
    """Call the Differential Evolution solver.

    Parameters
    ----------
    fn : obj
        The function to evaluate and minimise.
    bounds : list
        Lower and upper bounds for each DoF [[lb, ub], ...].
    population : int
        Number of agents in the population.
    generations : int
        Number of cross-over cycles/steps to perform.
    limit : float
        Value of the objective function for which to terminate optimisation.
    results : str
        Where to store results files.
    vectored : bool
        Vectored function output.
    F : float
        Differential evolution parameter.
    CR : float
        Differential evolution cross-over ratio parameter.
    polish : bool
        Polish the final result with L-BFGS-B.
    args : seq
        Sequence of optional arguments to pass to fn.
    callback : obj
        Callback function for each generation.

    Returns
    -------
    float
        Optimal value of objective function.
    list
        Values that give the optimum (minimised) function.

    Notes
    -----
    fn must return vectorised output for input (k, population) if vectored is True.

    """
    tic = time()

    # Heading

    print('\n' + '-' * 50)
    print('Differential Evolution started')
    print('-' * 50)

    # Setup bounds

    k = len(bounds)
    bounds = array(bounds)
    b_max = bounds[:, 1][:, newaxis]
    b_min = bounds[:, 0][:, newaxis]
    lb = tile(b_min, (1, population))
    ub = tile(b_max, (1, population))

    # Setup population

    agents = (rand(k, population) * (ub - lb) + lb)
    candidates = tile(array(range(population)), (1, population))
    candidates = reshape(delete(candidates, where(eye(population).ravel() == 1)), (population, population - 1))

    # Initial conditions

    if vectored:
        f = fn(agents, *args)
    else:
        f = zeros(population)
        for i in range(population):
            f[i] = fn(agents[:, i], *args)
    fopt = min(f)

    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))

    ts = 0
    print('\nGeneration: {0}  fopt: {1:.5g}'.format(ts, fopt))

    # Start evolution

    while ts < generations + 1:

        if callback:
            callback(ts, f, **kwargs)

        for i in range(population):
            inds = candidates[i, choice(population - 1, 3, replace=False)]
            ac[:, i] = agents[:, inds[0]]
            bc[:, i] = agents[:, inds[1]]
            cc[:, i] = agents[:, inds[2]]

        ind = rand(k, population) < CR
        agents_ = ind * (ac + F * (bc - cc)) + ~ind * agents
        log_lb = agents_ < lb
        log_ub = agents_ > ub
        agents_[log_lb] = lb[log_lb]
        agents_[log_ub] = ub[log_ub]

        if vectored:
            f_ = fn(agents_, *args)
        else:
            f_ = zeros(population)
            for i in range(population):
                f_[i] = fn(agents_[:, i], *args)

        log = where((f - f_) > 0)[0]
        agents[:, log] = agents_[:, log]
        f[log] = f_[log]
        fopt = min(f)
        xopt = agents[:, argmin(f)]

        ts += 1
        ac *= 0
        bc *= 0
        cc *= 0

        if fopt < limit:
            break

        if ts % 10 == 0:
            print('Generation: {0}  fopt: {1:.5g}'.format(ts, fopt))

        # Save generation

        if results:

            fnm = '{0}generation_{1:0>5}_population.pop'.format(results, ts - 1)
            with open(fnm, 'w') as f:

                f.write('Generation\n')
                f.write('{0}\n\n'.format(ts - 1))

                f.write('Number of individuals per generation\n')
                f.write('{0}\n\n'.format(population))

                f.write('Population scaled variables\n')
                for i in range(population):
                    entry = [str(i)] + [str(j) for j in list(agents[:, i])]
                    f.write(', '.join(entry) + '\n')

                f.write('\nPopulation fitness value\n')
                for i in range(population):
                    f.write('{0}, {1}\n'.format(i, f[i]))

                f.write('\n')

    # L-BFGS-B polish

    if polish:
        opt = fmin_l_bfgs_b(fn, xopt, args=args, approx_grad=1, bounds=bounds, iprint=1, pgtol=10**(-6), factr=10000,
                            maxfun=10**5, maxiter=10**5, maxls=100)
        xopt = opt[0]
        fopt = opt[1]

    # Save parameters

    if results:

        parameters = {
            'num_pop': population,
            'min_fit': limit,
            'fit_type': 'min',
            'end_gen': ts - 1,
            'num_gen': generations - 1,
            'start_from_gen': 0}

        with open('{0}parameters.json'.format(results), 'w+') as fp:
            json.dump(parameters, fp)

    # Summary

    print('\n' + '-' * 50)
    print('Differential Evolution finished : {0:.4g} s'.format(time() - tic))
    print('fopt: {0:.3g}'.format(fopt))
    print('-' * 50 + '\n')

    return fopt, list(xopt)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.plotters.evoplotter import EvoPlotter

    def fn(u, *args):
        # Booth's function, fopt=0, uopt=(1, 3)
        x = u[0]
        y = u[1]
        z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
        return z

    def callback(ts, f, evoplotter):
        evoplotter.update_points(generation=ts, values=f)
        evoplotter.update_lines(generation=ts, values=f)

    evoplotter = EvoPlotter(generations=50, fmax=30, xaxis_div=25, yaxis_div=10, pointsize=0.1)

    bounds = [(-10, 10), (-15, 15)]
    devo_numpy(fn, bounds, population=20, generations=50, polish=False, callback=callback, evoplotter=evoplotter)
