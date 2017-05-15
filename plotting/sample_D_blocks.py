import matplotlib.pyplot as plt
import matplotlib
import nifty
import vigra
import sys
import numpy as np
from decimal import Decimal
sys.path.append('..')
from utils import model_paths_mcluigi, read_from_mcluigi, nifty_mc_objective, parse_out_niftyfm

time_offsets_mc    = np.array([0, 1484.5, 298.3, 349.2, 1035.2])
time_offsets_merge = np.array([0, 3286.5, 356.6, 255.1, 198.2])
t_offsets          = np.cumsum(time_offsets_mc + time_offsets_merge)#[::-1]

energy_offsets = [
        -301629076.633,
        -464023504.7815482,
        -490128654.61634934,
        -502916749.99766165,
        -510288693.97572863]


def plot_optimality():
    fig, ax = plt.subplots()

    x = np.arange(2)
    y = [-4234305.069998,-4229536.135864]
    #rects1 = ax.bar(x, y)
    ax.scatter(x,y,s=1)

    ax.set_title('Optimality on SampleD_sub')
    ax.set_ylabel('Final energy')
    ax.set_xlabel('Number of levels')
    ax.set_xticklabels(['0', '1'])

    #def autolabel(rects):
    #    """
    #    Attach a text label above each bar displaying its height
    #    """
    #    for rect in rects:
    #        height = round(rect.get_height(), -4)
    #        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
    #                '%.4E' % Decimal(height),
    #                ha='center', va='bottom')

    #autolabel(rects1)

    plt.show()



def plot_initial_energies():
    fig, ax = plt.subplots()

    # plot initial energies
    for i, t in enumerate(t_offsets):
        ax.scatter([t], [energy_offsets[i]], label = 'L%i' % i, s = 100)

    ax.get_yaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.set_xlabel('Runtime [s]')
    ax.set_ylabel('Energy')
    ax.set_title('SampleD - Initial Energies')
    ax.legend()

    plt.show()


def plot_performance():
    fig, ax = plt.subplots()
    ax2 = plt.axes([.5,.2,.4,.4])

    # plot inference energies
    for level in (3,4):
        t, e = [], []
        t.append(t_offsets[level])
        e.append(energy_offsets[level])

        t_, e_ = parse_out_niftyfm('../tests/anytime_data/sampleD/sampleD_L%i.txt' % level)
        assert len(t_) == len(e_)
        t_ += t_offsets[level]
        for i in range(len(t_)):
            t.append(t_[i])
            e.append(e_[i])

        t = np.array(t)
        e = np.array(e)
        #e *= -1

        ax.plot(t, e, c = 'C%i' % level, label = 'L%i' % level)
        ax.scatter(t_offsets[level], energy_offsets[level], s = 100, c = 'C%i' % level)
        ax2.plot(t[1:], e[1:], c = 'C%i' % level)

    #plt.setp(ax2, xticks = [], yticks = [])

    ax.get_yaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    #ax.set_yscale('log')

    ax.set_xlabel('Runtime [s]')
    ax.set_ylabel('Energy')
    ax.set_title('SampleD - Block-wise Performance')
    ax.legend()

    plt.show()



def read_nodes(model_path):
    graph_data = vigra.readHDF5(model_path, 'graph')
    toGlobalNodes = vigra.readHDF5(model_path, "new2global")
    graph = nifty.graph.UndirectedGraph()
    graph.deserialize(graph_data)
    assert graph.numberOfNodes == len(toGlobalNodes)
    return graph, toGlobalNodes



def to_global_energy(global_obj, graph, toGlobalNodes):
    nodeResult = np.zeros(global_obj.graph.numberOfNodes, dtype = 'uint32')
    for nodeId in xrange(graph.numberOfNodes):
        nodeResult[toGlobalNodes[nodeId]] = nodeId
    return global_obj.evalNodeLabels(nodeResult)



def get_initial_energy():
    n_var_g, uv_ids_g, costs_g = read_from_mcluigi( model_paths_mcluigi['sampleD_full'] )
    global_obj = nifty_mc_objective(
            n_var_g, uv_ids_g, costs_g
            )
    return global_obj.evalNodeLabels(np.arange(n_var_g, dtype = 'uint32'))



def get_energy_offsets():
    models = ['sampleD_full', 'sampleD_L1', 'sampleD_L2', 'sampleD_L3', 'sampleD_L4']

    n_var_g, uv_ids_g, costs_g = read_from_mcluigi( model_paths_mcluigi[models[0]] )
    global_obj = nifty_mc_objective(
            n_var_g, uv_ids_g, costs_g
            )
    energies = [0.]

    #global_obj = None

    for mm in models[1:]:
        graph, to_global = read_nodes(model_paths_mcluigi[mm])
        energies.append( to_global_energy(
            global_obj,
            graph,
            to_global
            )
        )

    return energies


if __name__ == '__main__':
    #plot_optimality()
    #plot_initial_energies()
    plot_performance()
