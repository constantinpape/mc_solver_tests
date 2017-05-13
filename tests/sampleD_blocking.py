import nifty
import time
import numpy as np
import sys
sys.path.append('..')
from utils import nifty_mc_objective, nifty_ilp_factory, nifty_mp_factory, nifty_kl_factory, run_nifty_solver
from utils import read_from_mcluigi, read_nodes, model_paths_mcluigi

models = ['sampleD_full', 'sampleD_L1', 'sampleD_L2', 'sampleD_L3', 'sampleD_L4']

time_offsets_mc    = np.array([0, 1484.5, 298.3, 349.2, 1035.2])
time_offsets_merge = np.array([0, 3286.5, 356.6, 255.1, 198.2])
t_offsets          = np.cumsum(time_offsets_mc + time_offsets_merge)[::-1]


def run_sample_d(model, time_limit, time_offset, global_obj = None):
    n_var, uv_ids, costs = read_from_mcluigi(model_paths_mcluigi[model])
    obj = nifty_mc_objective(n_var, uv_ids, costs)

    # TODO select solver

    t_inf  = time.time()
    node_res = run_nifty_solver(obj, factory, verbose = True, time_limit = time_limit + time_offset )
    t_inf = time.time() - t_inf

    if global_obj is not None:
        to_global_nodes = read_nodes(model_paths_mcluigi[model], dtype = 'uint32')
        global_res = np.zeros(global_obj.graph.numberOfNodes)
        for node_id, cluster_id in enumerate(node_res):
            global_res[to_global_nodes[node_id]] = cluster_id

        return global_obj.evalNodeLabels(gloabl_res), t_inf
    else:
        return obj.evalNodeLabels(node_res), t_inf


def test_full(time_limit):
    t_off = t_offsets[0]
    e_full, t_full = run_sample_d(models[0], time_limit, t_off)


def test_blocking():
    pass


if __name__ == '__main__':
    # 5 hour time limit
    time_limit = 5 * 3600
    #run_sample_d()
