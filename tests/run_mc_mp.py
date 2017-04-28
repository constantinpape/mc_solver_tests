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
    print "Message-Passing Multicut:"
    print "primal: %f, t-inf: %f" % (e_mcmp, t_mcmp)
    #print "Opengm: primal: %f, t-inf: %f" % (e_fm_opengm, t_fm_opengm)


def check_python_vs_cmdln(sample):
    pass



if __name__ == '__main__':
    for sample in ('sampleA', 'sampleB', 'sampleC'):
        compare_opengm_nifty(sample)
