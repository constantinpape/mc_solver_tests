import nifty
import time
import numpy as np
import sys
sys.path.append('..')
from utils import nifty_mc_objective, nifty_ilp_factory, nifty_mp_factory, nifty_kl_factory, run_nifty_solver, nifty_fusion_move_factory
from utils import read_from_mcluigi, read_nodes, model_paths_mcluigi

models = ['sampleD_full', 'sampleD_L1', 'sampleD_L2', 'sampleD_L3', 'sampleD_L4']

time_offsets_mc    = np.array([0, 1484.5, 298.3, 349.2, 1035.2])
time_offsets_merge = np.array([0, 3286.5, 356.6, 255.1, 198.2])
t_offsets          = np.cumsum(time_offsets_mc + time_offsets_merge)
print t_offsets


def run_sample_d(model, time_limit, time_offset, seed_fraction, chain_kl = True, global_obj = None):
    n_var, uv_ids, costs = read_from_mcluigi(model_paths_mcluigi[model])
    obj = nifty_mc_objective(n_var, uv_ids, costs)

    #
    factory = nifty_fusion_move_factory(obj,
            backend_factory = nifty_kl_factory(obj),
            kl_chain = chain_kl,
            seed_fraction = seed_fraction)

    t_inf  = time.time()
    node_res = run_nifty_solver(obj, factory, verbose = True, time_limit = time_limit - time_offset )
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
    e_full, t_full = run_sample_d(models[0], time_limit, t_off, 1e-6, chain_kl = False)
    print "Results for full model:"
    print "Energy:", e_full
    print "Runtume", t_full


def test_blocking(time_limit, level):
    model = models[level]
    t_off = t_offsets[level]

    n_var, uv_ids, costs = read_from_mcluigi(model_paths_mcluigi[0])
    global_obj = nifty_mc_objective(n_var, uv_ids, costs)

    e_l, t_l = run_sample_d(model, time_limit, t_off, 1e-4, chain_kl = True, global_obj = global_obj)

    print "Results for level %i:" % level
    print "Energy:", e_l
    print "Runtume", t_l



if __name__ == '__main__':
    # 8 hour time limit
    time_limit = 8 * 3600
    test_full(time_limit)
