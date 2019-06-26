from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import re
import json
import math
import os
import matplotlib.pyplot as plt


__all__ = ['GaPlotter']


class GaPlotter(object):
    """This class is to be used for the visualization of the optimization performed by the
    ``compas_ga.ga`` function. The function ``draw_ga_evolution`` produces a PDF that shows the
    minimum, maximum and average fitness value of the genetic population per generation.
    """

    def __init__(self):
        """Initializes the GA_VIS object
        Parameters
        ----------
        boundaries: dict
            This dictionary contains all the max and min bounds for each optimization variable.
            ``boundaries[index] = [min,max]``.
        color_dict: dict
            Index to color dictionary.
        conversion_function: function
            If a function ``foo(x)`` is given, the fitness values will be displayed not as
            originally used during optimization, but as the output of ``foo(x)``. This is
            convinient for unit changes or general fitness value transformations.
        generation: int
            The current generation.
        fit_name: str
            The name assigend to the fitnness function.
        input_path: str
            The path to the GA results file.
        lable_size: int
            Lable size in pt.
        num_gen: int
            The total number of generations in the GA optimization.
        num_var: int
            The number of optimization variables.
        number_size: int
            The size if numbers in the visualization in pt.
        output_path: str
            The path in which the visualization PDF will be written.
        pop: dict
            The population dictionary, contains the binary, decoded and scaled data for each
            individual of the population, as well as their fitness values.
        start_from_gen: int
            If this value is given, the visualization will show only from the selected
            generation.
        title_size: int
            The size title of the visualization in pt.
        xtics: int
            The number of tics in the x axis or vertical lines in the visualization.
        """
        # self.boundaries = {}
        self.color_dict = {0: 'r', 1: 'y', 2: 'g', 3: 'c', 4: 'b', 5: 'k'}
        self.conversion_function = None
        self.generation = 0
        self.fit_name = []
        self.fit_type = ''
        self.input_path = ''
        self.lable_size = 15
        self.num_gen = 0
        self.num_pop = 0
        # self.num_var = 0
        self.number_size = 15
        self.output_path = ''
        self.pop = {'binary': {}, 'decoded': {}, 'scaled': {},
                    'fit_value': {}}
        self.start_from_gen = 0
        self.title_size = 20
        self.xticks = None
        self.y_bounds = {'y_min': None, 'y_max': None}
        self.y_caps = {'y_min': float('-inf'), 'y_max': float('inf')}
        self.plot_avg = True
        self.plot_max = True
        self.loc_dict = {'min': 1, 'max': 4}

    def get_ga_input_from_file(self):
        files = os.listdir(self.input_path)
        for f in files:
            if os.path.splitext(f)[1] == '.json':
                filename = f
                break

        with open(self.input_path + filename, 'r') as fh:
            ga = json.load(fh)

        # self.num_var        = ga['num_var']
        self.num_pop        = ga['num_pop']
        # self.boundaries     = ga['boundaries']
        self.fit_name       = ga['fit_name']
        self.min_fit        = ga['min_fit']
        self.fit_type       = ga['fit_type']
        if ga['end_gen']:
            self.num_gen = ga['end_gen']
        else:
            self.num_gen        = ga['num_gen']
        if not self.start_from_gen and self.start_from_gen != 0:
            if ga['start_from_gen']:
                self.start_from_gen = ga['start_from_gen']

    def get_pop_from_pop_file(self):
        file_pop  = {'binary': {}, 'decoded': {}, 'scaled': {}, 'fit_value': {}, 'pf': {}}
        filename  = 'generation_' + "%05d" % self.generation + '_population' + ".txt"
        filename = self.input_path + filename
        pf_file = open(filename, 'r')
        lines = pf_file.readlines()
        pf_file.close()

        for i in range(self.num_pop):
            file_pop['scaled'][i] = {}
            file_pop['fit_value'][i] = {}
            line_scaled = lines[i + 7]
            line_fit = lines[i + 9 + self.num_pop]
            string_scaled = re.split(',', line_scaled)
            string_fit = re.split(',', line_fit)
            string_fit = string_fit[1]
            del string_scaled[-1]
            del string_scaled[0]
            scaled = [float(j) for j in string_scaled]
            fit_value = float(string_fit)
            for j in range(len(scaled)):
                file_pop['scaled'][i][j] = scaled[j]
            file_pop['fit_value'][i] = fit_value

        return file_pop

    def get_min_max_avg(self, pop):
        values = pop['fit_value'].values()
        # values_ = values
        values_ = []
        for value in values:
            if value <= self.y_caps['y_min'] or value >= self.y_caps['y_max']:
                continue
                # values_.append(None)
            else:
                values_.append(value)
        min_ = min(values_)
        max_ = max(values_)
        avg_ = sum(values_) / len(values_)
        return min_, max_, avg_

    def find_tick_size(self):
        size = self.num_gen
        size = int(math.ceil(size / 10.0)) * 10
        self.xticks = int(round(size / 5.0, 10))
        # print('self.xticks',self.xticks)

    def draw_ga_evolution(self, make_pdf=True, show_plot=False):

        self.get_ga_input_from_file()
        min_list = []
        max_list = []
        avg_list = []
        for i in range(self.start_from_gen, self.num_gen + 1):
            # print('reading gen ',i)
            self.generation = i
            try:
                fpop = self.get_pop_from_pop_file()
                min_, max_, avg_ = self.get_min_max_avg(fpop)
                if self.conversion_function:
                    min_ = self.conversion_function(min_)
                    max_ = self.conversion_function(max_)
                    avg_ = self.conversion_function(avg_)
                if self.fit_type == 'max':
                    min_list.append(max_)
                    max_list.append(min_)
                    avg_list.append(avg_)
                else:
                    min_list.append(min_)
                    max_list.append(max_)
                    avg_list.append(avg_)
            except Exception:
                if self.generation == 0:
                    raise ValueError('population files not found')
                self.num_gen = self.generation - 1
                print('generation ', self.generation, ' pop file not found')
                print('results plotted until generation ', self.generation - 1)
                break

        fig = plt.gcf()
        plt.clf()
        fig.set_size_inches(12, 11)

        if not self.xticks:
            self.find_tick_size()

        plt.plot(min_list, color='black', lw=2, label='Minimum')
        if self.plot_max:
            plt.plot(max_list, color='black', lw=1, label='Maximum')
        if self.plot_avg:
            plt.plot(avg_list, color='red' , lw=1, label='Average')
        plt.minorticks_on()

        plt.xlim((-self.xticks / 2.0, self.num_gen - self.start_from_gen))

        if self.y_bounds['y_max']:
            y_max = self.y_bounds['y_max']
            y_min = self.y_bounds['y_min']
        else:
            if self.plot_max:
                full_list = min_list + max_list
            elif self.plot_avg:
                full_list = min_list + avg_list
            else:
                full_list = min_list
            y_min = min(full_list)
            y_max = max(full_list)
        print ('y_max', y_max)
        print ('y_min', y_min)

        if self.min_fit:
            plt.axhline(self.min_fit, color='red', ls=':', lw=0.5)
            string = self.fit_type + ' fit'
            plt.text(-self.xticks / 20, self.min_fit, string, horizontalalignment='right', color='red')
            # self.min_fit,self.num_gen-self.start_from_gen
            if self.min_fit < min(min_list):
                y_min = self.min_fit

        delta = y_max - y_min
        plt.ylim((y_min - (delta * 0.1), y_max + delta * 0.1))
        plt.title('Function ' + self.fit_name + ' evolution', fontsize=self.title_size)
        plt.xlabel('Generation', fontsize=self.lable_size)
        plt.ylabel('Function ' + self.fit_name, fontsize=self.lable_size)
        labels = range(self.start_from_gen, self.num_gen, self.xticks)
        x = range(0, len(labels) * self.xticks, self.xticks)
        plt.xticks(x, labels)
        plt.grid(True)
        plt.legend(loc=self.loc_dict[self.fit_type])
        if make_pdf:
            plt.savefig(self.output_path + self.fit_name + '_evolution.pdf')
        if show_plot:
            plt.show()
        print('Evolution visualisation complete')


def visualize_evolution(input_path,
                        output_path=None,
                        make_pdf=False,
                        show_plot=True,
                        start_from_gen=0,
                        conversion_function=None,
                        y_bounds=[None, None],
                        plot_avg=True,
                        plot_max=True):
    vis = GaPlotter()
    vis.input_path = input_path
    vis.output_path = output_path
    vis.conversion_function = conversion_function
    vis.start_from_gen = 0
    vis.y_bounds = {'y_min': y_bounds[0], 'y_max': y_bounds[1]}
    vis.plot_avg = plot_avg
    vis.plot_max = plot_max
    vis.draw_ga_evolution(make_pdf=make_pdf, show_plot=show_plot)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    input_path = os.path.join(compas.TEMP, 'ga_out/')
    output_path = input_path
    visualize_evolution(input_path, output_path, make_pdf=False, show_plot=True,
                        start_from_gen=0, conversion_function=None)
