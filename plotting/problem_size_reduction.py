import matplotlib.pyplot as plt

import cPickle as pickle
import numpy as np
from decimal import Decimal

import sys
sys.path.append('..')
from utils import model_paths_mcluigi, read_from_mcluigi




def get_problem_size_reduction():

    #problem_paths   = [model_paths_mcluigi[mod] for mod in ['sampleD_L4','sampleD_L3','sampleD_L2','sampleD_L1','sampleD_full'][::-1]]
    #edges_and_nodes = [read_from_mcluigi(path) for path in problem_paths]
    #edges_and_nodes = np.array([ (e_a_n[0], len(e_a_n[1])) for e_a_n in edges_and_nodes])
    #print edges_and_nodes.shape
    #print edges_and_nodes

    n_nodes = [90094369, 12299484, 7913447, 6017693, 5018154]
    n_edges = [650568046, 85191840, 52266335, 38008989, 30435430]

    return n_nodes, n_edges



def plot_problem_size_reduction():
    n_nodes, n_edges = get_problem_size_reduction()
    model_ticks = ['0', '1', '2', '3', '4']
    #model_ticks = { 0 : 'Full', 1 : 'L1', 2 : 'L2', 3 : 'L3', 4 : 'L4'}
    x = np.arange(len(n_nodes))
    width = 0.35

    f, ax = plt.subplots()

    # plot node reduction
    rects1 = ax.bar(x, n_nodes, width)
    rects2 = ax.bar(x + width, n_edges, width)

    ax.set_xticks(x)
    ax.set_xticklabels(model_ticks)
    ax.set_title('Problem Size Reduction')
    ax.set_yscale('log')
    ax.set_ylabel('Count (log-scale)')
    ax.set_xlabel('Number of levels')

    ax.legend( (rects1, rects2), ('Number of Nodes', 'Number of Edges') )

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = round(rect.get_height(), -4)
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%.4E' % Decimal(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()



if __name__ == '__main__':
    plot_problem_size_reduction()
