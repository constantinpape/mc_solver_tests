import nifty
import numpy as np
import vigra

def read_from_opengm(model_path):
    state_vector = vigra.readHDF5(model_path, 'gm/numbers-of-states')
    n_states = state_vector[0]
    assert (state_vector == n_state).all()
    factors = vigra.readHDF5(model_path, 'gm/factors')
    return n_states, factors

def read_from_mcluigi(model_path):
    graph_data = vigra.readHDF5(model_path, 'graph')
    costs = vigra.readHDF5(model_path, 'costs')
    graph = nifty.graph.UndirectedGraph()
    graph.deserialize(graph_data)

    n_var = graph.numberOfNodes
    uv_ids = graph.uvIds()
    #assert n_var == uv_ids.max() + 1, "%i, %i" % (n_var, uv_ids.max() + 1)
    assert len(costs) == len(uv_ids)
    return n_var, uv_ids, costs


def read_from_mcppl(uv_path, costs_path):
    uv_ids = vigra.readHDF5(uv_path, 'data')
    # assert uvs are consecutive and start at 0
    uniques = np.unique(uv_ids)
    assert len(uniques) == uniques.max() + 1
    costs  = vigra.readHDF5(costs_path, 'data')
    assert len(costs) == len(uv_ids)
    return uv_ids.max() + 1, uv_ids, costs
