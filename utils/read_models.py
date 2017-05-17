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


def read_nodes(model_path):
    return vigra.readHDF5(model_path, "new2global")


def read_from_mcppl(uv_path, costs_path):
    uv_ids = vigra.readHDF5(uv_path, 'data')
    # assert uvs are consecutive and start at 0
    uniques = np.unique(uv_ids)
    assert len(uniques) == uniques.max() + 1
    costs  = vigra.readHDF5(costs_path, 'data')
    assert len(costs) == len(uv_ids)
    return uv_ids.max() + 1, uv_ids, costs


def read_lifted(model_path_dict):
    uvs_local = vigra.readHDF5(model_path_dict['local_uvs'], 'data')
    uvs_lifted = vigra.readHDF5(model_path_dict['lifted_uvs'], 'data')
    n_nodes   = uvs_local.max() + 1
    assert uvs_lifted.max() + 1 == n_nodes

    # build the graph with local edges
    graph = nifty.graph.UndirectedGraph(n_nodes)
    graph.insertEdges(uvs_local)

    # build the lifted objective, insert local and lifted costs
    lifted_obj = nifty.graph.lifted_multicut.liftedMulticutObjective(graph)
    costs_local  = vigra.readHDF5(model_path_dict['local_costs'])
    assert len(costs_local) == len(uvs_local)
    costs_lifted = vigra.readHDF5(model_path_dict['lifted_costs'])
    assert len(costs_lifted) == len(uvs_lifted)
    lifted_obj.setCosts(uvs_local, costs_local)
    lifted_obj.setCosts(uvs_lifted, costs_lifted)

    return lifted_obj
