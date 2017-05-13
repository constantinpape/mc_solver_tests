import matplotlib.pyplot as plt
import nifty
import sys
sys.path.append('..')
from utils import model_paths_mcluigi, read_from_mcluigi, nifty_mc_objective

time_offsets_mc    = [0, 1484.5, 298.3, 349.2, 1035.2]
time_offsets_merge = [0, 3286.5, 356.6, 255.1, 198.2]

energy_offsets = []


def read_nodes(model_path):
    graph_data = vigra.readHDF5(model_path, 'graph')
    toGlobalNodes = reducedProblem.read("new2global")
    graph = nifty.graph.UndirectedGraph()
    graph.deserialize(graph_data)
    assert len(graph.numberOfNodes) == len(toGlobalNodes)
    return graph, toGlobalNodes


def to_global_energy(global_obj, graph, toGlobalNodes):
    nodeResult = np.zeros(global_obj.graph.numberOfNodes, dtype = 'uint32')
    for nodeId in xrange(graph.numberOfNodes):
        nodeResult[toGlobalNodes[nodeId]] = nodeId
    globalEnergy = globalObjective.evalNodeLabels(nodeResult)
    return globalEnergy


def get_energy_offsets():
    models = ['sampleD_full', 'sampleD_L1', 'sampleD_L2', 'sampleD_L3', 'sampleD_L4']

    n_var_g, uv_ids_g, costs_g = read_from_mcluigi( model_paths_mcluigi[models[0]] )
    global_obj = nifty_mc_objective(
            n_var_g, uv_ids_g, costs_g
            )
    energies = [0.]

    for mm in models[1:]:
        energies.append( to_global_energy(
            global_obj,
            read_all(model_paths_mcluigi[mm]) )
        )

    return energies


if __name__ == '__main__':
    get_energy_offsets()
