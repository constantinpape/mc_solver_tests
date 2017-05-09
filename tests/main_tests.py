import os
from functools import partial
import sys
sys.path.append('..')
from utils import *
from model_paths import model_paths_new, model_paths_mcluigi


def test_nifty_kl(sample):
    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    #print "Run nifty fm"
    #nodes_fm, e_fm_nifty, t_fm_nifty = run_fusion_moves_nifty(n_var, uv_ids, costs)
    #project(sample, nodes_fm, './segmentations/nifty_fm_%s.h5' % sample)

    #print "Run nifty kl"
    nodes_kl, e_kl_nifty, t_kl_nifty = run_kl_nifty(n_var, uv_ids, costs)
    #project(sample, nodes_kl, './segmentations/nifty_kl_%s.h5' % sample)

    print "Summary for %s:" % sample
    #print "FM: primal: %f, t-inf: %f" % (e_fm_nifty, t_fm_nifty)
    print "KL: primal: %f, t-inf: %f" % (e_kl_nifty, t_kl_nifty)



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


# compare the main algorithms in nifty on the small samples
def compare_nifty_algos(sample):

    def _run(sample):

        # FIXME this is not working multi-threaded yet, maybe due to the async call in LP_MP ?!
        print "Run nifty fm-mp"
        _, e_fmmp, t_fmmp = run_fusion_moves_nifty(n_var, uv_ids, costs, backend = 'mp', n_threads = 1)

        print "Run nifty fm-ilp"
        _, e_fmilp, t_fmilp = run_fusion_moves_nifty(n_var, uv_ids, costs, backend = 'ilp', n_threads = 20)

        print "Run nifty ilp"
        _, e_ilp, t_ilp = run_fusion_moves_nifty(n_var, uv_ids, costs, backend = 'ilp', n_threads = 20)

        print "Run nifty mp"
        _, e_mp, t_mp = run_mp_nifty(n_var, uv_ids, costs)

        return e_fmmp, t_fmmp, e_fmilp, t_fmilp, e_ilp, t_ilp, e_mp, t_mp


    samples = ('sampleA', 'sampleB', 'sampleC')

    res_dict = {}
    for sample in samples:
        res_dict[sample] = _run(sample)

    for sample in ('sampleA', 'sampleB', 'sampleC'):
        e_fmmp, t_fmmp, e_fmilp, t_fmilp, e_ilp, t_ilp, e_mp, t_mp = res_dict[sample]
        print
        print "Summary for %s:" % sample
        print "FM MP : primal: %f, t-inf: %f" % (e_fmmp, t_fmmp)
        print "FM IlP: primal: %f, t-inf: %f" % (e_fmilp, t_fmilp)
        print "Ilp   : primal: %f, t-inf: %f" % (e_ilp, t_ilp)
        print "Mp    : primal: %f, t-inf: %f" % (e_mp, t_mp)
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
            e,t  = res_dict[(size, key)]
            print "Solver: %s" % key
            print "Energy: %f" % e
            print "Runtime: %f" % t


if __name__ == '__main__':
    test_nifty_kl('sampleA')
    #sampleD_problems()
    #for sample in ('sampleA', 'sampleB', 'sampleC'):
    #    compare_opengm_nifty(sample)
