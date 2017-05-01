import os
from functools import partial
import sys
sys.path.append('..')
from utils import *
from model_paths import model_paths_new, model_paths_mcluigi

def compare_opengm_nifty(sample):

    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    # run fusionmoves
    print "Run nifty fm"
    _, e_fm_nifty, t_fm_nifty = run_fusion_moves_nifty(n_var, uv_ids, costs)
    print "Run opengm fm"
    _, e_fm_opengm, t_fm_opengm = run_fusion_moves_opengm(n_var, uv_ids, costs)

    # run ilps
    print "Run nifty ilp"
    _, e_ilp_nifty,  t_ilp_nifty  = run_ilp_nifty(n_var, uv_ids, costs)
    print "Run opengm ilp"
    _, e_ilp_opengm, t_ilp_opengm = run_ilp_opengm(n_var, uv_ids, costs)

    print
    print "Summary for %s:" % sample
    print "Fusionmoves:"
    print "Nifty: primal: %f, t-inf: %f" % (e_fm_nifty, t_fm_nifty)
    print "Opengm: primal: %f, t-inf: %f" % (e_fm_opengm, t_fm_opengm)
    print "Ilp:"
    print "Nifty: primal: %f, t-inf: %f"  % (e_ilp_nifty,  t_ilp_nifty)
    print "Opengm: primal: %f, t-inf: %f" % (e_ilp_opengm, t_ilp_opengm)
    print


def sampleD_problems():

    def _run(size, solver):
        n_var, uv_ids, costs = read_from_mcluigi(
                model_paths_mcluigi['sampleD_%s' % size])
        _, energy, runtime = solver(n_var, uv_ids, costs)
        return energy, runtime

    solver_dict = {
            'fm' : run_fusion_moves_nifty,
            'mcmp' : partial(run_mc_mp_pybindings, max_iter = 5000)
            }

    res_dict = {}
    for size in ('medium', 'large'):
        for key, solver in solver_dict.iteritems():
            print "Run for size %s  with solver %s" % (size, key)
            res_dict[(size, key)] = _run(size, solver)

    print "Sample D problem summary:"
    for size in ('medium', 'large'):
        print "Problem size: %s" % size
        for key in solver_dict:
            e,t  = res_dit[(size, key)]
            print "Solver: %s" % key
            print "Energy: %f" % e
            print "Runtime: %f" % t



def nifty_mp_tests(sample):

    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    # FIXME this is not working multi-threaded yet, maybe due to the async call in LP_MP ?!
    print "Run nifty fm-mp"
    _, e_fm_nifty, t_fm_nifty = run_fusion_moves_nifty(n_var, uv_ids, costs, backend = 'mp', n_threads = 1)
    print "Run nifty mp"
    _, e_mp_nifty, t_mp_nifty = run_mp_nifty(n_var, uv_ids, costs)
    print "Run LP_MP mp"
    _, e_mp_lpmp, t_mp_lpmp = run_mc_mp_pybindings(n_var, uv_ids, costs)

    print
    print "Summary for %s:" % sample
    print "Message passing multicut:"
    print "Nifty-fm mp: primal: %f, t-inf: %f" % (e_fm_nifty, t_fm_nifty)
    print "Nifty: primal: %f, t-inf: %f" % (e_mp_nifty, t_mp_nifty)
    print "LP_MP: primal: %f, t-inf: %f" % (e_mp_lpmp, t_mp_lpmp)
    print


if __name__ == '__main__':
    nifty_mp_tests('sampleA')
    #sampleD_problems()
    #for sample in ('sampleA', 'sampleB', 'sampleC'):
    #    compare_opengm_nifty(sample)
