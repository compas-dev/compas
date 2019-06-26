from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import re
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


__all__ = ['MogaPlotter']


class MogaPlotter(object):
    """This class is to be used for the visualization of the optimization performed by the
    ``compas_ga.moga`` function. The function ``draw_objective_spaces`` produces a multi page PDF
    that shows the objective space resulting from each generaton of genetic optimization per page.
    """

    def __init__(self):
        """
        """
        self.num_var = 0
        self.num_pop = 0
        self.num_gen = 0
        self.num_fit_func = 0
        self.boundaries   = {}
        self.parent_pop   = {'binary': {}, 'decoded': {}, 'scaled': {}, 'fit_values': {}, 'pf': {}}
        self.input_path = ''
        self.output_path = ''
        self.fit_names = []
        self.pop = {}
        self.generation = 0
        self.color_dict = {0: 'r', 1: 'y', 2: 'g', 3: 'c', 4: 'b', 5: 'k'}

        self.number_size = 15
        self.lable_size = 15
        self.title_size = 20
        self.pareto_size = 10
        self.dominated_size = 5

        self.fixed_individuals = {}
        self.conversion_functions = {}
        self.def_conv_func = None

        self.scale = None

    def draw_objective_spaces(self, filename, number=False):

        self.get_ga_input_from_file(filename)

        func_combinations = self.get_func_combinations()
        filename = ''
        for name in self.fit_names:
            filename += name + '-'
        filename += '.pdf'
        print(filename)
        fpath = os.path.join(self.output_path, filename)
        with PdfPages(fpath) as pdf:
            for k in range(self.num_gen):
                self.generation = k
                self.pop = self.get_pop_from_pf_file()
                if not self.pop:
                    print('the last generation file found is ' + str(self.generation - 1))
                    print('pdf file written')
                    return
                for j in range(len(func_combinations)):
                    combination = func_combinations[j]
                    f1 = combination[0]
                    f2 = combination[1]
                    name = self.fit_names[f1] + ' vs. ' + self.fit_names[f2] + '_gen_' + str(self.generation)

                    fig = plt.gcf()
                    fig.set_size_inches(12, 11)
                    ax = fig.add_subplot(111)

                    matplotlib.rcParams.update({'font.size': self.number_size})

                    if self.scale:
                        bound = self.scale
                    else:
                        f1_values = [self.pop['fit_values'][i][f1] for i in range(self.num_pop)]
                        f2_values = [self.pop['fit_values'][i][f2] for i in range(self.num_pop)]
                        if self.fixed_individuals:
                            num_fixed = len(self.fixed_individuals['labels'])
                            f1_values.extend([self.fixed_individuals['fit_values'][i][f1] for i in range(num_fixed)])
                            f2_values.extend([self.fixed_individuals['fit_values'][i][f2] for i in range(num_fixed)])
                        df1 = (max(f1_values) - min(f1_values)) / 10.0
                        df2 = (max(f2_values) - min(f2_values)) / 10.0
                        bound = ((min(f1_values) - df1, max(f1_values) + df1), (min(f2_values) - df2, max(f2_values) + df2))

                    a = (bound[0][1] - bound[0][0]) / 10.0
                    a_ = (bound[1][1] - bound[1][0]) / 10.0

                    for i in range(self.num_pop):
                        x, y = self.pop['fit_values'][i][f1], self.pop['fit_values'][i][f2]
                        if self.conversion_functions:
                            x = self.conversion_functions[f1](x)
                            y = self.conversion_functions[f2](y)
                        if self.pop['pf'][i] <= 5:
                            color = self.color_dict[self.pop['pf'][i]]
                        else:
                            color = '0.9'
                        if self.pop['pf'][i] == 0:
                            size = self.pareto_size
                            if number:
                                ax.text(x + (a * 0.2), y + (a_ * 0.2), str(i),
                                        verticalalignment='top', horizontalalignment='right',
                                        color=color, fontsize=size)
                        else:
                            size = self.dominated_size

                        plt.plot(x, y, color=color, markersize=size, marker='o')
                        # plt.annotate(str(i),xy=(x,y),color=color,fontsize=10)

                    if self.fixed_individuals:
                        for i in range(len(self.fixed_individuals)):
                            x, y = self.fixed_individuals['fit_values'][i][f1],
                            self.fixed_individuals['fit_values'][i][f2]
                            if self.conversion_functions:
                                x = self.conversion_functions[f1](x)
                                y = self.conversion_functions[f2](y)
                            color = '0.1'
                            size = self.pareto_size
                            ax.text(x + (a * 0.2), y + (a_ * 0.2), self.fixed_individuals['labels'][i],
                                    verticalalignment='top', horizontalalignment='right', color=color, fontsize=size)
                            plt.plot(x, y, color=color, markersize=size, marker='o')

                    plt.xlabel(self.fit_names[f1], fontsize=self.lable_size)
                    plt.ylabel(self.fit_names[f2], fontsize=self.lable_size)
                    plt.title(name, fontsize=self.title_size)
                    plt.grid(True)
                    # plt.savefig(self.output_path+name+'.pdf')
                    if self.scale:
                        x_ = [bound[0][0] + i * a for i in range(11)]
                        y_ = [bound[1][0] + i * a_ for i in range(11)]
                        plt.xticks(x_)
                        plt.yticks(y_)
                    pdf.savefig()
                    # plt.show()
                    plt.close()
        print('pdf file written')

    def get_ga_input_from_file(self, filename):
        with open(self.input_path + filename, 'rb') as fh:
            moga = json.load(fh)

        self.num_var        = moga['num_var']
        self.num_pop        = moga['num_pop']
        self.num_fit_func   = moga['num_fit_func']
        self.boundaries     = moga['boundaries']
        self.fit_names      = moga['fit_names']
        self.num_gen        = moga['num_gen']

    def get_pop_from_pf_file(self):
        file_pop  = {'binary': {}, 'decoded': {}, 'scaled': {}, 'fit_values': {},
                     'pf': {}}
        filename  = 'generation ' + "%03d" % self.generation + '_pareto_front' + ".pareto"
        filename = self.input_path + filename
        try:
            pf_file = open(filename, 'r')
        except Exception:
            return None
        lines = pf_file.readlines()
        pf_file.close()

        for i in range(self.num_pop):
            file_pop['scaled'][i] = {}
            file_pop['fit_values'][i] = {}

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

        return file_pop

    def get_func_combinations(self):
        comb = []
        for i in range(self.num_fit_func):
            for j in range(i, self.num_fit_func):
                if i != j:
                    comb.append([i, j])
        return comb

    def add_fixed_individuals(self, fit_list, labels):
        self.fixed_individuals['fit_values'] = {}
        self.fixed_individuals['labels'] = {}
        for i in range(len(labels)):
            fit_ = fit_list[i]
            self.fixed_individuals['labels'][i] = labels[i]
            self.fixed_individuals['fit_values'][i] = {}
            for j in range(len(fit_)):
                self.fixed_individuals['fit_values'][i][j] = fit_[j]

    def default_conv_func(self, values):
        return values

    def add_conversion_functions(self, func_dict):
        for key in func_dict:
            if func_dict[key]:
                self.conversion_functions[key] = func_dict[key]
            else:
                self.conversion_functions[key] = self.default_conv_func


if __name__ == '__main__':

    vis = MULTI_VIS()
    vis.input_path = '/out/'
    filename = 'fitness1_fitness2_.json'
    # vis.generation = 1
    vis.output_path = vis.input_path
    vis.scale = ((-0.05, 1.05), (-0.05, 1.05))
    fit_list = ((0, 1), (1, 0))
    labels = ('A', 'B')
    # is.add_fixed_individuals(fit_list,labels)
    vis.draw_objective_spaces(filename, number=False)
