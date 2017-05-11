import os
from functools import partial
import sys
sys.path.append('..')
from utils import *

# compare the main algorithms in nifty on the small samples
def small_problems():

    def run_sample(sample, timeout = None, verbose = False):
        uv_path, costs_path = model_paths_new[sample]
        n_var, uv_ids, costs = read_from_mcppl(uv_path, costs_path)
        obj = nifty_mc_objective(n_var, uv_ids, costs)

        solver_dict = {
            'fm-ilp' : nifty_fusion_move_factory(obj,
                backend_factory = nifty_ilp_factory(obj),
                seed_fraction = 0.01),
            'ilp' : nifty_ilp_factory(obj),
            'cgc' : nifty_cgc_factory(obj),
            'kl'  : nifty_kl_factory(obj),
            'mp'  : nifty_mp_factory(obj)
        }

        res_dict = {}
        for solver in solver_dict:
            print "Run - nifty solver:", solver
            res_dict[solver] = run_nifty_solver(obj, solver_dict[solver], time_limit = timeout, verbose = verbose)
        return res_dict

    res_dict = {}
    #samples = ('sampleA','sampleB','sampleC')
    samples = ('sampleA',)
    for sample in samples:
        res_dict[sample] = run_sample(sample)

    for sample in samples:
        res = res_dict[sample]
        print "Summary for %s:" % sample
        for solver_name, solver_res in res.iteritems():
            print "%s : primal: %f, t-inf: %f" % (solver_name, solver_res[1], solver_res[2])

def sampleD_problems():

    def _run(size, solver):
        n_var, uv_ids, costs = read_from_mcluigi(
                model_paths_mcluigi['sampleD_%s' % size])
        _, energy, runtime = solver(n_var, uv_ids, costs)
        return energy, runtime

    timeout = 1800
    solver_dict = {
            'fm' : partial(run_fusion_moves_nifty, n_threads = 20, verbose = True),
            'mp' : partial(run_mp_nifty, timeout = 1800, n_threads = 20, max_iter = long(1e5)),
            'mp-fmkl' : partial(run_mp_nifty, timeout = 1800, n_threads = 20, n_threads_fuse = 20, seed_fraction_fuse = 0.01, mp_primal_rounder = 'fm-kl', max_iter = long(1e5)),
            'ilp' : partial(run_ilp_nifty, verbose = True, timeout = 1800)
            }

    res_dict = {}
    samples = ('medium',)#'large')
    for size in samples:
        for key, solver in solver_dict.iteritems():
            print "Run for size %s  with solver %s" % (size, key)
            res_dict[(size, key)] = _run(size, solver)

    print "Sample D problem summary:"
    for size in samples:
        print "Problem size: %s" % size
        for key in solver_dict:
            e,t  = res_dict[(size, key)]
            print "Solver: %s" % key
            print "Energy: %f" % e
            print "Runtime: %f" % t


if __name__ == '__main__':
    small_problems()
    #sampleD_problems()
    #for sample in ('sampleA', 'sampleB', 'sampleC'):
    #    compare_opengm_nifty(sample)
