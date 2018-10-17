from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import random
import json


__all__ = ['moga']


TPL = """
================================================================================
MOGA summary
================================================================================

- fitness function names: {}

- fitnes function types : {}

- number of generations : {}

- number of individuals : {}

- number of variables : {}

- optimal individuals : {}

- optimal fitness values : {}

================================================================================
"""


def moga(fit_functions,
         fit_types,
         num_var,
         boundaries,
         num_gen=100,
         num_pop=100,
         mutation_probability=0.01,
         num_bin_dig=None,
         start_from_gen=False,
         fit_names=None,
         fargs=None,
         fkwargs=None,
         output_path=None):

    """Multi-objective Genetic Algorithm optimisation.

    Parameters
    ----------
    fit_functions : list
        List of functions to be used by the :class'MOGA' to determine the fitness values.
        The function must have as a first argument a list of variables that determine the
        fitness value. Other arguments and keyword arguments can be used to feed
        the function relevant data.
    fit_types : list
        List of strings that indicate if the fitness functions are to be minimized
        or maximized, "min" for minimization and "max" for maximization.
    num_var :  int
        The number of variables used by the fitness function.
    boundaries : list
        The minimum and vaximum values each variable is allowed to have. Must be
        a ``num_var`` long list of tuples in the form [(min, max),...].
    num_gen : int, optional [100]
        The maximum number of generations.
    num_pop : int, optional [100]
        The number of individuals in the population. Must be an even number.
    mutation_probability : float, optional [0.001]
        Float from 0 to 1. If 0 is used, none of the genes in each individuals
        chromosome will be mutated. If 1 is used, all of them will mutate.
    num_bin_dig : list, optional [None]
        Number of genes used to codify each variable. Must be a ``num_var`` long
        list of intergers. If None is given, each variable will be coded with a
        8 digit binary number, corresponding to 256 steps.
    start_from_gen : int, optional [None]
        The generation number to restart a previous optimization process.
    fit_names : list, optional [None]
        The names of the fitness functions. If None is given, the name of the fitness
        functions are used.
    fargs : list, optional [None]
        Arguments fo be fed to the fitness function.
    fkwargs : dict, optional [None]
        Keyword arguments to be fed to the fitness function.
    output_path : str, optional [None]
        Path for the optimization result files.

    Returns
    -------
    moga : object
        The resulting :class'MOGA' instance.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Deb K., *Multi-Objective Optimization using Evolutionary Algorithms*,
           John Wiley & Sons, Chichester, 2001.

    Examples
    --------
    Zitzler-Deb-Thiele Test problem 3

    .. code-block:: python

        import os
        import compas
        import math

        def zdt3_f1(X, a):
            fit = X[0]
            return fit

        def zdt3_f2(X, a):
            n = len(X)
            totX = 0
            for i in range(1, n):
                totX  = totX + X[i]
            G = 1 + (9 / (n - 1)) * totX
            H = 1 - math.sqrt(X[0] / G) - ((X[0] / G) * math.sin(10 * math.pi * X[0]))
            fit = G * H
            return fit

        fit_functions = [zdt3_f1, zdt3_f2]
        fit_types = ['min', 'min']
        num_var = 30
        boundaries = [(0, 1)] * num_var
        num_bin_dig  = [8] * num_var
        output_path = os.path.join(compas.TEMP, 'moga_out/')

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        moga = moga(fit_functions,
                    fit_types,
                    num_var,
                    boundaries,
                    num_gen=100,
                    num_pop=50,
                    num_bin_dig=num_bin_dig,
                    output_path=output_path)

    .. code-block:: none

        ================================================================================
        MOGA summary
        ================================================================================

        - fitness function name: ['zdt3_f1', 'zdt3_f2']

        - fitnes function type : ['min', 'min']

        - number of generations : 100

        - number of individuals : 50

        - number of variables : 30

        - optimal individuals : [0, 1]

        - optimal fitness values : [0.0, -0.7730627737349554]

        ================================================================================

    """

    moga = MOGA()

    moga.fit_names            = fit_names or [ff.__name__ for ff in fit_functions]
    moga.fit_types            = fit_types
    moga.num_gen              = num_gen
    moga.num_pop              = num_pop
    moga.num_var              = num_var
    moga.mutation_probability = mutation_probability
    moga.start_from_gen       = start_from_gen
    moga.boundaries           = boundaries
    moga.num_bin_dig          = num_bin_dig or [8] * num_var
    moga.max_bin_dig          = max(moga.num_bin_dig)
    moga.total_bin_dig        = sum(moga.num_bin_dig)
    moga.fargs                = fargs or {}
    moga.fkwargs              = fkwargs or {}
    moga.fit_functions        = fit_functions
    moga.output_path          = output_path or ''
    moga.num_fit_func         = len(fit_functions)
    moga.moga_optimize()
    return moga


class MOGA(object):
    """This class contains a binary coded, multiple objective genetic algorithm called
    NSGA-II [deb2001]_. NSGA-II uses the concept of non-domination (Pareto-domination) to
    classify solutions and optimize as a genetic algorith. NSGA-II also employs a crowding distance
    operator designed to distribute individuals in the population allong the Pareto
    front, avoid crowding in small areas.

    Attributes
    ----------

    fit_functions : list
        List of functions to be used by the :class'MOGA' to determine the fitness values.
        The function must have as a first argument a list of variables that determine the
        fitness value. Other arguments and keyword arguments can be used to feed
        the function relevant data.
    fit_types : list
        List of strings that indicate if the fitness functions are to be minimized
        or maximized, "min" for minimization and "max" for maximization.
    boundaries : list
        The minimum and vaximum values each variable is allowed to have. Must be
        a ``num_var`` long list of tuples in the form [(min, max),...].
    num_var :  int
        The number of variables used by the fitness function.
    num_pop : int, optional [100]
        The number of individuals in the population. Must be an even number.
    num_gen : int, optional [100]
        The maximum number of generations.
    num_bin_dig : list, optional [None]
        Number of genes used to codify each variable. Must be a ``num_var`` long
        list of intergers. If None is given, each variable will be coded with a
        8 digit binary number, corresponding to 256 steps.
    mutation_probability : float, optional [0.001]
        Float from 0 to 1. If 0 is used, none of the genes in each individuals
        chromosome will be mutated. If 1 is used, all of them will mutate.
    fit_names : list, optional [None]
        The names of the fitness functions. If None is given, the name of the fitness
        functions are used.
    start_from_gen : int, optional [None]
        The generation number to restart a previous optimization process.
    max_bin_digit : int
        The maximum number of binary digits that are used to code a variable values.
        The number of binary digits assigned to code a variable determine the number
        of discrete steps inside the variable bounds. For example, an 8 digit binary
        number will produce 256 steps.
    total_bin_dig : int
        The total number of binary digits.
    num_fit_func : int
        The number of fitness functions.
    output_path : str, optional [None]
        Path for the optimization result files.
    parent_combined_dict : dict
        The combined parent population dictionary.
    parent_pop : dict
        The parent population dictionary.
    current_pop : dict
        The current population dictionary.
    combined_pop : dict
        The combined population dictionary.
    new_pop_cd : list
        The crowding distance list for the newly created population.
    fixed_start_pop : dict
        The user-selected population dictionary for MOGA restarting.
    fargs : list, optional [None]
        Arguments fo be fed to the fitness function.
    fkwargs : dict, optional [None]
        Keyword arguments to be fed to the fitness function.
    ind_fit_dict : dict
        This dictionary keeps track of already evaluated solutions to avoid dupplicate
        fitness function calls.
    """

    def __init__(self):
        """
        # Populations are kept in dictionaries with the following data structure_ansys:
        # pop = {'binary':binary_dict,'decoded':decoded_dict,'scaled':scaled_dict,
        #         'fit_values':fit_values_dict,'pf':pf_dict}
        # binary_dict     = {individual index: {variable index : binary list}}
        # decoded_dict    = {individual index: {variable index : decoded variable}}
        # scaled_dict     = {individual index: {variable index : scaled variable}}
        # fit_values_dict = {individual index: {fit function index : fitness value}}
        # pf_dict         = {individual index: pf number}
        """
        self.fit_functions = []
        self.fit_types = []
        self.boundaries   = {}
        self.num_var = 0
        self.num_pop = 0
        self.num_gen = 0
        self.num_bin_dig = 0
        self.mutation_probability = 0
        self.fit_names = []
        self.start_from_gen = False
        self.max_bin_dig = 0
        self.total_bin_dig = 0
        self.num_fit_func = 0
        self.output_path = []
        self.parent_combined_dict = {}
        self.parent_pop   = {'binary': [], 'decoded': [], 'scaled': [], 'fit_values': [], 'pf': []}
        self.current_pop  = {'binary': [], 'decoded': [], 'scaled': [], 'fit_values': []}
        self.combined_pop = {'binary': [], 'decoded': [], 'scaled': [], 'fit_values': []}
        self.new_pop_cd = []
        self.fixed_start_pop = None  # {'binary':{},'decoded':{},'scaled':{}}
        self.fargs = {}
        self.fkwargs = {}
        self.ind_fit_dict = {}

    def __str__(self):
        """Compile a summary of the MOGA."""
        fit_names = self.fit_names
        fit_types = self.fit_types
        num_gen = self.num_gen
        num_pop = self.num_pop
        num_var = self.num_var
        try:
            fitl = [list(x) for x in zip(*self.parent_pop['fit_values'])]
            best = [self.get_sorting_indices(l, reverse=False)[0] if self.fit_types[i] == 'min' else self.get_sorting_indices(l, reverse=True)[0] for i, l in enumerate(fitl)]
            fit = [min(x) if self.fit_types[i] == 'min' else max(x) for i, x in enumerate(fitl)]
        except(Exception):
            best = None
            fit = None
        return TPL.format(fit_names, fit_types, num_gen, num_pop, num_var, best, fit)

    def summary(self):
        """Print a summary of the MOGA."""
        print(self)

    def moga_optimize(self):
        """This is the main optimization function, this function permorms the multi objective
        GA optimization, performing all genetic operators.
        """
        self.write_moga_json_file()
        if self.start_from_gen:
            self.parent_pop = self.get_pop_from_pf_file()
            start_gen_number = self.start_from_gen + 1
        else:
            start_gen_number = 0
            self.parent_pop['binary'] = self.generate_random_bin_pop()
            self.parent_pop['decoded'] = self.decode_binary_pop(self.parent_pop['binary'])
            self.parent_pop['scaled'] = self.scale_population(self.parent_pop['decoded'])

            if self.fixed_start_pop:
                for i in range(self.fixed_start_pop['num_pop']):
                    # print('fixed start individual', i)
                    # print(self.fixed_start_pop['binary'][i])
                    self.parent_pop['binary'][i] = self.fixed_start_pop['binary'][i]
                    self.parent_pop['decoded'][i] = self.fixed_start_pop['decoded'][i]
                    # print(self.fixed_start_pop['decoded'][i])
                    self.parent_pop['scaled'][i] = self.fixed_start_pop['scaled'][i]
                    # print(self.fixed_start_pop['scaled'][i])
                    # print('')
            self.parent_pop['fit_values'] = [[[]] * self.num_fit_func for i in range(self.num_pop)]
            for i in range(self.num_pop):
                for j in range(self.num_fit_func):
                    fit_func = self.fit_functions[j]
                    self.parent_pop['fit_values'][i][j] = fit_func(self.parent_pop['scaled'][i], **self.fkwargs)

        self.current_pop['binary'] = self.generate_random_bin_pop()

        for generation in range(start_gen_number, self.num_gen):
            print('generation ', generation)

            self.current_pop['decoded'] = self.decode_binary_pop(self.current_pop['binary'])
            self.current_pop['scaled'] = self.scale_population(self.current_pop['decoded'])
            self.current_pop['fit_values'] = [[[]] * self.num_fit_func for i in range(self.num_pop)]
            for i in range(self.num_pop):
                for j in range(self.num_fit_func):
                    fit_func = self.fit_functions[j]
                    self.current_pop['fit_values'][i][j] = fit_func(self.current_pop['scaled'][i], **self.fkwargs)
                    # self.parent_pop['fit_values'][i][j] = self.evaluate_fitness(i, fit_func)

            self.combine_populations()
            self.non_dom_sort()

            for u in range(len(self.pareto_front_indices) - 1):
                self.extract_pareto_front(u)
                self.calculate_crowding_distance()

            self.crowding_distance_sorting()
            self.parent_reseting()
            self.write_out_file(generation)

            if generation < self.num_gen - 1:
                self.nsga_tournament()
                self.create_mating_pool()
                self.simple_crossover()
                self.random_mutation()
            else:
                print(self)

    def evaluate_fitness(self, index, fit_func):
        chromo = ''.join(str(y) for x in self.current_pop['binary'][index] for y in x)
        fit = self.ind_fit_dict.setdefault(chromo, None)
        if not fit:
            fit = fit_func(self.current_pop['scaled'][index], *self.fargs, **self.fkwargs)
            self.ind_fit_dict[chromo] = fit
        return fit

    def write_out_file(self, generation):
        """This function writes a file containing all of the population data for
        the given ``generation``.

        Parameters
        ----------
        generation: int
            The generation to write the population data of.
        """
        filename  = 'generation ' + "%03d" % generation + '_pareto_front' + ".pareto"
        pf_file  = open(self.output_path + (str(filename)), "wb")
        pf_file.write('Generation \n')
        pf_file.write(str(generation) + '\n')
        pf_file.write('\n')

        pf_file.write('Number of individuals per generation\n')
        pf_file.write(str(self.num_pop))
        pf_file.write('\n')
        pf_file.write('\n')

        pf_file.write('Population scaled variables \n')
        for i in range(self.num_pop):
            pf_file.write(str(i) + ',')
            for f in range(self.num_var):
                pf_file.write(str(self.parent_pop['scaled'][i][f]))
                pf_file.write(',')
            pf_file.write('\n')
        pf_file.write('\n')

        pf_file.write('Population fitness values \n')
        for i in range(self.num_pop):
            pf_file.write(str(i) + ',')
            for f in range(self.num_fit_func):
                pf_file.write(str(self.parent_pop['fit_values'][i][f]))
                pf_file.write(',')
            pf_file.write('\n')
        pf_file.write('\n')

        pf_file.write('Population Pareto front indices \n')
        for i in range(self.num_pop):
            pf_file.write(str(i) + ',')
            pf_file.write(str(self.parent_pop['pf'][i]) + '\n')
        pf_file.write('\n')

        pf_file.write('\n')
        pf_file.close()

    def generate_random_bin_pop(self):
        """This function generates a random binary population

        Returns
        -------
        rendom_bin_pop: dict
            The generated random binary population dictionary.
        """

        random_bin_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(self.num_pop):
            for i in range(self.num_var):
                random_bin_pop[j][i] = [random.randint(0, 1) for u in range(self.num_bin_dig[i])]
        return random_bin_pop

    def decode_binary_pop(self, bin_pop):
        """This function decodes the given binary population

        Parameters
        ----------
        bin_pop: dict
            The binary population to decode.

        Returns
        -------
        decoded_pop: dict
            The decoded population dictionary.
        """
        decoded_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(len(bin_pop)):
            decoded_pop[j] = {}
            for i in range(self.num_var):
                value = 0
                chrom = bin_pop[j][i]
                for u, gene in enumerate(chrom):
                    if gene == 1:
                        value = value + 2**u
                decoded_pop[j][i] = value
        return decoded_pop

    def scale_population(self, decoded_pop):
        """Scales the decoded population, variable values are scaled according to each
        of their bounds contained in ``GA.boundaries``.

        Parameters
        ----------
        decoded_pop: list
            The decoded population list.

        Returns
        -------
        scaled_pop: list
            The scaled ppopulation list.
        """
        # scaled_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        # for j in range(self.num_pop):
        #     for i in range(self.num_var):
        #         maxbin = float((2 ** self.num_bin_dig[i]) - 1)
        #         scaled_pop[j][i] = self.boundaries[i][0] + (self.boundaries[i][1] - self.boundaries[i][0]) * decoded_pop[j][i] / maxbin
        # return scaled_pop
        scaled_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(self.num_pop):
            for i in range(self.num_var):
                maxbin = (2 ** self.num_bin_dig[i]) - 1
                scaled_pop[j][i] = decoded_pop[j][i] * (self.boundaries[i][1] - self.boundaries[i][0]) / float((maxbin + self.boundaries[i][0]))
        return scaled_pop

    def combine_populations(self):
        """This function combines the parent population with the current population
        to create a 2 x ``MOGA.num_pop`` long current population.
        """

        self.combined_pop['binary'] = [[[]] * self.num_var for i in range(self.num_pop * 2)]
        self.combined_pop['decoded'] = [[[]] * self.num_var for i in range(self.num_pop * 2)]
        self.combined_pop['scaled'] = [[[]] * self.num_var for i in range(self.num_pop * 2)]
        self.combined_pop['fit_values'] = [[[]] * self.num_fit_func for i in range(self.num_pop * 2)]

        for i in range(self.num_pop):
            self.combined_pop['binary'][i] = self.parent_pop['binary'][i]
            self.combined_pop['binary'][i + self.num_pop] = self.current_pop['binary'][i]

            self.combined_pop['decoded'][i] = self.parent_pop['decoded'][i]
            self.combined_pop['decoded'][i + self.num_pop] = self.current_pop['decoded'][i]

            self.combined_pop['scaled'][i] = self.parent_pop['scaled'][i]
            self.combined_pop['scaled'][i + self.num_pop] = self.current_pop['scaled'][i]

            self.combined_pop['fit_values'][i] = self.parent_pop['fit_values'][i]
            self.combined_pop['fit_values'][i + self.num_pop] = self.current_pop['fit_values'][i]

    def non_dom_sort(self):
        """This function performs the non dominated sorting operator of the NSGA-II
        algorithm. It assigns each individual in the population a Pareto front level,
        according to their fitness values.
        """
        self.domination_count = {}
        self.dominated_set = []
        self.dominating_individuals = []
        self.pareto_front_indices = []
        self.pareto_front_individuals = []

        for i in range(self.num_pop * 2):
            self.domination_count[i] = 0

            for k in range(self.num_pop * 2):
                if i == k:
                    continue
                count_sup = 0
                count_inf = 0
                for j in range(self.num_fit_func):
                    if self.fit_types[j] == 'min':
                        if self.combined_pop['fit_values'][i][j] < self.combined_pop['fit_values'][k][j]:
                            count_sup += 1
                        elif self.combined_pop['fit_values'][i][j] > self.combined_pop['fit_values'][k][j]:
                            count_inf += 1
                    elif self.fit_types[j] == 'max':
                        if self.combined_pop['fit_values'][i][j] > self.combined_pop['fit_values'][k][j]:
                            count_sup += 1
                        elif self.combined_pop['fit_values'][i][j] < self.combined_pop['fit_values'][k][j]:
                            count_inf += 1

                if count_sup < 1 and count_inf >= 1:
                    self.domination_count[i] += 1

                elif count_sup >= 1 and count_inf < 1:
                    self.dominated_set.append(k)
                    self.dominating_individuals.append(i)

        pareto_front_number = 0
        self.pareto_front_indices.append(0)
        while len(self.pareto_front_individuals) < self.num_pop:
            index_count = 0
            for i in range(self.num_pop * 2):
                if self.domination_count[i] == 0:
                    self.pareto_front_individuals.append(i)
                    self.domination_count[i] -= 1
                    index_count += 1

            index = index_count + self.pareto_front_indices[pareto_front_number]
            self.pareto_front_indices.append(index)

            a  = self.pareto_front_indices[pareto_front_number]
            b  = self.pareto_front_indices[pareto_front_number + 1]

            for k in range(a, b):
                for h in range(len(self.dominating_individuals)):
                    if self.pareto_front_individuals[k] == self.dominating_individuals[h]:
                        if self.domination_count[self.dominated_set[h]] >= 0:
                            self.domination_count[self.dominated_set[h]] = self.domination_count[self.dominated_set[h]] - 1

            pareto_front_number += 1

    def extract_pareto_front(self, u):
        """Adds each new level of pareto front individuals to the ``MOGA.i_pareto_front`` list.
        """
        self.i_pareto_front = []
        for i in range(self.pareto_front_indices[u], self.pareto_front_indices[u + 1]):
            self.i_pareto_front.append(self.pareto_front_individuals[i])

    def calculate_crowding_distance(self):
        """This function calculates the crowding distance for all inividuals in the population.
        The crowding distance computes the volume of the hypercube that surrounds each individual
        and whose boundaries are determined by their closest neighbors in the objective space. The
        crowdng distance is used by NSGA-II to better distribute the population allong the Pareto
        front and avoid crowded areas, thus better representing the variety of solutions in the front.
        """
        self.num_i_pareto_front      = len(self.i_pareto_front)
        self.pf_values               = [0] * self.num_i_pareto_front
        self.crowding_distance       = [0] * self.num_i_pareto_front

        for i in range(self.num_fit_func):
            ind_fit_values_list = [fit_val[i] for fit_val in self.combined_pop['fit_values']]
            # print (ind_fit_values_list)
            delta = max(ind_fit_values_list) - min(ind_fit_values_list)
            # print (delta)
            # print()

            for k in range(self.num_i_pareto_front):
                self.pf_values[k] = (self.combined_pop['fit_values'][self.i_pareto_front[k]][i])

            if self.fit_types[i] == 'max':
                self.sorted_indices = self.get_sorting_indices(self.pf_values, reverse=True)
            else:
                self.sorted_indices = self.get_sorting_indices(self.pf_values, reverse=False)

            self.crowding_distance[self.sorted_indices[0]] = float('inf')
            self.crowding_distance[self.sorted_indices[self.num_i_pareto_front - 1]] = float('inf')

            for j in range(1, self.num_i_pareto_front - 1):
                formula = (self.pf_values[self.sorted_indices[j + 1]] - self.pf_values[self.sorted_indices[j - 1]]) / delta
                self.crowding_distance[self.sorted_indices[j]] += formula

        for i in range(self.num_i_pareto_front):
            self.new_pop_cd.append(self.crowding_distance[i])

    def get_sorting_indices(self, l, reverse=False):
        """Reurns the indices that would sort a list of floats.

        Parameters
        ----------
        l: list
            The list of floats to be sorted.
        reverse: bool
            If true the sorting will be done from top to bottom.

        Returns
        -------
        sorting_index: list
            The list of indices that would sort the given list of floats.
        """
        sorting_index = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(l))]
        if reverse is True:
            sorting_index = list(reversed(sorting_index))
        return sorting_index

    def crowding_distance_sorting(self):
        """This function sorts the individuals in the population according
        to their crowding distance.
        """
        cd_sorted_last_pf_index = []
        sorted_last_pf_cd  = sorted(self.crowding_distance)
        sorted_last_pf_cd = list(reversed(sorted_last_pf_cd))
        sorting_index = self.get_sorting_indices(self.crowding_distance, reverse=True)

        for i in range(self.num_i_pareto_front):
            cd_sorted_last_pf_index.append(self.i_pareto_front[sorting_index[i]])

        self.new_pop_cd[len(self.new_pop_cd) - self.num_i_pareto_front:len(self.new_pop_cd)] = sorted_last_pf_cd[:]
        self.pareto_front_individuals[len(self.new_pop_cd) - self.num_i_pareto_front: len(self.new_pop_cd)] = cd_sorted_last_pf_index[:]

    def parent_reseting(self):
        """This function updates the patent population, selecting the individuals that are higher
        in the pareto front level, and have the largest crowding distance.
        """
        self.parent_pop['scaled'] = []
        self.parent_pop['decoded'] = []
        self.parent_combined_dict = {}

        for i in range(self.num_pop):
            self.parent_pop['binary'][i] = self.combined_pop['binary'][self.pareto_front_individuals[i]]
            self.parent_pop['fit_values'][i] = self.combined_pop['fit_values'][self.pareto_front_individuals[i]]
            self.parent_combined_dict[i] = self.pareto_front_individuals[i]

        self.parent_pop['decoded'] = self.decode_binary_pop(self.parent_pop['binary'])
        self.parent_pop['scaled']  = self.scale_population(self.parent_pop['decoded'])
        self.parent_pop['pf'] = self.make_pop_pf_dict()

    def nsga_tournament(self):
        """This function performs the tournament selection operator of the NSGA-II
        algorithm.
        """
        pf_indices_a                = [0] * self.num_pop
        pf_indices_b                = [0] * self.num_pop
        cd_b                        = [0] * self.num_pop
        self.mp_individual_indices  = [0] * self.num_pop

        temp_pf_individuals_a = []
        temp_pf_individuals_a[:]  = self.pareto_front_individuals[0:self.num_pop]
        temp_pf_individuals_b = random.sample(temp_pf_individuals_a, len(temp_pf_individuals_a))

        pf_individuals_2 = []
        indices = []

        cd_a = self.new_pop_cd

        for i in range(self.num_pop):
            while temp_pf_individuals_a[i] == temp_pf_individuals_b[0] and i != self.num_pop - 1:
                temp_pf_individuals_b = random.sample(temp_pf_individuals_b, len(temp_pf_individuals_b))

            pf_individuals_2.append(temp_pf_individuals_b[0])
            del temp_pf_individuals_b[0]
            # t emp_pf_individuals_b = np.delete(tempPFindividualsB,0,0)

        for j in range(len(self.pareto_front_indices) - 1):
            pf_indices_a[self.pareto_front_indices[j]: self.pareto_front_indices[j + 1]] = [j] * (self.pareto_front_indices[j + 1] - self.pareto_front_indices[j])

        for i in range(len(pf_individuals_2)):
            for u in range(len(temp_pf_individuals_a)):
                if pf_individuals_2[i] == temp_pf_individuals_a[u]:
                    indices.append(u)

        for k in range(self.num_pop):
            pf_indices_b[k] = pf_indices_a[indices[k]]

        for k in range(self.num_pop):
            cd_b[k] = cd_a[indices[k]]

        for j in range(self.num_pop):
            if pf_indices_a[j] > pf_indices_b[j]:
                self.mp_individual_indices[j] = pf_individuals_2[j]
            elif pf_indices_a[j] < pf_indices_b[j]:
                self.mp_individual_indices[j] = temp_pf_individuals_a[j]
            else:
                if cd_a[j] > cd_b[j]:
                    self.mp_individual_indices[j] = temp_pf_individuals_a[j]
                elif cd_a[j] < cd_b[j]:
                    self.mp_individual_indices[j] = pf_individuals_2[j]
                else:
                    self.mp_individual_indices[j] = temp_pf_individuals_a[j]

        self.pareto_front_indices       = []
        self.sorted_crowding_distance   = []
        self.new_pop_cd                 = []
        self.dominated_set              = []
        self.dominating_individuals     = []
        self.pareto_front_individuals   = []
        self.new_pop_cd                 = []

    def create_mating_pool(self):
        """Creates two lists of cromosomes to be used by the crossover operator.
        """
        self.mating_pool_a = []
        self.mating_pool_b = []
        for i in range(int(self.num_pop / 2)):
            chrom_a = []
            chrom_b = []
            for j in range(self.num_var):
                chrom_a += self.combined_pop['binary'][self.mp_individual_indices[i]][j]
                chrom_b += self.combined_pop['binary'][self.mp_individual_indices[i + int(self.num_pop / 2)]][j]
            self.mating_pool_a.append(chrom_a)
            self.mating_pool_b.append(chrom_b)

    def simple_crossover(self):
        """Performs the simple crossover operator. Individuals in ``MOGA.mating_pool_a`` are
        combined with individuals in ``MOGA.mating_pool_b`` using a single, randomly selected
        crossover point.
        """
        self.current_pop = {'binary': [], 'decoded': [], 'scaled': [], 'fit_values': []}
        self.current_pop['binary'] = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(int(self.num_pop / 2)):
            cross = random.randint(1, self.total_bin_dig - 1)
            a = self.mating_pool_a[j]
            b = self.mating_pool_b[j]
            c = a[:cross] + b[cross:]
            d = b[:cross] + a[cross:]

            for i in range(self.num_var):
                variable_a = c[:self.num_bin_dig[i]]
                variable_b = d[:self.num_bin_dig[i]]
                del c[:self.num_bin_dig[i]]
                del d[:self.num_bin_dig[i]]
                self.current_pop['binary'][j][i] = variable_a
                self.current_pop['binary'][j + int(self.num_pop / 2)][i] = variable_b

    def random_mutation(self):
        """This mutation operator replaces a gene from 0 to 1 or viceversa
        with a probability of ``MOGA.mutation_probability``.
        """
        for i in range(self.num_pop):
            for j in range(self.num_var):
                for u in range(self.num_bin_dig[j]):
                    random_value = random.random()
                    if random_value < (self.mutation_probability):
                        if self.current_pop['binary'][i][j][u] == 0:
                            self.current_pop['binary'][i][j][u] = 1
                        else:
                            self.current_pop['binary'][i][j][u] = 0

    def get_pop_from_pf_file(self):
        """Reads the pareto front file corresponding to the ``MOGA.start_from_gen``
        generation and returns the saved population data. The pareto front file
        must be in ``GA.output_path``.

        Returns
        -------
        file_pop: dict
            The population dictionary contained in the file.
        """

        file_pop = {'binary': [], 'decoded': [], 'scaled': [], 'fit_values': [],
                    'pf': []}
        filename  = 'generation ' + "%03d" % self.start_from_gen + '_pareto_front' + ".pareto"
        filename = self.output_path + filename
        pf_file = open(filename, 'r')
        lines = pf_file.readlines()
        pf_file.close()

        file_pop['scaled'] = [[[]] * self.num_var for i in range(self.num_pop)]
        file_pop['scaled'] = [[[]] * self.num_fit_func for i in range(self.num_pop)]
        for i in range(self.num_pop):
            line_scaled = lines[i + 7]
            line_fit = lines[i + 9 + self.num_pop]
            line_pf = lines[i + 11 + (self.num_pop * 2)]

            string_scaled = re.split(',', line_scaled)
            string_fit = re.split(',', line_fit)
            string_pf = re.split(',', line_pf)

            del string_scaled[-1]
            del string_scaled[0]
            del string_fit[-1]
            del string_fit[0]

            scaled = [float(j) for j in string_scaled]
            fit_values = [float(j) for j in string_fit]
            pf = int(string_pf[1])

            for j in range(len(scaled)):
                file_pop['scaled'][i][j] = scaled[j]

            for j in range(len(fit_values)):
                file_pop['fit_values'][i][j] = fit_values[j]

            file_pop['pf'][i] = pf

        file_pop['decoded'] = self.unscale_pop(file_pop['scaled'])
        file_pop['binary']  = self.code_decoded(file_pop['decoded'])
        return file_pop

    def code_decoded(self, decoded_pop):
        """Returns a binary coded population from a decoded population

        Parameters
        ----------
        decoded_pop: dict
        The decoded population dictionary to be coded

        Returns
        -------
        binary_pop: dict
            The binary population dictionary.
        """
        binary_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for i in range(len(decoded_pop)):
            binary_pop[i] = {}
            for j in range(self.num_var):
                bin_list = []
                temp_bin = bin(decoded_pop[i][j])[2:]
                temp_bin = temp_bin[::-1]
                digit_dif = self.num_bin_dig[j] - len(temp_bin)
                for h in range(digit_dif):
                    temp_bin = temp_bin + '0'
                for k in range(self.num_bin_dig[j]):
                    bin_list.append(int(temp_bin[k]))
                binary_pop[i][j] = bin_list
        return binary_pop

    def unscale_pop(self, scaled_pop):
        """Returns an unscaled population from a scaled one. The variable values are scaled
        from 0 to x, where x is the highest number described by the number of binary digits
        used to encode that variable. For example, if ``GA.num_bin_dig`` for a variable is 8, that
        variable will be scaled back from its bounds to its corresponding value from 0 to 255.

        Parameters
        ----------
        scaled_pop: dict
            the scaled population dictionary.

        Returns
        -------
        unscaled_pop: dict
            The unscaled population dictionary.
        """
        unscaled_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for i in range(len(scaled_pop)):
            unscaled_pop[i] = {}
            for j in range(self.num_var):
                bin_dig = self.num_bin_dig[j]
                bounds = self.boundaries[j]
                max_unscaled_value = self.get_max_value_from_bin_big(bin_dig)
                dom = abs(bounds[1] - bounds[0])
                value_s = scaled_pop[i][j]
                value = (value_s - bounds[0]) / float(dom)
                unscaled = int(value * max_unscaled_value)
                unscaled_pop[i][j] = unscaled

        return unscaled_pop

    def get_max_value_from_bin_big(self, bin_dig):
        """Returns the highest number described by a ``GA.bin_dig`` long binary number.

        Parameters
        ----------
        bin_dig: int
            The number of digits in the binary number.

        Returns
        -------
        value: int
            The highest number described by a ``GA.bin_dig`` long binary number.
        """
        binary = ''
        for i in range(bin_dig):
            binary += '1'
        value = 0
        for i in range(bin_dig):
            value = value + 2**i
        return value

    def make_pop_pf_dict(self):
        """This function returns a dictionary containing the pareto front level of
        all individuals in the population

        Returns
        -------
        pf_dict: dict
            The dictionary containing the pareto front level of all individuals.
        """
        pf_dict = {}
        for j in range(len(self.pareto_front_indices) - 1):
            pf_ind = self.pareto_front_individuals[self.pareto_front_indices[j]:self.pareto_front_indices[j + 1]]
            for i in range(self.num_pop):
                index = self.parent_combined_dict[i]
                if index in pf_ind:
                    pf_dict[i] = j

        return pf_dict

    def make_moga_input_data(self):
        """Returns a dictionary containing the most relavant genetic data present in the instance
        of ``MOGA``. This is the data required to restart a genetic optimization process or to
        launch a visualization using ``compas_ga.visualization.moga_visualization``.

        Returns
        -------
        data: dict
            A dictionary containing genetic data.
        """
        data = {'num_var': self.num_var,
                'num_pop': self.num_pop,
                'num_gen': self.num_gen,
                'boundaries': self.boundaries,
                'num_bin_dig': self.num_bin_dig,
                'mutation_probability': self.mutation_probability,
                'fit_names': self.fit_names,
                'fit_type': self.fit_types,
                'start_from_gen': self.start_from_gen,
                'max_bin_dig': self.max_bin_dig,
                'total_bin_dig': self.total_bin_dig,
                'num_fit_func': self.num_fit_func,
                'output_path': self.output_path,
                'fixed_start_pop': self.fixed_start_pop
                # 'additional_data':self.additional_data,
                }
        return data

    def make_gen_data(self):
        """Returns a dictionary containing the most relavant genetic data present in the instance
        of ``MOGA`` for the current generation only.

        Returns
        -------
        data: dict
            A dictionary containing genetic data.
        """

        data = {'parent_fit_values': self.parent_pop['fit_values'],
                'parent_scaled': self.parent_pop['scaled'],
                'parent_pf': self.parent_pop['pf']
                }
        return data

    def write_moga_json_file(self):
        """Writes a JSON file containing the most relevant data for MOGA optimization and
        visualization using ``compas_ga.visualization.moga_visualization``.
        """
        data = self.make_moga_input_data()
        filename = ''
        for name in self.fit_names:
            filename += name + '-'
        filename += '.json'
        with open(self.output_path + filename, 'wb+') as fh:
            json.dump(data, fh)

    def write_gen_json_file(self, generation):
        """Writes a JSON file containing the most relevant data for MOGA optimization and
        visualization using ``compas_ga.visualization.ga_visualization`` for the given
        generation ``generation``.

        Parameters
        ----------
        generation : int
            The generation to write the JSON file for.

        """
        data = self.make_gen_data()
        filename = 'generation ' + "%03d" % generation + '_pareto_front' + ".json"
        fh = open(self.output_path + filename, 'wb+')
        json.dump(data, fh)

    def create_fixed_start_pop(self, scaled=None, binary=None):
        """This function creates a population to start the MOGA from a given scaled
        or binary populaiton. This function is used then the start of the MOGA
        should not be with a random population, but with a user defined population.
        The user may chose a binary or a scaled population, one of them must be
        given as a keyword argument. The fixed starting population is saved in
        ``MOGA.fixed_start_pop``. If this function is used, the ``MOGA.moga``
        function will automatically use the ``MOGA.fixed_start_pop`` instead of a
        random population.

        Parameters
        ----------
        scaled: dict
            The scaled population to start the MOGA process from.
        binary: dict
            The binary population to start the MOGA process from.
        """
        self.fixed_start_pop = {'binary': {}, 'decoded': {}, 'scaled': {}, 'num_pop': 0}

        if scaled:
            self.fixed_start_pop['num_pop'] = len(scaled)

            for i in range(self.fixed_start_pop['num_pop']):
                self.fixed_start_pop['scaled'][i] = scaled[i]

            self.fixed_start_pop['decoded'] = self.unscale_pop(self.fixed_start_pop['scaled'])
            self.fixed_start_pop['binary'] = self.code_decoded(self.fixed_start_pop['decoded'])

        if binary:
            self.fixed_start_pop['num_pop'] = len(binary)

            for i in range(self.fixed_start_pop['num_pop']):
                self.fixed_start_pop['binary'][i] = binary[i]

            self.fixed_start_pop['decoded'] = self.decode_binary_pop(self.fixed_start_pop['binary'])
            self.fixed_start_pop['scaled'] = self.scale_population(self.fixed_start_pop['decoded'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import os
    import compas
    import math
    from compas.plotters.mogaplotter import MogaPlotter

    def zdt3_f1(X):
        fit = X[0]
        return fit

    def zdt3_f2(X):
        n = len(X)
        g = 1 + (9. / (n - 1.)) * sum(X[1:])
        h = 1 - math.sqrt(X[0] / g) - ((X[0] / g) * math.sin(10 * math.pi * X[0]))
        fit = g * h
        return fit

    # X = [0.8] * 30
    # X[5] = 0.2
    # print (zdt3_f2(X))

    fit_functions = [zdt3_f1, zdt3_f2]
    fit_types = ['min', 'min']
    num_var = 30
    boundaries = [(0, 1)] * num_var
    num_bin_dig  = [8] * num_var
    output_path = os.path.join(compas.TEMP, 'moga_out/')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    moga_ = moga(fit_functions,
                 fit_types,
                 num_var,
                 boundaries,
                 num_gen=100,
                 num_pop=200,
                 mutation_probability=0.004,
                 num_bin_dig=num_bin_dig,
                 output_path=output_path)

    vis = MogaPlotter()
    vis.input_path = moga_.output_path
    filename = ''
    for name in moga_.fit_names:
        filename += name + '-'
    filename += '.json'
    vis.output_path = vis.input_path
    vis.draw_objective_spaces(filename, number=True)
    print (len(moga_.ind_fit_dict))


    # is crowding distance calculation working?
    # or is the problem simply loss of diversity?
    # - bug on the crossover was found, did this make a big difference? seems to...
