import os
import numpy as np
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


def test_nifty_mp_settings():
    pass


# compare all mcmp implementations / instantiations
def compare_all_mcmp():

    def _run(sample, N = 1):
        paths = model_paths_new[sample]
        n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

        e_lpmp_py_list = []
        t_lpmp_py_list = []
        e_lpmp_nifty_list = []
        t_lpmp_nifty_list = []
        e_fmmp_list = []
        t_fmmp_list = []
        for _ in range(N):

            # save fm result for comparison
            print "Run fusion moves nifty with mp backend"
            nodes_fm, e_fm, t_fm = run_fusion_moves_mp(n_var, uv_ids, costs, n_threads = 1)
            e_fmmp_list.append(e_fm)
            t_fmmp_list.append(t_fm)
            #project(sample, nodes_fm, './segmentations/nifty_fm_%s.h5' % sample)

            print "Run nifty mp"
            nodes_mp_nifty, e_lpmp_nifty, t_lpmp_nifty = run_mp_nifty(n_var, uv_ids, costs, max_iter = 200)
            e_lpmp_nifty_list.append(e_lpmp_nifty)
            t_lpmp_nifty_list.append(t_lpmp_nifty)
            #project(sample, nodes_mp_nifty, './segmentations/nifty_mp_%s.h5' % sample)

            #print "Run LP_MP mp with pythonbindigns"
            #nodes_lpmp_py, e_lpmp_py, t_lpmp_py = run_mc_mp_pybindings(n_var, uv_ids, costs, max_iter = 200)
            #e_lpmp_py_list.append(e_lpmp_py)
            #t_lpmp_py_list.append(t_lpmp_py)
            #project(sample, nodes_lpmp_py, './segmentations/lpmp_py_%s.h5' % sample)

            #print "Run LP_MP mp from commandline"
            #_, e_lpmp_cmd, t_lpmp_cmd = run_mc_mp_cmdline(n_var, uv_ids, costs)
            #e_lpmp_cmd_list.append(e_lpmp_cmd)
            #t_lpmp_cmd_list.append(t_lpmp_cmd)

        return e_lpmp_py_list, t_lpmp_py_list, e_lpmp_nifty_list, t_lpmp_nifty_list, e_fmmp_list, t_fmmp_list

    #samples = ('sampleA', 'sampleB', 'sampleC')
    samples = ('sampleA',)

    N = 1
    res_dict = {}
    for sample in samples:
        res_dict[sample] = _run(sample, N)

    for sample in samples:
        e_py, t_py, e_nifty, t_nifty, e_fm, t_fm = res_dict[sample]
        print
        print "Summary for %s:" % sample
        print "Message passing multicut:"
        #print "Nifty mp     : primal: %f, t-inf: %f" % (e_nifty, t_nifty)
        #print "Pybindings mp: primal: %f +- %f, t-inf: %f +- %f" % (np.mean(e_py), np.std(e_py), np.mean(t_py), np.std(t_py))
        print "Nifty mp     : primal: %f +- %f, t-inf: %f +- %f" % (np.mean(e_nifty), np.std(e_nifty), np.mean(t_nifty), np.std(t_nifty))
        print "Nifty fmmp   : primal: %f +- %f, t-inf: %f +- %f" % (np.mean(e_fm), np.std(e_fm), np.mean(t_fm), np.std(t_fm))
        print



if __name__ == '__main__':
    compare_all_mcmp()
