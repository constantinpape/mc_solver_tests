# import os
# import cPickle as pickle
# from functools import partial
import sys
sys.path.append('..')
from utils import *


# compare the main algorithms in nifty on the small samples
def small_problems():

    def run_sample(sample, solver_choice, timeout=None, verbose=False):
        uv_path, costs_path = model_paths_new[sample]
        n_var, uv_ids, costs = read_from_mcppl(uv_path, costs_path)
        obj = nifty_mc_objective(n_var, uv_ids, costs)

        solver_dict = {
            'fm-ilp': nifty_fusion_move_factory(obj,
                backend_factory = nifty_ilp_factory(obj),
                seed_fraction = 0.01),
            'fm-kl': nifty_fusion_move_factory(obj,
                backend_factory = nifty_kl_factory(obj),
                seed_fraction = 0.01),
            'fm-cgc': nifty_fusion_move_factory(obj,
                backend_factory = nifty_cgc_factory(obj),
                seed_fraction = 0.01),
            'ilp' : nifty_ilp_factory(obj),
            'cgc' : nifty_cgc_factory(obj), # FIXME does not converge!
            'kl'  : nifty_kl_factory(obj),
            'mp'  : nifty_mp_factory(obj, number_of_iterations = 500, n_threads = 20),
            'mp-fmkl' : nifty_mp_factory(obj,
                n_threads = 20,
                number_of_iterations = 500,
                backend_factory = nifty_fusion_move_factory(
                    obj,
                    backend_factory = nifty_kl_factory(obj),
                    seed_fraction = 0.05,
                    number_of_iterations = 500,
                    n_stop = 8,
                    n_threads = 20
                )
            ),
        }

        res_dict = {}
        for solver in solver_choice:
            print "Run - nifty solver:", solver
            res_dict[solver] = run_nifty_solver(obj, solver_dict[solver], time_limit = timeout, verbose = verbose)
        return res_dict

    samples = ('sampleA','sampleB','sampleC')
    #samples = ('sampleA',)
    solver_choice = ('fm-ilp', 'fm-kl', 'fm-greedy')

    res_dict = {}
    for sample in samples:
        res_dict[sample] = run_sample(sample, solver_choice)

    for sample in samples:
        print sample
        res = res_dict[sample]
        print "Summary for %s:" % sample
        for solver_name, solver_res in res.iteritems():
            print "%s : primal: %f, t-inf: %f" % (solver_name, solver_res[1], solver_res[2])




def sampleD_problems():

    def run_sample(sample, solver_choice, timeout = None, verbose = False):
        model_path = model_paths_mcluigi[sample]
        n_var, uv_ids, costs = read_from_mcluigi(model_path)
        obj = nifty_mc_objective(n_var, uv_ids, costs)

        pgen_type = 'ws'
        kl_ws     = True

        solver_dict = {
            'greedy' : nifty_greedy_factory(obj),
            'fm-greedy' : nifty_fusion_move_factory(obj,
                n_threads = 20,
                backend_factory = nifty_greedy_factory(obj),
                seed_fraction = 0.01,
                pgen_type = pgen_type,
                kl_chain = kl_ws,
                n_fuse = 1,
                parallel_per_thread = 1,
                number_of_iterations = 40,
                n_stop = 4
                ),
            #'fm-ilp' : nifty_fusion_move_factory(obj,
            #    backend_factory = nifty_ilp_factory(obj),
            #    pgen_type = pgen_type,
            #    seed_fraction = 0.001,
            #    kl_Chain = kl_ws
                #),
            'fm-kl' : nifty_fusion_move_factory(obj,
                backend_factory = nifty_kl_factory(obj),
                pgen_type = pgen_type,
                seed_fraction = 0.01,
                kl_chain = kl_ws
                ),
            'fm-cgc' : nifty_fusion_move_factory(obj,
                backend_factory = nifty_cgc_factory(obj),
                seed_fraction = 0.01,
                kl_chain = True),
            'ilp' : nifty_ilp_factory(obj),
            'cgc' : nifty_cgc_factory(obj),
            'kl'  : nifty_kl_factory(obj),
            'mp'  : nifty_mp_factory(
                obj,
                number_of_iterations = 100000,
                n_threads = 20,
                timeout = int(timeout)
            ),
            'mp-fmkl' : nifty_mp_factory(
                obj,
                number_of_iterations = 100000,
                n_threads = 20,
                timeout = int(timeout),
                backend_factory = nifty_fusion_move_factory(
                    obj,
                    n_threads = 20,
                    backend_factory = nifty_kl_factory(obj),
                    seed_fraction = 0.005,
                    number_of_iterations = 20,
                    n_stop = 4
                )
            ),
            'mp-fmgreedy' : nifty_mp_factory(
                obj,
                number_of_iterations = 100000,
                n_threads = 20,
                timeout = int(timeout),
                backend_factory = nifty_fusion_move_factory(
                    obj,
                    n_threads = 20,
                    backend_factory = nifty_greedy_factory(obj),
                    seed_fraction = 0.01,
                    number_of_iterations = 25,
                    n_stop = 3,
                    kl_chain = True,
                    n_fuse = 1,
                    parallel_per_thread = 1
                )
            ),
        }

        res_dict = {}
        for solver in solver_choice:
            print "Run - nifty solver:", solver
            res_dict[solver] = run_nifty_solver(obj, solver_dict[solver], time_limit = timeout, verbose = verbose)
        return res_dict

    timeout = 3600.
    samples = ('sampleD_sub_L1',) #'sampleD_sub_full')
    #solver_choice = ('kl','fm-ilp','fm-kl','ilp','mp','mp-fmkl')
    solver_choice = ('cgc', 'fm-cgc')

    res_dict = {}
    for sample in samples:
        print sample
        res_dict[sample] = run_sample(sample, solver_choice, timeout)
        #with open('./anytime_data/sampleD/save_%s.pkl' % sample, 'w') as f:
        #    pickle.dump(res_dict[sample], f)

    for sample in samples:
        print "%s summary:" % sample
        for solver_name, solver_res in res_dict[sample].iteritems():
            print "%s : Energy %f, Runtime %f" % (solver_name, solver_res[1], solver_res[2])


if __name__ == '__main__':
    small_problems()
    # sampleD_problems()
    # for sample in ('sampleA', 'sampleB', 'sampleC'):
    #     compare_opengm_nifty(sample)
