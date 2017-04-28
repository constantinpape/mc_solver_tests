import os
import sys
sys.path.append('..')
from utils import *
from model_paths import model_paths_new

def compare_opengm_nifty(sample):

    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    # run fusionmoves
    print "Run nifty fm"
    _, e_fm_nifty, t_fm_nifty = run_fusion_moves_nifty(n_var, uv_ids, costs)
    #print "Run opengm fm"
    #_, e_fm_opengm, t_fm_opengm = run_fusion_moves_opengm(n_var, uv_ids, costs)

    # run ilps
    print "Run nifty ilp"
    _, e_ilp_nifty,  t_ilp_nifty  = run_ilp_nifty(n_var, uv_ids, costs)
    print "Run opengm ilp"
    #_, e_ilp_opengm, t_ilp_opengm = run_ilp_opengm(n_var, uv_ids, costs)

    print
    print "Summary for %s:" % sample
    print "Fusionmoves:"
    print "Nifty: primal: %f, t-inf: %f" % (e_fm_nifty, t_fm_nifty)
    #print "Opengm: primal: %f, t-inf: %f" % (e_fm_opengm, t_fm_opengm)
    print "Ilp:"
    print "Nifty: primal: %f, t-inf: %f"  % (e_ilp_nifty,  t_ilp_nifty)
    #print "Opengm: primal: %f, t-inf: %f" % (e_ilp_opengm, t_ilp_opengm)
    print



if __name__ == '__main__':
    for sample in ('sampleA', 'sampleB', 'sampleC'):
        compare_opengm_nifty(sample)
