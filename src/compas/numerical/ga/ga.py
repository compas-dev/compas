from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import random
import json
import copy


__all__ = ['ga']


TPL = """
================================================================================
GA summary
================================================================================

- fitness function name: {}

- fitnes function type : {}

- number of generations : {}

- number of individuals : {}

- number of variables : {}

- optimal individual : {}

- optimal fitness value : {}

================================================================================
"""


def ga(fit_function,
       fit_type,
       num_var,
       boundaries,
       num_gen=100,
       num_pop=100,
       num_elite=10,
       mutation_probability=0.01,
       n_cross=1,
       num_bin_dig=None,
       num_pop_init=None,
       num_gen_init_pop=None,
       start_from_gen=False,
       min_fit=None,
       fit_name=None,
       fargs=None,
       fkwargs=None,
       output_path=None,
       input_path=None,
       print_refresh=1):

    """Genetic Algorithm optimisation.

    Parameters
    ----------
    fit_function : callable
        The function used by the :class'GA' to determine the fitness value. The function
        must have as a first argument a list of variables that determine the
        fitness value. Other arguments and keyword arguments can be used to feed
        the function relevant data.
    fit_type : str
        String that indicates if the fitness function is to be minimized or maximized.
        "min" for minimization and "max" for maximization.
    num_var :  int
        The number of variables used by the fitness function.
    boundaries : list
        The minimum and vaximum values each variable is allowed to have. Must be
        a ``num_var`` long list of tuples in the form [(min, max),...].
    num_gen : int, optional [100]
        The maximum number of generations.
    num_pop : int, optional [100]
        The number of individuals in the population. Must be an even number.
    num_elite : int, optional [10]
        The number of individuals in the elite population. Must be an even number.
    mutation_probablity : float, optional [0.001]
        Float from 0 to 1. Percentage of genes that will be mutated.
    n_cross: int, optional [1]
        Number of crossover points used in the crossover operator.
    num_bin_dig : list, optional [None]
        Number of genes used to codify each variable. Must be a ``num_var`` long
        list of intergers. If None is given, each variable will be coded with a
        8 digit binary number, corresponding to 256 steps.
    num_pop_init : int, optional [None]
        The number of individuals in the population for the first ``num_gen_init_pop``
        generations.
    num_gen_init_pop : int, optional
        The number of generations to keep a ``num_pop_init`` size population for.
    start_from_get : int, optional [None]
        The generation number to restart a previous optimization process.
    min_fit : float, optional [None]
        A target fitness value. If the GA finds a solution with a fitness value
        equal or better than ``min_fit``, the optimization is stopped.
    fit_name : str, optional [None]
        The name of the optimisation. If None is given, the name of the fitness
        function is used.
    fargs : list, optional [None]
        Arguments fo be fed to the fitness function.
    fkwargs : dict, optional [None]
        Keyword arguments to be fed to the fitness function.
    output_path : str, optional [None]
        Path for the optimization result files.
    input_path : str, optional [None]
        Path to the fitness function file.
    print_refresh : int
        Print current generation summary every ``print_refresh`` generations.

    Returns
    -------
    ga_ : object
        The resulting :class'GA' instance.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Holland, J. H., *Adaptation in Natural and Artificial Systems*, 1st edn,
           The University of Michigan, Ann Arbor, 1975.

    Examples
    --------
    .. code-block:: python

        import os
        import compas
        from compas.numerical.solvers.ga import ga

        def foo(X):
            fit = sum(X)
            return fit

        fit_function = foo
        fit_type = 'min'
        num_var = 10
        boundaries = [(0, 1)] * num_var
        num_bin_dig  = [8] * num_var
        output_path = os.path.join(compas.TEMP, 'ga_out/')

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ga = ga(fit_function,
                fit_type,
                num_var,
                boundaries,
                num_gen=100,
                num_pop=100,
                num_elite=40,
                num_bin_dig=num_bin_dig,
                output_path=output_path,
                min_fit=0.01)

    .. code-block:: none

        ================================================================================
        GA summary
        ================================================================================

        - fitness function name: foo

        - fitnes function type : min

        - number of generations : 100

        - number of individuals : 100

        - number of variables : 10

        - optimal individual : 31

        - optimal fitness value : 0.0705882352941

        ================================================================================

    """
    ga_ = GA()

    ga_.fit_name             = fit_name or fit_function.__name__
    ga_.fit_type             = fit_type
    ga_.num_gen              = num_gen
    ga_.num_pop              = num_pop
    ga_.num_pop_init         = num_pop_init
    ga_.num_gen_init_pop     = num_gen_init_pop
    ga_.num_elite            = num_elite
    ga_.num_var              = num_var
    ga_.mutation_probability = mutation_probability
    ga_.ncross               = n_cross
    ga_.start_from_gen       = start_from_gen
    ga_.min_fit              = min_fit
    ga_.boundaries           = boundaries
    ga_.num_bin_dig          = num_bin_dig or [8] * num_var
    ga_.max_bin_dig          = max(ga_.num_bin_dig)
    ga_.total_bin_dig        = sum(ga_.num_bin_dig)
    ga_.fargs                = fargs or {}
    ga_.fkwargs              = fkwargs or {}
    ga_.fit_function         = fit_function
    ga_.output_path          = output_path or ''
    ga_.input_path           = input_path or ''
    ga_.print_refresh        = print_refresh
    ga_.ga_optimize()
    return ga_


class GA(object):
    """This class contains a binary coded, single objective genetic algorithm.

    Attributes
    ----------
    best_fit : float
        The fitness value of the best performing solution for the current generation.
    best_individual_index: int
        The index of the best performing individual for the current generation.
    boundaries : dict
        This dictionary contains all the max and min bounds for each optimization variable.
        ``GA.boundaries[index] = [min,max]``.
    current_pop : dict
        This dictionary contains the coded, decoded and scaled population of the current
        generation, as well as their fitness values.
    elite_pop : dict
        This dictionary contains the coded, decoded and scaled data for the elite
        population of the current generation, as well as their fitness values.
    end_gen : int
        The maximum number of generations the GA is allowed to run.
    fit_function: function
        The fitness function.
    fit_name : str
        The name of the python file containing the fitness function (without extension).
    fit_type : str
        String that indicates if the fitness function is to be minimized or maximized.
        "min" for minimization and "max" for maximization.
    input_path: str
        Path to the fitness function file.
    fkwargs : dict
        This dictionary will be passed as a keyword argument to all fitness functions.
        It can be used to pass required data, objects, that are not related to the
        optimmization variables but are required to run the fitness function.
    max_bin_digit : int
        The maximum number of binary digits that are used to code a variable values.
        The number of binary digits assigned to code a variable determine the number
        of discrete steps inside the variable bounds. For example, an 8 digit binary
        number will produce 256 steps.
    min_fit : float
        An end condition related to fitness value. If it is set, the GA will stop
        when any individual achieves a fitness equal or better that ``GA.min_fit``. If
        it is not set, the GA will end after ``GA.num_gen`` generations.
    min_fit_flag : bool
        Flag the GA uses to determine if the ``GA.min_fit`` value has been achieved.
    mutation_probability : float
        Determines the probability that the mutation operator will mutate each gene.
        For each gene a random number ``x`` between 0 and 1 is generated, if ``x``
        is higher than ``GA.mutation_probability`` it will be mutated.
    num_bin_dig : list
        List of the number of binary digits for each variable. The number of binary
        digits assigned to code a variable determine the number of discrete steps
        inside the variable bounds. For example, an 8 digit binary number will
        produce 256 steps.
    num_elite : int
        The number of top performing individuals in the population that are not subject
        to genetic operators, but are simply copied to the next generation.
    num_gen : int
        The number of genertions the GA will run.
    num_pop : int
        The number of individuals per generation.
    num_var : int
        The number of variables in the optimization problem.
    output_path : str
        The path to which the GA outputs result files.
    start_from_gen : int
        The generation from which the GA will restart. If this number is given, the GA
        will look for generation output files in the ``GA.input_path`` and if found,
        the GA will resume optimization from the ``GA.start_from_gen`` generation.
    total_bin_dig : int
        The total number of binary digits. It is the sum of the ``GA.num_bin_dig`` of
        all variables.
    ind_fit_dict : dict
        This dictionary keeps track of already evaluated solutions to avoid dupplicate
        fitness function calls.

    """

    def __init__(self):
        """ Initializes the GA object."""

        self.fkwargs = {}
        self.fargs = {}
        self.best_fit = None
        self.best_individual_index = None
        self.boundaries   = {}
        self.current_pop  = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': []}
        self.elite_pop    = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': []}
        self.end_gen = None
        self.fit_function = None
        self.fit_name = ''
        self.fit_type = None
        self.input_path = None
        self.max_bin_dig = []
        self.min_fit = None
        self.min_fit_flag = False
        self.mutation_probability = 0
        self.n_cross = 1
        self.num_bin_dig = 0
        self.num_elite = 0
        self.num_gen = 0
        self.num_gen_init_pop = 1
        self.num_pop = 0
        self.num_pop_init = None
        self.num_pop_temp = None
        self.num_var = 0
        self.output_path = []
        self.start_from_gen = False
        self.total_bin_dig = 0
        self.check_diversity = False
        self.ind_fit_dict = {}
        self.print_refresh = 1

    def __str__(self):
        """Compile a summary of the GA."""
        fit_name = self.fit_name
        fit_type = self.fit_type
        num_gen = self.num_gen
        num_pop = self.num_pop
        num_var = self.num_var
        best = self.best_individual_index, self.current_pop['scaled'][self.best_individual_index]
        try:
            fit = self.current_pop['fit_value'][self.best_individual_index]
        except(Exception):
            fit = None
        return TPL.format(fit_name, fit_type, num_gen, num_pop, num_var, best, fit)

    def summary(self):
        """Print a summary of the GA."""
        print(self)

    def ga_optimize(self):
        """ This is the main optimization function, this function permorms the GA optimization,
        performing all genetic operators.
        """
        self.write_ga_json_file()

        if self.num_pop_init:
            self.num_pop_temp = copy.deepcopy(self.num_pop)
            self.num_pop = self.num_pop_init

        if self.start_from_gen:
            self.current_pop = self.get_pop_from_pop_file(self.start_from_gen)
            start_gen_number = self.start_from_gen + 1
        else:
            self.current_pop['binary'] = self.generate_random_bin_pop()
            start_gen_number = 0

        for generation in range(start_gen_number, self.num_gen):

            self.current_pop['decoded'] = self.decode_binary_pop(self.current_pop['binary'])
            self.current_pop['scaled']  = self.scale_population(self.current_pop['decoded'])

            if generation == 0:
                num = self.num_pop
                self.current_pop['fit_value'] = [[]] * num
            else:
                num = self.num_pop - self.num_elite

            for i in range(num):
                self.current_pop['fit_value'][i] = self.evaluate_fitness(i)

            if self.num_pop_init and generation >= self.num_gen_init_pop:
                self.num_pop = self.num_pop_temp
                self.current_pop = self.select_elite_pop(self.current_pop, num_elite=self.num_pop)
            self.write_out_file(generation)

            if self.min_fit:
                self.update_min_fit_flag()
            else:
                self.get_best_fit()
            if generation % self.print_refresh == 0:
                print('generation ', generation, ' best fit ', self.best_fit, 'min fit', self.min_fit)

            #####################################################################
            # print ('before')
            # for i in range(len(self.current_pop['binary'])):
            #     print (i, self.current_pop['binary'][i], self.current_pop['fit_value'][i])
            #####################################################################

            if self.check_diversity:
                print('num repeated individuals', self.check_pop_diversity())
            if generation < self.num_gen - 1 and self.min_fit_flag is False:
                self.elite_pop = self.select_elite_pop(self.current_pop)
                self.tournament_selection()  # n-e
                self.create_mating_pool()  # n-e
                self.npoint_crossover()  # n-e
                self.random_mutation()  # n-e
                self.add_elite_to_current()  # n

                #####################################################################
                # print ('after')
                # for i in range(len(self.current_pop['binary'])):
                #     print (i, self.current_pop['binary'][i], self.current_pop['binary'][i] in self.elite_pop['binary'])
                # print ()
                #####################################################################
            else:
                self.end_gen = generation
                self.get_best_individual_index()
                self.write_ga_json_file()
                print(self)
                break

    def evaluate_fitness(self, index):
        chromo = ''.join(str(y) for x in self.current_pop['binary'][index] for y in x)
        fit = self.ind_fit_dict.setdefault(chromo, None)
        if not fit:
            fit = self.fit_function(self.current_pop['scaled'][index], *self.fargs, **self.fkwargs)
            self.ind_fit_dict[chromo] = fit
        return fit

    def check_pop_diversity(self):
        seen = []
        all_ = []
        for ind in self.current_pop['scaled']:
            if ind not in seen:
                seen.append(ind)
            all_.append(ind)
        return len(all_) - len(seen)

    def decode_binary_pop(self, bin_pop):
        """Decodes the binary population, from binary to unscaled variable values

        Parameters
        ----------
        bin_pop: list
            The binary population list.

        Returns
        -------
        decoded_pop:
            The decoded population list.
        """
        decoded_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(self.num_pop):
            for i in range(self.num_var):
                value = 0
                chrom = bin_pop[j][i]
                for u, gene in enumerate(chrom):
                    if gene == 1:
                        value = value + 2**u
                decoded_pop[j][i] = value
        return decoded_pop

    def generate_random_bin_pop(self):
        """ Generates random binary population of ``GA.num_pop`` size.

        Returns
        -------
        random_bin_pop: list
            A list containing a random binary population.
        """
        random_bin_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(self.num_pop):
            for i in range(self.num_var):
                random_bin_pop[j][i] = [random.randint(0, 1) for u in range(self.num_bin_dig[i])]
        return random_bin_pop

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
        scaled_pop = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(self.num_pop):
            for i in range(self.num_var):
                maxbin = float((2 ** self.num_bin_dig[i]) - 1)
                scaled_pop[j][i] = self.boundaries[i][0] + (self.boundaries[i][1] - self.boundaries[i][0]) * decoded_pop[j][i] / maxbin
        return scaled_pop

    def tournament_selection(self):
        """Performs the tournament selection operator on the current population.
        """
        pop_a = []
        pop_b = []
        indices = range(self.num_pop)
        # for i in range((self.num_pop - self.num_elite)):
        #     u, v = random.sample(indices, 2)
        #     pop_a.append(u)
        #     pop_b.append(v)
        pop_a = random.sample(indices,self.num_pop-self.num_elite)
        pop_b = random.sample(indices,self.num_pop-self.num_elite)
        self.mp_indices = []
        for i in range(self.num_pop - self.num_elite):
            fit_a = self.current_pop['fit_value'][pop_a[i]]
            fit_b = self.current_pop['fit_value'][pop_b[i]]
            if self.fit_type == 'min':
                if fit_a < fit_b:
                    self.mp_indices.append(pop_a[i])
                else:
                    self.mp_indices.append(pop_b[i])
            elif self.fit_type == 'max':
                if fit_a > fit_b:
                    self.mp_indices.append(pop_a[i])
                else:
                    self.mp_indices.append(pop_b[i])
        # print (pop_a, 'tournament pop_a')
        # print (pop_b, 'tournament pop_a')
        # print()
        # print (self.mp_indices, 'tournament winners')

    def select_elite_pop(self, pop, num_elite=None):
        """Saves the elite population in the elite population dictionary

        Parameters
        ----------
        pop: dict
            A population dictionary

        Returns
        -------
        elite_pop: dict
            The elite population dictionary.
        """
        if self.fit_type == 'min':
            sorted_ind = self.get_sorting_indices(self.current_pop['fit_value'])
        elif self.fit_type == 'max':
            sorted_ind = self.get_sorting_indices(self.current_pop['fit_value'], reverse=True)
        else:
            raise ValueError('User selected fit_type is wrong. Use "min" or "max" only')
        if not num_elite:
            num_elite = self.num_elite

        elite_pop   = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': []}
        for i in range(num_elite):
            elite_pop['binary'].append(pop['binary'][sorted_ind[i]])
            elite_pop['decoded'].append(pop['decoded'][sorted_ind[i]])
            elite_pop['scaled'].append(pop['scaled'][sorted_ind[i]])
            elite_pop['fit_value'].append(pop['fit_value'][sorted_ind[i]])
        return elite_pop

    def get_sorting_indices(self, l, reverse=False):
        """Reurns the indices that would sort a list of floats. If floats are
        repeated in the list, only one instance is considered. The index of
        repeaded floats are included in the end of the index list.

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
        l_ = []
        if reverse:
            x = float('-inf')
        else:
            x = float('inf')
        for i in l:
            if i in l_:
                l_.append(x)
            else:
                l_.append(i)
        sorting_index = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(l_))]
        if reverse is True:
            sorting_index = list(reversed(sorting_index))
        return sorting_index

    def create_mating_pool(self):
        """Creates two lists of cromosomes to be used by the crossover operator.
        """
        self.mating_pool_a = []
        self.mating_pool_b = []
        for i in range(int((self.num_pop - self.num_elite) / 2)):
            chrom_a = []
            chrom_b = []
            # print (i, ' ',self.mp_indices[i], self.mp_indices[i + (int((self.num_pop - self.num_elite) / 2))], '       mp individual ab')
            # print (i + (int((self.num_pop - self.num_elite) / 2)), ' ', self.mp_indices[i + (int((self.num_pop - self.num_elite) / 2))], self.mp_indices[i], '       mp individual ba')
            for j in range(self.num_var):
                chrom_a += self.current_pop['binary'][self.mp_indices[i]][j]
                chrom_b += self.current_pop['binary'][self.mp_indices[i + (int((self.num_pop - self.num_elite) / 2))]][j]
            self.mating_pool_a.append(chrom_a)
            self.mating_pool_b.append(chrom_b)

    def simple_crossover(self):
        """Performs the simple crossover operator. Individuals in ``GA.mating_pool_a`` are
        combined with individuals in ``GA.mating_pool_b`` using a single, randomly selected
        crossover point.
        """
        self.current_pop  = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': []}
        self.current_pop['binary'] = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(int((self.num_pop - self.num_elite) / 2)):
            cross = random.randint(1, self.total_bin_dig - 1)
            # print (j, cross, 'crossover point')
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
                self.current_pop['binary'][j + (int((self.num_pop - self.num_elite) / 2))][i] = variable_b

    def npoint_crossover(self):
        """Performs the n-point crossover operator. Individuals in ``GA.mating_pool_a`` are
        combined with individuals in ``GA.mating_pool_b`` using ne, randomly selected
        crossover points.
        """
        self.current_pop  = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': []}
        self.current_pop['binary'] = [[[]] * self.num_var for i in range(self.num_pop)]
        for j in range(int((self.num_pop - self.num_elite) / 2)):
            a = self.mating_pool_a[j]
            b = self.mating_pool_b[j]
            cross_list = sorted(random.sample(range(1, self.total_bin_dig - 1), self.n_cross))
            for cross in cross_list:
                c = a[:cross] + b[cross:]
                d = b[:cross] + a[cross:]
                a = d
                b = c
            for i in range(self.num_var):
                variable_a = a[:self.num_bin_dig[i]]
                variable_b = b[:self.num_bin_dig[i]]
                self.current_pop['binary'][j][i] = variable_a
                self.current_pop['binary'][j + (int((self.num_pop - self.num_elite) / 2))][i] = variable_b

    def random_mutation(self):
        """This mutation operator replaces a gene from 0 to 1 or viceversa
        with a probability of ``GA.mutation_probability``.
        """
        for i in range(self.num_pop - self.num_elite):
            for j in range(self.num_var):
                for u in range(self.num_bin_dig[j]):
                    random_value = random.random()
                    if random_value < (self.mutation_probability):
                        if self.current_pop['binary'][i][j][u] == 0:
                            self.current_pop['binary'][i][j][u] = 1
                        else:
                            self.current_pop['binary'][i][j][u] = 0

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
        for i in range(self.num_pop):
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
        unscaled_pop = {}

        for i in range(self.num_pop):
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

    def write_out_file(self, generation):
        """Writes the population data for a given generation.

        Parameters
        ----------
        generation: int
            The generation number.
        """
        filename  = 'generation_' + "%05d" % generation + '_population' + ".txt"
        pf_file  = open(self.output_path + (str(filename)), "w")
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
                pf_file.write(str(self.current_pop['scaled'][i][f]))
                pf_file.write(',')
            pf_file.write('\n')
        pf_file.write('\n')

        pf_file.write('Population fitness value \n')
        for i in range(self.num_pop):
            pf_file.write(str(i) + ',')
            pf_file.write(str(self.current_pop['fit_value'][i]))
            pf_file.write('\n')
        pf_file.write('\n')
        pf_file.write('\n')
        pf_file.close()

    def add_elite_to_current(self):
        """Adds the elite population to the current population dictionary.
        """
        self.current_pop['decoded'] = [[[]] * self.num_var for i in range(self.num_pop)]
        self.current_pop['decoded'] = [[[]] * self.num_var for i in range(self.num_pop)]
        self.current_pop['scaled'] = [[[]] * self.num_var for i in range(self.num_pop)]
        self.current_pop['fit_value'] = [[]] * self.num_pop
        for i in range(self.num_elite):
            self.current_pop['binary'][self.num_pop - self.num_elite + i] = self.elite_pop['binary'][i]
            self.current_pop['decoded'][self.num_pop - self.num_elite + i] = self.elite_pop['decoded'][i]
            self.current_pop['scaled'][self.num_pop - self.num_elite + i] = self.elite_pop['scaled'][i]
            self.current_pop['fit_value'][self.num_pop - self.num_elite + i] = self.elite_pop['fit_value'][i]

    def make_ga_input_data(self):
        """Returns a dictionary containing the most relavant genetic data present in the instance
        of ``GA``. This is the data required to restart a genetic optimization process or to
        launch a visualization using ``compas_ga.visualization.ga_visualization``.

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
                'fit_name': self.fit_name,
                'fit_type': self.fit_type,
                'start_from_gen': self.start_from_gen,
                'max_bin_dig': self.max_bin_dig,
                'total_bin_dig': self.total_bin_dig,
                'output_path': self.output_path,
                'num_elite': self.num_elite,
                'min_fit': self.min_fit,
                'end_gen': self.end_gen,
                'best_individual_index': self.best_individual_index
                }
        return data

    def write_ga_json_file(self):
        """Writes a JSON file containing the most relevant data for GA optimization and
        visualization using ``compas_ga.visualization.ga_visualization``.
        """
        data = self.make_ga_input_data()
        filename = self.fit_name + '.json'
        with open(self.output_path + filename, 'w') as fh:
            json.dump(data, fh)

    def update_min_fit_flag(self):
        """Checks if the minimum desired fitness value has been achieved during optimization
        and saves the result in ``GA.min_fit_flag``.
        """
        values = self.current_pop['fit_value']
        if self.fit_type == 'min':
            self.best_fit = min(values)
            if self.best_fit <= self.min_fit:
                self.min_fit_flag = True
        elif self.fit_type == 'max':
            self.best_fit = max(values)
            if self.best_fit >= self.min_fit:
                self.min_fit_flag = True

    def get_best_fit(self):
        """Saves the best fitness value in ``GA.best_fit``
        """
        if self.fit_type == 'min':
            self.best_fit = min(self.current_pop['fit_value'])
        elif self.fit_type == 'max':
            self.best_fit = max(self.current_pop['fit_value'])

    def get_pop_from_pop_file(self, gen):
        """Reads the population file corresponding to the ``gen`` generation and returns
        the saved population data. The population file must be in ``GA.input_path``.

        Parameters
        ----------
        gen: int
            The generation index.

        Returns
        -------
        file_pop: dict
            The population dictionary contained in the file.
        """
        # file_pop  = {'binary': [], 'decoded': [], 'scaled': [], 'fit_value': [],
        #              'pf': []}
        filename  = 'generation_' + "%05d" % gen + '_population' + ".txt"
        filename = self.input_path + filename
        pf_file = open(filename, 'r')
        lines = pf_file.readlines()
        pf_file.close()
        file_pop = {}
        file_pop['scaled'] = [[[]] * self.num_var for i in range(self.num_pop)]
        file_pop['fit_value'] = [[[]] * self.num_var for i in range(self.num_pop)]

        for i in range(self.num_pop):
            line_scaled = lines[i + 7]
            line_fit = lines[i + 9 + self.num_pop]
            string_scaled = re.split(',', line_scaled)
            string_fit = re.split(',', line_fit)
            string_fit = string_fit[1]
            del string_scaled[-1]
            del string_scaled[0]
            scaled = [float(j) for j in string_scaled]
            fit_value = float(string_fit)
            file_pop['fit_value'][i] = fit_value
            for j in range(len(scaled)):
                file_pop['scaled'][i][j] = scaled[j]

        file_pop['decoded'] = self.unscale_pop(file_pop['scaled'])
        file_pop['binary'] = self.code_decoded(file_pop['decoded'])
        return file_pop

    def get_best_individual_index(self):
        """Saves the index of the best performing individual of the current population
         in ``GA.best_individual_index``.
        """
        # fit_values = self.current_pop['fit_value'].values()
        fit_values = [self.current_pop['fit_value'][i] for i in range(len(self.current_pop['fit_value']))]
        if self.fit_type == 'min':
            indices = self.get_sorting_indices(fit_values)
        elif self.fit_type == 'max':
            indices = self.get_sorting_indices(fit_values, reverse=True)
        self.best_individual_index = indices[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import os
    import compas
    from compas.plotters.gaplotter import visualize_evolution
    from math import cos
    from math import pi

    def rastrigin(X):
        a = 10
        fit = a * 2 + sum([(x ** 2 - a * cos(2 * pi * x)) for x in X])
        return fit

    def foo(X):
        fit = sum(X)
        # print ('fit', fit, X)
        return fit

    fit_function = rastrigin
    # fit_function = foo
    fit_type = 'min'
    num_var = 2
    boundaries = [(-5.12, 5.12)] * num_var
    # boundaries = [(1, 5)] * num_var

    num_bin_dig  = [40] * num_var
    output_path = os.path.join(compas.TEMP, 'ga_out/')
    min_fit = 0.000001  # num_var * boundaries[0][0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ga_ = ga(fit_function,
             fit_type,
             num_var,
             boundaries,
             num_gen=100,
             num_pop=100,
             num_elite=20,
             num_bin_dig=num_bin_dig,
             output_path=output_path,
             min_fit=min_fit,
             mutation_probability=0.03,
             n_cross=2)

    visualize_evolution(ga_.output_path)
