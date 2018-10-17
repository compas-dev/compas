from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import array
    from numpy import argsort
    from numpy import argmin
    from numpy import delete
    from numpy import eye
    from numpy import floor
    from numpy import max
    from numpy import min
    from numpy import newaxis
    from numpy import ones
    from numpy import reshape
    from numpy import tile
    from numpy import where
    from numpy import zeros
    from numpy.random import choice
    from numpy.random import rand

    from matplotlib import pyplot as plt

    from scipy.optimize import fmin_l_bfgs_b

except ImportError:
    compas.raise_if_not_ironpython()

from time import time


__all__ = ['devo_numpy']


def devo_numpy(fn, bounds, population, generations, limit=0, elites=0.2, F=0.8, CR=0.5, polish=False, args=(),
               plot=False, frange=[], printout=10, **kwargs):

    """ Call the Differential Evolution solver.

    Parameters
    ----------
    fn : obj
        The function to evaluate and minimize.
    bounds : list
        Lower and upper bounds for each DoF [[lb, ub], ...].
    population : int
        Number of starting agents in the population.
    generations : int
        Number of cross-over cycles/steps to perform.
    limit : float
        Value of the objective function to terminate optimisation.
    elites : float
        Fraction of elite agents kept.
    F : float
        Differential evolution parameter.
    CR : float
        Differential evolution cross-over ratio parameter.
    polish : bool
        Polish the final result with L-BFGS-B.
    args : seq
        Sequence of optional arguments to pass to fn.
    plot : bool
        Plot progress.
    frange : list
        Minimum and maximum f value to plot.
    printout : int
        Print progress to screen.

    Returns
    -------
    float
        Optimal value of objective function.
    list
        Values that give the optimum (minimized) function.

    """

    tic = time()

    # Heading

    if printout:
        print('\n' + '-' * 50)
        print('Differential Evolution started')
        print('-' * 50)

    # Bounds

    k = len(bounds)
    bounds = array(bounds)
    lb = tile(bounds[:, 0][:, newaxis], (1, population))
    ub = tile(bounds[:, 1][:, newaxis], (1, population))

    # Population

    agents = (rand(k, population) * (ub - lb) + lb)
    candidates = tile(array(range(population)), (1, population))
    candidates = reshape(delete(candidates, where(eye(population).ravel() == 1)), (population, population - 1))

    # Initial

    f = zeros(population)
    for i in range(population):
        f[i] = fn(agents[:, i], *args)
    fopt = min(f)

    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))

    ts = 0
    switch = 1

    if printout:
        print('Generation: {0}  fopt: {1:.5g}'.format(ts, fopt))

    # Set-up plot

    if plot:

        fmin = frange[0] if frange[0] else 0
        fmax = frange[1] if frange[1] else max(fopt)
        ydiv = 100
        dc = 1. / population
        data = ones((ydiv + 1, generations + 1, 3))
        yticks = list(range(0, ydiv + 1, int(ydiv * 0.1)))
        ylabels = ['{0:.1f}'.format(i * (fmax - fmin) * 0.1 + fmin) for i in range(11)]
        aspect = generations / ydiv

        plt.plot([generations * 0.5] * 2, [0, ydiv], ':k')
        plt.yticks(yticks, ylabels, rotation='horizontal')
        plt.ylabel('Value')
        plt.xlabel('Generations')
        plt.ion()

    # Evolution

    while ts < generations + 1:

        # Elites

        if (ts > generations * 0.5) and switch:
            switch = 0

            elite_agents = argsort(f)[:int(floor(elites * population))]
            population = len(elite_agents)
            candidates = tile(array(range(population)), (1, population))
            candidates = reshape(delete(candidates, where(eye(population).ravel() == 1)), (population, population - 1))

            f = f[elite_agents]
            ac = ac[:, elite_agents]
            bc = bc[:, elite_agents]
            cc = cc[:, elite_agents]
            agents = agents[:, elite_agents]

            lb = lb[:, elite_agents]
            ub = ub[:, elite_agents]

        # Update plot

        if plot:

            fsc = (f - fmin) / (fmax - fmin)
            fsc[fsc > 1] = 1
            fsc *= ydiv
            fbin = floor(fsc).astype(int)
            for i in fbin:
                if data[i, ts, 0] == 1:
                    data[i, ts, :] = 0.9 - dc
                else:
                    data[i, ts, :] -= dc
            data[data < 0] = 0
            data[min(fbin), ts, :] = [1, 0, 0]
            data[max(fbin), ts, :] = [0, 0, 1]

            if ts % 10 == 0:
                plt.imshow(data, origin='lower', aspect=aspect)
                plt.plot([generations * 0.5] * 2, [0, ydiv], ':k')
                plt.yticks(yticks, ylabels, rotation='horizontal')
                plt.ylabel('Value')
                plt.xlabel('Generations')
                plt.pause(0.001)

        # Pick candidates

        for i in range(population):
            inds = candidates[i, choice(population - 1, 3, replace=False)]
            ac[:, i] = agents[:, inds[0]]
            bc[:, i] = agents[:, inds[1]]
            cc[:, i] = agents[:, inds[2]]

        # Update agents

        ind = rand(k, population) < CR
        agents_ = ind * (ac + F * (bc - cc)) + ~ind * agents
        log_lb = agents_ < lb
        log_ub = agents_ > ub
        agents_[log_lb] = lb[log_lb]
        agents_[log_ub] = ub[log_ub]

        # Update f values

        f_ = zeros(population)
        for i in range(population):
            f_[i] = fn(agents_[:, i], *args)

        log = where((f - f_) > 0)[0]
        agents[:, log] = agents_[:, log]
        f[log] = f_[log]
        fopt = min(f)
        xopt = agents[:, argmin(f)]

        # Reset

        ts += 1
        ac *= 0
        bc *= 0
        cc *= 0

        if printout and (ts % printout == 0):
            print('Generation: {0}  fopt: {1:.5g}'.format(ts, fopt))

        # Limit check

        if fopt < limit:
            break

    # L-BFGS-B

    if polish:
        opt = fmin_l_bfgs_b(fn, xopt, args=args, approx_grad=1, bounds=bounds, iprint=1, pgtol=10**(-6), factr=10000,
                            maxfun=10**5, maxiter=10**5, maxls=200)
        xopt = opt[0]
        fopt = opt[1]

    # Summary

    if printout:
        print('\n' + '-' * 50)
        print('Differential Evolution finished : {0:.4g} s'.format(time() - tic))
        print('fopt: {0:.5g}'.format(fopt))
        print('-' * 50)

    if plot:
        plt.ioff()
        plt.show()

    return fopt, list(xopt)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    def fn(u, *args):
        # Booth's function, fopt=0, uopt=(1, 3)
        x = u[0]
        y = u[1]
        z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
        return z

    bounds = [(-10, 10), (-15, 15)]
    devo_numpy(fn=fn, bounds=bounds, population=100, generations=100, polish=False, plot=True, frange=[0, 100])
