import nifty
import numpy as np
import sys
sys.path.append('..')
from utils import nifty_mc_objective, nifty_ilp_factory, nifty_mp_factory, nifty_kl_factory, run_nifty_solver
from utils import read_from_mcluigi, read_nodes, model_paths_mcluigi

models = ['sampleD_full', 'sampleD_L1', 'sampleD_L2', 'sampleD_L3', 'sampleD_L4']


def run_sample_d(model, time_limit, time_offset, global_obj = None):
    n_var, uv_ids, costs = read_from_mcluigi(model_paths_mcluigi[model])
    obj = nifty_mc_objective(n_var, uv_ids, costs)

    # TODO select solver

    node_res = run_nifty_solver(obj, factory, verbose = True, time_limit = time_limit + time_offset )

    if global_obj is not None:
        to_global_nodes = read_nodes(model_paths_mcluigi[model], dtype = 'uint32')
        global_res = np.zeros(global_obj.graph.numberOfNodes)
        for node_id, cluster_id in enumerate(node_res):
            global_res[to_global_nodes[node_id]] = cluster_id

        return global_obj.evalNodeLabels(gloabl_res)
    else:
        return obj.evalNodeLabels(node_res)

if __name__ == '__main__':
    run_sample_d()
