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

    return e_mcmp, t_mcmp


# compare all mcmp implementations / instantiations
def compare_all_mcmp():

    def _run(sample):
        paths = model_paths_new[sample]
        n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

        #print "Run nifty mp"
        #_, e_mp_nifty, t_mp_nifty = run_mp_nifty(n_var, uv_ids, costs)

        print "Run LP_MP mp with pythonbindigns"
        _, e_mp_lpmp_py, t_mp_lpmp_py = run_mc_mp_pybindings(n_var, uv_ids, costs)

        #print "Run LP_MP mp from commandline"
        #_, e_mp_lpmp_cmd, t_mp_lpmp_cmd = run_mc_mp_cmdline(n_var, uv_ids, costs)

        return e_mp_lpmp_py, t_mp_lpmp_py, e_mp_lpmp_cmd, t_mp_lpmp_cmd
        #return e_mp_nifty, t_mp_nifty, e_mp_lpmp_cmd, t_mp_lpmp_cmd

    #samples = ('sampleA', 'sampleB', 'sampleC')
    samples = ('sampleA',)

    res_dict = {}
    for sample in samples:
        res_dict[sample] = _run(sample)

    for sample in samples:
        #e_nifty, t_nifty, e_py, t_py, e_cmd, t_cmd = res_dict[sample]
        e_py, t_py, e_cmd, t_cmd = res_dict[sample]
        print
        print "Summary for %s:" % sample
        print "Message passing multicut:"
        #print "Nifty mp     : primal: %f, t-inf: %f" % (e_nifty, t_nifty)
        print "Pybindings mp: primal: %f, t-inf: %f" % (e_py, t_py)
        print "Commandline  : primal: %f, t-inf: %f" % (e_cmd, t_cmd)
        print



if __name__ == '__main__':
    compare_all_mcmp()
