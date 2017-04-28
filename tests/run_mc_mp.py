import os
import sys
sys.path.append('..')
from utils import *
from model_paths import model_paths_new

def run_mc_mp(sample):

    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    # run mc mp
    print "Run mc mp"
    _, e_mcmp, t_mcmp = run_mc_mp_pybindings(n_var, uv_ids, costs)
    # TODO run commandline mcmp for sanity check

    print
    print "Summary for %s:" % sample
    print "Fusionmoves:"
    print "Nifty: primal: %f, t-inf: %f" % (e_fm_nifty, t_fm_nifty)
    print "Opengm: primal: %f, t-inf: %f" % (e_fm_opengm, t_fm_opengm)
    print "Ilp:"
    print "Nifty: primal: %f, t-inf: %f"  % (e_ilp_nifty,  t_ilp_nifty)
    print "Opengm: primal: %f, t-inf: %f" % (e_ilp_opengm, t_ilp_opengm)
    print



if __name__ == '__main__':
    for sample in ('sampleA', 'sampleB', 'sampleC'):
        compare_opengm_nifty(sample)
