
from __future__ import print_function

# from compas.numerical.solvers.evolutionary.genetic.visualization.ga_visualization import visualize_evolution

from numpy import array
from numpy import argmin
from numpy import delete
from numpy import eye
from numpy import min
from numpy import newaxis
from numpy import random
from numpy import reshape
from numpy import tile
from numpy import where
from numpy import zeros
from numpy.random import choice

from scipy.optimize import fmin_l_bfgs_b

from time import time

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'devo'
]


def devo(fn, bounds, population, iterations, limit=0, results=None, vectored=False,
         F=0.8, CR=0.9, name='f', polish=False, args=()):
    """Call the differential evolution solver.

    Note:
        fn must return vectorised output for input (k, population) if vectored is True.

    Parameters:
        fn (obj): The function to evaluate and minimise.
        bounds (list): Lower and upper bounds for each DoF.
        population (int): Number of agents in the population.
        iterations (int): Number of cross-over cycles or steps to perform.
        limit (float): Value of the objective function for which to terminate optimisation.
        results (str): Where to store results files.
        vectored (bool): Vectored function output.
        F (float): Differential evolution parameter.
        CR (float): Differential evolution cross-over ratio parameter.
        name (str): Name of the analysis function.
        polish (bool): Polish the final result with L-BFGS-B.
        arg (seq): Sequence of optional arguments to pass to fn.

    Returns:
        float: Optimal value of objective function.
        array: Values that give the optimum (minimised) function.

    Examples:
        >>> def fn(u, *args):
        >>>     # Booth's function, fopt=0, uopt=(1, 3)
        >>>     x = u[0, :]
        >>>     y = u[1, :]
        >>>     z = (x + 2*y - 7)**2 + (2*x + y - 5)**2
        >>>     return z
        >>> bounds = [[-10, 10], [-10, 10]]
        >>> fopt, uopt = de_solver(fn, bounds, population=100, vectored=True, iterations=150, threads=0)
        Iteration: 0 fopt: 9.29475634582
        Iteration: 1 fopt: 0.714845258545
        Iteration: 2 fopt: 0.714845258545
        ...
        Iteration: 148 fopt: 4.22441611201e-22
        Iteration: 149 fopt: 4.22441611201e-22
        Iteration: 150 fopt: 5.18467217924e-23
        >>> print(uopt)
        array([ 1.,  3.])
    """

    # Heading

    tic = time()
    print('\n' + '-' * 50)
    print('Differential Evolution started...')
    print('-' * 50)

    # Setup population

    k = len(bounds)
    bounds = array(bounds)
    b_ran = array(bounds[:, 1] - bounds[:, 0])[:, newaxis]
    b_min = array(bounds[:, 0])[:, newaxis]
    lower_bound = tile(bounds[:, 0][:, newaxis], (1, population))
    upper_bound = tile(bounds[:, 1][:, newaxis], (1, population))
    agents = (random.rand(k, population) * tile(b_ran, (1, population)) + tile(b_min, (1, population)))
    candidates = tile(array(range(population)), (1, population))
    candidates = reshape(delete(candidates, where(eye(population).ravel() == 1)), (population, population - 1))
    ts = 0
    if vectored:
        fun = fn(agents, *args)
    else:
        fun = zeros(population)
        for i in range(population):
            fun[i] = fn(agents[:, i], *args)
    fopt = min(fun)
    print('\nGeneration: {0}  fopt: {1:.5g}'.format(ts, fopt))
    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))

    # Start evolution

    fopt = 10**10
    while (ts < iterations) and (fopt > limit):
        ind = random.rand(k, population) < CR
        for i in range(population):
            inds = candidates[i, choice(population - 1, 3, replace=False)]
            ac[:, i] = agents[:, inds[0]]
            bc[:, i] = agents[:, inds[1]]
            cc[:, i] = agents[:, inds[2]]
        agents_ = ind * (ac + F * (bc - cc)) + ~ind * agents
        log_lower = agents_ < lower_bound
        log_upper = agents_ > upper_bound
        agents_[log_lower] = lower_bound[log_lower]
        agents_[log_upper] = upper_bound[log_upper]
        if vectored:
            fun_ = fn(agents_, *args)
        else:
            fun_ = zeros(population)
            for i in range(population):
                fun_[i] = fn(agents_[:, i], *args)
        log = where((fun - fun_) > 0)[0]
        agents[:, log] = agents_[:, log]
        fun[log] = fun_[log]
        fopt = min(fun)
        xopt = agents[:, argmin(fun)]
        ts += 1
        ac *= 0
        bc *= 0
        cc *= 0
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
                    f.write('{0}, {1}\n'.format(i, fun[i]))
                f.write('\n')

    # L-BFGS-B polish

    if polish:
        opt = fmin_l_bfgs_b(fn, xopt, args=args, approx_grad=1, bounds=bounds, iprint=1, pgtol=10**(-6), factr=10000,
                            maxfun=10**5, maxiter=10**5, maxls=100)
        xopt = opt[0]
        fopt = opt[1]

    # Save parameters

    if results:
        path = results
        parameters = {
            'num_pop': population,
            'fit_name': name,
            'min_fit': None,
            'fit_type': 'min',
            'end_gen': ts - 1,
            'num_gen': iterations - 1,
            'start_from_gen': 0}
        filename = '{0}parameters.json'.format(path)
        with open(filename, 'w+') as fp:
            json.dump(parameters, fp)
        # visualize_evolution(path, path, show_plot=False)

    # Summary

    print('\n' + '-' * 50)
    print('Differential Evolution finished : {0:.4g} s'.format(time() - tic))
    print('fopt: {0:.3g}'.format(fopt))
    print('-' * 50)

    return fopt, xopt


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    def fn(u, *args):
        # Booth's function, fopt=0, uopt=(1, 3)
        x = u[0]
        y = u[1]
        z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
        return z

    bounds = [(-10, 10), (-10, 10)]
    fopt, uopt = devo(fn, bounds, population=20, iterations=20, polish=True)
    print(fopt, uopt)
