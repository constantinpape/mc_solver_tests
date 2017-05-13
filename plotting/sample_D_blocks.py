import matplotlib.pyplot as plt
import nifty
import vigra
import sys
import numpy as np
sys.path.append('..')
from utils import model_paths_mcluigi, read_from_mcluigi, nifty_mc_objective

time_offsets_mc    = np.array([0, 1484.5, 298.3, 349.2, 1035.2])
time_offsets_merge = np.array([0, 3286.5, 356.6, 255.1, 198.2])
t_offsets          = np.cumsum(time_offsets_mc + time_offsets_merge)#[::-1]
print t_offsets
quit()

energy_offsets = [
        -301629076.633,
        -464023504.7815482,
        -490128654.61634934,
        -502916749.99766165,
        -510288693.97572863]



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
    print get_initial_energy()
